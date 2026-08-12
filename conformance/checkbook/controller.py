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
HIDDEN_SUITE_SHA256 = "5822d5eca6049ba60856e76a32ca5b773504981629683329a89193f3b2b9f354"
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


def verify_specify(specify: Path) -> dict[str, str]:
    python = specify.parent / "python"
    if not python.is_file():
        raise ValueError("specify must come from a virtual environment")
    script = (
        "import importlib.metadata,json;"
        "d=importlib.metadata.distribution('specify-cli');"
        "p=d.locate_file('specify_cli-'+d.version+'.dist-info/direct_url.json');"
        "print(json.dumps({'version':d.version,'direct_url':json.loads(p.read_text())}))"
    )
    completed = run_command([str(python), "-c", script], ROOT)
    metadata = json.loads(completed.stdout)
    commit = metadata.get("direct_url", {}).get("vcs_info", {}).get("commit_id")
    if commit != SPEC_KIT_COMMIT:
        raise ValueError(f"unexpected Spec Kit commit: {commit}")
    return {"version": metadata["version"], "commit": commit}


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


def generated_manifest(repository: Path) -> dict[str, str]:
    initial = json.loads((repository / "INPUT-MANIFEST.json").read_text())["files"]
    current = file_manifest(repository)
    current.pop("INPUT-MANIFEST.json", None)
    return {
        path: digest for path, digest in current.items() if initial.get(path) != digest
    }


def run_hidden_suite(repository: Path, output: Path) -> tuple[int, dict]:
    completed = run_command(
        [
            sys.executable,
            str(CHECKBOOK / "sandbox.py"),
            str(repository),
            "--timeout",
            "60",
            "--mount",
            f"{CHECKBOOK / 'hidden'}=/suite",
            "--",
            "/usr/bin/python3",
            "/suite/run_suite.py",
            "/candidate/checkbook.py",
        ],
        ROOT,
        check=False,
    )
    try:
        summary = json.loads(completed.stdout)
    except json.JSONDecodeError:
        summary = {
            "schema_version": "1.0",
            "implementation": "checkbook.py",
            "tests": 0,
            "passed": 0,
            "failed": 1,
            "successful": False,
            "passed_tests": [],
            "failures": [
                {"test": "sandbox_runner", "detail": completed.stderr.strip()}
            ],
        }
    write_json(output, summary)
    return completed.returncode, summary


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
        "schema_version": "2.0",
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
        "timeout_seconds": timeout,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "hidden_suite_sha256": sha256(CHECKBOOK / "hidden/run_suite.py"),
        "wall_seconds": elapsed,
        "tool_calls": tool_calls,
        "usage": usage,
        "hidden": hidden,
        "scenario_outcomes": {
            "passed": hidden["passed_tests"],
            "failures": hidden["failures"],
        },
        "human_minutes": 0,
        "repair_cycles": 0,
        "cost_usd": None,
        "diagnosis_seconds": None,
        "metrics": metrics,
        "generated_files_sha256": generated_manifest(repository),
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
            (
                item["codex_version"],
                item["model"],
                item["reasoning_effort"],
                item["sandbox"],
                item["timeout_seconds"],
                item["python_version"],
                item["platform"],
            )
            for item in results
        }
    )
    suite_hashes = sorted({item["hidden_suite_sha256"] for item in results})
    schemas = sorted({item["schema_version"] for item in results})
    metric_schemas = {tuple(sorted(item["metrics"])) for item in results}
    outcomes_valid = all(
        item.get("terminal_state") == "completed"
        and item.get("codex_returncode") == 0
        and item.get("hidden_returncode") == 0
        and isinstance(item.get("hidden"), dict)
        and item["hidden"].get("successful") is True
        and item["hidden"].get("passed") == 15
        and item["hidden"].get("failed") == 0
        and item.get("scenario_outcomes", {}).get("failures") == []
        and len(item.get("scenario_outcomes", {}).get("passed", [])) == 15
        and isinstance(item.get("generated_files_sha256"), dict)
        and bool(item["generated_files_sha256"])
        for item in results
    )
    input_audit_path = batch / "input-audit.json"
    input_audit = (
        json.loads(input_audit_path.read_text()) if input_audit_path.exists() else {}
    )
    expected_manifests = input_audit.get("manifest_sha256", {})
    input_audit_valid = input_audit.get("valid") is True and set(
        expected_manifests
    ) == set(ARMS)
    if input_audit_valid:
        input_audit_valid = all(
            sha256(batch / "repositories" / arm / "INPUT-MANIFEST.json")
            == expected_manifests[arm]
            for arm in ARMS
        )
    batch_path = batch / "batch.json"
    batch_metadata_valid = False
    if batch_path.exists():
        metadata = json.loads(batch_path.read_text())
        batch_metadata_valid = (
            metadata.get("specify", {}).get("commit") == SPEC_KIT_COMMIT
            and metadata.get("hidden_suite_sha256") == HIDDEN_SUITE_SHA256
        )
    comparable = (
        len(results) == len(ARMS)
        and [item["arm"] for item in results] == list(ARMS)
        and brief_hashes == [BRIEF_SHA256]
        and prompt_hashes == [PROMPT_SHA256]
        and suite_hashes == [HIDDEN_SUITE_SHA256]
        and schemas == ["2.0"]
        and len(settings) == 1
        and len(metric_schemas) == 1
        and outcomes_valid
        and input_audit_valid
        and batch_metadata_valid
    )
    audit = {
        "schema_version": "1.0",
        "comparable": comparable,
        "arms_expected": list(ARMS),
        "arms_present": [item["arm"] for item in results],
        "brief_sha256_values": brief_hashes,
        "prompt_sha256_values": prompt_hashes,
        "hidden_suite_sha256_values": suite_hashes,
        "result_schema_versions": schemas,
        "metric_schema_count": len(metric_schemas),
        "outcomes_valid": outcomes_valid,
        "input_audit_valid": input_audit_valid,
        "batch_metadata_valid": batch_metadata_valid,
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
        "manifest_arm_identity": all(manifests[arm].get("arm") == arm for arm in ARMS),
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
    required_core = {
        ".agents/skills/speckit-specify/SKILL.md",
        ".specify/workflows/speckit/workflow.yml",
    }
    checks["spec_kit_core_required_files"] = all(
        required_core <= set(files[arm])
        for arm in ("spec-kit-core", "proofmill-standard")
    )
    shared_core = [
        path
        for path in files["spec-kit-core"]
        if path.startswith(".agents/skills/speckit-")
        or path.startswith(".specify/scripts/")
        or path.startswith(".specify/templates/")
    ]
    checks["spec_kit_core_bytes_identical"] = bool(shared_core) and all(
        files["proofmill-standard"].get(path) == files["spec-kit-core"][path]
        for path in shared_core
    )
    release_skills = ROOT / "releases/proofmill-standard/0.1.0/skills"
    checks["ponytail_bytes_exact"] = all(
        files[arm].get(".agents/skills/ponytail/SKILL.md")
        == sha256(release_skills / "ponytail/SKILL.md")
        for arm in ("ponytail", "cavekit-ponytail", "proofmill-standard")
    )
    checks["proofmill_provider_bytes_exact"] = all(
        files["proofmill-standard"].get(path) == sha256(release_skills / source)
        for path, source in {
            ".agents/skills/simple-english/SKILL.md": "simple-english/SKILL.md",
            ".agents/skills/simple-english/references/checklist.md": "simple-english/references/checklist.md",
            ".agents/skills/simple-english/references/use-cases.md": "simple-english/references/use-cases.md",
        }.items()
    )
    release_components = ROOT / "releases/proofmill-standard/0.1.0/components"
    checks["proofmill_component_bytes_exact"] = all(
        files["proofmill-standard"].get(path) == sha256(release_components / source)
        for path, source in {
            ".specify/presets/proofmill-contract/preset.yml": "proofmill-contract/preset.yml",
            ".specify/workflows/proofmill-standard/workflow.yml": "proofmill-standard-workflow/workflow.yml",
        }.items()
    )
    cavekit = CHECKBOOK / "arms/cavekit-ponytail/vendor/cavekit/skills"
    checks["cavekit_bytes_exact"] = all(
        files["cavekit-ponytail"].get(f".agents/skills/{name}/SKILL.md")
        == sha256(cavekit / name / "SKILL.md")
        for name in ("spec", "build", "check", "caveman", "backprop")
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
    specify_metadata = verify_specify(specify)
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
        "specify": specify_metadata,
        "hidden_suite_sha256": sha256(CHECKBOOK / "hidden/run_suite.py"),
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
