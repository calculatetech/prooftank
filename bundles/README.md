# Bundle scaffolds

The bootstrap reviewed Spec Kit `0.16.3.dev0` at commit
`bd595cf838cc200f84fee9e9327b643dfe277d2c`.

The current local composition is in `prooftank-standard/`. Read its `README.md`
before installation.

The pinned Codex release path is in
`releases/prooftank-standard/0.2.0/`.

Planned bundles:

- `prooftank-lite`
- `prooftank-standard`
- `prooftank-critical`

`prooftank-lite` and `prooftank-critical` remain designs only.

Each bundle must:

- pin exact component versions or commits;
- state licenses;
- declare required and optional providers;
- install idempotently;
- define disable and uninstall behavior;
- preserve repository artifacts when an optional provider is removed;
- pass Codex conformance.
