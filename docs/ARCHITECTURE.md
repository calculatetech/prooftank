# Architecture

## Three layers

### 1. Agent runtime

Examples:

- Codex.
- Claude Code.
- OpenCode.
- Pi.
- OpenHarness.

The runtime owns the model loop, tool execution, context, permissions, and user interface.
Codex is the only supported MVP runtime. The other examples are postponed
post-MVP candidates.

### 2. Development-process substrate

GitHub Spec Kit owns:

- constitution;
- specification;
- clarification;
- plan;
- tasks;
- implementation flow;
- artifact analysis;
- convergence;
- presets, extensions, workflows, catalogs, and bundles.

### 3. ProofTank assurance distribution

ProofTank owns:

- approved composition;
- risk profiles;
- qualification records;
- scope boundaries;
- provider trust classes;
- conformance tests;
- evidence-state semantics;
- benchmark and gap analysis.

## Information flow

```text
idea
  ↓
risk classification
  ↓
optional prior-art and design exploration
  ↓
reviewed specification
  ↓
bounded work packet
  ↓
minimal implementation
  ↓
project-native build, test, lint, analysis, and runtime checks
  ↓
artifact consistency and traceability checks
  ↓
release evidence or explicit unknowns
```

## Authority model

| Artifact or result | Trust class | Can govern release? |
|---|---|---:|
| Reviewed repository specification | authoritative | yes |
| Human approval or waiver | authoritative | yes |
| Project-native test with current revision | deterministic | yes |
| Static linter or schema check | deterministic | yes |
| CBM impact result | observational | no, alone |
| NeuroArxiv recommendation | advisory | no |
| ADHD design selection | advisory | no |
| Cavemem retrieval | advisory | no |
| LLM review | advisory | no, alone |

CBM, NeuroArxiv, ADHD, and Cavemem are trust-class examples only. Their current
qualifications are blocked and they are not part of the MVP composition.

## Work-packet model

```yaml
must_do:
  - behavior and invariants that must exist
must_not_do:
  - scope that the agent must not enter
may_do:
  - implementation freedom inside the boundary
stop_when:
  - objective completion conditions
```

The contract sets a floor and a ceiling.

## Provider replacement

Project truth must not depend on a provider-specific database or conversation.

A provider can be replaced when:

- its capability is no longer needed;
- its license changes;
- it becomes unmaintained;
- a safer or better provider passes qualification;
- a user selects a different approved provider.

A provider change requires:

- updated registry pin;
- conformance run;
- migration or removal test;
- no loss of authoritative repository artifacts.

## Why no ProofTank runtime in version 0

A new runtime would add:

- installation and update risk;
- permission and sandbox surface;
- process lifecycle complexity;
- persistent state ownership;
- compatibility work;
- duplicated features.

The benchmark must first show that existing harness and Spec Kit interfaces cannot carry the required workflow.
