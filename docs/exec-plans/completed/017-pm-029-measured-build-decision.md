# Publish the measured build-versus-integrate decision

<!-- markdownlint-disable MD013 MD046 -->

This completed ExecPlan follows `.agent/PLANS.md`.

## Purpose / Big Picture

This task published one consistent MVP decision from the completed
qualifications and benchmark. The supported composition is Codex, GitHub Spec
Kit, Ponytail, SimpleEnglish, native tests and lint, and declarative Proofmill
files. No runtime code or optional runtime provider is authorized.

## Bounded Work Packet

    profile: standard
    must_do:
      - reconcile the registry, roadmap, benchmark, gap report, and decision log
      - name accepted, comparison-only, blocked, postponed, and unknown items
      - state the supported Codex MVP composition and remaining claims
      - state whether any Proofmill runtime code is authorized
    must_not_do:
      - add a provider, extension, runtime, workflow, or critical profile
      - change a source pin without a new qualification
      - overclaim the single benchmark batch
    stop_when:
      - one human-readable decision is consistent with all versioned records

## Progress

- [x] (2026-08-12 01:53Z) Activated PM-029 after provider-health review.
- [x] (2026-08-12 01:58Z) Reconciled all current qualification and benchmark conclusions.
- [x] (2026-08-12 02:01Z) Published the measured decision in existing sources of truth.

## Surprises & Discoveries

- Observation: several starter claims still described the pre-measurement
  product.
  Evidence: the README advertised five harnesses, optional graph and memory
  providers, and a warrant; the policy required an absent deterministic gate.

## Decision Log

- Decision: Close the MVP provider set.
  Rationale: Every additional candidate is blocked, postponed, comparison-only,
  or unreviewed, and the benchmark authorizes no more runtime.
  Date/Author: 2026-08-12 / Codex.
- Decision: Publish in existing source-of-truth files.
  Rationale: A new report would duplicate the registry, build decision, and gap
  report.
  Date/Author: 2026-08-12 / Codex.

## Outcomes & Retrospective

PM-029 is complete. Accepted, blocked, comparison-only, postponed, and backlog
states now agree across policy and human-readable docs. The product claim is
narrowed to what the single benchmark and dry run support. No executable code,
dependency, provider, workflow, or runtime was added.

## Context and Orientation

`upstream/registry.yml` owns component states. `docs/BUILD-VS-INTEGRATE.md`
owns selection. `docs/BOOTSTRAP-GAP-REPORT.md` owns the measured recommendation.
`docs/DECISIONS.md` records the closed provider set. `README.md` presents that
state to new users.

## Plan of Work

The completed work compared every registry entry with the roadmap, benchmark,
gap report, policy, decision log, and README. It removed stale active claims and
preserved negative findings and unknowns.

## Concrete Steps

Work ran from `/home/mbeutler/Projects/proofmill`. Only versioned documentation
and declarative product policy changed.

## Validation and Acceptance

Acceptance requires valid YAML and Markdown, one roadmap task, no blocked
provider in a bundle or release, no unsupported harness claim, and no benchmark
quality overclaim.

## Idempotence and Recovery

The published state can be reconstructed from exact reviews and the preserved
benchmark. No product state changed.

## Artifacts and Notes

Durable conclusions remain in existing source-of-truth files. Detailed
validation stays in `.agent/test-results/pm-029.md`.

## Interfaces and Dependencies

No interface or dependency was added.

Latest revision: 2026-08-12. PM-029 completed with no runtime code authorized.
