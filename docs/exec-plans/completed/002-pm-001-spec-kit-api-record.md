# Close the Spec Kit API record

<!-- markdownlint-disable MD013 MD046 -->

This ExecPlan is a living document. Maintain it according to
`.agent/PLANS.md`. Update `docs/roadmap.md` in the same change when PM-001
changes status.

## Purpose / Big Picture

Proofmill already has a current-valid preset, workflow, and bundle, but its
composition guide does not fully record the extension manifest or the trust
boundary between Spec Kit's default and community catalogs. After this task, a
reader can identify each current format, know what catalog placement does and
does not mean, and validate the unchanged standard composition against the
reviewed Spec Kit pin.

This task changes documentation only unless current source validation proves a
manifest mismatch. It must not add an extension, provider, runtime, catalog, or
new architecture.

## Bounded Work Packet

    profile: standard
    must_do:
      - inspect the pinned current Spec Kit extension and catalog sources
      - record the extension.yml 1.0 format and its installed effects
      - record default, community, and explicit catalog install policies
      - connect the boundary to the existing preset, workflow, bundle, and catalog record
      - preserve the reviewed Spec Kit commit and exact composition pins
      - update the roadmap and durable qualification record
    must_not_do:
      - add or enable an extension
      - publish a Proofmill catalog or release artifact
      - update Spec Kit or any provider pin
      - start PM-002, PM-003, PM-030, or the checkbook benchmark
      - add a runtime, adapter, daemon, database, or agent loop
    may_do:
      - correct documentation that conflicts with the pinned primary source
      - add a small manifest fixture only if native validation cannot exercise the format
    stop_when:
      - the four composition formats and catalog trust boundary are explicit
      - the unchanged standard composition validates with pinned Spec Kit
      - PM-001 is complete and PM-002 remains next

## Progress

- [x] (2026-08-11 22:00Z) Activated PM-001 and bounded it to the pinned API
      record and current composition documentation.
- [x] (2026-08-11 22:00Z) Inspected exact extension fields, catalog source
      policies, and current CLI behavior at the reviewed Spec Kit commit.
- [x] (2026-08-11 22:00Z) Updated the composition and upstream qualification
      records. No manifest or pin needed a change.
- [x] (2026-08-11 22:00Z) Ran YAML, Markdown, extension-install, and pinned
      Spec Kit composition validation with no failures.
- [x] (2026-08-11 22:00Z) Completed PM-001 and updated the roadmap. This plan is
      ready to archive under `docs/exec-plans/completed/`.

## Surprises & Discoveries

- Observation: The built-in catalog trust split is permission-based, not an
  assurance claim.
  Evidence: all current catalog list commands mark default sources
  install-allowed and community sources discovery-only; upstream notices say
  community source code is not audited or endorsed.
- Observation: The reviewed Spec Kit commit does not pin built-in HTTP catalog
  contents.
  Evidence: default and community catalog URLs use the upstream `main` branch.
- Observation: Extension installation has a wider write surface than its
  `extension.yml` directory.
  Evidence: the clean fixture wrote project registry and configuration state;
  current runtime events can also update native integration hook files.

## Decision Log

- Decision: Preserve commit
  `bd595cf838cc200f84fee9e9327b643dfe277d2c` and source version
  `0.16.3.dev0`.
  Rationale: PM-001 closes the API record for the already reviewed composition;
  it does not authorize an upstream update.
  Date/Author: 2026-08-11 / Codex with Ponytail.
- Decision: Call the default source upstream-maintained, not Proofmill-approved.
  Rationale: Spec Kit calls some default entries official and allows installation
  by ID, but Proofmill qualification and exact pins remain separate controls.
  Date/Author: 2026-08-11 / Codex with Ponytail.
- Decision: Change documentation only.
  Rationale: The current preset, workflow, and bundle validate at the reviewed
  pin. Adding a sample extension or catalog would create unused distribution
  surface and is outside PM-001.
  Date/Author: 2026-08-11 / Codex with Ponytail.
- Decision: Do not start the adversarial review cycle.
  Rationale: PM-001 changed documentation, the roadmap, and an execution plan
  only. Repository rules exclude these from meaningful code review.
  Date/Author: 2026-08-11 / Codex.

## Outcomes & Retrospective

PM-001 closed the API record. The extension schema and write surface are
documented beside presets, workflows, bundles, and catalogs. The default and
community source boundary is explicit, including the unpinned `main` URLs and
the rule that discovery or installation permission is not Proofmill approval.

No manifest, pin, provider, catalog, or runtime changed. The existing standard
composition still validates and installs with the reviewed Spec Kit source.
PM-002 remains next.

The source and fixture observations did not start an adversarial review cycle.
The simple-and-relevant finding challenge applies only to findings reported by
fresh clean-context adversarial review subagents.

## Context and Orientation

`docs/SPEC-KIT-COMPOSITION.md` records the preset, workflow, bundle, and
catalog formats consumed by Proofmill. `upstream/reviews/github-spec-kit.md`
records the pinned upstream identity and lifecycle behavior.
`presets/proofmill-contract/preset.yml`,
`workflows/proofmill-standard/workflow.yml`, and
`bundles/proofmill-standard/bundle.yml` are the current composition manifests.

An extension is a Spec Kit component rooted at `extension.yml`. It can declare
agent commands, replacement templates and scripts, configuration templates,
and lifecycle hooks. A catalog is a JSON discovery index. A catalog source has
an installation policy. `install-allowed` permits installation by component ID;
`discovery-only` permits search and inspection but not installation by ID.

The pinned source has separate default and community catalogs for extensions,
presets, workflows, workflow steps, and bundles. Default catalogs contain
upstream-maintained entries and are install-allowed. Community catalogs contain
third-party entries and are discovery-only. Format validation or a `verified`
field is not a Proofmill qualification.

## Plan of Work

First, read the extension API reference, template manifest, catalog stack code,
and community notices at the pinned Spec Kit commit. Record exact schema fields
and policy behavior, not names inferred from the Proofmill starter files.

Second, revise `docs/SPEC-KIT-COMPOSITION.md` so its preset, workflow, bundle,
extension, and catalog sections form one current API record. Revise
`upstream/reviews/github-spec-kit.md` only where the provider review needs the
same trust boundary. Keep the current manifests unchanged unless native
validation proves they are invalid.

Finally, parse all affected YAML, lint changed Markdown, and install the local
preset and workflow in a disposable pinned Spec Kit fixture. Validate and
install the bundle there. Because this task is documentation-only, do not start
an adversarial code-review cycle.

## Milestones

The source milestone ends when the exact extension manifest shape and catalog
policy stack are known from the pinned source. The evidence is a concise source
record with the default and community install behavior.

The documentation milestone ends when a reader can follow the relationship
from each Proofmill component to its Spec Kit format and can tell catalog
discovery from Proofmill approval.

The validation milestone ends when changed Markdown has no lint findings,
affected YAML parses, and a fresh pinned Spec Kit fixture accepts the unchanged
local preset, workflow, and bundle.

## Concrete Steps

Work from `/home/mbeutler/Projects/proofmill`. Confirm the reviewed source:

    git -C /tmp/proofmill-pm026.zl2kRq/spec-kit rev-parse HEAD
    /tmp/proofmill-speckit-venv/bin/specify version --features --json

Inspect these pinned source files:

    extensions/EXTENSION-API-REFERENCE.md
    extensions/template/extension.yml
    extensions/catalog.json
    extensions/catalog.community.json
    src/specify_cli/extensions/__init__.py
    src/specify_cli/presets/__init__.py
    src/specify_cli/workflows/catalog.py
    src/specify_cli/bundler/models/catalog.py

Keep command results in `.agent/test-results/pm-001.md`. Use a disposable
directory under `/tmp` for installation validation. Do not initialize Spec Kit
inside the Proofmill checkout.

## Validation and Acceptance

Acceptance requires the composition guide to state the `extension.yml` schema,
the declared command, template, script, config, hook, tag, and default surfaces,
and the install effects. It must state that default catalog sources are
install-allowed, community sources are discovery-only, and neither community
listing nor metadata validation is an audit or approval.

The reviewed commit and all Proofmill component pins must stay unchanged. The
local preset, workflow, and bundle must install or validate in a fresh fixture.
All changed Markdown must pass the existing markdownlint command. All affected
YAML must parse.

## Idempotence and Recovery

Source inspection is read-only. Fixture directories are disposable. Recreate a
fixture instead of repairing uncertain local state. Documentation edits can be
reapplied without changing the composition. If validation exposes a current
manifest mismatch, record it before making the smallest necessary correction.

## Artifacts and Notes

The durable API record belongs in `docs/SPEC-KIT-COMPOSITION.md`. Provider trust
and catalog failure behavior belong in `upstream/reviews/github-spec-kit.md`.
Detailed commands and repeat results belong only in the ignored
`.agent/test-results/pm-001.md` file.

## Interfaces and Dependencies

Use Spec Kit source version `0.16.3.dev0` at commit
`bd595cf838cc200f84fee9e9327b643dfe277d2c`. Use its schema 1.0 manifests and
native CLI. Add no dependency and define no Proofmill executable interface.

Latest revision: 2026-08-11. PM-001 completed after source, documentation, and
pinned composition validation; no executable change was needed.
