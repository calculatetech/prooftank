"""Focused checks for blind quality-review artifacts."""

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).parent
SPEC = importlib.util.spec_from_file_location(
    "quality_review", ROOT / "quality_review.py"
)
QUALITY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(QUALITY)


class QualityReviewTest(unittest.TestCase):
    def test_hidden_suite_identity_is_exact(self):
        expected = {
            f"__main__.CheckbookScenarios.test_req_{index:02d}_{suffix}"
            for index, suffix in enumerate(
                (
                    "account_currency_and_opening_balance",
                    "integer_money_and_signs",
                    "transaction_shape_and_deterministic_order",
                    "edit_clear_and_expected_version",
                    "import_success_and_idempotent_duplicate",
                    "conflicting_duplicate_is_atomic",
                    "malformed_middle_row_and_retry",
                    "reconcile_and_mismatch_are_atomic",
                    "reconciled_history_uses_one_linked_reversal",
                    "closed_period_prevents_historical_mutation",
                    "two_connections_detect_lost_edit",
                    "every_successful_command_is_audited",
                    "state_survives_restart_after_abort",
                    "real_calendar_dates",
                    "failure_operation_ids_are_structured",
                ),
                start=1,
            )
        }
        self.assertEqual(QUALITY.hidden_scenarios(QUALITY.HIDDEN_SUITE), expected)
        self.assertEqual(
            QUALITY.sha256(QUALITY.HIDDEN_SUITE),
            "5822d5eca6049ba60856e76a32ca5b773504981629683329a89193f3b2b9f354",
        )

    def test_report_requires_all_quality_dimensions(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "candidate-1"
            candidate.mkdir()
            for name in ("PRODUCT-BRIEF.md", "checkbook.py", "test_checkbook.py"):
                (candidate / name).write_text("line\n")
            files = {
                name: QUALITY.sha256(candidate / name)
                for name in ("PRODUCT-BRIEF.md", "checkbook.py", "test_checkbook.py")
            }
            manifest = {"candidates": {"candidate-1": {"files": files}}}
            report = {
                "schema_version": "1.0",
                "candidate_id": "candidate-1",
                "findings": [],
                "production_blockers": [],
                "dimensions": {},
            }
            with self.assertRaisesRegex(ValueError, "ten dimensions"):
                QUALITY.validate_report(candidate, manifest, report)

    def test_report_rejects_boolean_scores_and_missing_rationale(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "candidate-1"
            candidate.mkdir()
            names = ("PRODUCT-BRIEF.md", "checkbook.py", "test_checkbook.py")
            for name in names:
                (candidate / name).write_text("line\n")
            files = {name: QUALITY.sha256(candidate / name) for name in names}
            evidence = [{"path": "checkbook.py", "line": 1, "detail": "line"}]
            report = {
                "schema_version": "1.0",
                "candidate_id": "candidate-1",
                "findings": [],
                "production_blockers": [],
                "security_posture": "bounded",
                "strongest_quality": "clear",
                "weakest_quality": "operations",
                "dimensions": {
                    name: {"score": True, "evidence": evidence}
                    for name in QUALITY.DIMENSIONS
                },
                "overall_readiness": {"score": True},
                "take_production_ownership": {"answer": "no", "conditions": []},
                "test_confidence": {"gaps": []},
            }
            manifest = {"candidates": {"candidate-1": {"files": files}}}
            with self.assertRaisesRegex(ValueError, "dimension score"):
                QUALITY.validate_report(candidate, manifest, report)

    def test_report_requires_every_audit_surface(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "candidate-1"
            candidate.mkdir()
            names = ("PRODUCT-BRIEF.md", "checkbook.py", "test_checkbook.py")
            for name in names:
                (candidate / name).write_text("line\n")
            files = {name: QUALITY.sha256(candidate / name) for name in names}
            evidence = [{"path": "checkbook.py", "line": 1, "detail": "line"}]
            report = {
                "schema_version": "1.0",
                "candidate_id": "candidate-1",
                "findings": [],
                "production_blockers": [],
                "security_posture": "bounded",
                "strongest_quality": "clear",
                "weakest_quality": "operations",
                "dimensions": {
                    name: {"score": 3, "evidence": evidence}
                    for name in QUALITY.DIMENSIONS
                },
                "overall_readiness": {"score": 3, "rationale": "bounded"},
                "take_production_ownership": {
                    "answer": "conditional",
                    "conditions": [],
                    "rationale": "bounded",
                },
                "test_confidence": {"supplied": "one test", "gaps": []},
                "audit_surfaces": {},
                "verification": {
                    "command": "test",
                    "exit_status": 0,
                    "outcome": "passed",
                },
            }
            manifest = {"candidates": {"candidate-1": {"files": files}}}
            with self.assertRaisesRegex(ValueError, "audit surfaces"):
                QUALITY.validate_report(candidate, manifest, report)

    def test_batch_rejects_reused_reviewer(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "reports"
            candidate = root / "candidate-1"
            candidate.mkdir(parents=True)
            envelope = {
                "reviewer_id": "same-reviewer",
                "settings": {"context": "clean"},
                "report": {},
            }
            for name in ("review-1.json", "review-2.json"):
                (candidate / name).write_text(__import__("json").dumps(envelope))
            manifest = {
                "candidates": {f"candidate-{index}": {} for index in range(1, 6)}
            }
            protocol = {
                "app_reviews_per_candidate": 2,
                "reviewer_settings": {"context": "clean"},
            }
            with (
                mock.patch.object(QUALITY, "validate_report"),
                self.assertRaisesRegex(ValueError, "fresh reviewer"),
            ):
                QUALITY.validate_review_batch(root, manifest, protocol)

    def test_snapshot_rejects_nested_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidates = {}
            for index in range(1, 6):
                candidate = root / f"candidate-{index}"
                candidate.mkdir()
                files = {}
                for name in ("PRODUCT-BRIEF.md", "checkbook.py", "test_checkbook.py"):
                    path = candidate / name
                    path.write_text("line\n")
                    files[name] = QUALITY.sha256(path)
                candidates[candidate.name] = {"files": files}
            nested = root / "candidate-1/__pycache__"
            nested.mkdir()
            (nested / "leak.pyc").write_bytes(b"identity")
            with self.assertRaisesRegex(ValueError, "unexpected review directory"):
                QUALITY.validate_snapshots(root, {"candidates": candidates})


if __name__ == "__main__":
    unittest.main()
