#!/usr/bin/env python3
"""Generate Personal English Loop audio with the ac-3090 cloned voice.

The reference voice is streamed over SSH and kept in memory. It is never
written into the repository. Generated chunks are cached so an interrupted
run can resume without repeating completed TTS calls.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.request
import wave
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SERVER = "http://100.108.119.78:3003"
DEFAULT_REF_AUDIO_SSH = "ac-3090:/home/ac3090/alan_voice.wav"
DEFAULT_REF_TEXT = (
    "大家好，歡迎收聽今天的節目，我是你們的主持人，今天我們要一起來聊聊"
)
MODEL_ID = "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
TRACKS = ("slow", "natural", "listen-repeat", "qa")
DAY_SLUGS = {
    1: "day-01-energy-management",
    2: "day-02-ai-iot-energy",
}
PAUSE_AFTER_LINE_MS = {
    "Your turn.": 4500,
    "Think and answer.": 6500,
    "Take your time and answer now.": 12000,
    "Listen one more time.": 1200,
}
EXPLICIT_PAUSE_RE = re.compile(r"\[\[slnc\s+(\d+)\]\]")
SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])\s+")
CLAUSE_BOUNDARY_RE = re.compile(r"(?<=[,;:])\s+")


class SpeechUnit(NamedTuple):
    text: str
    pause_ms: int


class CommuteEntry(NamedTuple):
    track: str
    pause_after_ms: int


def build_speech_units(script: str) -> list[SpeechUnit]:
    """Split a script where learner-response silence must be inserted."""
    script = script.strip()
    if not script:
        raise ValueError("Audio script is empty")

    if EXPLICIT_PAUSE_RE.search(script):
        units: list[SpeechUnit] = []
        cursor = 0
        for marker in EXPLICIT_PAUSE_RE.finditer(script):
            text = script[cursor : marker.start()].strip()
            if not text:
                raise ValueError("Silence marker must follow spoken text")
            units.append(SpeechUnit(text=text, pause_ms=int(marker.group(1))))
            cursor = marker.end()
        remaining = script[cursor:].strip()
        if remaining:
            units.append(SpeechUnit(text=remaining, pause_ms=0))
        return units

    matching_lines = {
        line.strip(): PAUSE_AFTER_LINE_MS[line.strip()]
        for line in script.splitlines()
        if line.strip() in PAUSE_AFTER_LINE_MS
    }
    if not matching_lines:
        return [SpeechUnit(text=script, pause_ms=0)]

    units = []
    buffer: list[str] = []
    for line in script.splitlines():
        buffer.append(line)
        stripped = line.strip()
        if stripped in PAUSE_AFTER_LINE_MS:
            text = "\n".join(buffer).strip()
            units.append(SpeechUnit(text=text, pause_ms=PAUSE_AFTER_LINE_MS[stripped]))
            buffer = []
    remaining = "\n".join(buffer).strip()
    if remaining:
        units.append(SpeechUnit(text=remaining, pause_ms=0))
    return units


def build_commute_plan() -> list[CommuteEntry]:
    """Three complete rounds, with two seconds after every component."""
    return [
        CommuteEntry(track=track, pause_after_ms=2000)
        for _round in range(3)
        for track in TRACKS
    ]


def split_text_for_tts(text: str, max_chars: int = 260) -> list[str]:
    """Split long prose into bounded sentence groups for reliable generation."""
    normalized = " ".join(text.split())
    if not normalized:
        raise ValueError("TTS text is empty")
    sentences = SENTENCE_BOUNDARY_RE.split(normalized)
    bounded_parts: list[str] = []
    for sentence in sentences:
        if len(sentence) <= max_chars:
            bounded_parts.append(sentence)
            continue
        clauses = CLAUSE_BOUNDARY_RE.split(sentence)
        for clause in clauses:
            if len(clause) <= max_chars:
                bounded_parts.append(clause)
                continue
            words = clause.split(" ")
            if any(len(word) > max_chars for word in words):
                raise ValueError(
                    f"A single sentence exceeds the {max_chars}-character TTS limit "
                    "and contains an unsplittable token"
                )
            current_part = ""
            for word in words:
                candidate = word if not current_part else f"{current_part} {word}"
                if len(candidate) <= max_chars:
                    current_part = candidate
                else:
                    bounded_parts.append(current_part)
                    current_part = word
            if current_part:
                bounded_parts.append(current_part)

    chunks: list[str] = []
    current = ""
    for part in bounded_parts:
        candidate = part if not current else f"{current} {part}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            chunks.append(current)
            current = part
    if current:
        chunks.append(current)
    return chunks


def run(command: list[str], *, capture_output: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        check=True,
        capture_output=capture_output,
        text=capture_output,
    )


def load_reference_audio(local_path: str | None, ssh_spec: str | None) -> bytes:
    if local_path:
        data = Path(local_path).expanduser().read_bytes()
    elif ssh_spec:
        if ":" not in ssh_spec:
            raise ValueError("--ref-audio-ssh must use HOST:/absolute/path.wav")
        host, remote_path = ssh_spec.split(":", 1)
        if not host or not remote_path.startswith("/"):
            raise ValueError("--ref-audio-ssh must use HOST:/absolute/path.wav")
        remote_command = (
            "python3 -c "
            + shlex.quote(
                "import sys; "
                f"sys.stdout.buffer.write(open({remote_path!r}, 'rb').read())"
            )
        )
        result = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", host, remote_command],
            check=True,
            capture_output=True,
        )
        data = result.stdout
    else:
        raise ValueError("Provide --ref-audio or --ref-audio-ssh")

    if len(data) < 1000 or not data.startswith(b"RIFF"):
        raise ValueError("Reference audio is not a valid non-empty WAV file")
    return data


def healthcheck(server: str) -> dict:
    with urllib.request.urlopen(f"{server.rstrip('/')}/health", timeout=20) as response:
        payload = json.loads(response.read())
    if payload.get("status") != "ok":
        raise RuntimeError(f"TTS health check failed: {payload}")
    return payload


def request_clone(
    server: str,
    text: str,
    ref_audio: bytes,
    ref_text: str,
    timeout: int,
) -> tuple[bytes, dict[str, str]]:
    payload = json.dumps(
        {
            "text": text,
            "language": "English",
            "ref_audio_base64": base64.b64encode(ref_audio).decode("ascii"),
            "ref_text": ref_text,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{server.rstrip('/')}/clone",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read(), {key.lower(): value for key, value in response.headers.items()}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"TTS request failed with HTTP {exc.code}: {body}") from exc


def inspect_wav(path: Path) -> tuple[tuple[int, int, int], float]:
    with wave.open(str(path), "rb") as wav_file:
        if wav_file.getcomptype() != "NONE":
            raise ValueError(f"Expected PCM WAV, got {wav_file.getcomptype()}: {path}")
        signature = (
            wav_file.getnchannels(),
            wav_file.getsampwidth(),
            wav_file.getframerate(),
        )
        duration = wav_file.getnframes() / wav_file.getframerate()
    return signature, duration


def concatenate_wavs(parts: list[tuple[Path, int]], output_path: Path) -> float:
    if not parts:
        raise ValueError("No WAV parts to concatenate")

    expected_signature = None
    total_frames = 0
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_path), "wb") as output:
        for part_path, pause_after_ms in parts:
            with wave.open(str(part_path), "rb") as source:
                signature = (
                    source.getnchannels(),
                    source.getsampwidth(),
                    source.getframerate(),
                )
                if source.getcomptype() != "NONE":
                    raise ValueError(f"Only PCM WAV is supported: {part_path}")
                if expected_signature is None:
                    expected_signature = signature
                    output.setnchannels(signature[0])
                    output.setsampwidth(signature[1])
                    output.setframerate(signature[2])
                elif signature != expected_signature:
                    raise ValueError(
                        f"WAV format mismatch: {part_path} is {signature}, expected {expected_signature}"
                    )
                frames = source.readframes(source.getnframes())
                output.writeframes(frames)
                total_frames += source.getnframes()

            if pause_after_ms:
                channels, sample_width, sample_rate = expected_signature
                silence_frames = round(sample_rate * pause_after_ms / 1000)
                output.writeframes(b"\x00" * silence_frames * channels * sample_width)
                total_frames += silence_frames

    return total_frames / expected_signature[2]


def encode_mp3(raw_wav: Path, output_mp3: Path, *, slow: bool) -> None:
    filters = []
    if slow:
        filters.append("atempo=0.88")
    filters.append("loudnorm=I=-16:TP=-1.5:LRA=11")
    output_mp3.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(raw_wav),
            "-af",
            ",".join(filters),
            "-ar",
            "24000",
            "-ac",
            "1",
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "96k",
            str(output_mp3),
        ]
    )


def probe_audio(path: Path) -> dict:
    result = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size,bit_rate:stream=codec_name,sample_rate,channels",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
    )
    return json.loads(result.stdout)


def generate_chunk(
    *,
    server: str,
    text: str,
    ref_audio: bytes,
    ref_text: str,
    cache_dir: Path,
    timeout: int,
) -> Path:
    cache_key = hashlib.sha256(
        ref_audio + ref_text.encode("utf-8") + text.encode("utf-8")
    ).hexdigest()
    output = cache_dir / f"{cache_key}.wav"
    if output.exists():
        inspect_wav(output)
        return output

    wav_bytes, headers = request_clone(server, text, ref_audio, ref_text, timeout)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(wav_bytes)
    _signature, duration = inspect_wav(output)
    generation_time = headers.get("x-generation-time", "unknown")
    print(f"      generated {duration:.1f}s audio in {generation_time}s")
    return output


def generate_track(
    *,
    server: str,
    source_path: Path,
    track: str,
    ref_audio: bytes,
    ref_text: str,
    cache_dir: Path,
    raw_output: Path,
    timeout: int,
) -> float:
    units = build_speech_units(source_path.read_text(encoding="utf-8"))
    print(f"    {track}: {len(units)} generation unit(s)")
    parts = []
    for index, unit in enumerate(units, start=1):
        print(f"      [{index}/{len(units)}] {len(unit.text)} characters")
        chunk = generate_chunk(
            server=server,
            text=unit.text,
            ref_audio=ref_audio,
            ref_text=ref_text,
            cache_dir=cache_dir,
            timeout=timeout,
        )
        parts.append((chunk, unit.pause_ms))
    return concatenate_wavs(parts, raw_output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, nargs="+", default=[1, 2], choices=DAY_SLUGS)
    parser.add_argument("--server", default=DEFAULT_SERVER)
    parser.add_argument("--ref-audio")
    parser.add_argument("--ref-audio-ssh", default=DEFAULT_REF_AUDIO_SSH)
    parser.add_argument("--ref-text", default=DEFAULT_REF_TEXT)
    parser.add_argument("--output-root", type=Path, default=ROOT / "outputs/cloned-audio")
    parser.add_argument("--work-root", type=Path, default=ROOT / "work/cloned-audio")
    parser.add_argument("--timeout", type=int, default=900)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    health = healthcheck(args.server)
    print(f"TTS server healthy: {health}")
    ref_audio = load_reference_audio(args.ref_audio, args.ref_audio_ssh)
    ref_hash = hashlib.sha256(ref_audio).hexdigest()
    print(f"Reference voice: {len(ref_audio)} bytes, sha256={ref_hash[:12]}…")

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": MODEL_ID,
        "server": args.server,
        "language": "English",
        "reference_audio_sha256": ref_hash,
        "source_commit": run(
            ["git", "rev-parse", "HEAD"], capture_output=True
        ).stdout.strip(),
        "days": {},
    }

    for day in args.days:
        day_label = f"day-{day:02d}"
        source_dir = ROOT / "lessons" / DAY_SLUGS[day] / "audio-scripts"
        raw_dir = args.work_root / day_label / "raw"
        cache_dir = args.work_root / "cache"
        output_dir = args.output_root / day_label
        raw_tracks: dict[str, Path] = {}
        day_manifest = {"tracks": {}}
        print(f"\n{day_label}")

        for track in TRACKS:
            source_path = source_dir / f"{track}.txt"
            raw_wav = raw_dir / f"{day_label}-{track}.wav"
            output_mp3 = output_dir / f"{day_label}-{track}.mp3"
            raw_duration = generate_track(
                server=args.server,
                source_path=source_path,
                track=track,
                ref_audio=ref_audio,
                ref_text=args.ref_text,
                cache_dir=cache_dir,
                raw_output=raw_wav,
                timeout=args.timeout,
            )
            encode_mp3(raw_wav, output_mp3, slow=(track == "slow"))
            raw_tracks[track] = raw_wav
            day_manifest["tracks"][track] = {
                "source": str(source_path.relative_to(ROOT)),
                "raw_duration_seconds": round(raw_duration, 3),
                "file": str(output_mp3.relative_to(ROOT)),
                "probe": probe_audio(output_mp3),
            }

        commute_parts = [
            (raw_tracks[entry.track], entry.pause_after_ms)
            for entry in build_commute_plan()
        ]
        commute_raw = raw_dir / f"{day_label}-commute-pack.wav"
        commute_duration = concatenate_wavs(commute_parts, commute_raw)
        commute_mp3 = output_dir / f"{day_label}-commute-pack.mp3"
        encode_mp3(commute_raw, commute_mp3, slow=False)
        day_manifest["tracks"]["commute-pack"] = {
            "rounds": 3,
            "pause_after_each_component_ms": 2000,
            "raw_duration_seconds": round(commute_duration, 3),
            "file": str(commute_mp3.relative_to(ROOT)),
            "probe": probe_audio(commute_mp3),
        }
        manifest["days"][day_label] = day_manifest

    args.output_root.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output_root / "generation-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nDone. Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
