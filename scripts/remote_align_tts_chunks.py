#!/usr/bin/env python3
"""Align existing English TTS chunks on the GPU without changing their audio.

Uses the official TorchAudio CTC alignment API:
https://docs.pytorch.org/audio/stable/tutorials/ctc_forced_alignment_api_tutorial.html
Chunk offsets come from saved WAV frames, not text-length estimates.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path


def words(text):
    digits = ['zero','one','two','three','four','five','six','seven','eight','nine']
    def number(match):
        integer, dot, fraction = match.group(0).partition('.')
        if len(integer) != 1:
            raise ValueError('Spell out multi-digit integers for alignment')
        return digits[int(integer)] + (' point ' + ' '.join(digits[int(c)] for c in fraction) if dot else '')
    # Older Q&A prompts contain numeric decimals even though the answer text
    # spells them out. Normalize only the alignment input, preserving the audio.
    text = re.sub(r'\d+(?:\.\d+)?', number, text)
    return re.findall(r"[A-Z]+(?:'[A-Z]+)*", text.upper())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=Path, required=True)
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--limit', type=int)
    args = parser.parse_args()
    jobs = json.loads(args.jobs.read_text())['jobs']
    if args.limit:
        jobs = jobs[:args.limit]

    import soundfile as sf
    import torch
    import torchaudio
    torch.set_num_threads(4)
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    model = bundle.get_model().to('cuda').eval()
    labels = bundle.get_labels()
    dictionary = {char: i for i, char in enumerate(labels)}
    output = []
    for job in jobs:
        name = job['output']
        if not re.fullmatch(r'[a-f0-9]{64}\.wav', name):
            raise ValueError('Invalid chunk filename')
        path = args.cache / name
        wav, sample_rate = sf.read(path, dtype='float32')
        if wav.ndim != 1 or len(wav) == 0:
            raise ValueError(f'Expected nonempty mono audio: {name}')
        tokens = words(job['text'])
        transcript = '|'.join(tokens)
        targets = torch.tensor([[dictionary[c] for c in transcript]], dtype=torch.int64)
        waveform = torchaudio.functional.resample(
            torch.from_numpy(wav).unsqueeze(0), sample_rate, bundle.sample_rate
        )
        with torch.inference_mode():
            emissions, _ = model(waveform.to('cuda'))
            emissions = emissions.log_softmax(-1).cpu()
        aligned, scores = torchaudio.functional.forced_align(emissions, targets, blank=0)
        spans = torchaudio.functional.merge_tokens(aligned[0], scores[0].exp(), blank=0)
        if len(spans) != len(transcript):
            raise ValueError(f'Incomplete character alignment: {name}')
        ratio = (len(wav) / sample_rate) / emissions.shape[1]
        cursor = 0
        aligned_words = []
        for token in tokens:
            region = spans[cursor:cursor + len(token)]
            aligned_words.append({
                'word': token,
                'start': round(region[0].start * ratio, 5),
                'end': round(region[-1].end * ratio, 5),
                'score': round(sum(x.score for x in region) / len(region), 5),
            })
            cursor += len(token) + 1
        greedy = torch.unique_consecutive(emissions[0].argmax(-1)).tolist()
        decoded = ''.join(labels[i] for i in greedy if i != 0).replace('|', ' ')
        output.append({
            'output': name, 'text': job['text'],
            'wav_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'duration_seconds': len(wav) / sample_rate,
            'words': aligned_words, 'greedy_transcript': decoded,
        })
        print(json.dumps({'aligned': len(output), 'total': len(jobs),
                          'id': job['id'], 'decoded': decoded}), flush=True)
    args.output.write_text(json.dumps({
        'model': 'torchaudio/WAV2VEC2_ASR_BASE_960H',
        'method': 'CTC forced alignment on original TTS WAV chunks',
        'chunks': output,
    }, indent=2) + '\n')


if __name__ == '__main__':
    main()
