# Cavemem qualification

## Identity

- Primary repository: <https://github.com/JuliusBrussee/cavemem>
- Current published release: `v0.2.1`, published 2026-05-06.
- Release commit: `e934e436e0dcb68422475d85385f7f8eb5e449b1`.
- npm package: `cavemem@0.2.1`.
- npm integrity:
  `sha512-sujtPDxbgyFTNT8d3yREFDYLTbkCTTvcBIN0VIvVER/4qtx2cH64b9oEDmL1m0usfpNAo4Il8H058shoGZTFFA==`.
- Current `main` inspected: `d21a134e412b81cc04e445789883aaf1113b5fed`.
- License: MIT, copyright Julius Brussee.
- Review date: 2026-08-12.
- Qualification state: `blocked-product-boundary`.

The current source declares version `0.3.0` but has no matching tag, GitHub
release, or npm package. The published release is the exact reproducible pin.

## Capability and trust

Cavemem captures coding-agent session events through hooks, compresses them,
and stores them in a persistent SQLite memory. MCP tools search observations,
list sessions, show a timeline, and fetch full observation bodies. A background
worker builds embeddings and serves a local viewer.

Trust class: memory. Retrieved text can be stale, incomplete, compressed, or
from another session. It cannot change a governing specification, evidence
state, or pass state. Repository docs and Git remain authoritative.

## Installation and written state

The published installation is `npm install -g cavemem`, requiring Node 20 or
newer, followed by `cavemem install --ide <name>`. The package depends on
Commander, Kleur, `better-sqlite3`, Hono, its Node server, and the MCP SDK.

Release `0.2.1` writes `~/.cavemem/settings.json`, `data.db`, downloaded model
state, a worker PID file, and logs. It can also write an export file selected by
the user. For Codex, the release installer writes
`~/.codex/config.json` with an MCP entry. Codex uses `config.toml`, so this
published installer is not current-valid for Codex and only supplies query
configuration, not session capture hooks.

Current unpublished `main` changes the Codex integration to edit
`~/.codex/config.toml` and `~/.codex/hooks.json`. It enables Codex hooks, adds
the MCP server, and registers `SessionStart`, `UserPromptSubmit`, `PostToolUse`,
and `Stop` capture commands. That code is not a released install candidate.

## Commands, hooks, and network

The CLI registers `install`, `uninstall`, `status`, `doctor`, `config`, `start`,
`stop`, `restart`, `viewer`, `search`, `compress`, `reindex`, `export`, and
`mcp`. Current source also adds `import`. The MCP server exposes `search`,
`timeline`, `get_observations`, and `list_sessions`; current source adds an
opt-in web `enrich` tool.

Release hooks write memory synchronously. After a successful hook, the default
local embedding configuration auto-spawns a detached worker. The worker binds
to loopback port 37777 and normally exits after ten idle minutes. Hook failures
are written to standard error and return exit 1 without blocking the agent turn.

npm installation contacts the npm registry. The default local embedding model
is `Xenova/all-MiniLM-L6-v2`; Transformers.js can download it when it is not
already cached. Optional Ollama and OpenAI providers use their configured
network endpoints. Current source also contains an off-by-default DuckDuckGo
enrichment path. Therefore “no network” applies only after required artifacts
are local and optional remote features remain disabled.

## Health, disable, and uninstall

`cavemem doctor` checks settings and opens the SQLite database. `cavemem status`
reports configuration, database counts, selected IDEs, embedding backfill, and
worker state. These checks can report storage health; they cannot prove that a
particular Codex event was captured or that retrieved content is true.

Disable capture and the local listener with
`cavemem config set embedding.autoStart false`, stop the worker with
`cavemem stop`, and remove the IDE integration with
`cavemem uninstall --ide codex`. Full removal also requires
`npm uninstall -g cavemem` and explicit deletion or preservation of the
selected Cavemem data directory. The CLI uninstall only removes the IDE entry
and updates settings. It does not delete stored memory or the npm package.

## Failure behavior and pilot result

The published Codex installer writes a configuration file that current Codex
does not use. Hook errors are fail-open, worker auto-spawn is best effort, and a
healthy database does not demonstrate successful capture. Retrieval can be
missing, stale, or semantically similar without being authoritative.

The planned truth-boundary check did not run. Producing even one realistic
retrieval requires creating the persistent memory system and SQLite database
that the MVP explicitly prohibits. Current Codex capture would also add four
account-level hooks and an MCP server. The published release cannot supply that
capture because its Codex installer uses the wrong configuration format.

These findings are simple: the provider describes itself as persistent SQLite
memory, and the released Codex path is one directly inspected installer file.
They are relevant: the first reverses an explicit product boundary, while the
second prevents the current published package from performing the planned
Codex pilot. Cavemem is blocked without executing its package.

## Fallback

Keep durable knowledge in versioned repository docs and Git. Read those sources
directly in every fresh context. Record unknown when a prior conversation is
not represented there. Reconsider Cavemem only after an explicit product
decision permits a memory system and a released, current-valid Codex installer
passes qualification.
