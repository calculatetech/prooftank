# Deterministic gate qualification

<!-- markdownlint-disable MD013 -->

## Decision

Select no provider for `prooftank-standard` in PM-026. Keep the existing
project-native test and lint fallback. Missing deterministic coverage remains
`unknown`.

This is a `revise` result. It is not permission to build a ProofTank gate or
start the checkbook benchmark.

## Current source screen

Spec Kit source version `0.16.3.dev0` at commit
`bd595cf838cc200f84fee9e9327b643dfe277d2c` was current on 2026-08-11. Every
candidate below was marked `verified: false` in its community catalog. All
reviewed repositories used the MIT license.

| Candidate | Exact source | Actual mechanism | Result |
| --- | --- | --- | --- |
| `gates` `0.3.3` | `b3800b9d04a7ed489b94052074c94c8980dd6d4b` | Local shell gate plus agent-projected hooks and policy | Blocked after full qualification |
| `ci-guard` `1.0.0` | `856bce5924fbdbb519e5aa61f796bf8aca6f1f36` | Five prompt commands and two prompt hooks | Advisory only |
| `tdd` `1.1.2` | `ad730e238e85aa1cd11e998a1fabd5456883a0cc` | Four prompt commands and three prompt hooks | Agent-driven, not gate owner |
| `verify` `1.0.3` | `a6d8f3804d2e2877485b60f363ed025a3ff8b42f` | One prompt command, one prompt hook, config loaders | Agent judgment |
| `verify-tasks` `1.0.0` | `09942f6274820ab07f5cc45b28ed779736aa3090` | Prompt command and hook | Agent judgment |
| `trace` `1.0.0` | `aadf25d7e6507a336b4f882256596ae173e10795` | Four prompt commands | Trace advice, not proof |
| `v-model` `0.6.0` | `3b39ad3ccbdf7fea45ddd3bf6a8341cc0290d565` | Deterministic scripts, 14 commands, and new V-model artifacts | Too broad; adds another specification owner |
| `spectest` `1.0.0` | `646a2d14bd3066980adef61f3d8640d4fc4290fc` | Four prompt commands and one hook | Agent-driven test design |
| `patchwarden-evidence` `1.0.1` | `fd761fdedb4068b12e9816e267505ae8ddae7b62` | Prompt commands and hooks over PatchWarden MCP | Adds an external service; evidence packaging is not verification |
| `docguard` `0.33.0` | `87c8f66ffe1012c705ef6f7e1aa596d6c73e7ab8` | Node CLI, MCP server, commands, hooks, and scripts | Broad documentation system, not the missing gate |

The prompt-only candidates can recommend checks, but their output is advisory.
`v-model`, PatchWarden, and DocGuard add more ownership or runtime than the
standard profile needs. Full lifecycle testing was therefore limited to
`gates`, the smallest candidate with a local deterministic entrypoint.

## Leading candidate result

The exact `gates` release installed through current Spec Kit. Its full upstream
suite passed after installing its locked npm dependencies and declared
ShellCheck version. Direct tests proved distinct success, gate-failure, and
malformed-input states.

It still does not meet the ProofTank contract. A `Complete` feature with checked
tasks and no executable acceptance block returned success. Its health check
also called that feature enforced. The release has no deterministic rule that
maps every `REQ-*` and `INV-*` identifier to an executable check.

The release also depends on an agent command to project its runtime after
installation. Current Spec Kit warned that its policy template was not
scaffolded. Disable and uninstall left the projected runtime executable. Its
locked npm dependency audit reported two high-severity advisories.

The complete component record is in
`upstream/reviews/spec-gates.md`.

## Review scope

PM-026 used upstream qualification, source inspection, and disposable fixtures.
It did not start a clean-context adversarial review cycle because no meaningful
code or runtime configuration changed. The simple-and-relevant finding challenge
applies only to findings reported by those adversarial review subagents.

## Safe remaining state

The preset, workflow, bundle, and catalog composition stay unchanged. They
continue to require project-native tests and lint, and they must report missing
deterministic evidence as `unknown`. The rejected provider remains visible in
the registry so catalog discovery cannot be mistaken for approval.
