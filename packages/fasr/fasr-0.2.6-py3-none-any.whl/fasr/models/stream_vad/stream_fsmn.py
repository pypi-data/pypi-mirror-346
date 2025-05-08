import time
from typing_extensions import Self
from typing import Dict, Iterable
from pathlib import Path

from .base import StreamVADModel
from funasr import AutoModel
from funasr_onnx import Fsmn_vad_online
from fasr.config import registry
from fasr.data import Waveform, AudioSpan
import numpy as np


DEFAULT_CHECKPOINT_DIR = Path(__file__).parent.parent.parent / "asset" / "fsmn-vad"


@registry.stream_vad_models.register("stream_fsmn.torch")
class FSMNForStreamVAD(StreamVADModel):
    fsmn: AutoModel | None = None
    chunk_size_ms: int = 100
    sample_rate: int = 16000
    max_end_silence_time: int = 200

    def detect_chunk(
        self,
        waveform: Waveform,
        state: Dict,
        is_last: bool,
    ) -> Iterable[AudioSpan]:
        """Detect voice activity in the given chunk of waveform.

        Args:
            waveform (Waveform): The chunk of waveform to detect voice activity in.
            is_last (bool): Indicates if the chunk is the last chunk of the audio.
            state (Dict): The state of the model, which includes buffer, cache, offset, is_detected, and audio_waveform.

        Notes:
            - The function processes the waveform in chunks of size `self.chunk_size`.
            - If the sample rate of the input waveform does not match `self.sample_rate`, it will be resampled.
            - The function maintains a buffer to handle waveform chunks and updates the state accordingly.
            - Voice activity detection is performed using the FSMN model, and detected segments are yielded as AudioSpan objects.
            - If `is_last` is True and there is remaining data in the buffer, it processes the final chunk.

        Yields:
            AudioSpan: Detected voice activity spans, each represented as an AudioSpan object.
        """
        if waveform.sample_rate != self.sample_rate:
            waveform = waveform.resample(self.sample_rate)
        buffer: Waveform = state.get(
            "buffer",
            Waveform(data=np.array([], dtype=np.float32), sample_rate=self.sample_rate),
        )
        buffer = buffer.append(waveform)
        audio_waveform: Waveform = state.get(
            "audio_waveform",
            Waveform(data=np.array([], dtype=np.float32), sample_rate=self.sample_rate),
        )
        audio_waveform = audio_waveform.append(waveform=waveform)
        cache = state.get("cache", {})
        offset = state.get("offset", 0)
        is_detected = state.get("is_detected", False)
        while len(buffer) >= self.chunk_size:
            chunk_waveform = buffer[: self.chunk_size]
            buffer = buffer[self.chunk_size :]
            data = chunk_waveform.data
            sample_rate = chunk_waveform.sample_rate
            start = time.perf_counter()
            segments = self.fsmn.generate(
                input=data,
                fs=sample_rate,
                chunk_size=self.chunk_size_ms,
                is_final=is_last,
                cache=cache,
            )[0]["value"]
            end = time.perf_counter()
            if len(segments) > 0:
                for segment in segments:
                    start, end = segment
                    if start != -1 and end == -1:
                        is_detected = True
                        start_idx = start * sample_rate // 1000
                        end_idx = len(data) + offset
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            vad_state="segment_start",
                        )

                    if start == -1 and end != -1:
                        is_detected = False
                        start_idx = offset
                        end_idx = end * sample_rate // 1000
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            vad_state="segment_end",
                        )

                    if start != -1 and end != -1:
                        is_detected = False
                        start_idx = start * sample_rate // 1000
                        end_idx = end * sample_rate // 1000
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            vad_state="segment_mid",
                        )
            else:
                if is_detected:
                    yield AudioSpan(
                        start_ms=-1,
                        end_ms=-1,
                        waveform=waveform,
                        sample_rate=sample_rate,
                        vad_state="segment_mid",
                    )

            offset += len(data)

        if is_last and 0 < len(buffer) < self.chunk_size:
            chunk_waveform = buffer
            buffer = Waveform(data=np.array([]), sample_rate=self.sample_rate)
            data = chunk_waveform.data
            sample_rate = chunk_waveform.sample_rate
            segments = self.fsmn.generate(
                input=data,
                fs=sample_rate,
                is_final=True,
                cache=cache,
            )[0]["value"]

            if len(segments) > 0:
                for segment in segments:
                    start, end = segment
                    if start != -1 and end == -1:
                        is_detected = True
                        start_idx = start * sample_rate // 1000
                        end_idx = len(data) + offset
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            vad_state="segment_start",
                        )

                    if start == -1 and end != -1:
                        is_detected = False
                        start_idx = offset
                        end_idx = end * sample_rate // 1000
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            vad_state="segment_end",
                        )

                    if start != -1 and end != -1:
                        is_detected = False
                        start_idx = start * sample_rate // 1000
                        end_idx = end * sample_rate // 1000
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            vad_state="segment_mid",
                        )
            else:
                if is_detected:
                    yield AudioSpan(
                        start_ms=-1,
                        end_ms=-1,
                        waveform=waveform,
                        sample_rate=sample_rate,
                        vad_state="segment_mid",
                    )

            offset += len(data)

        state.update(
            {
                "buffer": buffer,
                "cache": cache,
                "offset": offset,
                "is_detected": is_detected,
                "audio_waveform": audio_waveform,
            }
        )

    def reset(self):
        pass

    def from_checkpoint(self, checkpoint_dir: str | None = None, **kwargs) -> Self:
        checkpoint_dir = checkpoint_dir or DEFAULT_CHECKPOINT_DIR
        self.fsmn = AutoModel(
            model=str(checkpoint_dir),
            disable_update=True,
            disable_log=True,
            disable_pbar=True,
            max_end_silence_time=self.max_end_silence_time,
            **kwargs,
        )
        return self

    @property
    def chunk_size(self) -> int:
        return self.chunk_size_ms * self.sample_rate // 1000


@registry.stream_vad_models.register("stream_fsmn.onnx")
class FSMNForStreamVADOnnx(StreamVADModel):
    fsmn: Fsmn_vad_online | None = None
    chunk_size_ms: int = 100
    sample_rate: int = 16000
    max_end_silence_time: int = 200

    def detect_chunk(
        self,
        waveform: Waveform,
        state: Dict,
        is_last: bool,
    ) -> Iterable[AudioSpan]:
        """Detect voice activity in the given chunk of waveform.
        Args:
            waveform (Waveform): The chunk of waveform to detect voice activity in.
            is_last (bool): Indicates if the chunk is the last chunk of the audio.
            state (Dict): The state of the model, which includes buffer, cache, offset, is_detected, and audio_waveform.
        Notes:
            - The function processes the waveform in chunks of size `self.chunk_size`.
            - If the sample rate of the input waveform does not match `self.sample_rate`, it will be resampled.
            - The function maintains a buffer to handle waveform chunks and updates the state accordingly.
            - Voice activity detection is performed using the FSMN model, and detected segments are yielded as AudioSpan objects.
            - If `is_last` is True and there is remaining data in the buffer, it processes the final chunk.
        Yields:
            AudioSpan: Detected voice activity spans, each represented as an AudioSpan object.
        """
        if waveform.sample_rate != self.sample_rate:
            waveform = waveform.resample(self.sample_rate)
        buffer: Waveform = state.get(
            "buffer",
            Waveform(data=np.array([], dtype=np.float32), sample_rate=self.sample_rate),
        )
        buffer = buffer.append(waveform)
        audio_waveform: Waveform = state.get(
            "audio_waveform",
            Waveform(data=np.array([], dtype=np.float32), sample_rate=self.sample_rate),
        )
        audio_waveform = audio_waveform.append(waveform=waveform)
        in_cache = state.get("in_cache", [])
        offset = state.get("offset", 0)
        is_detected = state.get("is_detected", False)
        param_dict = {"in_cache": in_cache, "is_final": is_last}
        while len(buffer) >= self.chunk_size:
            chunk_waveform = buffer[: self.chunk_size]
            buffer = buffer[self.chunk_size :]
            data = chunk_waveform.data
            sample_rate = chunk_waveform.sample_rate
            start = time.perf_counter()
            segments = self.fsmn(audio_in=data, param_dict=param_dict)
            end = time.perf_counter()
            if len(segments) > 0:
                for segment in segments[
                    0
                ]:  # segments[0] is the result of the first input, batch size is 1
                    start, end = segment
                    if start != -1 and end == -1:
                        is_detected = True
                        start_idx = start * sample_rate // 1000
                        end_idx = len(data) + offset
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            vad_state="segment_start",
                        )
                    if start == -1 and end != -1:
                        is_detected = False
                        start_idx = offset
                        end_idx = end * sample_rate // 1000
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            vad_state="segment_end",
                        )
                    if start != -1 and end != -1:
                        is_detected = False
                        start_idx = start * sample_rate // 1000
                        end_idx = end * sample_rate // 1000
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            vad_state="segment_mid",
                        )
            else:
                if is_detected:
                    yield AudioSpan(
                        start_ms=-1,
                        end_ms=-1,
                        waveform=waveform,
                        sample_rate=sample_rate,
                        vad_state="segment_mid",
                    )
            offset += len(data)
        if is_last and 0 < len(buffer) < self.chunk_size:
            chunk_waveform = buffer
            buffer = Waveform(data=np.array([]), sample_rate=self.sample_rate)
            data = chunk_waveform.data
            sample_rate = chunk_waveform.sample_rate
            segments = self.fsmn(audio_in=data, param_dict=param_dict)
            if len(segments) > 0:
                for segment in segments[0]:
                    start, end = segment
                    if start != -1 and end == -1:
                        is_detected = True
                        start_idx = start * sample_rate // 1000
                        end_idx = len(data) + offset
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            vad_state="segment_start",
                        )
                    if start == -1 and end != -1:
                        is_detected = False
                        start_idx = offset
                        end_idx = end * sample_rate // 1000
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            vad_state="segment_end",
                        )
                    if start != -1 and end != -1:
                        is_detected = False
                        start_idx = start * sample_rate // 1000
                        end_idx = end * sample_rate // 1000
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            vad_state="segment_mid",
                        )
            else:
                if is_detected:
                    yield AudioSpan(
                        start_ms=-1,
                        end_ms=-1,
                        waveform=waveform,
                        sample_rate=sample_rate,
                        vad_state="segment_mid",
                    )
            offset += len(data)
        state.update(
            {
                "buffer": buffer,
                "in_cache": in_cache,
                "offset": offset,
                "is_detected": is_detected,
                "audio_waveform": audio_waveform,
            }
        )

    def reset(self):
        pass

    def from_checkpoint(self, checkpoint_dir: str | None = None, **kwargs) -> Self:
        checkpoint_dir = checkpoint_dir or DEFAULT_CHECKPOINT_DIR
        self.fsmn = Fsmn_vad_online(
            model_dir=str(checkpoint_dir),
            max_end_sil=self.max_end_silence_time,
            **kwargs,
        )
        return self

    @property
    def chunk_size(self) -> int:
        return self.chunk_size_ms * self.sample_rate // 1000
