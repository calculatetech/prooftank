# Generated application quality audit

Audit only the candidate directory supplied to you. Do not inspect sibling
candidates, benchmark arms, model logs, efficiency results, or repository
history. Run tests only through the supplied sandbox command.

Find one root cause once. A finding must be actionable and cite an existing
candidate file and line. Use severity `critical`, `high`, `medium`, or `low` and
lens `correctness`, `production`, `security`, or `maintainability`. Optional
polish is not a finding.

Inspect correctness, failure atomicity, concurrency, durability, input
boundaries, secrets, injection, denial of service, observability, packaging,
operations, and maintainability. Passing tests are evidence only for the
behavior they exercise. Their count is not a quality measure.

Record every named audit surface as `checked`, `finding`, or `unknown`. A
checked or finding surface needs file-and-line evidence. An unknown surface
needs a reason and must not claim evidence. Record the exact supplied sandbox
command, exit status, and observed outcome; if it could not run, use `null` and
state why.

Score each dimension from one to five. One means the quality cannot be
established or a blocking design problem exists. Three means workable with
clear gaps. Five means clear, deliberate, and production-credible. Every score
needs file-and-line evidence.

- `single_outcome_ownership`: one clear code path owns each business transition
  and result without duplicated or competing rules.
- `code_alone_readability`: names, structure, and local control flow explain the
  ordinary design without external planning documents.
- `cohesion`: related responsibilities stay together and unrelated concerns do
  not accumulate in one unit.
- `change_locality`: a likely rule change has one obvious, bounded edit surface.
- `invariant_visibility`: money, dates, versions, atomicity, closure, reversal,
  and audit rules are explicit near their enforcement.
- `error_model_clarity`: failures are stable, useful, and consistent across the
  public interface.
- `accidental_complexity`: nesting, branching, duplication, indirection, and
  state mutation are no greater than the behavior needs.
- `test_confidence`: tests exercise important failure paths and design risks,
  independent of count or size.
- `operational_clarity`: setup, lifecycle, diagnostics, recovery, and support
  expectations are credible for production.
- `production_ownership`: a maintainer could understand, change, diagnose, and
  take on-call responsibility for this application.

Return one JSON object with this shape and no prose outside it:

```json
{
  "schema_version": "1.0",
  "candidate_id": "candidate-N",
  "findings": [
    {
      "id": "F-001",
      "severity": "high",
      "lens": "correctness",
      "title": "Short root-cause title",
      "evidence": [
        {"path": "checkbook.py", "line": 1, "detail": "What the code shows"}
      ],
      "impact": "Why this matters",
      "remediation": "Smallest credible fix"
    }
  ],
  "production_blockers": ["F-001"],
  "security_posture": "Concise assessment",
  "strongest_quality": "Concise evidence-backed strength",
  "weakest_quality": "Concise evidence-backed weakness",
  "dimensions": {
    "single_outcome_ownership": {
      "score": 3,
      "evidence": [
        {"path": "checkbook.py", "line": 1, "detail": "Why this score fits"}
      ]
    }
  },
  "overall_readiness": {"score": 3, "rationale": "Concise rationale"},
  "take_production_ownership": {
    "answer": "conditional",
    "conditions": ["Condition that must be met"],
    "rationale": "Concise rationale"
  },
  "test_confidence": {
    "supplied": "What the tests genuinely establish",
    "gaps": ["Important behavior they do not establish"]
  },
  "audit_surfaces": {
    "correctness": {
      "status": "checked",
      "detail": "What was established",
      "evidence": [
        {"path": "checkbook.py", "line": 1, "detail": "What the code shows"}
      ]
    }
  },
  "verification": {
    "command": "Exact supplied sandbox command",
    "exit_status": 0,
    "outcome": "What ran and what happened",
    "unknown_reason": null
  }
}
```

The `dimensions` object must contain all ten named dimensions and
`audit_surfaces` must contain all twelve named surfaces. A finding-free report
is valid only after every required surface and dimension is addressed.
