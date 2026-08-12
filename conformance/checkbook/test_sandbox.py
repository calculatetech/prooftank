"""Security checks for generated-code isolation."""

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).parent
SPEC = importlib.util.spec_from_file_location("benchmark_sandbox", ROOT / "sandbox.py")
SANDBOX = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SANDBOX)


class SandboxTest(unittest.TestCase):
    def test_sandbox_runs_positive_control(self):
        with tempfile.TemporaryDirectory() as directory:
            completed = SANDBOX.run(Path(directory), ["/bin/true"])
            self.assertEqual(0, completed.returncode, completed.stderr)

    def test_command_applies_resource_limits(self):
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.object(SANDBOX, "uid_thread_count", return_value=100):
                command = SANDBOX.command_for(Path(directory), ["/bin/true"])
            self.assertEqual("prlimit", Path(command[0]).name)
            self.assertTrue(set(SANDBOX.RESOURCE_LIMITS) <= set(command))
            self.assertIn("--nproc=164", command)

    def test_candidate_cannot_write_outside_sandbox(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = root / "candidate"
            candidate.mkdir()
            sentinel = root / "escape"
            (candidate / "attempt.py").write_text(
                "from pathlib import Path\n"
                f"Path({str(sentinel)!r}).write_text('escaped')\n"
            )
            completed = SANDBOX.run(
                candidate, ["/usr/bin/python3", "/candidate/attempt.py"]
            )
            self.assertNotEqual(0, completed.returncode)
            self.assertFalse(sentinel.exists())

    def test_candidate_has_no_network_namespace(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory)
            (candidate / "network.py").write_text(
                "import socket\nsocket.create_connection(('1.1.1.1', 53), timeout=1)\n"
            )
            completed = SANDBOX.run(
                candidate, ["/usr/bin/python3", "/candidate/network.py"]
            )
            self.assertNotEqual(0, completed.returncode)

    def test_candidate_output_is_bounded(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory)
            (candidate / "flood.py").write_text(
                "import sys\nsys.stdout.write('x' * 2_000_000)\n"
            )
            completed = SANDBOX.run(
                candidate, ["/usr/bin/python3", "/candidate/flood.py"]
            )
            self.assertNotEqual(0, completed.returncode)
            self.assertLessEqual(len(completed.stdout), SANDBOX.MAX_OUTPUT_BYTES)


if __name__ == "__main__":
    unittest.main()
