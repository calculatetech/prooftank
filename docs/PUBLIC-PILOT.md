# Codex public pilot

## Status

Proofmill Standard `0.1.0` is ready for a local Codex pilot. It is not a
published package or a cleared public product name. Codex is the only supported
MVP harness. The owner accepted `ProofTank` as the working name for this
open-source hobby project. [Name research](NAME-CLEARANCE.md) records the limits
of that decision. Existing `Proofmill` identifiers remain exact until PM-036
validates the migration.

The pilot shows that the pinned composition installs, keeps a bounded contract,
and reports missing evidence as `unknown`. It does not show a quality advantage,
lower lifecycle cost, or a release warrant.

## Prerequisites

Use an empty target repository. You need Codex, Git, Python 3 with `venv`, and
`sha256sum`. You also need network access while Python installs the exact GitHub
Spec Kit commit. The Proofmill release needs no network access after that.

## Install and check health

Follow the exact commands in the
[`0.1.0` release guide](../releases/proofmill-standard/0.1.0/README.md). Do not
replace its commit, version, or hashes with a branch or an unpinned package.

Installation is healthy only when all of these checks pass:

- the release checksum manifest passes;
- Spec Kit reports `0.16.3.dev0`;
- the Ponytail and SimpleEnglish hashes match the release guide;
- `specify preset resolve spec-template` succeeds; and
- `specify workflow info proofmill-standard` succeeds.

Keep specifications, plans, tasks, test output, and lint output in the target
repository. Provider output alone is not proof.

## Evidence and limits

- [Upstream qualification manual](UPSTREAM-QUALIFICATION.md)
- [Spec Kit review](../upstream/reviews/github-spec-kit.md)
- [Ponytail review](../upstream/reviews/ponytail.md)
- [SimpleEnglish review](../upstream/reviews/simple-english.md)
- [Codex qualification result](BOOTSTRAP-GAP-REPORT.md)
- [First comparable checkbook result](../conformance/checkbook/results/first-comparable-001/README.md)
- [Claims Proofmill does not make](WHAT-PROOFMILL-DOES-NOT-PROVE.md)

The benchmark used one run per arm. All five arms passed the 15 accepted
scenarios. Ponytail-only used the least measured time, tools, and tokens.
Proofmill Standard did not improve accepted behavior. Cost, mutation score,
change-request regression, diagnosis time, and general model behavior remain
`unknown`.

## Contribute or replace a provider

Record a proposed change in [`docs/roadmap.md`](roadmap.md) before implementation.
For a provider change, inspect current primary sources and follow the
[qualification manual](UPSTREAM-QUALIFICATION.md). Add an exact pin and review
under `upstream/reviews/`, update `upstream/registry.yml`, and run the required
install, health, failure, disable, and uninstall checks.

Do not switch providers automatically. Keep rejected candidates and negative
results. A provider can replace an active component only after its exact bytes
pass qualification and the roadmap authorizes the change.

For feedback, report the release version, Codex version, operating system,
command, exit status, and the shortest reproducible failure. Remove credentials,
repository secrets, and private source before sharing a report. Submit the
report through the
[`ProofTank` issue tracker](https://github.com/calculatetech/prooftank/issues).

## Disable or uninstall

Use only the exact disable and uninstall commands in the
[`0.1.0` release guide](../releases/proofmill-standard/0.1.0/README.md). Disabling
a required provider makes workflow preflight stop. Uninstall removes the local
Spec Kit integration and provider directories but preserves repository-owned
specifications, plans, tasks, and source files.
