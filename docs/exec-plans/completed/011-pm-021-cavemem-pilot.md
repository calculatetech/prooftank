# Pilot Cavemem as advisory memory

<!-- markdownlint-disable MD013 MD046 -->

This completed ExecPlan follows `.agent/PLANS.md`. It records why the planned
truth-boundary check stopped before executing Cavemem.

## Purpose / Big Picture

This task determined whether current Cavemem could supply optional Codex context
without changing repository truth. Cavemem's useful behavior is a persistent
SQLite memory system with capture hooks and a background worker, which is
outside the MVP boundary. Its current published release also writes an obsolete
Codex configuration shape. The candidate was blocked.

## Bounded Work Packet

    profile: standard
    must_do:
      - inspect the current primary repository and exact release identity
      - record license, installation, files, commands, network, health, failure, fallback, and trust
      - preserve repository docs and Git as the fallback
      - stop before creating prohibited memory state
    must_not_do:
      - add Cavemem to a bundle, workflow, release, or default Codex configuration
      - let retrieved text change a specification, evidence state, or pass state
      - create a memory system, daemon, database, MCP aggregator, or adapter
      - modify user-level MCP or Codex configuration
    stop_when:
      - the registry and review reflect the product-boundary result

## Progress

- [x] (2026-08-12 01:14Z) Activated PM-021 after closing the CBM pilot.
- [x] (2026-08-12 01:20Z) Inspected current main and pinned published release `v0.2.1`.
- [x] (2026-08-12 01:24Z) Stopped before execution because useful retrieval requires prohibited persistent memory state.
- [x] (2026-08-12 01:24Z) Recorded the blocked qualification and repository fallback.

## Surprises & Discoveries

- Observation: the published Codex installer is not current-valid.
  Evidence: release `0.2.1` writes `~/.codex/config.json`; current unpublished
  main changes this to `config.toml` and adds `hooks.json` capture hooks.
- Observation: “no network” has a narrower practical meaning than the headline.
  Evidence: npm must download the package, the default Transformers.js model
  can require a first-use download, and remote embedding providers are optional.

## Decision Log

- Decision: Keep all provider state and configuration outside Proofmill.
  Rationale: Advisory memory cannot own durable project truth.
  Date/Author: 2026-08-12 / Codex.
- Decision: Stop before installing or writing a retrieval fixture.
  Rationale: The check would create the forbidden memory system to demonstrate
  that the memory system is advisory. Source inspection already proves the
  architectural mismatch, and the published Codex installer is unusable.
  Date/Author: 2026-08-12 / Codex.

## Outcomes & Retrospective

PM-021 is complete with a negative result. Cavemem `v0.2.1` is pinned for the
record and blocked for the MVP. No package, SQLite database, model, worker,
hook, MCP entry, or user configuration was created. Versioned repository docs
and Git remain the fallback.

## Context and Orientation

`upstream/reviews/cavemem.md` is the durable qualification record.
`upstream/registry.yml` keeps the exact release and blocked state visible.
`.agent/test-results/pm-021.md` contains bounded command evidence and stays
untracked.

## Plan of Work

The completed work resolved the official current source, published release,
npm identity, license, runtime, Codex installer, commands, hooks, written files,
network behavior, health checks, disable path, uninstall path, and failures. It
applied the product boundary before package execution.

## Concrete Steps

Work ran from `/home/mbeutler/Projects/proofmill`. A detached checkout under
`/tmp` was compared with the current remote head, GitHub release record, and npm
package metadata. No install command or package code ran.

## Validation and Acceptance

Acceptance requires the registry and review to parse, Markdown lint to pass,
Cavemem to remain absent from Proofmill compositions, and repository docs and
Git to remain available without it.

## Idempotence and Recovery

Source inspection is repeatable and read-only. The detached checkout can be
discarded. There is no provider state to stop or uninstall.

## Artifacts and Notes

Durable conclusions are in `upstream/reviews/cavemem.md` and
`upstream/registry.yml`. Detailed commands are limited to the untracked task
result file.

## Interfaces and Dependencies

No Proofmill interface or dependency was added. Repository docs and Git remain
the only supported memory fallback.

Latest revision: 2026-08-12. PM-021 completed with Cavemem blocked at the
product boundary before execution.
