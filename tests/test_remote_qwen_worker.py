import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/remote_qwen_clone_worker.py"


def load_module():
    spec = importlib.util.spec_from_file_location("remote_qwen_worker", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RemoteQwenWorkerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.worker = load_module()

    def test_validates_safe_unique_job_outputs(self):
        jobs = [
            {"id": "one", "text": "Hello.", "output": "a" * 64 + ".wav"},
            {"id": "two", "text": "World.", "output": "b" * 64 + ".wav"},
        ]

        self.assertEqual(self.worker.validate_jobs(jobs), jobs)

    def test_rejects_path_traversal_output(self):
        with self.assertRaisesRegex(ValueError, "output"):
            self.worker.validate_jobs(
                [{"id": "bad", "text": "Hello.", "output": "../bad.wav"}]
            )


if __name__ == "__main__":
    unittest.main()
