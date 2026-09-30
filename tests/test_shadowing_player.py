import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/build_shadowing_player.py"


def load_module():
    spec = importlib.util.spec_from_file_location("shadowing_player", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ShadowingPlayerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.builder = load_module()

    def test_builds_one_visible_audio_and_transcript_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "slide-01.txt").write_text("Hello & welcome.\n", encoding="utf-8")
            (root / "slide-01-display.txt").write_text(
                "IMDELD uses TECA for industrial Pseudo-NILM.\n",
                encoding="utf-8",
            )
            (root / "slide-01.mp3").write_bytes(b"ID3")
            (root / "slide-01.png").write_bytes(b"PNG")
            manifest = {
                "collections": [
                    {
                        "id": "conference",
                        "title": "研討會講稿",
                        "items": [
                            {
                                "number": 1,
                                "title": "Opening <Question>",
                                "audio": "slide-01.mp3",
                                "spoken_transcript": "slide-01.txt",
                                "display_transcript": "slide-01-display.txt",
                                "slide_image": "slide-01.png",
                            }
                        ],
                    },
                    {
                        "id": "about-me",
                        "title": "自我介紹",
                        "items": [
                            {
                                "number": 1,
                                "title": "Short intro",
                                "audio": "slide-01.mp3",
                                "spoken_transcript": "slide-01.txt",
                            }
                        ],
                    },
                ]
            }
            manifest_path = root / "generation-manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            output = root / "shadowing-player.html"
            self.builder.build_player(manifest_path, output)
            loaded_collections = self.builder.load_collections(manifest_path)
            html = output.read_text(encoding="utf-8")
            web_manifest = json.loads((root / "manifest.webmanifest").read_text(encoding="utf-8"))
            service_worker = (root / "service-worker.js").read_text(encoding="utf-8")
            generated_assets = {
                name: (root / name).is_file()
                for name in (
                    "service-worker.js",
                    "icon-180.png",
                    "icon-192.png",
                    "icon-512.png",
                )
            }

        self.assertIn("slide-01.mp3", html)
        self.assertIn("IMDELD uses TECA for industrial Pseudo-NILM.", html)
        self.assertEqual(
            loaded_collections[0]["items"][0]["transcript"],
            "IMDELD uses TECA for industrial Pseudo-NILM.",
        )
        self.assertEqual(loaded_collections[0]["items"][0]["slide_image"], "slide-01.png")
        self.assertEqual(loaded_collections[1]["items"][0]["transcript"], "Hello & welcome.")
        self.assertIn("Opening <Question>", html)
        self.assertIn('id="practice-audio"', html)
        self.assertIn('id="slide-visual"', html)
        self.assertIn('id="slide-image"', html)
        self.assertIn('item.slide_image', html)
        self.assertIn('slide-01.png', html)
        self.assertIn('id="collection-select"', html)
        self.assertIn('研討會講稿', html)
        self.assertIn('自我介紹', html)
        self.assertIn('data-speed="0.8"', html)
        self.assertIn('data-speed="0.9"', html)
        self.assertIn('data-speed="1"', html)
        self.assertNotIn('data-speed="0.75"', html)
        self.assertIn('id="repeat-all"', html)
        self.assertIn("audio.addEventListener('ended'", html)
        self.assertIn('<link rel="manifest" href="manifest.webmanifest?v=4">', html)
        self.assertIn('<meta name="apple-mobile-web-app-title" content="Shadow">', html)
        self.assertIn('id="install-app"', html)
        self.assertIn("navigator.serviceWorker.register", html)
        self.assertEqual(web_manifest["display"], "standalone")
        self.assertEqual(web_manifest["name"], "Personal English Loop")
        self.assertEqual(web_manifest["short_name"], "Shadow")
        self.assertLessEqual(len(web_manifest["short_name"]), 7)
        self.assertEqual({icon["sizes"] for icon in web_manifest["icons"]}, {"192x192", "512x512"})
        self.assertTrue(all(generated_assets.values()), generated_assets)
        self.assertIn("personal-english-loop-v4", service_worker)
        self.assertNotIn("fetch(", html)


if __name__ == "__main__":
    unittest.main()
