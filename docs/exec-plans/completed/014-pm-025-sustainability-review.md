# Add an advisory sustainability review

<!-- markdownlint-disable MD013 MD046 -->

This completed ExecPlan follows `.agent/PLANS.md`.

## Purpose / Big Picture

This task selected the smallest safe use of current best-of-Agent-Harnesses: a
human reads pinned JSON to identify primary-source reviews worth doing. The
source cannot select a provider, change a pin, or widen the Codex-only MVP. No
updater or MCP runtime was added.

## Bounded Work Packet

    profile: standard
    must_do:
      - inspect the current primary source and exact data revision
      - record license, data fields, update process, network, health, failure, fallback, and trust
      - define a manual maintenance rule that cannot change pins automatically
    must_not_do:
      - add a daemon, scheduled updater, dependency, database, or runtime
      - add or qualify another harness for the MVP
      - change any component pin from ranking data alone
    stop_when:
      - the registry and maintenance guidance reflect the advisory boundary

## Progress

- [x] (2026-08-12 01:38Z) Activated PM-025 after closing the ADHD pilot.
- [x] (2026-08-12 01:42Z) Inspected and pinned current data commit `c81b202...`.
- [x] (2026-08-12 01:44Z) Validated the JSON and upstream integrity checks.
- [x] (2026-08-12 01:44Z) Recorded the manual maintenance rule and fallback.

## Surprises & Discoveries

- Observation: the data carries useful dates and evidence links but mixes them
  with popularity and editorial judgment.
  Evidence: star capture is dated; complexity and several capability axes are
  curator-assigned from public docs.
- Observation: the published MCP server is broader and less reproducible than
  the required check.
  Evidence: it fetches repository `main` at startup, while a pinned JSON file
  can be checked directly with no installed runtime.

## Decision Log

- Decision: Keep sustainability input manual and advisory.
  Rationale: Ranking data can trigger investigation but cannot replace exact
  provider qualification.
  Date/Author: 2026-08-12 / Codex.
- Decision: Use pinned JSON, not the MCP server.
  Rationale: Direct inspection satisfies the need with less state, network, and
  mutable behavior.
  Date/Author: 2026-08-12 / Codex.

## Outcomes & Retrospective

PM-025 is complete. The exact data commit is an approved advisory maintenance
input. The process creates no automatic action: a human may add a roadmap item,
then must inspect the provider's primary source. No harness, dependency, MCP
server, schedule, token, or runtime was added.

## Context and Orientation

`upstream/reviews/best-of-agent-harnesses.md` is the qualification record.
`upstream/registry.yml` pins the data revision. `docs/BUILD-VS-INTEGRATE.md`
contains the manual rule. `.agent/test-results/pm-025.md` holds bounded output.

## Plan of Work

The completed work resolved source identity, license, schema, generation and
curation process, refresh network and credentials, MCP alternative, integrity
checks, freshness, disable, uninstall, and fallback. It added only guidance.

## Concrete Steps

Work ran from `/home/mbeutler/Projects/proofmill`. A detached checkout under
`/tmp` supplied the exact JSON and existing integrity check. No refresh or MCP
command ran.

## Validation and Acceptance

The reviewed JSON parses, upstream integrity checks pass, the registry contains
the exact commit, and maintenance guidance prohibits automatic pin changes.

## Idempotence and Recovery

The inspection is repeatable and read-only. Delete the detached checkout when
done. Manual provider source review remains the fallback.

## Artifacts and Notes

Durable conclusions are in the review, registry, and existing build-versus-
integrate guide. Detailed output stays untracked.

## Interfaces and Dependencies

No code or dependency was added. The result is documentation only.

Latest revision: 2026-08-12. PM-025 completed with pinned manual JSON inspection
selected over the MCP server.
