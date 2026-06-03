from dataclasses import dataclass


@dataclass
class VocabItem:
    id: str                  # e.g. "v001"
    vi: str                  # Vietnamese text
    en: str                  # English gloss
    ipa: str                 # IPA transcription (southern accent)
    level: int
    day_introduced: int      # the lesson day on which this word is first taught

    # NOTE: review scheduling is computed deterministically from `level` +
    # `day_introduced` against config.SRS_REVIEW_OFFSETS (see VocabDB.due_on_day).
    # There is no per-user SM-2 state because lessons are generated as static
    # MP3s — there is no learner feedback signal to grade against.
