# Access point survey: ap2002

From `ap_survey.sh`. The raw files next to this one hold the config, spool, held jobs, GPUs
and hold reasons; this page summarises the job history and glidein lifetimes.

1147804 finished jobs in `history.txt`.

## Jobs that finished in the period

| Group | Jobs | Removed | Interrupted ≥ 1× | Interruptions per interrupted job | Badput share |
|---|---|---|---|---|---|
| CPU, not checkpointing | 938741 | 9.2% | 1.3% | 1.4 | 7.2% |
| CPU, self-checkpointing | 177595 | 13.2% | 9.6% | 1.9 | 7.1% |
| GPU, not checkpointing | 27614 | 30.5% | 3.7% | 8.2 | 29.2% |
| GPU, self-checkpointing | 3854 | 21.4% | 16.0% | 1.9 | 9.7% |

## Mean time per execution, interrupted jobs only

A rough stand-in for how long jobs run before an interruption (see the notes at the top of
`ap_survey_summary.py`). Share of interrupted jobs in each range.

| Group | n | 0–1 h | 1–2 h | 2–4 h | 4–6 h | 6–8 h | 8–12 h | 12–24 h | ≥ 24 h |
|---|---|---|---|---|---|---|---|---|---|
| CPU, not checkpointing | 12206 | 71% | 5% | 10% | 3% | 3% | 4% | 3% | 1% |
| CPU, self-checkpointing | 16984 | 60% | 14% | 15% | 6% | 4% | 0% | 0% | 0% |
| GPU, not checkpointing | 1030 | 55% | 16% | 13% | 7% | 4% | 3% | 1% | 1% |
| GPU, self-checkpointing | 616 | 30% | 20% | 34% | 6% | 3% | 3% | 4% | 1% |

## Vacates by reason (`NumVacatesByReason`)

| Group | Reason | Count |
|---|---|---|
| CPU, not checkpointing | JobRemoved | 28512 |
| CPU, not checkpointing | TransferInputError | 15744 |
| CPU, not checkpointing | JobOutOfResources | 8251 |
| CPU, not checkpointing | InvalidDockerImage | 3883 |
| CPU, not checkpointing | TransferOutputError | 2577 |
| CPU, not checkpointing | ClaimDeactivated | 2554 |
| CPU, not checkpointing | StartdDraining | 1910 |
| CPU, not checkpointing | ActivationRefusedClaimNotFound | 1356 |
| CPU, self-checkpointing | SuccessfulCheckpoint | 25161 |
| CPU, self-checkpointing | TransferOutputError | 18713 |
| CPU, self-checkpointing | ShadowException | 11237 |
| CPU, self-checkpointing | JobOutOfResources | 3553 |
| CPU, self-checkpointing | ReconnectFailed | 2055 |
| CPU, self-checkpointing | JobRemoved | 1986 |
| CPU, self-checkpointing | StartdPreemptExpression | 1723 |
| CPU, self-checkpointing | StartdShutdown | 428 |
| GPU, not checkpointing | TransferOutputError | 842 |
| GPU, not checkpointing | StartdPreemptExpression | 398 |
| GPU, not checkpointing | TransferInputError | 282 |
| GPU, not checkpointing | JobOutOfResources | 282 |
| GPU, not checkpointing | JobRemoved | 247 |
| GPU, not checkpointing | ReconnectFailed | 206 |
| GPU, not checkpointing | StartdHeldJob | 170 |
| GPU, not checkpointing | StartdShutdown | 162 |
| GPU, self-checkpointing | SuccessfulCheckpoint | 557 |
| GPU, self-checkpointing | StartdHeldJob | 234 |
| GPU, self-checkpointing | StartdPreemptExpression | 220 |
| GPU, self-checkpointing | ReconnectFailed | 175 |
| GPU, self-checkpointing | JobRemoved | 135 |
| GPU, self-checkpointing | TransferInputError | 82 |
| GPU, self-checkpointing | TransferOutputError | 53 |
| GPU, self-checkpointing | JobOutOfResources | 36 |

## Holds by reason (`NumHoldsByReason`)

| Group | Reason | Count |
|---|---|---|
| CPU, not checkpointing | JobOutOfResources | 7067 |
| CPU, not checkpointing | InvalidDockerImage | 3883 |
| CPU, not checkpointing | UserRequest | 3605 |
| CPU, not checkpointing | TransferInputError | 3262 |
| CPU, not checkpointing | TransferOutputError | 2348 |
| CPU, not checkpointing | SubmittedOnHold | 2000 |
| CPU, not checkpointing | JobPolicy | 99 |
| CPU, not checkpointing | StartdHeldJob | 38 |
| CPU, self-checkpointing | TransferOutputError | 18489 |
| CPU, self-checkpointing | JobOutOfResources | 2551 |
| CPU, self-checkpointing | UserRequest | 1460 |
| CPU, self-checkpointing | JobPolicy | 161 |
| CPU, self-checkpointing | InvalidDockerImage | 121 |
| CPU, self-checkpointing | SubmittedOnHold | 77 |
| CPU, self-checkpointing | FailedToCheckpoint | 54 |
| CPU, self-checkpointing | TransferInputError | 27 |
| GPU, not checkpointing | UserRequest | 2681 |
| GPU, not checkpointing | TransferOutputError | 587 |
| GPU, not checkpointing | TransferInputError | 252 |
| GPU, not checkpointing | JobOutOfResources | 251 |
| GPU, not checkpointing | StartdHeldJob | 119 |
| GPU, not checkpointing | JobPolicy | 64 |
| GPU, not checkpointing | InvalidDockerImage | 62 |
| GPU, not checkpointing | SubmittedOnHold | 6 |
| GPU, self-checkpointing | UserRequest | 319 |
| GPU, self-checkpointing | StartdHeldJob | 234 |
| GPU, self-checkpointing | SubmittedOnHold | 100 |
| GPU, self-checkpointing | TransferOutputError | 50 |
| GPU, self-checkpointing | JobOutOfResources | 36 |
| GPU, self-checkpointing | TransferInputError | 34 |
| GPU, self-checkpointing | JobPolicy | 21 |
| GPU, self-checkpointing | InvalidDockerImage | 4 |

## Glidein lifetimes

No glidein slots found (not an OSPool collector?).
