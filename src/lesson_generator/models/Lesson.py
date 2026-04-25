from dataclasses import dataclass

from lesson_generator.models.LessonSegment import LessonSegment
from lesson_generator.models.VocabItem import VocabItem

@dataclass
class Lesson:
    id: str          # e.g. "L1-D3"
    level: int
    day: int
    title: str
    vocab: list[VocabItem]
    review_ids: list[str]
    segments: list[LessonSegment]