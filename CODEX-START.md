# Completed Codex bootstrap prompt

This prompt is a historical bootstrap record. Do not execute it again. The
completed plan is `docs/exec-plans/completed/000-bootstrap.md`. Current work and
progress are in `docs/roadmap.md`.

Proofmill is an audited assurance distribution for agent-built software. GitHub Spec Kit is the process substrate. Codex is the first runtime target.

Read these files before you change anything:

1. `AGENTS.md`
2. `docs/PRODUCT-CHARTER.md`
3. `docs/DECISIONS.md`
4. `docs/ARCHITECTURE.md`
5. `docs/HARNESS-ENGINEERING.md`
6. `docs/BUILD-VS-INTEGRATE.md`
7. `docs/UPSTREAM-QUALIFICATION.md`
8. `docs/exec-plans/completed/000-bootstrap.md`

The bootstrap plan is complete.

## Objective

Create the smallest current-valid `proofmill-standard` Spec Kit composition. Prove one Codex dry run. Then stop.

## Required first action

Inspect the current upstream primary sources. Do not implement against assumptions in this starter kit.

Start with:

- `github/spec-kit`;
- `DietrichGebert/ponytail`;
- `AminBlg/SimpleEnglish`.

Inspect current Spec Kit core and extension candidates for traceability, verification, architecture rules, quality gates, and evidence.

Do not audit every optional provider during this milestone. Their reviews remain in the backlog.

For each active component, record:

- exact commit or release;
- license;
- capability;
- installation method;
- files and configuration that it writes;
- hooks and commands that it registers;
- network access;
- health check;
- disable and uninstall path;
- failure behavior;
- fallback;
- trust class.

Write reviews under `upstream/reviews/` and update `upstream/registry.yml`.

## Working method

- Keep the bounded work packet in the active execution plan.
- Use current project-native validation tools.
- Use SimpleEnglish for technical instructions.
- Apply Ponytail to every implementation choice.
- Keep repository knowledge in versioned files.
- Keep `AGENTS.md` as a map, not an encyclopedia.
- Preserve rejected components and negative findings.
- Do not claim that provider output is proof without deterministic support.

## Prohibited work

Do not create:

- a daemon;
- a database;
- an MCP aggregator;
- a new agent loop;
- a code graph;
- a memory system;
- a generic adapter protocol;
- a checkbook implementation;
- a cross-harness test matrix;
- a critical-profile workflow.

## Definition of done

- Current Spec Kit composition formats are documented and validated.
- Spec Kit, Ponytail, and SimpleEnglish have exact pins and qualification records.
- A current-valid Proofmill contract preset exists.
- A current-valid standard workflow exists.
- A current-valid local bundle or catalog composition exists.
- The composition installs or validates through Codex.
- One minimal dry run produces the required repository artifacts.
- Missing optional providers remain visible and safe.
- The gap report recommends proceed, revise, or stop.
- No unnecessary Proofmill runtime exists.

Do not start the checkbook benchmark without approval.
