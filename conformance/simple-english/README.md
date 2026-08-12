# SimpleEnglish preservation fixtures

These fixtures test the reviewed SimpleEnglish skill in pragmatic mode. Each
input contains prose that needs a rewrite and technical text that must not
change.

The four cases are:

- `contract`: specification requirements and invariants;
- `work-packet`: bounded implementation instructions;
- `error`: an error-message guide;
- `runbook`: an operational recovery procedure.

Each file under `protected/` lists literal text from its input. The matching
output must contain every listed value with the same bytes and occurrence count.
The output can change all other prose. A passing fixture shows preservation for
that run only. It does not prove full ASD-STE100 compliance.

Run each fixture in a disposable Codex project with SimpleEnglish commit
`59bf6702197a5aadc96d197ea17f290d8d50dcd3`. Ask for a pragmatic rewrite and
prohibit all work except the returned text. Preserve the model output under
`outputs/`.

On 2026-08-11, Codex CLI `0.147.0` rewrote all four inputs with the reviewed
exact-copy skill. Every protected value retained the same bytes and occurrence
count. This is bounded preservation evidence, not a language-compliance claim.
