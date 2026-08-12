# Harness conformance

## Purpose

The MVP must produce the required repository artifacts through Codex. Future
runtime comparisons must preserve the governing specification and evidence.

## MVP target

Codex is the only supported MVP harness.

Claude Code, OpenCode, Pi, and OpenHarness are postponed post-MVP candidates.

## Conformance fixture

Use the same repository snapshot, prompt, profile, provider pins, and checkbook
task.

Each runtime must produce:

- the same required Spec Kit artifact set;
- the same stable requirement and invariant IDs;
- a bounded work packet;
- implementation evidence;
- a final state that distinguishes passed, failed, stale, degraded, and unknown;
- no unapproved source of truth.

## Measurements

- Installation steps.
- Context injected at session start.
- Skill and command discovery.
- Provider availability.
- Artifact names and content shape.
- Tool calls.
- Tokens and cost where available.
- Wall time.
- Interrupt and resume behavior.
- Optional-provider failure behavior.
- Uninstall behavior.

## Codex

Codex is the first target.

Verify:

- plugin or skill installation;
- hook trust and behavior;
- `AGENTS.md` discovery;
- Spec Kit command availability;
- repository-local execution plans;
- no hidden dependency on another harness.

## Claude Code

Verify:

- plugin and Agent Skills installation;
- command namespace collisions;
- hook order;
- subagent behavior used by optional providers;
- equivalent artifacts.

PM-007 currently pins Claude Code `2.1.228`. Spec Kit integration install,
native project-skill discovery, provider failure, auto and explicit preflight,
and uninstall truth preservation pass. The model-backed artifact run is blocked
because this host has no authenticated Claude account or API key. Claude
evidence remains `unknown` until a human authenticates the official CLI.
PM-007 and all non-Codex harness work are postponed at the user's direction.
The active standard workflow is Codex-only; the explored Claude routing remains
recorded in PM-007 rather than shipped in the Codex release.

## OpenCode

Verify:

- plugin or instruction loading;
- MCP naming and configuration;
- lifecycle event differences;
- equivalent artifacts.

## Pi

Pi is the neutral open reference runtime.

Verify:

- skills and package installation;
- `AGENTS.md` and project instruction discovery;
- prompt-template compatibility;
- extension needs;
- no assumption that MCP is built in;
- JSON/RPC mode for automated conformance.

## OpenHarness

Verify later:

- skills and plugin compatibility;
- dry-run readiness reporting;
- permission rules;
- context and memory interaction;
- team/subagent behavior;
- equivalent repository artifacts.

## Passing criterion

A runtime passes when differences are limited to runtime configuration and
execution metadata. Contract meaning, IDs, task scope, and deterministic gate
state must remain equivalent.
