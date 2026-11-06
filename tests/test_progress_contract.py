import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProgressContractTest(unittest.TestCase):
    def test_pel100_ids_and_legacy_sessions_are_accepted(self):
        schema=json.loads((ROOT/'progress/progress.schema.json').read_text())
        weekly=json.loads((ROOT/'progress/weekly-summary.schema.json').read_text())
        lesson_pattern=schema['properties']['lesson']['properties']['lesson_id']['pattern']
        session_pattern=schema['properties']['session_id']['pattern']
        weekly_pattern=weekly['properties']['session_ids']['items']['pattern']
        for lesson in ['D01','B01']+[f'pel100-origin-{n:03d}' for n in range(1,101)]:
            self.assertRegex(lesson,lesson_pattern)
            session=f'2026-11-06-{lesson}-1900'
            self.assertRegex(session,session_pattern)
            self.assertRegex(session,weekly_pattern)
        for bad in ['pel100-origin-000','pel100-origin-101','pel100-origin-1','../D01']:
            self.assertIsNone(re.fullmatch(lesson_pattern,bad))

    def test_session_schema_tracks_evidence_and_materials(self):
        schema = json.loads((ROOT / "progress/progress.schema.json").read_text())
        required = set(schema["required"])

        self.assertEqual(schema["properties"]["schema_version"]["const"], "2.0")
        self.assertTrue(
            {
                "session_id",
                "recorded_at",
                "lesson",
                "materials",
                "practice_events",
                "issues",
                "chunk_progress",
                "next_plan",
            }.issubset(required)
        )

    def test_example_contains_traceable_session_evidence(self):
        example = json.loads(
            (ROOT / "progress/examples/2026-09-10-D01.example.json").read_text()
        )

        self.assertEqual(example["schema_version"], "2.0")
        self.assertEqual(example["session_id"], "2026-09-10-D01-2030")
        self.assertGreaterEqual(len(example["materials"]), 1)
        self.assertGreaterEqual(len(example["practice_events"]), 1)
        self.assertGreaterEqual(len(example["issues"]), 1)

    def test_weekly_summary_contract_exists(self):
        schema = json.loads(
            (ROOT / "progress/weekly-summary.schema.json").read_text()
        )
        required = set(schema["required"])

        self.assertTrue(
            {
                "week_id",
                "session_ids",
                "coverage",
                "recurring_issues",
                "chunk_changes",
                "proposed_adjustments",
                "discussion_questions",
            }.issubset(required)
        )

    def test_coach_index_uses_weekly_sb_notes(self):
        index = json.loads((ROOT / "coach/coach-index.json").read_text())
        storage = index["progress_storage"]

        self.assertEqual(storage["weekly_note_title"], "PEL 進度 YYYY-Www")
        self.assertNotIn("monthly_note_title", storage)
        self.assertIn("weekly_summary_schema", index)


if __name__ == "__main__":
    unittest.main()
