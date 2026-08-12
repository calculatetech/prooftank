# Architectural decision log

<!-- markdownlint-disable MD013 -->

These decisions are locked for the bootstrap milestone. Change one only through a new decision entry with evidence.

## D001 — Product name

**Decision:** Use the working name `Proofmill`.

**Reason:** The product turns intent and implementation attempts into evidence-backed output.

**Status:** Superseded by D023. `ProofTank` is the accepted working name; PM-036
owns the identifier migration.

## D002 — Product boundary

**Decision:** Proofmill is an assurance distribution, not an agent runtime.

**Reason:** Codex, Claude Code, OpenCode, Pi, and OpenHarness already provide agent loops, tools, context, and user interfaces.

**Status:** Accepted.

## D003 — Process substrate

**Decision:** Use GitHub Spec Kit as the version 0 process and packaging substrate.

**Reason:** It already owns constitutions, specifications, plans, tasks, analysis, convergence, extensions, presets, workflows, catalogs, and bundles.

**Status:** Accepted, subject to current API verification.

## D004 — Repository as system of record

**Decision:** Versioned repository files and Git history own the project contract and decisions.

**Reason:** Conversations, memory systems, and dashboards can disappear or drift.

**Status:** Accepted.

## D005 — One specification owner

**Decision:** A project must not use Spec Kit and Cavekit as concurrent authoritative spec owners.

**Reason:** Two owners create drift and conflict.

**Status:** Accepted.

**Consequence:** Cavekit is a design reference in version 0. Its right-size, compact-spec, drift, and backprop principles can inform the Proofmill preset.

## D006 — Minimal implementation provider

**Decision:** Ponytail is the default minimal-implementation provider.

**Reason:** It applies a reuse and YAGNI ladder while preserving root-cause fixes, trust-boundary checks, data-loss protection, security, accessibility, and focused tests.

**Status:** Accepted and qualified at the registry pin.

## D007 — Controlled language provider

**Decision:** SimpleEnglish is the default technical-writing and instruction-clarity provider.

**Reason:** It adapts ASD-STE100 concepts into testable agent instructions and preserves code and identifiers.

**Status:** Accepted and qualified at the registry pin.

## D008 — Structural provider

**Decision:** CBM is the primary candidate structural provider. CodeGraph is a candidate alternative. Both remain optional and observational.

**Reason:** Structural graphs are useful for impact and bypass detection, but missing or stale edges cannot prove absence.

**Status:** Superseded for the MVP by D022. CBM is blocked and CodeGraph remains
an unreviewed backlog candidate.

## D009 — Research and divergence

**Decision:** NeuroArxiv and ADHD belong to the critical profile by default.

**Reason:** They are valuable but expensive. Routine work does not earn this ceremony.

**Status:** Superseded for the MVP by D022. The critical profile is postponed,
and both reviewed candidates are blocked on current runtime or process rules.

## D010 — Memory

**Decision:** Cavemem is optional and advisory.

**Reason:** It can recover prior experience, but retrieved memory cannot silently modify the governing contract.

**Status:** Superseded for the MVP by D022. Cavemem is blocked by the product
boundary.

## D011 — Runtime targets

**Decision:** Codex is the first runtime. Claude Code, OpenCode, and Pi are required conformance targets. OpenHarness is optional in the bootstrap milestone.

**Reason:** This covers mainstream and neutral open harnesses without creating a new interface.

**Status:** Superseded by D019 for the MVP.

## D012 — License policy

**Decision:** Use permissive-license-only defaults. Exclude RepoWise from the default product due to AGPL-3.0.

**Reason:** The product must remain easy to package, embed, and distribute.

**Status:** Accepted. GPL-family optional out-of-process exceptions require explicit human review.

## D013 — Version 0 implementation

**Decision:** Do not build a Proofmill daemon, database, MCP aggregator, code graph, memory system, or agent loop.

**Reason:** Existing tools already own these capabilities. A gap must be measured before code is added.

**Status:** Accepted.

## D014 — Risk grades

**Decision:** Define `lite`, `standard`, and `critical` profiles.

**Reason:** Reliability ceremony must scale with blast radius.

**Status:** Accepted.

## D015 — Work packet

**Decision:** Every implementation packet must define `must_do`, `must_not_do`, `may_do`, and `stop_when`.

**Reason:** The packet must prevent both omission and overengineering.

**Status:** Accepted.

## D016 — Evidence semantics

**Decision:** Preserve `passed`, `failed`, `stale`, `degraded`, `unknown`, and `waived` as distinct states.

**Reason:** Missing evidence and tool failure must not produce a false green result.

**Status:** Accepted.

## D017 — Benchmark

**Decision:** Use a checkbook application and ablation arms to measure value.

**Reason:** Money, reconciliation, import atomicity, duplicate identity, audit, concurrency, and recovery expose meaningful reliability differences in a small application.

**Status:** Accepted.

## D018 — Build only after gap test

**Decision:** Before creating a Proofmill extension, compare current Spec Kit core and community extensions against the requirement.

**Reason:** Curation and conformance are the product. Duplication is not.

**Status:** Accepted.

## D019 — MVP runtime scope

**Decision:** Codex is the only supported MVP harness. Other harness work is
postponed and must not enter MVP artifacts.

**Reason:** The MVP must complete one qualified runtime path before it expands
its support surface.

**Status:** Accepted.

## D020 — No MVP release warrant

**Decision:** Do not add a release-warrant extension to the Codex MVP.

**Reason:** The first comparable benchmark found no quality difference across
five arms, while the qualified gate candidate allowed missing executable
coverage to pass. Project-native tests, lint, checksums, and explicit unknowns
are smaller and more honest.

**Status:** Accepted. Reconsider only after a preserved release failure shows a
decision that current controls cannot express.

## D021 — No MVP provider-health extension

**Decision:** Use each active provider's exact version or hash check. Do not add
a shared provider-health extension to the MVP.

**Reason:** Spec Kit, Ponytail, and SimpleEnglish already have bounded health,
disable, reinstall, and uninstall checks. The standard workflow stops when a
required skill is unavailable. No observed incident needs an aggregator or new
protocol.

**Status:** Accepted. Reconsider only after a preserved provider incident cannot
be represented as failed, stale, degraded, unavailable, or unknown.

## D022 — Close the MVP provider set

**Decision:** The supported MVP composition is Codex, GitHub Spec Kit,
Ponytail, SimpleEnglish, project-native tests and lint, and declarative
Proofmill files. No optional runtime provider is active.

**Reason:** CBM and Cavemem cross prohibited product boundaries. NeuroArxiv and
ADHD cannot run under current Codex-only and coordination rules. Cavekit is a
comparison input only. The benchmark found no quality gain that authorizes more
process or runtime.

**Status:** Accepted. New providers require a roadmap task, exact source
qualification, and a measured need.

## D023 — Adopt ProofTank as the working name

**Decision:** Use `ProofTank` as the working name for the open-source hobby
project. Publish the repository at `calculatetech/prooftank`. Keep existing
`Proofmill` identifiers unchanged until one bounded migration passes validation.

**Reason:** An active Python CLI already uses the `ProofMill` product name,
`proofmill` distribution name, and `proofmill` command. `ProofTank` had no exact
collision in the bounded web, GitHub, package-registry, or DNS screen. The owner
accepts the remaining naming risk for a project that is not formally marketed.

**Status:** Accepted. This is a working-name decision, not legal or trademark
clearance. PM-036 owns the migration.
