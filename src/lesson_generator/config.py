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
ELEVENLABS_VOICE_VI_F = "N0Z0aL8qHhzwUHwRBcVo"   # "Thanh" - female
ELEVENLABS_VOICE_VI_M = "JYT6xPLD3LGl0ui3YXNq"   # "Khanh" - male
ELEVENLABS_VOICE_EN = "D11AWvkESE7DJwqIVi7L"   # "Brian"
ELEVENLABS_MODEL    = "eleven_flash_v2_5"  # Cheaper model, supports Vietnamese

# Vietnamese speaking speeds. A brand-new content word is introduced at SLOW
# speed so an English ear can catch the tone contour before hearing the word at
# conversational pace. ElevenLabs' speed floor is ~0.7 (below that the tone
# smears), so SLOW cannot go much lower. Anything that is not a first-exposure
# of a new word uses NORMAL.
VI_SPEED_NORMAL = 0.85   # general Vietnamese pace (was 0.90; slower per feedback)
VI_SPEED_SLOW   = 0.72   # first exposures of a new word
EN_SPEED        = 1.0    # English narrator

# How many of a new word's first renderings play slowly before dropping to
# NORMAL. Covers the isolated introduction (model says it, learner repeats it)
# without dragging out the later drills, where the word should sound natural.
SLOW_FIRST_N = 2

ELEVENLABS_VOICE_SETTINGS_EN = VoiceSettings(
    speed=EN_SPEED,
    stability=0.75,           # Lower = more expressive, higher = more consistent
    similarity_boost=0.75,
    style=0.20,
    use_speaker_boost=True,
)

ELEVENLABS_VOICE_SETTINGS_VI = VoiceSettings(
    speed=VI_SPEED_NORMAL,
    stability=0.75,           # Lower = more expressive, higher = more consistent
    similarity_boost=0.75,
    style=0.20,
    use_speaker_boost=True,
)

# ---------------------------------------------------------------------------
# Spaced repetition (deterministic, lesson-day based)
# ---------------------------------------------------------------------------
# Lessons are generated as static MP3s, so there is no learner-grading loop.
# Instead of calendar-date SM-2, reviews are scheduled by *lesson-day index*:
# a word introduced on absolute day N is reviewed on days N + offset.
# The two long offsets (75, 140) keep early survival vocab in rotation into the
# later levels instead of abandoning it after ~day 65; only words introduced in
# the first ~10 days reach the 140 review, which is exactly the survival core.
SRS_REVIEW_OFFSETS = [1, 3, 7, 16, 35, 75, 140]

# The recall segment can only realistically drill a handful of items, so
# due_on_day caps each day's review list at this many (most-at-risk first).
SRS_MAX_REVIEWS_PER_LESSON = 6

# Days per level — used to turn (level, day) into a continuous absolute day
# index so review scheduling carries across level boundaries
# (e.g. L2-D1 follows L1-D30).
DAYS_PER_LEVEL = 30


def absolute_day(level: int, day: int) -> int:
    """Continuous day index across levels. L1-D1 -> 1, L2-D1 -> DAYS_PER_LEVEL+1."""
    return (level - 1) * DAYS_PER_LEVEL + day


# Silence durations (milliseconds) used between segments
PAUSE_DURATIONS = {
    "short":  1500,   # between prompt and repeat
    "medium": 3000,   # answer pause — time for learner to respond
    "long":   5000,   # end-of-drill pause
}

# Anthropic model used for lesson generation
CLAUDE_MODEL = "claude-opus-4-8"

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
      "type": "recall" | "dialogue" | "consolidate" | "drill" | "synthesis",
      "duration_s": number,
      "script": string
    }
  ]
}
 
Script formatting rules:
- [VI_M: text] — male Vietnamese voice (the learner's voice, or a male character)
- [VI_F: text] — female Vietnamese voice (a female character, e.g. vendor, colleague)
- [VI: text]   — shorthand for [VI_M: text], use for the learner's prompted responses
- [EN: text]   — English narrator voice
- [PAUSE 3s]   — silence gap in seconds
- Use realistic HCMC dialogue scenes (street cafés, markets, xe ôm rides, restaurants)
- After every new Vietnamese word/phrase, immediately provide the English gloss in [EN: ...]
- Southern (HCMC) phonology: 5 spoken tones (the hỏi and ngã marks sound the same), ơ distinct from ă
- Pimsleur style: build from repetition, graduated intervals, never more than 4 new words
 
Gender and pronoun guidance:
- In dialogues, assign a consistent gender to each character and use the correct voice tag throughout
- Use natural southern Vietnamese pronouns: anh (older male), chị (older female), em (younger speaker)
- Female characters (vendors, colleagues, friends) use [VI_F: ...] and refer to themselves as "em" or "chị"
- The learner uses [VI: ...] or [VI_M: ...] and can use "anh" or "em" depending on context
- This allows natural exchanges like: [VI_F: Anh muốn uống gì?] [VI: Anh muốn cà phê sữa đá.]
 
CRITICAL tagging rule — [EN: ...] must contain ONLY English words. Never place any
Vietnamese word or phrase inside an [EN: ...] tag, even short ones like "em", "xin", "ba".
Always use a separate [VI: ...] or [VI_F: ...] tag for Vietnamese. Split mixed sentences.
Spell English words in [EN: ...] WITHOUT accent marks (write "cafe", not "café"; "banh mi",
not "bánh mì") so an accented letter is never mistaken for Vietnamese. Use the [VI: ...] tag
if you actually want the Vietnamese word spoken.
 
WRONG:  [EN: The word for thank you is cảm ơn.]
WRONG:  [EN: Say xin chào to greet someone.]
CORRECT: [EN: The word for thank you is] [VI: cảm ơn] [EN: Repeat after me.]
CORRECT: [EN: Say] [VI: xin chào] [EN: to greet someone.]

This applies just as much to a casual mid-instruction mention of a word's name, and to a
recap/summary sentence that lists several words' meanings — both are common places this rule
gets broken. Also never spell out a bare Vietnamese vowel letter (ư, ơ, ươ, etc.) inside [EN:
...] when giving a mouth-shape cue; describe the sound instead.
WRONG:  [EN: Now add her pronoun, chị, to be polite.]
WRONG:  [EN: dạ is a soft, polite yes, and ơi calls to someone.]
WRONG:  [EN: The ư sound here — keep your lips relaxed, not rounded.]
CORRECT: [EN: Now add her pronoun,] [VI: chị] [EN: to be polite.]
CORRECT: [VI: dạ] [EN: is a soft, polite yes, and] [VI: ơi] [EN: calls to someone.]
CORRECT: [EN: Keep your lips relaxed, not rounded, for that sound.]

Narration style:
- Be terse. No scene-setting narration like "You are at a café in District 1." or "The vendor looks up and smiles."
- Jump straight into dialogue and vocabulary. Trust the learner to follow context from the Vietnamese itself.
- Never narrate what is about to happen. Do it.
- Keep English narration to the minimum needed to gloss a word or cue a response.

Introducing a new word (do this for EVERY new content word; this is the most important rule):
- A beginner cannot catch a Vietnamese word at full speed on first hearing, so every new word must
  get a SLOW, ISOLATED, REPEATED hearing somewhere in its introduction. The audio engine
  automatically plays the first two ISOLATED utterances of a new word more slowly, so each new word
  must be said on its own (not only ever buried inside a sentence) at least twice.
- Teach in whichever order is clearer for the item:
    (a) Word first: say the word alone, gloss + tone it, say it again, pause, say it again, then have
        the learner produce it, then use it in a phrase.
    (b) Sentence first: present a short natural sentence, then break it down (say each new word alone,
        gloss + tone it, repeat it), then restate the whole sentence and give its meaning. This is
        often easier for phrases and for words that only make sense in context.
- Example of the word-first pattern:
    [VI_F: một] [EN: means one. It has] [VI: dấu nặng] [EN: . Listen again.] [VI_F: một] [PAUSE 1s] [VI_F: một]
    [EN: Now you say it.] [PAUSE 4s] [VI: một]
- Every new content word must be heard at least 5-6 times across the whole lesson
  (intro + repeats + drill + synthesis). Repetition is the point; do not be stingy with it.
- Re-say each new word in isolation once more near the end of the drill, before the synthesis scene.

Vocabulary control (important — do not break this):
- Teaching segments (recall, dialogue, drill) must use ONLY Vietnamese words taught in
  this lesson or a prior lesson. Never put an untaught content word in front of the learner.
- Synthesis scenes should sound natural but must STILL stay within taught words, plus the
  allowed function-word set below. Do not slip untaught nouns/verbs into a scene for flavour.
- Allowed function words (may appear once glossed): dạ (polite "yes" / soft opener),
  nha (friendly softener), hả (tag question, "right?"), lắm and quá (intensifier, "very/too"),
  vậy (so/then), không (yes-no question marker at the end), của (possessive, "of"),
  rồi (already), ơi (vocative), alô (hello, on the phone).
- The FIRST time any allowed function word appears in a lesson, gloss it once in [EN: ...].
  After that you may reuse it freely within that lesson.

Southern (HCMC) conventions:
- Use ngàn for "thousand", never nghìn.
- There is no word for "please". Politeness comes from pronouns and from dạ. Open polite
  replies with dạ, and attach the listener's pronoun to thanks and questions:
  "Cảm ơn anh", "Bao nhiêu vậy chị?".
- Address the listener as anh (older man), chị (older woman), or em (younger person); the
  learner refers to themselves with the matching pronoun.
- To ask for a lower price use giảm giá ("to discount"); do not use rẻ hơn.

Pause rules:
- ONLY add a [PAUSE Xs] when the learner is expected to speak. Two cases:
  1. Production pause — learner repeats a word or phrase out loud:
     Pattern: [EN: cue word or phrase —] [PAUSE 4s] [VI: answer]
     Example: [EN: Thank you —] [PAUSE 4s] [VI: Cảm ơn.]
  2. Response pause — learner answers a question in Vietnamese:
     Pattern: [EN: question in English —] [PAUSE 4s] [VI: answer]
     Example: [EN: How do you say hello?] [PAUSE 4s] [VI: Xin chào.]
- Use 4s for production pauses (speaking takes more time than listening).
- Use 3s for recognition pauses (reverse drill: Vietnamese cue → English meaning).
- Add a .5s pause after rhetorical or transitional phrases like "Ready?", "Listen.",
  "Now reverse.", "Good.", "Let us begin.", or after scene dialogue the learner just listens to.
- Always place the pause BEFORE the answer reveal, not after it.
 
Tone naming (southern Vietnamese — FIVE distinct sounds, not six):
- Southern speech MERGES the hỏi and ngã marks: they sound identical (a dipping tone). Keep
  using both names in writing (the spelling still distinguishes them), but never cue the learner
  to hear a difference between them — a southern voice pronounces them the same.
- LEVELS 1-3 (before the tone-mark names are taught): describe a word's tone in plain English,
  never name it. Use exactly these descriptions so they stay consistent lesson to lesson:
    ngang: "a flat tone, no mark"       dấu huyền: "a falling tone"
    dấu sắc: "a high, rising tone"      dấu hỏi / dấu ngã: "a dipping tone — it falls, then rises"
    dấu nặng: "a low tone, cut off short"
  Tag these as plain [EN: ...] text, never as [VI: ...] — they are English, not the Vietnamese
  tone-mark name:
    [VI_F: Cảm] [EN: has a dipping tone — it falls, then rises.] [PAUSE 0.3s]
    [VI_F: Ơn] [EN: is a flat tone, no mark.]
- LEVEL 4 ONWARD: the learner was taught the tone-mark NAMES as vocabulary at L4-D0: ngang,
  dấu huyền, dấu sắc, dấu hỏi, dấu ngã, dấu nặng. From L4-D0 onward, NAME the tone in Vietnamese
  instead of describing it in English — do not fall back to the Level 1-3 English-description
  style once L4-D0 has taught the names. Always tag the tone name itself as [VI: ...], never
  inside [EN: ...]:
    [VI_F: Cảm] [EN: has] [VI: dấu hỏi] [PAUSE 0.3s]
    [VI_F: Ơn] [EN: is] [VI: ngang] [EN: — flat, no mark.]
- Periodically remind the learner of a word's tone during drill and recall — roughly every 3rd or
  4th time a word appears, at every level. Do not name the tone every single time.
- Level 1-3 example: [VI_F: Cảm ơn] [EN: means thank you.] [VI_F: Cảm] [EN: has a dipping tone — it falls, then rises.] [VI_F: Ơn] [EN: is a flat tone, no mark.]
- Level 4+ example: [VI_F: Cảm ơn] [EN: means thank you.] [VI_F: Cảm] [EN: has] [VI: dấu hỏi] [EN: .] [VI_F: Ơn] [EN: is] [VI: ngang] [EN: — flat.]

Vowel pronunciation cues (use sparingly, like tone reminders):
- The hardest vowels for English speakers are the NEUTRAL (unrounded) ones: ư, ơ, â. English
  has no ư, and learners wrongly round their lips. When a new word hinges on one, add ONE short
  mouth-shape cue alongside the tone cue, in [EN: ...], referring to the sound, never the spelling:
    rounded vowels (o, ô, u): "round your lips"
    neutral vowels (ư, ơ, â):  "keep your lips relaxed, not rounded"
    front vowels (i, ê, e):    "spread your lips into a smile"
- Example: [VI_F: nước] [EN: the ư sound here — keep your lips relaxed, not rounded.]
- Never write a Vietnamese vowel letter inside an [EN: ...] tag; describe the sound, or put the
  syllable in a [VI: ...] tag. Reserve cues for ư / ơ / â and the rounded-versus-neutral contrast.

 
Grammar and structure lessons (favour structure over vocabulary):
- Some lessons teach a STRUCTURE — a reusable pattern — rather than new content words
  (negation, yes/no questions, completion questions, measure words). For these:
    1. State the pattern in one plain English sentence.
    2. Drill it by SUBSTITUTION: hold the frame fixed and swap in words the learner
       already knows. This is where the lesson's value is — prioritise it over new vocab.
    3. Introduce at most one or two genuinely new words; recombine known vocabulary.
- Measure words (classifiers): to count a noun, use [number] + [measure] + [noun],
  e.g. hai ly cà phê (two glasses of coffee), một tô phở (one bowl of pho).
  Common southern measure words: cái (generic), tô (bowl), ly (glass), chai (bottle),
  ổ (loaf, for bánh mì).
- Yes/no questions: [statement] + không?  OR  có + [verb/noun] + không?
  Answer with có (yes) or không (no).
- Completion questions: [subject] + [verb] + chưa?  Answer rồi (already) or chưa (not yet).
- Negation: không + [verb or adjective], e.g. không ngon (not tasty), không muốn (do not want).

Cold open (Pimsleur-style — apply from Day 1 onward, no exceptions for early lessons):
- The dialogue segment must OPEN by playing the day's target scene once, in full, at natural
  speed, with NO English translation or scaffolding beyond a single one-line cue like
  [EN: Listen.]. The learner is not meant to understand it yet — that is the point. It is a
  preview they earn by the end of the lesson, not a comprehension check.
- This cold-open scene is a SHORT natural exchange (2-4 lines) built from this lesson's new
  material — write it, then teach its pieces, then close the lesson by replaying this EXACT
  same scene in synthesis, now that the learner understands it. That replay is the payoff; the
  cold open and the synthesis replay must be the identical scene, word for word, not two
  different scenes.
- After the cold open, move straight into the normal teach flow (word-first or sentence-first,
  per the rule above) — do not explain the cold open line by line right away, that is what the
  rest of dialogue and consolidate are for.

Segment guidelines:
- recall:      ~90s  — drill EVERY review item in the list you are given (it is already sorted most-at-risk first and capped to what fits), learner responds, confirm each. Do not silently skip any.
- dialogue:    ~210s — open with the cold-open scene (see above), then introduce new vocab OR a
  structure; gloss + tone-name each new word on first use; for structures, state the rule then
  model it.
- consolidate: ~75s  — a light, low-pressure pass back over every new word/phrase from dialogue,
  once each, in the order taught. This is a bridge, not a test: recognition or a gentle single
  production per item, no reversal, no graduated intervals — that is drill's job. Keep the
  pressure low; the point is to confirm today's words are solid before drill works them harder.
  Do not skip this segment or fold it into dialogue — it exists so the jump from "just taught"
  to "drilled hard" is not so abrupt.
- drill:       ~240s — this is the longest segment; do not shortchange it. Graduated interval
  repetition PLUS a full reversal pass (Vietnamese cue -> English meaning) for every new item
  this lesson, not just a sample. For structures, drill by substitution. Pauses only for learner
  responses.
- synthesis:   ~150s — replay the EXACT cold-open scene from the start of dialogue, now at
  natural speed with no gaps — the learner should recognise it and understand it this time. Then
  a short practice turn using today's material, then preview 1 word from next lesson."""
