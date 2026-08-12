# Requalify the corrected Codex contract

<!-- markdownlint-disable MD013 MD046 -->

This ExecPlan is a living document. Maintain it according to
`.agent/PLANS.md` and update `docs/roadmap.md` with PM-030 status.

## Purpose / Big Picture

The first Codex dry run created the expected specification but incorrectly
treated human inspection as evidence and did not carry the appended Proofmill
contract into its checklist. This task runs one corrected, specification-only
fixture. It shows whether Codex now keeps missing deterministic coverage
`unknown`, includes the contract in review, and stops before planning.

## Bounded Work Packet

    profile: standard
    must_do:
      - use the reviewed Spec Kit, Ponytail, and SimpleEnglish exact pins
      - run one fresh Codex specification-only fixture
      - require stable requirement and invariant identifiers
      - require human inspection and missing executable coverage to stay unknown
      - require the Proofmill contract to reach the generated checklist
      - preserve the generated specification and checklist as evidence
    must_not_do:
      - create a plan, tasks, source code, or runtime
      - claim provider or agent output as deterministic proof
      - start the checkbook benchmark
      - broaden the fixture after the run begins
    may_do:
      - refine fixture instructions before the single measured run
      - report a negative qualification result without repairing generated output
    stop_when:
      - one fresh run is preserved and evaluated against every condition
      - roadmap, gap report, and this plan record the result

## Progress

- [x] (2026-08-11 23:09Z) Activated PM-030 and bounded it to one corrected
      Codex specification-only qualification.
- [x] (2026-08-11 23:18Z) Prepared a fresh pinned Spec Kit target with both
      exact-copy approved skills.
- [x] (2026-08-11 23:22Z) Ran Codex once and preserved the generated
      specification and checklist byte for byte.
- [x] (2026-08-11 23:25Z) Passed artifact scope, full contract coverage, and
      evidence-state assertions.
- [x] (2026-08-11 23:31Z) Updated durable records, passed relevant validation,
      completed PM-030, and archived this plan.

## Surprises & Discoveries

- Observation: Current Spec Kit `init` does not accept `--no-git`.
  Evidence: The setup-only attempt exited before creating `.specify/`; removing
  that option completed initialization before Codex started.
- Observation: One corrected prompt was sufficient for the generated core
  checklist to review the appended Proofmill contract.
  Evidence: The preserved checklist contains a Proofmill Contract Review section
  and leaves both missing deterministic mappings unchecked.

## Decision Log

- Decision: Measure generated output as-is and do not repair it after the run.
  Rationale: Qualification must expose Codex behavior, including negative
  results, instead of converting agent output into a hand-authored pass.
  Date/Author: 2026-08-11 / Codex.

## Outcomes & Retrospective

PM-030 is complete. One fresh Codex run created only the required specification
and checklist. It preserved stable IDs, reviewed the appended contract, and
kept missing executable coverage and human inspection `unknown`. The result is
bounded evidence for this run, not proof of implementation or future output.

## Context and Orientation

Spec Kit is pinned at commit
`bd595cf838cc200f84fee9e9327b643dfe277d2c`, source version `0.16.3.dev0`.
`presets/proofmill-contract/templates/spec-template.md` appends the Proofmill
contract to core feature specifications. It explicitly says human inspection
and agent output are not deterministic evidence, and it requires absent
deterministic coverage to remain `unknown`.

The first dry run is recorded in `.agent/test-results/bootstrap.md`. It created
`spec.md` and the core requirements checklist, but its evidence field relied on
human review, its unknowns field said none, and the checklist did not review the
appended contract. PM-026 later selected no deterministic gate. Therefore this
run must report the fixture's missing executable coverage honestly.

## Plan of Work

Create a disposable Git repository. Initialize current pinned Spec Kit for
Codex, add the local Proofmill preset, and install exact copies of Ponytail and
SimpleEnglish using the reviewed commits and hashes. Use the generated
`speckit.specify` skill plus both provider skills in one Codex invocation.

The fixture adds one README status sentence and nothing else. Ask for
specification artifacts only, stable `REQ-001` and `INV-001`, explicit
`unknown` evidence where no executable check exists, and checklist review of
the Proofmill contract. Prohibit plan, tasks, and implementation. After the
single run, copy only its specification and checklist into a bounded conformance
directory. Do not edit their content.

Evaluate the preserved artifacts with literal searches and file-boundary
checks. Update the gap report and roadmap whether the result passes or fails.
Run only relevant Markdown, YAML, and composition checks.

## Milestones

The fixture milestone ends when a fresh target contains the reviewed
composition and exact provider bytes. The run milestone ends after one Codex
invocation returns and its artifacts are copied without repair. The evaluation
milestone ends when scope, stable IDs, contract coverage, and evidence states
have explicit pass or fail results. The record milestone ends when those facts
are durable and PM-030 is closed.

## Concrete Steps

Work from `/home/mbeutler/Projects/proofmill`. Use the pinned `specify`
executable from the bootstrap validation environment, or install the same
commit into a disposable virtual environment if it is absent. Initialize a
temporary target with:

    specify init --here --integration codex --force
    specify preset add --dev /home/mbeutler/Projects/proofmill/presets/proofmill-contract --priority 10

Copy exact provider directories into `.agents/skills/`, check their reviewed
hashes, and run one `codex exec --ephemeral --ignore-user-config` invocation.
Detailed commands and results belong in `.agent/test-results/pm-030.md`.

## Validation and Acceptance

The run must create one feature `spec.md` and one checklist. It must create no
plan, task list, source file, or implementation artifact. The specification
must include `REQ-001`, `INV-001`, the appended Proofmill contract, and an
`unknown` state for human inspection and missing deterministic coverage. The
checklist must review the contract rather than stopping at the core template.

Changed Markdown must lint, repository YAML must parse, the current preset must
resolve through pinned Spec Kit, and `git diff --check` must pass. A failed
artifact condition is a valid negative qualification outcome, not permission to
edit the generated evidence.

## Idempotence and Recovery

The target is disposable. If setup fails before Codex starts, recreate it and
retry. Once Codex begins the measured invocation, do not rerun it to improve the
answer. Preserve failure output and close the qualification honestly.

## Artifacts and Notes

Generated evidence belongs under `conformance/codex/pm-030/`. Detailed command
status belongs only in `.agent/test-results/pm-030.md`. Durable interpretation
belongs in `docs/BOOTSTRAP-GAP-REPORT.md` and this plan.

## Interfaces and Dependencies

Use the reviewed Spec Kit CLI, current Codex CLI, and the exact-copy Ponytail
and SimpleEnglish skills. Add no dependency, executable source, or runtime to
Proofmill.

Latest revision: 2026-08-11. PM-030 completed with one positive bounded Codex
contract qualification.
