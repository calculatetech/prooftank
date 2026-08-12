# PM-030 Codex contract qualification

Codex CLI `0.147.0` produced the two files in `specs/` during one measured run
on 2026-08-11. The target used Spec Kit `0.16.3.dev0` at commit
`bd595cf838cc200f84fee9e9327b643dfe277d2c` and exact-copy approved provider
skills.

The generated files are preserved without repair. The run passed the bounded
qualification because it:

- created only a specification and its requirements checklist;
- defined `REQ-001` and `INV-001`;
- carried every Proofmill contract field into the checklist;
- kept missing executable coverage and human inspection `unknown`;
- excluded agent output and the checklist from deterministic evidence; and
- left both missing deterministic mappings unchecked.

This result qualifies one Codex specification run. It does not prove
implementation behavior or general model reliability.
