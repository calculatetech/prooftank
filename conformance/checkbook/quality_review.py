#!/usr/bin/env python3
"""Create blind review snapshots and validate quality-audit reports."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import secrets
import shutil
from pathlib import Path


ARMS = (
    "bare",
    "ponytail",
    "cavekit-ponytail",
    "spec-kit-core",
    "proofmill-standard",
)
DIMENSIONS = (
    "single_outcome_ownership",
    "code_alone_readability",
    "cohesion",
    "change_locality",
    "invariant_visibility",
    "error_model_clarity",
    "accidental_complexity",
    "test_confidence",
    "operational_clarity",
    "production_ownership",
)
SEVERITIES = {"critical", "high", "medium", "low"}
LENSES = {"correctness", "production", "security", "maintainability"}
AUDIT_SURFACES = {
    "correctness",
    "failure_atomicity",
    "concurrency",
    "durability",
    "input_boundaries",
    "secrets",
    "injection",
    "denial_of_service",
    "observability",
    "packaging",
    "operations",
    "maintainability",
}
HIDDEN_SUITE = Path(__file__).parent / "hidden/run_suite.py"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def test_path(repository: Path) -> Path:
    choices = (repository / "test_checkbook.py", repository / "tests/test_checkbook.py")
    matches = [path for path in choices if path.is_file()]
    if len(matches) != 1:
        raise ValueError(f"expected one generated test file in {repository}")
    return matches[0]


def commitment(mapping: dict, nonce: str) -> str:
    encoded = json.dumps(mapping, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(f"{nonce}:{encoded}".encode()).hexdigest()


def hidden_scenarios(path: Path) -> set[str]:
    tree = ast.parse(path.read_text())
    return {
        f"__main__.CheckbookScenarios.{item.name}"
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "CheckbookScenarios"
        for item in node.body
        if isinstance(item, ast.FunctionDef) and item.name.startswith("test_")
    }


def requalify(batch: Path, source_manifest_path: Path, destination: Path) -> dict:
    source_manifest = json.loads(source_manifest_path.read_text())
    batch_data = json.loads((batch / "batch.json").read_text())
    suite_sha256 = sha256(HIDDEN_SUITE)
    scenarios = hidden_scenarios(HIDDEN_SUITE)
    if (
        source_manifest.get("batch_id") != batch.name
        or set(source_manifest.get("arms", {})) != set(ARMS)
        or batch_data.get("arms") != list(ARMS)
        or set(batch_data.get("order", [])) != set(ARMS)
        or not batch_data.get("spec_kit_commit")
        or source_manifest.get("hidden_suite_sha256") != suite_sha256
        or len(scenarios) != 15
    ):
        raise ValueError("frozen batch identity does not match")
    audit_path = batch / "results/audit.json"
    if (
        not audit_path.is_file()
        or sha256(audit_path) != source_manifest.get("batch_audit_sha256")
        or json.loads(audit_path.read_text()).get("comparable") is not True
    ):
        raise ValueError("frozen batch audit does not match")
    arms = {}
    for arm in ARMS:
        repository = batch / "repositories" / arm
        files = {
            "PRODUCT-BRIEF.md": repository / "PRODUCT-BRIEF.md",
            "checkbook.py": repository / "checkbook.py",
            "test_checkbook.py": test_path(repository),
        }
        actual = {name: sha256(path) for name, path in files.items()}
        if actual != source_manifest["arms"][arm]["files"]:
            raise ValueError(f"source hash mismatch: {arm}")
        result_path = batch / "rescored" / f"{arm}.json"
        result = json.loads(result_path.read_text())
        hidden = result.get("hidden", result)
        passed_tests = hidden.get("passed_tests")
        if (
            sha256(result_path)
            != source_manifest.get("rescored_result_sha256", {}).get(arm)
            or hidden.get("successful") is not True
            or hidden.get("passed") != 15
            or hidden.get("failed") != 0
            or not isinstance(passed_tests, list)
            or len(passed_tests) != len(set(passed_tests))
            or set(passed_tests) != scenarios
        ):
            raise ValueError(f"rescored result does not match: {arm}")
        arms[arm] = {"files": actual, "rescored_result_sha256": sha256(result_path)}
    result = {
        "schema_version": "1.0",
        "batch_id": batch.name,
        "batch_sha256": sha256(batch / "batch.json"),
        "batch_audit_sha256": sha256(audit_path),
        "source_manifest_sha256": sha256(source_manifest_path),
        "spec_kit_commit": batch_data["spec_kit_commit"],
        "hidden_suite_sha256": suite_sha256,
        "hidden_scenarios_passed_per_arm": 15,
        "arms": arms,
        "valid": True,
    }
    write_json(destination, result)
    return result


def snapshot(
    batch: Path,
    destination: Path,
    mapping_path: Path,
    source_manifest_path: Path,
    requalification_path: Path,
) -> dict:
    if destination.exists() or mapping_path.exists():
        raise FileExistsError(destination if destination.exists() else mapping_path)
    repositories = batch.resolve(strict=True) / "repositories"
    source_manifest = json.loads(source_manifest_path.read_text())
    requalification = json.loads(requalification_path.read_text())
    if source_manifest.get("batch_id") != batch.name or set(
        source_manifest.get("arms", {})
    ) != set(ARMS):
        raise ValueError("source manifest does not match the frozen batch")
    if (
        requalification.get("valid") is not True
        or requalification.get("batch_id") != batch.name
        or requalification.get("source_manifest_sha256") != sha256(source_manifest_path)
    ):
        raise ValueError("current requalification does not match")
    audit_path = batch / "results/audit.json"
    if (
        not audit_path.is_file()
        or sha256(audit_path) != source_manifest.get("batch_audit_sha256")
        or json.loads(audit_path.read_text()).get("comparable") is not True
    ):
        raise ValueError("frozen batch audit does not match")
    rescored = source_manifest.get("rescored_result_sha256", {})
    if set(rescored) != set(ARMS):
        raise ValueError("all rescored results are required")
    for arm, expected in rescored.items():
        result_path = batch / "rescored" / f"{arm}.json"
        result = json.loads(result_path.read_text())
        if (
            sha256(result_path) != expected
            or result.get("hidden", result).get("successful") is not True
        ):
            raise ValueError(f"rescored result does not match: {arm}")
    order = list(ARMS)
    secrets.SystemRandom().shuffle(order)
    mapping = {f"candidate-{index}": arm for index, arm in enumerate(order, start=1)}
    nonce = secrets.token_hex(32)
    write_json(
        mapping_path,
        {"schema_version": "1.0", "nonce": nonce, "mapping": mapping},
    )
    candidates = {}
    for candidate_id, arm in mapping.items():
        repository = repositories / arm
        candidate = destination / candidate_id
        candidate.mkdir(parents=True)
        shutil.copy2(repository / "PRODUCT-BRIEF.md", candidate / "PRODUCT-BRIEF.md")
        shutil.copy2(repository / "checkbook.py", candidate / "checkbook.py")
        shutil.copy2(test_path(repository), candidate / "test_checkbook.py")
        source_files = {
            "PRODUCT-BRIEF.md": repository / "PRODUCT-BRIEF.md",
            "checkbook.py": repository / "checkbook.py",
            "test_checkbook.py": test_path(repository),
        }
        expected = source_manifest["arms"][arm]["files"]
        actual_source = {name: sha256(path) for name, path in source_files.items()}
        if actual_source != expected:
            raise ValueError(f"source hash mismatch: {arm}")
        files = {
            path.name: sha256(path)
            for path in sorted(candidate.iterdir())
            if path.is_file()
        }
        candidates[candidate_id] = {"files": files}
    manifest = {
        "schema_version": "1.0",
        "batch_id": batch.name,
        "mapping_commitment": commitment(mapping, nonce),
        "source_manifest_sha256": sha256(source_manifest_path),
        "requalification_sha256": sha256(requalification_path),
        "candidates": candidates,
    }
    write_json(destination.parent / "review-manifest.json", manifest)
    validate_snapshots(destination, manifest)
    return manifest


def validate_snapshots(destination: Path, manifest: dict) -> None:
    expected_ids = {f"candidate-{index}" for index in range(1, 6)}
    if set(manifest.get("candidates", {})) != expected_ids:
        raise ValueError("manifest must contain five neutral candidates")
    for candidate_id, item in manifest["candidates"].items():
        candidate = destination / candidate_id
        actual = {
            str(path.relative_to(candidate)): sha256(path)
            for path in sorted(candidate.rglob("*"))
            if path.is_file()
        }
        if any(path.is_dir() for path in candidate.rglob("*")):
            raise ValueError(f"unexpected review directory: {candidate_id}")
        if actual != item.get("files"):
            raise ValueError(f"snapshot hash mismatch: {candidate_id}")
        if set(actual) != {"PRODUCT-BRIEF.md", "checkbook.py", "test_checkbook.py"}:
            raise ValueError(f"unexpected review file set: {candidate_id}")


def validate_evidence(evidence: object, candidate: Path, files: dict) -> None:
    if not isinstance(evidence, list) or not evidence:
        raise ValueError("evidence must be a non-empty list")
    for reference in evidence:
        if not isinstance(reference, dict):
            raise ValueError("evidence entry must be an object")
        path = reference.get("path")
        line = reference.get("line")
        detail = reference.get("detail")
        if path not in files or type(line) is not int or line < 1:
            raise ValueError(f"invalid evidence location: {reference}")
        line_count = len((candidate / path).read_text().splitlines())
        if line > line_count or not isinstance(detail, str) or not detail.strip():
            raise ValueError(f"invalid evidence detail: {reference}")


def validate_report(candidate: Path, manifest: dict, report: dict) -> None:
    candidate_id = candidate.name
    if (
        report.get("schema_version") != "1.0"
        or report.get("candidate_id") != candidate_id
    ):
        raise ValueError("report identity does not match candidate")
    files = manifest["candidates"][candidate_id]["files"]
    findings = report.get("findings")
    if not isinstance(findings, list):
        raise ValueError("findings must be a list")
    finding_ids = set()
    for finding in findings:
        finding_id = finding.get("id")
        if not isinstance(finding_id, str) or finding_id in finding_ids:
            raise ValueError("finding ids must be unique strings")
        finding_ids.add(finding_id)
        if (
            finding.get("severity") not in SEVERITIES
            or finding.get("lens") not in LENSES
        ):
            raise ValueError(f"invalid finding classification: {finding_id}")
        for field in ("title", "impact", "remediation"):
            if not isinstance(finding.get(field), str) or not finding[field].strip():
                raise ValueError(f"missing finding {field}: {finding_id}")
        validate_evidence(finding.get("evidence"), candidate, files)
    blockers = report.get("production_blockers")
    if not isinstance(blockers, list) or not set(blockers) <= finding_ids:
        raise ValueError("production blockers must reference findings")
    dimensions = report.get("dimensions")
    if not isinstance(dimensions, dict) or set(dimensions) != set(DIMENSIONS):
        raise ValueError("all ten dimensions are required")
    for name, dimension in dimensions.items():
        score = dimension.get("score")
        if type(score) is not int or score not in range(1, 6):
            raise ValueError(f"invalid dimension score: {name}")
        validate_evidence(dimension.get("evidence"), candidate, files)
    readiness = report.get("overall_readiness")
    readiness_score = readiness.get("score") if isinstance(readiness, dict) else None
    if type(readiness_score) is not int or readiness_score not in range(1, 6):
        raise ValueError("overall readiness score must be one through five")
    require_text(readiness, "rationale")
    ownership = report.get("take_production_ownership")
    if not isinstance(ownership, dict) or ownership.get("answer") not in {
        "yes",
        "conditional",
        "no",
    }:
        raise ValueError("production ownership answer is required")
    if not isinstance(ownership.get("conditions"), list):
        raise ValueError("production ownership conditions must be a list")
    require_text(ownership, "rationale")
    for field in ("security_posture", "strongest_quality", "weakest_quality"):
        if not isinstance(report.get(field), str) or not report[field].strip():
            raise ValueError(f"missing report field: {field}")
    confidence = report.get("test_confidence")
    if not isinstance(confidence, dict) or not isinstance(confidence.get("gaps"), list):
        raise ValueError("test confidence and gaps are required")
    require_text(confidence, "supplied")
    surfaces = report.get("audit_surfaces")
    if not isinstance(surfaces, dict) or set(surfaces) != AUDIT_SURFACES:
        raise ValueError("all audit surfaces are required")
    for name, surface in surfaces.items():
        if not isinstance(surface, dict) or surface.get("status") not in {
            "checked",
            "finding",
            "unknown",
        }:
            raise ValueError(f"invalid audit surface: {name}")
        require_text(surface, "detail")
        evidence = surface.get("evidence")
        if surface["status"] == "unknown":
            if evidence not in (None, []):
                raise ValueError(f"unknown surface cannot claim evidence: {name}")
        else:
            validate_evidence(evidence, candidate, files)
    verification = report.get("verification")
    if not isinstance(verification, dict):
        raise ValueError("verification is required")
    require_text(verification, "command")
    require_text(verification, "outcome")
    exit_status = verification.get("exit_status")
    if exit_status is not None and type(exit_status) is not int:
        raise ValueError("verification exit status must be an integer or null")
    if exit_status is None:
        require_text(verification, "unknown_reason")


def require_text(value: dict, field: str) -> None:
    if not isinstance(value.get(field), str) or not value[field].strip():
        raise ValueError(f"non-empty {field} is required")


def validate_review_batch(root: Path, manifest: dict, protocol: dict) -> dict:
    expected = protocol.get("app_reviews_per_candidate")
    if expected != 2:
        raise ValueError("protocol must require two reviews per candidate")
    reports = {}
    reviewers = {}
    for candidate_id in sorted(manifest["candidates"]):
        paths = sorted((root / candidate_id).glob("review-*.json"))
        if len(paths) != expected:
            raise ValueError(f"expected two reports: {candidate_id}")
        reports[candidate_id] = {}
        for path in paths:
            envelope = json.loads(path.read_text())
            reviewer_id = envelope.get("reviewer_id")
            if (
                not isinstance(reviewer_id, str)
                or not reviewer_id
                or reviewer_id in reviewers
            ):
                raise ValueError("every report requires a fresh reviewer")
            if envelope.get("settings") != protocol.get("reviewer_settings"):
                raise ValueError(f"review settings drift: {path}")
            validate_report(
                root.parent / "candidates" / candidate_id,
                manifest,
                envelope.get("report"),
            )
            reports[candidate_id][path.name] = sha256(path)
            reviewers.setdefault(reviewer_id, []).append(candidate_id)
    validate_snapshots(root.parent / "candidates", manifest)
    protocol_root = Path(__file__).parent
    if sha256(protocol_root / "QUALITY-AUDIT.md") != protocol.get("rubric_sha256"):
        raise ValueError("rubric hash drift")
    sandbox_path = root.parent / "sandbox.py"
    if sha256(sandbox_path) != protocol.get("sandbox_sha256"):
        raise ValueError("sandbox hash drift")
    result = {
        "schema_version": "1.0",
        "reports": reports,
        "reviewer_assignments": reviewers,
    }
    write_json(root.parent / "report-manifest.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare = subparsers.add_parser("snapshot")
    prepare.add_argument("batch", type=Path)
    prepare.add_argument("destination", type=Path)
    prepare.add_argument("mapping", type=Path)
    prepare.add_argument("source_manifest", type=Path)
    prepare.add_argument("requalification", type=Path)
    qualify = subparsers.add_parser("requalify")
    qualify.add_argument("batch", type=Path)
    qualify.add_argument("source_manifest", type=Path)
    qualify.add_argument("destination", type=Path)
    validate = subparsers.add_parser("validate-report")
    validate.add_argument("candidate", type=Path)
    validate.add_argument("manifest", type=Path)
    validate.add_argument("report", type=Path)
    batch_validate = subparsers.add_parser("validate-batch")
    batch_validate.add_argument("reports", type=Path)
    batch_validate.add_argument("manifest", type=Path)
    batch_validate.add_argument("protocol", type=Path)
    args = parser.parse_args()
    if args.command == "requalify":
        requalify(args.batch, args.source_manifest, args.destination)
    elif args.command == "snapshot":
        snapshot(
            args.batch,
            args.destination,
            args.mapping,
            args.source_manifest,
            args.requalification,
        )
    elif args.command == "validate-report":
        manifest = json.loads(args.manifest.read_text())
        report = json.loads(args.report.read_text())
        validate_snapshots(args.candidate.parent, manifest)
        validate_report(args.candidate, manifest, report.get("report", report))
    else:
        validate_review_batch(
            args.reports,
            json.loads(args.manifest.read_text()),
            json.loads(args.protocol.read_text()),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
