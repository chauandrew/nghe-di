import json

from pathlib import Path
from dataclasses import asdict, fields

from lesson_generator.config import SRS_REVIEW_OFFSETS, absolute_day
from lesson_generator.models.VocabItem import VocabItem

# ---------------------------------------------------------------------------
# Vocab database (persistent across lesson runs)
# ---------------------------------------------------------------------------

class VocabDB:
    def __init__(self, path: Path):
        self.path = path
        self.items: dict[str, VocabItem] = {}
        self._load()

    def _load(self):
        if self.path.exists():
            raw = json.loads(self.path.read_text())
            # Tolerate legacy records that still carry old SM-2 fields
            # (ease_factor, next_review, ...) by keeping only known fields.
            allowed = {f.name for f in fields(VocabItem)}
            self.items = {
                k: VocabItem(**{kk: vv for kk, vv in v.items() if kk in allowed})
                for k, v in raw.items()
            }

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(
            {k: asdict(v) for k, v in self.items.items()},
            ensure_ascii=False, indent=2
        ))

    def add(self, item: VocabItem):
        self.items[item.id] = item

    def due_on_day(self, level: int, day: int) -> list[str]:
        """Vocab IDs scheduled for review on the given lesson day.

        A word introduced on absolute day N is due whenever the current
        absolute day equals N + offset for some offset in SRS_REVIEW_OFFSETS.
        Words introduced on (or after) the current day are excluded — they are
        being taught now, not reviewed.
        """
        current = absolute_day(level, day)
        due = []
        for k, v in self.items.items():
            intro = absolute_day(v.level, v.day_introduced)
            if intro >= current:
                continue
            if any(intro + off == current for off in SRS_REVIEW_OFFSETS):
                due.append(k)
        return due

    def next_id(self) -> str:
        return f"v{len(self.items) + 1:03d}"

    def get(self, vid: str) -> VocabItem | None:
        return self.items.get(vid)
