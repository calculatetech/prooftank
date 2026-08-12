# Cavekit comparison qualification

## Identity

- Primary repository: <https://github.com/JuliusBrussee/cavekit>
- Reviewed release: `v4.1.0`.
- Reviewed commit: `c322f0bb6db82163041930467f3ce32754d42827`.
- Commit date: 2026-06-18.
- License: MIT, copyright Julius Brussee.

Qualification state: `approved-comparison-only`. Cavekit is not an active
ProofTank provider or specification owner.

## Capability and trust

Cavekit supplies a compact one-file specification process. Its normal loop is
`spec`, `build`, and `check`. The benchmark also copies its `caveman` and
`backprop` utility skills because the loop refers to them.

All output is advisory agent output. Cavekit does not produce deterministic
proof. Trust class: advisory comparison input.

## Installation and files

The benchmark vendors exact `SKILL.md` files from the reviewed commit and copies
them to these Codex paths:

- `.agents/skills/spec/SKILL.md`.
- `.agents/skills/build/SKILL.md`.
- `.agents/skills/check/SKILL.md`.
- `.agents/skills/caveman/SKILL.md`.
- `.agents/skills/backprop/SKILL.md`.

The benchmark does not use Cavekit's mutable `npx` command, Claude marketplace,
slash commands, plugin manifest, research skill, review skill, or deepen skill.
It writes no hook, MCP setting, daemon, database, or user configuration.

The five copied skills register only their named agent instructions. `SPEC.md`
is the only Cavekit-owned artifact in its isolated comparison arm.

## Network, health, disable, and removal

Fetching the reviewed source used GitHub. The vendored benchmark skills need no
network or credentials. Health requires the exact hashes:

- `spec`: `99361ddf25a66390dc32b27329d929cf2c610bda3378fc2f81ead664ad60fed1`.
- `build`: `44b8a0699b5a45bd43619dbf780f3c9a31e95a80eb65a3b36c5c5bb533b977ce`.
- `check`: `6daabb7099f28c06551e22a74e76e608c6a90c05a8ec8d7602b37ff95b8c4b4c`.
- `caveman`: `9a93187ecba5923ae74739a04986a1a138ffe02414b481ece2236f0ae6b2a16f`.
- `backprop`: `35eb93f05ef6c407f10759b74ff48274f303a3dc36d45cde9263e97c5662567e`.

Disable Cavekit by moving those five exact directories outside
`.agents/skills/`. Uninstall it by removing those exact directories. Removal
must preserve `SPEC.md`, product source, tests, and benchmark evidence.

## Failure behavior and fallback

If one copied skill is absent or has the wrong hash, do not run the Cavekit arm.
Record the arm setup as failed. The benchmark can still preserve other arm
results, but it cannot claim a five-arm comparison. The fallback comparison is
the separately defined Ponytail-only arm; never silently replace Cavekit within
its named arm.

## Negative findings

The upstream installation paths are mutable or Claude-specific. They are not
approved for this Codex benchmark. Cavekit must not become a second
specification owner in the Spec Kit or ProofTank arms.
