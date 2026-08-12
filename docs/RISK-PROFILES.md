# Risk profiles

## Classification questions

Use the highest profile whose condition applies.

1. Can a failure corrupt or lose user data?
2. Does the change affect money, identity, authorization, privacy, or security?
3. Does it add durable state, retries, restart behavior, concurrency, or
   distributed coordination?
4. Does it cross a process, language, database, or provider boundary?
5. Is the architecture expensive to reverse after release?
6. Is the affected path shared by many callers or products?

## Lite

Use for:

- local typo or clear root-cause patch;
- isolated UI behavior;
- small internal utility;
- low-risk configuration change.

Stop and reclassify before implementation continues if any classification
question becomes true during the work.

Required:

- focused specification or task statement;
- bounded work packet;
- Ponytail or equivalent minimality rules;
- focused regression check;
- current project-native tests.

Skip by default:

- NeuroArxiv;
- ADHD;
- CBM;
- cross-session memory;
- formal or mutation checks.

## Standard

Use for:

- normal product feature;
- shared-module change;
- API or schema change;
- non-trivial bug fix;
- database migration without complex recovery.

Required:

- Spec Kit specification and plan;
- invariants and acceptance scenarios;
- SimpleEnglish check;
- bounded work packet;
- Ponytail implementation;
- requirement-to-test traceability;
- current build, test, and lint evidence;
- deterministic artifact analysis.

Optional:

- native repository search for impact;
- versioned repository history for prior decisions;
- mutation testing when business logic is important.

## Critical

The critical profile is a postponed design target. The MVP does not provide a
critical workflow. Reclassify critical work for explicit human handling rather
than silently running the standard profile.

Use for:

- financial correctness;
- security and authorization;
- durable state machine;
- concurrency and coordination;
- crash and restart recovery;
- cross-language ABI;
- provider ambiguity;
- architecture that is costly to replace.

Required:

- prior-art research with citations;
- divergent and adversarial design review;
- explicit owners and prohibited owners;
- failure, retry, cancellation, restart, and concurrency rules;
- bidirectional requirement/test traceability;
- stronger verification selected for the language and risk;
- current evidence gate;
- human approval for waivers and contract changes.

Possible stronger verification:

- property-based state-machine tests;
- mutation testing;
- fuzzing;
- schedule exploration;
- sanitizer builds;
- model checking;
- formal proof for a small kernel.
