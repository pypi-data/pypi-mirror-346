from fasr.models.base import CachedModel
from fasr.data import AudioSpan, Waveform
from abc import abstractmethod
from typing import List, Dict


class StreamVADModel(CachedModel):
    chunk_size_ms: int = 100
    sample_rate: int = 16000
    max_end_silence_time: int = 500

    @abstractmethod
    def detect_chunk(
        self, waveform: Waveform, is_last: bool, state: Dict
    ) -> List[AudioSpan]:
        raise NotImplementedError
