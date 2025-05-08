from fasr.models.base import CachedModel
from fasr.data import AudioSpan, Waveform
from abc import abstractmethod
from typing import List


class StreamVADModel(CachedModel):
    @abstractmethod
    def detect_chunk(self, waveform: Waveform, is_last: bool) -> List[AudioSpan]:
        raise NotImplementedError
