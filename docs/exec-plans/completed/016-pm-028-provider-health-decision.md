# Decide whether a provider-health extension is necessary

<!-- markdownlint-disable MD013 MD046 -->

This completed ExecPlan follows `.agent/PLANS.md`.

## Purpose / Big Picture

This task compared active provider health and lifecycle records to decide
whether Proofmill needs shared health code. It does not. Exact native version
and hash checks already expose the measured states, and the workflow stops when
a required provider is unavailable.

## Bounded Work Packet

    profile: standard
    must_do:
      - compare active provider health and lifecycle records
      - identify any measured health state current commands cannot express
      - preserve unavailable, stale, degraded, and unknown as distinct states
      - record build, integrate, defer, or stop with evidence
    must_not_do:
      - implement a provider-health command, protocol, daemon, or adapter
      - aggregate providers behind a new interface
    stop_when:
      - the build-versus-integrate decision names the measured result

## Progress

- [x] (2026-08-12 01:49Z) Activated PM-028 after the release-warrant decision.
- [x] (2026-08-12 01:52Z) Compared exact active-provider health and fallback paths.
- [x] (2026-08-12 01:53Z) Recorded a no-build and no-integrate decision.

## Surprises & Discoveries

- Observation: a shared boolean health result would lose information already
  present in provider-specific checks.
  Evidence: current records distinguish absent skills, wrong hashes, source-test
  failures, offline catalogs, degraded results, and unknown evidence.

## Decision Log

- Decision: Add no shared provider-health extension.
  Rationale: Existing exact commands cover active providers, and no observed
  incident needs a new owner.
  Date/Author: 2026-08-12 / Codex.

## Outcomes & Retrospective

PM-028 is complete with no code authorized. Spec Kit version output, provider
hashes, source tests, workflow preflight, and explicit evidence states remain
the health system. A future preserved incident can reopen the decision.

## Context and Orientation

Active provider records are `upstream/reviews/github-spec-kit.md`,
`upstream/reviews/ponytail.md`, and `upstream/reviews/simple-english.md`. The
release health commands are in `releases/proofmill-standard/0.1.0/README.md`.
The durable decision is in `docs/BUILD-VS-INTEGRATE.md` and
`docs/DECISIONS.md`.

## Plan of Work

The completed work compared native health, preflight failure, hash identity,
disable, reinstall, uninstall, blocked optional-provider fallbacks, and evidence
states. It found no missing consumer for a shared abstraction.

## Concrete Steps

Work ran from `/home/mbeutler/Projects/proofmill`. Existing review, workflow,
release, and registry files were read. No provider install or executable ran.

## Validation and Acceptance

The decision preserves unavailable as unknown or failure, never success, and
names the future evidence that can reopen it.

## Idempotence and Recovery

Revisit after a provider incident that exact current checks cannot represent.
Until then, provider-specific commands remain the fallback.

## Artifacts and Notes

Durable conclusions are in existing decision and build-versus-integrate docs.
Detailed checks stay in `.agent/test-results/pm-028.md`.

## Interfaces and Dependencies

No interface or dependency was added.

Latest revision: 2026-08-12. PM-028 completed with a measured no-build decision.
