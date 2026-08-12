#!/usr/bin/env python3
"""Prepare, run, and preserve the first checkbook comparison."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKBOOK = ROOT / "conformance/checkbook"
ARMS = (
    "bare",
    "ponytail",
    "cavekit-ponytail",
    "spec-kit-core",
    "proofmill-standard",
)
BRIEF_SHA256 = "6588b63ee0996ed3141cd41b0640f0ce6ff7ff58dec7e271d2d28c10ae4956e5"
PROMPT_SHA256 = "01cd99dcbd35a2391193fe0409929d86b65d173ecec1354074c285d29aa8875a"
SPEC_KIT_COMMIT = "bd595cf838cc200f84fee9e9327b643dfe277d2c"
MODEL = "gpt-5.4"
EFFORT = "medium"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def run_command(
    command: list[str],
    cwd: Path,
    *,
    check: bool = True,
    capture: bool = True,
    timeout: int | None = None,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=cwd,
        check=check,
        capture_output=capture,
        text=True,
        timeout=timeout,
    )


def copy_tree(source: Path, destination: Path) -> None:
    if destination.exists():
        raise FileExistsError(destination)
    shutil.copytree(source, destination)


def install_skills(repository: Path, arm: str) -> None:
    if arm not in {"ponytail", "cavekit-ponytail", "proofmill-standard"}:
        return
    skill_root = repository / ".agents/skills"
    skill_root.mkdir(parents=True, exist_ok=True)
    release_skills = ROOT / "releases/proofmill-standard/0.1.0/skills"
    if arm in {"ponytail", "cavekit-ponytail", "proofmill-standard"}:
        copy_tree(release_skills / "ponytail", skill_root / "ponytail")
    if arm == "proofmill-standard":
        copy_tree(release_skills / "simple-english", skill_root / "simple-english")
    if arm == "cavekit-ponytail":
        vendor = CHECKBOOK / "arms/cavekit-ponytail/vendor/cavekit/skills"
        for name in ("spec", "build", "check", "caveman", "backprop"):
            copy_tree(vendor / name, skill_root / name)


def install_spec_kit(repository: Path, specify: Path, proofmill: bool) -> None:
    run_command(
        [
            str(specify),
            "init",
            "--here",
            "--integration",
            "codex",
            "--force",
            "--ignore-agent-tools",
            "--script",
            "sh",
        ],
        repository,
    )
    if not proofmill:
        return
    release = ROOT / "releases/proofmill-standard/0.1.0/components"
    run_command(
        [
            str(specify),
            "preset",
            "add",
            "--dev",
            str(release / "proofmill-contract"),
            "--priority",
            "10",
        ],
        repository,
    )
    run_command(
        [
            str(specify),
            "workflow",
            "add",
            "--dev",
            str(release / "proofmill-standard-workflow"),
        ],
        repository,
    )


def file_manifest(repository: Path) -> dict[str, str]:
    manifest = {}
    for path in sorted(repository.rglob("*")):
        relative = path.relative_to(repository)
        if (
            not path.is_file()
            or ".git" in path.parts
            or "__pycache__" in path.parts
            or path.suffix == ".pyc"
            or relative.parts[:2] == (".agent", "test-results")
        ):
            continue
        manifest[str(relative)] = sha256(path)
    return manifest


def prepare_arm(batch: Path, arm: str, specify: Path) -> Path:
    repository = batch / "repositories" / arm
    if repository.exists():
        raise FileExistsError(repository)
    repository.mkdir(parents=True)
    shutil.copy2(CHECKBOOK / "PRODUCT-BRIEF.md", repository / "PRODUCT-BRIEF.md")
    shutil.copy2(CHECKBOOK / "PROMPT.txt", repository / "PROMPT.txt")
    source = CHECKBOOK / "arms" / arm
    shutil.copy2(source / "arm.json", repository / "arm.json")
    if (source / "AGENTS.md").exists():
        shutil.copy2(source / "AGENTS.md", repository / "AGENTS.md")
    run_command(["git", "init", "-q"], repository)
    run_command(["git", "config", "user.name", "Proofmill Benchmark"], repository)
    run_command(["git", "config", "user.email", "benchmark@invalid.local"], repository)
    if arm == "spec-kit-core":
        install_spec_kit(repository, specify, False)
    elif arm == "proofmill-standard":
        install_spec_kit(repository, specify, True)
    install_skills(repository, arm)
    manifest = {
        "schema_version": "1.0",
        "arm": arm,
        "brief_sha256": sha256(repository / "PRODUCT-BRIEF.md"),
        "prompt_sha256": sha256(repository / "PROMPT.txt"),
        "files": file_manifest(repository),
    }
    write_json(repository / "INPUT-MANIFEST.json", manifest)
    run_command(["git", "add", "."], repository)
    run_command(["git", "commit", "-qm", "Frozen benchmark input"], repository)
    return repository


def parse_events(path: Path) -> tuple[dict[str, int | None], int]:
    usage = {
        "input_tokens": None,
        "cached_input_tokens": None,
        "output_tokens": None,
        "reasoning_output_tokens": None,
    }
    tool_calls = 0
    if not path.exists():
        return usage, tool_calls
    for line in path.read_text(errors="replace").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "turn.completed" and isinstance(
            event.get("usage"), dict
        ):
            for key in usage:
                value = event["usage"].get(key)
                usage[key] = value if isinstance(value, int) else None
        if event.get("type") == "item.completed":
            item_type = event.get("item", {}).get("type")
            if item_type not in {None, "agent_message", "reasoning"}:
                tool_calls += 1
    return usage, tool_calls


def changed_metrics(repository: Path) -> dict:
    initial = json.loads((repository / "INPUT-MANIFEST.json").read_text())["files"]
    current = file_manifest(repository)
    current.pop("INPUT-MANIFEST.json", None)
    changed = sorted(
        path for path, digest in current.items() if initial.get(path) != digest
    )
    deleted = sorted(path for path in initial if path not in current)
    counts = {"source_lines": 0, "test_lines": 0, "specification_lines": 0}
    text_lines = 0
    for relative in changed:
        path = repository / relative
        try:
            lines = len(path.read_text().splitlines())
        except UnicodeDecodeError:
            continue
        text_lines += lines
        name = path.name.lower()
        if path.suffix == ".py" and (name.startswith("test_") or "test" in path.parts):
            counts["test_lines"] += lines
        elif path.suffix == ".py":
            counts["source_lines"] += lines
        if (
            relative == "SPEC.md"
            or relative.startswith("specs/")
            or relative.startswith("docs/checkbook/")
        ):
            counts["specification_lines"] += lines
    dependency_files = [
        path
        for path in changed
        if Path(path).name
        in {
            "requirements.txt",
            "pyproject.toml",
            "Pipfile",
            "poetry.lock",
            "package.json",
        }
    ]
    scope_files = [
        path
        for path in changed
        if Path(path).name
        in {
            "Dockerfile",
            "docker-compose.yml",
            "compose.yml",
            "package.json",
            "requirements.txt",
        }
    ]
    return {
        **counts,
        "generated_text_lines": text_lines,
        "changed_files": changed,
        "changed_file_count": len(changed),
        "deleted_files": deleted,
        "declared_dependency_files": dependency_files,
        "scope_addition_files": scope_files,
        "one_implementation_abstractions": None,
        "unrequested_source_lines": None,
    }


def run_hidden_suite(repository: Path, output: Path) -> tuple[int, dict]:
    completed = run_command(
        [
            sys.executable,
            str(CHECKBOOK / "hidden/run_suite.py"),
            str(repository / "checkbook.py"),
            "--output",
            str(output),
        ],
        ROOT,
        check=False,
    )
    return completed.returncode, json.loads(output.read_text())


def run_arm(
    batch: Path,
    arm: str,
    codex: Path,
    timeout: int,
) -> dict:
    repository = batch / "repositories" / arm
    raw = batch / "raw" / arm
    raw.mkdir(parents=True, exist_ok=True)
    events = raw / "codex.jsonl"
    last_message = raw / "last-message.txt"
    prompt = (repository / "PROMPT.txt").read_text()
    command = [
        str(codex),
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--skip-git-repo-check",
        "-s",
        "workspace-write",
        "-m",
        MODEL,
        "-c",
        f'model_reasoning_effort="{EFFORT}"',
        "--json",
        "-C",
        str(repository),
        "-o",
        str(last_message),
        prompt,
    ]
    started = time.monotonic()
    terminal = "completed"
    returncode = None
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["NO_COLOR"] = "1"
    with events.open("w") as stream:
        try:
            completed = subprocess.run(
                command,
                cwd=repository,
                stdout=stream,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=timeout,
                env=environment,
            )
            returncode = completed.returncode
            if returncode != 0:
                terminal = "failed"
        except subprocess.TimeoutExpired:
            terminal = "timeout"
    elapsed = round(time.monotonic() - started, 3)
    hidden_output = raw / "hidden-result.json"
    hidden_returncode, hidden = run_hidden_suite(repository, hidden_output)
    hidden["implementation"] = "checkbook.py"
    usage, tool_calls = parse_events(events)
    metrics = changed_metrics(repository)
    result = {
        "schema_version": "1.0",
        "arm": arm,
        "terminal_state": terminal,
        "codex_returncode": returncode,
        "hidden_returncode": hidden_returncode,
        "brief_sha256": sha256(repository / "PRODUCT-BRIEF.md"),
        "prompt_sha256": sha256(repository / "PROMPT.txt"),
        "codex_version": run_command([str(codex), "--version"], ROOT).stdout.strip(),
        "model": MODEL,
        "reasoning_effort": EFFORT,
        "sandbox": "workspace-write",
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "wall_seconds": elapsed,
        "tool_calls": tool_calls,
        "usage": usage,
        "hidden": hidden,
        "accepted_capabilities": hidden["passed"],
        "hidden_scenarios_passed": hidden["passed"],
        "severe_defects": hidden["failed"],
        "human_minutes": 0,
        "repair_cycles": 0,
        "cost_usd": None,
        "diagnosis_seconds": None,
        "metrics": metrics,
    }
    write_json(batch / "results" / f"{arm}.json", result)
    return result


def audit_batch(batch: Path) -> dict:
    results = []
    for arm in ARMS:
        path = batch / "results" / f"{arm}.json"
        if path.exists():
            results.append(json.loads(path.read_text()))
    brief_hashes = sorted({item["brief_sha256"] for item in results})
    prompt_hashes = sorted({item["prompt_sha256"] for item in results})
    settings = sorted(
        {
            (item["codex_version"], item["model"], item["reasoning_effort"])
            for item in results
        }
    )
    comparable = (
        len(results) == len(ARMS)
        and brief_hashes == [BRIEF_SHA256]
        and prompt_hashes == [PROMPT_SHA256]
        and len(settings) == 1
    )
    audit = {
        "schema_version": "1.0",
        "comparable": comparable,
        "arms_expected": list(ARMS),
        "arms_present": [item["arm"] for item in results],
        "brief_sha256_values": brief_hashes,
        "prompt_sha256_values": prompt_hashes,
        "runner_settings": [list(item) for item in settings],
    }
    write_json(batch / "results/audit.json", audit)
    return audit


def audit_inputs(batch: Path) -> dict:
    manifests = {
        arm: json.loads(
            (batch / "repositories" / arm / "INPUT-MANIFEST.json").read_text()
        )
        for arm in ARMS
    }
    files = {arm: value["files"] for arm, value in manifests.items()}
    checks = {
        "all_arms_present": set(manifests) == set(ARMS),
        "brief_identical": all(
            value["brief_sha256"] == BRIEF_SHA256 for value in manifests.values()
        ),
        "prompt_identical": all(
            value["prompt_sha256"] == PROMPT_SHA256 for value in manifests.values()
        ),
        "no_hidden_files": all(
            not any("hidden" in Path(path).parts for path in value)
            for value in files.values()
        ),
        "bare_has_no_treatment": set(files["bare"])
        == {"PRODUCT-BRIEF.md", "PROMPT.txt", "arm.json"},
        "ponytail_has_only_named_skill": set(files["ponytail"])
        == {
            ".agents/skills/ponytail/SKILL.md",
            "AGENTS.md",
            "PRODUCT-BRIEF.md",
            "PROMPT.txt",
            "arm.json",
        },
        "cavekit_has_only_named_skills": set(files["cavekit-ponytail"])
        == {
            ".agents/skills/backprop/SKILL.md",
            ".agents/skills/build/SKILL.md",
            ".agents/skills/caveman/SKILL.md",
            ".agents/skills/check/SKILL.md",
            ".agents/skills/ponytail/SKILL.md",
            ".agents/skills/spec/SKILL.md",
            "AGENTS.md",
            "PRODUCT-BRIEF.md",
            "PROMPT.txt",
            "arm.json",
        },
        "spec_kit_has_no_proofmill_providers": not any(
            name in files["spec-kit-core"]
            for name in (
                ".agents/skills/ponytail/SKILL.md",
                ".agents/skills/simple-english/SKILL.md",
            )
        ),
        "proofmill_has_required_providers": all(
            name in files["proofmill-standard"]
            for name in (
                ".agents/skills/ponytail/SKILL.md",
                ".agents/skills/simple-english/SKILL.md",
                ".specify/presets/proofmill-contract/preset.yml",
                ".specify/workflows/proofmill-standard/workflow.yml",
            )
        ),
    }
    shared_core = [
        path
        for path in files["spec-kit-core"]
        if path.startswith(".agents/skills/speckit-")
        or path.startswith(".specify/scripts/")
        or path.startswith(".specify/templates/")
    ]
    checks["spec_kit_core_bytes_identical"] = all(
        files["proofmill-standard"].get(path) == files["spec-kit-core"][path]
        for path in shared_core
    )
    audit = {
        "schema_version": "1.0",
        "valid": all(checks.values()),
        "checks": checks,
        "manifest_sha256": {
            arm: sha256(batch / "repositories" / arm / "INPUT-MANIFEST.json")
            for arm in ARMS
        },
    }
    write_json(batch / "input-audit.json", audit)
    return audit


def prepare_batch(batch: Path, specify: Path) -> list[str]:
    if batch.exists():
        raise FileExistsError(batch)
    batch.mkdir(parents=True)
    if sha256(CHECKBOOK / "PRODUCT-BRIEF.md") != BRIEF_SHA256:
        raise ValueError("frozen brief hash changed")
    if sha256(CHECKBOOK / "PROMPT.txt") != PROMPT_SHA256:
        raise ValueError("frozen prompt hash changed")
    order = list(ARMS)
    random.Random(batch.name).shuffle(order)
    for arm in ARMS:
        prepare_arm(batch, arm, specify)
    input_audit = audit_inputs(batch)
    if not input_audit["valid"]:
        raise ValueError("arm input parity audit failed")
    metadata = {
        "schema_version": "1.0",
        "batch_id": batch.name,
        "order": order,
        "arms": list(ARMS),
        "spec_kit_commit": SPEC_KIT_COMMIT,
    }
    write_json(batch / "batch.json", metadata)
    return order


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("batch", type=Path)
    parser.add_argument("--specify", type=Path, required=True)
    parser.add_argument("--codex", type=Path, default=Path(shutil.which("codex") or ""))
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    order = prepare_batch(args.batch.resolve(), args.specify.resolve())
    if args.prepare_only:
        print(json.dumps({"batch": str(args.batch), "order": order}, sort_keys=True))
        return 0
    for arm in order:
        result = run_arm(args.batch.resolve(), arm, args.codex.resolve(), args.timeout)
        print(json.dumps({"arm": arm, "state": result["terminal_state"]}))
    audit = audit_batch(args.batch.resolve())
    print(json.dumps(audit, sort_keys=True))
    return 0 if audit["comparable"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
