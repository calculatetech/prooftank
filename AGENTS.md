# AGENTS.md

This file is the map. The documents in `docs/` are the source of truth.

## Mission

Build Proofmill as an audited assurance distribution for existing coding-agent harnesses.

Proofmill packages and qualifies existing tools. It adds only the missing deterministic seams.

## Read first

1. `CODEX-START.md`
2. `docs/PRODUCT-CHARTER.md`
3. `docs/DECISIONS.md`
4. `docs/ARCHITECTURE.md`
5. `docs/HARNESS-ENGINEERING.md`
6. `docs/BUILD-VS-INTEGRATE.md`
7. `docs/UPSTREAM-QUALIFICATION.md`
8. `docs/roadmap.md`

## Locked architecture

- GitHub Spec Kit is the process substrate.
- Codex is the only supported MVP harness and remains the user interface.
- Other harness work is postponed and must not enter MVP artifacts.
- One project has one authoritative specification system.
- Proofmill version 0 does not own a daemon, database, agent loop, code graph, memory system, or MCP aggregator.
- Repository files and Git history own project truth.
- Upstream providers are swappable and optional unless the selected profile marks them required.
- Missing or degraded evidence is `unknown`. It is not `passed`.

## Product rules

1. Integrate before you build.
2. Read an upstream project before you duplicate its capability.
3. Pin every accepted upstream to an exact release or commit.
4. Record its license, trust class, commands, hooks, file writes, network access, and uninstall path.
5. Never auto-switch an upstream provider.
6. Never let memory or a chat transcript change the governing specification.
7. Never let an agent approve its own contract change or waiver.
8. Use deterministic scripts for pass/fail claims.
9. Use agent judgment for proposals and review, not final evidence.
10. Keep the implementation bounded by `must_do`, `must_not_do`, `may_do`, and `stop_when`.

## Writing rules

- Use SimpleEnglish principles for technical instructions.
- Use one term for one concept.
- Put a condition before its instruction.
- Use `must` for requirements.
- Preserve code, paths, identifiers, commands, and quoted errors exactly.
- Keep this file short. Add detail to the correct document and link it here.

## Implementation rules

- Apply Ponytail: understand the full path, then choose the smallest sufficient solution.
- Reuse repository code, standard tools, native platform features, and installed dependencies before adding new code.
- Do not add an abstraction with one implementation unless a current requirement needs it.
- Do not add a service, database, queue, plugin host, or runtime for a hypothetical future use.
- Do not add code until a written gap analysis shows that the approved upstream stack cannot satisfy the requirement.

## Planning rules

- Complex work requires an execution plan in `docs/exec-plans/active/`.
- Update `docs/roadmap.md` when work starts, completes, changes order, or is
  discovered. Never mark more than one roadmap task active.
- Update progress, decisions, findings, and verification results during the work.
- Move completed plans to `docs/exec-plans/completed/`.
- Record changes to locked architecture as a new decision in `docs/DECISIONS.md`.

## Upstream rules

Before enabling an upstream component:

- Review source and license.
- Identify all commands, hooks, tools, network access, and persistent files.
- Run install, health, update, disable, and uninstall tests.
- Run the applicable harness-conformance fixtures.
- Define a fallback.
- Define failure behavior.
- Classify output as advisory, observational, deterministic, or authoritative.

Community catalog inclusion is not approval.

## Verification rules

- Run repository tests before claiming completion.
- Record the exact command and source revision.
- A tool crash is a failed or unknown check.
- An empty graph result does not prove that no relationship exists.
- A test without a requirement link does not prove contract coverage.
- A completed task without implementation evidence is stale.
- Preserve failed benchmark runs and negative results.

## Current target

The bootstrap is complete. Follow the order in `docs/roadmap.md`.

Do not start the checkbook benchmark without explicit approval.
