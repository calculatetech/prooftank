# Add Claude Code conformance

<!-- markdownlint-disable MD013 MD046 -->

This ExecPlan is a living document. Maintain it according to
`.agent/PLANS.md` and update `docs/roadmap.md` with PM-007 status.

## Purpose / Big Picture

ProofTank Standard has one positive Codex specification run. This postponed
candidate task checks whether current Claude Code can install the same pinned composition, discover
the same contract and provider instructions, produce equivalent bounded
artifacts, expose missing providers, and uninstall without removing repository
truth.

## Bounded Work Packet

    profile: standard
    must_do:
      - inspect the current official Claude Code CLI and Spec Kit integration
      - use the reviewed Spec Kit, Ponytail, and SimpleEnglish exact pins
      - test clean integration install, provider failure, restart, and uninstall
      - run the PM-030 specification-only fixture if Claude authentication exists
      - compare stable IDs, artifact shape, scope, and evidence states with Codex
      - preserve unavailable or blocked states honestly
    must_not_do:
      - install a system-wide package or change user Claude configuration
      - request, print, or persist credentials
      - create plan, tasks, implementation, source code, or runtime
      - start OpenCode, Pi, normalization, or the checkbook benchmark
    may_do:
      - use a disposable package invocation and temporary project
      - stop for human authentication if the official CLI requires it
    stop_when:
      - conformance passes, or the exact human intervention is recorded

## Progress

- [x] (2026-08-11 23:39Z) Activated PM-007 and bounded it to current Claude
      integration and one specification-only fixture.
- [x] (2026-08-11 23:48Z) Pinned official Claude Code `2.1.228` and inspected
      the current Spec Kit Claude integration.
- [x] (2026-08-11 23:56Z) Corrected native provider discovery and passed
      disposable install, provider failure, dispatch, and uninstall checks.
- [x] (2026-08-12 00:12Z) Rejected unsafe integration input, passed relevant
      validation, and completed adversarial review cycle 2 with no findings.
- [ ] Run and compare the fixture if Claude conformance resumes with an
      authenticated subscription.
- [x] (2026-08-12 00:20Z) Preserved partial evidence and postponed PM-007 at the
      user's direction because no Claude subscription is available.

## Surprises & Discoveries

- Observation: The host has no `claude` executable on `PATH` at task start.
  Evidence: `command -v claude` returned unavailable.
- Observation: The standard workflow was Codex-specific at both its integration
  declaration and provider preflight path.
  Evidence: A valid `.claude/skills/` provider install failed as `unavailable:
  ponytail` until the workflow selected Claude's native directory.
- Observation: The current official CLI is installed only through a disposable
  exact-version invocation and is not authenticated.
  Evidence: `claude auth status --json` returned `loggedIn: false`, method
  `none`, and exit status 1.
- Observation: Review found that the workflow interpolated an unrestricted
  integration input into provider-preflight shell text.
  Evidence: Spec Kit supports an input enum while resolving the special `auto`
  value before execution. Restricting the input removes command substitution.

## Decision Log

- Decision: Use only a disposable official CLI invocation.
  Rationale: Conformance does not need a global package or changes to the user's
  harness configuration.
  Date/Author: 2026-08-11 / Codex.
- Decision: Add one native Claude branch to provider preflight.
  Rationale: Claude officially discovers `.claude/skills/`. A small explicit
  branch fixes the current target without introducing a generic adapter.
  Date/Author: 2026-08-11 / Codex.
- Decision: Restrict the integration input to `codex` and `claude`.
  Rationale: The workflow supports only those runtimes, and the constraint
  prevents shell metacharacters from reaching provider preflight. Current Spec
  Kit resolves its `auto` sentinel before applying the enum.
  Date/Author: 2026-08-11 / Codex.
- Decision: Do not ship the explored Claude branch in the active standard
  workflow while PM-007 is postponed.
  Rationale: The user redirected delivery to Codex, and the Claude model-backed
  comparison is still unknown.
  Date/Author: 2026-08-12 / Codex.

## Outcomes & Retrospective

PM-007 is postponed. Source, install, provider-failure, dispatch, security, and
uninstall evidence is complete. The required model-backed artifact comparison
did not run and remains `unknown`. The validated Claude workflow support stays
recorded in this plan, but it is not present in the active Codex-only workflow.

## Context and Orientation

`docs/HARNESS-CONFORMANCE.md` defines equivalent artifacts and runtime metadata.
The Codex reference output is preserved under `conformance/codex/pm-030/`.
Equivalent means the runtime can differ, but `REQ-001`, `INV-001`, feature
scope, artifact roles, and unknown deterministic evidence must retain the same
meaning.

Spec Kit `0.16.3.dev0` includes a Claude integration. The installed files and
namespace must be inspected from the pinned CLI rather than inferred from old
documentation. Provider skills must be copied at exact reviewed hashes.

## Plan of Work

Inspect the pinned Spec Kit Claude integration implementation and initialize a
disposable Claude target. Record every integration file and configuration
change. Test missing-provider preflight, exact-copy provider health, fresh
process discovery, integration uninstall, and repository-truth survival.

Resolve the current official Claude Code package version and license from its
primary package metadata. Invoke it without a global install. If it is already
authenticated, run the same specification-only status-note fixture used for
PM-030 and preserve its generated specification and checklist without repair.
If the CLI requires interactive login, stop and report that exact human action;
do not substitute credentials or another model.

## Milestones

The source milestone ends when exact current Claude and integration identities
are known. The lifecycle milestone ends when install effects, provider failure,
restart, disable, uninstall, and truth preservation have direct evidence. The
runtime milestone ends with either a preserved equivalent run or a precise
authentication blocker.

## Concrete Steps

Work from the current ProofTank checkout. Use
`/tmp/proofmill-speckit-venv/bin/specify` for the pinned Spec Kit CLI. Use
`npm view` and `npx` only for the official Claude Code package. Keep detailed
commands in `.agent/test-results/pm-007.md`.

Initialize the disposable target with:

    specify init --here --integration claude --force --ignore-agent-tools --script sh
    specify preset add --dev /absolute/path/to/prooftank/releases/prooftank-standard/0.2.0/components/prooftank-contract --priority 10

Install exact-copy providers, then test the same provider-preflight conditions
as the standard workflow. Use non-interactive Claude print mode only if current
CLI help confirms it and authentication is available.

## Validation and Acceptance

Current package and integration facts must come from primary metadata or pinned
source. Integration installation and uninstall must preserve the fixture's
specification truth. Missing required providers must be visible and stop the
standard workflow. A runtime pass also requires equivalent stable IDs, artifact
roles, scope, and `unknown` evidence without plan or implementation artifacts.

Changed Markdown must lint, repository YAML must parse, and `git diff --check`
must pass. A missing login is a human-intervention blocker, not a conformance
pass or provider failure.

## Idempotence and Recovery

All package and project targets are disposable. Recreate a failed setup before
the runtime invocation. Do not retry a measured Claude run to improve output.
Never modify user-level Claude configuration.

## Artifacts and Notes

Durable runtime evidence belongs under `conformance/claude/` only after a run.
Detailed command results belong in `.agent/test-results/pm-007.md`. If blocked,
keep this plan active and make the needed human action explicit.

## Interfaces and Dependencies

Use current official Claude Code, pinned Spec Kit, and exact-copy approved
provider skills. Add no repository dependency, executable source, adapter, or
runtime.

Latest revision: 2026-08-12. PM-007 was postponed without a model-backed run
because the project has no Claude subscription.
