# What ProofTank does not prove

ProofTank must not market ordinary evidence as mathematical proof.

## It does not prove that all software is correct

Tests cover selected executions. Static tools use models and approximations. Structural graphs can miss edges. Formal tools prove only the stated property under stated assumptions.

## It does not make agent judgment authoritative

Research summaries, architecture proposals, reviews, and remembered context remain advisory until a reviewed repository artifact adopts them.

## It does not make an empty result meaningful by itself

Examples:

- zero callers from a code graph does not prove dead code;
- zero selected tests does not prove that no tests are needed;
- no reported vulnerability does not prove security;
- no observed race does not prove race freedom.

## It does not remove human responsibility

Humans still approve:

- product intent;
- high-impact architecture;
- contract changes;
- security and privacy decisions;
- waivers;
- release risk.

## It does not guarantee upstream sustainability

Pinned providers can become unmaintained, insecure, relicensed, or incompatible. ProofTank records the dependency and supports replacement. It cannot prevent upstream change.

## It does not replace project-specific harness engineering

Each repository still needs:

- domain invariants;
- architecture boundaries;
- build and test commands;
- application diagnostics;
- logs, metrics, traces, or UI automation that agents can inspect;
- feedback rules learned from real failures.
