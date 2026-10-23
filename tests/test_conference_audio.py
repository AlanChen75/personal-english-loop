import importlib.util
import json
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

    def test_spoken_text_expands_qa_terms_and_contact_email(self):
        source = (
            "This is a NILM question. Please email me at "
            "d11351004@mail.ntust.edu.tw."
        )

        spoken = self.pipeline.prepare_spoken_text(source)

        self.assertEqual(
            spoken,
            "This is a nil-em question. Please email me at "
            "d one one three five one zero zero four at mail dot "
            "N T U S T dot E D U dot T W.",
        )

    def test_loads_supplemental_script_with_required_sequence(self):
        source = {
            "source_document": "script-v3.docx",
            "items": [
                {
                    "number": 11,
                    "title": "Thank you and Q&A",
                    "script": "Thank you for listening.",
                    "slide_image": "slides/slide-15.png",
                },
                {
                    "number": 12,
                    "title": "Is this method training-free?",
                    "script": "The main method does not train a supervised model.",
                },
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "supplement.json"
            path.write_text(json.dumps(source), encoding="utf-8")

            items = self.pipeline.load_supplemental_slides(path)

        self.assertEqual([item["number"] for item in items], [11, 12])
        self.assertEqual(items[0]["slide_image"], "slides/slide-15.png")
        self.assertEqual(items[1]["title"], "Is this method training-free?")

    def test_rejects_invalid_supplemental_script_boundaries(self):
        cases = [
            ({}, "items list"),
            ({"items": []}, "must not be empty"),
            ({"items": [{"number": 11, "title": "Missing script"}]}, "needs number"),
            (
                {"items": [{"number": 0, "title": "Invalid number", "script": "Text."}]},
                "positive integers",
            ),
            (
                {"items": [{"number": 11, "title": " ", "script": "Text."}]},
                "titles must be non-empty",
            ),
            (
                {"items": [{"number": 11, "title": "Empty", "script": " "}]},
                "scripts must be non-empty",
            ),
            (
                {
                    "items": [
                        {
                            "number": 11,
                            "title": "Unsafe image",
                            "script": "Text.",
                            "slide_image": "../private.png",
                        }
                    ]
                },
                "safe relative path",
            ),
            (
                {
                    "items": [
                        {"number": 11, "title": "First", "script": "Text."},
                        {"number": 13, "title": "Gap", "script": "Text."},
                    ]
                },
                "consecutive and ordered",
            ),
        ]

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "supplement.json"
            for payload, message in cases:
                with self.subTest(message=message):
                    path.write_text(json.dumps(payload), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, message):
                        self.pipeline.load_supplemental_slides(path)

    def test_plan_keeps_canonical_text_separate_from_tts_pronunciation(self):
        canonical = "IMDELD uses TECA for industrial Pseudo-NILM at zero point seven."
        slides = [{"number": 4, "title": "Dispatch", "script": canonical}]

        plan = self.pipeline.build_xvector_plan(
            slides,
            pronunciation_guide="I M D E L D.",
            max_chars=140,
        )

        slide_track = plan["tracks"][0]
        self.assertEqual(
            slide_track["display_text"],
            "IMDELD uses TECA for industrial Pseudo-NILM at 0.7.",
        )
        self.assertIn("eye em dee ee el dee", slide_track["spoken_text"])
        self.assertNotEqual(slide_track["display_text"], slide_track["spoken_text"])

    def test_display_text_formats_spoken_numbers_as_digits(self):
        source = (
            "The TECA reference is zero point seven. "
            "IMDELD reaches zero point seven six one nine. "
            "Monitored devices contribute only three point eight three percent. "
            "Segment F1 remains between zero point one five and zero point three two."
        )

        display = self.pipeline.prepare_display_text(source)

        self.assertEqual(
            display,
            "The TECA reference is 0.7. "
            "IMDELD reaches 0.7619. "
            "Monitored devices contribute only 3.83%. "
            "Segment F1 remains between 0.15 and 0.32.",
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

    def test_published_slide_07_uses_approved_bootstrap_wording(self):
        conference_dir = ROOT / "conference/cacs2026-pseudonilm"
        spoken = (conference_dir / "slide-07-main-teca-results.txt").read_text(
            encoding="utf-8"
        )
        display = (conference_dir / "slide-07-main-teca-results-display.txt").read_text(
            encoding="utf-8"
        )
        player = (conference_dir / "index.html").read_text(encoding="utf-8")

        self.assertIn(
            "The lowest bootstrap lower bound is zero point seven zero six one "
            "for the activity chunks used in this analysis.",
            spoken,
        )
        self.assertIn(
            "The lowest bootstrap lower bound is 0.7061 "
            "for the activity chunks used in this analysis.",
            display,
        )
        self.assertNotIn("eligible activity-bearing chunks", spoken)
        self.assertNotIn("eligible activity-bearing chunks", display)
        self.assertIn(
            "The lowest bootstrap lower bound is 0.7061 "
            "for the activity chunks used in this analysis.",
            player,
        )
        self.assertNotIn("eligible activity-bearing chunks", player)

    def test_published_conference_places_closing_before_combined_qa(self):
        conference_dir = ROOT / "conference/cacs2026-pseudonilm"
        manifest = json.loads(
            (conference_dir / "library-manifest.json").read_text(encoding="utf-8")
        )
        conference = next(
            collection
            for collection in manifest["collections"]
            if collection["id"] == "conference"
        )
        items = conference["items"]

        self.assertEqual(items[9]["title"], "Supported claims and limits")
        self.assertEqual(items[10]["number"], 11)
        self.assertEqual(items[10]["title"], "Thank you and Q&A")
        self.assertEqual(items[10]["slide_image"], "slides/slide-15.png")
        self.assertEqual(items[11]["number"], 12)
        self.assertEqual(items[11]["title"], "Q&A response pack")
        self.assertEqual(len(items), 12)
        for item in items[10:]:
            self.assertTrue((conference_dir / item["audio"]).is_file())
            self.assertTrue((conference_dir / item["spoken_transcript"]).is_file())
            self.assertTrue((conference_dir / item["display_transcript"]).is_file())

        closing = (conference_dir / items[10]["display_transcript"]).read_text(
            encoding="utf-8"
        )
        self.assertEqual(
            closing.strip(),
            "Thank you for listening. I am happy to take your questions. "
            "If we do not have enough time, please email me at "
            "d11351004@mail.ntust.edu.tw.",
        )

        qa_pack = (conference_dir / items[11]["display_transcript"]).read_text(
            encoding="utf-8"
        )
        self.assertIn("Question one. Is this method training-free?", qa_pack)
        self.assertIn("Question seven. What does the cost table measure?", qa_pack)
        self.assertIn("General response one. Different setting or condition.", qa_pack)
        self.assertIn("General response two. Question outside the tested evidence.", qa_pack)
        self.assertIn("Useful phrase. Please repeat the question.", qa_pack)


if __name__ == "__main__":
    unittest.main()
