import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/generate_conference_audio.py"


def load_module():
    spec = importlib.util.spec_from_file_location("conference_audio", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ConferenceAudioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = load_module()

    def test_spoken_text_expands_required_pronunciations(self):
        source = "Pseudo-NILM uses TECA on IMDELD, WELTRON, HIPE, and Case1."

        spoken = self.pipeline.prepare_spoken_text(source)

        self.assertEqual(
            spoken,
            "pseudo nil-em uses tee ee see ay on eye em dee ee el dee, well-tron, hype, and Case one.",
        )

    def test_extracts_slide_scripts_without_executing_source(self):
        source = "ENGLISH_SLIDES = [{'number': 1, 'title': 'One', 'script': 'Hello.'}]\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "build_documents.py"
            path.write_text(source, encoding="utf-8")

            slides = self.pipeline.load_english_slides(path)

        self.assertEqual(slides[0]["number"], 1)
        self.assertEqual(slides[0]["script"], "Hello.")

    def test_builds_stable_xvector_jobs_with_clean_terminal_punctuation(self):
        slides = [
            {
                "number": 1,
                "title": "Opening",
                "script": "A practical question: When should it stop?",
            }
        ]

        plan = self.pipeline.build_xvector_plan(
            slides,
            pronunciation_guide="N I L M.",
            max_chars=24,
        )

        self.assertEqual(plan["generation_mode"], "x-vector-only")
        self.assertEqual(len(plan["tracks"]), 2)
        self.assertTrue(plan["jobs"])
        self.assertTrue(all(job["text"].endswith((".", "!", "?")) for job in plan["jobs"]))
        self.assertTrue(all(",." not in job["text"] for job in plan["jobs"]))
        self.assertTrue(
            all(job["output"].endswith(".wav") and len(job["output"]) == 68 for job in plan["jobs"])
        )


if __name__ == "__main__":
    unittest.main()
