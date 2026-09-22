#!/usr/bin/env python3
"""Run bounded Qwen3-TTS voice-clone jobs directly on the GPU host."""

from __future__ import annotations

import argparse
import gc
import json
import re
import sys
import time
from pathlib import Path


MODEL_ID = "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
DEFAULT_REF_TEXT = (
    "大家好，歡迎收聽今天的節目，我是你們的主持人，今天我們要一起來聊聊"
)
SAFE_OUTPUT_RE = re.compile(r"^[a-f0-9]{64}\.wav$")


def validate_jobs(jobs: object) -> list[dict]:
    if not isinstance(jobs, list) or not jobs:
        raise ValueError("jobs must be a non-empty list")
    seen_outputs = set()
    for job in jobs:
        if not isinstance(job, dict):
            raise ValueError("each job must be an object")
        if not isinstance(job.get("id"), str) or not job["id"]:
            raise ValueError("each job needs a non-empty id")
        if not isinstance(job.get("text"), str) or not job["text"].strip():
            raise ValueError("each job needs non-empty text")
        output = job.get("output")
        if not isinstance(output, str) or not SAFE_OUTPUT_RE.fullmatch(output):
            raise ValueError("each job output must be a safe SHA-256 WAV filename")
        if output in seen_outputs:
            raise ValueError(f"duplicate job output: {output}")
        seen_outputs.add(output)
    return jobs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--ref-audio", type=Path, required=True)
    parser.add_argument("--ref-text", default=DEFAULT_REF_TEXT)
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--reject-duration-seconds", type=float, default=20.8)
    parser.add_argument("--x-vector-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    jobs = validate_jobs(json.loads(args.jobs.read_text(encoding="utf-8"))["jobs"])
    if not args.ref_audio.is_file():
        raise FileNotFoundError(args.ref_audio)
    if not 128 <= args.max_new_tokens <= 2048:
        raise ValueError("--max-new-tokens must be between 128 and 2048")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    pending = [job for job in jobs if not (args.output_dir / job["output"]).exists()]
    print(json.dumps({"event": "plan", "jobs": len(jobs), "pending": len(pending)}), flush=True)
    if not pending:
        return 0

    import soundfile as sf
    import torch
    from qwen_tts import Qwen3TTSModel

    started = time.time()
    model = Qwen3TTSModel.from_pretrained(
        MODEL_ID,
        device_map="cuda:0",
        dtype=torch.bfloat16,
        attn_implementation="sdpa",
    )
    prompt = model.create_voice_clone_prompt(
        ref_audio=str(args.ref_audio),
        ref_text=None if args.x_vector_only else args.ref_text,
        x_vector_only_mode=args.x_vector_only,
    )
    print(
        json.dumps(
            {
                "event": "loaded",
                "seconds": round(time.time() - started, 2),
                "max_new_tokens": args.max_new_tokens,
            }
        ),
        flush=True,
    )

    try:
        for index, job in enumerate(pending, start=1):
            output_path = args.output_dir / job["output"]
            generation_started = time.time()
            wavs, sample_rate = model.generate_voice_clone(
                text=job["text"],
                language="English",
                voice_clone_prompt=prompt,
                max_new_tokens=args.max_new_tokens,
                non_streaming_mode=True,
            )
            wav = wavs[0]
            duration = len(wav) / sample_rate
            if duration >= args.reject_duration_seconds:
                raise RuntimeError(
                    f"Job {job['id']} produced {duration:.3f}s, which suggests "
                    "generation reached the safety cap"
                )
            sf.write(output_path, wav, sample_rate)
            print(
                json.dumps(
                    {
                        "event": "generated",
                        "index": index,
                        "total": len(pending),
                        "id": job["id"],
                        "output": job["output"],
                        "duration_seconds": round(duration, 3),
                        "generation_seconds": round(time.time() - generation_started, 3),
                    }
                ),
                flush=True,
            )
    finally:
        del prompt, model
        torch.cuda.empty_cache()
        gc.collect()

    return 0


if __name__ == "__main__":
    sys.exit(main())
