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
suite. Proofmill added process cost without a measured quality gain.
