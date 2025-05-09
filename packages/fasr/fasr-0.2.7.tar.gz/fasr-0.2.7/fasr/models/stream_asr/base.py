from typing import Iterable, Dict
from fasr.models.base import CachedModel
from fasr.data import AudioToken, Waveform
from abc import abstractmethod


class StreamASRModel(CachedModel):
    """流式语音识别模型基类"""

    chunk_size_ms: int = None

    @abstractmethod
    def transcribe_chunk(
        self,
        waveform: Waveform,
        is_last: bool,
        state: Dict,
        **kwargs,
    ) -> Iterable[AudioToken]:
        raise NotImplementedError
