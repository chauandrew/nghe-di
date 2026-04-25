from dataclasses import dataclass

@dataclass
class VocabItem:
    id: str                  # e.g. "v001"
    vi: str                  # Vietnamese text
    en: str                  # English gloss
    ipa: str                 # IPA transcription (southern accent)
    level: int
    day_introduced: int
    # SM-2 SRS fields
    ease_factor: float = 2.5
    interval_days: int = 1
    repetitions: int = 0
    next_review: str = ""    # ISO date string

    def __post_init__(self):
        if not self.next_review:
            self.next_review = date.today().isoformat()

    def update_srs(self, quality: int):
        """Update SM-2 state. quality: 0=fail, 1=hard, 2=good, 3=easy"""
        if quality < 1:
            self.repetitions = 0
            self.interval_days = 1
        else:
            if self.repetitions == 0:
                self.interval_days = 1
            elif self.repetitions == 1:
                self.interval_days = 6
            else:
                self.interval_days = round(self.interval_days * self.ease_factor)
            self.ease_factor = max(1.3, self.ease_factor + 0.1 - (3 - quality) * 0.08)
            self.repetitions += 1
        self.next_review = (date.today() + timedelta(days=self.interval_days)).isoformat()
