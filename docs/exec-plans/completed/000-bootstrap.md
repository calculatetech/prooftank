# Bootstrap Proofmill Standard for Codex

<!-- markdownlint-disable MD013 MD046 -->

This ExecPlan is a living document. Maintain it according to `.agent/PLANS.md`.

## Purpose / Big Picture

This milestone creates the smallest current-valid `proofmill-standard`
composition. A user can install a Proofmill contract preset and standard
workflow into a Spec Kit Codex project. One Codex dry run shows that the preset
adds a bounded contract to the generated feature specification.

Stop before the checkbook benchmark, cross-harness conformance, optional
provider pilots, and the critical profile.

## Bounded work packet

```yaml
profile: standard
must_do:
  - qualify GitHub Spec Kit, Ponytail, and SimpleEnglish at exact commits
  - create a current Spec Kit preset, workflow, and local bundle
  - prove one Codex specification-only dry run
  - preserve failures, unknowns, and rejected extension candidates
must_not_do:
  - build a daemon, database, agent loop, code graph, memory store, or MCP
    aggregator
  - build the checkbook application or a cross-harness runner
  - enable an unqualified community extension or critical-profile provider
  - create a release warrant or provider-health runtime
may_do:
  - use core Spec Kit analysis and convergence commands
  - add declarative templates and manifests
  - reject or reduce the proposed composition
stop_when:
  - current formats validate with the reviewed Spec Kit CLI
  - exact provider pins and qualification records exist
  - one Codex dry run produces a specification and checklist only
  - optional-provider absence is visible and repository truth survives uninstall
  - the gap report recommends proceed, revise, or stop
required_checks:
  - Spec Kit install, schema, malformed-input, disable, and uninstall checks
  - Ponytail upstream tests
  - SimpleEnglish self-test and unit tests
  - Markdown and YAML lint
known_unknowns:
  - no community extension has a source-level qualification in this milestone
providers:
  used:
    - github-spec-kit
    - ponytail
    - simple-english
  unavailable: []
  degraded: []
```

## Progress

- [x] (2026-08-11 19:05Z) B001 resolved Spec Kit commit, license, composition
      formats, and Codex integration behavior.
- [x] (2026-08-11 19:14Z) B002 screened current catalog candidates for
      traceability, verification, architecture, quality gates, and evidence.
- [x] (2026-08-11 19:21Z) B003-B005 wrote qualification records for Spec Kit,
      Ponytail, and SimpleEnglish.
- [x] (2026-08-11 19:31Z) B006-B011 created and installed the preset, workflow,
      and local bundle. Missing-provider and uninstall behavior stayed visible
      and safe.
- [x] (2026-08-11 19:34Z) B012 completed one Codex specification-only dry run.
- [x] (2026-08-11 19:38Z) B013 wrote the composition reference and gap report.
- [x] (2026-08-11 19:48Z) Completed schema, lint, and one fresh adversarial
      review. Corrected provider status, installation safety, and the dry-run
      evidence claim.
- [x] (2026-08-11 20:03Z) Review cycle 2 found an advisory provider gate. The
      native shell step now stops on either missing skill before creating a
      specification. This finding triggered review cycle 3.
- [x] (2026-08-11 20:09Z) Review cycle 3 found no composition or fixture defect.
      Its one documentation finding added the exact Spec Kit source install to
      the consumer guide. All final validation passed.

## Surprises & Discoveries

- Observation: Current local bundles do not install custom component folders
  that sit beside `bundle.yml`. Evidence: The supported install added the preset
  and workflow first. Bundle install then reported `0 added, 2 already present`.
- Observation: Bundle install skips a component that already exists by ID.
  Evidence: Current bundle documentation says that install-time idempotency does
  not compare the installed version.
- Observation: Ponytail's root test command has an undeclared benchmark setup
  dependency. Evidence: The first run passed 83 of 84 core tests and failed the
  CSV case. The documented `pandas` dependency made all tests pass.
- Observation: The community catalog marks the inspected candidates as
  unverified. Evidence: Each selected catalog entry had `verified: false`.
- Observation: The Codex dry run composed the preset but called human inspection
  deterministic evidence. Evidence: Its `Evidence` field named inspection and
  its `Unknowns` field said `None`.
- Observation: Spec Kit bundles cannot install Codex skills. Evidence: The two
  required provider skills needed separate exact-copy installation.
- Observation: Spec Kit's native workflow shell step can enforce provider
  presence without a Proofmill runtime. Evidence: Both missing-provider fixtures
  failed at step zero and created no `specs/` directory.

## Decision Log

- Decision: Use Spec Kit main commit `bd595cf838cc200f84fee9e9327b643dfe277d2c`
  instead of release `v0.16.2`. Rationale: Current bundle and Codex skill
  behavior in the requested primary source is `0.16.3.dev0`. The composition
  pins that exact source. Date/Author: 2026-08-11 / Codex.
- Decision: Append three Proofmill sections to core templates. Rationale: Core
  owns the full template. Append composition adds the contract without copying
  upstream content. Date/Author: 2026-08-11 / Codex with Ponytail.
- Decision: Enable no community extension. Rationale: Catalog metadata is
  discovery evidence, not qualification. Core analysis plus project-native
  checks is the smallest safe pilot. Date/Author: 2026-08-11 / Codex.
- Decision: Recommend revision before the benchmark. Rationale: The composition
  works, but it has no qualified deterministic traceability or evidence gate.
  Date/Author: 2026-08-11 / Codex.
- Decision: Keep Ponytail and SimpleEnglish at `pilot`. Rationale: Their exact
  sources and basic behavior were tested, but the required update and complete
  host lifecycle matrix was not. Date/Author: 2026-08-11 / Codex.

## Outcomes & Retrospective

The bootstrap produced a valid Spec Kit preset, workflow, and local bundle. A
Codex dry run created `spec.md`, `checklists/requirements.md`, and the current
feature pointer. It created no plan, tasks, application code, or runtime.

The run also exposed a gap: agent-generated inspection was mislabeled as
deterministic evidence. The preset now requires an executable command or an
explicit `unknown`. That correction needs a future qualification run.

The composition keeps Spec Kit as the only specification owner. Ponytail and
SimpleEnglish remain provider skills. The gap report recommends revision before
the checkbook benchmark.

## Context and Orientation

GitHub Spec Kit owns the specification process. `presets/proofmill-contract/`
adds the Proofmill contract to core Spec Kit templates.
`workflows/proofmill-standard/` sequences core commands with human review gates.
`bundles/proofmill-standard/` pins those two components for Codex.

`upstream/registry.yml` records active and backlog providers. Detailed active
provider reviews are under `upstream/reviews/`. `docs/SPEC-KIT-COMPOSITION.md`
records current formats. `docs/BOOTSTRAP-GAP-REPORT.md` records capability gaps
and rejected candidates.

## Plan of Work

Inspect exact current upstream commits before editing. Read the current schemas
and integration code. Add only declarative Spec Kit artifacts. Install them in a
disposable Codex fixture. Run one specification-only Codex session. Remove the
composition and make sure that the feature artifacts remain. Record all findings
and stop.

## Milestones

The first milestone qualifies the three active upstream sources. It ends when
their exact commits, licenses, effects, failure behavior, fallback, trust, and
tested lifecycle limits are visible in `upstream/reviews/` and
`upstream/registry.yml`.

The second milestone composes only current Spec Kit artifacts. It ends when the
preset, workflow, and bundle validate and install in a separate disposable Codex
project. No Proofmill executable exists.

The third milestone runs Codex once for specification only. It ends when the
fixture contains a feature specification, checklist, and feature pointer but no
plan, tasks, or implementation. Any false evidence claim is a gap, not a pass.

## Concrete Steps

Run these commands from `/home/mbeutler/Projects/proofmill`. They reproduce the
sources and composition without initializing this source tree:

    proofmill_source=$(pwd)
    upstream_root=$(mktemp -d /tmp/proofmill-upstreams.XXXXXX)
    git clone https://github.com/github/spec-kit.git "$upstream_root/spec-kit"
    git -C "$upstream_root/spec-kit" checkout --detach bd595cf838cc200f84fee9e9327b643dfe277d2c
    git clone https://github.com/DietrichGebert/ponytail.git "$upstream_root/ponytail"
    git -C "$upstream_root/ponytail" checkout --detach 2ed6c52c9d7e5e56942508591085fd45dea277d3
    git clone https://github.com/AminBlg/SimpleEnglish.git "$upstream_root/simple-english"
    git -C "$upstream_root/simple-english" checkout --detach 59bf6702197a5aadc96d197ea17f290d8d50dcd3
    speckit_venv=$(mktemp -d /tmp/proofmill-speckit-venv.XXXXXX)
    python3 -m venv "$speckit_venv"
    "$speckit_venv/bin/pip" install "$upstream_root/spec-kit"
    "$speckit_venv/bin/specify" version --features --json

Expect version `0.16.3.dev0`. Create a separate fixture and install the local
components and exact-copy skills:

    fixture=$(mktemp -d /tmp/proofmill-fixture.XXXXXX)
    cd "$fixture"
    "$speckit_venv/bin/specify" init --here --integration codex --force --ignore-agent-tools --script sh
    "$speckit_venv/bin/specify" preset add --dev "$proofmill_source/presets/proofmill-contract" --priority 10
    "$speckit_venv/bin/specify" workflow add --dev "$proofmill_source/workflows/proofmill-standard"
    mkdir -p .agents/skills
    cp -R "$upstream_root/ponytail/skills/ponytail" .agents/skills/ponytail
    cp -R "$upstream_root/simple-english/skills/simple-english" .agents/skills/simple-english
    test -f .agents/skills/ponytail/SKILL.md
    test -f .agents/skills/simple-english/SKILL.md
    "$speckit_venv/bin/specify" bundle validate --path "$proofmill_source/bundles/proofmill-standard" --offline
    "$speckit_venv/bin/specify" bundle install "$proofmill_source/bundles/proofmill-standard" --offline
    "$speckit_venv/bin/specify" preset resolve spec-template
    "$speckit_venv/bin/specify" workflow info proofmill-standard

Bundle install reports `0 added, 2 already present` because it records the two
preinstalled local components. The one completed Codex run used CLI `0.147.0`
and this exact command:

    codex -a never exec --ephemeral --ignore-user-config -s workspace-write --json -o "$fixture/codex-last-message.txt" 'Use the simple-english and speckit-specify skills. Create specification artifacts only for feature 001-status-note. The feature adds one README status sentence: "The service reports ready after startup." Define REQ-001. Do not plan, create tasks, or implement code. If a feature directory is needed, use specs/001-status-note. Stop after the specification exists.'

The command used the service default model. The model identifier was not
retained, so the prose is not byte-for-byte reproducible. Do not run Codex again
in this milestone. Inspect the completed artifacts with:

    find specs -type f -print | sort
    rg -n 'REQ-001|INV-001|Proofmill contract' specs/001-status-note/spec.md
    find specs/001-status-note -type f -name plan.md -o -name tasks.md

Run provider checks from their source directories:

    cd "$upstream_root/ponytail"
    npm test
    "$speckit_venv/bin/pip" install pandas
    PATH="$speckit_venv/bin:$PATH" npm test
    cd "$upstream_root/simple-english"
    python3 evals/ste_lint.py --self-test
    python3 -m unittest evals.test_run_pi_bench

The first Ponytail command is a preserved negative result: 83 of 84 core tests
pass and the CSV case fails without `pandas`. The second run must pass 84 core,
23 Pi, and 3 MCP tests. SimpleEnglish must pass its self-test and seven unit
tests. Detailed results belong only in the ignored
`.agent/test-results/bootstrap.md` file.

## Validation and Acceptance

Acceptance requires all current schema and lint commands to exit zero. The
bundle must install after its local components. The workflow must run its
provider check before specification. Codex must create one feature specification
with a `Proofmill contract` section and stable requirement IDs. No `plan.md`,
`tasks.md`, or implementation file can exist in the fixture.

After uninstall, the feature specification and checklist must remain. A
malformed bundle must fail validation. Missing SimpleEnglish or Ponytail must
stop the standard workflow at its first step. The completed dry run's human
inspection claim is a failure, not deterministic evidence.

## Idempotence and Recovery

Spec Kit component installation is idempotent by component ID. A failed local
component install can be removed with its matching remove command. Bundle
rollback is best effort, so inspect `.specify/` after a failed install.

The dry-run fixture is disposable. The source repository does not depend on
fixture state. Provider removal must not remove repository specifications.

## Artifacts and Notes

Detailed command results are in the ignored file
`.agent/test-results/bootstrap.md`. The durable conclusions are in the three
upstream reviews and the gap report.

## Interfaces and Dependencies

The composition requires Spec Kit `0.16.3.dev0` built from commit
`bd595cf838cc200f84fee9e9327b643dfe277d2c`, Codex CLI, Git, Python 3.11 or
newer, and Node.js for the Ponytail hooks.

The preset, workflow, and bundle use Spec Kit schema `1.0`. No Proofmill
executable interface exists.

Latest revision: 2026-08-11. Updated after adversarial review corrected provider
status, installation safety, reproducibility, and the dry-run evidence claim.
The third review found no composition or fixture defect.
