# SimpleEnglish qualification

## Identity

- Repository and homepage: <https://github.com/AminBlg/SimpleEnglish>
- Reviewed commit: `59bf6702197a5aadc96d197ea17f290d8d50dcd3`
- Declared source version: `1.2.0`
- Latest release tag: `v1.2.0` at
  `dfd0ca7615eb6f9297d2261c932f44807a8f4c0b`
- Commit date: 2026-08-07
- License: MIT, copyright AminBlg
- Activity: The reviewed commit remained upstream `HEAD` on 2026-08-12. The
  `v1.2.0` release tag remained the latest reviewed release.

## Capability and trust

SimpleEnglish supplies technical-writing instructions based on ASD-STE100
principles. The skill is advisory. Its regex linter is deterministic for the
patterns that it counts, but it does not prove ASD-STE100 compliance.

Qualification state: `approved` for the Codex-normalized skill derived from the
reviewed commit. The only changed value is frontmatter `compatibility`, narrowed
from the upstream harness list to `codex`. The skill remains advisory. Only the
linter's explicit pattern counts are deterministic. The unpinned `npx` path is
not approved.

## Installation and updates

The upstream install command is:

```bash
npx skills add AminBlg/SimpleEnglish
```

That command selects supported agents and writes the skill to their skill
directories. It does not pin a commit. ProofTank does not use it. Install the
Codex-normalized directory from the pinned ProofTank release at
`skills/simple-english/` into `.agents/skills/simple-english/`.

Run `python3 evals/ste_lint.py --self-test` in the reviewed checkout as the
provider test. The installed health check verifies these reviewed hashes:

- Upstream `SKILL.md`:
  `b688022acbb9b9b1293f8f3da9bc6305f8b8c6855b0c8e96ef7393e0cf256e25`
- Installed Codex-normalized `SKILL.md`:
  `7640dff70b1b95a1a77f00837cb678ee6e0a200ca05cbd4eb615fc21fb8806ad`
- `references/checklist.md`:
  `c90c3834fa691da11e23f11ccb922ad09ddb18fbea04004ad047b5070c0ae846`
- `references/use-cases.md`:
  `a875819fe39687282b893d92d9d5f91c89685a01e21ffed0579d8873d4de6a68`

## Files, configuration, hooks, and commands

The Codex installation writes `SKILL.md` and two reference files under
`.agents/skills/simple-english/`. The installed skill declares only Codex
compatibility. The upstream repository also includes material for other
harnesses, prompts, examples, evaluation data, and a Python linter. ProofTank
does not install that material.

The Codex skill registers no hook, command process, daemon, or persistent state.
It changes no Codex configuration.

## Network, credentials, and privacy

The `npx` and skills installation path contacts the npm registry and GitHub. The
installed skill and linter make no network request and use no credential.
Optional benchmark scripts can start configured agent CLIs and send their
scenario prompts to those providers.

## Disable and uninstall

Disable the skill by not invoking it or by removing it from the active skill
set. For a visible reversible disable, move `.agents/skills/simple-english/`
outside the active skill directory. Uninstall the exact-copy Codex form by
removing that directory. The skills CLI can also remove its managed copy.

Removal does not change specifications, plans, tasks, or source code.

## Failure behavior and fallback

If the skill is absent, record the provider as `unavailable`. Stop the standard
profile before specification work. The short writing rules in `AGENTS.md` are a
degraded fallback for the lite profile only.

The linter reports only mechanical patterns. It can undercount violations and
misread unusual Markdown. Treat a clean lint report as limited deterministic
evidence, not a compliance certificate.

## Conformance results

- Codex loaded the upstream exact-copy skill during the earlier dry run. The
  normalized copy changes no instruction body or reference byte.
- The dry-run specification preserved the quoted sentence and identifiers.
- The dry-run prose used short sentences and stable terms.
- `python3 evals/ste_lint.py --self-test` found 12 violations in the bad fixture
  and zero in the clean fixture.
- `python3 -m unittest evals.test_run_pi_bench` passed all 7 tests.
- Clean install, fresh-process restart, unavailable, disable, reinstall, and
  uninstall checks passed for the exact-copy skill.
- An explicit update from commit
  `401c2934a3cbd8627bee54492a52dc7bc678b68f` replaced skill hash
  `6842eaed2dacd5fb908cc7216f7b2cd3ada72d973799b317eaa78fdf629c296b`
  with the reviewed hash. Repository truth remained unchanged.
- Four bounded Codex rewrites preserved every listed code span, command, path,
  identifier, and quoted error byte for byte with the same occurrence count.
  Inputs, protected values, and outputs are under
  `conformance/simple-english/`.

## Known limitations

Approval covers the two exact reviewed reference files and the one normalized
skill file in the pinned Codex release. The normalized file differs from
upstream only at `compatibility: codex`. Approval does not cover the mutable
`npx` path, other harness material, benchmark providers, or future commits. The
four fixtures show bounded preservation, not universal protection or
ASD-STE100 compliance.
