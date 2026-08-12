# Product charter

## Mission

Proofmill converts a software idea into a bounded implementation process and an evidence-backed delivery.

Proofmill uses existing coding agents and specialist tools. It does not replace them.

## Product category

**Audited assurance distribution for agent-built software.**

The nearest analogy is a software distribution:

- Agent harnesses are runtimes.
- GitHub Spec Kit is the process substrate and package model.
- Specialist skills and tools are packages.
- Proofmill selects, qualifies, pins, configures, and tests the composition.

## Users

MVP users work through Codex. Other harnesses are post-MVP candidates and are
not supported by the current product.

A user must not migrate to a Proofmill-specific agent runtime.

## Problem statement

A capable LLM can write working code but can still fail in two opposite ways:

- **Underbuild:** omit failure behavior, concurrency, recovery, diagnostics, or edge cases.
- **Overbuild:** add unrequested abstractions, services, dependencies, and speculative systems.

Proofmill gives the implementation agent a reviewed work packet that defines both:

- the minimum behavior that must exist;
- the maximum scope that the change can enter.

## Product principles

1. Research before invention when the mechanism is expensive to reverse.
2. Integrate before build.
3. One repository owns project truth.
4. One project has one authoritative specification system.
5. A short map points to deeper documentation.
6. Mechanical checks enforce important rules.
7. Agent judgment proposes. Deterministic evidence gates.
8. Unknown does not pass.
9. Ceremony follows risk.
10. Bugs and review findings improve the permanent harness.
11. Provider replacement is normal.
12. The benchmark can disprove the product claim.

## Primary outcome

The product does not optimize for minimum first-pass tokens.

The primary economic measure is:

```text
lifecycle cost per accepted capability
```

This includes:

- generation;
- research;
- review;
- repair;
- regression handling;
- human intervention;
- incident diagnosis.

## Version 0 deliverable

- A `proofmill-lite` design and one working `proofmill-standard` composition.
- A postponed `proofmill-critical` roadmap item, not a workflow.
- One working `proofmill-standard` bundle.
- Codex conformance.
- Upstream qualification records.
- Checkbook benchmark.
- Measured gap report.

The first comparable benchmark found no accepted-behavior gain from Proofmill
Standard. Version 0 therefore claims a pinned, bounded Codex process, not lower
lifecycle cost or higher implementation quality.

## Version 0 non-goals

- Hosted control plane.
- Multi-tenant service.
- Agent runtime.
- General MCP server.
- Persistent Proofmill memory.
- Code graph.
- New test framework.
- New issue tracker.
- General formal-verification system.
- Automatic contract approval.
