import copy
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AutomationOpeningRestoreTest(unittest.TestCase):
    def test_restore_original_opening_only(self):
        base = ROOT / 'practice-materials/automation2026'
        original = json.loads((base / 'extension-v7.json').read_text())
        previous = json.loads((base / 'extension-v9.json').read_text())
        current = json.loads((base / 'extension-v10.json').read_text())
        expected = copy.deepcopy(previous)
        expected.update(version='10.0', source_deck='automation2026_13min_deck_v10.pptx',
                        source_script='automation2026_13min_script_v9.md')
        expected['overrides'][0] = original['overrides'][0]
        self.assertEqual(expected, current)


if __name__ == '__main__':
    unittest.main()
