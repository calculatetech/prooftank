# NeuroArxiv qualification

## Identity

- Primary repository: <https://github.com/UditAkhourii/neuroarxiv>
- Reviewed commit: `b5d20efa12dd1ba177ce890d56809d2e027f8055`.
- Declared version: `0.1.0`.
- Release state: no Git tag, GitHub release, or published npm package.
- License: MIT, copyright NeuroArxiv contributors.
- Review date: 2026-08-12.
- Qualification state: `blocked-codex-mvp`.

The exact source commit can be inspected, but upstream's advertised
`npx github:UditAkhourii/neuroarxiv install` follows mutable repository state.
It is not an exact release installation.

## Capability and trust

NeuroArxiv maps a design question to arXiv categories, fetches paper metadata
and abstracts, uses isolated model calls to read them, scores and clusters the
results, and asks a final model call to recommend one path. Results retain an
arXiv paper ID, version, title, authors, publication and update dates, abstract
and PDF links, plus the generated role assigned to each citation.

Trust class: advisory research. arXiv metadata is useful provenance, but the
paper selection, abstract reading, scores, limitations, clusters, and final
recommendation are model output. An abstract is not the full paper. Citations
must be opened and checked manually before they support a decision.

## Installation and written state

The source requires Node 18 or newer. Its documented install runs a mutable
GitHub checkout through `npx`, then copies one file to
`~/.claude/skills/neuroarxiv/SKILL.md`. A local checkout instead runs
`npm install`, TypeScript build, and `node dist/cli.js install`. There is no
Codex installer, Codex skill path, MCP server, hook, daemon, or database.

The CLI can read a user-selected context file up to 10 MiB and can write JSON
results when shell redirection is used. It otherwise writes no project state.

## Commands and network

The package registers the `neuroarxiv` CLI and a Claude `/neuroarxiv` skill.
CLI flags select categories, paper count, concurrency, age, context, Claude
models, JSON, and quiet output. The implementation depends on the Claude Agent
SDK, `p-limit`, and Zod.

The engine sends sequential HTTPS requests to
`https://export.arxiv.org/api/query`, waits three seconds between categories,
uses a 20-second timeout, and retries HTTP 429 once after five seconds. It then
sends the problem, optional context, and fetched abstracts to Claude through
the Anthropic SDK. npm or `npx` also contacts its package and Git sources. The
workflow therefore requires network access and working Claude authentication.

## Health, disable, and uninstall

There is no provider health or doctor command. The closest source checks are
`npm test`, `npm run typecheck`, and `npm run build`; an operational check must
also reach arXiv and complete authenticated Claude calls. Source tests alone do
not show that either service is available.

Disable the skill by moving its exact directory outside
`~/.claude/skills/`. Uninstall it by deleting only
`~/.claude/skills/neuroarxiv/` and removing any local checkout or npm cache the
user chose to create. There is no uninstall command and no Codex state to
remove.

## Failure behavior and pilot result

Bad CLI inputs and oversized context files return exit 1. arXiv HTTP failures,
timeouts, parse failures, Claude failures, and invalid model JSON throw and make
the CLI exit 1. Thin searches can widen once. A failed final convergence can
still render raw readings with no chosen path. None of these states is a pass.

The planned citation run did not execute. The current CLI is hard-wired to the
Claude Agent SDK, the installer targets only Claude Code, this project has no
Claude subscription, and the MVP supports only Codex. The skill alternative
also assumes Claude-specific `WebFetch` and Agent/Task behavior. There is no
released artifact to qualify for a Codex integration.

These findings are simple: the package dependency, install destination, and
skill commands state the runtime directly. They are relevant: running the
provider would contradict the Codex-only MVP and require unavailable
authentication. NeuroArxiv is blocked without creating a critical-profile
workflow or running model calls.

## Fallback

Search current primary sources manually with Codex's supported web access.
Record exact paper or documentation links, versions, dates, and limitations.
Open every important source and distinguish fetched facts from inference. A
manual research gap stays unknown; it never becomes a provider-generated pass.
