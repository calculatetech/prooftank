# Checkbook conformance fixture

This fixture measures whether Proofmill improves lifecycle delivery.

Use the same frozen product brief, stack, model settings, prompt, and hidden
suite across arms.

Files:

- `PRODUCT-BRIEF.md`: neutral requirements given to every arm.
- `EXPERIMENT.md`: arms, controls, hidden scenarios, and metrics.

The benchmark is approved through its first comparable result. Implementation
arms must receive `PRODUCT-BRIEF.md` but not `EXPERIMENT.md` or hidden tests.

The first comparable result is preserved under
`results/first-comparable-001/`. All arms passed the corrected contract-aligned
suite. That result did not measure generated-app quality and its quality
conclusion is superseded.

PM-037 preserves sanitized content-addressed snapshots under
`results/quality-review-001/`. Two fresh blind reviewers per candidate assess
correctness, production readiness, security, maintainability, single outcome
ownership, readability, complexity, and willingness to take production
ownership. Tests and efficiency remain context only. The completed result found
Spec Kit core strongest on single-outcome ownership, no readability or
accidental-complexity separation, and no production-ready arm. See
`results/quality-review-001/README.md`.
