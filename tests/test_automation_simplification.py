import copy
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPLACEMENTS = {
  "3": [
    [
      "We used a chronological 50%, 20%, 30% split for calibration, validation, and test.",
      "We split the data in time order. The first 50% is for calibration. The next 20% is for validation. The last 30% is for testing."
    ],
    [
      "We used a chronological fifty, twenty, thirty percent split for calibration, validation, and test.",
      "We split the data in time order. The first fifty percent is for calibration. The next twenty percent is for validation. The last thirty percent is for testing."
    ]
  ],
  "6": [
    [
      "The reported macro MCC is the arithmetic mean of the 9 device MCC values.",
      "To calculate macro MCC, we add the 9 MCC scores and divide by 9."
    ],
    [
      "The reported macro MCC is the arithmetic mean of the nine device MCC values.",
      "To calculate macro MCC, we add the nine MCC scores and divide by nine."
    ]
  ],
  "9": [
    [
      "This is an exploratory validation-only audit. We checked whether each wide-range joint configuration met every active engineering limit.",
      "Here, we use only validation data for an extra check. We check how many candidates meet all the engineering limits."
    ],
    [
      "These figures describe candidate feasibility.",
      "These numbers show whether candidates meet the engineering limits."
    ],
    [
      "They add no new sealed-test result.",
      "This check adds no new test results."
    ]
  ]
}


class AutomationSimplificationTest(unittest.TestCase):
    def test_only_user_approved_passages_change(self):
        before = json.loads((ROOT / 'practice-materials/automation2026/extension-v8.json').read_text())
        after = json.loads((ROOT / 'practice-materials/automation2026/extension-v9.json').read_text())
        expected = copy.deepcopy(before)
        expected['version'] = '9.0'
        expected['source_deck'] = 'automation2026_13min_deck_v9.pptx'
        expected['source_script'] = 'automation2026_13min_script_v8.md'
        for item in expected['overrides']:
            for old, new in REPLACEMENTS.get(str(item['slide']), []):
                for field in ['spoken_transcript', 'display_transcript']:
                    item[field] = item[field].replace(old, new)
        self.assertEqual(expected, after)


if __name__ == '__main__':
    unittest.main()
