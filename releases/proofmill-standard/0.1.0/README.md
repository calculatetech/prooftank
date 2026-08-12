# Proofmill Standard 0.1.0 for Codex

This directory is the versioned local release. It contains the Proofmill
contract preset, standard workflow, Ponytail skill, and SimpleEnglish skill.
All component bytes are covered by `SHA256SUMS`.

The SimpleEnglish skill preserves the reviewed upstream files except for one
frontmatter value: `compatibility` is narrowed to `codex`. The release manifest
records both the upstream and installed hashes.

Use GitHub Spec Kit `0.16.3.dev0` from commit
`bd595cf838cc200f84fee9e9327b643dfe277d2c`. Install that prerequisite from its
exact commit. Do not use an unpinned package or branch.

Set `proofmill_release` to this directory and `target_project` to an empty
target directory. Then run:

```bash
set -e
proofmill_release=/absolute/path/to/releases/proofmill-standard/0.1.0
target_project=/absolute/path/to/target-project
speckit_venv=$(mktemp -d /tmp/proofmill-speckit.XXXXXX)
python3 -m venv "$speckit_venv"
"$speckit_venv/bin/pip" install \
  "git+https://github.com/github/spec-kit.git@bd595cf838cc200f84fee9e9327b643dfe277d2c"
"$speckit_venv/bin/specify" version --features --json
(cd "$proofmill_release" && sha256sum -c SHA256SUMS)
mkdir -p "$target_project"
cd "$target_project"
"$speckit_venv/bin/specify" init \
  --here --integration codex --force --ignore-agent-tools --script sh
"$speckit_venv/bin/specify" preset add --dev \
  "$proofmill_release/components/proofmill-contract" --priority 10
"$speckit_venv/bin/specify" workflow add --dev \
  "$proofmill_release/components/proofmill-standard-workflow"
mkdir -p .agents/skills
test ! -e .agents/skills/ponytail
test ! -e .agents/skills/simple-english
cp -R "$proofmill_release/skills/ponytail" .agents/skills/ponytail
cp -R "$proofmill_release/skills/simple-english" \
  .agents/skills/simple-english
```

The version command must report `0.16.3.dev0`. Run these health checks:

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
"$speckit_venv/bin/specify" preset resolve spec-template
"$speckit_venv/bin/specify" workflow info proofmill-standard
```

After the prerequisite is installed, release installation needs no external
network. The native Spec Kit commands copy the preset and workflow into the
target. The two `cp` commands copy reviewed provider bytes.

To disable a provider, move its directory to the exact disabled path. For
example, disable Ponytail with:

```bash
set -e
mkdir -p .agents/skills-disabled
test ! -e .agents/skills-disabled/ponytail
mv .agents/skills/ponytail .agents/skills-disabled/ponytail
```

The standard workflow then stops at provider preflight. To uninstall the
release, run:

```bash
set -e
"$speckit_venv/bin/specify" workflow remove proofmill-standard
"$speckit_venv/bin/specify" preset remove proofmill-contract
"$speckit_venv/bin/specify" integration uninstall codex
for provider_path in \
  .agents/skills/ponytail \
  .agents/skills/simple-english \
  .agents/skills-disabled/ponytail \
  .agents/skills-disabled/simple-english
do
  if test -e "$provider_path"; then
    rm -r -- "$provider_path"
  fi
done
```

These commands preserve specifications, plans, tasks, and source files. Remove
only the four exact active or disabled provider directories shown above.
