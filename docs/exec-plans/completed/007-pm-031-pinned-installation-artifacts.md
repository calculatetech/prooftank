# Publish pinned Codex installation artifacts

<!-- markdownlint-disable MD013 MD046 -->

This ExecPlan is a living document. Maintain it according to
`.agent/PLANS.md` and update `docs/roadmap.md` with PM-031 status.

## Purpose / Big Picture

The current Codex install uses a Proofmill source checkout plus exact upstream
clones. A user can reproduce the pins, but Proofmill does not yet publish one
versioned local release path. This task creates the smallest installable Codex
release that carries reviewed bytes for the contract preset, standard workflow,
Ponytail, and SimpleEnglish without following any default branch.

## Bounded Work Packet

    profile: standard
    must_do:
      - confirm all four reviewed source identities from current primary sources
      - use current native Spec Kit package and catalog formats
      - publish one versioned local Codex release path
      - include exact component identity and archive checksums
      - install every component into a clean target without a mutable branch
      - validate health, missing-provider failure, disable, and uninstall safety
      - keep the roadmap and installation guidance current
    must_not_do:
      - publish a remote release, package, or catalog
      - add an installer runtime, custom package manager, or adapter protocol
      - include Claude, OpenCode, Pi, OpenHarness, or cross-harness metadata
      - start the checkbook benchmark or a critical profile
      - claim an archive checksum proves provider output
    may_do:
      - use a versioned repository release directory instead of a hosted catalog
      - use native Spec Kit archives plus normalized provider-skill archives
    stop_when:
      - a clean Codex target installs and validates only from versioned artifacts
      - no install step follows an upstream default branch
      - disable and uninstall preserve repository truth

## Progress

- [x] (2026-08-12 00:22Z) Activated PM-031 after non-Codex harness work was
      postponed.
- [x] (2026-08-12 00:31Z) Confirmed current upstream identities and native
      component interfaces. Spec Kit upstream moved beyond the reviewed pin.
- [x] (2026-08-12 00:42Z) Built the versioned local release from native component
      directories, exact provider bytes, license notices, and checksums.
- [x] (2026-08-12 00:51Z) Installed and exercised the release in a clean Codex
      target with external network routes unavailable after the prerequisite.
- [x] (2026-08-12 00:51Z) Updated durable records and passed repository
      validation.
- [x] (2026-08-12 01:19Z) Completed three clean-context adversarial review
      cycles and resolved every in-scope finding.
- [x] (2026-08-12 01:33Z) Narrowed SimpleEnglish compatibility metadata to
      Codex, validated the one-line derivation, and completed PM-031.

## Surprises & Discoveries

- Observation: Spec Kit upstream `HEAD` moved to
  `7dd706880e73cd05ccda95fb8d5ce6cf2d652ae4`.
  Evidence: The qualified release stays on reviewed commit
  `bd595cf838cc200f84fee9e9327b643dfe277d2c`; updating it needs separate
  qualification.
- Observation: Current Spec Kit accepts local workflow archives but its preset
  CLI accepts local directories or remote archives, not local archives.
  Evidence: `preset add --dev` requires a directory, while `workflow add --dev`
  accepts either shape.
- Observation: Native directory installs copy their component files into the
  target and remain healthy when the release directory is temporarily absent.
  Evidence: Preset resolution and workflow inspection passed after moving the
  staged release path away.
- Observation: Upstream SimpleEnglish declares compatibility with multiple
  harnesses.
  Evidence: The final review found that metadata in the Codex release. The
  installed skill now changes only that line to `compatibility: codex`; its
  instruction body and references remain upstream bytes.

## Decision Log

- Decision: Prefer a versioned local release path over a remote catalog.
  Rationale: The repository has no authorized remote publication target. Local
  artifacts can prove immutable installation without inventing hosting or
  claiming an unpublished URL works.
  Date/Author: 2026-08-12 / Codex.
- Decision: Publish inspectable component directories, not archives or an
  installer.
  Rationale: Both components already have native local-directory installation.
  Directories keep checksummed provider and license bytes visible and avoid a
  custom extraction step.
  Date/Author: 2026-08-12 / Codex.
- Decision: Normalize SimpleEnglish compatibility metadata for the MVP.
  Rationale: Codex is the only supported MVP harness. The release records both
  the upstream hash and the installed derived hash.
  Date/Author: 2026-08-12 / Codex.

## Outcomes & Retrospective

PM-031 is complete. Release `0.1.0` installs the pinned preset, Codex-only
workflow, Ponytail, and Codex-normalized SimpleEnglish from one checksummed
directory. It uses native Spec Kit commands and adds no Proofmill runtime.

## Context and Orientation

Spec Kit is pinned at commit
`bd595cf838cc200f84fee9e9327b643dfe277d2c`, source version `0.16.3.dev0`.
`presets/proofmill-contract/` and `workflows/proofmill-standard/` are the local
Proofmill components. `upstream/registry.yml` pins Ponytail commit
`2ed6c52c9d7e5e56942508591085fd45dea277d3` and SimpleEnglish commit
`59bf6702197a5aadc96d197ea17f290d8d50dcd3`, with reviewed skill hashes.

The standard bundle cannot embed local component directories or agent skills.
Spec Kit can build and install its own component archives. Provider skills are
ordinary directories containing `SKILL.md` and references. A release path must
retain these ownership boundaries instead of adding a Proofmill installer.

## Plan of Work

Inspect current upstream heads and the pinned Spec Kit CLI help and source for
preset, workflow, bundle, and catalog archive support. Use the highest native
format that installs from local immutable files. If Spec Kit cannot package
provider skills, create normalized archives containing only their reviewed skill
directories and license files. Record archive SHA-256 values in one versioned
manifest.

Create one release directory under `releases/proofmill-standard/0.1.0/`. Keep it
small: native Proofmill component archives, exact provider-skill archives, a
machine-readable manifest, checksums, and concise install guidance. Do not add
an executable installer unless native commands cannot complete the install.

Create a clean disposable Codex project. Install from the release directory
with network disabled after artifact creation. Verify exact bytes, resolve the
contract, inspect the workflow, exercise both missing-provider failures, and
confirm disable and uninstall preserve a reference specification.

Update `docs/SPEC-KIT-COMPOSITION.md`, bundle guidance, the gap report, roadmap,
and this plan. Run relevant package, YAML, Markdown, shell, and clean-install
checks. Because installation configuration is meaningful, obtain a fresh
read-only adversarial review before task completion.

## Milestones

The format milestone ends when native build and install commands are proven in
a disposable experiment. The publication milestone ends when every versioned
artifact has an exact checksum and no mutable source. The lifecycle milestone
ends when a clean Codex target passes install, health, failure, disable, and
uninstall checks. The record milestone ends when review and validation pass and
PM-031 is archived.

## Concrete Steps

Work from `/home/mbeutler/Projects/proofmill`. Use
`/tmp/proofmill-speckit-venv/bin/specify` at the reviewed commit. Inspect command
help before building:

    specify preset --help
    specify workflow --help
    specify bundle --help

Use fresh upstream checkouts or exact commit archives for provider bytes. Keep
detailed commands, generated file lists, checksums, and exit states only in
`.agent/test-results/pm-031.md`.

## Validation and Acceptance

A clean target must install the preset, workflow, and both provider skills from
files under `releases/proofmill-standard/0.1.0/`. After artifact creation, no
step may contact GitHub, npm, a Spec Kit catalog, or a default branch. Installed
provider files must match reviewed hashes. Pinned Spec Kit must resolve the
contract and report the standard workflow.

Removing one provider at a time must stop provider preflight with its exact
name. Removing the release components and Codex integration must preserve a
reference specification. Changed Markdown must lint, YAML and JSON must parse,
archive contents and checksums must match, and `git diff --check` must pass.

## Idempotence and Recovery

Build into a disposable directory before replacing versioned artifacts. A
failed clean install can be discarded and recreated. Never update an existing
release directory in place after publication; a changed byte requires another
version. During this task, version `0.1.0` remains unpublished and can be
rebuilt until final validation completes.

## Artifacts and Notes

Published local artifacts belong under `releases/proofmill-standard/0.1.0/`.
Durable format facts belong in `docs/SPEC-KIT-COMPOSITION.md`. Detailed command
results belong only in `.agent/test-results/pm-031.md`.

## Interfaces and Dependencies

Use pinned Spec Kit, standard archive tools, SHA-256, and the exact reviewed
provider directories. Add no dependency, service, daemon, database, or custom
runtime.

Latest revision: 2026-08-12. PM-031 is complete and validated for Codex only.
