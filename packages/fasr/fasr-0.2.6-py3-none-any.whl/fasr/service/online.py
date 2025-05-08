from asyncio import Queue
from pathlib import Path
import asyncio
import traceback
from urllib.parse import parse_qs
from typing import Literal, Iterable, List

from loguru import logger
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel, Field, ConfigDict

from fasr.config import registry
from fasr.data import AudioBytesStream, AudioSpan, AudioChunk
from fasr.models.stream_asr.base import StreamASRModel
from fasr.models.stream_vad.stream_fsmn import FSMNForStreamVADOnnx
from .schema import AudioChunkResponse, TranscriptionResponse


class RealtimeASRService(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="ignore"
    )

    host: str = Field("127.0.0.1", description="服务地址")
    port: int = Field(27000, description="服务端口")
    device: Literal["cpu", "cuda", "mps"] = Field("cpu", description="设备")
    asr_model_name: Literal["stream_sensevoice", "stream_paraformer"] = Field(
        "stream_paraformer", description="流式asr模型"
    )
    asr_checkpoint_dir: str | Path | None = Field(
        None,
        description="asr模型路径",
    )
    asr_model: StreamASRModel = Field(None, description="asr模型")
    vad_model: FSMNForStreamVADOnnx = Field(None, description="vad模型")
    vad_chunk_size_ms: int = Field(100, description="音频分片大小")
    vad_end_silence_ms: int = Field(500, description="vad判定音频片段结束最大静音时间")
    sample_rate: int = Field(16000, description="音频采样率")
    bit_depth: int = Field(16, description="音频位深")
    channels: int = Field(1, description="音频通道数")

    def setup(self):
        app = FastAPI()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logger.info(
            f"Start online ASR Service on {self.host}:{self.port}, device: {self.device}"
        )

        self.asr_model = registry.stream_asr_models.get(self.asr_model_name)()
        self.asr_model.from_checkpoint(
            checkpoint_dir=self.asr_checkpoint_dir,
            device=self.device,
        )

        self.vad_model = FSMNForStreamVADOnnx(
            chunk_size_ms=self.vad_chunk_size_ms,
            max_end_silence_time=self.vad_end_silence_ms,
        ).from_checkpoint()

        @app.websocket("/asr/realtime")
        async def transcribe(ws: WebSocket):
            try:
                # 解析请求参数
                await ws.accept()
                query_params = parse_qs(ws.scope["query_string"].decode())
                itn = query_params.get("itn", ["false"])[0].lower() == "true"
                model = query_params.get("model", ["paraformer"])[0].lower()
                chunk_size = int(self.vad_chunk_size_ms * self.sample_rate / 1000)
                logger.info(f"itn: {itn}, chunk_size: {chunk_size}, model: {model}")
                queue = Queue()
                tasks = []
                tasks.append(asyncio.create_task(self.vad_task(ws, span_queue=queue)))
                tasks.append(
                    asyncio.create_task(self.asr_task(ws=ws, span_queue=queue))
                )
                await asyncio.gather(
                    *tasks,
                )
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected")
            except Exception as e:
                logger.error(
                    f"Unexpected error: {e}\nCall stack:\n{traceback.format_exc()}"
                )
                await ws.close()
            finally:
                logger.info("Cleaned up resources after WebSocket disconnect")

        uvicorn.run(app, host=self.host, port=self.port, ws="wsproto")

    async def vad_task(self, ws: WebSocket, span_queue: Queue):
        bytes_buffer = AudioBytesStream(
            sample_rate=self.sample_rate, chunk_size_ms=self.vad_chunk_size_ms
        )
        cache: dict = {}
        while True:
            try:
                raw_data = await ws.receive()
            except Exception as e:
                logger.error(f"Error receiving data: {e}")
                break
            bytes_data = raw_data.get("bytes", None)
            chunks: List[AudioChunk] = bytes_buffer.push(bytes_data)
            for chunk in chunks:
                spans: Iterable[AudioSpan] = self.vad_model.detect_chunk(
                    waveform=chunk.waveform,
                    state=cache,
                    is_last=chunk.is_last,
                )
                for span in spans:
                    if span.vad_state != "segment_mid":
                        await self.send_response("", ws, span.vad_state)
                        logger.info(f"vad state: {span.vad_state}")
                    await span_queue.put(span)

    async def asr_task(self, span_queue: Queue, ws: WebSocket):
        cache = {}
        while True:
            span: AudioSpan = await span_queue.get()
            is_last = span.vad_state == "segment_end"
            if is_last:
                final_text = ""
                for span in self.asr_model.transcribe_chunk(
                    waveform=span.waveform, is_last=True, state=cache
                ):
                    final_text += span.text

                await self.send_response(final_text, ws, "final_transcript")
                logger.info(f"asr state: final_transcript, text: {final_text}")
                cache = {}
            else:
                for span in self.asr_model.transcribe_chunk(
                    waveform=span.waveform, is_last=False, state=cache
                ):
                    await self.send_response(span.text, ws, "interim_transcript")
                    logger.info(f"asr state: interim_transcript, text: {span.text}")
            span_queue.task_done()

    async def send_response(self, text: str, ws: WebSocket, state: str):
        response = TranscriptionResponse(
            data=AudioChunkResponse(text=text, state=state)
        )
        await ws.send_json(response.model_dump())
