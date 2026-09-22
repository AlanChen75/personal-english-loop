#!/usr/bin/env python3
"""Generate slide-by-slide CACS 2026 audio with Alan's cloned voice."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_cloned_audio import (  # noqa: E402
    DEFAULT_REF_AUDIO_SSH,
    DEFAULT_REF_TEXT,
    DEFAULT_SERVER,
    MODEL_ID,
    concatenate_wavs,
    encode_mp3,
    generate_chunk,
    healthcheck,
    load_reference_audio,
    probe_audio,
    split_text_for_tts,
)


DEFAULT_SOURCE = Path(
    "/Users/user/Desktop/NILM+LLM/cacs2026-nilm-llm/"
    "paper/R1/presentation/src/build_documents.py"
)
PRONUNCIATION_REPLACEMENTS = (
    (re.compile(r"\bPseudo-?NILM\b", re.IGNORECASE), "pseudo nil-em"),
    (re.compile(r"\bTECA\b"), "tee ee see ay"),
    (re.compile(r"\bIMDELD\b"), "eye em dee ee el dee"),
    (re.compile(r"\bWELTRON\b"), "well-tron"),
    (re.compile(r"\bHIPE\b"), "hype"),
    (re.compile(r"\bVFD\b"), "vee eff dee"),
    (re.compile(r"\bCase1\b"), "Case one"),
    (re.compile(r"\bF1\b"), "F one"),
)
PRONUNCIATION_GUIDE = (
    "Conference pronunciation guide. "
    "Pseudo nil-em. Pseudo nil-em. "
    "N I L M, pronounced en eye el em. En eye el em. "
    "T E C A, pronounced tee ee see ay. Tee ee see ay. "
    "I M D E L D, pronounced eye em dee ee el dee. Eye em dee ee el dee. "
    "HIPE is pronounced hype. Hype. "
    "WELTRON is pronounced well-tron. Well-tron. "
    "V F D, pronounced vee eff dee. Vee eff dee. "
    "Case one. Segment F one. "
    "Variable-frequency load. Aggregate power. Energy attribution. "
    "Pseudo trace. Defensive dispatch. Explicit abstention."
)


def load_english_slides(source_path: Path) -> list[dict]:
    """Read ENGLISH_SLIDES with AST so the document builder is not executed."""
    tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "ENGLISH_SLIDES" for target in node.targets):
            slides = ast.literal_eval(node.value)
            if not isinstance(slides, list) or not slides:
                raise ValueError("ENGLISH_SLIDES must be a non-empty list")
            required = {"number", "title", "script"}
            for slide in slides:
                if not isinstance(slide, dict) or not required.issubset(slide):
                    raise ValueError("Every slide needs number, title, and script")
            return slides
    raise ValueError(f"ENGLISH_SLIDES not found in {source_path}")


def prepare_spoken_text(text: str) -> str:
    spoken = text
    for pattern, replacement in PRONUNCIATION_REPLACEMENTS:
        spoken = pattern.sub(replacement, spoken)
    return spoken


def normalize_request_text(text: str) -> str:
    """Give every bounded TTS request one clean terminal punctuation mark."""
    request_text = re.sub(r"[,;:]$", ".", text.strip())
    if not request_text.endswith((".", "!", "?")):
        request_text += "."
    return request_text


def xvector_cache_name(text: str) -> str:
    # Keep this key identical to the GPU trial/batch cache convention so a
    # verified chunk is reused instead of regenerated.
    digest = hashlib.sha256(b"x-vector-only" + text.encode("utf-8")).hexdigest()
    return f"{digest}.wav"


def build_xvector_plan(
    slides: list[dict],
    *,
    pronunciation_guide: str = PRONUNCIATION_GUIDE,
    max_chars: int = 140,
) -> dict:
    """Build reproducible cross-language clone jobs and their track mapping."""
    jobs_by_output: dict[str, dict] = {}
    tracks = []

    def add_track(*, track_id: str, text: str, pause_ms: int, **metadata: object) -> None:
        chunk_outputs = []
        for index, chunk in enumerate(split_text_for_tts(text, max_chars=max_chars), start=1):
            request_text = normalize_request_text(chunk)
            output = xvector_cache_name(request_text)
            chunk_outputs.append(output)
            jobs_by_output.setdefault(
                output,
                {
                    "id": f"{track_id}-{index:02d}",
                    "text": request_text,
                    "output": output,
                },
            )
        tracks.append(
            {
                "id": track_id,
                "spoken_text": text,
                "pause_between_chunks_ms": pause_ms,
                "chunks": chunk_outputs,
                **metadata,
            }
        )

    for slide in slides:
        number = slide["number"]
        title = slide["title"]
        add_track(
            track_id=f"slide-{number:02d}",
            text=prepare_spoken_text(slide["script"]),
            pause_ms=350,
            kind="slide",
            number=number,
            title=title,
            stem=f"slide-{number:02d}-{safe_slug(title)}",
        )

    add_track(
        track_id="pronunciation-guide",
        text=pronunciation_guide,
        pause_ms=500,
        kind="pronunciation-guide",
        stem="pronunciation-guide",
    )
    return {
        "generation_mode": "x-vector-only",
        "max_chars": max_chars,
        "jobs": list(jobs_by_output.values()),
        "tracks": tracks,
    }


def safe_slug(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:60] or "slide"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--slides", type=int, nargs="+", choices=range(1, 11))
    parser.add_argument("--server", default=DEFAULT_SERVER)
    parser.add_argument("--ref-audio")
    parser.add_argument("--ref-audio-ssh", default=DEFAULT_REF_AUDIO_SSH)
    parser.add_argument("--ref-text", default=DEFAULT_REF_TEXT)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT / "outputs/cacs2026-conference-audio",
    )
    parser.add_argument(
        "--work-root",
        type=Path,
        default=ROOT / "work/cacs2026-conference-audio",
    )
    parser.add_argument("--max-chars", type=int, default=140)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument(
        "--prepare-xvector",
        action="store_true",
        help="Write bounded x-vector-only GPU jobs and stop.",
    )
    parser.add_argument(
        "--assemble-xvector",
        action="store_true",
        help="Assemble generated x-vector WAV chunks and normalize final MP3 files.",
    )
    parser.add_argument(
        "--xvector-cache",
        type=Path,
        help="Directory containing the generated x-vector-only WAV chunks.",
    )
    return parser.parse_args()


def write_xvector_plan(plan: dict, work_root: Path) -> tuple[Path, Path]:
    work_root.mkdir(parents=True, exist_ok=True)
    plan_path = work_root / "xvector-plan.json"
    jobs_path = work_root / "xvector-jobs.json"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    jobs_path.write_text(
        json.dumps({"jobs": plan["jobs"]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return plan_path, jobs_path


def assemble_xvector_plan(
    *,
    plan: dict,
    cache_dir: Path,
    work_root: Path,
    output_root: Path,
    source_path: Path,
    reference_audio_sha256: str,
) -> Path:
    missing = sorted(
        {output for track in plan["tracks"] for output in track["chunks"]}
        - {path.name for path in cache_dir.glob("*.wav")}
    )
    if missing:
        raise FileNotFoundError(f"Missing {len(missing)} generated WAV chunks; first: {missing[0]}")

    raw_dir = work_root / "raw-xvector"
    output_root.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": MODEL_ID,
        "generation_mode": "voice_clone_x-vector-only_existing_parameters",
        "post_processing": "loudnorm I=-16 LUFS, TP=-1.5 dB, LRA=11; no speed change",
        "language": "English",
        "reference_audio_sha256": reference_audio_sha256,
        "source_path": str(source_path),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "slides": [],
    }
    full_talk_parts = []

    for track in plan["tracks"]:
        parts = []
        for index, filename in enumerate(track["chunks"]):
            pause = track["pause_between_chunks_ms"] if index < len(track["chunks"]) - 1 else 0
            parts.append((cache_dir / filename, pause))
        raw_path = raw_dir / f"{track['stem']}.wav"
        duration = concatenate_wavs(parts, raw_path)
        mp3_path = output_root / f"{track['stem']}.mp3"
        transcript_path = output_root / f"{track['stem']}.txt"
        encode_mp3(raw_path, mp3_path, slow=False)
        transcript_path.write_text(track["spoken_text"] + "\n", encoding="utf-8")
        item = {
            "audio": mp3_path.name,
            "spoken_transcript": transcript_path.name,
            "chunk_count": len(track["chunks"]),
            "raw_duration_seconds": round(duration, 3),
            "probe": probe_audio(mp3_path),
        }
        if track["kind"] == "slide":
            item.update({"number": track["number"], "title": track["title"]})
            manifest["slides"].append(item)
            full_talk_parts.append((raw_path, 1500))
        else:
            manifest["pronunciation_guide"] = item

    if full_talk_parts:
        full_talk_parts[-1] = (full_talk_parts[-1][0], 0)
        full_raw = raw_dir / "cacs2026-full-talk.wav"
        full_duration = concatenate_wavs(full_talk_parts, full_raw)
        full_mp3 = output_root / "cacs2026-full-talk.mp3"
        encode_mp3(full_raw, full_mp3, slow=False)
        manifest["full_talk"] = {
            "audio": full_mp3.name,
            "raw_duration_seconds": round(full_duration, 3),
            "probe": probe_audio(full_mp3),
        }

    manifest_path = output_root / "generation-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest_path


def generate_spoken_track(
    *,
    text: str,
    raw_output: Path,
    server: str,
    ref_audio: bytes,
    ref_text: str,
    cache_dir: Path,
    max_chars: int,
    timeout: int,
    pause_ms: int = 350,
) -> dict:
    chunks = split_text_for_tts(text, max_chars=max_chars)
    parts = []
    for index, chunk_text in enumerate(chunks, start=1):
        print(f"      [{index}/{len(chunks)}] {len(chunk_text)} characters")
        request_text = re.sub(r"[,;:]$", ".", chunk_text)
        if not request_text.endswith((".", "!", "?")):
            request_text += "."
        chunk_path = generate_chunk(
            server=server,
            text=request_text,
            ref_audio=ref_audio,
            ref_text=ref_text,
            cache_dir=cache_dir,
            timeout=timeout,
        )
        trailing_pause = pause_ms if index < len(chunks) else 0
        parts.append((chunk_path, trailing_pause))
    duration = concatenate_wavs(parts, raw_output)
    return {"chunk_count": len(chunks), "raw_duration_seconds": round(duration, 3)}


def main() -> int:
    args = parse_args()
    slides = load_english_slides(args.source)
    if args.slides:
        selected = set(args.slides)
        slides = [slide for slide in slides if slide["number"] in selected]

    if args.prepare_xvector or args.assemble_xvector:
        plan = build_xvector_plan(slides, max_chars=args.max_chars)
        plan_path, jobs_path = write_xvector_plan(plan, args.work_root)
        print(f"X-vector plan: {plan_path}")
        print(f"GPU jobs: {jobs_path} ({len(plan['jobs'])} unique chunks)")
        if args.prepare_xvector and not args.assemble_xvector:
            return 0
        if not args.xvector_cache:
            raise ValueError("--assemble-xvector requires --xvector-cache")
        ref_audio = load_reference_audio(args.ref_audio, args.ref_audio_ssh)
        manifest_path = assemble_xvector_plan(
            plan=plan,
            cache_dir=args.xvector_cache,
            work_root=args.work_root,
            output_root=args.output_root,
            source_path=args.source,
            reference_audio_sha256=hashlib.sha256(ref_audio).hexdigest(),
        )
        print(f"Done: {manifest_path}")
        return 0

    health = healthcheck(args.server)
    print(f"TTS server healthy: {health}")

    ref_audio = load_reference_audio(args.ref_audio, args.ref_audio_ssh)
    ref_hash = hashlib.sha256(ref_audio).hexdigest()
    source_hash = hashlib.sha256(args.source.read_bytes()).hexdigest()
    cache_dir = args.work_root / "cache"
    raw_dir = args.work_root / "raw"
    args.output_root.mkdir(parents=True, exist_ok=True)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": MODEL_ID,
        "generation_mode": "voice_clone_existing_server_parameters",
        "post_processing": "loudnorm I=-16 LUFS, TP=-1.5 dB, LRA=11; no speed change",
        "server": args.server,
        "language": "English",
        "reference_audio_sha256": ref_hash,
        "source_path": str(args.source),
        "source_sha256": source_hash,
        "slides": [],
    }
    full_talk_parts = []

    for slide in slides:
        number = slide["number"]
        title = slide["title"]
        spoken_text = prepare_spoken_text(slide["script"])
        stem = f"slide-{number:02d}-{safe_slug(title)}"
        raw_path = raw_dir / f"{stem}.wav"
        mp3_path = args.output_root / f"{stem}.mp3"
        transcript_path = args.output_root / f"{stem}.txt"
        print(f"\nSlide {number}: {title}")
        generation = generate_spoken_track(
            text=spoken_text,
            raw_output=raw_path,
            server=args.server,
            ref_audio=ref_audio,
            ref_text=args.ref_text,
            cache_dir=cache_dir,
            max_chars=args.max_chars,
            timeout=args.timeout,
        )
        encode_mp3(raw_path, mp3_path, slow=False)
        transcript_path.write_text(spoken_text + "\n", encoding="utf-8")
        full_talk_parts.append((raw_path, 1500))
        manifest["slides"].append(
            {
                "number": number,
                "title": title,
                "audio": mp3_path.name,
                "spoken_transcript": transcript_path.name,
                **generation,
                "probe": probe_audio(mp3_path),
            }
        )

    print("\nPronunciation guide")
    guide_raw = raw_dir / "pronunciation-guide.wav"
    guide_generation = generate_spoken_track(
        text=PRONUNCIATION_GUIDE,
        raw_output=guide_raw,
        server=args.server,
        ref_audio=ref_audio,
        ref_text=args.ref_text,
        cache_dir=cache_dir,
        max_chars=args.max_chars,
        timeout=args.timeout,
        pause_ms=500,
    )
    guide_mp3 = args.output_root / "pronunciation-guide.mp3"
    encode_mp3(guide_raw, guide_mp3, slow=False)
    (args.output_root / "pronunciation-guide.txt").write_text(
        PRONUNCIATION_GUIDE + "\n", encoding="utf-8"
    )
    manifest["pronunciation_guide"] = {
        "audio": guide_mp3.name,
        **guide_generation,
        "probe": probe_audio(guide_mp3),
    }

    if full_talk_parts:
        full_talk_parts[-1] = (full_talk_parts[-1][0], 0)
        full_raw = raw_dir / "cacs2026-full-talk.wav"
        full_duration = concatenate_wavs(full_talk_parts, full_raw)
        full_mp3 = args.output_root / "cacs2026-full-talk.mp3"
        encode_mp3(full_raw, full_mp3, slow=False)
        manifest["full_talk"] = {
            "audio": full_mp3.name,
            "raw_duration_seconds": round(full_duration, 3),
            "probe": probe_audio(full_mp3),
        }

    manifest_path = args.output_root / "generation-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nDone: {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
