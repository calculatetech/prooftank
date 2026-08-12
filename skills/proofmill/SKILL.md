---
name: proofmill
version: 0.1-draft
description: Selects the smallest reliable Proofmill workflow for a coding task. Routes work to lite, standard, or critical assurance. Uses repository specifications as truth, existing providers for research, design, clarity, minimal implementation, graph observations, and memory. Produces a bounded work packet before implementation. Never treats agent opinion, graph absence, or memory as proof.
---

# Proofmill

Use this skill for non-trivial coding work in a Proofmill repository.

## 1. Load repository truth

Read the constitution, decisions, current specification, plan, and tasks.

Do not replace repository truth with memory or provider output.

## 2. Classify the change

### Lite

Choose lite only when the change is narrow, reversible, and low risk.

Examples:

- local display fix;
- small parser correction with one owner;
- isolated utility change;
- typo or documentation correction.

### Standard

Choose standard for shared behavior, database changes, APIs, or normal product features.

### Critical

Choose critical when the task includes money, security, destructive behavior, concurrency, durable state, restart recovery, migration, ABI, or public protocol changes.

If uncertain between two grades, choose the higher grade and state why.

A human can approve a lower grade.

## 3. Select providers

Use only qualified and available providers.

- Use NeuroArxiv only when prior art can change an expensive technical mechanism.
- Use ADHD only when multiple viable designs exist and the choice is expensive to reverse.
- Use CBM only as structural observation.
- Use Cavemem only to retrieve possible prior lessons.
- Use SimpleEnglish for technical instructions.
- Use Ponytail after the work packet is approved.

Provider failure must remain visible.

Use the documented fallback when an optional provider is absent.

## 4. Create the bounded work packet

Write:

```yaml
profile: lite|standard|critical
must_do: []
must_not_do: []
may_do: []
stop_when: []
required_checks: []
known_unknowns: []
providers:
  used: []
  unavailable: []
  degraded: []
```

The packet must cover the full requested behavior.

The packet must forbid unrequested expansion.

## 5. Implement minimally

Apply Ponytail after you understand the full path.

Reuse existing code, standard libraries, platform features, and installed dependencies before adding new code.

Do not remove required validation, security, data protection, accessibility, or diagnostics.

## 6. Verify

Run the required native checks.

For standard and critical work, map each required behavior to evidence.

Report these states separately:

- passed;
- failed;
- stale;
- unknown;
- degraded;
- waived.

Unknown does not pass.

## 7. Backpropagate defects

When a test or review finds a recurring defect class:

1. identify the root cause;
2. add or strengthen an invariant;
3. add a regression check;
4. record the lesson in repository artifacts;
5. keep memory as a retrieval aid only.

## Output

Return:

1. selected profile;
2. bounded work packet;
3. implementation summary;
4. evidence summary;
5. unknowns and degraded providers;
6. next permitted step.
