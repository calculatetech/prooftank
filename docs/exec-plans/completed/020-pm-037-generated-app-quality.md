# Measure generated-app quality

<!-- markdownlint-disable MD013 MD046 -->

This ExecPlan is a living document. Maintain it according to
`.agent/PLANS.md` and keep `docs/roadmap.md` current.

## Purpose / Big Picture

The benchmark must show where generated applications need attention, not reward
small output or cheap execution. A reader must be able to compare the five
unchanged checkbook applications by defects found during clean-context code
review, production-readiness audit, security audit, and an overall engineering
assessment. Lines, tokens, time, and test counts remain context only.

If the checkbook application gives every arm the same quality result, this task
must design and run a replacement benchmark with enough real operational and
security surface to expose differences. It must not invent a winner from weak
evidence.

## Bounded Work Packet

    profile: critical
    must_do:
      - preserve the five first-comparable checkbook repositories unchanged
      - review the existing benchmark setup as ProofTank-owned code
      - blind each generated application behind a neutral candidate label
      - use one fixed audit rubric and two fresh clean-context reviewers per candidate
      - count evidence-backed findings by severity and audit lens
      - record production blockers and an overall engineering assessment
      - assess single outcome ownership and readability from code alone
      - assess cohesion, change locality, invariant visibility, and complexity
      - treat tests, lines, tokens, tools, and time as descriptive context only
      - challenge setup-review findings for simplicity and relevance
      - replace checkbook when its audited outputs do not produce useful direction
    must_not_do:
      - repair a generated application before measuring it
      - reveal arm identity or another candidate's results to an app reviewer
      - convert reviewer opinion into deterministic proof
      - reward more files, tests, process, tokens, or lines by themselves
      - add another harness, ProofTank runtime, service, database, or dashboard
      - perform PM-036 during this task
    may_do:
      - run application tests and read Git history inside a frozen candidate
      - preserve compact review evidence and anonymized mappings
      - run a replacement Codex-only benchmark after its setup passes review
    stop_when:
      - evidence identifies the strongest and weakest generated-app qualities
      - the result gives a defensible direction for ProofTank's next investment

## Progress

- [x] (2026-08-12) Activated PM-037 and preserved the original quality conclusion as superseded.
- [x] (2026-08-12) Reviewed the setup for three clean-context adversarial cycles; all challenged findings were simple and relevant, and the third-cycle fixes are the review cap.
- [x] (2026-08-12) Froze the blind app-audit rubric, ten perceived-quality dimensions, two-review rule, sanitized snapshots, and anonymized mapping hash.
- [x] (2026-08-12) Audited all five unchanged applications with ten fresh blind reviewers.
- [x] (2026-08-12) Found checkbook discriminating on outcome ownership and invariant failures; no replacement was needed.
- [x] (2026-08-12) Published the direction, immutable reports, unblinding evidence, and validated comparison.

## Surprises & Discoveries

- Observation: The original experiment listed review findings as a metric but
  published none.
  Evidence: `conformance/checkbook/EXPERIMENT.md` names review findings, while
  `results/first-comparable-001/summary.json` contains only execution and size
  measures.
- Observation: All five unchanged generated repositories remain available.
  Evidence: `.agent/benchmark-runs/first-comparable-001/repositories/` contains
  each arm's generated application and Git history.
- Observation: Setup review cycle 1 found seven simple and relevant benchmark
  integrity gaps.
  Evidence: Outputs lacked hashes, candidate contents leaked treatment, one
  reviewer confounded strictness, generated code ran on the host, the quality
  schema was incomplete, comparability checks were weak, and test counts were
  mislabeled as capabilities and defects.
- Observation: Passing the same 15 scenarios concealed material design risk.
  Evidence: Every arm passed, but paired reviews replicated concurrency,
  closure, reversal, storage-failure, numeric, and input-boundary findings.
- Observation: Readability and accidental complexity did not separate the arms.
  Evidence: All ten reviewers scored both dimensions 4/5.

## Decision Log

- Decision: Reuse frozen outputs before spending on new model runs.
  Rationale: A blind audit can test whether checkbook already contains useful
  quality differences without changing an input or implementation.
  Date/Author: 2026-08-12 / Codex.
- Decision: Separate product-code review from benchmark app auditing.
  Rationale: ProofTank setup changes use the repository's repeat-until-clean or
  three-cycle adversarial rule. Frozen app outputs use two fixed independent
  audits per candidate because findings are measurements and no repair occurs.
  Date/Author: 2026-08-12 / Codex.
- Decision: Use two independent reviews per candidate.
  Rationale: A single different reviewer per candidate cannot distinguish arm
  quality from reviewer strictness. Differences without replicated support stay
  exploratory or require blind adjudication.
  Date/Author: 2026-08-12 / Codex.
- Decision: Exclude generated process documents from the blind review view.
  Rationale: The audit measures the delivered runtime and tests, while planning
  files name treatments and would bias perceived-quality scores.
  Date/Author: 2026-08-12 / Codex.
- Decision: Keep checkbook and do not run a replacement benchmark.
  Rationale: The paired reviews exposed meaningful differences and a specific
  product direction. A new application would add cost without changing that
  immediate decision.
  Date/Author: 2026-08-12 / Codex.
- Decision: Prioritize deterministic single-outcome checks over more guidance.
  Rationale: Spec Kit core made transition ownership clearest, while Proofmill
  standard did not preserve it. All arms were already readable and simple.
  Date/Author: 2026-08-12 / Codex.

## Outcomes & Retrospective

PM-037 is complete. Ten blind audits showed that code can be readable and pass
the same scenarios while still hiding production-blocking transition failures.
Spec Kit core was strongest on single-outcome ownership, but no arm was
production-ready. Proofmill standard did not beat core or preserve its ownership
advantage. The smallest supported next investment is deterministic checks for
concurrency, closure, reversal, storage errors, numeric limits, and bounded
imports. No replacement benchmark or ProofTank runtime was needed.

## Context and Orientation

`conformance/checkbook/` owns the public brief, experiment, arm definitions,
controller, hidden suite, and compact first result. The complete generated
repositories and raw logs are ignored local evidence under
`.agent/benchmark-runs/first-comparable-001/`. The five arm identities are
`bare`, `ponytail`, `cavekit-ponytail`, `spec-kit-core`, and
`proofmill-standard`.

A finding is one distinct, actionable defect or readiness gap supported by a
file, line, command, or observable behavior. Severity is `critical`, `high`,
`medium`, or `low`. Audit lens is `correctness`, `production`, `security`, or
`maintainability`. Duplicate symptoms with one root cause count once. Missing
features already required by the brief count as correctness findings; optional
polish does not.

Single outcome ownership means one clear code path owns each business state
transition and its result. A reviewer must be able to locate where a transaction,
import, reconciliation, close, reversal, or audit outcome becomes authoritative
without reconciling competing implementations or duplicated rules. Code-alone
readability means names, structure, and local control flow explain the design
without requiring generated planning documents to decode ordinary behavior.

## Plan of Work

First, send the current benchmark setup to fresh clean-context adversarial
review. Apply only findings that are both simple and relevant. Repeat with a new
reviewer until no further finding or the third cycle. This review covers the
controller, hidden suite, experiment controls, arms, and result-production path.

Next, freeze one concise audit prompt and machine-readable result shape. Create
five neutral candidate directories from files produced after each arm's input
commit. Give every reviewer the same product brief, audit prompt, candidate
files, model class, and tool access. Do not expose treatment names, raw model
logs, efficiency results, or other reviews. Use one new clean-context subagent
per report, two reports per candidate, and run only one at a time.

Each reviewer must run available tests, inspect the full application, and report
distinct findings with severity, lens, evidence, impact, and smallest credible
remediation. It must also state production blockers, security posture, strongest
quality, weakest quality, and a five-point overall readiness score with concise
rationale. A reviewer may report zero findings only after explicitly checking
correctness, failure atomicity, concurrency, durability, input boundaries,
secrets, injection, denial of service, observability, packaging, operations, and
maintainability.

The overall engineering assessment must also score these anchored dimensions
from one to five: single outcome ownership, code-alone readability, cohesion,
change locality, invariant visibility, error-model clarity, accidental
complexity, test confidence, operational clarity, and willingness to own the
application in production. A score of one means the reviewer cannot establish
the quality or sees a blocking design problem; three means workable with clear
gaps; five means clear, deliberate, and production-credible. Each score needs
one evidence sentence. Test count, line count, and documentation volume must not
raise a score by themselves.

Aggregate counts without treating the readiness score as precise measurement.
Unblind only after all five reports are frozen. Compare critical and high
findings first, then production blockers, security findings, total distinct
findings, and qualitative strengths. Efficiency metrics are tie-breaking context
only when quality is materially equivalent.

The final comparison must answer which application makes business outcomes
easiest to trace, which can be understood with the least external explanation,
which localizes likely changes, which hides invariants or duplicates ownership,
and which a maintainer would most readily take on call. These perceived-quality
judgments remain advisory, but they are central benchmark evidence.

If reviewer findings are uniformly empty, trivial, or dominated by limitations
of the task rather than implementation choices, record checkbook as
non-discriminating. Then freeze a replacement product brief with meaningful
deployment, trust-boundary, concurrency, recovery, and maintenance decisions;
review its setup before execution; run the same five Codex arms; and apply the
same blind audit protocol.

## Milestones

The setup-review milestone ends when the benchmark-owned executable path has no
unchallenged finding or reaches its third clean review cycle. The blind-audit
milestone ends when five immutable reports use the same rubric and the mapping
is revealed. The direction milestone ends when the evidence either identifies a
quality pattern or proves that a replacement task is necessary and completes
that replacement comparison.

## Concrete Steps

Work from `/home/mbeutler/Projects/proofmill`. Use `apply_patch` for tracked
edits. Keep generated candidate directories and raw reviewer material under
`.agent/benchmark-runs/`. Preserve compact final evidence under
`conformance/checkbook/results/`.

Run Python unit tests, Ruff check and format check, Python compileall, authored
Markdown lint, YAML and JSON parsing, release checksums when touched, local-link
checks, and `git diff --check`. Record detailed results in
`.agent/test-results/pm-037.md`.

## Validation and Acceptance

The setup must preserve input parity and prove that candidate directories contain
only generated outputs plus the common brief. Every review report must match the
frozen result shape and cite evidence that resolves within its candidate. The
mapping must remain outside reviewer context until all reports finish. The final
report must not rank arms by tests, lines, tokens, tools, or elapsed time.

Every report must include the ten anchored perceived-quality dimensions and
evidence. It must distinguish code that is genuinely self-explanatory from code
whose generated documents merely compensate for complexity.

A useful result names recurring defect classes, shows which arms avoid them,
states uncertainty from two reviewers and one generation per arm, and recommends
the smallest next ProofTank change supported by those findings. If it cannot do
that, acceptance requires a completed replacement benchmark rather than a vague
request for more research.

## Idempotence and Recovery

Candidate preparation may replace only its exact ignored PM-037 directory.
Review reports are immutable after unblinding. A failed reviewer attempt remains
recorded and uses a fresh subagent for retry. Generated apps never receive fixes.

## Artifacts and Notes

The frozen rubric, anonymized mapping hash, compact reports, and final analysis
belong under `conformance/checkbook/results/quality-review-001/` if checkbook is
useful. A replacement benchmark receives its own directory and run identifier.

## Interfaces and Dependencies

Use Python's standard library and existing repository tools. Add no package,
service, protocol, database, or runtime. Reviewer reports use JSON only if a
small parser is needed; Markdown is sufficient when a deterministic validation
script can check the required headings and evidence paths.

Latest revision: 2026-08-12. PM-037 is complete; paired blind audits made
single-outcome ownership the next deterministic quality target.
