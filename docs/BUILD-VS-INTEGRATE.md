# Build versus integrate

## Decision rule

Build a Proofmill capability only when all conditions are true:

1. The capability is required by a measured user or benchmark need.
2. No approved upstream satisfies it.
3. Adapting an upstream costs more or creates more risk than a focused implementation.
4. The new code has a narrow owner and test plan.
5. The implementation does not create a second source of truth.

## Capability map

| Function | Integrate | Build in version 0? |
|---|---|---:|
| Agent loop and tools | Codex for the MVP | no |
| Specification process | GitHub Spec Kit | no |
| Minimal implementation | Ponytail | no |
| Controlled technical language | SimpleEnglish | no |
| Prior-art research | manual primary-source research; NeuroArxiv blocked | no |
| Divergent architecture review | fresh Codex review; ADHD blocked | no |
| Cross-session memory | repository docs and Git; Cavemem blocked | no |
| Structural code intelligence | native search; CBM blocked; CodeGraph unreviewed | no |
| Prose compression | normal prose; Caveman unreviewed | no |
| Compact-spec and backprop ideas | Cavekit comparison only | no second spec engine |
| Harness discovery | pinned best-of-Agent-Harnesses JSON, manual only | no |
| Risk profile templates | Proofmill | yes, declarative |
| Contract floor and ceiling | Proofmill preset | yes, declarative |
| Provider qualification record | Proofmill | yes, files and tests |
| Cross-harness conformance | postponed | no |
| Checkbook benchmark | Proofmill | yes |
| Evidence-state vocabulary | Proofmill | yes, declarative first |
| Release warrant | native tests, lint, checksums, unknowns | no measured need |
| Provider-health command | exact provider-native checks | no measured need |

## Measured MVP decision

Integrate only Codex, the pinned GitHub Spec Kit source, the exact Ponytail
skill, and the Codex-normalized SimpleEnglish skill. Keep Proofmill code-free:
its owned product surface is declarative presets, workflows, policy, reviews,
release files, and benchmark tooling.

Do not integrate CBM, Cavemem, NeuroArxiv, ADHD, spec-gates, or another harness.
Cavekit remains comparison-only. best-of-Agent-Harnesses remains a manual
maintenance signal. CodeGraph and Caveman are unreviewed backlog candidates,
not active providers.

The first comparable batch does not support a quality or lifecycle-cost benefit
for Proofmill Standard. It supports only the narrower claim that the pinned
Codex composition installs, carries a bounded contract, preserves unknowns, and
can produce correct software. No new runtime, release warrant, provider-health
layer, graph, memory, database, daemon, or adapter is authorized.

## Known candidates to inspect before custom code

The bootstrap agent must inspect the current Spec Kit catalog for capabilities such as:

- requirements traceability;
- V-Model workflows;
- architecture guards;
- CI guards;
- TDD evidence;
- mutation checks;
- verification and task verification;
- deterministic quality gates;
- evidence packs;
- worktree isolation;
- brownfield bootstrap;
- research and red-team review.

Catalog presence is not approval. Review source, license, behavior, and maintenance.

## Sustainability input

Use the exact reviewed `harnesses.json` revision from
best-of-Agent-Harnesses only to decide what deserves primary-source inspection.
Check its capture date, graveyard, movement, license signal, and linked evidence.
Then inspect the named provider's own current repository before changing any
Proofmill record.

Never install its MCP server for this check. Never change a component pin,
qualification state, or supported harness from stars, ranks, or editorial
ratings. If the list or a linked source is unavailable, record the signal as
unknown and use manual upstream review.

## Release-warrant decision

Do not build or integrate a release-warrant extension for the MVP. The first
comparable benchmark gave every arm the same 15 of 15 accepted behaviors and
showed no Proofmill quality gain. It did not expose a release decision that
needs another owner.

The qualified `spec-gates` candidate is not a fallback: it lets a complete
feature with no executable acceptance block pass, and its projected runtime
survives disable and removal. Keep project-native tests, lint, release
checksums, and explicit unknowns. Reopen this decision only after a preserved
failure shows that those controls cannot express a required release decision.

## Provider-health decision

Do not build or integrate a shared provider-health extension for the MVP. Use
the provider's own smallest exact check:

- Spec Kit reports its version and feature set.
- Ponytail and SimpleEnglish use release hashes; their source tests remain
  provider qualification evidence.
- The standard workflow stops when either required skill is missing.
- A blocked optional provider stays absent and uses its documented native
  fallback.

Do not translate unavailable into success. Record failed, stale, degraded,
unavailable, and unknown without collapsing them. Reopen this decision only
after a preserved provider incident cannot be represented or recovered with
the exact existing commands.
