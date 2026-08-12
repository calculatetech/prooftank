# Rename the project to ProofTank

<!-- markdownlint-disable MD013 MD046 -->

This ExecPlan is a living document. Maintain it according to
`.agent/PLANS.md` and keep `docs/roadmap.md` current.

## Purpose / Big Picture

The repository is already published at `calculatetech/prooftank`, but its
current product files still use the rejected Proofmill name. After this task,
new users install `prooftank-standard`, select `prooftank-contract`, and follow
ProofTank documentation. The immutable Proofmill `0.1.0` release and frozen
benchmark evidence remain available as historical records.

## Bounded Work Packet

    profile: standard
    must_do:
      - rename current human-facing product references to ProofTank
      - rename current policy, preset, workflow, bundle, and skill identifiers
      - publish a checksummed replacement release without changing 0.1.0
      - update current documentation and local links before commit
      - prove install, validation, Codex dry run, disable, and uninstall
      - preserve historical benchmark and completed-plan evidence
    must_not_do:
      - rewrite frozen benchmark candidates, reports, or first-result metadata
      - alter the contents or checksums of release 0.1.0
      - add a runtime, dependency, provider, harness, profile, or feature
      - claim trademark clearance or a general quality advantage
    may_do:
      - preserve historical uses of Proofmill where exact old identifiers matter
      - add short migration notes from 0.1.0 to the replacement
    stop_when:
      - only intentional historical Proofmill references remain
      - the replacement release passes the Codex lifecycle checks

## Progress

- [x] (2026-08-12) Activated PM-036 after completing the quality benchmark.
- [x] (2026-08-12) Inventoried current identifiers and immutable historical exceptions.
- [x] (2026-08-12) Renamed the live composition and current documentation.
- [x] (2026-08-12) Built and checksummed replacement release `0.2.0`.
- [x] (2026-08-12) Validated install, Codex dry run, disable, uninstall, tests, lint, links, and checksums.
- [x] (2026-08-12) Completed the three-cycle adversarial review cap and fixed
  every simple, relevant finding.
- [x] (2026-08-12) Prepared the reviewed, validated scope for commit, push, and
  required CI monitoring.

## Surprises & Discoveries

- Observation: The public repository already uses the accepted working name.
  Evidence: The configured remote points to `calculatetech/prooftank`.
- Observation: The first Codex dry-run attempt used a read-only sandbox and
  could not create artifacts.
  Evidence: The attempt stopped before artifacts existed. The accepted run used
  workspace-write, exited successfully, and created only the required spec and
  checklist.
- Observation: The historical benchmark arm was Proofmill Standard `0.1.0`,
  not the renamed ProofTank Standard `0.2.0` release.
  Evidence: The frozen mapping and source manifest identify
  `proofmill-standard`; current docs now limit `0.2.0` to lifecycle
  qualification.

## Decision Log

- Decision: Preserve release `0.1.0` and frozen benchmark identifiers byte for byte.
  Rationale: They are content-addressed historical evidence. Renaming them would
  invalidate checksums and the completed comparison.
  Date/Author: 2026-08-12 / Codex.
- Decision: Use `0.2.0` for the first ProofTank-named release.
  Rationale: Machine-visible package and composition identifiers change, so the
  replacement must be distinguishable from the immutable `0.1.0` artifact.
  Date/Author: 2026-08-12 / Codex.

## Outcomes & Retrospective

The live composition and current documentation use ProofTank. Release `0.2.0`
passes install, health, one Codex specification dry run, provider disable, and
uninstall. Historical release `0.1.0` matches its pre-migration hashes. Three
fresh clean-context review cycles found bounded sandbox, evidence-integrity,
lifecycle-command, and naming gaps. Every finding was challenged as simple and
relevant, every gap was repaired, and the review stopped at the required cap.

## Context and Orientation

`prooftank.yml` is the current product policy. `presets/prooftank-contract/`,
`workflows/prooftank-standard/`, `bundles/prooftank-standard/`, and
`skills/prooftank/` are the live composition sources. The release under
`releases/proofmill-standard/0.1.0/` is immutable. Completed execution plans,
the checkbook arm named `proofmill-standard`, and frozen result files describe
the old experiment and keep their exact names.

## Plan of Work

First, hash release `0.1.0` and record the digest set. Rename only live source
paths and update their internal identifiers. Rename current explanatory docs and
links while retaining explicit historical statements where readers need the old
name to locate evidence.

Next, create `releases/prooftank-standard/0.2.0/` from the renamed live sources.
Update its release metadata, install paths, removal paths, license filename, and
checksums. Do not modify the old release.

Finally, install the new release into an isolated temporary Codex home and
temporary repository. Validate the preset and workflow, run the same bounded
Codex specification dry run used for qualification, then prove disable and
uninstall. Run repository tests and lint. A fresh clean-context adversarial
review is required because paths, workflow configuration, and release metadata
are meaningful runtime and build changes.

## Milestones

The live-source milestone ends when every current path and identifier uses
ProofTank and only historical evidence retains Proofmill. The release milestone
ends when `0.2.0` installs without the old product path. The lifecycle milestone
ends when one Codex dry run produces its required specification artifacts and
disable plus uninstall leave project truth intact.

## Concrete Steps

Work from `/home/mbeutler/Projects/proofmill`. Use `apply_patch` for content
edits and explicit `mv` operations for renames. Record repeated command output
in `.agent/test-results/pm-036.md`.

Run focused Python tests and Ruff checks for changed executable files. Parse all
YAML and JSON, run authored Markdown lint, verify local links, compile Python,
verify both release checksum manifests, and run `git diff --check`. Compare the
old release hashes before and after the migration.

## Validation and Acceptance

The replacement is accepted when its documented install command creates only
ProofTank-named composition files and the exact pinned provider files, its health
check succeeds, and one Codex dry run creates the specified repository
artifacts. Disable and uninstall must remove the installed composition while
leaving repository specifications and evidence intact. Every `Proofmill` or
`proofmill` match outside frozen history must be either removed or documented as
an intentional migration reference.

## Idempotence and Recovery

Use temporary directories for lifecycle tests. A failed replacement build may
delete only its exact `releases/prooftank-standard/0.2.0/` directory and rebuild
it from live sources. Never alter or delete `releases/proofmill-standard/0.1.0/`.

## Artifacts and Notes

The replacement release, migration guidance, validation conclusions, and
remaining historical-name inventory are durable. Raw dry-run logs and repeated
test output remain ignored under `.agent/`.

## Interfaces and Dependencies

Use existing Spec Kit, Ponytail, SimpleEnglish, shell, Python standard library,
and repository validation commands. Add no package or service. The new public
identifiers are `ProofTank`, `prooftank.yml`, `prooftank-contract`,
`prooftank-standard`, and `skills/prooftank`.

Latest revision: 2026-08-12. PM-036 implementation, lifecycle validation, and
the required three-cycle adversarial review are complete. The validated scope
is ready for publication without further documentation edits.
