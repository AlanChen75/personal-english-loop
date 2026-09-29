import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CoachPromptTest(unittest.TestCase):
    def test_today_stop_phrase_triggers_verified_sb_save(self):
        prompt = (ROOT / "coach/CHATGPT_COACH.md").read_text(encoding="utf-8")

        self.assertIn("今天到此", prompt)
        self.assertIn("立即結束", prompt)
        self.assertIn("找不到當週週誌", prompt)
        self.assertIn("建立", prompt)
        self.assertIn("讀回", prompt)
        self.assertIn("不要再問下一題", prompt)


if __name__ == "__main__":
    unittest.main()
