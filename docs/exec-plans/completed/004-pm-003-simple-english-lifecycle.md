# Close SimpleEnglish lifecycle qualification

<!-- markdownlint-disable MD013 MD046 -->

This ExecPlan is a living document. Maintain it according to
`.agent/PLANS.md` and update `docs/roadmap.md` with PM-003 status.

## Purpose / Big Picture

Proofmill Standard requires SimpleEnglish for technical instructions, but its
review does not yet prove the full lifecycle or protected technical text across
representative documents. This task qualifies the exact-copy skill and uses
four bounded Codex fixtures to show whether prose can improve without changing
code, commands, paths, identifiers, or quoted errors.

## Bounded Work Packet

    profile: standard
    must_do:
      - confirm current upstream and the reviewed exact pin
      - test clean install, health, update, restart, unavailable, disable, and uninstall
      - exercise contract, work-packet, error, and runbook fixtures through Codex
      - compare protected technical tokens byte for byte
      - preserve advisory trust and the lite-only degraded fallback
    must_not_do:
      - claim full ASD-STE100 compliance from the regex linter
      - change protected code, commands, paths, identifiers, or quoted errors
      - add a prose-rewriting runtime or dependency to Proofmill
      - start PM-030 before PM-003 completes
    may_do:
      - approve the exact-copy skill if every lifecycle and preservation check passes
      - keep the unpinned npx path unapproved
    stop_when:
      - all lifecycle states and four fixtures have direct evidence
      - review, registry, roadmap, and installation guidance agree

## Progress

- [x] (2026-08-11 22:16Z) Activated PM-003 and bounded it to exact-copy
      lifecycle and protected-text fixtures.
- [x] (2026-08-11 22:35Z) Confirmed current source, exact pin, skill files,
      references, linter, and mutable upstream install path.
- [x] (2026-08-11 22:43Z) Passed provider tests and the exact-copy lifecycle
      matrix, including an explicit prior-commit update.
- [x] (2026-08-11 22:52Z) Ran four bounded Codex fixtures; every protected value
      retained the same bytes and occurrence count.
- [x] (2026-08-11 23:05Z) Updated durable records, passed relevant validation,
      completed PM-003, and archived this plan.

## Surprises & Discoveries

- Observation: The reviewed commit remains upstream `HEAD`, four commits after
  release tag `v1.2.0`.
  Evidence: `git describe --tags --always` returned `v1.2.0-4-g59bf670`.
- Observation: The upstream `npx skills add` command does not express the
  reviewed commit.
  Evidence: Exact qualification required copying the three reviewed skill files
  and comparing their SHA-256 values.
- Observation: The installed skill starts no persistent process.
  Evidence: It registers instructions and references only, so an interrupted
  operation test is not applicable.

## Decision Log

- Decision: Keep SimpleEnglish advisory and preserve technical spans exactly.
  Rationale: Clear prose can reduce ambiguity, but it cannot rename interfaces
  or become deterministic proof of language compliance.
  Date/Author: 2026-08-11 / Codex.
- Decision: Approve only the exact-copy three-file Codex skill.
  Rationale: Its lifecycle and bounded preservation checks passed, while the
  upstream `npx` path remains mutable and unpinned.
  Date/Author: 2026-08-11 / Codex.

## Outcomes & Retrospective

PM-003 is complete. The exact-copy SimpleEnglish skill is approved as advisory
at one commit and three file hashes. Provider tests, lifecycle states, explicit
update, and four protected-text fixtures passed. The unpinned `npx` install and
all general compliance claims remain outside approval.

## Context and Orientation

`upstream/reviews/simple-english.md` records the provider identity and current
limitations. `upstream/registry.yml` pins commit
`59bf6702197a5aadc96d197ea17f290d8d50dcd3`. The standard install copies
`skills/simple-english/` into `.agents/skills/simple-english/`. The standard
workflow stops if `SKILL.md` is absent.

Protected text means code spans and fences, shell commands, file paths, stable
IDs, and quoted error text. The skill may simplify surrounding prose but must
copy protected text byte for byte.

## Plan of Work

Clone the current primary source and detach the reviewed commit. Inspect the
skill, its reference files, linter, tests, install metadata, network behavior,
and removal path. Run the upstream self-test and unit tests.

Use disposable exact-copy targets for install, restart, update, unavailable,
disable, reinstall, and uninstall checks. Record a content hash for every file
in the approved skill directory.

Create four small versioned input fixtures under
`conformance/simple-english/`. In a disposable Codex project with the reviewed
skill, ask Codex to simplify one fixture at a time without changing protected
text. Preserve the outputs and a compact token list. Compare every protected
token literally. Provider output is advisory even when every check passes.

Update the review, registry, bundle guidance, roadmap, and this plan. Run only
the Markdown, YAML, provider, and fixture checks relevant to the changes.

## Milestones

The source milestone ends when current upstream identity and all installed files
are exact. The lifecycle milestone ends when every state is visible and
repository truth survives. The fixture milestone ends when all four outputs
preserve their protected text. The record milestone ends when the provider can
be approved or blocked without ambiguity.

## Concrete Steps

Work from `/home/mbeutler/Projects/proofmill`. Clone the primary source to
`/tmp`, inspect the reviewed commit, and run:

    python3 evals/ste_lint.py --self-test
    python3 -m unittest evals.test_run_pi_bench

Use `codex exec --ephemeral --ignore-user-config` in a disposable fixture. Do
not let a fixture create plans, tasks, implementation, or repository changes
outside its output file. Detailed results belong in
`.agent/test-results/pm-003.md`.

## Validation and Acceptance

The exact-copy install must match reviewed hashes and remain readable in a fresh
process. A missing skill must fail standard preflight. Update must be explicit.
Disable and uninstall must make the provider unavailable and preserve fixture
truth.

Each output must preserve all listed protected text byte for byte. The linter
self-test and unit tests must pass. Changed Markdown must lint, affected YAML
must parse, and the registry must retain the reviewed commit.

## Idempotence and Recovery

All provider and Codex targets are disposable. Recreate failed runs rather than
editing ambiguous output. Exact-copy recovery moves the prior directory aside
and copies the reviewed source again. Versioned fixture inputs remain unchanged.

## Artifacts and Notes

Durable provider facts belong in `upstream/reviews/simple-english.md`. Fixture
inputs and outputs belong under `conformance/simple-english/`. Repeated logs and
command exit states belong only in the ignored result file.

## Interfaces and Dependencies

Use the reviewed SimpleEnglish commit, its Python standard-library linter, and
the current Codex CLI. Add no repository dependency or executable interface.

Latest revision: 2026-08-11. PM-003 completed with exact-copy approval and
bounded preservation evidence.
