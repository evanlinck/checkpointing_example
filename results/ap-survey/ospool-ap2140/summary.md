# Access point survey: ospool-ap2140

From `ap_survey.sh`. The raw files next to this one hold the config, spool, held jobs, GPUs
and hold reasons; this page summarises the job history and glidein lifetimes.

871308 finished jobs in `history.txt`.

## Jobs that finished in the period

| Group | Jobs | Removed | Interrupted ≥ 1× | Interruptions per interrupted job | Badput share |
|---|---|---|---|---|---|
| CPU, not checkpointing | 638142 | 16.4% | 9.1% | 1.5 | 21.7% |
| CPU, self-checkpointing | 226818 | 3.7% | 12.8% | 1.3 | 14.3% |
| GPU, not checkpointing | 5794 | 9.1% | 3.6% | 1.3 | 19.1% |
| GPU, self-checkpointing | 554 | 22.9% | 38.6% | 1.7 | 18.9% |

## Mean time per execution, interrupted jobs only

A rough stand-in for how long jobs run before an interruption (see the notes at the top of
`ap_survey_summary.py`). Share of interrupted jobs in each range.

| Group | n | 0–1 h | 1–2 h | 2–4 h | 4–6 h | 6–8 h | 8–12 h | 12–24 h | ≥ 24 h |
|---|---|---|---|---|---|---|---|---|---|
| CPU, not checkpointing | 58284 | 55% | 13% | 17% | 8% | 3% | 3% | 1% | 0% |
| CPU, self-checkpointing | 28970 | 65% | 26% | 7% | 1% | 1% | 0% | 0% | 0% |
| GPU, not checkpointing | 211 | 52% | 42% | 4% | 0% | 0% | 0% | 1% | 0% |
| GPU, self-checkpointing | 214 | 64% | 25% | 8% | 2% | 0% | 0% | 0% | 0% |

## Vacates by reason (`NumVacatesByReason`)

| Group | Reason | Count |
|---|---|---|
| CPU, not checkpointing | StarterError | 45445 |
| CPU, not checkpointing | StartdShutdown | 20734 |
| CPU, not checkpointing | TransferInputError | 18063 |
| CPU, not checkpointing | ReconnectFailed | 15559 |
| CPU, not checkpointing | StartdHeldJob | 8223 |
| CPU, not checkpointing | TransferOutputError | 7333 |
| CPU, not checkpointing | ClaimDeactivated | 6768 |
| CPU, not checkpointing | HookPrepareJobFailure | 3749 |
| CPU, self-checkpointing | ClaimDeactivated | 14533 |
| CPU, self-checkpointing | SuccessfulCheckpoint | 11477 |
| CPU, self-checkpointing | StartdShutdown | 6357 |
| CPU, self-checkpointing | StarterError | 6272 |
| CPU, self-checkpointing | TransferInputError | 5077 |
| CPU, self-checkpointing | JobRemoved | 3796 |
| CPU, self-checkpointing | ReconnectFailed | 3116 |
| CPU, self-checkpointing | TransferOutputError | 772 |
| GPU, not checkpointing | TransferInputError | 476 |
| GPU, not checkpointing | ReconnectFailed | 221 |
| GPU, not checkpointing | StarterError | 139 |
| GPU, not checkpointing | ClaimDeactivated | 77 |
| GPU, not checkpointing | ActivationRefusedStillCleaning | 54 |
| GPU, not checkpointing | JobRemoved | 49 |
| GPU, not checkpointing | StartdShutdown | 38 |
| GPU, not checkpointing | FailedToActivateClaim | 16 |
| GPU, self-checkpointing | ClaimDeactivated | 255 |
| GPU, self-checkpointing | SuccessfulCheckpoint | 73 |
| GPU, self-checkpointing | ReconnectFailed | 31 |
| GPU, self-checkpointing | JobRemoved | 26 |
| GPU, self-checkpointing | StartdShutdown | 25 |
| GPU, self-checkpointing | UserRequest | 12 |
| GPU, self-checkpointing | StarterError | 3 |
| GPU, self-checkpointing | TransferInputError | 2 |

## Holds by reason (`NumHoldsByReason`)

| Group | Reason | Count |
|---|---|---|
| CPU, not checkpointing | UserRequest | 42408 |
| CPU, not checkpointing | JobPolicy | 12614 |
| CPU, not checkpointing | StartdHeldJob | 8176 |
| CPU, not checkpointing | TransferOutputError | 7268 |
| CPU, not checkpointing | MaxTransferInputSizeExceeded | 4502 |
| CPU, not checkpointing | HookPrepareJobFailure | 3749 |
| CPU, not checkpointing | JobExecuteExceeded | 3255 |
| CPU, not checkpointing | SystemPolicy | 1570 |
| CPU, self-checkpointing | SystemPolicy | 13353 |
| CPU, self-checkpointing | JobPolicy | 10067 |
| CPU, self-checkpointing | TransferInputError | 889 |
| CPU, self-checkpointing | TransferOutputError | 772 |
| CPU, self-checkpointing | StartdHeldJob | 106 |
| CPU, self-checkpointing | UserRequest | 104 |
| GPU, not checkpointing | JobExecuteExceeded | 18 |
| GPU, not checkpointing | StartdHeldJob | 14 |
| GPU, not checkpointing | SubmittedOnHold | 13 |
| GPU, not checkpointing | TransferOutputError | 11 |
| GPU, not checkpointing | UserRequest | 7 |
| GPU, not checkpointing | JobDurationExceeded | 7 |
| GPU, not checkpointing | TransferInputError | 7 |
| GPU, not checkpointing | JobPolicy | 6 |
| GPU, self-checkpointing | SystemPolicy | 484 |
| GPU, self-checkpointing | UserRequest | 15 |
| GPU, self-checkpointing | MaxTransferInputSizeExceeded | 2 |
| GPU, self-checkpointing | FailedToCheckpoint | 1 |
| GPU, self-checkpointing | JobPolicy | 1 |
| GPU, self-checkpointing | StartdHeldJob | 1 |
| GPU, self-checkpointing | TransferOutputError | 1 |
| GPU, self-checkpointing | SubmittedOnHold | 1 |

## Glidein lifetimes left, over all slots now

Hours from now until each slot's glidein stops taking jobs (`GLIDEIN_ToRetire`) and is
killed (`GLIDEIN_ToDie`), over 82 sites. A snapshot: it shows how much runway a job starting
now would get, not the full lifetime of a glidein.

| Range | Slots, to retire | Slots, to die |
|---|---|---|
| already past | 564 | 0 |
| 0–1 h | 1090 | 12 |
| 1–2 h | 386 | 41 |
| 2–4 h | 2132 | 79 |
| 4–6 h | 1048 | 145 |
| 6–8 h | 1801 | 112 |
| 8–12 h | 3027 | 1632 |
| 12–24 h | 9068 | 15375 |
| ≥ 24 h | 19758 | 21590 |
| undefined | 3232 | 3120 |
