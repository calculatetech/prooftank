# Proofmill Roadmap

This file is the source of truth for product work and progress. Task identifiers
are permanent. The original backlog items keep their numbers as `PM-001` through
`PM-029`. New work starts at `PM-030`. Never reuse or renumber an identifier.

Move a task when its status changes. Keep no more than one task active. Update
this file in the same change that starts, completes, reorders, adds, or removes
product work. Execution plans can add detail, but they do not own roadmap status.

Status legend:

- 🎯 **Active** — currently being implemented
- ⏭ **Planned next** — accepted and ordered for near-term delivery
- ◻ **Planned later** — accepted but not yet scheduled
- ⏸ **Postponed** — intentionally removed from the active delivery path
- ✅ **Completed** — implemented and validated

## Active

No tasks are currently active.

## Planned next

- ⏭ **PM-036 — Rename Proofmill to ProofTank.** Migrate human-facing names,
  machine identifiers, paths, presets, workflows, policy, release metadata, and
  checksum manifests as one bounded change. Preserve the current `0.1.0`
  artifact until the replacement installs and passes a Codex dry run.

## Postponed

- ⏸ **PM-007 — Add Claude Code conformance.** Source, integration, provider
  failure, dispatch, and uninstall checks passed. The model-backed run is
  postponed because the project has no Claude subscription.
- ⏸ **PM-008 — Add OpenCode conformance.** Postponed while Proofmill focuses on
  Codex.
- ⏸ **PM-009 — Add Pi conformance.** Postponed while Proofmill focuses on Codex.
- ⏸ **PM-010 — Normalize conformance results.** Postponed until another harness
  has a completed model-backed run.
- ⏸ **PM-024 — Add OpenHarness conformance.** Postponed while Proofmill focuses
  on Codex.
- ⏸ **PM-033 — Design `proofmill-critical`.** Postponed because the bootstrap
  prohibits a critical-profile workflow and its research providers are blocked.

## Planned later

No tasks are currently planned later.

## Completed

- ✅ **PM-035 — Clear the product and package names.** `Proofmill` was rejected
  after finding an active Python CLI with the same product, distribution, and
  command name. The owner accepted `ProofTank` for this open-source hobby
  project after a clean bounded collision screen. The public repository is
  `calculatetech/prooftank`; PM-036 owns the identifier migration.
- ✅ **PM-034 — Prepare the public pilot.** One Codex-only local pilot guide
  points to the checksummed release procedure, qualification and benchmark
  evidence, explicit limitations, provider contribution and replacement rules,
  feedback requirements, and exact lifecycle guidance.
- ✅ **PM-029 — Publish the measured build-versus-integrate decision.** The MVP
  provider set is closed around Codex, Spec Kit, Ponytail, SimpleEnglish, and
  native checks. Blocked and comparison-only candidates remain visible. The
  benchmark supports no quality-gain claim and authorizes no runtime code.
- ✅ **PM-028 — Decide whether a provider-health extension is necessary.** No
  extension is authorized. Exact provider versions, hashes, source tests,
  workflow preflight, lifecycle commands, and explicit unknowns cover the MVP.
- ✅ **PM-027 — Decide whether a release-warrant extension is necessary.** No
  extension is authorized. The benchmark exposed no release failure, and the
  qualified gate candidate creates false success when coverage is absent.
  Native tests, lint, checksums, and explicit unknowns remain the controls.
- ✅ **PM-025 — Add sustainability review.** Pinned `harnesses.json` is an
  approved manual maintenance signal. It can trigger a primary-source review,
  but cannot change pins, qualification, or the Codex-only MVP. No MCP server,
  updater, schedule, credential, or runtime was added.
- ✅ **PM-023 — Pilot ADHD for the same critical design.** Release `v0.1.4` is
  pinned and blocked. Its Codex skill requires parallel isolated agents that
  conflict with the one-subagent rule, while its CLI requires Claude. Fresh
  clean-context Codex review remains the bounded fallback.
- ✅ **PM-022 — Pilot NeuroArxiv for a critical design.** Current source is
  pinned for traceability and blocked. No release exists, the CLI requires the
  Claude Agent SDK, and its installer writes only a Claude skill. Manual
  primary-source research remains the Codex fallback.
- ✅ **PM-021 — Pilot Cavemem as advisory memory.** Release `v0.2.1` is pinned
  and blocked. Useful retrieval requires the persistent SQLite memory system
  prohibited by the MVP, and its released Codex installer writes an obsolete
  configuration shape. Repository docs and Git remain the fallback.
- ✅ **PM-020 — Pilot CBM as an observational provider.** Current release
  `v0.10.2` is pinned and blocked. Its first useful operation creates the code
  graph and SQLite state prohibited by the MVP; MCP use also starts a daemon.
  No provider binary ran, and native repository tools remain the fallback.
- ✅ **PM-019 — Run the first benchmark.** All five frozen Codex arms completed.
  Every unchanged implementation passed 15 of 15 contract-aligned scenarios.
  Ponytail-only led measured efficiency; Proofmill added no quality gain.
- ✅ **PM-018 — Add benchmark metrics and result preservation.** One
  standard-library controller prepares isolated arms, audits input parity,
  preserves failures, runs the external suite, and records JSON metrics with
  unavailable values kept distinct from zero.
- ✅ **PM-017 — Create the Proofmill Standard arm.** The arm uses release
  `0.1.0` and only its qualified Codex providers.
- ✅ **PM-016 — Create the Spec Kit core arm.** The arm uses the pinned core
  integration without Proofmill components or provider skills.
- ✅ **PM-015 — Create the Cavekit-plus-Ponytail arm.** Cavekit `4.1.0` is pinned,
  reviewed, and vendored as a comparison-only Codex input beside Ponytail.
- ✅ **PM-014 — Create the Ponytail-only arm.** The arm adds only the approved
  exact Ponytail skill and its minimality instruction.
- ✅ **PM-013 — Create the bare-agent arm.** The arm contains only the frozen
  brief, prompt, empty repository shape, and common runner.
- ✅ **PM-012 — Build the external hidden suite.** Fifteen external scenarios
  pass against a private reference and reject an incomplete fixture. Arm
  repositories receive none of the hidden files.
- ✅ **PM-011 — Freeze the checkbook brief.** The public Python and SQLite
  contract, common prompt, Codex runner, controls, success rules, and exact
  hashes are frozen before any arm starts.
- ✅ **PM-032 — Design `proofmill-lite`.** The Codex-only design preserves a
  bounded packet, Ponytail, focused regression, native tests and lint, explicit
  unknowns, and risk escalation without creating an unused composition.
- ✅ **PM-031 — Publish pinned installation artifacts.** Release `0.1.0` installs
  the exact preset, Codex-only workflow, Ponytail, and Codex-normalized
  SimpleEnglish from one checksummed local directory without a custom runtime.
- ✅ **PM-030 — Requalify the corrected Codex contract.** One fresh pinned
  Codex run created only a specification and checklist, carried the full
  Proofmill contract into checklist review, and kept missing executable coverage
  and human inspection `unknown`.
- ✅ **PM-003 — Close SimpleEnglish qualification.** The exact-copy three-file
  Codex skill passed clean install, restart, explicit update, unavailable,
  disable, reinstall, and uninstall checks. Four bounded rewrites preserved all
  listed technical text byte for byte; the mutable `npx` path remains
  unapproved.
- ✅ **PM-002 — Close Ponytail qualification.** The exact-copy main skill passed
  clean install, restart, explicit update, unavailable, disable, reinstall, and
  uninstall checks. It is approved as advisory at its exact commit and byte
  hash; the mutable marketplace path remains unapproved.
- ✅ **PM-001 — Close the Spec Kit API record.** The schema 1.0 extension
  surface, install effects, default install-allowed catalogs, community
  discovery-only catalogs, and catalog trust limits are documented. The
  reviewed Spec Kit pin and standard composition are unchanged and validated.
- ✅ **PM-026 — Qualify the smallest deterministic gate.** The exact current
  candidate screen is preserved. The leading `gates` release passed its own
  suite but allowed missing executable coverage to pass, left projected runtime
  active after disable and uninstall, and carried vulnerable locked
  dependencies. No provider or new Proofmill runtime was added.
- ✅ **PM-004 — Create the Proofmill contract preset.** The current Spec Kit
  preset adds the standard profile, bounded scope, stable requirement and
  invariant IDs, failures, evidence, and explicit unknowns without copying core
  templates.
- ✅ **PM-005 — Create the Proofmill Standard workflow.** The current workflow
  uses native Spec Kit steps, stops on missing required skills, reviews the
  contract and work packet, runs core analysis and convergence, and adds no
  Proofmill runtime.
- ✅ **PM-006 — Package `proofmill-standard` for Codex.** Exact source pins,
  qualification records, a local preset, workflow, bundle, install and uninstall
  guidance, negative provider fixtures, and one bounded Codex dry run are
  validated. The completed run exposed the evidence gap tracked by `PM-026` and
  `PM-030`.
