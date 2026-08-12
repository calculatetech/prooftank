# First comparable checkbook result

Batch `first-comparable-001` is comparable. All five arms used the same frozen
brief, prompt, Codex CLI `0.147.0`, `gpt-5.4`, medium reasoning effort,
`workspace-write` sandbox, and 30-minute timeout. The input parity audit passed
all ten checks.

## Result

| Arm | Hidden | Seconds | Tools | Input tokens | Source | Tests | Spec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bare | 15/15 | 268.183 | 16 | 312,996 | 548 | 133 | 0 |
| Ponytail | 15/15 | 224.766 | 15 | 237,746 | 571 | 116 | 0 |
| Cavekit + Ponytail | 15/15 | 514.037 | 37 | 752,641 | 611 | 218 | 69 |
| Spec Kit core | 15/15 | 630.492 | 50 | 1,786,773 | 745 | 209 | 525 |
| Proofmill Standard | 15/15 | 626.656 | 47 | 1,602,751 | 682 | 226 | 551 |

There is no quality winner in this batch. Every unchanged implementation passed
every contract-aligned hidden scenario. Ponytail-only used the least time, tool
calls, input tokens, output tokens, reasoning tokens, and test lines. The bare
arm produced the fewest source lines. Proofmill Standard used slightly less
time, fewer tools and tokens, and less source than Spec Kit core, but it did not
improve accepted behavior over any arm.

This batch does not support the Proofmill lifecycle-cost claim. It shows process
overhead without a measured quality gain for this task and model run.

## Preserved negative finding

The first hidden-suite score contained two requirements that the frozen brief
did not state. It required `closed_through` in account output and exact operation
IDs on every validation error. The brief requires exact operation IDs only for
import and reconciliation errors.

The suite was corrected and rerun against the five unchanged repositories. No
model arm was rerun or repaired. All five then passed 15 of 15. The original raw
scores remain in the ignored batch directory as negative controller evidence.

## Limits

This is one run per arm, not a replicated estimate. Cost, mutation score,
change-request regression, diagnosis time, unrequested source lines, and
abstraction counts remain `unknown`. The comparison cannot establish statistical
significance or general model behavior.

The machine-readable result is in `summary.json`. Generated repositories and
raw Codex transcripts are not product artifacts and remain outside versioned
results.
