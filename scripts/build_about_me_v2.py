#!/usr/bin/env python3
"""Build only the six personalized B01 units; preserve every other collection."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from generate_library_audio import build_xvector_plan, write_plan, assemble_plan

SOURCE = ROOT/'lessons/about-me-introduction/units-v2.json'
REF_SHA = 'f191156890b60d505173f5ef33e0a72736297728f938f5884f244e86efbee8ba'


def validate_pack(pack):
    units = pack.get('units', [])
    if pack.get('lesson_id') != 'B01' or pack.get('version') != '2.0' or len(units) != 6:
        raise ValueError('Expected B01 version 2.0 with six units')
    for n, unit in enumerate(units, 1):
        if unit.get('number') != n or unit.get('material_id') != f'B01-U{n:02d}':
            raise ValueError('Unit numbers and stable material IDs must match')
        sentences = unit.get('sentences', [])
        if len(sentences) != 4 or any(not isinstance(s, str) or not s.strip() or s[-1] != '.' for s in sentences):
            raise ValueError('Each unit requires four complete sentences')
        if set(unit.get('focus', {})) != {'T','L','E'} or any(not value for value in unit['focus'].values()):
            raise ValueError('Missing T/L/E focus')
        for field in ['title','source_refs','recombine_task','practice_question','transfer_task','related_pel100']:
            if not unit.get(field): raise ValueError(f'Missing {field}')
    return units


def make_plan(pack, numbers=None):
    units = validate_pack(pack)
    if numbers is not None:
        if not numbers or len(set(numbers)) != len(numbers) or any(n not in range(1,7) for n in numbers):
            raise ValueError('Pilot numbers must be distinct integers 1–6')
        units = [u for u in units if u['number'] in numbers]
    items = []
    for unit in units:
        display = ' '.join(unit['sentences'])
        # 2026-11-06: spell out initials only in TTS, never in the visible script.
        spoken = re.sub(r'\bAI\b', 'A, I', display)
        items.append(dict(number=unit['number'],title=unit['title'],
                          stem=f"about-v2-{unit['number']:02d}",
                          source='lessons/about-me-introduction/units-v2.json',
                          spoken_text=spoken,display_text=display))
    plan = build_xvector_plan({'collections':[{'id':'about-me','title':'自我介紹','items':items}]})
    return {**plan,'tracks':[{**t,'script':t['spoken_text'],'kind':'lesson',
                             'pause_between_chunks_ms':350} for t in plan['tracks']]}


def replace_about(manifest, pack):
    units = validate_pack(pack)
    collections = manifest.get('collections', [])
    if sum(c['id'] == 'about-me' for c in collections) != 1:
        raise ValueError('Expected exactly one about-me collection')
    items=[]
    for unit in units:
        stem=f"learning/about-v2/about-v2-{unit['number']:02d}"
        items.append(dict(number=unit['number'],title=unit['title'],
                          material_id=unit['material_id'],audio=stem+'.mp3',
                          spoken_transcript=stem+'.txt',display_transcript=stem+'-display.txt',
                          timings=stem+'.timings.json'))
    return {**manifest,'collections':[{**c,'title':'自我介紹','items':items}
                                      if c['id']=='about-me' else c for c in collections]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-root',type=Path,required=True)
    parser.add_argument('--units',help='Optional comma-separated pilot unit numbers')
    parser.add_argument('--assemble',action='store_true')
    parser.add_argument('--cache',type=Path)
    parser.add_argument('--output-root',type=Path)
    args=parser.parse_args()
    pack=json.loads(SOURCE.read_text())
    plan=make_plan(pack,[int(x) for x in args.units.split(',')] if args.units else None)
    write_plan(plan,args.work_root)
    print(f"Prepared {len(plan['tracks'])} units / {len(plan['jobs'])} chunks",flush=True)
    if args.assemble:
        if not args.cache or not args.output_root: raise ValueError('Assembly requires cache and output-root')
        assemble_plan(plan=plan,cache_dir=args.cache,work_root=args.work_root,
                      output_root=args.output_root,catalog_path=SOURCE,reference_audio_sha256=REF_SHA)
        for t in plan['tracks']:
            (args.output_root/(t['stem']+'-display.txt')).write_text(t['display_text']+'\n')
        print('Audio assembly complete',flush=True)


if __name__=='__main__': main()
