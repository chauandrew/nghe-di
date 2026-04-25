from dataclasses import dataclass

@dataclass
class LessonSegment:
    type: str        # "recall" | "dialogue" | "drill" | "synthesis"
    duration_s: int
    script: str      # narration with [PAUSE Xs], [VI: ...], [EN: ...] tags