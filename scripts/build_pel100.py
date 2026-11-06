#!/usr/bin/env python3
"""Import the frozen OLMCP corpus without rewriting its four-sentence lessons."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from generate_automation_audio import prepare_spoken_text
from generate_library_audio import build_xvector_plan, write_plan, assemble_plan

SOURCE = ROOT/'lessons/pel-100/source-v1.1.md'
SOURCE_URL = 'https://github.com/AlanChen75/knowledge-base/blob/3af9420a6e4876e71b202cbc1b763f5209b8310b/raw/2026-11/20261106074615-mcp-note.md'
REF_SHA = 'f191156890b60d505173f5ef33e0a72736297728f938f5884f244e86efbee8ba'


def parse_source(source):
    blocks = re.findall(r'^### (\d{3})｜([^\n]+)\n(.*?)(?=^### |^## |\Z)', source, re.M|re.S)
    records = []
    for number, title, body in blocks:
        title_match = re.fullmatch(r'(.+)（(.+)）', title)
        fields = dict(re.findall(r'^- \*\*(.+?)\*\*：(.+)$', body, re.M))
        required = {'origin_id', 'English（4句）', 'T 時態', 'L 邏輯', 'E 表達'}
        if not title_match or not required.issubset(fields):
            raise ValueError(f'Incomplete lesson {number}')
        text = fields['English（4句）']
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) != 4 or any(not s or s[-1] not in '.?!' for s in sentences):
            raise ValueError(f'Expected four full sentences: {number}')
        origin = fields['origin_id']
        if not re.fullmatch(r'\d{3}', origin): raise ValueError('Invalid origin ID')
        records.append(dict(unit_id=f'pel100-origin-{origin}', lesson_id=f'pel100-{number}',
                            canonical_order=int(number), origin_id=origin,
                            stage=(int(number)-1)//20+1, title_zh=title_match[1],
                            title_en=title_match[2], text=text, sentences=sentences,
                            T=fields['T 時態'], L=fields['L 邏輯'], E=fields['E 表達']))
    if [r['canonical_order'] for r in records] != list(range(1,101)):
        raise ValueError('Expected ordered lessons 001–100')
    if {r['origin_id'] for r in records} != {f'{i:03d}' for i in range(1,101)}:
        raise ValueError('Missing or duplicate origin IDs')
    return records


def make_plan(records):
    items = [dict(number=r['canonical_order'], title=f"{r['title_zh']} · {r['title_en']}",
                  stem=r['lesson_id'], source='lessons/pel-100/source-v1.1.md',
                  spoken_text=prepare_spoken_text(r['text'])) for r in records]
    plan = build_xvector_plan({'collections':[{'id':'daily-practice','title':'每日練習 · 100 集','items':items}]})
    return {**plan, 'tracks':[{**track, 'script':record['text'], 'display_text':record['text'],
                              'kind':'lesson', 'pause_between_chunks_ms':350}
                             for track,record in zip(plan['tracks'],records)]}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def replace_daily(manifest, records):
    """Only replace the daily list; never delete old assets or mutate other collections."""
    if len(records)!=100 or [r['canonical_order'] for r in records]!=list(range(1,101)):
        raise ValueError('Publishing requires all 100 ordered episodes')
    collections=manifest.get('collections',[])
    if sum(c['id']=='daily-practice' for c in collections)!=1:
        raise ValueError('Expected exactly one daily-practice collection')
    items=[]
    for r in records:
        stem='learning/pel100/'+r['lesson_id']
        items.append(dict(number=r['canonical_order'],
                          title=f"{r['title_zh']} · {r['title_en']}",unit_id=r['unit_id'],
                          audio=stem+'.mp3',spoken_transcript=stem+'.txt',
                          display_transcript=stem+'-display.txt',timings=stem+'.timings.json'))
    return {**manifest,'collections':[
        {**c,'title':'每日練習 · 100 集','items':items} if c['id']=='daily-practice' else c
        for c in collections]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-root',type=Path,required=True)
    parser.add_argument('--episodes',help='Optional comma-separated pilot episode numbers')
    parser.add_argument('--assemble',action='store_true')
    parser.add_argument('--cache',type=Path)
    parser.add_argument('--output-root',type=Path)
    args=parser.parse_args()
    records=parse_source(SOURCE.read_text())
    if args.episodes:
        selected=[int(x) for x in args.episodes.split(',')]
        if len(set(selected))!=len(selected) or any(x<1 or x>100 for x in selected):
            raise ValueError('Episodes must be distinct numbers in 1–100')
        records=[r for r in records if r['canonical_order'] in selected]
    plan=make_plan(records)
    write_plan(plan,args.work_root)
    catalog=dict(version='1.1',source_url=SOURCE_URL,
                 source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                 source_type='original teaching scenarios, not personal biography or research results',
                 level_status='A2–B1 design intent; not professionally CEFR calibrated',units=records)
    catalog_path=args.work_root/'corpus.json'
    write_json(catalog_path,catalog)
    print(f"Prepared {len(records)} episodes / {len(plan['jobs'])} unique TTS chunks",flush=True)
    if args.assemble:
        if not args.cache or not args.output_root: raise ValueError('Assembly requires cache and output-root')
        assemble_plan(plan=plan,cache_dir=args.cache,work_root=args.work_root,
                      output_root=args.output_root,catalog_path=catalog_path,reference_audio_sha256=REF_SHA)
        for track in plan['tracks']:
            (args.output_root/(track['stem']+'-display.txt')).write_text(track['display_text']+'\n')
        print('Audio assembly complete',flush=True)


if __name__=='__main__': main()
