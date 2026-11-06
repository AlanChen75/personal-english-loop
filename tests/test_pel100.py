import importlib.util
import unittest
import tempfile
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Pel100Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('pel100', ROOT/'scripts/build_pel100.py')
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)
        cls.source = (ROOT/'lessons/pel-100/source-v1.1.md').read_text()

    def test_exact_original_content_and_mapping(self):
        items = self.module.parse_source(self.source)
        self.assertEqual(len(items), 100)
        self.assertEqual(items[1]['origin_id'], '003')
        self.assertEqual(items[1]['unit_id'], 'pel100-origin-003')
        self.assertEqual(items[0]['sentences'][0], "Hi, I'm Sam.")
        self.assertEqual(items[90]['title_zh'], '介紹研究主題')
        self.assertEqual([x['canonical_order'] for x in items], list(range(1,101)))
        self.assertTrue(all(len(x['sentences']) == 4 for x in items))

    def test_rejects_missing_duplicate_or_malformed_records(self):
        for changed in [self.source.replace('### 100｜', '### 101｜'),
                        self.source.replace('**origin_id**：003', '**origin_id**：001'),
                        self.source.replace('Hi, I\'m Sam.', ''),
                        self.source.replace('- **T 時態**：現在式／目標表達', '')]:
            with self.subTest():
                with self.assertRaises(ValueError): self.module.parse_source(changed)

    def test_plan_keeps_display_and_pronunciation_separate(self):
        items = self.module.parse_source(self.source)
        plan = self.module.make_plan(items)
        self.assertEqual(len(plan['tracks']), 100)
        self.assertEqual(plan['tracks'][0]['stem'], 'pel100-001')
        self.assertEqual(plan['tracks'][-1]['stem'], 'pel100-100')
        self.assertEqual(plan['tracks'][70]['display_text'], items[70]['text'])
        self.assertEqual(len({j['output'] for j in plan['jobs']}),len(plan['jobs']))
        self.assertTrue(all(t['pause_between_chunks_ms']==350 for t in plan['tracks']))

    def test_cli_pilot_and_full_export(self):
        for selection,count in [('1,22,91',3),(None,100)]:
            with tempfile.TemporaryDirectory() as directory:
                args=['build_pel100.py','--work-root',directory]
                if selection: args += ['--episodes',selection]
                with patch('sys.argv',args): self.module.main()
                import json
                corpus=json.loads((Path(directory)/'corpus.json').read_text())
                self.assertEqual(len(corpus['units']),count)
                self.assertIn('source_sha256',corpus)

    def test_cli_invalid_selection(self):
        for selection in ['0','101','1,1']:
            with tempfile.TemporaryDirectory() as directory:
                with patch('sys.argv',['x','--work-root',directory,'--episodes',selection]):
                    with self.assertRaises(ValueError): self.module.main()

    def test_cli_assembly_writes_original_display_text(self):
        with tempfile.TemporaryDirectory() as directory:
            work=Path(directory)/'work'
            output=Path(directory)/'audio'
            output.mkdir()
            args=['x','--work-root',str(work),'--episodes','1','--assemble']
            with patch('sys.argv',args):
                with self.assertRaises(ValueError): self.module.main()
            with patch('sys.argv',args+['--cache',directory,'--output-root',str(output)]):
                with patch.object(self.module,'assemble_plan') as assemble:
                    self.module.main()
                    self.assertEqual(assemble.call_count,1)
            self.assertEqual((output/'pel100-001-display.txt').read_text().strip(),
                             self.module.parse_source(self.source)[0]['text'])

    def test_daily_replacement_is_bounded(self):
        records=self.module.parse_source(self.source)
        old={'version':2,'collections':[{'id':'conference','items':[{'title':'Keep'}]},
                                       {'id':'daily-practice','items':[{'title':'Old'}]}]}
        import copy
        snapshot=copy.deepcopy(old)
        result=self.module.replace_daily(old,records)
        self.assertEqual(old,snapshot)
        self.assertEqual(result['collections'][0],old['collections'][0])
        daily=result['collections'][1]
        self.assertEqual(len(daily['items']),100)
        self.assertEqual(daily['items'][0]['number'],1)
        self.assertEqual(daily['items'][-1]['number'],100)
        self.assertEqual(daily['items'][1]['unit_id'],'pel100-origin-003')
        with self.assertRaises(ValueError): self.module.replace_daily(old,records[:3])
        with self.assertRaises(ValueError): self.module.replace_daily({'collections':[]},records)

    def test_exported_units_and_coach_ids_match(self):
        import json
        records=self.module.parse_source(self.source)
        corpus=json.loads((ROOT/'lessons/pel-100/corpus.json').read_text())
        self.assertEqual(corpus['units'],records)
        index=json.loads((ROOT/'coach/coach-index.json').read_text())
        days=[x['day'] for x in index['lessons'] if 'day' in x]
        self.assertEqual(days,list(range(1,101)))
        for record in records:
            md=(ROOT/'lessons/pel-100/units'/f"{record['lesson_id']}.md").read_text()
            self.assertIn(record['text'],md)
            for key in ['T','L','E','unit_id','origin_id']:
                self.assertIn(record[key],md)
            self.assertEqual(index['lessons'][record['canonical_order']-1]['id'],record['unit_id'])


if __name__ == '__main__': unittest.main()
