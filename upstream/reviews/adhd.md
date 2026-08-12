# ADHD qualification

## Identity

- Primary repository: <https://github.com/UditAkhourii/adhd>
- Current release: `v0.1.4`, published 2026-05-30.
- Release commit: `770834e3e2f56f2620f835253996c3eb143b72ed`.
- Current `main` inspected: `3d9dc487bc2eba4449742e2db0d92be9ebdf95b6`.
- npm package: `adhd-agent@0.1.4`.
- npm integrity:
  `sha512-j/UzhOd8VjMcjStw/Hx3etAT5WrSSunGZcMjKJ3gsLzNWenOkvOzk/A1f6hgYtLpwTyowquz3guA/c8GxWWw8g==`.
- Release skill SHA-256:
  `a0624f0ca1ccc45184f858cefdf02034b359b7706132edda2ddea7449dc29b70`.
- License: MIT, copyright ADHD contributors.
- Review date: 2026-08-12.
- Qualification state: `blocked-process-and-runtime`.

## Capability and trust

ADHD explores an open question through multiple isolated model branches under
different cognitive frames. Separate model calls then score, cluster, reject
traps, and deepen selected ideas. The skill describes roughly ten model calls
and a cost of five to ten times one answer.

Trust class: advisory review. Generated alternatives and scores can reveal a
missed idea, but they cannot approve a specification, contract, evidence state,
or release. A separate deterministic or human decision remains required.

## Installation and written state

The generic skill path is `npx skills add UditAkhourii/adhd`; upstream also
documents `npx skills add UditAkhourii/adhd -a codex -g`. Those commands use a
separate mutable skills installer and current repository content. The manual
Codex path writes `~/.codex/skills/adhd/SKILL.md` from mutable `main`.

An exact install could copy the reviewed release skill by commit and verify its
hash, but ProofTank does not select it. The CLI path installs
`adhd-agent@0.1.4`, requires Node 18 or newer, and registers `adhd`. It depends
on the Claude Agent SDK, `p-limit`, and Zod. It writes no hook, daemon, database,
MCP setting, or repository file unless the user redirects JSON output.

## Commands and network

The skill registers `/adhd`. Its required flow uses parallel Agent or Task calls
for five isolated branches, followed by critic and deepening calls. It explicitly
says serial branches are not ADHD. The CLI accepts frame, idea, survivor,
concurrency, context, model, JSON, and quiet controls.

Skill installation contacts GitHub and npm through the external skills tool.
CLI installation contacts npm. CLI execution sends the problem, optional
context, and generated content to Anthropic through the Claude Agent SDK. It
uses `ANTHROPIC_API_KEY` or local Claude Code authentication. The Codex skill
uses the active model service through Codex rather than a separate network
client.

## Health, disable, and uninstall

There is no doctor command. Source checks are `npm test`, `npm run typecheck`,
and `npm run build`; they do not show model authentication or branch isolation.
A useful health check must also prove that every divergent branch received a
fresh context and ran in parallel.

Disable the Codex skill by moving its exact directory outside the skill search
path. Uninstall it by deleting only the exact ADHD skill directory. Remove the
CLI with `npm uninstall -g adhd-agent`. Preserve any user-selected result file.

## Failure behavior and pilot result

Invalid CLI numbers, oversized context files, Claude failures, and invalid
model JSON make the CLI exit 1. The skill requires all divergence branches to
remain mutually isolated; cross-talk or serial execution invalidates the method.
Its output can still converge confidently on an unsupported idea, so provider
completion is not approval.

The planned isolation comparison did not run. ProofTank permits only one
subagent at a time, while the reviewed skill explicitly requires five parallel
isolated agents and rejects serialization. The alternative CLI requires the
Claude Agent SDK and authentication unavailable to this Codex-only MVP.
Changing the skill to fit would be a new agent loop or adapter, both prohibited.

These findings are simple: the skill states its parallel isolation invariant,
and the CLI imports the Claude SDK directly. They are relevant: either available
execution path violates a governing MVP or repository constraint. ADHD is
blocked without creating a critical workflow or weakening review rules.

## Fallback

Use one fresh clean-context Codex subagent for a bounded adversarial review when
repository rules require it. Keep that review read-only and separate from
contract approval. For wider ideation, record it as future work until the
coordinator rule explicitly permits parallel isolated branches.
