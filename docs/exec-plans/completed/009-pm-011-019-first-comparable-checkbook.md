# Produce the first comparable checkbook benchmark

<!-- markdownlint-disable MD013 MD046 -->

This ExecPlan is a living document. Maintain it according to
`.agent/PLANS.md`. Update `docs/roadmap.md` whenever the active benchmark task
changes.

## Purpose / Big Picture

The benchmark must determine whether Proofmill Standard improves accepted
behavior enough to justify its added process. This plan freezes one neutral
checkbook contract, creates an external hidden suite, runs the same Codex model
against five controlled instruction arms, preserves results, and publishes the
first honest comparison. The work stops as soon as a valid comparable result
exists.

## Bounded Work Packet

    profile: critical
    must_do:
      - complete PM-011 through PM-019 in roadmap order
      - freeze one stack, public interface, requirement ceiling, and prompt
      - keep hidden acceptance and fault checks outside arm repositories
      - use Codex as the only runtime with one pinned CLI, model, and effort
      - create bare, Ponytail, Cavekit-plus-Ponytail, Spec Kit core, and Proofmill Standard arms
      - preserve failed and negative runs
      - record quality, scope, effort, and lifecycle metrics
      - audit requirement and input parity before comparison
      - publish a result even when Proofmill loses
    must_not_do:
      - run Proofmill Critical or another harness
      - reveal hidden suite source to an implementation arm
      - repair an arm before recording its first-pass result
      - add an application framework, service, daemon, or benchmark database
      - change success thresholds after a run starts
      - implement PM-020 or later provider pilots
    may_do:
      - use Python standard library and SQLite for every arm
      - stop after one complete run per arm when it yields a comparable result
      - mark unavailable measurements unknown
    stop_when:
      - all five arms receive byte-identical neutral inputs and fixed settings
      - the hidden suite produces comparable first-pass results
      - preserved metrics state limitations and a winner or no-winner result

## Progress

- [x] (2026-08-12 02:04Z) Received explicit approval to run the checkbook
      benchmark until a comparable result exists.
- [x] (2026-08-12 02:09Z) Read the existing brief and experiment, selected
      standard-library Python and SQLite, and inspected current Cavekit `4.1.0`.
- [x] (2026-08-12 02:22Z) Completed PM-011. Froze the public contract,
      experiment controls, exact input hashes, and working Codex runner.
- [x] (2026-08-12 02:44Z) Completed PM-012 through PM-017. Added the external
      suite and five exact, isolated arm definitions. PM-018 remains.
- [x] (2026-08-12 03:01Z) Completed PM-018. The controller passes unit, lint,
      preparation, treatment-isolation, and parity checks.
- [x] (2026-08-12 03:47Z) Completed PM-019. All five arms completed and passed
      15 of 15 after a contract-aligned rescore of unchanged repositories.

## Surprises & Discoveries

- Observation: The starter brief lists behavior but no callable interface or
  fixed stack, so an external suite cannot compare independent implementations.
  Evidence: `conformance/checkbook/PRODUCT-BRIEF.md` names neither language,
  module, signatures, return shapes, nor error contract.
- Observation: Current Cavekit is `4.1.0` at commit
  `c322f0bb6db82163041930467f3ce32754d42827` and targets Claude by default.
  Evidence: Its primary repository tags that commit and installs skills under
  `.claude/skills/`. The comparison arm must use exact skill copies under
  Codex's `.agents/skills/` without enabling Cavekit as a Proofmill owner.
- Observation: The first hidden score enforced two details absent from the
  frozen public contract.
  Evidence: All five arms omitted `closed_through` from account output, and the
  suite demanded operation identifiers on validation errors beyond import and
  reconciliation. Removing those assertions made all unchanged arms pass.

## Decision Log

- Decision: Use Python 3.12 or newer, only its standard library, and SQLite.
  Rationale: Every arm receives one inspectable local stack with transactional
  storage and no dependency-install variance.
  Date/Author: 2026-08-12 / Codex.
- Decision: Run Codex CLI `0.147.0`, model `gpt-5.4`, and medium reasoning for
  every arm.
  Rationale: Explicit runner settings are more comparable than a changing
  account default. Local CLI help confirms the model and config overrides.
  Date/Author: 2026-08-12 / Codex.
- Decision: One complete first-pass run per arm is the minimum comparable
  result authorized by the user.
  Rationale: Five arms under identical inputs can compare first-pass outcomes.
  Replication beyond that belongs after the first comparison establishes that
  the controller works.
  Date/Author: 2026-08-12 / Codex.
- Decision: Use a repository-local controller and external temporary arm
  repositories, not a benchmark service.
  Rationale: Files, subprocesses, JSON, `unittest`, and Git are sufficient.
  Date/Author: 2026-08-12 / Codex.
- Decision: Skip adversarial reviews for benchmark implementation.
  Rationale: The user explicitly waived these reviews for benchmarking. Normal
  production Proofmill work keeps the repository review rule.
  Date/Author: 2026-08-12 / User.
- Decision: Rescore unchanged repositories after correcting the external suite.
  Rationale: Rerunning model arms would measure a new sample. Rescoring removes
  controller overclaims without repairing an implementation.
  Date/Author: 2026-08-12 / Codex.

## Outcomes & Retrospective

PM-011 through PM-019 are complete. The first batch is comparable. Every arm
passed all 15 contract-aligned scenarios. Proofmill Standard added process cost
without a quality gain; Ponytail-only led the measured efficiency fields.

## Context and Orientation

`conformance/checkbook/PRODUCT-BRIEF.md` is the only product instruction shared
with every arm. `conformance/checkbook/EXPERIMENT.md` defines controller-only
rules. Hidden tests will live under `conformance/checkbook/hidden/` in Proofmill
and will not be copied into an arm repository. Arm definitions will live under
`conformance/checkbook/arms/`. Preserved run summaries will live under
`conformance/checkbook/results/`; bulky transcripts and disposable repositories
belong under ignored `.agent/benchmark-runs/`.

An arm is one instruction treatment. The bare arm gets only the neutral brief.
The provider arms add only their named exact skills. Spec Kit core adds the
pinned core integration. Proofmill Standard adds the pinned release. All arms
use the same Codex executable, model, reasoning effort, sandbox, prompt, starting
Git repository, and time boundary.

## Plan of Work

First, make the neutral brief callable without teaching hidden scenarios. Freeze
the Python module, method signatures, value conventions, required results, and
error contract. Record its checksum before any arm runs.

Second, write a standard-library `unittest` suite that imports an arm's
`checkbook.py` by path. Cover every public requirement and the already frozen
fault scenarios. Add controller self-tests using deliberately good and broken
fixtures. The controller copies only the brief and arm instruction files into a
fresh Git repository, invokes Codex, runs the hidden suite externally, collects
Git and JSONL metrics, and preserves immutable summaries.

Third, define the five arms with the smallest real distinction. Copy exact
Ponytail and Cavekit skill bytes where required. Install pinned Spec Kit core for
its arm. Install the PM-031 local release for Proofmill Standard. Do not add
synthetic descriptions of tools that an arm does not actually receive.

Finally, audit all generated arm inputs before execution. Run each arm once in a
recorded order. Do not repair first-pass output. Execute the external suite,
measure files, lines, dependencies, tokens, tools, time, findings, and accepted
capabilities, then publish the comparison and its limitations.

## Milestones

The freeze milestone ends when the public brief has a checksum and sufficient
interface detail for an external suite. The controller milestone ends when good
and broken fixtures prove that hidden checks detect real defects. The arm
milestone ends when five dry-created repositories differ only by their declared
instruction treatment. The result milestone ends when all five first-pass
summaries are comparable and preserved.

## Concrete Steps

Work from `/home/mbeutler/Projects/proofmill`. Use `apply_patch` for tracked
files. Use `/tmp` and `.agent/benchmark-runs/` only for disposable runs and
large logs. Record exact commands and rerun evidence in
`.agent/test-results/checkbook-benchmark.md`.

Invoke every implementation arm with this fixed runner envelope:

    codex exec --ephemeral --ignore-user-config --ignore-rules \
      --skip-git-repo-check -s workspace-write -m gpt-5.4 \
      -c 'model_reasoning_effort="medium"' --json

The controller must use the current absolute `codex` executable and record its
`codex --version` output. It must never pass the hidden-suite path to an arm.

## Validation and Acceptance

PM-011 passes when the brief and experiment lint and the brief checksum is
recorded. PM-012 passes when controller self-tests prove good behavior passes
and representative bad behavior fails. PM-013 through PM-017 pass when dry-run
input manifests show byte-identical briefs and only the declared arm additions.
PM-018 passes when metrics serialize deterministically and distinguish missing
values from zero. PM-019 passes when every arm has one preserved first-pass
summary and the comparison audits parity before ranking results.

Run Python unit tests, Ruff only if already available without adding a project
dependency, ShellCheck only for shell files, Markdown lint for authored prose,
YAML or JSON parsing for manifests, and `git diff --check`. The user waived
adversarial review for benchmark code. All tests and lint still must pass before
an arm runs.

## Idempotence and Recovery

Every arm uses a new run directory and immutable run identifier. If Codex or a
test command fails, preserve that failure and continue to the next arm. Never
reuse a partially generated repository. A controller self-test can delete only
its exact temporary directory. Published result files are append-only by run ID;
a corrected controller requires a new benchmark batch.

## Artifacts and Notes

Keep the frozen public brief, experiment protocol, arm manifests, controller,
hidden suite, and compact results in `conformance/checkbook/`. Keep raw Codex
JSONL, full test logs, and generated repositories untracked under
`.agent/benchmark-runs/`.

## Interfaces and Dependencies

Use only Python 3 standard-library modules such as `argparse`, `csv`, `hashlib`,
`importlib`, `json`, `pathlib`, `sqlite3`, `statistics`, `subprocess`, `tempfile`,
`time`, and `unittest`. Use Git and the pinned external CLIs already qualified by
Proofmill. Add no Python package or persistent service.

Latest revision: 2026-08-12. PM-019 is complete. Stop at the approved first
comparable result boundary.
