# ProofTank Standard bundle

For a versioned, checksummed Codex install, use
`releases/prooftank-standard/0.2.0/README.md`. The source-checkout procedure
below remains the development path.

This local bundle uses Spec Kit `0.16.3.dev0` from commit
`bd595cf838cc200f84fee9e9327b643dfe277d2c`.

Install this composition into a separate target project. Do not run `specify
init --here` in the ProofTank source repository.

Set `prooftank_source` to this checkout and `target_project` to an empty target
directory. Then run:

```bash
set -e
prooftank_source=/absolute/path/to/prooftank
target_project=/absolute/path/to/target-project
speckit_venv=$(mktemp -d /tmp/prooftank-speckit.XXXXXX)
python3 -m venv "$speckit_venv"
"$speckit_venv/bin/pip" install \
  "git+https://github.com/github/spec-kit.git@bd595cf838cc200f84fee9e9327b643dfe277d2c"
"$speckit_venv/bin/specify" version --features --json
mkdir -p "$target_project"
cd "$target_project"
"$speckit_venv/bin/specify" init --here --integration codex --force
"$speckit_venv/bin/specify" preset add --dev \
  "$prooftank_source/presets/prooftank-contract" --priority 10
"$speckit_venv/bin/specify" workflow add --dev \
  "$prooftank_source/workflows/prooftank-standard"
"$speckit_venv/bin/specify" bundle validate \
  --path "$prooftank_source/bundles/prooftank-standard" --offline
"$speckit_venv/bin/specify" bundle install \
  "$prooftank_source/bundles/prooftank-standard" --offline
```

The version command must report `0.16.3.dev0`. The Git URL pins the reviewed
Spec Kit commit instead of trusting another `specify` executable on `PATH`.

Current Spec Kit bundles cannot install agent skills or local component folders.
Before the workflow starts, install Ponytail `4.9.0` from its reviewed commit
and the Codex-normalized SimpleEnglish `1.2.0` from this ProofTank release into
`.agents/skills/`:

```bash
set -e
provider_checkout=$(mktemp -d /tmp/prooftank-providers.XXXXXX)
git clone \
  https://github.com/DietrichGebert/ponytail.git \
  "$provider_checkout/ponytail"
git -C "$provider_checkout/ponytail" checkout --detach 2ed6c52c9d7e5e56942508591085fd45dea277d3
mkdir -p .agents/skills
test ! -e .agents/skills/ponytail
test ! -e .agents/skills/simple-english
cp -R "$provider_checkout/ponytail/skills/ponytail" .agents/skills/ponytail
cp -R \
  "$prooftank_source/releases/prooftank-standard/0.2.0/skills/simple-english" \
  .agents/skills/simple-english
```

Run these provider checks:

```bash
set -e
test "$(sha256sum .agents/skills/ponytail/SKILL.md | cut -d' ' -f1)" = \
  1316a2f3f95741d2300b116fe0c2d81ce4a9568656ed0a62643f54aaf09957f2
simple_english_skill=.agents/skills/simple-english
se_refs="$simple_english_skill/references"
test "$(sha256sum "$simple_english_skill/SKILL.md" | cut -d' ' -f1)" = \
  7640dff70b1b95a1a77f00837cb678ee6e0a200ca05cbd4eb615fc21fb8806ad
test "$(sha256sum "$se_refs/checklist.md" | cut -d' ' -f1)" = \
  c90c3834fa691da11e23f11ccb922ad09ddb18fbea04004ad047b5070c0ae846
test "$(sha256sum "$se_refs/use-cases.md" | cut -d' ' -f1)" = \
  a875819fe39687282b893d92d9d5f91c89685a01e21ffed0579d8873d4de6a68
```

The install health check validates both provider skill copies. The workflow
checks provider presence as its first step and stops if either skill is absent.
The current qualification limits are in the two upstream reviews.

Do not update Ponytail with the marketplace command or SimpleEnglish with the
unpinned `npx` command. Review and pin a new commit, rebuild the Codex-normalized
release directory, move the old directory aside, and verify the new hashes.

To disable or uninstall either pinned provider, move or remove its directory
under `.agents/skills/`. The workflow then stops at provider preflight. These
operations do not remove specifications, plans, tasks, or source files.

Run `"$speckit_venv/bin/specify" preset resolve spec-template` as the
composition health check. Use the same executable for `workflow info
prooftank-standard` and `bundle list`.

To disable the contract, run `"$speckit_venv/bin/specify" preset disable
prooftank-contract`. To enable it again, run `"$speckit_venv/bin/specify"
preset enable prooftank-contract`.

To remove the composition, run:

```bash
set -e
"$speckit_venv/bin/specify" bundle remove prooftank-standard
"$speckit_venv/bin/specify" workflow remove prooftank-standard
"$speckit_venv/bin/specify" preset remove prooftank-contract
"$speckit_venv/bin/specify" integration uninstall codex
```

The remove commands preserve feature specifications, plans, tasks, and other
repository truth.
