# GitHub Spec Kit qualification

## Identity

- Repository and homepage: <https://github.com/github/spec-kit>
- Reviewed commit: `bd595cf838cc200f84fee9e9327b643dfe277d2c`
- Source version: `0.16.3.dev0`
- Latest release seen during review: `v0.16.2`
- Commit date: 2026-08-11 UTC
- License: MIT, copyright GitHub, Inc.
- Activity: The reviewed commit was current on 2026-08-11. On 2026-08-12,
  upstream `HEAD` was `7dd706880e73cd05ccda95fb8d5ce6cf2d652ae4`.
  Proofmill did not update because that commit has not been qualified.

## Capability and trust

Spec Kit supplies the specification process, preset composition, workflows,
bundles, integration scaffolds, and artifact analysis. The CLI is a
deterministic installer and schema validator. Agent-generated content stays
advisory until a human reviews it. Reviewed repository artifacts can then become
authoritative.

Qualification state: `pilot`.

## Installation and updates

Install the reviewed source with:

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@bd595cf838cc200f84fee9e9327b643dfe277d2c
```

The bootstrap test built the same commit in an isolated Python environment. Run
`specify version --features --json` as the health check. Do not use
`specify self upgrade` for this composition. That command changes the pin.

## Files, configuration, hooks, and commands

The Python tool installation writes an isolated tool environment and a `specify`
executable. The exact tool path depends on `uv`, `pipx`, or `pip`.

`specify init --here --integration codex` writes:

- `.specify/` templates, scripts, memory, workflow state, integration state, and
  local registries;
- `.agents/skills/speckit-*/SKILL.md` for Codex;
- managed ignore and provenance files under `.specify/`.

The current Codex integration can write `.codex/config.toml` when an installed
component registers supported lifecycle events. The tested core composition did
not write this file or register hooks.

The core Codex skills are `speckit-constitution`, `speckit-specify`,
`speckit-plan`, `speckit-tasks`, `speckit-taskstoissues`, `speckit-implement`,
`speckit-converge`, `speckit-clarify`, `speckit-analyze`, and
`speckit-checklist`.

The CLI starts no persistent process. A workflow dispatch can start the selected
agent command. The Codex adapter uses `codex exec`.

## Format and catalog boundary

The reviewed extension format is `extension.yml` with
`schema_version: "1.0"`. It declares component identity and compatibility, then
can provide commands, replacement templates, scripts, configuration templates,
core-command hooks, and agent runtime events. It can also carry tags and default
configuration. Presets, not extensions, own composable template strategies such
as `append`.

A clean CLI fixture installed the pinned source's template extension. The CLI
wrote `.specify/extensions.yml`, `.specify/extensions/.registry`, the extension
tree, and its scaffolded configuration. It registered one command and one hook.
Removal backed up configuration and removed managed registration.

The built-in integration, preset, workflow, workflow-step, extension, and
bundle catalog stacks have a default source and a community source. The default
source is install-allowed. The community source is discovery-only. Spec Kit
calls some default entries official, but this means upstream-maintained; it does
not mean independently audited by Proofmill.

Community maintainers check submission metadata and format. They do not review,
audit, endorse, or support the component code. Catalog `verified` metadata has
no Proofmill approval effect. An explicit project or user catalog can be marked
install-allowed, and a direct `--from` URL can bypass catalog selection after a
warning. Both paths still need Proofmill qualification.

The built-in catalog URLs use the upstream `main` branch. The reviewed Spec Kit
commit does not pin their future contents. Proofmill therefore records every
accepted component with its own exact commit or release in
`upstream/registry.yml`.

## Network, credentials, and privacy

Source installation contacts GitHub. Python dependency installation can contact
the selected package index. Project initialization from the built package is
offline.

Catalog, extension, preset, workflow, bundle, authentication, and update
commands can contact configured HTTPS sources. The built-in catalogs use
`raw.githubusercontent.com` and track the upstream `main` branch. Release
downloads commonly use `github.com`.
Private sources can use tokens from Spec Kit authentication configuration.

The tested local composition used no credential and no runtime network access.
Spec Kit keeps project state in repository files. Catalog caches and user
catalog configuration can exist outside the repository.

## Disable and uninstall

Use `specify preset disable <id>` to remove a preset from template resolution
without erasing it. Use the matching `enable` command to restore it.

Use these commands to remove project components:

```bash
specify bundle remove <id>
specify workflow remove <id>
specify preset remove <id>
specify integration uninstall codex
```

Use `uv tool uninstall specify-cli` to remove the CLI. Integration removal
preserves `.specify/` and feature artifacts. Modified managed files can require
`--force` for removal.

## Failure behavior and fallback

Schema errors return a nonzero exit and list the invalid fields. Offline bundle
validation warns about unresolved remote references. An unreachable catalog can
produce an unknown result instead of a hard failure. Bundle installation
attempts best-effort rollback, but partial files can remain after rollback
errors.

A community catalog entry can appear in search and info output but cannot be
installed by ID from the built-in discovery-only source. Marking another source
install-allowed changes that permission only. It does not attest to source
quality, safety, or correctness.

Bundle pins apply when the bundle installs or updates a component. An already
installed component is skipped by ID without a version comparison. Therefore,
install local components from reviewed paths before bundle validation, and
inspect their registries.

If Spec Kit is unavailable, keep the reviewed specification, plan, tasks, and
evidence as normal repository Markdown. Do not create a second specification
owner.

## Conformance results

- `specify version --features --json` reported `0.16.3.dev0` and workflow
  support.
- The CLI installed the Codex integration, the Proofmill preset, and the
  Proofmill workflow in a clean fixture.
- The CLI listed default extension, preset, workflow, workflow-step,
  integration, and bundle sources as install-allowed and their community
  sources as discovery-only.
- The pinned template `extension.yml` installed in a clean fixture, scaffolded
  its configuration, registered one command and one hook, and removed cleanly
  with a configuration backup.
- `specify bundle validate --offline` accepted the local bundle.
- A malformed bundle schema returned exit 1.
- Preset disable and enable changed template resolution as documented.
- Bundle, workflow, preset, and Codex integration removal preserved the dry-run
  specification.
- One Codex dry run created `spec.md`, `checklists/requirements.md`, and
  `.specify/feature.json` only.

## Known limitations

A local bundle does not install custom component directories carried beside
`bundle.yml`. Custom components need prior local installation or install-allowed
HTTPS catalogs. The local Proofmill bundle therefore records two already
installed components and reports `0 added`.

Core `speckit.analyze` and `speckit.converge` use agent judgment. They do not
make deterministic release claims.
