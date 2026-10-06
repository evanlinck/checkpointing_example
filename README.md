# Checkpointing recipes for HTCondor

Starting points for AI training jobs that survive being stopped and restarted on HTCondor, built for [CHTC](https://chtc.cs.wisc.edu/) and the [OSPool](https://osg-htc.org/services/ospool/).

Long training runs on a shared pool get interrupted: runtime limits end them, backfill slots get reclaimed, machines go away. A job that saves its state correctly, tells HTCondor "restart me" (exit code 85) and resumes exactly where it stopped loses minutes instead of days. Each recipe here trains or fine-tunes a text-generation model, but **the subject of every recipe is checkpointing**: what to save, when, where, and how to resume.

## Status

Work in progress.

- [x] **Measure how HTCondor actually behaves** on CHTC (CPU, GPU Lab, GPU backfill) and the OSPool: signals, grace periods, which checkpoint files survive which kind of eviction, restart costs, launchers like `torchrun`. Results: [`docs/environment.md`](docs/environment.md).
- [x] [Recipe 0](recipes/00_minimal/): a minimal, dependency-free example of the five things every job needs. Tested locally and on HTCondor (CHTC: vacate, hold, hard kill; OSPool: timed checkpoints, vacate).
- [ ] Recipe 1: small GPT on TinyStories, 1 GPU.
- [ ] Recipe 2: GPT-2 124M on FineWeb-Edu, multi-GPU DDP.
- [ ] Recipe 3: ~8B full fine-tune with FSDP2 and sharded checkpoints.
- [ ] A user-facing checkpointing guide.

## What we've learned so far

From the measurements in [`docs/environment.md`](docs/environment.md):

- **Evictions give you 600 seconds.** On every slot type tested, HTCondor sends SIGTERM within seconds (usually under one) of evicting a job, then kills it 600 s later.
- **A save made after SIGTERM is lost** unless the checkpoint lives on `/staging`, or the submit file adds `when_to_transfer_output = ON_EXIT_OR_EVICT` and names the checkpoint directory in `transfer_output_files`, alongside `checkpoint_exit_code = 85`.
- **A planned exit 85 is cheap.** The job usually restarts in place within seconds, so checkpointing on a timer (~1 h) costs little and protects against hard kills.
- **Only the top process gets the signal.** Shell wrappers must `exec`; `torchrun` needs a wrapper (it kills workers after ~30 s and turns exit 85 into 1).
- **GPU jobs should set `+is_resumable = true`.** It makes backfill possible and, by CHTC policy, turns the GPU runtime limit into a restartable eviction instead of a hold.

## Layout

| Path | What it is |
|---|---|
| [`docs/`](docs/) | Measured environment, recipe specifications, and (later) the guide |
| [`probes/`](probes/) | Test jobs that measure HTCondor's checkpoint behavior. Maintainer tooling; rerun when the pool changes |
| [`results/`](results/) | Summaries of the probe runs cited by `docs/environment.md` |
| `htcondor_ckpt/` | *(coming)* Shared checkpointing code, written to become an installable package later |
| [`examples/`](examples/) | Copyable starter files: a minimal training script and submit files (more to come) |
| [`recipes/`](recipes/) | The recipes (recipe 0 so far) |
| [`CLAUDE.md`](CLAUDE.md) | Design contract and working notes used when building the recipes with Claude Code |

## License

[Apache License 2.0](LICENSE).
