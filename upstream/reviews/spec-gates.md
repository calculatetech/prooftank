# spec-gates qualification

## Identity

- Repository: <https://github.com/schwichtgit/spec-gates>
- Reviewed release: `v0.3.3`
- Reviewed commit: `b3800b9d04a7ed489b94052074c94c8980dd6d4b`
- Release archive SHA-256:
  `f2a0736e142d48b4e2764dbddfef1f8eff915a59d96e99492625bf8626f39c5b`
- License: MIT, copyright Stefan Schwichtenberg
- Review date: 2026-08-11
- Qualification state: `blocked`

The release was current in the Spec Kit community catalog during this review.
The catalog marked it `verified: false`.

## Capability and trust

spec-gates can run formatters, linters, checked tasks, and shell acceptance
blocks from one policy. Its local shell scripts give clear pass and fail exit
states for the inputs they execute.

Trust class: deterministic for an explicit configured check, but not
authoritative. It does not prove that every Proofmill requirement or invariant
has a check. A passing run cannot become a Proofmill release claim.

## Installation and written state

The tested current Spec Kit command was:

```bash
specify extension add gates --from https://github.com/schwichtgit/spec-gates/releases/download/v0.3.3/gates-0.3.3.zip
```

Spec Kit writes the release under `.specify/extensions/gates/`, adds the
extension to `.specify/extensions/.registry`, and updates
`.specify/extensions.yml`. Current Spec Kit warned that `policy.json` was not
scaffolded.

Installation alone does not create a working gate. The
`speckit.gates.init` agent command asks an agent to copy the runtime to
`.specify/gates/`, infer and approve `policy.json`, and optionally write:

- `.claude/hooks/gates/` and `.claude/settings.json`;
- `.git/hooks/pre-commit` and `.git/hooks/commit-msg`, or another configured
  Git hook path;
- `package.json`, a lockfile, `.markdownlint-cli2.jsonc`, and
  `.prettierignore`;
- later, one CI file for GitHub Actions, GitLab CI, or Jenkins.

The projection can also write `.specify/gates/attestations.jsonl`. That file is
a bounded local log, not proof by itself. No daemon or database starts.

## Commands, hooks, and network

The extension registers eight agent commands: `init`, `verify`, `doctor`,
`ci`, `upgrade`, `sync`, `propose`, and `constitution`. It also registers
optional `after_implement` and `before_constitution` hooks. Agent-boundary
runtime hooks support Claude Code, not Codex. Git and CI hooks are
harness-independent.

Verification is local. Installation contacts GitHub. Package seeding can
contact the npm registry. Contract sync and proposal commands can contact a
configured Git remote and may use the user's existing Git credentials. The
review used no token. The extension has no separate privacy control; repository
and local tool rules apply.

Run this after projection as the health check:

```bash
bash .specify/gates/doctor.sh
```

Run this as the CI gate:

```bash
bash .specify/gates/verify.sh --boundary ci --json
```

The documented exit states are 0 for success, 1 for an internal error, and 2
for a gate failure.

## Disable, update, and uninstall

`specify extension disable gates` disables the registered Spec Kit commands
and hooks. It does not disable the copied `.specify/gates/` runtime, Git hooks,
Claude hooks, or CI file. The tested copied gate still returned a gate failure
after disable.

`specify extension remove gates --force` removes the installed extension and
backs up its config. It intentionally leaves projected runtime and hook files.
The tested copied gate still ran after removal. Repository specifications and
tasks remained intact. Full removal therefore needs a reviewed manual cleanup
of every projected path.

Updates replace the installed extension. The `upgrade` agent command must copy
the new runtime into the project. It preserves the user-owned policy. Do not
update without a new pin and qualification review.

## Failure behavior and conformance

With npm dependencies and ShellCheck `0.11.0`, all upstream release tests
passed. A malformed acceptance fence returned exit 2. A passing block returned
exit 0. A failing block returned exit 2, including in a fresh shell process.
Missing required tools are reported by `doctor`; disabled policy tools can be
skipped by `verify`.

The following blockers prevent selection:

- A feature marked `Complete` with checked tasks but no executable acceptance
  blocks returned exit 0. `doctor` also returned exit 0 and called the feature
  enforced. Proofmill needs missing deterministic coverage to stay `unknown`.
- The release does not require or validate one acceptance block for every
  Proofmill requirement and invariant ID.
- Current Spec Kit reported that the policy template was not scaffolded. An
  agent conversation, not the installer, creates the operational gate.
- Disable and uninstall do not stop or remove projected enforcement.
- `npm ci` reported two high-severity advisories in the exact release lockfile:
  one for direct `markdownlint-cli2` and one for transitive `js-yaml`.
- The extension adds eight agent commands and about 6,600 lines of shell and
  hook code. That is broader than the one missing coverage check.

These findings are simple: each is visible through one install, command, or
lockfile audit. They are relevant: each affects false success, safe lifecycle,
security, or the minimum trusted surface. The candidate is blocked.

## Fallback

Keep project-native tests, lint, and schema checks. Record missing
requirement-to-check coverage as `unknown`. Do not add a Proofmill gate or
claim a release warrant. Reconsider a later release only if it requires
deterministic coverage, fixes its dependencies, and has a complete disable and
uninstall path.
