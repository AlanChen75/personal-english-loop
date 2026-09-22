import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/generate_library_audio.py"


def load_module():
    spec = importlib.util.spec_from_file_location("library_audio", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LibraryAudioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pipeline = load_module()

    def test_builds_grouped_xvector_plan_from_local_scripts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "lesson.txt").write_text(
                "Hello.\n\nYour turn.\n\nThis is my work.", encoding="utf-8"
            )
            catalog_path = root / "catalog.json"
            catalog_path.write_text(
                json.dumps(
                    {
                        "collections": [
                            {
                                "id": "about-me",
                                "title": "自我介紹",
                                "items": [
                                    {
                                        "number": 1,
                                        "title": "Short intro",
                                        "source": "lesson.txt",
                                        "stem": "about-me-short",
                                    }
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            catalog = self.pipeline.load_catalog(catalog_path, root=root)
            plan = self.pipeline.build_xvector_plan(catalog, max_chars=18)

        self.assertEqual(plan["generation_mode"], "x-vector-only")
        self.assertEqual(plan["collections"][0]["id"], "about-me")
        self.assertEqual(plan["tracks"][0]["stem"], "about-me-short")
        self.assertIn("This is my work.", plan["tracks"][0]["spoken_text"])
        self.assertEqual(
            [part["pause_after_ms"] for part in plan["tracks"][0]["parts"]],
            [4500, 0],
        )
        self.assertTrue(all(job["text"].endswith((".", "!", "?")) for job in plan["jobs"]))

    def test_rejects_source_outside_repository_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog_path = root / "catalog.json"
            catalog_path.write_text(
                json.dumps(
                    {
                        "collections": [
                            {
                                "id": "bad",
                                "title": "Bad",
                                "items": [
                                    {
                                        "number": 1,
                                        "title": "Bad",
                                        "source": "../outside.txt",
                                        "stem": "bad-item",
                                    }
                                ],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "source"):
                self.pipeline.load_catalog(catalog_path, root=root)


if __name__ == "__main__":
    unittest.main()
