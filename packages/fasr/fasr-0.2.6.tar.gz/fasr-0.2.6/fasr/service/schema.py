from pydantic import BaseModel
from typing import Literal


class AudioChunkResponse(BaseModel):
    text: str
    state: (
        Literal[
            "segment_start", "segment_end", "interim_transcript", "final_transcript"
        ]
        | None
    ) = None
    lang: str | None = None
    event: Literal[
        "BGM",
        "Speech",
        "Applause",
        "Laughter",
        "Cry",
        "Sneeze",
        "Breath",
        "Cough",
        "Event_UNK",
    ] = "Event_UNK"
    emo: Literal[
        "HAPPY",
        "SAD",
        "ANGRY",
        "NEUTRAL",
        "FEARFUL",
        "DISGUSTED",
        "SURPRISED",
        "EMO_UNKNOWN",
    ] = "EMO_UNKNOWN"


class TranscriptionResponse(BaseModel):
    code: Literal[0, -1] = 0
    msg: str = "success"
    data: AudioChunkResponse | None = None
