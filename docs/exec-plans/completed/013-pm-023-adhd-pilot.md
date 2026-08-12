# Pilot ADHD as isolated advisory review

<!-- markdownlint-disable MD013 MD046 -->

This completed ExecPlan follows `.agent/PLANS.md`. It records the current ADHD
qualification without creating a critical-profile workflow.

## Purpose / Big Picture

This task determined whether current ADHD could provide isolated divergent
review in the Codex-only MVP. Its skill requires parallel isolated subagents,
while this repository permits only one subagent at a time and explicitly rejects
serial execution as invalid. Its CLI requires Claude. ADHD was blocked.

## Bounded Work Packet

    profile: standard
    must_do:
      - inspect the current primary repository and exact release identity
      - record license, installation, files, commands, network, health, failure, fallback, and trust
      - preserve review isolation from contract approval
    must_not_do:
      - add ADHD to a bundle, workflow, release, or Codex configuration
      - create a critical-profile workflow or start critical design work
      - let divergent output approve a contract, evidence state, or pass state
      - weaken the one-subagent rule or create an adapter
    stop_when:
      - the registry and review reflect the process and runtime result

## Progress

- [x] (2026-08-12 01:31Z) Activated PM-023 after closing NeuroArxiv.
- [x] (2026-08-12 01:35Z) Inspected current main and pinned release `v0.1.4`.
- [x] (2026-08-12 01:38Z) Stopped before execution because neither path can satisfy current rules.
- [x] (2026-08-12 01:38Z) Recorded the blocked qualification and clean-context fallback.

## Surprises & Discoveries

- Observation: the Codex skill is syntactically portable but operationally
  incompatible with repository coordination.
  Evidence: it requires five parallel isolated Agent calls and says serial
  branches are not ADHD; repository rules permit only one subagent at a time.
- Observation: the packaged CLI is not a runtime-neutral alternative.
  Evidence: it imports the Claude Agent SDK and needs Anthropic or Claude Code
  authentication.

## Decision Log

- Decision: Qualify isolation without designing a critical profile.
  Rationale: Provider review can be audited without creating prohibited product
  work.
  Date/Author: 2026-08-12 / Codex.
- Decision: Do not weaken coordination or port the provider.
  Rationale: Either change would expand the task into a new agent loop or
  adapter and invalidate the method being qualified.
  Date/Author: 2026-08-12 / Codex.

## Outcomes & Retrospective

PM-023 is complete with ADHD `v0.1.4` pinned and blocked. No package, skill,
model call, workflow, or user configuration was created. One fresh clean-context
Codex adversarial review remains the supported bounded fallback.

## Context and Orientation

`upstream/reviews/adhd.md` is the durable qualification record.
`upstream/registry.yml` keeps the exact release, skill hash, and blocked state
visible. `.agent/test-results/pm-023.md` contains bounded command evidence.

## Plan of Work

The completed work resolved source and release identity, npm integrity, license,
install paths, files, command surface, parallel isolation invariant, network,
health limits, failures, disable, uninstall, and fallback.

## Concrete Steps

Work ran from `/home/mbeutler/Projects/proofmill`. A detached checkout under
`/tmp` was compared with current GitHub and npm state. No dependency install,
skill install, subagent run, or provider command ran.

## Validation and Acceptance

Acceptance requires the registry and review to parse, Markdown lint to pass,
ADHD to remain absent from Proofmill compositions, and divergent output to stay
outside contract approval.

## Idempotence and Recovery

Source inspection is repeatable and read-only. The detached checkout can be
discarded. There is no provider state to remove.

## Artifacts and Notes

Durable conclusions are in `upstream/reviews/adhd.md` and
`upstream/registry.yml`. Detailed commands are limited to the untracked result.

## Interfaces and Dependencies

No Proofmill interface or dependency was added. Fresh clean-context Codex review
remains the only supported isolation mechanism.

Latest revision: 2026-08-12. PM-023 completed with ADHD blocked by the
one-subagent rule and Codex-only runtime.
