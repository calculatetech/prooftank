# Pilot NeuroArxiv as an advisory research provider

<!-- markdownlint-disable MD013 MD046 -->

This completed ExecPlan follows `.agent/PLANS.md`. It records the current source
qualification without creating a critical-profile workflow.

## Purpose / Big Picture

This task determined whether current NeuroArxiv could add traceable research in
the Codex-only MVP. Its citations retain useful arXiv provenance, but its
installer and skill target Claude Code and its CLI requires the Claude Agent
SDK. There is no release or npm package. It was blocked and manual research
remains the fallback.

## Bounded Work Packet

    profile: standard
    must_do:
      - inspect the current primary repository and exact source identity
      - record license, installation, files, commands, network, health, failure, fallback, and trust
      - identify citation provenance and manual verification needs
    must_not_do:
      - add NeuroArxiv to a bundle, workflow, release, or Codex configuration
      - create a critical-profile workflow or start critical design work
      - treat a summary, citation, or provider success as deterministic proof
      - use an unsupported harness or unavailable subscription
    stop_when:
      - the registry and review reflect the Codex runtime result

## Progress

- [x] (2026-08-12 01:24Z) Activated PM-022 after closing the Cavemem pilot.
- [x] (2026-08-12 01:29Z) Inspected and pinned current source; confirmed there is no release.
- [x] (2026-08-12 01:31Z) Stopped before execution because both supported paths require Claude.
- [x] (2026-08-12 01:31Z) Recorded citation provenance, failures, and manual fallback.

## Surprises & Discoveries

- Observation: the advertised one-line install is mutable.
  Evidence: `npx github:UditAkhourii/neuroarxiv install` follows repository
  state, and upstream has no tag, GitHub release, or npm publication.
- Observation: citations retain more provenance than the final recommendation.
  Evidence: paper records include IDs, versions, dates, authors, and URLs;
  scores, readings, roles, and the chosen path are model-generated.

## Decision Log

- Decision: Qualify the provider without creating a critical profile.
  Rationale: A source and citation audit is bounded; critical workflow design is
  prohibited during bootstrap.
  Date/Author: 2026-08-12 / Codex.
- Decision: Do not port or run NeuroArxiv.
  Rationale: A port would create an unplanned adapter or agent loop, while the
  existing paths require unsupported Claude authentication.
  Date/Author: 2026-08-12 / Codex.

## Outcomes & Retrospective

PM-022 is complete with NeuroArxiv blocked for the Codex MVP. The current source
commit is preserved for traceability, but it is not a release pin. No package,
skill, workflow, or user configuration was created. Manual primary-source
research remains the fallback.

## Context and Orientation

`upstream/reviews/neuroarxiv.md` is the durable qualification record.
`upstream/registry.yml` keeps the exact inspected source and blocked state
visible. `.agent/test-results/pm-022.md` contains bounded command evidence.

## Plan of Work

The completed work resolved source identity, release state, license,
dependencies, install effect, command surface, citation fields, arXiv and Claude
network calls, health limits, failures, disable, uninstall, and fallback.

## Concrete Steps

Work ran from `/home/mbeutler/Projects/proofmill`. A detached checkout under
`/tmp` was compared with current GitHub and npm state. No dependency install,
model call, or provider command ran.

## Validation and Acceptance

Acceptance requires the registry and review to parse, Markdown lint to pass,
NeuroArxiv to remain absent from Proofmill compositions, and manual research to
remain explicit and advisory.

## Idempotence and Recovery

Source inspection is repeatable and read-only. The detached checkout can be
discarded. There is no provider state to remove.

## Artifacts and Notes

Durable conclusions are in `upstream/reviews/neuroarxiv.md` and
`upstream/registry.yml`. Detailed commands are limited to the untracked result.

## Interfaces and Dependencies

No Proofmill interface or dependency was added. Codex-native manual research is
the supported fallback.

Latest revision: 2026-08-12. PM-022 completed with NeuroArxiv blocked by the
Codex-only MVP and unavailable Claude authentication.
