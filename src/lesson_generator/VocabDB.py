import json

from pathlib import Path
from dataclasses import asdict, fields

from lesson_generator.config import (
    SRS_REVIEW_OFFSETS,
    SRS_MAX_REVIEWS_PER_LESSON,
    absolute_day,
)
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

    def due_on_day(self, level: int, day: int,
                   cap: int = SRS_MAX_REVIEWS_PER_LESSON) -> list[str]:
        """Vocab IDs to review on the given lesson day — most-at-risk first, capped.

        A word introduced on absolute day N is due whenever the current absolute
        day equals N + offset for some offset in SRS_REVIEW_OFFSETS. Words
        introduced on (or after) the current day are excluded — they are being
        taught now, not reviewed.

        The list is sorted by the triggering offset DESCENDING (a longer interval
        since the word was introduced = more forgetting risk = higher priority),
        then capped at `cap`, because the recall segment can only drill a handful
        of items. Capping after sorting means the reviews dropped on a heavy day
        are the short-interval ones (e.g. N+1) — fine, since a word taught
        yesterday already recurs in today's drills. Ties break toward the
        earlier-introduced (more foundational) word.
        """
        current = absolute_day(level, day)
        due = []  # (offset, intro, id)
        for k, v in self.items.items():
            intro = absolute_day(v.level, v.day_introduced)
            if intro >= current:
                continue
            gap = current - intro
            if gap in SRS_REVIEW_OFFSETS:
                due.append((gap, intro, k))
        due.sort(key=lambda t: (-t[0], t[1]))
        return [k for _, _, k in due[:cap]]

    def next_id(self) -> str:
        return f"v{len(self.items) + 1:03d}"

    def get(self, vid: str) -> VocabItem | None:
        return self.items.get(vid)
