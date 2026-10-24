#!/usr/bin/env python3
"""Prepare and assemble Automation 2026 Shadow audio with Alan's cloned voice."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_cloned_audio import (
    MODEL_ID,
    concatenate_wavs,
    encode_mp3,
    load_reference_audio,
    probe_audio,
    split_text_for_tts,
)
from generate_conference_audio import (
    normalize_request_text,
    prepare_display_text as prepare_conference_display_text,
    safe_slug,
    xvector_cache_name,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path(
    "/Users/user/Desktop/NILM+LLM/automation2026-nilm-llm/"
    "presentation/tts_13min_v3/spoken_segments.json"
)
DEFAULT_APPENDIX_SOURCE = ROOT / "practice-materials/automation2026/extension-v5.json"
DEFAULT_REF_AUDIO_SSH = "ac-3090:/home/ac3090/alan_voice.wav"
PRONUNCIATION_REPLACEMENTS = (
    (
        re.compile(r"\bd11351004@mail\.ntust\.edu\.tw\b", re.IGNORECASE),
        "d one one three five one zero zero four at mail dot N T U S T dot E D U dot T W",
    ),
    (re.compile(r"\bNILM\b"), "nil-em"),
    (re.compile(r"\bLLM\b"), "ell ell em"),
    (re.compile(r"\bLHS\b"), "ell aitch ess"),
    (re.compile(r"\bMCCs\b"), "em see see values"),
    (re.compile(r"\bMCC\b"), "em see see"),
    (re.compile(r"\bTP\b"), "tee pee"),
    (re.compile(r"\bTN\b"), "tee en"),
    (re.compile(r"\bFP\b"), "eff pee"),
    (re.compile(r"\bFN\b"), "eff en"),
    (re.compile(r"\bIMDELD\b"), "eye em dee ee el dee"),
    (re.compile(r"\bWELTRON\b"), "well-tron"),
    (re.compile(r"\bCase 1\b", re.IGNORECASE), "Case one"),
    (re.compile(r"\bseed-one-oh-one\b", re.IGNORECASE), "seed one oh one"),
    (re.compile(r"\bQ&A\b"), "Q and A"),
)
PRONUNCIATION_GUIDE = (
    "Automation pronunciation guide. "
    "N I L M, pronounced nil-em. Nil-em. "
    "L L M, pronounced ell ell em. Ell ell em. "
    "L H S, pronounced ell aitch ess. Ell aitch ess. "
    "M C C, pronounced em see see. Em see see. "
    "I M D E L D, pronounced eye em dee ee el dee. "
    "WELTRON is pronounced well-tron. "
    "Case one. Seed one oh one. Event F one."
)
LEADING_DECIMAL_RE = re.compile(
    r"\bpoint ((?:zero|one|two|three|four|five|six|seven|eight|nine)"
    r"(?: (?:zero|one|two|three|four|five|six|seven|eight|nine))*)\b",
    re.IGNORECASE,
)
DIGIT_WORDS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
DISPLAY_REPLACEMENTS = (
    (re.compile(r"\bseed-one-oh-one\b", re.IGNORECASE), "seed 101"),
    (
        re.compile(r"\bfifty, twenty, thirty percent split\b", re.IGNORECASE),
        "50%, 20%, 30% split",
    ),
    (re.compile(r"\btwo hundred twenty-five\b", re.IGNORECASE), "225"),
    (re.compile(r"\bfifty-four\b", re.IGNORECASE), "54"),
    (re.compile(r"\bnine hundred\b", re.IGNORECASE), "900"),
    (re.compile(r"\bsix percent\b", re.IGNORECASE), "6%"),
    (re.compile(r"\btwenty-seed\b", re.IGNORECASE), "20-seed"),
    (re.compile(r"\bfifteen joint configurations\b", re.IGNORECASE), "15 joint configurations"),
    (re.compile(r"\bnine devices\b", re.IGNORECASE), "9 devices"),
    (re.compile(r"\bnine device MCC values\b", re.IGNORECASE), "9 device MCC values"),
    (re.compile(r"\bfour counts\b", re.IGNORECASE), "4 counts"),
    (re.compile(r"\bfive LLM generation seeds\b", re.IGNORECASE), "5 LLM generation seeds"),
    (re.compile(r"\bAcross five LLM test seeds\b", re.IGNORECASE), "Across 5 LLM test seeds"),
    (re.compile(r"\bfive-seed\b", re.IGNORECASE), "5-seed"),
    (re.compile(r"\bfive over 225\b", re.IGNORECASE), "5/225"),
    (re.compile(r"\b54 over 900\b", re.IGNORECASE), "54/900"),
    (re.compile(r"\bfive out of\b", re.IGNORECASE), "5 out of"),
    (re.compile(r"\bthree industrial corpora\b", re.IGNORECASE), "3 industrial corpora"),
    (re.compile(r"\bthese three datasets\b", re.IGNORECASE), "these 3 datasets"),
    (re.compile(r"\bone power sample per second\b", re.IGNORECASE), "1 power sample per second"),
    (re.compile(r"\bone fixed seed\b", re.IGNORECASE), "1 fixed seed"),
)


def prepare_spoken_text(text: str) -> str:
    spoken = text
    for pattern, replacement in PRONUNCIATION_REPLACEMENTS:
        spoken = pattern.sub(replacement, spoken)
    return spoken


def prepare_display_text(text: str) -> str:
    def replace_leading_decimal(match: re.Match[str]) -> str:
        fraction = "".join(DIGIT_WORDS[word.lower()] for word in match.group(1).split())
        return f"0.{fraction}"

    display = prepare_conference_display_text(text)
    display = LEADING_DECIMAL_RE.sub(replace_leading_decimal, display)
    for pattern, replacement in DISPLAY_REPLACEMENTS:
        display = pattern.sub(replacement, display)
    display = re.sub(r"\b(\d+(?:\.\d+)?) percent\b", r"\1%", display)
    return display


def _require_text(item: dict, field: str) -> str:
    value = item.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Every item needs non-empty {field}")
    return value.strip()


def _qa_number_word(index: int) -> str:
    words = {1: "one", 2: "two", 3: "three", 4: "four"}
    if index not in words:
        raise ValueError("Automation Q&A supports four numbered questions")
    return words[index]


def load_automation_tracks(
    source_path: Path, appendix_path: Path | None = None
) -> list[dict]:
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    segments = payload.get("segments")
    qa_answers = payload.get("qa_answers")
    if not isinstance(segments, list) or len(segments) != 12:
        raise ValueError("Automation source must contain exactly 12 segments")
    if not isinstance(qa_answers, list) or not qa_answers:
        raise ValueError("Automation source must contain Q&A answers")

    extension_payload = {}
    if appendix_path is not None:
        extension_payload = json.loads(appendix_path.read_text(encoding="utf-8"))
    overrides = extension_payload.get("overrides", [])
    if not isinstance(overrides, list):
        raise ValueError("Automation extension overrides must be a list")
    overrides_by_slide = {}
    for override in overrides:
        if not isinstance(override, dict) or not isinstance(override.get("slide"), int):
            raise ValueError("Every Automation override needs an integer slide")
        slide_number = override["slide"]
        if slide_number < 1 or slide_number > 12 or slide_number in overrides_by_slide:
            raise ValueError("Automation overrides must target unique slides from 1 to 12")
        overrides_by_slide[slide_number] = override

    tracks = []
    for expected, segment in enumerate(segments, start=1):
        if not isinstance(segment, dict) or segment.get("slide") != expected:
            raise ValueError("Automation slides must be consecutive from 1 to 12")
        effective = {**segment, **overrides_by_slide.get(expected, {})}
        script = _require_text(effective, "spoken_transcript")
        display_source = effective.get("display_transcript", script)
        if not isinstance(display_source, str) or not display_source.strip():
            raise ValueError("Every slide needs a display transcript")
        tracks.append(
            {
                "number": expected,
                "title": _require_text(effective, "title"),
                "script": script,
                "display_text": prepare_display_text(display_source.strip()),
                "slide_image": f"automation2026/slides/slide-{expected}.png",
                "kind": "slide",
            }
        )

    if appendix_path is not None:
        additional_slides = extension_payload.get("additional_slides", [])
        if not isinstance(additional_slides, list):
            raise ValueError("Automation extension additional_slides must be a list")
        for additional in additional_slides:
            expected = len(tracks) + 1
            if not isinstance(additional, dict) or additional.get("slide") != expected:
                raise ValueError("Automation additional slides must continue the slide sequence")
            script = _require_text(additional, "spoken_transcript")
            display_source = additional.get("display_transcript", script)
            if not isinstance(display_source, str) or not display_source.strip():
                raise ValueError("Every additional slide needs a display transcript")
            tracks.append(
                {
                    "number": expected,
                    "title": _require_text(additional, "title"),
                    "script": script,
                    "display_text": prepare_display_text(display_source.strip()),
                    "slide_image": f"automation2026/slides/slide-{expected}.png",
                    "kind": "slide",
                }
            )

        appendices = extension_payload.get("appendices")
        if not isinstance(appendices, list) or not appendices:
            raise ValueError("Automation extension source must contain appendices")
        for appendix in appendices:
            expected = len(tracks) + 1
            if not isinstance(appendix, dict) or appendix.get("slide") != expected:
                raise ValueError("Automation appendices must continue the slide sequence")
            script = _require_text(appendix, "spoken_transcript")
            display_source = appendix.get("display_transcript", script)
            if not isinstance(display_source, str) or not display_source.strip():
                raise ValueError("Every appendix needs a display transcript")
            tracks.append(
                {
                    "number": expected,
                    "title": _require_text(appendix, "title"),
                    "script": script,
                    "display_text": prepare_display_text(display_source.strip()),
                    "slide_image": f"automation2026/slides/slide-{expected}.png",
                    "kind": "appendix",
                }
            )

    qa_spoken = []
    qa_display = []
    numbered = 0
    for answer in qa_answers:
        if not isinstance(answer, dict):
            raise ValueError("Every Q&A answer must be an object")
        answer_text = _require_text(answer, "spoken_transcript")
        question = _require_text(answer, "question")
        if answer.get("id") == "general":
            spoken_heading = display_heading = "General response."
        else:
            numbered += 1
            question_text = re.sub(r"^Q\d+\s*[—-]\s*", "", question).strip()
            spoken_heading = f"Question {_qa_number_word(numbered)}. {question_text}"
            display_heading = f"Q{numbered}. {question_text}"
        qa_spoken.append(f"{spoken_heading} Answer. {answer_text}")
        qa_display.append(f"{display_heading} Answer. {prepare_display_text(answer_text)}")

    tracks.append(
        {
            "number": len(tracks) + 1,
            "title": "Q&A response pack",
            "script": "\n\n".join(qa_spoken),
            "display_text": "\n\n".join(qa_display),
            "slide_image": tracks[-1]["slide_image"],
            "kind": "qa",
        }
    )
    return tracks


def build_xvector_plan(tracks: list[dict], *, max_chars: int = 140) -> dict:
    jobs_by_output: dict[str, dict] = {}
    planned_tracks = []

    def add_track(track: dict, text: str, *, kind: str, pause_ms: int) -> None:
        outputs = []
        for index, chunk in enumerate(split_text_for_tts(text, max_chars=max_chars), start=1):
            request_text = normalize_request_text(chunk)
            output = xvector_cache_name(request_text)
            outputs.append(output)
            jobs_by_output.setdefault(
                output,
                {"id": f"{track['stem']}-{index:02d}", "text": request_text, "output": output},
            )
        planned_tracks.append(
            {
                **track,
                "kind": kind,
                "spoken_text": text,
                "pause_between_chunks_ms": pause_ms,
                "chunks": outputs,
            }
        )

    for item in tracks:
        stem = f"slide-{item['number']:02d}-{safe_slug(item['title'])}"
        add_track(
            {**item, "stem": stem},
            prepare_spoken_text(item["script"]),
            kind=item.get("kind", "slide"),
            pause_ms=350,
        )
    add_track(
        {"stem": "pronunciation-guide", "title": "Pronunciation guide"},
        PRONUNCIATION_GUIDE,
        kind="pronunciation-guide",
        pause_ms=500,
    )
    return {
        "generation_mode": "x-vector-only",
        "max_chars": max_chars,
        "jobs": list(jobs_by_output.values()),
        "tracks": planned_tracks,
    }


def write_plan(plan: dict, work_root: Path) -> tuple[Path, Path]:
    work_root.mkdir(parents=True, exist_ok=True)
    plan_path = work_root / "xvector-plan.json"
    jobs_path = work_root / "xvector-jobs.json"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    jobs_path.write_text(
        json.dumps({"jobs": plan["jobs"]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return plan_path, jobs_path


def assemble_plan(
    *,
    plan: dict,
    cache_dir: Path,
    work_root: Path,
    output_root: Path,
    source_path: Path,
    appendix_path: Path | None = None,
) -> Path:
    missing = sorted(
        {name for track in plan["tracks"] for name in track["chunks"]}
        - {path.name for path in cache_dir.glob("*.wav")}
    )
    if missing:
        raise FileNotFoundError(f"Missing {len(missing)} WAV chunks; first: {missing[0]}")

    raw_dir = work_root / "raw-xvector"
    output_root.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": MODEL_ID,
        "generation_mode": "voice_clone_x-vector-only_existing_parameters",
        "post_processing": "loudnorm I=-16 LUFS, TP=-1.5 dB, LRA=11; no speed change",
        "source_path": source_path.name,
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "source_inputs": [
            {
                "path": source_path.name,
                "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
            },
            *(
                [
                    {
                        "path": appendix_path.name,
                        "sha256": hashlib.sha256(appendix_path.read_bytes()).hexdigest(),
                    }
                ]
                if appendix_path is not None
                else []
            ),
        ],
        "items": [],
    }
    full_talk_parts = []
    full_talk_spoken = []
    full_talk_display = []

    for track in plan["tracks"]:
        parts = [
            (
                cache_dir / filename,
                track["pause_between_chunks_ms"] if index < len(track["chunks"]) - 1 else 0,
            )
            for index, filename in enumerate(track["chunks"])
        ]
        raw_path = raw_dir / f"{track['stem']}.wav"
        duration = concatenate_wavs(parts, raw_path)
        mp3_path = output_root / f"{track['stem']}.mp3"
        encode_mp3(raw_path, mp3_path, slow=False)
        spoken_path = output_root / f"{track['stem']}.txt"
        spoken_path.write_text(track["spoken_text"] + "\n", encoding="utf-8")

        if track["kind"] == "pronunciation-guide":
            manifest["pronunciation_guide"] = {
                "audio": mp3_path.name,
                "spoken_transcript": spoken_path.name,
                "probe": probe_audio(mp3_path),
            }
            continue

        display_path = output_root / f"{track['stem']}-display.txt"
        display_path.write_text(track["display_text"] + "\n", encoding="utf-8")
        manifest["items"].append(
            {
                "number": track["number"],
                "title": track["title"],
                "audio": mp3_path.name,
                "spoken_transcript": spoken_path.name,
                "display_transcript": display_path.name,
                "slide_image": track["slide_image"],
                "raw_duration_seconds": round(duration, 3),
                "probe": probe_audio(mp3_path),
            }
        )
        if track["kind"] == "slide":
            full_talk_parts.append((raw_path, 1500))
            full_talk_spoken.append(track["spoken_text"])
            full_talk_display.append(track["display_text"])

    full_talk_parts[-1] = (full_talk_parts[-1][0], 0)
    full_raw = raw_dir / "automation2026-full-talk.wav"
    full_duration = concatenate_wavs(full_talk_parts, full_raw)
    full_mp3 = output_root / "automation2026-full-talk.mp3"
    encode_mp3(full_raw, full_mp3, slow=False)
    full_spoken_path = output_root / "automation2026-full-talk.txt"
    full_display_path = output_root / "automation2026-full-talk-display.txt"
    full_spoken_path.write_text("\n\n".join(full_talk_spoken) + "\n", encoding="utf-8")
    full_display_path.write_text("\n\n".join(full_talk_display) + "\n", encoding="utf-8")
    manifest["full_talk"] = {
        "audio": full_mp3.name,
        "spoken_transcript": full_spoken_path.name,
        "display_transcript": full_display_path.name,
        "raw_duration_seconds": round(full_duration, 3),
        "probe": probe_audio(full_mp3),
    }
    manifest_path = output_root / "generation-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--appendix-source", type=Path, default=DEFAULT_APPENDIX_SOURCE)
    parser.add_argument("--work-root", type=Path, default=ROOT / "work/automation2026-audio")
    parser.add_argument("--output-root", type=Path, default=ROOT / "outputs/automation2026-audio")
    parser.add_argument("--max-chars", type=int, default=140)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--assemble", action="store_true")
    parser.add_argument("--xvector-cache", type=Path)
    parser.add_argument("--ref-audio-ssh", default=DEFAULT_REF_AUDIO_SSH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    tracks = load_automation_tracks(args.source, args.appendix_source)
    plan = build_xvector_plan(tracks, max_chars=args.max_chars)
    plan_path, jobs_path = write_plan(plan, args.work_root)
    print(f"Plan: {plan_path}")
    print(f"Jobs: {jobs_path} ({len(plan['jobs'])} unique chunks)")
    if args.prepare and not args.assemble:
        return 0
    if not args.assemble or not args.xvector_cache:
        raise ValueError("Use --prepare or provide --assemble with --xvector-cache")
    load_reference_audio(None, args.ref_audio_ssh)
    manifest = assemble_plan(
        plan=plan,
        cache_dir=args.xvector_cache,
        work_root=args.work_root,
        output_root=args.output_root,
        source_path=args.source,
        appendix_path=args.appendix_source,
    )
    print(f"Done: {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
