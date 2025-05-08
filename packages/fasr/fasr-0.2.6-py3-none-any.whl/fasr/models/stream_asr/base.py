from typing import Iterable
from fasr.models.base import CachedModel
from fasr.data import AudioToken, Waveform
from abc import abstractmethod


class StreamASRModel(CachedModel):
    """流式语音识别模型基类"""

    @abstractmethod
    def transcribe_chunk(
        self,
        waveform: Waveform,
        is_last: bool = False,
        **kwargs,
    ) -> Iterable[AudioToken]:
        raise NotImplementedError
