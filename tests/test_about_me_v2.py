import copy
import importlib.util
import json
from pathlib import Path
import unittest
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class AboutMeV2Test(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('about_v2', ROOT/'scripts/build_about_me_v2.py')
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.pack = json.loads((ROOT/'lessons/about-me-introduction/units-v2.json').read_text())

    def test_six_traceable_four_sentence_units(self):
        units = self.mod.validate_pack(self.pack)
        self.assertEqual([u['material_id'] for u in units], [f'B01-U{i:02d}' for i in range(1,7)])
        self.assertEqual(units[0]['sentences'][0], 'Hello, my name is Chung-Kuang Chen.')
        self.assertTrue(all(len(u['sentences']) == 4 for u in units))
        self.assertTrue(all(set(u['focus']) == {'T','L','E'} for u in units))
        self.assertTrue(all(u['source_refs'] and u['practice_question'] and u['transfer_task'] for u in units))
        combined = ' '.join(' '.join(u['sentences']) for u in units)
        for invented in ['doctoral student', 'twenty-five years', 'replace their judgment', 'improved accuracy']:
            self.assertNotIn(invented, combined)

    def test_invalid_pack_is_rejected(self):
        for field,value in [('units',[]),('lesson_id','B02'),('version','1.0')]:
            with self.subTest(field=field):
                with self.assertRaises(ValueError): self.mod.validate_pack({**self.pack,field:value})
        for field,value in [('material_id','B01-U00'),('sentences',['Incomplete']),('focus',{}),('source_refs',[]),('practice_question','')]:
            pack=copy.deepcopy(self.pack);pack['units'][0][field]=value
            with self.subTest(field=field):
                with self.assertRaises(ValueError): self.mod.validate_pack(pack)

    def test_tts_and_display_are_separate_and_bounded(self):
        plan=self.mod.make_plan(self.pack)
        self.assertEqual(len(plan['tracks']),6)
        self.assertEqual(plan['tracks'][0]['stem'],'about-v2-01')
        self.assertIn('AI',plan['tracks'][0]['display_text'])
        self.assertIn('A, I',plan['tracks'][0]['spoken_text'])
        self.assertNotIn('A, I',plan['tracks'][0]['display_text'])
        self.assertEqual(len({j['output'] for j in plan['jobs']}),len(plan['jobs']))
        self.assertTrue(all(len(j['text'])<=140 for j in plan['jobs']))

    def test_only_about_me_changes(self):
        manifest={'collections':[{'id':'about-me','items':[{'title':'old'}]},
                                 {'id':'daily-practice','items':[{'title':'keep'}]}]}
        before=copy.deepcopy(manifest)
        result=self.mod.replace_about(manifest,self.pack)
        self.assertEqual(manifest,before)
        self.assertEqual(result['collections'][1],before['collections'][1])
        self.assertEqual(len(result['collections'][0]['items']),6)
        self.assertTrue(all(i['timings'] for i in result['collections'][0]['items']))
        with self.assertRaises(ValueError): self.mod.replace_about({'collections':[]},self.pack)

    def test_pilot_and_cli_paths(self):
        self.assertEqual(len(self.mod.make_plan(self.pack,[1,5])['tracks']),2)
        for bad in [[],[0],[7],[1,1]]:
            with self.assertRaises(ValueError): self.mod.make_plan(self.pack,bad)
        with tempfile.TemporaryDirectory() as directory:
            work=Path(directory)/'work';output=Path(directory)/'audio';output.mkdir()
            argv=['x','--work-root',str(work),'--units','1,5']
            with patch('sys.argv',argv): self.mod.main()
            self.assertTrue((work/'xvector-plan.json').is_file())
            with patch('sys.argv',argv+['--assemble']):
                with self.assertRaises(ValueError): self.mod.main()
            with patch('sys.argv',argv+['--assemble','--cache',directory,'--output-root',str(output)]):
                with patch.object(self.mod,'assemble_plan') as assemble:
                    self.mod.main();self.assertEqual(assemble.call_count,1)
            self.assertIn('AI',(output/'about-v2-01-display.txt').read_text())

    def test_lesson_and_coach_follow_new_practice_contract(self):
        lesson=(ROOT/'lessons/about-me-introduction/lesson.md').read_text()
        for u in self.pack['units']:
            for sentence in u['sentences']: self.assertIn(sentence,lesson)
            self.assertIn(u['material_id'],lesson)
        self.assertIn('背誦正確不等於能力通過',lesson)
        self.assertIn('先自行回答',lesson)
        coach=(ROOT/'coach/CHATGPT_COACH.md').read_text()
        self.assertIn('For B01 version 2.0',coach)
        self.assertIn('T/L/E',coach)
        index=json.loads((ROOT/'coach/coach-index.json').read_text())
        item=next(x for x in index['lessons'] if x['id']=='B01')
        self.assertEqual(item['version'],'2.0')
        self.assertEqual(len(item['units']),6)


if __name__=='__main__': unittest.main()
