# Proofmill Lite design

## Purpose

Proofmill Lite is the smallest Proofmill process for a low-risk Codex change.
It preserves the scope ceiling and executable checks. It removes Standard-only
analysis and approval steps.

This document defines a future composition. It does not authorize or publish a
Lite preset, workflow, bundle, or release.

## Entry boundary

Use Lite only when the change is isolated, reversible, and cheap to diagnose.
Examples include a typo, a local root-cause fix, isolated user-interface
behavior, a small internal utility, or a low-risk configuration change.

Do not use Lite when a change affects:

- user data integrity or loss.
- money, identity, authorization, privacy, or security.
- durable state, retry, restart, concurrency, or coordination.
- a process, language, database, network, or provider boundary.
- architecture that is expensive to reverse.
- a path shared by many callers or products.

If one condition appears during work, stop before implementation continues.
Reclassify the work as Standard or Critical. Preserve completed artifacts as
input. Do not call the Lite result passed.

## Minimum contract

The future `proofmill-lite-contract` preset must add only:

- `profile: lite`.
- a focused behavior statement.
- `must_do`, `must_not_do`, `may_do`, and `stop_when`.
- one focused regression check.
- current project-native test and lint commands.
- known unknowns and unavailable providers.

Stable requirement or invariant identifiers are optional unless the project
already uses them. Owners, concurrency, recovery, and full traceability sections
are Standard or Critical concerns. Their absence is acceptable only because the
entry boundary excludes those risks.

## Bounded work packet

The future plan template must use this minimum shape:

```yaml
profile: lite
must_do: []
must_not_do: []
may_do: []
stop_when: []
focused_check: ""
native_tests: []
native_lint: []
known_unknowns: []
providers:
  used: []
  unavailable: []
  degraded: []
```

An empty `focused_check`, `native_tests`, or `native_lint` value does not pass.
If the project has no applicable command, record `unknown` and stop completion.

## Providers

Ponytail is required. If `.agents/skills/ponytail/SKILL.md` is absent, stop
before specification work and report `unavailable: ponytail`.

SimpleEnglish is optional for Lite. Use the short writing rules in `AGENTS.md`
when the skill is absent. Do not report that fallback as degraded assurance.
Lite does not require controlled-language qualification.

Research, divergent design review, structural graphs, cross-session memory,
mutation tests, and formal checks are excluded by default. Escalate the profile
when the failure model needs one of them.

## Future native composition

The future Codex-only composition must contain:

- preset `proofmill-lite-contract`.
- workflow `proofmill-lite`.
- bundle `proofmill-lite`.
- a versioned local release with exact component and provider checksums.

The workflow must use these native Spec Kit steps:

1. Check for Ponytail.
2. Run `speckit.specify`.
3. Run `speckit.plan` to create the bounded packet.
4. Present one gate for scope and risk escalation.
5. Run `speckit.tasks`.
6. Run `speckit.implement`.
7. Run `speckit.converge`.
8. Present one gate for current focused-check, test, and lint evidence.

Do not add `speckit.analyze` by default. Do not add separate contract, plan, and
analysis gates. A project can reclassify the change when it needs that ceremony.

The workflow must dispatch only to Codex. It must contain no compatibility or
routing metadata for another harness.

## Evidence and completion

Lite can pass only when all of these facts are current:

- the focused regression check passes.
- the project-native tests pass.
- the project-native lint command passes.
- the bounded packet has no unresolved `must_do` item.
- no escalation condition applies.
- no required provider is unavailable.
- every remaining gap is reported as `unknown`, not `passed`.

Agent review and human inspection can explain a result. They are not
deterministic evidence. Preserve `passed`, `failed`, `stale`, `degraded`,
`unknown`, and `waived` as distinct states.

## Installation and removal boundary

Use the same pinned Spec Kit release and native local-directory installation as
Proofmill Standard. The future release can reuse the approved Ponytail bytes.
It must not install SimpleEnglish unless the user selects it.

Disable or remove only the exact Lite preset, workflow, bundle, and provider
directories. Removal must preserve specifications, plans, tasks, source files,
and test evidence.

## Implementation acceptance

A later implementation task can complete only after it proves all of these
behaviors in a disposable Codex project:

- native preset, workflow, and bundle validation passes.
- a low-risk fixture produces the minimum contract and bounded packet.
- missing Ponytail stops before specification.
- missing SimpleEnglish does not stop Lite.
- one escalation fixture stops before implementation.
- failed or absent focused checks remain `failed` or `unknown`.
- disable and uninstall preserve repository truth.
- no Proofmill runtime, installer, daemon, database, or adapter is added.
