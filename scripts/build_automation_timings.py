#!/usr/bin/env python3
"""Build sentence timing sidecars from aligned words and exact TTS chunk offsets."""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_automation_audio import prepare_spoken_text
from remote_align_tts_chunks import words


def sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())


def track_cues(track, chunks):
    script = track.get('script', track.get('spoken_text', ''))
    display = track.get('display_text', script)
    spoken_sentences = sentences(script)
    display_sentences = sentences(display)
    if len(spoken_sentences) != len(display_sentences):
        raise ValueError('Display and spoken sentence counts differ')
    aligned = []
    offset = 0.0
    for filename in track['chunks']:
        chunk = chunks[filename]
        aligned.extend({**word, 'start':word['start']+offset, 'end':word['end']+offset}
                       for word in chunk['words'])
        offset += chunk['duration_seconds'] + track['pause_between_chunks_ms']/1000
    expected = [words(prepare_spoken_text(s)) for s in spoken_sentences]
    if [word for sentence in expected for word in sentence] != [w['word'] for w in aligned]:
        raise ValueError(f'Script and alignment tokens differ: {track.get("stem", "track")}')
    cues = []
    cursor = 0
    for sentence, tokens in zip(display_sentences, expected):
        if not tokens:
            raise ValueError('Sentence contains no spoken tokens')
        region = aligned[cursor:cursor + len(tokens)]
        cues.append({'text':sentence, 'start':round(region[0]['start'],5),
                     'end':round(region[-1]['end'],5)})
        cursor += len(tokens)
    return cues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--alignment', type=Path, required=True)
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--audio-root', type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    alignment = json.loads(args.alignment.read_text())
    chunks = {c['output']: c for c in alignment['chunks']}
    for job in plan['jobs']:
        chunk = chunks[job['output']]
        if chunk['text'] != job['text']:
            raise ValueError(f'Changed TTS input: {job["id"]}')
        sha = hashlib.sha256((args.cache/job['output']).read_bytes()).hexdigest()
        if sha != chunk['wav_sha256']:
            raise ValueError(f'Changed WAV: {job["id"]}')
    for track in plan['tracks']:
        stem = track['stem']
        if track['kind'] == 'pronunciation-guide':
            print(f'{stem}: summary-only display, no sentence alignment')
            continue
        transcript = track.get('display_text',track['spoken_text']).strip()
        display_path = args.audio_root/(stem+'-display.txt')
        if not display_path.exists():
            display_path = args.audio_root/(stem+'.txt')
        if display_path.read_text().strip() != transcript:
            raise ValueError(f'Changed visible transcript: {stem}')
        if (args.audio_root/(stem+'.txt')).read_text().strip() != track['spoken_text']:
            raise ValueError(f'Changed TTS transcript: {stem}')
        cues = track_cues(track,chunks)
        duration = sum(chunks[f]['duration_seconds'] for f in track['chunks'])
        duration += (len(track['chunks'])-1)*track['pause_between_chunks_ms']/1000
        payload = {
            'version':1, 'method':alignment['method'], 'model':alignment['model'],
            'audio_sha256':hashlib.sha256((args.audio_root/(stem+'.mp3')).read_bytes()).hexdigest(),
            'transcript_sha256':hashlib.sha256(transcript.encode()).hexdigest(),
            'duration_seconds':round(duration,5), 'cues':cues,
        }
        output = args.audio_root/(stem+'.timings.json')
        output.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
        print(f'{stem}: {len(cues)} sentence cues, {duration:.2f}s')


if __name__ == '__main__':
    main()
