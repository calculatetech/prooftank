# Current Spec Kit composition

This document records the formats reviewed at GitHub Spec Kit commit
`bd595cf838cc200f84fee9e9327b643dfe277d2c` (`0.16.3.dev0`). The preset,
workflow, bundle, extension, and catalog formats use
`schema_version: "1.0"`.

## Preset

A preset directory contains `preset.yml` and the files that its
`provides.templates` entries name. The manifest can provide templates, commands,
and scripts. Each entry can use `replace`, `prepend`, `append`, or `wrap`.

Proofmill uses `append` for `spec-template`, `plan-template`, and
`tasks-template`. Spec Kit keeps its core templates as the base. The Proofmill
contract adds only the missing scope and evidence sections.

Install a local preset with:

```bash
specify preset add --dev ./presets/proofmill-contract --priority 10
```

## Workflow

A workflow directory contains `workflow.yml`. The manifest defines metadata,
compatible integrations, inputs, and ordered steps. A step can dispatch a
command or stop at a review gate.

Proofmill reuses the core Spec Kit commands. It starts with a deterministic
required-provider shell check, then adds review gates before planning, before
implementation, and after convergence.

Install a local workflow with:

```bash
specify workflow add --dev ./workflows/proofmill-standard
```

## Bundle

A bundle directory contains `bundle.yml` and `README.md`. The manifest pins
extension, preset, step, and workflow versions. It can also pin one integration.

Current bundles point to components. They do not install local component
directories or Codex skills. A local Proofmill install must install the preset,
workflow, Ponytail skill, and SimpleEnglish skill first. The bundle then
validates and records the Spec Kit components.

From the separate target project, use these commands after setting
`proofmill_source` to the Proofmill checkout:

```bash
specify bundle validate --path "$proofmill_source/bundles/proofmill-standard" --offline
specify bundle install "$proofmill_source/bundles/proofmill-standard" --offline
```

Offline validation cannot prove that an unresolved remote reference exists. It
reports a warning. The Proofmill validation installs both local components
first, so both references resolve locally.

## Extension

An extension directory contains `extension.yml` and every file named by that
manifest. The required top-level mappings are `extension`, `requires`, and
`provides`.

The `extension` mapping identifies the component with a lowercase ID, semantic
version, name, description, author, repository, and license. It can also state a
homepage, free-form category, and `read-only` or `read-write` effect. The
`requires` mapping states a Spec Kit version range and can list required or
optional tools.

An extension can provide:

- namespaced agent commands such as `speckit.example.check`;
- replacement templates and scripts;
- configuration templates;
- hooks around core Spec Kit commands;
- canonical agent runtime events such as `pre_tool_use`, `post_tool_use`, and
  `stop`;
- search tags and default configuration values.

Extension templates and scripts always replace the same named artifact. They
cannot use the preset-only `prepend`, `append`, or `wrap` strategies. Hook
priority controls order around Spec Kit commands. Runtime events can write the
active integration's native hook configuration. For Codex, that can include
`.codex/config.toml` and the shared `.specify/events.py` dispatcher.

Install a reviewed local extension with:

```bash
specify extension add --dev ./path/to/extension
```

Installation validates compatibility, writes or links the release under
`.specify/extensions/<id>/`, updates `.specify/extensions.yml` and
`.specify/extensions/.registry`, scaffolds declared configuration, and
registers commands with active skill-based integrations. Disable suppresses
registered commands, hooks, and events without deleting files. Remove cleans
managed registration and can back up configuration. An extension can also
project files outside its managed directory through an agent command; its own
review must record how those files are disabled and removed.

Proofmill Standard has no active extension. A future extension must have an
exact pin and pass `docs/UPSTREAM-QUALIFICATION.md` before it enters the bundle.

## Catalog

Integration, preset, workflow, workflow-step, extension, and bundle catalogs
are JSON documents with `schema_version: "1.0"`. An entry names a component,
version, source, and download. A catalog source also has an installation
policy.

The built-in stack separates two trust boundaries:

- The `default` source contains upstream-maintained or first-party entries. It
  is `install-allowed`, so the CLI can install an entry by ID.
- The `community` source contains third-party entries. It is
  `discovery-only`, so search and info commands can show an entry but an install
  by ID is refused.

Spec Kit maintainers check community submission metadata and format. They do
not audit, endorse, or support the component code. A catalog `verified` value
is source metadata, not Proofmill evidence. Default catalog placement also does
not replace Proofmill qualification.

The built-in catalog URLs point at the Spec Kit `main` branch. Their contents
can therefore change while the Proofmill Spec Kit commit stays pinned. A
Proofmill component record must keep its own exact release or commit, archive
identity when available, license, trust class, and qualification state.

Project and user catalog configuration can add another source and mark it
install-allowed. That flag is permission to install, not an approval result.
Direct `--from` installation bypasses catalog selection and shows an untrusted
source warning. Proofmill must review either path before use.

Proofmill does not publish a hosted catalog. A public catalog needs hosted,
versioned downloads. PM-031 instead publishes the inspectable local release
path `releases/proofmill-standard/0.1.0/`. It uses native local-directory
installation for the preset and workflow, pinned provider-skill files, and one
checksum file. SimpleEnglish narrows upstream compatibility metadata to Codex.
It does not follow a catalog or upstream default branch.

The local release keeps component ownership visible. Spec Kit installs its two
native components. Codex discovers the two provider skills under
`.agents/skills/`. Proofmill adds no installer or package manager.

## Codex projection

`specify init --here --integration codex` writes core Spec Kit skills to
`.agents/skills/`. Preset template fragments stay under `.specify/presets/` and
resolve at runtime. Workflow files stay under `.specify/workflows/`.

The repository feature specification is the only normative specification.
Ponytail and SimpleEnglish change agent behavior. They do not own a second
specification.
