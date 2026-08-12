"""Focused checks for benchmark metrics and batch auditing."""

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parent
SPEC = importlib.util.spec_from_file_location("controller", ROOT / "controller.py")
CONTROLLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTROLLER)


class ControllerTest(unittest.TestCase):
    def test_parse_events_preserves_unavailable_usage(self):
        with tempfile.TemporaryDirectory() as directory:
            events = Path(directory) / "events.jsonl"
            events.write_text(
                '{"type":"item.completed","item":{"type":"command_execution"}}\n'
            )
            usage, tools = CONTROLLER.parse_events(events)
        self.assertEqual(1, tools)
        self.assertTrue(all(value is None for value in usage.values()))

    def test_changed_metrics_counts_source_and_tests(self):
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            initial = {"files": {}}
            (repository / "INPUT-MANIFEST.json").write_text(json.dumps(initial))
            (repository / "checkbook.py").write_text("x = 1\n")
            (repository / "test_checkbook.py").write_text("def test_x():\n    pass\n")
            metrics = CONTROLLER.changed_metrics(repository)
        self.assertEqual(1, metrics["source_lines"])
        self.assertEqual(2, metrics["test_lines"])
        self.assertIsNone(metrics["unrequested_source_lines"])

    def test_audit_requires_every_arm_and_identical_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            manifests = {}
            for arm in CONTROLLER.ARMS:
                path = batch / "repositories" / arm / "INPUT-MANIFEST.json"
                CONTROLLER.write_json(path, {"arm": arm})
                manifests[arm] = CONTROLLER.sha256(path)
            CONTROLLER.write_json(
                batch / "input-audit.json",
                {"valid": True, "manifest_sha256": manifests},
            )
            CONTROLLER.write_json(
                batch / "batch.json",
                {
                    "specify": {"commit": CONTROLLER.SPEC_KIT_COMMIT},
                    "hidden_suite_sha256": CONTROLLER.HIDDEN_SUITE_SHA256,
                },
            )
            for arm in CONTROLLER.ARMS:
                result = {
                    "schema_version": "2.0",
                    "arm": arm,
                    "brief_sha256": CONTROLLER.BRIEF_SHA256,
                    "prompt_sha256": CONTROLLER.PROMPT_SHA256,
                    "hidden_suite_sha256": CONTROLLER.HIDDEN_SUITE_SHA256,
                    "codex_version": "codex-cli 0.147.0",
                    "model": CONTROLLER.MODEL,
                    "reasoning_effort": CONTROLLER.EFFORT,
                    "sandbox": "workspace-write",
                    "timeout_seconds": 1800,
                    "python_version": "3.14.4",
                    "platform": "test-platform",
                    "metrics": {"source_lines": 1},
                    "terminal_state": "completed",
                    "codex_returncode": 0,
                    "hidden_returncode": 0,
                    "hidden": {"successful": True, "passed": 15, "failed": 0},
                    "scenario_outcomes": {
                        "passed": [f"test-{index}" for index in range(15)],
                        "failures": [],
                    },
                    "generated_files_sha256": {"checkbook.py": "hash"},
                }
                CONTROLLER.write_json(batch / "results" / f"{arm}.json", result)
            self.assertTrue(CONTROLLER.audit_batch(batch)["comparable"])
            changed = json.loads((batch / "results/bare.json").read_text())
            changed["timeout_seconds"] = 60
            CONTROLLER.write_json(batch / "results/bare.json", changed)
            self.assertFalse(CONTROLLER.audit_batch(batch)["comparable"])
            changed["timeout_seconds"] = 1800
            changed["arm"] = "ponytail"
            CONTROLLER.write_json(batch / "results/bare.json", changed)
            self.assertFalse(CONTROLLER.audit_batch(batch)["comparable"])

            changed = json.loads((batch / "results/bare.json").read_text())
            changed["arm"] = "bare"
            changed.pop("terminal_state")
            CONTROLLER.write_json(batch / "results/bare.json", changed)
            self.assertFalse(CONTROLLER.audit_batch(batch)["comparable"])
            changed["terminal_state"] = "completed"
            CONTROLLER.write_json(batch / "results/bare.json", changed)

            changed["arm"] = "bare"
            CONTROLLER.write_json(batch / "results/bare.json", changed)
            CONTROLLER.write_json(
                batch / "repositories/bare/INPUT-MANIFEST.json", {"arm": "changed"}
            )
            self.assertFalse(CONTROLLER.audit_batch(batch)["comparable"])
            (batch / "results/bare.json").unlink()
            self.assertFalse(CONTROLLER.audit_batch(batch)["comparable"])

    def test_run_arm_preserves_failed_hidden_result(self):
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            repository = batch / "repositories/bare"
            repository.mkdir(parents=True)
            shutil.copy2(ROOT / "PRODUCT-BRIEF.md", repository)
            shutil.copy2(ROOT / "PROMPT.txt", repository)
            initial = {
                "files": {
                    "PRODUCT-BRIEF.md": CONTROLLER.sha256(
                        repository / "PRODUCT-BRIEF.md"
                    ),
                    "PROMPT.txt": CONTROLLER.sha256(repository / "PROMPT.txt"),
                }
            }
            CONTROLLER.write_json(repository / "INPUT-MANIFEST.json", initial)
            fake = ROOT / "hidden/fixtures/fake_codex.py"
            result = CONTROLLER.run_arm(batch, "bare", fake, 30)
        self.assertEqual("completed", result["terminal_state"])
        self.assertFalse(result["hidden"]["successful"])
        self.assertEqual(1, result["tool_calls"])
        self.assertEqual(10, result["usage"]["input_tokens"])
        self.assertIn("checkbook.py", result["metrics"]["changed_files"])


if __name__ == "__main__":
    unittest.main()
