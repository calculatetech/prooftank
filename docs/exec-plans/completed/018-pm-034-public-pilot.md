# Prepare the Codex public pilot

<!-- markdownlint-disable MD013 MD046 -->

This ExecPlan is a living document. Maintain it according to
`.agent/PLANS.md` and keep `docs/roadmap.md` current.

## Purpose / Big Picture

This task makes the measured Codex MVP understandable to a pilot user. It
publishes one bounded guide for installation, validation, limitations,
contribution, provider replacement, disable, and uninstall. It does not publish
a package, create a remote catalog, open a pull request, or start a release.

## Bounded Work Packet

    profile: standard
    must_do:
      - provide exact local installation and health commands
      - link qualification and benchmark evidence
      - state unsupported claims and Codex-only scope
      - explain contribution, replacement, disable, and uninstall boundaries
    must_not_do:
      - publish a package, catalog, site, release, PR, or announcement
      - add a provider, harness, runtime, or critical profile
      - claim a benchmark quality or lifecycle-cost advantage
      - start PM-035 before this task completes
    stop_when:
      - a new pilot user can follow one current guide without stale starter claims

## Progress

- [x] (2026-08-12 02:01Z) Activated PM-034 after publishing the measured decision.
- [x] (2026-08-12) Wrote the bounded public-pilot guide from existing exact commands.
- [x] (2026-08-12) Validated links, checksums, Markdown, and roadmap state.
- [x] (2026-08-12) Archived this plan and stopped at the human name-clearance task.

## Surprises & Discoveries

- Observation: The repository has no configured remote or public issue tracker.
  Evidence: `git remote -v` returned no entries.

## Decision Log

- Decision: Publish guidance only, not distribution infrastructure.
  Rationale: The local checksummed release already installs; remote publication
  needs name clearance and separate authority.
  Date/Author: 2026-08-12 / Codex.

## Outcomes & Retrospective

PM-034 is complete. A new user has one Codex-only local pilot guide. It reuses
the checksummed `0.1.0` release procedure and makes the benchmark limits and
provider replacement boundary explicit. No external publication occurred.

## Context and Orientation

The exact local release is `releases/proofmill-standard/0.1.0/`. Provider
reviews are under `upstream/reviews/`. The preserved benchmark is under
`conformance/checkbook/results/first-comparable-001/`. Current limitations are
in `docs/BOOTSTRAP-GAP-REPORT.md` and
`docs/WHAT-PROOFMILL-DOES-NOT-PROVE.md`.

## Plan of Work

Create one guide under `docs/` that points to existing commands and records
rather than copying long procedures. Cover supported scope, prerequisites,
install, health, first use, evidence, limitations, contribution rules, provider
replacement, disable, uninstall, and feedback. Link it from the README.

## Concrete Steps

Work from `/home/mbeutler/Projects/proofmill`. Add documentation only. Validate
all linked local paths and the release checksum manifest.

## Validation and Acceptance

Every local link must resolve. The release checksum command must pass. The guide
must say Codex-only, local pilot, no quality advantage, no release warrant, and
no external publication.

## Idempotence and Recovery

The guide delegates exact operational commands to the versioned release README,
so a later release can replace one link rather than duplicate procedures.

## Artifacts and Notes

Create `docs/PUBLIC-PILOT.md`. Detailed validation belongs in
`.agent/test-results/pm-034.md`.

## Interfaces and Dependencies

Add no interface or dependency.

Latest revision: 2026-08-12. PM-034 completed; PM-035 requires human name
clearance before public distribution.
