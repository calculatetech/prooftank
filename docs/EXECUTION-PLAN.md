# Execution plan

This file describes the version 0 delivery stages. `docs/roadmap.md` owns task
status and order.

## Milestone 0 — Repository constitution

Deliver:

- starter documents;
- decision log;
- product policy;
- active bootstrap plan;
- upstream registry;
- checkbook benchmark brief.

Exit criteria:

- A new Codex session can identify the product boundary without conversation history.
- No document instructs Codex to build a new runtime.

## Milestone 1 — Current upstream audit

Deliver:

- reviewed current Spec Kit architecture and extension API;
- qualification records for Ponytail and SimpleEnglish;
- blocked qualification records for CBM, Cavemem, NeuroArxiv, and ADHD;
- comparison-only Cavekit and advisory best-of-Agent-Harnesses records;
- postponed non-Codex harness work;
- exact pins and license records.

Exit criteria:

- Every selected component has a health, failure, disable, uninstall, and fallback plan.
- No unreviewed community extension is enabled by default.

## Milestone 2 — ProofTank Standard composition

Deliver:

- current-valid Spec Kit preset;
- standard workflow;
- installable bundle or catalog entry;
- ProofTank contract template;
- bounded work-packet template;
- deterministic artifact-consistency checks using existing extensions where possible.

Exit criteria:

- The composition installs in Codex.
- One example feature reaches a completed and analyzed state.
- Required and optional provider failures are distinguishable.

## Milestone 3 — Post-MVP cross-harness conformance

This milestone is postponed. Codex is the only supported MVP harness.

Deliver:

- Codex runner;
- Claude Code runner or manual protocol;
- OpenCode runner or manual protocol;
- Pi automated runner through print/JSON or RPC mode;
- normalized conformance report.

Post-MVP exit criteria:

- Stable contract IDs and task scope are equivalent across required harnesses.
- No harness becomes a hidden source of project truth.

## Milestone 4 — Checkbook benchmark

Deliver:

- neutral product brief;
- bare-agent control;
- Ponytail-only arm;
- Cavekit-plus-Ponytail comparison arm;
- Spec Kit core arm;
- historical Proofmill Standard arm, ProofTank's predecessor;
- hidden acceptance and fault suite;
- token, tool, time, LOC, dependency, defect, rework, and diagnosis measurements.

Exit criteria:

- Runs are reproducible from clean repositories.
- Failed and negative runs are preserved.
- Requirement parity is audited.

## Milestone 5 — Critical profile spike

This milestone is postponed. The bootstrap prohibits a critical-profile
workflow, and the reviewed research and divergence providers cannot run under
current MVP rules.

Deliver:

- a harder checkbook change involving offline concurrent edits, crash recovery, or atomic transfer;
- NeuroArxiv research phase;
- ADHD or equivalent isolated design review;
- stronger verification selected for the failure model;
- V-Model or equivalent traceability evaluation.

Exit criteria:

- The critical workflow catches failures that standard does not.
- Its additional cost is measured.

## Milestone 6 — Gap-based implementation

Compare existing Spec Kit core and approved extensions against the remaining needs.

Possible gaps:

- provider qualification validator;
- cross-harness result normalizer;
- release warrant that preserves unknown and degraded states;
- provider-health summary.

Build only the smallest gap that survives the comparison.

PM-027 and PM-028 found no release-warrant or provider-health gap. No custom
runtime code is authorized by the MVP evidence.

Exit criteria:

- Every new ProofTank code module has a written rejected-upstream analysis.
- The custom implementation is smaller and safer than the alternatives.

## Milestone 7 — Public pilot

Deliver:

- pinned bundle catalog;
- installation guide;
- qualification reports;
- checkbook results;
- limitations;
- contribution and provider-replacement guide.

Exit criteria:

- A new user can install, run, and uninstall the standard profile.
- The user can replace or disable optional providers without losing project artifacts.
