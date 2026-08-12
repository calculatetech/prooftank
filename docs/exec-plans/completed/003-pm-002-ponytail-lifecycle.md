# Close Ponytail lifecycle qualification

<!-- markdownlint-disable MD013 MD046 -->

This ExecPlan is a living document. Maintain it according to
`.agent/PLANS.md` and update `docs/roadmap.md` with PM-002 status.

## Purpose / Big Picture

Proofmill Standard requires Ponytail but its review does not yet prove the full
host lifecycle. This task tests the exact reviewed source in disposable Codex
state, records update and failure behavior, and either promotes the advisory
qualification or preserves a blocker. The user can then distinguish a healthy
instruction provider from deterministic evidence.

## Bounded Work Packet

    profile: standard
    must_do:
      - confirm the exact reviewed source and current upstream identity
      - test clean install, health, restart, update, unavailable, disable, and uninstall
      - preserve repository truth and the stop-before-implementation fallback
      - update the review, registry, roadmap, and this plan
    must_not_do:
      - change Ponytail source or its exact reviewed pin
      - claim that Ponytail output proves correctness or minimality
      - add a Proofmill runtime or provider adapter
      - start PM-003 before PM-002 completes
    may_do:
      - use repository-local exact-copy installation when it is the only pin-safe path
      - keep marketplace installation blocked if it cannot enforce the pin
    stop_when:
      - every required lifecycle state has direct evidence
      - the qualification state and fallback are current

## Progress

- [x] (2026-08-11 22:08Z) Activated PM-002 and bounded it to Ponytail lifecycle
      qualification.
- [x] (2026-08-11 22:13Z) Resolved current upstream at the reviewed commit and
      constructed disposable exact-pin fixtures.
- [x] (2026-08-11 22:13Z) Passed clean install, health, restart, explicit update,
      unavailable, disable, reinstall, uninstall, and truth-preservation checks.
- [x] (2026-08-11 22:13Z) Updated durable records and passed Markdown, YAML, hash,
      and upstream test validation.
- [x] (2026-08-11 22:13Z) Completed PM-002. This plan is ready to archive.

## Surprises & Discoveries

- Observation: Current remote HEAD still equals the reviewed pin.
  Evidence: a fresh clone resolved
  `2ed6c52c9d7e5e56942508591085fd45dea277d3`.
- Observation: Marketplace update is not a pin-safe path.
  Evidence: `.agents/plugins/marketplace.json` declares `ref: main`; moving from
  release `v4.9.0` to the reviewed commit changed hook bytes without changing
  package version or the main skill bytes.
- Observation: The exact-copy path has a complete and smaller lifecycle.
  Evidence: one skill directory installed, restarted, updated from `v4.8.4`,
  disabled, reinstalled, and uninstalled without changing repository truth.

## Decision Log

- Decision: Treat all Ponytail output as advisory.
  Rationale: Its instructions can influence implementation choices but cannot
  produce deterministic correctness or release evidence.
  Date/Author: 2026-08-11 / Codex with Ponytail.
- Decision: Approve only the exact-copy main skill.
  Rationale: It is byte-verifiable, contains no hook runtime, and matches the
  existing standard workflow. The marketplace follows a mutable branch and is
  unnecessary for the current composition.
  Date/Author: 2026-08-11 / Codex with Ponytail.
- Decision: Do not start an adversarial review cycle.
  Rationale: PM-002 changed qualification and installation documentation only,
  not executable source or runtime configuration.
  Date/Author: 2026-08-11 / Codex.

## Outcomes & Retrospective

PM-002 approved Ponytail as an advisory provider through the exact-copy main
skill. Every required lifecycle state passed, the reviewed pin and skill hash
are durable, and absence still stops the standard workflow before work begins.
Marketplace installation remains unapproved. PM-031 owns immutable publication.
PM-003 remains next.

## Context and Orientation

`upstream/reviews/ponytail.md` records identity, writes, hooks, network access,
failure behavior, and the incomplete lifecycle. `upstream/registry.yml` pins
commit `2ed6c52c9d7e5e56942508591085fd45dea277d3`. The standard workflow checks
for `.agents/skills/ponytail/SKILL.md` before specification work.

The marketplace install follows its configured repository branch. The exact
copy path copies `skills/ponytail/` from the reviewed checkout into the target
repository. Exact-copy installation omits plugin hooks but makes the source pin
inspectable and removable.

## Plan of Work

Clone the current primary repository and detach the reviewed commit. Inspect
the plugin manifest, marketplace metadata, lifecycle scripts, and tests. Use
temporary project and configuration paths; do not mutate the user's installed
plugin.

Test the exact-copy path from empty target state, including content identity,
a fresh process, an absent skill, disable by removal from discovery, reinstall,
and uninstall. Test the plugin scripts in isolated plugin data/config state for
mode disable and cleanup. Model an update with two local source revisions so a
new copy changes only after explicit replacement and the exact reviewed copy is
restorable.

Run upstream health tests with their documented dependencies in disposable
state. Update the provider review and registry only after every required state
is known. If any standard-profile absence can become success, keep the provider
blocked.

## Milestones

The source milestone ends when current remote HEAD, reviewed commit, release,
license, manifest, hooks, and update mechanism are known. The lifecycle
milestone ends when clean install, health, restart, update, unavailable,
disable, and uninstall have distinct observed states. The record milestone ends
when review, registry, roadmap, and validation agree.

## Concrete Steps

Work from `/home/mbeutler/Projects/proofmill`. Clone to a temporary directory,
then run:

    git rev-parse HEAD
    git checkout --detach 2ed6c52c9d7e5e56942508591085fd45dea277d3
    npm test

Keep detailed results in `.agent/test-results/pm-002.md`. Use temporary target
repositories and task-specific environment paths. Do not change the installed
personal marketplace or global Codex plugin state.

## Validation and Acceptance

The exact-copy health check is a readable `SKILL.md` whose bytes match the
reviewed source. A fresh process must see the same file. Absence must make the
standard workflow preflight fail. Disable and uninstall must make the skill
unavailable without changing specifications, plans, tasks, or source files.

An update must be explicit and its new source identity visible. Restoring the
reviewed pin must restore the reviewed bytes. Upstream tests and repository
Markdown/YAML validation must pass.

## Idempotence and Recovery

All lifecycle targets are disposable. Recreate them rather than repair them.
Exact-copy install is recovered by removing the target skill directory and
copying it again from the detached reviewed source. No global plugin mutation is
needed.

## Artifacts and Notes

Durable conclusions belong in `upstream/reviews/ponytail.md` and
`upstream/registry.yml`. Repeated command output belongs only in the ignored
result file.

## Interfaces and Dependencies

Use the reviewed Ponytail source only. Node.js runs plugin hooks and upstream
tests. Python with pandas is a documented benchmark-test dependency. Add no
dependency to Proofmill.

Latest revision: 2026-08-11. PM-002 completed with exact-copy approval after the
full lifecycle and provider tests passed.
