# Recipe 4: LoRA fine-tuning on the OSPool

Spec for `recipes/04_ospool_lora/`. Built before recipe 3, at the user's request (2026-10-27): it doesn't depend on FSDP or DCP, and it turns the OSPool measurements in `docs/environment.md` §10 into a working example.

## Goal

A typical OSPool job that trains a "big" model on borrowed GPUs and survives everything the OSPool does to it. It should be readable by someone with little programming experience: numbered sections in `train.py`, a README organized like recipe 0's, a comment on every submit-file line.

## Design decisions, and the measurements behind them

| Decision | Why | Evidence |
|---|---|---|
| LoRA (rank 16, all attention and MLP projections) on Qwen2.5-1.5B (Apache-2.0), one GPU | Multi-GPU slots are scarce on the OSPool; LoRA keeps the checkpoint at ~220 MB (18.5M adapter parameters + AdamW state, fp32) | §10 GPU mix |
| The base model is input, never checkpointed; its identity (repo + commit) is saved and checked on resume | Small checkpoints; adapters only fit their base model | – |
| Base model and container through OSDF (`/ospool/apXX/data/<user>/...`), data and code from `/home` | OSPool data guide (files > 1 GB and containers via OSDF); OSDF inputs don't count against `MAX_TRANSFER_INPUT_MB` | P11d |
| Checkpoint stays far below the AP's input limit | A spooled checkpoint restored after an eviction counts as input; over the limit, the job is held | P11d |
| Spool mode: `checkpoint_exit_code`, `transfer_checkpoint_files = checkpoints`, `ON_EXIT_OR_EVICT`, `transfer_output_files = checkpoints, outputs`, `kill_sig` | Durable SIGTERM saves | §4, P2b |
| Timed checkpoint every 5 h, shortened by `runtime_limit()` to `GLIDEIN_ToDie − 15 min` and `AllowedExecuteDuration − 15 min` | Glidein ends are hard kills without SIGTERM, 104–355 s after `ToDie`; each exit 85 starts a new execution | P12a, P14a |
| Hand-off (exit 86) at `job_time_left()` (`JobStartDate + AllowedJobDuration − 15 min`) | The total-time hold (code 46) isn't auto-released on ap40; spool dies with the job | P14b, P13 |
| The DAG: `RETRY train 50 UNLESS-EXIT 2`, POST `handoff.sh` maps 0 → done, 86 → move `checkpoints/` to `resume/` and retry, other → stop | A new job gets a fresh `AllowedJobDuration`; DAGMan (scheduler universe) is exempt from ap40's duration transform | P13b (exit 86 is a normal termination), §10 config |
| The hand-off goes through `/home` (the final output), not OSDF | The checkpoint is small; `transfer_output_remaps` to OSDF only happens at the end anyway, so the simplest path suffices. A multi-GB variant would remap `checkpoints` to a new, step-named OSDF path and list it as an `osdf://` input | P13 |
| `metrics.jsonl` inside `checkpoints/` (copied from `resume/` by a new job) | One log across restarts and jobs (CLAUDE.md §7) | – |
| `request_cpus = 2` | Training uses about one CPU; ap40 holds jobs above 1.8 × `request_cpus` | §10 |
| Interval checkpointing only (no epoch mode) | Recipe 1 teaches the choice; this recipe stays short | – |

## Acceptance

- [x] `test_local.py` (CPU, tiny random Qwen2 model, no download): SIGTERM resume equivalence (identical losses), timed exit, `GLIDEIN_ToDie` stop, exit-86 hand-off through `handoff.sh` with identical losses, base-model mismatch refused. Passed 2026-10-27.
- [x] `prepare.sub`: the model directory reached OSDF via `transfer_output_remaps` (from ap2002: `/staging`), `data/` came back (2026-10-27).
- [x] Measurements (README table): 222 MB checkpoint in 2 files, saved in ~0.5 s; peak GPU memory 19.0 GB on A40, A100, H100 and RTX A5000; host 6.3 GB (`request_memory` lowered to 10 GB); ~0.9 CPUs; start-up 9–18 s.
- [x] `test_htcondor.sh` on the OSPool, all PASS (2026-10-27): timed (12 timed checkpoints), vacate and hold (resumed from the SIGTERM save, 599–600 s of the window left), fast (resumed from the last timed checkpoint), handoff (7 exits 86, each continued by a new job from `resume/`), reference.
- [x] Resume equivalence on GPUs (2026-10-28): two uninterrupted references differ by up to 0.0003 in validation loss (0.009 in training loss, at logged steps). Every interrupted test stays within 0.0007 (timed, vacate, hold, fast, handoff), the hand-off run within 0.0005 after 17 restarts (7 of them hand-offs) on A40, H100 and RTX A5000 GPUs. Plot: `recipes/04_ospool_lora/resume_equivalence_gpu.png`; `compare_runs.py` copied from recipe 1 (title and hand-off lines adapted).
- [x] The cost of one timed checkpoint: ~23 s (0.5 s save + ~22 s restart in place, median), 0.13% of 5 h. Hand-off to a new job: 2.5–13 min (median ~4).

## Open points

- ~~Whether `osdf://...?recursive` brings the model directory in under its own name~~: it does (all test runs).
- `deterministic: true` uses `warn_only=True` on GPUs (attention's backward pass has no deterministic version), so GPU resume equivalence is within noise, not exact.
