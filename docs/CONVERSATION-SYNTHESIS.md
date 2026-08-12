# Conversation synthesis

## Starting problem

Meridian exposed a recurring failure pattern in agent-built software:

1. The model produced functional code quickly.
2. Review found behavioral relationships that the implementation had missed.
3. Fixing one issue exposed or created related defects.
4. Structural code graphs showed callers and dependencies, but not the full behavioral contract.
5. A highly capable model added too much code and too many abstractions.
6. A minimal model or skill wrote less code but could miss edge cases.

The original idea was a behavioral-contract layer above Codebase Memory MCP.

## First direction: contract-aware impact graph

The proposed layer modeled:

- Authoritative and projected state.
- Owners and prohibited secondary owners.
- State transitions.
- Failure, retry, cancellation, restart, and concurrency behavior.
- Boundary crossings.
- Exact tests that prove each behavior.

This remained valuable, but it risked becoming a large second graph that reconstructed meaning after implementation.

## Second direction: behavior compiler

The design moved upstream:

```text
reviewed behavior contract
        ↓
implementation constraints
        ↓
tests, traces, models, and proofs
        ↓
structural graph audits for bypass and drift
```

This made the contract active rather than descriptive. It also suggested a software-factory control plane called Proofmill.

## Third direction: integrate before build

The ecosystem review found that many parts already exist:

- Ponytail controls implementation bloat.
- SimpleEnglish reduces instruction ambiguity.
- NeuroArxiv checks prior art.
- ADHD explores competing designs and traps.
- Cavekit demonstrates compact specs, invariants, drift checks, and bug backpropagation.
- Cavemem supplies local cross-agent memory.
- CBM supplies structural code intelligence.

Proofmill did not need to rebuild these capabilities.

## Final pivot: Spec Kit distribution

OpenAI's harness-engineering account reinforced that reliable agent development depends on:

- Repository knowledge as the system of record.
- A short `AGENTS.md` that maps to deeper documentation.
- First-class execution plans and decision history.
- Agent-legible build, test, UI, logs, metrics, and traces.
- Mechanical architecture and quality rules.
- Continuous backpropagation of failures into the repository harness.

GitHub Spec Kit supplies the missing process and packaging substrate:

- Constitution.
- Specification.
- Plan.
- Tasks.
- Analysis and convergence.
- Presets, extensions, workflows, catalogs, and bundles.
- Broad agent-harness integration.

The locked product definition became:

> Proofmill is an audited, risk-graded Spec Kit distribution for reliable agent-built software.

## Novel work that remains

Proofmill must provide value through curation and assurance, not a new runtime:

1. Qualified, pinned, replaceable upstream components.
2. Risk-graded profiles.
3. A contract template that defines behavioral floor and implementation ceiling.
4. Cross-harness conformance.
5. Deterministic distinction between passed, failed, stale, degraded, and unknown.
6. A release evidence format only where existing extensions leave a proven gap.
7. A scientific benchmark that measures lifecycle value, not only first-pass tokens.

## Core philosophy

LLMs are good at producing functional output.

Proofmill must help them produce useful output:

- Grounded in existing knowledge.
- Complete enough to cover important edge cases.
- Small enough to avoid speculative architecture.
- Legible to future agents.
- Diagnosable when it fails.
- Supported by evidence that belongs to the current source revision.
