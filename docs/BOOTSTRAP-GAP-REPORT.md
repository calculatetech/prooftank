# Bootstrap gap report

## Recommendation

**Revise the product claim; do not add runtime.** The current schemas and
installation path are valid. The corrected Codex run preserves missing evidence
as unknown, but the first comparable benchmark found no accepted-behavior gain
from Proofmill Standard. The composition is not a deterministic assurance gate.

Do not build a Proofmill runtime. PM-026 screened the current candidates and
selected none. The full result is in
`docs/DETERMINISTIC-GATE-QUALIFICATION.md`.

PM-027 also rejected a release-warrant extension for the MVP. No benchmark or
release failure requires one, and the qualified gate candidate can create false
success when executable coverage is absent.

## What works

- Spec Kit `0.16.3.dev0` accepts the Proofmill preset, workflow, and bundle
  schemas.
- The contract preset adds a floor, a ceiling, stable IDs, failure behavior, and
  evidence mapping.
- The standard workflow uses core Spec Kit commands and review gates.
- Codex reads the generated Spec Kit skills and exact-copy provider skills.
- One dry run created a feature specification and checklist without planning or
  implementation.
- The corrected PM-030 Codex run kept absent executable coverage and human
  inspection `unknown`, excluded agent output from proof, and reviewed every
  Proofmill contract field in its checklist.
- Disable and uninstall operations preserve repository truth.
- The workflow begins with a required-provider shell check. Missing
  SimpleEnglish or Ponytail stops the standard profile before specification.

## Gaps

### Local bundle installation

The bundle cannot install its custom local preset and workflow in one command.
The supported path still needs separate native component commands. PM-031 adds
a versioned, checksummed local release directory, so those commands no longer
depend on a mutable Proofmill checkout. A hosted install-allowed catalog remains
optional future publication work.

### Exact agent-skill pins

Ponytail's Codex marketplace entry tracks `main`. The SimpleEnglish `npx skills`
command also uses a repository reference without a commit pin. The versioned
PM-031 release carries pinned provider bytes, licenses, source commits, and
checksums. Its install path uses neither mutable command. SimpleEnglish differs
from upstream only by narrowing `compatibility` to `codex`.

Ponytail is approved as advisory through its exact-copy skill path. Its
marketplace path remains unapproved because it tracks `main`. SimpleEnglish is
approved as advisory through its Codex-normalized three-file release path. Its
two reference files remain exact upstream copies. Its unpinned `npx` path
remains unapproved. Hosted publication remains separate from the versioned
local release.

### Claude conformance availability

PM-007 identified Claude's native `.claude/skills/` path and passed disposable
installation, provider failure, dispatch, and uninstall checks. The current
official Claude Code release is pinned, but the host is not authenticated.
The active standard workflow is Codex-only while PM-007 is postponed. Artifact
equivalence remains `unknown` until that work resumes with authentication.

### Deterministic traceability and evidence

Core `speckit.analyze` finds cross-artifact problems with agent judgment. Core
`speckit.converge` finds remaining work with agent judgment. Neither command
proves requirement-to-test coverage or release readiness.

The current workflow therefore requires project-native tests and lint. It
reports missing evidence as `unknown`. It does not issue a release warrant.

The first dry-run specification called human inspection evidence and reported
no unknowns. That output remains a preserved negative result, not proof. The
corrected PM-030 run followed the revised contract: both stable identifiers had
unknown executable coverage, and the checklist left both deterministic mappings
incomplete. This shows one current Codex run handled the gap honestly; it does
not supply the missing deterministic evidence.

PM-026 fully qualified the leading `gates` `0.3.3` candidate. It can execute
explicit checks, but a `Complete` feature with no executable acceptance block
passes its gate and health check. Its install also needs an agent-driven runtime
projection, its disable and uninstall commands leave that projection active,
and its exact lockfile has two high-severity advisories. It is blocked and not
part of the standard composition.

### First comparable benchmark

Batch `first-comparable-001` ran five Codex arms with identical frozen inputs
and runner settings. After removing two hidden-suite assertions that exceeded
the public brief, every unchanged arm passed all 15 scenarios.

Proofmill Standard did not improve accepted behavior in this batch. It used
626.656 seconds, 47 tool calls, and 1,602,751 input tokens. Ponytail-only used
224.766 seconds, 15 tool calls, and 237,746 input tokens. The bare arm produced
the least source. The result recommends revising the product claim and testing a
task that differentiates assurance behavior before adding process or runtime.

## Extension screen

The current community catalog lists relevant candidates. Every entry below has
`verified: false`. None entered the active bundle. PM-026 resolved the exact
source screen in `docs/DETERMINISTIC-GATE-QUALIFICATION.md`.

### Requirement traceability

The catalog lists `trace` `1.0.0`, `v-model` `0.6.0`, and `spectest`. Defer them
because their source and conformance reviews are incomplete.

### Implementation verification

The catalog lists `verify` `1.0.3` and `verify-tasks` `1.0.0`. Defer them
because both include agent-facing hooks. Deterministic coverage is not
established.

### Architecture rules

The catalog lists `architecture-guard` `1.13.1` and `blueprint-index` `0.2.0`.
Defer them because they add refactor tasks or a living architecture map.

### Quality gates

The catalog lists `gates` `0.3.3`, `ci-guard` `1.0.0`, and `tdd` `1.1.2`.
PM-026 fully qualified `gates` and blocked it. The other entries remain
unreviewed and disabled. The benchmark does not justify another gate review for
the MVP.

### Evidence packs

The catalog lists `patchwarden-evidence` `1.0.1` and `docguard` `0.33.0`. Defer
them. PatchWarden adds a required tool. DocGuard adds an MCP server and a
broader documentation system.

Catalog presence is discovery evidence only. The catalog does not audit or
endorse these components.

## Negative findings

- Offline bundle validation can warn and pass when a remote component cannot be
  checked.
- Bundle install skips a preinstalled component by ID without comparing the
  installed version to the bundle pin.
- Ponytail's complete upstream test command needs `pandas` for one CSV
  benchmark, but the package does not install it.
- The SimpleEnglish linter cannot prove controlled-language compliance.
- Provider output remains advisory unless a deterministic project tool supports
  the claim.
- The completed dry run did not validate its Proofmill contract in the generated
  checklist and mislabeled human inspection as evidence. PM-030 preserves a
  corrected positive run beside that negative result.

## Remaining work

The roadmap is in `docs/roadmap.md`. The supported MVP provider set is closed:
GitHub Spec Kit, Ponytail, and SimpleEnglish under Codex, with project-native
tests and lint. CBM, Cavemem, NeuroArxiv, ADHD, and spec-gates are blocked.
Cavekit is comparison-only. CodeGraph and Caveman remain unreviewed backlog
candidates. Non-Codex harness and critical-profile work is postponed.

Public-pilot documentation and human name clearance remain. The benchmark found
no quality gain from Proofmill Standard and authorizes no additional runtime.
