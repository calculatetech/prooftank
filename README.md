# Proofmill Codex MVP

<!-- markdownlint-disable MD013 MD060 -->

> **Naming transition:** The project owner accepted **ProofTank** as the working
> name for this open-source hobby project. The canonical repository is
> [`calculatetech/prooftank`](https://github.com/calculatetech/prooftank).
> `PM-036` will migrate the existing `Proofmill` names and identifiers. Until
> that task passes validation, release `0.1.0` keeps its current exact names and
> hashes.

**Proofmill** is an audited assurance distribution for agent-built software.

> Ideas enter. A bounded, reviewed work contract guides the agent. Repository evidence determines whether the result is ready.

The supported MVP runs only on Codex. Other harnesses and the critical profile
are postponed.

The first comparable benchmark found no accepted-behavior gain from Proofmill
Standard. The current claim is narrower: the exact composition installs,
preserves a bounded contract and explicit unknowns, and adds no Proofmill
runtime.

## The product in one diagram

```text
Codex
                         │
                         ▼
GitHub Spec Kit process substrate
constitution → specification → plan → tasks → implementation → analysis
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
   Ponytail + SimpleEnglish   project-native tests + lint
             │                       │
             └───────────┬───────────┘
                         │
                         ▼
              Proofmill assurance profile
       scope boundary · evidence states · explicit unknowns
```

## Locked direction

Proofmill version 0 is **not** a new agent runtime, MCP server, memory system, code graph, or software-development framework.

Proofmill version 0 is:

1. A curated and pinned **GitHub Spec Kit distribution**.
2. One working **standard** workflow for Codex; lite is design-only and critical
   is postponed.
3. A closed MVP provider set with visible rejected candidates.
4. A contract format that sets an implementation floor and ceiling.
5. Codex conformance; cross-harness work is postponed.
6. A checkbook application benchmark.
7. Native release checks and explicit unknowns, with no release warrant.

## Default component map

| Capability | Default | Status |
|---|---|---|
| Process substrate | `github/spec-kit` | required |
| Minimal implementation | `DietrichGebert/ponytail` | required |
| Controlled technical language | `AminBlg/SimpleEnglish` | required |
| Native tests and lint | project tools | required evidence |
| Structural code intelligence | native search; CBM blocked | fallback only |
| Prior-art research | manual primary sources; NeuroArxiv blocked | fallback only |
| Divergent review | fresh Codex review; ADHD blocked | fallback only |
| Cross-session memory | repository docs and Git; Cavemem blocked | fallback only |
| Spec-design reference | Cavekit | comparison only |
| Ecosystem sustainability feed | pinned best-of-Agent-Harnesses JSON | manual input |
| Other harnesses | Claude, OpenCode, Pi, OpenHarness | postponed |

Every upstream component must be reviewed, pinned, licensed, tested, and replaceable.

## Continue with Codex

For a local evaluation, follow the
[`0.1.0` Codex public-pilot guide](docs/PUBLIC-PILOT.md).

1. Open Codex in this repository.
2. Read [`AGENTS.md`](AGENTS.md) and [`docs/roadmap.md`](docs/roadmap.md).
3. Select work in roadmap order.
4. For complex work, create an execution plan before implementation.
5. Move the selected task to **Active** in the same change that starts it.

Do not build a Proofmill runtime. The approved first checkbook batch is complete;
do not add or rerun benchmark arms without a new roadmap task.

## Repository map

- [`AGENTS.md`](AGENTS.md): concise operating map for all agents.
- [`CODEX-START.md`](CODEX-START.md): historical prompt for the completed
  bootstrap session.
- [`proofmill.yml`](proofmill.yml): product policy and capability map.
- [`upstream/registry.yml`](upstream/registry.yml): qualification queue for upstream projects.
- [`docs/CONVERSATION-SYNTHESIS.md`](docs/CONVERSATION-SYNTHESIS.md): how the idea evolved and why.
- [`docs/DECISIONS.md`](docs/DECISIONS.md): locked architectural decisions.
- [`docs/EXECUTION-PLAN.md`](docs/EXECUTION-PLAN.md): staged delivery manual.
- [`docs/roadmap.md`](docs/roadmap.md): product work, order, and current progress.
- [`docs/NAME-CLEARANCE.md`](docs/NAME-CLEARANCE.md): working-name decision and
  preliminary collision research.
- [`docs/PUBLIC-PILOT.md`](docs/PUBLIC-PILOT.md): bounded local Codex pilot
  instructions and evidence.
- [`docs/HARNESS-ENGINEERING.md`](docs/HARNESS-ENGINEERING.md): repository-centered harness principles.
- [`docs/SPEC-KIT-COMPOSITION.md`](docs/SPEC-KIT-COMPOSITION.md): current preset, workflow, bundle, and catalog formats.
- [`docs/BOOTSTRAP-GAP-REPORT.md`](docs/BOOTSTRAP-GAP-REPORT.md): bootstrap evidence, gaps, and recommendation.
- [`skills/proofmill/SKILL.md`](skills/proofmill/SKILL.md): draft portable risk router.
- [`conformance/checkbook/`](conformance/checkbook/): A/B and ablation benchmark.

## Version 0 success condition

The MVP has demonstrated that `proofmill-standard` can:

- Install cleanly for Codex from exact local artifacts.
- Produce a current-valid specification and checklist.
- Build the checkbook application without speculative architecture.
- Report missing or stale evidence as unknown, not as success.
- Disable or uninstall required skills without losing project truth.

It has not demonstrated a quality advantage over bare Codex, Ponytail, Cavekit
plus Ponytail, or Spec Kit core. That product claim remains unsupported.

## Non-goals

Version 0 does not build:

- An agent loop.
- A hosted service.
- A dashboard.
- A daemon.
- A general MCP aggregator.
- A new code graph.
- A memory database.
- A replacement for Spec Kit.
- Formal verification for arbitrary code.
- Automatic approval of agent-written contracts or waivers.

The repository must remain small until the benchmark proves that a missing capability requires code.
