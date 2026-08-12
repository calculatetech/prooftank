# Ponytail qualification

## Identity

- Repository and homepage: <https://github.com/DietrichGebert/ponytail>
- Reviewed commit: `2ed6c52c9d7e5e56942508591085fd45dea277d3`
- Declared source version: `4.9.0`
- Latest release tag: `v4.9.0` at
  `0a4dd63ad4541f4f655c4108a295916f3c1d8fda`
- Commit date: 2026-08-07
- License: MIT, copyright Dietrich Gebert
- Activity: The reviewed commit remained upstream `HEAD` on 2026-08-12. The
  repository had recent `v4.8.x` and `v4.9.0` releases.

## Capability and trust

Ponytail supplies minimal implementation instructions, focused review skills,
and optional mode hooks. Its decisions are advisory. Project-native tests and
lint remain the deterministic evidence.

Qualification state: `approved` for advisory use through the exact-copy skill
path. The marketplace path remains unapproved because its descriptor follows
`main` instead of the reviewed commit.

## Installation and updates

For Codex, use the upstream marketplace commands:

```bash
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

The marketplace descriptor tracks `main`. It is useful for local experiments
but is not the Proofmill installation path. Proofmill installs
`.agents/skills/ponytail/` from the detached reviewed checkout. This exact-copy
path omits automatic hooks and makes the source identity inspectable.

The exact-copy health check is:

```bash
test "$(sha256sum .agents/skills/ponytail/SKILL.md | cut -d' ' -f1)" = \
  1316a2f3f95741d2300b116fe0c2d81ce4a9568656ed0a62643f54aaf09957f2
```

Run `npm test` with its documented pandas benchmark dependency in the reviewed
source checkout as the provider health check.

There is no automatic update on the approved path. Review and record a new
commit first, move the old skill directory aside, copy the new exact source,
and verify its new hash. The lifecycle fixture updated an exact copy from
`v4.8.4` to the reviewed commit and observed distinct hashes. The operation was
reversible.

## Files, configuration, hooks, and commands

The Codex plugin cache stores the plugin manifest, six skills, hook scripts,
assets, and the license. It registers these lifecycle hooks:

- `SessionStart` runs `ponytail-activate.js`;
- `SubagentStart` runs `ponytail-subagent.js`;
- `UserPromptSubmit` runs `ponytail-mode-tracker.js`.

Each hook uses Node.js and has a five-second timeout. The plugin registers
`ponytail`, `ponytail-review`, `ponytail-audit`, `ponytail-debt`,
`ponytail-gain`, and `ponytail-help` skills.

Codex mode state is `.ponytail-active` under the plugin data directory. Optional
configuration is `~/.config/ponytail/config.json`, or its platform equivalent.
Claude-only status-line setup can change `~/.claude/settings.json`. The plugin
starts no persistent process.

## Network, credentials, and privacy

Marketplace installation contacts GitHub. The reviewed Codex hooks make no
network request and use no credential. The plugin reads the user prompt only to
detect explicit mode commands. It writes only the mode value.

## Disable and uninstall

Use `/ponytail off` or `normal mode` to disable plugin instructions and erase
the active mode flag. Use `codex plugin remove ponytail` to remove an
experimental marketplace plugin. Run `node scripts/uninstall.js` before plugin
removal to erase optional external state.

Disable the approved exact-copy path by moving
`.agents/skills/ponytail/` outside `.agents/skills/`. Uninstall it by removing
that directory. The tested operations made the skill unavailable and did not
change specifications, plans, tasks, or source code.

## Failure behavior and fallback

Hook state writes and hook output errors are best effort. The hooks fail
silently so that they do not block the agent session. If Node.js or a hook is
unavailable, the installed skill still works when Codex loads it.

If Ponytail is unavailable in the standard profile, stop before implementation.
The fallback rules in `AGENTS.md` can guide investigation, but they do not
satisfy the required-provider state.

## Conformance results

- The installed Codex plugin reported version `4.9.0` and enabled status.
- The current session applied Ponytail to every implementation choice.
- Current remote HEAD remained the reviewed commit on 2026-08-11.
- A clean exact-copy install matched SHA-256
  `1316a2f3f95741d2300b116fe0c2d81ce4a9568656ed0a62643f54aaf09957f2`.
- A fresh shell process read the same skill. Two isolated hook starts restored
  `full` mode without a persistent process.
- Missing and moved-aside skill directories made the workflow preflight return
  unavailable. Reinstall restored the reviewed hash.
- An explicit exact-copy update from `v4.8.4` changed the skill hash from
  `d1ffcddbc486ab787d5797441e8b6e4717da3249c6786b83fc2abd2f12803c29`
  to the reviewed hash.
- `normal mode` removed isolated hook state. Exact-copy uninstall preserved a
  repository-owned fixture byte for byte.
- The upstream core suite first reported 83 passes and one failure because
  `pandas` was absent.
- The upstream README documents `pandas` as a CSV benchmark dependency.
- After `pandas` was added to the disposable test environment, all 84 core
  tests, 23 Pi tests, and 3 MCP tests passed.
- Hook timeout, invalid mode, uninstall, and malformed state cases passed in the
  upstream suite.

## Known limitations

Ponytail is an instruction provider. It cannot prove minimality or correctness.
The marketplace entry tracks `main`, so the host install and update commands do
not enforce the recorded commit. They are not approved for the standard
composition.

The approved path ships only the main `ponytail` skill. It does not register the
five optional review, audit, debt, gain, and help skills or automatic hooks.
PM-031 still owns publication of an immutable installation artifact.
