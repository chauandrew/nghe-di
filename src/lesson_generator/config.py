from pathlib import Path
from elevenlabs import VoiceSettings

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path("lessons")
VOCAB_DB_PATH = OUTPUT_DIR / "vocab_db.json"

# ElevenLabs voice IDs
# Find voices at elevenlabs.io/voice-library, or paste a cloned voice ID here.
# eleven_multilingual_v2 handles Vietnamese tones reasonably well.
# Tip: clone a native HCMC speaker for best accent accuracy.
ELEVENLABS_VOICE_VI = "JYT6xPLD3LGl0ui3YXNq"   # "Khanh"
ELEVENLABS_VOICE_EN = "D11AWvkESE7DJwqIVi7L"   # "Brian"
ELEVENLABS_MODEL    = "eleven_flash_v2_5"  # Cheaper model, supports Vietnamese

ELEVENLABS_VOICE_SETTINGS_EN = VoiceSettings(
    speed=1.1,
    stability=0.75,           # Lower = more expressive, higher = more consistent
    similarity_boost=0.75,
    style=0.20,
    use_speaker_boost=True,
)

ELEVENLABS_VOICE_SETTINGS_VI = VoiceSettings(
    speed=0.90,
    stability=0.75,           # Lower = more expressive, higher = more consistent
    similarity_boost=0.75,
    style=0.20,
    use_speaker_boost=True,
)

# Silence durations (milliseconds) used between segments
PAUSE_DURATIONS = {
    "short":  1500,   # between prompt and repeat
    "medium": 3000,   # answer pause — time for learner to respond
    "long":   5000,   # end-of-drill pause
}

# Anthropic model used for lesson generation
CLAUDE_MODEL = "claude-opus-4-6"

# ---------------------------------------------------------------------------
# Lesson generation via Claude
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a Vietnamese audio lesson writer for southern (HCMC) accent learners.
Output ONLY a valid JSON object — no prose, no markdown, no backticks.
 
Schema:
{
  "id": string,
  "title": string,
  "vocab": [
    {"vi": string, "en": string, "ipa": string}
  ],
  "segments": [
    {
      "type": "recall" | "dialogue" | "drill" | "synthesis",
      "duration_s": number,
      "script": string
    }
  ]
}
 
Script formatting rules:
- Wrap Vietnamese speech in [VI: text]
- Wrap English narration in [EN: text]
- Write pauses as [PAUSE 3s], [PAUSE 5s] etc.
- Use realistic HCMC dialogue scenes (street cafés, markets, xe ôm rides, restaurants)
- After every new Vietnamese word/phrase, immediately provide the English gloss in [EN: ...]
- Southern (HCMC) phonology: 6 tones, final -c/-ch → glottal stop, ơ distinct from ă
- Pimsleur style: build from repetition, graduated intervals, never more than 4 new words
 
CRITICAL tagging rule — [EN: ...] must contain ONLY English words. Never place any
Vietnamese word or phrase inside an [EN: ...] tag, even short ones like "em", "xin", "ba".
Always use a separate [VI: ...] tag for Vietnamese. Split mixed sentences into separate tags.
 
WRONG:  [EN: The word for thank you is cảm ơn.]
WRONG:  [EN: Say xin chào to greet someone.]
CORRECT: [EN: The word for thank you is] [VI: cảm ơn] [EN: Repeat after me.]
CORRECT: [EN: Say] [VI: xin chào] [EN: to greet someone.]
 
Segment guidelines:
- recall:    ~90s  — prompt 3-5 items from prior lesson with [PAUSE 3s] for learner to respond, then confirm
- dialogue:  ~180s — introduce new vocab in a realistic HCMC scene, repeat each new word 3x
- drill:     ~180s — graduated interval repetition, mix new + review, use [PAUSE 3s] throughout
- synthesis: ~150s — full scene replay at natural pace + preview 1 word from next lesson"""
