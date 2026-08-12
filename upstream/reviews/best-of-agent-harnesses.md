# best-of-Agent-Harnesses qualification

## Identity

- Primary repository:
  <https://github.com/RyanAlberts/best-of-Agent-Harnesses>
- Reviewed data commit: `c81b202ce6388c2d56c56f049dabf413288bb9da`.
- Data snapshot: 154 live projects, 3 graveyard entries, stars captured
  2026-08-09.
- Data license: Creative Commons Attribution-ShareAlike 4.0.
- Review date: 2026-08-12.
- Qualification state: `approved-advisory-input`.

The repository also ships an MIT-licensed MCP server at release `mcp-v0.4.0`.
ProofTank does not select or install that server.

## Capability and trust

The repository provides a curated list of agent harnesses, use cases,
complexity, autonomy, recovery, license signals, stars, examples, comparisons,
graveyard entries, and selected deeper capability ratings. It can highlight a
new project, a moved repository, an archived dependency, or a large activity
change that deserves primary-source review.

Trust class: advisory maintenance input. Stars are popularity data. Categories,
tiers, descriptions, and many ratings are editorial. Some deep ratings link to
primary evidence, but the list does not qualify a component for ProofTank. It
cannot add a harness, replace a pin, or create a pass state.

## Access and written state

The selected method is read-only inspection of `harnesses.json` at the reviewed
commit. A maintainer may fetch that exact file or inspect a detached checkout.
This writes no ProofTank file beyond a deliberate human update to a review or
roadmap item.

The unselected MCP alternative installs `agent-harnesses-mcp` through `uvx`,
registers an MCP server in the user's agent configuration, and fetches current
`harnesses.json` from repository `main` at startup. It registers recommendation,
selection, comparison, search, record, category, and guide tools. Its mutable
startup data and extra runtime are unnecessary for a periodic maintenance
signal.

## Update process, commands, and network

Upstream generates `README.md`, `projects.yaml`, `TAGS.md`, `harnesses.json`,
JSON-LD, and `llms.txt` from Python source. A weekly GitHub Action uses the
GitHub API to refresh stars, moved repositories, and archive state. Candidate
discovery searches GitHub and writes a curation queue. Maintainers then apply
editorial judgment. The refresh requires a GitHub token because its request
count exceeds the anonymous limit.

Direct pinned inspection contacts only GitHub. Running upstream generation or
refresh can contact the GitHub API and write all generated list artifacts. The
selected ProofTank process runs neither. It has no hook, daemon, database,
schedule, credential, or installed command.

## Health, disable, and uninstall

For a detached checkout, run:

```bash
python3 -m json.tool harnesses.json >/dev/null
python3 scripts/check_integrity.py
```

The reviewed commit passed both checks. Also read `meta.stars_captured` and
reject the snapshot as a current activity signal when its age is not acceptable
for the maintenance decision.

Disable the input by skipping the manual check. Uninstall it by deleting the
detached checkout or downloaded JSON. There is no ProofTank integration to
remove. If someone separately installed the MCP server, remove its exact agent
configuration and `uvx` cache entry through the package manager.

## Failure behavior and fallback

Upstream refresh stops when credentials are missing, the source format changes,
or more than five repositories fail. It keeps old counts for bounded individual
failures and records them. Integrity checks detect empty categories, truncated
comparison prose, and large project loss. A syntactically valid snapshot can
still contain stale or mistaken editorial claims.

If the repository, JSON, or evidence link is unavailable, record the
sustainability signal as unknown and inspect the exact provider repository,
release history, security policy, issue tracker, and current license manually.

## Selection rule

The input is approved only for a human-triggered maintenance review. A change
may create a roadmap item for primary-source qualification. It must never change
a pin, component state, or supported harness automatically. Codex remains the
only MVP harness regardless of list ranking.
