#!/usr/bin/env python3
"""
Vietnamese Audio Lesson Generator
----------------------------------
Generates Pimsleur-style Vietnamese audio lessons using:
  - Anthropic Claude API  → lesson JSON (script + vocab)
  - ElevenLabs TTS        → individual audio segments (HCMC southern accent)
  - pydub                 → stitches segments + silence gaps into final MP3

Usage:
    pip install anthropic elevenlabs pydub

    # pydub also needs ffmpeg for MP3 export:
    # macOS:  brew install ffmpeg
    # Ubuntu: sudo apt install ffmpeg

    # Set environment variables:
    export ANTHROPIC_API_KEY="sk-ant-..."
    export ELEVENLABS_API_KEY="sk_..."

    python generate_lessons.py --level 1 --days 1-5
    python generate_lessons.py --level 1 --days 1     # single day
    python generate_lessons.py --level 1 --days 1-30 --dry-run  # JSON only, no TTS

Output structure:
    lessons/
      L1-D1/
        lesson.json       ← full lesson metadata + SRS vocab
        L1-D1.mp3         ← final stitched audio
      L1-D2/
        ...
      _tts_cache/         ← cached audio clips (never re-billed)
      vocab_db.json       ← cumulative vocab + SRS state across all lessons
"""

import os
import re
import json
import time
import argparse
import hashlib
from pathlib import Path

import anthropic
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

from lesson_generator.curriculum import CURRICULUM
from lesson_generator.VocabDB import VocabDB
from lesson_generator.models.LessonSegment import LessonSegment
from lesson_generator.models.VocabItem import VocabItem

from lesson_generator.config import *

def generate_lesson_json(
    client: anthropic.Anthropic,
    level: int,
    day: int,
    new_vocab_hints: list[str],
    review_ids: list[str],
    scene: str,
    vocab_db: VocabDB,
) -> dict:
    """Call Claude to produce a lesson JSON for the given day."""
    review_words = []
    for vid in review_ids:
        item = vocab_db.get(vid)
        if item:
            review_words.append(f"{item.vi} ({item.en})")

    user_msg = (
        f"Generate lesson L{level}-D{day}.\n"
        f"New vocabulary hints: {', '.join(new_vocab_hints)}.\n"
        f"Review items due today ({len(review_words)}): {', '.join(review_words) or 'none'}.\n"
        f"Scene: {scene}.\n"
        f"Keep total new words to 3-4 maximum. Output JSON only."
    )

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=8092,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    print(response)

    raw = response.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


# ---------------------------------------------------------------------------
# TTS helpers — ElevenLabs
# ---------------------------------------------------------------------------

def tts_segment(
    tts_client: ElevenLabs,
    text: str,
    language: str,
    cache_dir: Path,
) -> AudioSegment:
    """Synthesise text → AudioSegment via ElevenLabs. Cached by content hash."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = hashlib.md5(f"{language}:{text}".encode()).hexdigest()
    cache_path = cache_dir / f"{key}.mp3"

    if not cache_path.exists():
        voice_id = ELEVENLABS_VOICE_VI if language == "vi" else ELEVENLABS_VOICE_EN
        voice_settings = ELEVENLABS_VOICE_SETTINGS_VI if language == "vi" else ELEVENLABS_VOICE_SETTINGS_EN

        audio_bytes = tts_client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id=ELEVENLABS_MODEL,
            voice_settings=voice_settings,
            output_format="mp3_44100_64",
        )
        # convert() returns a generator — collect all chunks
        cache_path.write_bytes(b"".join(audio_bytes))
        time.sleep(0.1)   # brief courtesy pause between API calls

    return AudioSegment.from_mp3(cache_path)


def parse_script(script: str) -> list[tuple[str, str]]:
    """
    Parse a script string into (type, content) tokens.
    Types: "vi", "en", "pause"
    Example: "[EN: Hello] [VI: Xin chào] [PAUSE 3s]"
    """
    tokens = []
    pattern = re.compile(r'\[VI:\s*(.*?)\]|\[EN:\s*(.*?)\]|\[PAUSE\s*(\d+)s\]', re.IGNORECASE)
    for m in pattern.finditer(script):
        if m.group(1):
            tokens.append(("vi", m.group(1).strip()))
        elif m.group(2):
            tokens.append(("en", m.group(2).strip()))
        elif m.group(3):
            tokens.append(("pause", m.group(3)))
    return tokens


def build_audio(
    segments: list[LessonSegment],
    tts_client: ElevenLabs,
    cache_dir: Path,
) -> AudioSegment:
    """Stitch all lesson segments into one AudioSegment."""
    full_audio = AudioSegment.silent(duration=500)  # 0.5s lead-in

    for seg in segments:
        tokens = parse_script(seg.script)

        for token_type, content in tokens:
            if token_type == "pause":
                ms = int(content) * 1000
                full_audio += AudioSegment.silent(duration=ms)
            elif token_type in ("vi", "en"):
                chunk = tts_segment(tts_client, content, token_type, cache_dir)
                full_audio += chunk
                full_audio += AudioSegment.silent(duration=300)  # brief breath gap

        # Inter-segment pause
        full_audio += AudioSegment.silent(duration=PAUSE_DURATIONS["short"])

    full_audio += AudioSegment.silent(duration=1000)  # 1s trail-out
    return full_audio


# ---------------------------------------------------------------------------
# Curriculum: vocab hints + scenes per day
# Extend this dict as you build out levels 2-5.
# ---------------------------------------------------------------------------

def get_day_config(level: int, day: int) -> dict:
    key = (level, day)
    if key in CURRICULUM:
        return CURRICULUM[key]
    return {
        "vocab": ["[add vocab hints to CURRICULUM dict]"],
        "scene": f"a realistic daily-life situation in Ho Chi Minh City (level {level}, day {day})",
    }


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def process_day(
    level: int,
    day: int,
    anthropic_client: anthropic.Anthropic,
    tts_client: ElevenLabs,
    vocab_db: VocabDB,
    dry_run: bool = False,
):
    lesson_id = f"L{level}-D{day}"
    lesson_dir = OUTPUT_DIR / lesson_id
    lesson_dir.mkdir(parents=True, exist_ok=True)
    mp3_path = lesson_dir / f"{lesson_id}.mp3"

    if mp3_path.exists():
        print(f"  [{lesson_id}] Already exists — skipping. Delete to regenerate.")
        return

    # Use existing lesson.json if present — skip Claude call
    lesson_json_path = lesson_dir / "lesson.json"
    if lesson_json_path.exists():
        print(f"  [{lesson_id}] Found existing lesson.json — skipping Claude.")
        raw_json = json.loads(lesson_json_path.read_text())
    else:
        print(f"  [{lesson_id}] Generating lesson script via Claude...")
        day_cfg = get_day_config(level, day)
        review_ids = vocab_db.due_today()
 
        raw_json = generate_lesson_json(
            client=anthropic_client,
            level=level,
            day=day,
            new_vocab_hints=day_cfg["vocab"],
            review_ids=review_ids,
            scene=day_cfg["scene"],
            vocab_db=vocab_db,
        )
 
        # Register new vocab in the DB
        for v in raw_json.get("vocab", []):
            vid = vocab_db.next_id()
            item = VocabItem(
                id=vid,
                vi=v["vi"],
                en=v["en"],
                ipa=v.get("ipa", ""),
                level=level,
                day_introduced=day,
            )
            vocab_db.add(item)
 
        lesson_json_path.write_text(json.dumps(raw_json, ensure_ascii=False, indent=2))
        print(f"  [{lesson_id}] Lesson JSON saved → {lesson_json_path}")

    if dry_run:
        print(f"  [{lesson_id}] Dry-run: skipping TTS + audio stitching.")
        return

    # Build audio via ElevenLabs
    print(f"  [{lesson_id}] Synthesising audio segments via ElevenLabs...")
    cache_dir = OUTPUT_DIR / "_tts_cache"
    segments = [LessonSegment(**s) for s in raw_json.get("segments", [])]
    audio = build_audio(segments, tts_client, cache_dir)

    print(f"  [{lesson_id}] Exporting MP3 ({len(audio)/1000:.1f}s)...")
    audio.export(mp3_path, format="mp3", bitrate="64k", tags={
        "title": raw_json.get("title", lesson_id),
        "artist": "NgheĐi",
        "album": f"Level {level}",
        "track": str(day),
        "comment": "Southern Vietnamese (HCMC) accent",
    })
    print(f"  [{lesson_id}] Done → {mp3_path}")


def parse_day_range(s: str) -> list[int]:
    """Parse '1', '1-5', or '1,3,5' into a sorted list of ints."""
    days = []
    for part in s.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            days.extend(range(int(a), int(b) + 1))
        else:
            days.append(int(part))
    return sorted(set(days))


def main():
    parser = argparse.ArgumentParser(description="NgheĐi — Vietnamese audio lesson generator")
    parser.add_argument("--level",   type=int, default=1,   help="Curriculum level (1-5)")
    parser.add_argument("--days",    type=str, default="1", help="Days to generate, e.g. '1', '1-5', '1,3,7'")
    parser.add_argument("--dry-run", action="store_true",   help="Generate JSON only, skip TTS + audio")
    args = parser.parse_args()

    days = parse_day_range(args.days)
    print(f"NgheĐi generator — Level {args.level}, Day(s): {days}")
    if args.dry_run:
        print("Dry-run mode: JSON only, no TTS calls.")

    anthropic_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    tts_client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    vocab_db = VocabDB(VOCAB_DB_PATH)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for day in days:
        process_day(
            level=args.level,
            day=day,
            anthropic_client=anthropic_client,
            tts_client=tts_client,
            vocab_db=vocab_db,
            dry_run=args.dry_run,
        )

    vocab_db.save()
    print(f"\nVocab DB updated → {VOCAB_DB_PATH} ({len(vocab_db.items)} total words)")


if __name__ == "__main__":
    main()
