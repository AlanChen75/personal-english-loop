import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/generate_cloned_audio.py"


def load_pipeline_module():
    spec = importlib.util.spec_from_file_location("cloned_audio_pipeline", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ClonedAudioPipelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = load_pipeline_module()

    def test_practice_prompts_receive_expected_silence(self):
        script = "Intro.\n\nYour turn.\n\nQuestion.\n\nThink and answer.\n"

        units = self.pipeline.build_speech_units(script)

        self.assertEqual([unit.pause_ms for unit in units], [4500, 6500])
        self.assertIn("Your turn.", units[0].text)
        self.assertIn("Think and answer.", units[1].text)

    def test_final_challenge_receives_long_pause(self):
        script = "Final challenge.\n\nTake your time and answer now.\n"

        units = self.pipeline.build_speech_units(script)

        self.assertEqual(len(units), 1)
        self.assertEqual(units[0].pause_ms, 12000)

    def test_regular_script_is_a_single_generation_unit(self):
        script = "First paragraph.\n\nSecond paragraph."

        units = self.pipeline.build_speech_units(script)

        self.assertEqual(len(units), 1)
        self.assertEqual(units[0].pause_ms, 0)
        self.assertEqual(units[0].text, script)

    def test_commute_plan_repeats_all_tracks_three_times(self):
        plan = self.pipeline.build_commute_plan()

        self.assertEqual(len(plan), 12)
        self.assertEqual(
            [entry.track for entry in plan[:4]],
            ["slow", "natural", "listen-repeat", "qa"],
        )
        self.assertTrue(all(entry.pause_after_ms == 2000 for entry in plan))

    def test_long_text_is_split_on_sentence_boundaries(self):
        text = (
            "This is the first sentence. This is the second sentence with more words. "
            "This is the third sentence."
        )

        chunks = self.pipeline.split_text_for_tts(text, max_chars=65)

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 65 for chunk in chunks))
        self.assertEqual(" ".join(chunks), text)

    def test_one_sentence_over_limit_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "single sentence"):
            self.pipeline.split_text_for_tts("A" * 81 + ".", max_chars=80)

    def test_long_sentence_with_words_is_split_without_losing_text(self):
        text = (
            "This single sentence contains enough ordinary words to require "
            "more than one reliable generation request."
        )

        chunks = self.pipeline.split_text_for_tts(text, max_chars=55)

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 55 for chunk in chunks))
        self.assertEqual(" ".join(chunks), text)


if __name__ == "__main__":
    unittest.main()
