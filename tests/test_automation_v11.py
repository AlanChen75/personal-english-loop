"""2026-11-07 approved oral simplification, not a rewrite of the research."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'practice-materials/automation2026'


class AutomationV11Test(unittest.TestCase):
    def setUp(self):
        self.before = json.loads((BASE / 'extension-v10.json').read_text())
        self.after = json.loads((BASE / 'extension-v11.json').read_text())
        self.slides = {x['slide']: x for x in self.after['overrides']}

    def test_scope_and_identity_unchanged(self):
        changed = {a['slide'] for a, b in zip(self.before['overrides'], self.after['overrides']) if a != b}
        self.assertEqual(changed, {3, 5, 6, 8, 9, 10, 12})
        for field in ('additional_slides', 'appendices', 'presentation_identity'):
            self.assertEqual(self.before[field], self.after[field])
        self.assertEqual(self.after['version'], '11.0')

    def test_approved_sentence_and_research_boundaries(self):
        s = {n: x['display_transcript'] for n, x in self.slides.items()}
        self.assertIn('We do this extra analysis after selection.', s[10])
        self.assertNotIn('post-hoc diagnostics', s[10])
        for text in ('validation labels', 'label-free selector', '0.3150', '0.2786', 'equal dataset weights'):
            self.assertIn(text, s[10])
        for text in ('5 LLM test seeds', '1 LHS test seed', '20 LHS validation seeds', 'no repeated test result'):
            self.assertIn(text, s[8])
        for text in ('2.22%', '6%', 'This check adds no new test results.', 'none of the selected unbounded configurations'):
            self.assertIn(text, s[9])
        for text in ('test labels', 'macro MCC', '9 scores and divide by 9', 'equal weight'):
            self.assertIn(text, s[6])
        for text in ('generation and reconstruction', 'engineering assumptions', 'true feasible region'):
            self.assertIn(text, s[5])
        self.assertIn('correct bounds, bounds near the boundary, and incorrect bounds', s[12])
        self.assertIn('candidate limits and reconstruction caps separately', s[12])

    def test_sentence_counts_and_shorter_total(self):
        import sys
        sys.path.insert(0, str(ROOT / 'scripts'))
        from build_automation_timings import sentences
        for item in self.after['overrides']:
            self.assertEqual(len(sentences(item['spoken_transcript'])), len(sentences(item['display_transcript'])))
        old = sum(len(x['display_transcript'].split()) for x in self.before['overrides'])
        new = sum(len(x['display_transcript'].split()) for x in self.after['overrides'])
        self.assertLess(new, old)
        self.assertGreater(new, old * .5)


if __name__ == '__main__':
    unittest.main()
