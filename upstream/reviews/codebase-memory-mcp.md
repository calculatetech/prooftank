# Codebase Memory MCP qualification

## Identity

- Primary repository: <https://github.com/DeusData/codebase-memory-mcp>
- Current release: `v0.10.2`, published 2026-08-11.
- Release commit: `b377c62a4e8b7ad64ccd295e4aa88abc8d275180`.
- Current `main` inspected: `7f23a66a0a50e6c8e973e9fa648196dbbdb28371`.
- Linux AMD64 release archive SHA-256:
  `6e3bb7353be21407a78e67b5465e53e3afb1a4a213e7a561606900ac08dcfdd6`.
- License: MIT, copyright DeusData.
- Review date: 2026-08-12.
- Qualification state: `blocked-product-boundary`.

The release is the exact reviewed pin. Current `main` is newer and includes
unreleased changes, so it is not an install pin.

## Capability and trust

Codebase Memory MCP, also called CBM, parses repository files and stores a
structural code graph. It offers code search, symbol search, call tracing,
change impact, architecture summaries, graph queries, coverage checks, and
architecture-decision storage through 15 MCP tools and matching local commands.

Trust class: observational. Its output can guide investigation. It cannot prove
absence, complete impact, deterministic coverage, or release readiness. Source
files, specifications, native tests, lint, and direct repository search remain
authoritative.

## Installation and written state

Upstream recommends downloading a release archive through its shell or
PowerShell installer. It also publishes npm, PyPI, Homebrew, Scoop, Winget,
Chocolatey, AUR, and Go installation paths. The shell installer downloads from
GitHub, verifies `checksums.txt`, installs the native executable and runtime
assets, then runs the executable's `install` command.

For Codex, automatic installation can edit these locations below `CODEX_HOME`,
which defaults to `~/.codex`:

- `config.toml` for the MCP server and, when selected, lifecycle hooks;
- `hooks.json` when that existing file owns hooks;
- `AGENTS.md` for managed instructions;
- `skills/codebase-memory/` for the skill;
- `agents/codebase-memory*.toml` for three read-only graph profiles.

The runtime can also write `${CBM_CACHE_DIR:-~/.cache/codebase-memory-mcp}`.
That directory contains graph SQLite databases, `_config.db`, UI configuration,
and lifecycle logs. An explicit index can write
`.codebase-memory/graph.db.zst` and `.gitattributes` inside a repository. Optional
configuration can be read from `.codebase-memory.json` in a repository and
`$XDG_CONFIG_HOME/codebase-memory-mcp/config.json` for the account.

## Commands, hooks, and network

The executable registers `install`, `uninstall`, `update`, `config`, and `cli`
commands. The local `cli` exposes every MCP tool, including `index_repository`,
`list_projects`, `delete_project`, `index_status`, `search_graph`, `trace_path`,
`detect_changes`, `query_graph`, `get_graph_schema`, `get_code_snippet`,
`get_architecture`, `search_code`, `manage_adr`, and `ingest_traces`.

Codex installation registers `SessionStart` and `SubagentStart` hooks that run
`codebase-memory-mcp hook-augment`. Starting an MCP session starts a detached,
per-account coordination daemon. It owns watchers, indexing work, logs, and the
optional local HTTP user interface. A one-shot `cli` query does not leave the
daemon running, but `index_repository` still starts a temporary worker and
creates the persistent graph.

Installation and package updates use the network to fetch GitHub or package
registry artifacts. The reviewed runtime says it performs code processing
locally, needs no API key, does not check for updates, and does not send code to
a hosted service. The optional user interface listens on localhost, normally
port 9749.

## Health, disable, and uninstall

Upstream exposes no single comprehensive health command. The smallest checks
are `codebase-memory-mcp --version`, `codebase-memory-mcp install --dry-run`,
`codebase-memory-mcp cli list_projects`, and
`codebase-memory-mcp cli index_status --project <name>`. A fresh result is still
observational; it must be compared with the current repository revision and
native search.

Do not install CBM in ProofTank Standard. If it was installed separately,
disable it by removing its exact Codex MCP entry and owned lifecycle hooks, or
by moving its exact skill and agent profiles outside Codex discovery paths.
Then restart Codex and use native repository tools.

`codebase-memory-mcp uninstall` removes owned agent entries, instructions,
skills, hooks, profiles, and the installed binary. It asks before deleting graph
indexes. It reports, but does not remove, the adjacent installer. Package-manager
installations also require their package-manager removal. Verify that no owned
Codex entry, hook, process, cache, or repository graph artifact remains.

## Failure behavior and pilot result

CBM rejects an active binary version, build, coordination interface, or cache
root that conflicts with the running daemon. Missing or invalid UI assets leave
the MCP service available with the UI disabled. Unsupported graph queries fail
instead of returning an empty result. The documentation also warns that files
inside an allowed root can be indexed and returned, and that a denylist cannot
identify every sensitive directory.

The planned lifecycle and correctness pilot did not run. The minimum act needed
to test revision freshness, interruption, restart, or ambiguous symbols is
`index_repository`. That act creates the persistent code graph and SQLite state
that this bootstrap explicitly prohibits. MCP operation would additionally
start the provider's daemon. Installing it for Codex would also add instruction,
agent, skill, and hook surfaces much broader than native search.

This is a simple finding: the provider's own documented first useful operation
creates the prohibited state. It is relevant: accepting it would reverse a
bootstrap boundary before the provider could produce evidence. CBM is therefore
blocked for the MVP without downloading or executing its release binary.

## Fallback

Use `rg`, direct file reads, Git, project-native analysis, tests, and lint. Mark
unknown any claim that those tools do not deterministically support. Keep CBM
visible as a rejected candidate and reconsider it only if ProofTank's product
boundary changes through an explicit decision.
