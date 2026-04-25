import json
from datetime import date

from pathlib import Path
from dataclasses import asdict

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
            self.items = {k: VocabItem(**v) for k, v in raw.items()}

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(
            {k: asdict(v) for k, v in self.items.items()},
            ensure_ascii=False, indent=2
        ))

    def add(self, item: VocabItem):
        self.items[item.id] = item

    def due_today(self) -> list[str]:
        today = date.today().isoformat()
        return [k for k, v in self.items.items() if v.next_review <= today]

    def next_id(self) -> str:
        return f"v{len(self.items) + 1:03d}"

    def get(self, vid: str) -> VocabItem | None:
        return self.items.get(vid)
