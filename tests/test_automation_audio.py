import importlib.util
import json
import tempfile
import unittest
import wave
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/generate_automation_audio.py"


def load_module():
    spec = importlib.util.spec_from_file_location("automation_audio", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AutomationAudioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = load_module()

    def test_applies_overrides_adds_closing_then_appendix_and_qa(self):
        payload = {
            "segments": [
                {
                    "slide": number,
                    "title": f"Slide {number}",
                    "spoken_transcript": f"Slide {number} script.",
                    "display_transcript": f"Slide {number} script.",
                }
                for number in range(1, 13)
            ],
            "qa_answers": [
                {
                    "id": "q1",
                    "question": "Q1 — What is MCC?",
                    "spoken_transcript": "It is a device metric.",
                },
                {
                    "id": "general",
                    "question": "General response",
                    "spoken_transcript": "This study does not test that case.",
                },
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "spoken_segments.json"
            source.write_text(json.dumps(payload), encoding="utf-8")
            extension = Path(directory) / "extension.json"
            extension.write_text(
                json.dumps(
                    {
                        "overrides": [
                            {
                                "slide": 1,
                                "spoken_transcript": "Opening with affiliation.",
                                "display_transcript": "Opening with affiliation.",
                            }
                        ],
                        "additional_slides": [
                            {
                                "slide": 13,
                                "title": "Thank you and Q&A",
                                "spoken_transcript": "Thank you. Email d11351004@mail.ntust.edu.tw.",
                                "display_transcript": "Thank you. Email d11351004@mail.ntust.edu.tw.",
                            }
                        ],
                        "appendices": [
                            {
                                "slide": 14,
                                "title": "How were the numbers calculated?",
                                "spoken_transcript": "We calculate an MCC for each device.",
                                "display_transcript": "We calculate an MCC for each device.",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            tracks = self.pipeline.load_automation_tracks(source, extension)

        self.assertEqual(len(tracks), 15)
        self.assertEqual([item["number"] for item in tracks[:12]], list(range(1, 13)))
        self.assertEqual(tracks[0]["script"], "Opening with affiliation.")
        self.assertEqual(tracks[12]["number"], 13)
        self.assertEqual(tracks[12]["kind"], "slide")
        self.assertEqual(tracks[12]["title"], "Thank you and Q&A")
        self.assertEqual(
            tracks[12]["slide_image"], "automation2026/slides/slide-13.png"
        )
        self.assertEqual(tracks[13]["number"], 14)
        self.assertEqual(tracks[13]["kind"], "appendix")
        self.assertEqual(tracks[-1]["number"], 15)
        self.assertEqual(tracks[-1]["title"], "Q&A response pack")
        self.assertEqual(
            tracks[-1]["slide_image"], "automation2026/slides/slide-14.png"
        )
        self.assertIn("Question one. What is MCC?", tracks[-1]["script"])
        self.assertIn("General response.", tracks[-1]["script"])

    def test_uses_tts_pronunciations_without_changing_display_terms(self):
        source = (
            "NILM compares LLM and LHS by MCC and five MCCs on IMDELD, Case 1, "
            "and WELTRON in seed-one-oh-one. TP, TN, FP, and FN are counted."
        )

        spoken = self.pipeline.prepare_spoken_text(source)

        self.assertIn("nil-em", spoken)
        self.assertIn("ell ell em", spoken)
        self.assertIn("ell aitch ess", spoken)
        self.assertIn("em see see", spoken)
        self.assertIn("five em see see values", spoken)
        self.assertIn("tee pee, tee en, eff pee, and eff en", spoken)
        self.assertIn("eye em dee ee el dee", spoken)
        self.assertIn("Case one", spoken)
        self.assertIn("well-tron", spoken)
        self.assertIn("seed one oh one", spoken)
        self.assertEqual(
            self.pipeline.prepare_display_text(source),
            "NILM compares LLM and LHS by MCC and five MCCs on IMDELD, Case 1, and "
            "WELTRON in seed 101. TP, TN, FP, and FN are counted.",
        )

    def test_speaks_email_address_but_keeps_visible_address(self):
        source = "Please email me at d11351004@mail.ntust.edu.tw."

        self.assertEqual(
            self.pipeline.prepare_spoken_text(source),
            "Please email me at d one one three five one zero zero four at mail dot "
            "N T U S T dot E D U dot T W.",
        )
        self.assertEqual(self.pipeline.prepare_display_text(source), source)

    def test_display_text_uses_digits_for_reported_results(self):
        source = (
            "The weights are point three five, point three zero, point two zero, "
            "and point one five. LHS rose from zero point zero nine nine one to "
            "zero point six two four four. Only five out of two hundred twenty-five "
            "configurations did so: two point two two percent. For LHS, it was "
            "six percent. The question cites 2.22 percent."
        )

        display = self.pipeline.prepare_display_text(source)

        self.assertEqual(
            display,
            "The weights are 0.35, 0.30, 0.20, and 0.15. LHS rose from 0.0991 "
            "to 0.6244. Only 5 out of 225 configurations did so: 2.22%. For LHS, "
            "it was 6%. The question cites 2.22%.",
        )

    def test_plan_keeps_display_and_spoken_transcripts_separate(self):
        tracks = [
            {
                "number": 1,
                "title": "Result",
                "script": "LLM reaches zero point five five seven seven MCC.",
                "display_text": "LLM reaches 0.5577 MCC.",
                "slide_image": "automation2026/slides/slide-1.png",
            }
        ]

        plan = self.pipeline.build_xvector_plan(tracks, max_chars=140)

        item = plan["tracks"][0]
        self.assertEqual(item["display_text"], "LLM reaches 0.5577 MCC.")
        self.assertIn("ell ell em", item["spoken_text"])
        self.assertEqual(item["slide_image"], "automation2026/slides/slide-1.png")
        self.assertTrue(plan["jobs"])

    def test_assembles_tracks_full_talk_and_generation_manifest(self):
        tracks = [
            {
                "number": 1,
                "title": "Opening",
                "script": "NILM opening.",
                "display_text": "NILM opening.",
                "slide_image": "automation2026/slides/slide-1.png",
                "kind": "slide",
            },
            {
                "number": 13,
                "title": "Calculation Q&A appendix",
                "script": "MCC appendix answer.",
                "display_text": "MCC appendix answer.",
                "slide_image": "automation2026/slides/slide-13.png",
                "kind": "appendix",
            },
            {
                "number": 14,
                "title": "Q&A response pack",
                "script": "LLM answer.",
                "display_text": "LLM answer.",
                "slide_image": "automation2026/slides/slide-13.png",
                "kind": "qa",
            },
        ]
        plan = self.pipeline.build_xvector_plan(tracks, max_chars=140)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan_path, jobs_path = self.pipeline.write_plan(plan, root / "plan")
            self.assertTrue(plan_path.is_file())
            self.assertTrue(jobs_path.is_file())
            cache = root / "cache"
            cache.mkdir()
            for job in plan["jobs"]:
                with wave.open(str(cache / job["output"]), "wb") as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(24000)
                    wav_file.writeframes(b"\0\0" * 2400)
            source = root / "source.json"
            source.write_text("{}\n", encoding="utf-8")
            output = root / "output"

            def fake_encode(_raw, target, *, slow):
                self.assertFalse(slow)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"ID3")

            with (
                mock.patch.object(self.pipeline, "encode_mp3", side_effect=fake_encode),
                mock.patch.object(
                    self.pipeline,
                    "probe_audio",
                    return_value={"streams": [{"sample_rate": "24000", "channels": 1}]},
                ),
            ):
                manifest_path = self.pipeline.assemble_plan(
                    plan=plan,
                    cache_dir=cache,
                    work_root=root / "work",
                    output_root=output,
                    source_path=source,
                )

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["items"]), 3)
            self.assertEqual(manifest["items"][0]["number"], 1)
            self.assertEqual(manifest["items"][1]["number"], 13)
            self.assertEqual(manifest["items"][2]["number"], 14)
            self.assertTrue((output / "automation2026-full-talk.mp3").is_file())
            self.assertTrue((output / "automation2026-full-talk.txt").is_file())
            self.assertTrue((output / "automation2026-full-talk-display.txt").is_file())
            self.assertNotIn(
                "appendix answer",
                (output / "automation2026-full-talk.txt").read_text(),
            )
            self.assertNotIn("LLM answer", (output / "automation2026-full-talk.txt").read_text())

    def test_rejects_incomplete_sources_and_missing_wav_chunks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.json"
            source.write_text(json.dumps({"segments": [], "qa_answers": []}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "exactly 12 segments"):
                self.pipeline.load_automation_tracks(source)

            plan = self.pipeline.build_xvector_plan(
                [
                    {
                        "number": 1,
                        "title": "Opening",
                        "script": "Opening.",
                        "display_text": "Opening.",
                        "slide_image": "automation2026/slides/slide-1.png",
                        "kind": "slide",
                    }
                ]
            )
            with self.assertRaisesRegex(FileNotFoundError, "Missing"):
                self.pipeline.assemble_plan(
                    plan=plan,
                    cache_dir=root / "empty",
                    work_root=root / "work",
                    output_root=root / "output",
                    source_path=source,
                )


if __name__ == "__main__":
    unittest.main()
