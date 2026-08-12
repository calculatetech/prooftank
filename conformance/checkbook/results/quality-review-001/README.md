# Generated application quality result

This blind audit found a useful direction. It does not prove that one provider
is better. It measures one generated application from each arm with two fresh
reviewers.

All five applications passed the same 15 hidden scenarios. Their reviewed
quality was not equal. This is why test count, lines, tokens, and elapsed time
remain context rather than success measures.

## Result

| Arm | Critical/high findings across two reviews | Readiness | Outcome ownership | Readability | Accidental complexity |
| --- | ---: | --- | ---: | ---: | ---: |
| bare | 1/4 | 2, 2 | 3.0 | 4.0 | 4.0 |
| Ponytail | 0/5 | 2, 2 | 3.0 | 4.0 | 4.0 |
| CaveKit + Ponytail | 0/3 | 2, 2 | 2.5 | 4.0 | 4.0 |
| Spec Kit core | 0/3 | 3, 2 | 4.0 | 4.0 | 4.0 |
| Proofmill standard | 0/4 | 2, 2 | 3.0 | 4.0 | 4.0 |

The severity counts are reviewer observations, not deterministic defects.
Conflicting severity remains visible. The stronger signal is replicated root
cause and whether a maintainer can locate one authoritative business outcome.

Spec Kit core gave the clearest ownership result. Both reviewers scored it
4/5 because an explicit transaction wrapper contains the business read, write,
audit event, and returned record. Its own reviewers still found a production
blocker: commit failure sits outside rollback and stable error handling.

Proofmill standard scored 3/5 for ownership. Its generated methods often read a
precondition before entering the write transaction. It therefore did not
preserve the strongest property seen in the Spec Kit core generation. This is
the most relevant gap in the current composition.

Every arm scored 4/5 for code-alone readability and accidental complexity.
The checkbook implementations are compact and understandable. Complexity is
important, but it does not distinguish these arms. More instructions, files,
or smaller output would not address the measured weakness.

## Direction

Proceed with ProofTank, but make single-outcome ownership the primary quality
target. For each business transition, the code should make one boundary own its
precondition reads, state write, audit write, failure mapping, commit, and
returned result.

The next benchmark change should be deterministic checks derived from replicated
review findings:

- concurrent stale edits and competing reversals;
- reconciliation across a closed period;
- later reversal of closed reconciled history;
- commit, lock, and storage failures with stable operation identity;
- SQLite integer boundaries; and
- bounded CSV bytes, rows, and fields.

Do not add more process layers yet. First prove whether the standard composition
preserves the ownership property already visible in the Spec Kit core result.

## Limits

One output per arm cannot establish a general provider effect. Reviews and
scores are advisory until deterministic checks reproduce them. The compact JSON
reports preserve classifications, scores, and evidence locations, but are
structured records rather than verbatim reviewer transcripts.

The archived `sandbox.py` is the exact runner used for this audit. It allowed
4,096 processes and captured output through unbounded pipes. The current runner
adds a dynamic process allowance and bounded output; those later controls do not
apply retroactively to this result.

The private mapping commitment validates after unblinding. See `mapping.json`,
`review-manifest.json`, and `report-manifest.json` for the frozen identities and
hashes. `analysis.json` contains the machine-readable comparison.
