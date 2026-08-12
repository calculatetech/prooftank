# Design Proofmill Lite for Codex

<!-- markdownlint-disable MD013 MD046 -->

This ExecPlan is a living document. Maintain it according to
`.agent/PLANS.md` and update `docs/roadmap.md` with PM-032 status.

## Purpose / Big Picture

Proofmill Lite needs a clear profile before anyone creates another preset or
workflow. After this task, a contributor can tell which changes qualify for
Lite, what artifacts and checks it requires, when it must escalate, and which
parts of Standard it deliberately omits. This task designs that behavior for
Codex only. It does not publish an executable Lite composition.

## Bounded Work Packet

    profile: lite
    must_do:
      - define Lite entry and escalation conditions
      - define the minimum contract, work packet, providers, workflow, and evidence
      - keep Codex as the only supported MVP harness
      - use native Spec Kit concepts and project-native checks
      - align the risk profile and provider registry
      - keep the roadmap current
    must_not_do:
      - create a Lite preset, workflow, bundle, release, installer, or runtime
      - include another harness or cross-harness metadata
      - weaken security, data-loss, or trust-boundary handling
      - start the checkbook benchmark or critical profile
    may_do:
      - define future artifact names and ordered native workflow steps
      - reuse Standard evidence states and uninstall behavior
    stop_when:
      - one human-readable design defines an implementable minimal Lite vertical
      - every active document agrees that Codex is the only MVP harness
      - Markdown and YAML validation pass

## Progress

- [x] (2026-08-12 01:38Z) Activated PM-032 after PM-031 completed.
- [x] (2026-08-12 01:42Z) Read the current risk profiles, Standard preset,
      workflow, bundle, registry, and MVP runtime decisions.
- [x] (2026-08-12 01:51Z) Wrote the Codex-only Lite design and aligned risk and
      provider policy.
- [x] (2026-08-12 01:54Z) Passed Markdown, SimpleEnglish, YAML, artifact-absence,
      and diff validation. Completed PM-032.

## Surprises & Discoveries

- Observation: The risk profile requires Ponytail or equivalent for Lite, but
  the registry marks Ponytail optional for Lite.
  Evidence: `docs/RISK-PROFILES.md` and `upstream/registry.yml` disagree.
- Observation: Reusing the Standard preset would falsely label Lite work as
  Standard and require Standard-only assurance fields.
  Evidence: Every current contract template hard-codes `standard` and adds
  traceability, failure, recovery, concurrency, and evidence detail.

## Decision Log

- Decision: Design a separate future Lite composition instead of parameterizing
  Standard.
  Rationale: Two small native compositions are clearer than one conditional
  template and workflow. Lite has a real current difference in required
  ceremony.
  Date/Author: 2026-08-12 / Codex.
- Decision: Keep Ponytail required and SimpleEnglish optional for Lite.
  Rationale: Minimal implementation is a defining Lite control. The repository
  writing rules are the sufficient fallback for short Lite instructions.
  Date/Author: 2026-08-12 / Codex.

## Outcomes & Retrospective

PM-032 is complete. `docs/PROOFMILL-LITE.md` defines a minimal future Codex
composition, strict escalation conditions, required evidence, and removal
boundaries. No executable Lite artifact or new runtime was created.

## Context and Orientation

`docs/RISK-PROFILES.md` classifies changes as Lite, Standard, or Critical.
`presets/proofmill-contract/` and `workflows/proofmill-standard/` implement only
Standard. A Spec Kit preset adds repository templates. A workflow orders native
Spec Kit commands and human gates. `upstream/registry.yml` records which
providers each profile requires. The MVP release under
`releases/proofmill-standard/0.1.0/` supports only Codex.

PM-032 is a design task. The production artifact is a versioned design under
`docs/`, not an unconsumed preset or workflow. A later roadmap task must be
authorized before it implements the design.

## Plan of Work

Create `docs/PROOFMILL-LITE.md`. Define strict entry and escalation rules, the
minimum future preset and workflow, required providers, deterministic evidence,
failure behavior, installation boundaries, and acceptance criteria. Name the
future artifacts without creating them.

Update `docs/RISK-PROFILES.md` so Lite stops when higher-risk conditions appear.
Update `upstream/registry.yml` so Ponytail is required for Lite. Update the
roadmap and this plan when validation passes.

## Milestones

The boundary milestone ends when the design makes misuse visible: a change with
data, money, security, durable state, concurrency, external boundaries, or wide
shared impact cannot remain Lite. The composition milestone ends when a future
implementer has exact native artifact roles and ordered steps. The record
milestone ends when documentation and YAML checks pass and PM-032 is archived.

## Concrete Steps

Work from `/home/mbeutler/Projects/proofmill`. Read the Standard composition
before writing Lite. Edit only the design, risk profile, provider registry,
roadmap, and this plan. Validate with the repository's Markdown linter, PyYAML,
and `git diff --check`.

Keep detailed results in `.agent/test-results/pm-032.md`. Do not create any
preset, workflow, bundle, release, installer, script, or test fixture.

## Validation and Acceptance

The design must state that Codex is the only MVP harness. It must require a
bounded packet, Ponytail, one focused regression check, and current native tests
and lint. It must not require SimpleEnglish, analysis, research, memory,
structural graphs, mutation tests, or multiple approval gates by default.

The design must define an observable escalation stop. Markdown lint, registry
YAML parsing, and `git diff --check` must pass. Because this task changes only
documentation and qualification metadata, it does not require an adversarial
code review.

## Idempotence and Recovery

All changes are versioned prose or registry metadata. Revert those exact edits
to recover. Do not create an executable artifact that could become a second
owner before implementation is authorized.

## Artifacts and Notes

The durable design belongs at `docs/PROOFMILL-LITE.md`. Detailed command output
belongs only in `.agent/test-results/pm-032.md`.

## Interfaces and Dependencies

Use the pinned Spec Kit concepts already qualified by Proofmill. Add no package,
dependency, service, or executable code. The future design can name native
preset and workflow interfaces but must not implement them in PM-032.

Latest revision: 2026-08-12. PM-032 is complete and validated.
