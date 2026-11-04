import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AutomationIdentityTest(unittest.TestCase):
    def test_builder_keeps_institutional_source_out_of_speaker_notes(self):
        builder = (ROOT / 'scripts/build_automation_identity.mjs').read_text()
        self.assertNotIn('Institutional identity source:', builder)

    def test_opening_and_identity_revision_preserves_research(self):
        before = json.loads((ROOT / 'practice-materials/automation2026/extension-v7.json').read_text())
        after = json.loads((ROOT / 'practice-materials/automation2026/extension-v8.json').read_text())
        self.assertEqual(before['overrides'][1:], after['overrides'][1:])
        self.assertEqual(before['additional_slides'], after['additional_slides'])
        self.assertEqual(before['appendices'], after['appendices'])
        opening = after['overrides'][0]
        self.assertEqual(opening['spoken_transcript'], opening['display_transcript'])
        for phrase in ['Chung-Kuang Chen', 'doctoral student', 'Graduate Institute of Intelligent Manufacturing Technology', 'National Taiwan University of Science and Technology']:
            self.assertIn(phrase, opening['display_transcript'])
        self.assertNotIn('Our result is conditional', opening['display_transcript'])
        self.assertEqual(after['presentation_identity']['header_scope'], 'all_slides')
        self.assertIn('ntust.edu.tw', after['presentation_identity']['header_source'])


if __name__ == '__main__':
    unittest.main()
