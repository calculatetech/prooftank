# Qualify the Smallest Deterministic Gate

<!-- markdownlint-disable MD013 MD046 -->

This ExecPlan is a living document. Maintain it according to
`.agent/PLANS.md`. Update `docs/roadmap.md` in the same change when PM-026
changes status.

## Purpose / Big Picture

Proofmill Standard can install and stop on missing required skills, but it
cannot yet prove requirement coverage or evidence readiness. This task reviews
current Spec Kit core and community candidates and qualifies the smallest
existing deterministic gate, or records that none is safe enough. A user can
then see one exact provider decision, its trust boundary, and a reproducible
pass and fail result without a new Proofmill runtime.

Stop before the checkbook benchmark, cross-harness work, optional structural or
memory providers, and critical-profile design.

## Bounded Work Packet

    profile: standard
    must_do:
      - inspect current Spec Kit core and catalog primary sources
      - screen quality-gate, CI-guard, TDD, verification, traceability, and evidence candidates
      - fully qualify only the smallest candidate that can make a deterministic claim
      - preserve exact pins, rejections, failures, fallback, and uninstall behavior
      - update the roadmap and durable qualification records
    must_not_do:
      - build a Proofmill gate, daemon, database, agent loop, or adapter protocol
      - start the checkbook benchmark or cross-harness matrix
      - claim that agent judgment is deterministic evidence
      - enable a candidate before its required lifecycle checks pass
    may_do:
      - select no provider when every candidate fails the qualification bar
      - add one reviewed Spec Kit component to the standard composition
      - keep project-native tests and lint as the fallback
    stop_when:
      - current candidate identities and source behavior are recorded
      - one provider is selected and validated or all candidates are rejected
      - the standard composition remains current-valid and removable
      - PM-026 is completed with the next roadmap task visible
    required_checks:
      - current source, license, manifest, hook, command, file, and network inspection
      - clean install, health, success, failure, malformed-input, restart, disable, and uninstall tests
      - repository-truth survival and false-success checks
      - current Spec Kit validation, YAML parse, and Markdown lint

## Progress

- [x] (2026-08-11 21:42Z) Activated PM-026 and bounded the qualification work.
- [x] (2026-08-11 21:51Z) Resolved ten exact candidate sources and separated
      prompt-driven advice from deterministic execution.
- [x] (2026-08-11 21:51Z) Qualified `gates` `0.3.3` and preserved the rejection
      set. The candidate passes its upstream suite but fails Proofmill's
      coverage, lifecycle, security, and minimum-surface bar.
- [x] (2026-08-11 21:51Z) Selected no provider. The composition and runtime
      configuration remain unchanged.
- [x] (2026-08-11 21:51Z) Ran repository YAML, Markdown, and current Spec Kit
      validation. No
      adversarial code review is required because PM-026 changed documentation
      and registry records only.
- [x] (2026-08-11 21:51Z) Completed PM-026 and updated the roadmap. This plan
      is ready to archive under `docs/exec-plans/completed/`.

## Surprises & Discoveries

- Observation: Most named verification candidates are prompt packs, not
  deterministic gates.
  Evidence: `ci-guard`, `tdd`, `verify`, `verify-tasks`, `trace`, and `spectest`
  register agent Markdown commands and hooks but no owning verifier.
- Observation: The leading candidate's exact upstream suite is healthy only
  after its full declared toolchain is present.
  Evidence: `bash tests/run.sh` passed with locked npm dependencies and
  ShellCheck `0.11.0`.
- Observation: A green spec-gates result does not prove deterministic coverage.
  Evidence: a `Complete` fixture with checked tasks and zero acceptance blocks
  returned exit 0; `doctor.sh` also returned exit 0 and called it enforced.
- Observation: Extension lifecycle commands do not own the projected runtime.
  Evidence: `.specify/gates/verify.sh` remained executable after both
  `specify extension disable gates` and `specify extension remove gates`.
- Observation: The exact release has a vulnerable development toolchain.
  Evidence: `npm ci` reported two high-severity advisories for direct
  `markdownlint-cli2` and transitive `js-yaml`.

## Decision Log

- Decision: A valid outcome can select no provider.
  Rationale: Proofmill must not convert catalog presence or agent output into a
  false deterministic gate. A measured rejection is safer than an unqualified
  dependency.
  Date/Author: 2026-08-11 / Codex with Ponytail.
- Decision: Block `gates` `0.3.3` and keep the current native fallback.
  Rationale: Its explicit checks are deterministic, but missing executable
  coverage can pass. Installation depends on an agent projection, disable and
  uninstall leave that projection active, the lockfile has high-severity
  advisories, and the extension adds a broad runtime. Fixing these gaps locally
  would create the prohibited Proofmill gate or adapter.
  Date/Author: 2026-08-11 / Codex with Ponytail.
- Decision: Do not start the adversarial code-review cycle.
  Rationale: PM-026 changed documentation, the roadmap, and an upstream registry
  record only. Repository rules exclude these changes from meaningful code
  review. The simple-and-relevant finding challenge applies only to findings
  from fresh clean-context adversarial review subagents.
  Date/Author: 2026-08-11 / Codex.

## Outcomes & Retrospective

PM-026 selected no provider. Ten current candidates have exact source records,
and the leading candidate has a complete qualification record. The standard
composition is unchanged and still uses project-native tests and lint. Missing
deterministic coverage remains `unknown`. No Proofmill runtime, daemon,
database, adapter, or checkbook work was added.

All changed YAML parsed, all changed Markdown linted without findings, and a
fresh current Spec Kit fixture installed and resolved the unchanged standard
composition. PM-001 remains the next roadmap task.

## Context and Orientation

GitHub Spec Kit owns extensions, workflows, bundles, and their installation.
`workflows/proofmill-standard/workflow.yml` currently uses core commands and a
native shell check. `bundles/proofmill-standard/bundle.yml` records the standard
composition. `upstream/registry.yml` and `upstream/reviews/` own provider pins
and qualification state. `docs/BOOTSTRAP-GAP-REPORT.md` records the evidence
gap and the initial unverified candidate screen.

A deterministic gate is a command whose defined input produces a reproducible
pass or fail result. An agent review, generated checklist, or human gate is not
deterministic. A selected provider must fail closed when it crashes, is absent,
or receives malformed input. Removal must preserve specifications, plans,
tasks, source code, and existing evidence.

The initial screen named `gates`, `ci-guard`, `tdd`, `verify`, `verify-tasks`,
`trace`, `v-model`, `spectest`, `patchwarden-evidence`, and `docguard`. Catalog
metadata is discovery evidence only. Inspect current source before relying on
any name, version, or behavior.

## Plan of Work

First, resolve the current Spec Kit commit and catalogs from the primary GitHub
repository. For each candidate, follow its catalog source to the exact package
or repository. Read manifests and executable paths before running anything.
Record a compact comparison that separates deterministic scripts from agent
commands, hooks, and human gates.

Second, choose the first candidate on the Ponytail ladder that covers the actual
gap. Prefer current Spec Kit core, then a declarative component with no new
dependency, then an already required tool. Reject broader frameworks, duplicate
specification owners, evidence packagers without verification, and components
whose source cannot be pinned or removed safely.

Third, run the full qualification matrix for only the leading candidate. Use a
disposable Spec Kit Codex fixture. Preserve failures in
`.agent/test-results/pm-026.md`. If the candidate passes, add the smallest
current-valid component reference and a qualification review. If it fails,
remove the fixture and record the rejection without enabling it.

Finally, validate all changed YAML and Markdown. If executable composition or
runtime configuration changed, run the required fresh adversarial review cycles
before completion. Move this plan to `docs/exec-plans/completed/` only when the
roadmap and durable records agree.

## Milestones

The source-resolution milestone ends when every screened candidate points to a
current exact source or an explicit unresolved-source rejection. The evidence is
a durable comparison with licenses, claimed capability, executable mechanism,
and maintenance state.

The qualification milestone ends when the smallest viable candidate completes
the required install and lifecycle matrix, or when every candidate is rejected
with a reproducible reason. No composition change is allowed before this point.

The integration milestone exists only if a candidate passes. It ends when a
fresh fixture can install, produce one deterministic pass and one deterministic
failure, fail closed when unavailable, and uninstall without removing repository
truth.

## Concrete Steps

Work from `/home/mbeutler/Projects/proofmill`. Resolve current source into a
disposable directory:

    upstream_root=$(mktemp -d /tmp/proofmill-pm026.XXXXXX)
    git clone https://github.com/github/spec-kit.git "$upstream_root/spec-kit"
    git -C "$upstream_root/spec-kit" rev-parse HEAD
    git -C "$upstream_root/spec-kit" describe --tags --always

Read the current community catalog and each selected manifest. Add exact
candidate commands here after their source formats are known. Do not improvise
install commands from stale bootstrap notes.

Use the current Spec Kit source in an isolated environment for fixture tests:

    speckit_venv=$(mktemp -d /tmp/proofmill-pm026-venv.XXXXXX)
    python3 -m venv "$speckit_venv"
    "$speckit_venv/bin/pip" install "$upstream_root/spec-kit"
    "$speckit_venv/bin/specify" version --features --json

Exact commands, source revisions, exit codes, and concise failure evidence are
recorded in `.agent/test-results/pm-026.md`. The durable comparison is
`docs/DETERMINISTIC-GATE-QUALIFICATION.md`, and the complete provider record is
`upstream/reviews/spec-gates.md`.

## Validation and Acceptance

Acceptance requires a durable source comparison and either one fully qualified
provider or an explicit no-selection result. A selected gate must show a known
passing input and a known failing input with different non-ambiguous exit states.
Absent, crashed, malformed, and stale evidence must not become `passed`.

The selected component, if any, must install through the reviewed current Spec
Kit interface, survive a fresh process, disable cleanly, uninstall cleanly, and
leave repository truth usable. All changed YAML must parse. All changed Markdown
must pass the repository's current `markdownlint-cli2` check.

## Idempotence and Recovery

All upstream clones, virtual environments, and conformance projects are
disposable under `/tmp`. Recreate a fixture instead of repairing uncertain
state. Never initialize Spec Kit in the Proofmill source tree.

Before uninstall tests, copy or create a small repository-owned specification
in the fixture. After removal, verify that it remains. A partial component
install must be removed with the reviewed Spec Kit command before a retry.

## Artifacts and Notes

Durable provider reviews belong under `upstream/reviews/`. Update
`upstream/registry.yml` for any newly selected or rejected provider. Put the
candidate comparison in `docs/` and link it from the gap report. Keep detailed
test output only in ignored `.agent/test-results/pm-026.md`.

## Interfaces and Dependencies

Use the current GitHub Spec Kit CLI and component schemas found during this
task. Do not add a Proofmill executable interface. A selected third-party gate
must have an exact source pin, a license allowed by `proofmill.yml`, an explicit
trust class, and a documented fallback to project-native tests and lint.

Latest revision: 2026-08-11. PM-026 completed with no provider selected after
the current source, lifecycle, and composition validations passed.
