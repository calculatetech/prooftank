"""Self-test the hidden suite with known reference and broken fixtures."""

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).parent
SPEC = importlib.util.spec_from_file_location("hidden_suite", ROOT / "run_suite.py")
SUITE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SUITE)


class HiddenSuiteSelfTest(unittest.TestCase):
    def test_reference_passes_every_scenario(self):
        result = SUITE.run(ROOT / "fixtures/reference/checkbook.py")
        self.assertTrue(result["successful"])
        self.assertEqual(15, result["passed"])
        self.assertEqual(0, result["failed"])

    def test_incomplete_fixture_fails(self):
        result = SUITE.run(ROOT / "fixtures/broken/checkbook.py")
        self.assertFalse(result["successful"])
        self.assertLess(result["passed"], 15)
        self.assertGreater(result["failed"], 0)


if __name__ == "__main__":
    unittest.main()
