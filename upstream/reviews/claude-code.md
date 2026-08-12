# Claude Code conformance qualification

## Identity

- Official repository: <https://github.com/anthropics/claude-code>
- Official package: `@anthropic-ai/claude-code`
- Reviewed release: `2.1.228`
- Release tag commit: `681a8be245e7759a405e276b16ae69ea6b75076f`
- npm integrity:
  `sha512-S3Iy+c6ZuFjswQOekbVgXA+RxAuU8H2ae2nxFynqmvR5r3Gm9oyFV19XgiuatYRFKKjxP0K3i5vvvelPDgx12g==`
- Package archive SHA-256:
  `b32ce01a3caa7d98b51897558a93a28d76a9af55a36ffbaf0f26549044d21ba3`
- Published: 2026-08-11
- License: Anthropic proprietary terms. The package says all rights are
  reserved and use is subject to Anthropic's legal agreements.

## Capability and trust

Claude Code is an agent runtime and a postponed post-MVP conformance candidate. It
can discover project skills, read and write repository files, run tools, and
return structured output in non-interactive print mode.

Trust class: runtime. Qualification state: `postponed-no-subscription`.
Installation and lifecycle checks passed, but no model-backed conformance run

## Installation and updates

The official npm command is `npm install -g @anthropic-ai/claude-code`. PM-007
used `npx @anthropic-ai/claude-code@2.1.228` so it did not add a global package.
That invocation downloads the exact npm package and its platform package into
the npm cache.

An update must select and review another exact version. Do not use an unpinned
latest tag for a measured conformance run.

## Files, configuration, hooks, and commands

The pinned Spec Kit Claude integration writes ten `speckit-*` skill directories
under `.claude/skills/`. It also writes the Claude integration manifest and
active integration record under `.specify/`. The ProofTank preset and workflow
remain under `.specify/`.

The skills register `/speckit-*` commands. The reviewed ProofTank composition
registers no Claude hook, MCP server, daemon, or background process. Exact-copy
Ponytail and SimpleEnglish skills belong under `.claude/skills/` for Claude.

## Network, credentials, and privacy

Package resolution contacts the npm registry. Authentication and model-backed
work contact Anthropic unless the user explicitly configures a supported
third-party provider. Claude Code can read user or project settings unless they
are excluded by its command flags.

PM-007 found no Anthropic API key and no user Claude configuration. `claude auth
status --json` returned `loggedIn: false`, authentication method `none`, and exit
status 1. No credential was requested or stored.

## Health, disable, and uninstall

Run `claude --version` and require `2.1.228`. Run `claude auth status --json`
before a measured run. An unauthenticated result is unavailable, not degraded.

Disable project skills by moving `.claude/skills/` outside the project. Remove
the Spec Kit integration with `specify integration uninstall claude`. The
uninstall removed the ten owned Spec Kit skills and its manifest. It preserved
feature specifications and the two separately installed provider skills.

Remove provider skills separately by removing their exact-copy directories.
These actions do not remove specifications, plans, tasks, or source files.

## Failure behavior and fallback

Missing Ponytail or SimpleEnglish stops the corrected standard workflow at
provider preflight. With both providers installed, workflow dispatch reaches
the specification step. If the Claude CLI is absent or unauthenticated, record
the runtime as unavailable and keep evidence `unknown`.

The fallback is the preserved Codex reference result plus repository-native
inspection. It is not a Claude conformance pass. Do not substitute another
runtime or credential source.

## Conformance results

- Spec Kit installed the Claude integration and exposed all ten core skills.
- Before correction, the standard workflow looked only in `.agents/skills/`
  and rejected valid Claude provider installs.
- The corrected workflow selects `.claude/skills/` for explicit Claude and for
  auto mode in a Claude project.
- Missing-provider cases stop with the correct provider name.
- With both exact-copy providers present, explicit Claude and auto mode pass
  provider preflight and reach runtime dispatch.
- Integration uninstall preserved the reference specification byte for byte
  and left provider skills under their separate owner.
- The model-backed artifact comparison is blocked by missing human
  authentication.

## Known limitations

This record does not qualify Claude output, restart behavior after a model run,
token or cost metadata, permission behavior, or artifact equivalence. Those
checks are postponed with PM-007 because the project has no Claude subscription.
The npm package is a launcher for a platform package and is governed by
proprietary terms.
