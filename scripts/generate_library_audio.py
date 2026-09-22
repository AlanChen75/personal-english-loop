#!/usr/bin/env python3
"""Prepare and assemble cloned-voice audio for grouped learning materials."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_cloned_audio import (  # noqa: E402
    DEFAULT_REF_AUDIO_SSH,
    MODEL_ID,
    build_speech_units,
    concatenate_wavs,
    encode_mp3,
    load_reference_audio,
    probe_audio,
    split_text_for_tts,
)
from generate_conference_audio import normalize_request_text, xvector_cache_name  # noqa: E402


SAFE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _safe_relative_path(value: object, field: str) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise ValueError(f"{field} must stay inside the repository root")
    return path


def _safe_id(value: object, field: str) -> str:
    if not isinstance(value, str) or not SAFE_ID_RE.fullmatch(value):
        raise ValueError(f"{field} must be a lowercase hyphenated identifier")
    return value


def load_catalog(catalog_path: Path, *, root: Path = ROOT) -> dict:
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    collections = payload.get("collections")
    if not isinstance(collections, list) or not collections:
        raise ValueError("catalog collections must be a non-empty list")

    result = []
    for collection in collections:
        collection_id = _safe_id(collection.get("id"), "collection id")
        title = collection.get("title")
        items = collection.get("items")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("collection title must be non-empty")
        if not isinstance(items, list) or not items:
            raise ValueError("collection items must be a non-empty list")

        loaded_items = []
        for item in items:
            number = item.get("number")
            item_title = item.get("title")
            stem = _safe_id(item.get("stem"), "stem")
            source = _safe_relative_path(item.get("source"), "source")
            if not isinstance(number, int) or number < 1:
                raise ValueError("item number must be a positive integer")
            if not isinstance(item_title, str) or not item_title.strip():
                raise ValueError("item title must be non-empty")
            source_path = root.joinpath(*source.parts).resolve()
            resolved_root = root.resolve()
            if resolved_root not in source_path.parents or not source_path.is_file():
                raise ValueError(f"source is not a readable file inside the repository: {source}")
            spoken_text = source_path.read_text(encoding="utf-8").strip()
            if not spoken_text:
                raise ValueError(f"source is empty: {source}")
            loaded_items.append(
                {
                    "number": number,
                    "title": item_title.strip(),
                    "source": source.as_posix(),
                    "stem": stem,
                    "spoken_text": spoken_text,
                }
            )
        result.append({"id": collection_id, "title": title.strip(), "items": loaded_items})
    return {"collections": result}


def build_xvector_plan(catalog: dict, *, max_chars: int = 140) -> dict:
    jobs_by_output: dict[str, dict] = {}
    tracks = []
    collections = []
    for collection in catalog["collections"]:
        collection_items = []
        for item in collection["items"]:
            chunk_outputs = []
            parts = []
            job_index = 0
            for unit in build_speech_units(item["spoken_text"]):
                chunks = split_text_for_tts(unit.text, max_chars=max_chars)
                for chunk_index, chunk in enumerate(chunks, start=1):
                    job_index += 1
                    request_text = normalize_request_text(chunk)
                    output = xvector_cache_name(request_text)
                    chunk_outputs.append(output)
                    pause_after_ms = (
                        unit.pause_ms if chunk_index == len(chunks) else 350
                    )
                    parts.append(
                        {"output": output, "pause_after_ms": pause_after_ms}
                    )
                    jobs_by_output.setdefault(
                        output,
                        {
                            "id": f"{item['stem']}-{job_index:02d}",
                            "text": request_text,
                            "output": output,
                        },
                    )
            track = {
                **item,
                "collection_id": collection["id"],
                "chunks": chunk_outputs,
                "parts": parts,
            }
            tracks.append(track)
            collection_items.append(
                {
                    "number": item["number"],
                    "title": item["title"],
                    "audio": f"{item['stem']}.mp3",
                    "spoken_transcript": f"{item['stem']}.txt",
                }
            )
        collections.append(
            {"id": collection["id"], "title": collection["title"], "items": collection_items}
        )
    return {
        "generation_mode": "x-vector-only",
        "max_chars": max_chars,
        "jobs": list(jobs_by_output.values()),
        "tracks": tracks,
        "collections": collections,
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
    catalog_path: Path,
    reference_audio_sha256: str,
) -> Path:
    required = {filename for track in plan["tracks"] for filename in track["chunks"]}
    available = {path.name for path in cache_dir.glob("*.wav")}
    missing = sorted(required - available)
    if missing:
        raise FileNotFoundError(f"Missing {len(missing)} WAV chunks; first: {missing[0]}")

    raw_dir = work_root / "raw"
    output_root.mkdir(parents=True, exist_ok=True)
    track_results = {}
    for track in plan["tracks"]:
        parts = [
            (cache_dir / part["output"], part["pause_after_ms"])
            for part in track["parts"]
        ]
        raw_path = raw_dir / f"{track['stem']}.wav"
        duration = concatenate_wavs(parts, raw_path)
        mp3_path = output_root / f"{track['stem']}.mp3"
        transcript_path = output_root / f"{track['stem']}.txt"
        encode_mp3(raw_path, mp3_path, slow=False)
        transcript_path.write_text(track["spoken_text"] + "\n", encoding="utf-8")
        track_results[track["stem"]] = {
            "raw_duration_seconds": round(duration, 3),
            "chunk_count": len(track["chunks"]),
            "probe": probe_audio(mp3_path),
        }

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": MODEL_ID,
        "generation_mode": "voice_clone_x-vector-only_existing_parameters",
        "post_processing": "loudnorm I=-16 LUFS, TP=-1.5 dB, LRA=11; no speed change",
        "language": "English",
        "reference_audio_sha256": reference_audio_sha256,
        "catalog_sha256": hashlib.sha256(catalog_path.read_bytes()).hexdigest(),
        "collections": [],
    }
    for collection in plan["collections"]:
        items = []
        for item in collection["items"]:
            stem = Path(item["audio"]).stem
            items.append({**item, **track_results[stem]})
        manifest["collections"].append({**collection, "items": items})

    manifest_path = output_root / "learning-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=ROOT / "lessons/shadowing-library.json")
    parser.add_argument("--work-root", type=Path, default=ROOT / "work/learning-library")
    parser.add_argument("--output-root", type=Path, default=ROOT / "outputs/learning-library")
    parser.add_argument("--max-chars", type=int, default=140)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--assemble", action="store_true")
    parser.add_argument("--xvector-cache", type=Path)
    parser.add_argument("--ref-audio")
    parser.add_argument("--ref-audio-ssh", default=DEFAULT_REF_AUDIO_SSH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    catalog = load_catalog(args.catalog)
    plan = build_xvector_plan(catalog, max_chars=args.max_chars)
    plan_path, jobs_path = write_plan(plan, args.work_root)
    print(f"Plan: {plan_path}")
    print(f"Jobs: {jobs_path} ({len(plan['jobs'])} unique chunks)")
    if args.prepare and not args.assemble:
        return 0
    if not args.assemble:
        return 0
    if not args.xvector_cache:
        raise ValueError("--assemble requires --xvector-cache")
    ref_audio = load_reference_audio(args.ref_audio, args.ref_audio_ssh)
    manifest_path = assemble_plan(
        plan=plan,
        cache_dir=args.xvector_cache,
        work_root=args.work_root,
        output_root=args.output_root,
        catalog_path=args.catalog,
        reference_audio_sha256=hashlib.sha256(ref_audio).hexdigest(),
    )
    print(f"Done: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
