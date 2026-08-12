# Frozen checkbook experiment

## Claim under test

Proofmill Standard can spend more effort before implementation and still reduce
total lifecycle cost. It wins only when it improves accepted behavior, rework,
diagnosis, or scope control enough to justify that effort.

## Frozen runner

- Runtime: Codex only.
- Codex CLI: `0.147.0`.
- Model: `gpt-5.4`.
- Reasoning effort: `medium`.
- Sandbox: `workspace-write`.
- User configuration and repository rules: ignored.
- Implementation language: Python 3.12 or newer.
- Runtime dependencies: Python standard library and SQLite only.
- Replicates for the first comparison: one complete first-pass run per arm.

Frozen input SHA-256 values:

- `PRODUCT-BRIEF.md`:
  `6588b63ee0996ed3141cd41b0640f0ce6ff7ff58dec7e271d2d28c10ae4956e5`.
- Common implementation prompt:
  `01cd99dcbd35a2391193fe0409929d86b65d173ecec1354074c285d29aa8875a`.

The controller records the exact executable, Python version, operating system,
start revision, prompt checksum, brief checksum, arm input checksums, event log,
and elapsed time.

## Arms

### A. Bare agent

Codex plus ordinary repository tools and the frozen brief.

### B. Ponytail only

The bare arm plus the exact approved Ponytail skill.

### C. Cavekit plus Ponytail

The bare arm plus exact Cavekit `4.1.0` comparison skills and exact Ponytail.
Cavekit owns its arm's `SPEC.md` only. It is not a Proofmill provider or a second
owner in another arm.

### D. Spec Kit core

The bare arm plus pinned GitHub Spec Kit core. It receives no Proofmill preset,
workflow, or provider skill.

### E. Proofmill Standard

The bare arm plus the pinned Proofmill Standard `0.1.0` local release.

Proofmill Critical is outside this experiment.

## Common implementation prompt

Every arm receives this exact prompt after its declared tools are installed:

```text
Read PRODUCT-BRIEF.md. Implement the complete product in this repository. Use
only the files, skills, and process installed in this arm. Add and run focused
tests. Do not ask questions. Do not read outside this repository. Stop when the
brief is implemented and repository checks pass.
```

## Controls

- Copy the identical frozen brief and prompt into every arm.
- Start every arm from the same empty Git repository shape.
- Use the same CLI, model, effort, sandbox, timeout, and environment policy.
- Install only the treatment named by the arm.
- Keep the hidden suite outside every arm repository.
- Do not tell an arm hidden scenario names or test paths.
- Preserve failures, timeouts, partial output, and negative results.
- Do not repair an arm before recording its first-pass result.
- Audit input parity before ranking results.
- Do not move thresholds after the first arm starts.

## Hidden scenarios

The external suite covers every frozen public requirement and these fault
classes:

- debit and credit sign behavior.
- integer-only money.
- identical and conflicting duplicate imports.
- malformed middle CSV rows and atomic abort.
- retry after abort.
- closed-period mutation.
- reconciled history and duplicate reversal.
- stale concurrent edits.
- real calendar dates at year and leap-day boundaries.
- reconciliation mismatch after correction.
- missing audit events.
- missing operation identifiers.
- restart after committed and aborted imports.

## Comparable result

A batch is comparable only when all five arms have:

- the same brief and prompt checksums.
- the frozen runner settings.
- an input manifest that differs only by declared treatment.
- a preserved terminal state, including timeout or failure.
- an external hidden-suite result.
- the same metric schema.

The first comparison can rank accepted capabilities and hidden scenarios passed.
It must label one-run variance, unavailable token or cost fields, and controller
limitations. It cannot claim general model superiority or statistical
significance.

## Metrics

Record:

- input, output, and cached tokens when Codex reports them.
- tool calls and wall time.
- generated source, test, specification, and total lines.
- files and external dependencies.
- public requirements and hidden scenarios passed.
- severe defects and failure diagnostics.
- process artifacts and review findings.
- repair cycles, regressions, diagnosis time, and human time when measured.
- unrequested files, services, dependencies, abstractions, and configuration.

Use `unknown`, not zero, for an unavailable measurement.

## Main economic metrics

The original economic ranking is superseded. Passing scenarios, tool calls,
wall time, tokens, source lines, test lines, and scope additions are descriptive
context. They are not success measures and cannot establish a quality winner.

## Generated application quality review

Success is measured primarily through clean-context review of frozen generated
applications. Every candidate receives two independent blind audits using
`QUALITY-AUDIT.md`. Reviewers see only the common brief, runtime source, and
repository tests. They do not see arm identity, treatment inputs, Git history,
process documents, model logs, efficiency results, or another review.

Generated Python runs only through `sandbox.py`, which removes network access,
credentials, and host filesystem visibility. Each candidate snapshot and review
report is content-addressed and validated before comparison.

Compare critical and high findings, production blockers, security findings,
replicated defect classes, single outcome ownership, code-alone readability,
cohesion, change locality, invariant visibility, error-model clarity, accidental
complexity, test confidence, operational clarity, and willingness to take
production ownership. Use efficiency only as context when quality is materially
equivalent.

Publish cases where another arm beats Proofmill. A no-winner result is valid.
