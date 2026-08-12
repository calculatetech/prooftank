# Pilot CBM as an observational Codex provider

<!-- markdownlint-disable MD013 MD046 -->

This completed ExecPlan follows `.agent/PLANS.md`. It records why the planned
runtime pilot stopped before executing the provider.

## Purpose / Big Picture

This task determined whether current Codebase Memory MCP (CBM) could provide
useful structural observations to Codex without crossing Proofmill's product
boundary. Source qualification showed that its first useful operation creates a
persistent code graph and SQLite state, while MCP use also starts a daemon. CBM
was blocked and native repository search remained the fallback.

## Bounded Work Packet

    profile: standard
    must_do:
      - inspect the current primary repository and exact release identity
      - record license, installation, files, commands, network, health, failure, fallback, and trust
      - preserve native repository search as the fallback
      - stop before creating prohibited provider state
    must_not_do:
      - add CBM to a bundle, workflow, release, or default Codex configuration
      - treat a missing edge or empty result as proof
      - create a code graph, daemon, database, MCP aggregator, or adapter
      - modify user-level MCP or Codex configuration
    stop_when:
      - the registry and review state reflect the measured current boundary

## Progress

- [x] (2026-08-12 01:01Z) Activated PM-020 after the first comparable benchmark.
- [x] (2026-08-12 01:10Z) Inspected current main and pinned release `v0.10.2`.
- [x] (2026-08-12 01:14Z) Stopped before release execution because indexing necessarily creates prohibited persistent graph and SQLite state.
- [x] (2026-08-12 01:14Z) Recorded the blocked qualification and native fallback.

## Surprises & Discoveries

- Observation: CBM is not merely a read-only MCP query surface.
  Evidence: upstream documents SQLite graph storage, a per-account daemon,
  watchers, optional local HTTP UI, Codex hooks, skills, instructions, and agent
  profiles.
- Observation: current `main` is newer than the current release.
  Evidence: release `v0.10.2` points to `b377c62...`; inspected main was
  `7f23a66...`, so the release commit is the reproducible pin.

## Decision Log

- Decision: Keep all provider state and configuration outside Proofmill.
  Rationale: The pilot must not alter the user's Codex environment or make CBM
  a hidden source of truth.
  Date/Author: 2026-08-12 / Codex.
- Decision: Stop before installing or indexing with CBM.
  Rationale: Revision freshness, interruption, restart, and symbol tests all
  require the graph state prohibited by the bootstrap. Crossing the boundary to
  test whether crossing it works would not qualify the provider for this MVP.
  Date/Author: 2026-08-12 / Codex.

## Outcomes & Retrospective

PM-020 is complete with a negative result. CBM `v0.10.2` is pinned for the
record and blocked for the MVP. It is not in a bundle, workflow, release, or
Codex configuration. Native `rg`, direct reads, Git, tests, and lint remain the
fallback. No provider binary ran and no graph, database, daemon, or user config
was created.

## Context and Orientation

`upstream/reviews/codebase-memory-mcp.md` is the durable qualification record.
`upstream/registry.yml` keeps the candidate visible with its exact release pin
and blocked state. `.agent/test-results/pm-020.md` contains the bounded command
record and stays untracked.

## Plan of Work

The completed work resolved the official release and current source identity,
read the license, configuration reference, runtime lifecycle, Codex installer,
uninstaller, command registry, and documented failure behavior. It then applied
the product boundary before execution and recorded the fallback.

## Concrete Steps

Work ran from `/home/mbeutler/Projects/proofmill`. A detached source checkout
under `/tmp` was compared with the repository's current remote head and GitHub's
current release record. No install command or release binary ran.

## Validation and Acceptance

Acceptance requires the registry and review to parse, Markdown lint to pass,
CBM to remain absent from Proofmill compositions, and native search to remain
available. It does not require a provider execution that would violate the
bounded packet.

## Idempotence and Recovery

Source inspection is repeatable and read-only. The detached checkout can be
discarded. There is no provider state to recover or uninstall.

## Artifacts and Notes

Durable conclusions are in `upstream/reviews/codebase-memory-mcp.md` and
`upstream/registry.yml`. Detailed commands are limited to the untracked task
result file.

## Interfaces and Dependencies

No Proofmill interface or dependency was added. Native repository tools remain
the only supported structural fallback.

Latest revision: 2026-08-12. PM-020 completed with CBM blocked at the product
boundary before execution.
