#!/usr/bin/env python3
"""Fake Codex process for controller failure-preservation tests."""

import json
import sys
from pathlib import Path


if "--version" in sys.argv:
    print("codex-cli 0.test")
    raise SystemExit(0)

repository = Path(sys.argv[sys.argv.index("-C") + 1])
last_message = Path(sys.argv[sys.argv.index("-o") + 1])
(repository / "checkbook.py").write_text(
    "class CheckbookError(Exception):\n    pass\n\nclass Checkbook:\n    pass\n"
)
last_message.write_text("incomplete\n")
print(json.dumps({"type": "thread.started", "thread_id": "fake"}))
print(
    json.dumps(
        {
            "type": "item.completed",
            "item": {"type": "command_execution"},
        }
    )
)
print(
    json.dumps(
        {
            "type": "turn.completed",
            "usage": {
                "input_tokens": 10,
                "cached_input_tokens": 2,
                "output_tokens": 3,
                "reasoning_output_tokens": 1,
            },
        }
    )
)
