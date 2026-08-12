# Clear the product and package names

<!-- markdownlint-disable MD013 MD046 -->

This ExecPlan is a living document. Maintain it according to
`.agent/PLANS.md` and keep `docs/roadmap.md` current.

## Purpose / Big Picture

This task prevents public distribution under a product or package name that has
not received human clearance. Codex can record current exact-name searches and
collision evidence. A human owner must define the jurisdictions, goods and
services, risk tolerance, and final name decision.

## Bounded Work Packet

    profile: standard
    must_do:
      - search current official trademark and package sources for exact names
      - preserve search date, scope, results, and database limits
      - identify the human decisions required before public distribution
    must_not_do:
      - provide legal advice or declare a trademark legally clear
      - reserve, register, publish, rename, or contact a third party
      - create a package, release, website, PR, or announcement
    stop_when:
      - current preliminary evidence is recorded and human clearance is required

## Progress

- [x] (2026-08-12) Activated PM-035 after the public-pilot guide passed validation.
- [x] (2026-08-12) Searched official exact-name sources and recorded preliminary results.
- [x] (2026-08-12) Stopped for the owner's jurisdiction, classification, and clearance decision.
- [x] (2026-08-12 04:02Z) Owner accepted `ProofTank` for the open-source hobby project.
- [x] (2026-08-12 04:02Z) Created the public `calculatetech/prooftank` repository.
- [x] (2026-08-12 04:02Z) Roadmapped the bounded identifier migration as PM-036.

## Surprises & Discoveries

- Observation: An active public Python CLI already uses `ProofMill`, the
  `proofmill` distribution name, and the `proofmill` command.
  Evidence: `KanadeK/proofmill` and its current `pyproject.toml`.
- Observation: Exact npm, PyPI, crates.io, and NuGet endpoints returned 404 for
  `proofmill` and `proofmill-standard`.
  Evidence: Direct official endpoint requests on 2026-08-12.
- Observation: `ProofTank` had no exact indexed software result, GitHub name,
  common package-registry entry, or DNS record for four obvious domains.
  Evidence: Web, GitHub, npm, PyPI, crates.io, NuGet, RubyGems, and DNS checks on
  2026-08-12.
- Limitation: Official trademark applications require interactive searches, and
  the project has not defined jurisdictions or goods and services.
  Evidence: USPTO and WIPO search guidance.

## Decision Log

- Decision: Separate preliminary collision research from legal clearance.
  Rationale: Database searches can reveal conflicts but cannot define legal
  scope, confusion risk, or an acceptable business risk.
  Date/Author: 2026-08-12 / Codex.
- Decision: Accept `ProofTank` for the hobby project without claiming legal
  clearance.
  Rationale: The owner explicitly accepted the remaining risk after the bounded
  collision screen and stated that the project will not be formally marketed.
  Date/Author: 2026-08-12 / project owner and Codex.

## Outcomes & Retrospective

PM-035 is complete. It found a directly relevant software collision for
`Proofmill`; `ProofTank` passed the bounded preliminary screen and was accepted
for the open-source hobby project. The public repository exists. No legal
clearance or formal marketing claim was made, and PM-036 owns the actual rename.

## Context and Orientation

The current product name is `Proofmill`. The local release and composition use
`proofmill-standard`. `ProofTank` is the replacement candidate. No package
registry, distribution ecosystem, jurisdiction, or trademark class has been
selected.

## Plan of Work

Search official trademark and common software-package sources for exact candidate
strings. Record only preliminary evidence and source limits. Ask the owner to
make or obtain the final clearance decision.

## Concrete Steps

Work from `/home/mbeutler/Projects/proofmill`. Add documentation only. Do not
reserve names or publish artifacts.

## Validation and Acceptance

The report must distinguish an exact-name search from legal clearance, cite
current sources, state missing jurisdictions and classifications, and keep
public distribution blocked.

## Idempotence and Recovery

Searches are read-only. Repeat them near any future publication date because
registry and trademark records change.

## Artifacts and Notes

Write preliminary results to `docs/NAME-CLEARANCE.md`. Detailed command results
belong in `.agent/test-results/pm-035.md`.

## Interfaces and Dependencies

Add no interface or dependency.

Latest revision: 2026-08-12. PM-035 completed with `ProofTank` accepted as the
working hobby-project name and PM-036 owning the identifier migration.
