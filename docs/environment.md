# Environment: what HTCondor actually does on our pools

Measured with the probe jobs in [`probes/`](../probes/) between 2026-10-01 and 2026-10-02. Every finding names the probe test that produced it and the run tag whose results live in `results/<tag>/`. The probes do no ML. They pretend to train, one step per second, and record what happens to them; see [`probes/README.md`](../probes/README.md).

Statements marked **(manual)** come from the HTCondor documentation, not from our measurements. **Open** items are listed at the end.

## 1. Pools and access

| | CHTC (CPU) | CHTC GPU Lab | CHTC GPU backfill | OSPool |
|---|---|---|---|---|
| Submit from | ap2002 | ap2002 | ap2002 | ap2002 (flocking) |
| Submit lines | (none) | `request_gpus = 1`, `+WantGPULab = true`, `+GPUJobLength = "short"` | GPU Lab lines + `+is_resumable = true` + `requirements = TARGET.BackfillSlot =?= true` | `want_ospool = true`, `requirements = (Poolname =!= "CHTC")` |
| HTCondor on EP | 25.14.0 | 25.14.0 | 25.14.0 | 25.14.1 (glidein, e.g. site MI-HORUS / SLURM) |
| EP OS | CentOS 9 | CentOS 9 | CentOS 9 | CentOS 8 |
| `/staging` mounted | yes (`HasCHTCStaging`) | yes | yes | **no** |
| Outbound internet | yes | yes | yes | yes |
| Source | P0, `smoke` | P0, `backfill` | P0, `backfill2` | P0, `ospool` |

**Access point (ap2002):** HTCondor **26.1.0** (RC, AlmaLinux 9), newer than the 25.14 on the execute points. `MachineMaxVacateTime = 10 * 60`. `MaxJobRetirementTime` is not defined in the AP's config (the slot values below come from the execute points).

**Default storage quotas (per user, checked 2026-10-02 with `get_quotas`):**

| Path | Size limit | File limit |
|---|---|---|
| `/home/<user>` | 40 GB | none |
| `/staging/<user>` | 100 GB | **1,000 files** |

These are CHTC's defaults. Users can ask CHTC to raise them.

Notes:
- **`+is_resumable = true` alone does not put a job on backfill.** It only makes the job *eligible*. Our first "backfill" run landed on an ordinary GPU Lab slot (its `ConcurrencyLimits` charged `GPULAB_MEDIUMSHORT`). Adding `requirements = TARGET.BackfillSlot =?= true` worked: P0 in `backfill2` reports `BackfillSlot = true`.
- Backfill `START` accepts GPU jobs (`RequestGPUs > 0`) that are `is_resumable`, OSPool, flocking or glidein jobs.
- `HasCHTCStaging` is itself an expression (`HasRaddusHtcCephFS`). Requiring `HasCHTCStaging =?= true` works.

## 2. Software in the job

| Item | Finding | Source |
|---|---|---|
| Container runtime | Apptainer 1.5.3 on CHTC EPs | P0, `smoke` |
| Container images | `container_image = osdf:///chtc/staging/<user>/<path>/<name>.sif` (the OSDF form of a file under `/staging/<user>/`) works on CHTC (CPU, GPU, backfill) and OSPool. OSDF caches by file name: give a rebuilt image a new name. A missing image gives a hold with HTTP 404 ("Transfer input files failure ... protocol osdf"). | P0 all runs; P7e hold in `p7-rerun` |
| Python | 3.12 in our `python312.sif`; host Python on CHTC EPs is 3.9 | P0, `smoke` |
| PyTorch | `pytorch.sif` = `python:3.12-slim` + CPU wheels → torch **2.14.1+cpu**. No GPU-enabled image tested yet. | P7g, `torchrun2` |
| `/staging` inside the container | visible and writable on CHTC | P0, P4a, `smoke`/`core-chtc` |
| `condor_chirp` | present and working on the host (`/usr/libexec/condor/condor_chirp`), **absent inside the container** | P0, `smoke` |
| Job/machine ads | `$_CONDOR_JOB_AD` and `$_CONDOR_MACHINE_AD` are readable inside the container | P0 |
| `NumJobStarts` in the sandbox job ad | counts *previous* starts (0 on the first start) and is **not updated** on an exit-85 restart. Don't use it to detect restarts. | P1, `smoke` |
| Signals ignored at start | none that matter (only SIGPIPE and SIGXFSZ, which Python ignores itself) | P0 |

## 3. Eviction: signal, grace and retirement

### Measured (`condor_vacate_job`)

| | CHTC CPU | GPU Lab | Backfill | OSPool | Source |
|---|---|---|---|---|---|
| Signal | SIGTERM | SIGTERM | SIGTERM | SIGTERM | P3a |
| Delay from vacate to signal | 0.0–0.2 s | 0.0 s | 0.2 s | 0.1–0.6 s (once 4.9 s) | P2, P3 |
| Grace before SIGKILL (default) | 599 s | 599 s | 600 s | 600 s | P3a |
| `job_max_vacate_time = 60` | 60 s | – | – | 59 s | P3b |
| `job_max_vacate_time = 900` | **899 s (not capped at 600)** | – | – | **900 s** | P3c |
| `kill_sig = SIGUSR1` | SIGUSR1 delivered | – | – | SIGUSR1 delivered | P3d |
| `condor_hold` | same as vacate: SIGTERM, 600 s grace | – | – | same | P3a hold-release |
| `condor_vacate_job -fast` | immediate SIGKILL, no signal | – | – | same | P2a, P2b, P4b |

All slot types report `MachineMaxVacateTime = 10 * 60`.

### Policy (from the machine ads)

| Slot | `MaxJobRetirementTime` | Evicted when | Source |
|---|---|---|---|
| CHTC CPU | `JobRuntimeGuarantee`: **72 h** by default; 336 h with `+LongJob`; 40 h for `want_ospool`/`want_campus_pools` jobs; 4 h for interactive, build and OSG-glidein jobs; 16 h for interactive jobs on prioritized machines | – | P0 machine ad, `smoke` |
| GPU Lab | `JobRuntimeGuarantee` = 12 / 24 / 72 / 168 h for `GPUJobLength` short / medium / mediumlong / long | `PREEMPT` only on disk overuse or `TIME_EXCEEDED`. At the time limit, `WANT_HOLD` holds the job **unless `Is_Resumable`**; resumable jobs are presumably vacated and requeued instead (inferred, not observed). | P0, `backfill` |
| Backfill | `JobRuntimeGuarantee = 30` → 30 s retirement | `PREEMPT = size(ResourceConflict) > 0`: a higher-priority claim needs the GPU. After the first 30 s of runtime, eviction means immediate SIGTERM, then SIGKILL after 600 s. Matches what `condor_vacate_job` gave us on a backfill slot. | grep of P0 machine ad, `backfill2` |
| OSPool | 10,000,000 s (1200 s if `SiteWMS_WN_Preempt`; −1/0 on disk or memory overuse) | HTCondor essentially never evicts by policy. Real evictions come from the glidein's batch allocation ending (`GLIDEIN_ToRetire`) or the site; those can't be simulated with `condor_vacate_job` and may give no SIGTERM. | P0, `ospool` |

Possible explanation for P3c: a job's `job_max_vacate_time` above `MachineMaxVacateTime` may be honored because the slot still has retirement time left. Both slots where 900 s was granted have long retirement times: 72 h on CHTC CPU, ~10⁷ s on OSPool. Backfill (30 s retirement) may cap it at 600 s. Not yet tested there.

## 4. Checkpoint durability

`A` = a planned checkpoint (save, exit 85). `B` = a later save made after SIGTERM, followed by exit 85.

| Setup | After vacate / hold | After `vacate -fast` | Tested on | Source |
|---|---|---|---|---|
| `checkpoint_exit_code = 85` + `transfer_checkpoint_files` | **B lost**, restarts from A | restarts from A | CHTC CPU, GPU Lab, backfill, OSPool | P2a, `core-chtc`, `backfill`, `backfill2`, `ospool` |
| … + `when_to_transfer_output = ON_EXIT_OR_EVICT` **and the checkpoint directory named in `transfer_output_files`** | **B survives** | restarts from A (not from scratch) | CHTC CPU, GPU Lab, backfill, OSPool | P2b, `core-chtc`, `rest-chtc`, `backfill2`, `ospool` |
| Checkpoint written directly to `/staging/...` | **B survives** (container and bare) | resumes from the previous complete checkpoint; a stale `step_*.tmp` dir is left behind | CHTC CPU, backfill | P4a, P4b, `core-chtc`, `backfill2` |
| `checkpoint_destination = osdf:///chtc/staging/...` | works, but B lost (like row 1) | – | CHTC CPU, OSPool | P6a, `rest-chtc`, `ospool` |
| `checkpoint_destination = file:///staging/...` | **fails**: upload hangs ~17 min, then "Starter failed to upload checkpoint" (code 36), hold | – | CHTC | P6b, `rest-chtc` |

Other durability facts:
- **Mid-save evictions (manual):** the HTCondor manual warns that an eviction "can happen at any time, including while the code is updating its checkpoint file(s)", and that with eviction transfers a half-written file can overwrite the previous complete one. Writing to a temporary name and renaming (what recipe 0 and `CheckpointStore` do) means a transfer only ever contains complete checkpoints, plus at most a `.tmp` leftover.
- **`condor_evicted_files get <job>`** (after vacate + hold) copies the files HTCondor kept into `<job>/`. For recipe 0 it returned exactly `checkpoints/checkpoint.pt` from the eviction-time transfer: the save made after SIGTERM, which the released job resumed from. (recipe 0 `test_htcondor.sh inspect`, CHTC, 2026-10-06)
- **`condor_ssh_to_job`** is turned off for GPU jobs on CHTC (policy); it works for CPU jobs.
- **Exit 0 in response to a vacate does not complete the job.** HTCondor ignores the exit code during a vacate and requeues. (P2c)
- **No SIGTERM handler at all:** the process dies at once and restarts from A. (P2d)
- **A path listed in `transfer_checkpoint_files` that doesn't exist** on exit 85 puts the job on hold at once ("Starter failed to upload checkpoint", code 36). List one directory that always exists. (P8a)
- An exit 85 with an empty checkpoint directory is accepted. (P8d)
- Twelve exit-85s 5 s apart: no throttling. (P8b)
- Without `checkpoint_exit_code`, exit 85 simply ends the job with return value 85. (P8c)

## 5. Restarts

| | Finding | Source |
|---|---|---|
| After a planned exit 85 | Normally restarts **in the same sandbox on the same host**, 0–7 s later. Files outside the checkpoint survive, nested checkpoint directories transfer, stdout/stderr are **appended**. | P1, all sites |
| Exception | Once (P7a, `rest-chtc`) HTCondor rescheduled to a new host after exit 85: "Rescheduling self-checkpoint job after checkpoint upload because reactivating the claim would have failed" (code 1025). **Never assume the same sandbox.** | P7a |
| Job event log | An in-place exit-85 restart writes **no new `001 executing` event**, only an output-file-transfer event (`040`). | P1 |
| After an eviction | New sandbox, usually a different host, 11–430 s later (typical 30–110 s). | P2–P4 |
| `torchrun` startup | ~18 s per (re)start before workers run (incl. `import torch`). | P7g/P7h |

## 6. Signal delivery inside the job

| Setup | Finding | Source |
|---|---|---|
| What HTCondor signals | **Only the top-level process.** Child processes (stand-ins for DataLoader workers) were never signaled, with or without the container. | P7c, `rest-chtc` |
| `run.sh` with `exec python ...` | Python receives SIGTERM (bare and in Apptainer). | P7a, `rest-chtc`, `p7-rerun` |
| Submit file `shell = exec python3 train.py ...` | Python receives SIGTERM (it saved with reason `signal` right after `condor_vacate_job`). | recipe 0 `test_htcondor.sh vacate`, CHTC, 2026-10-05 |
| `run.sh` without `exec` | bash gets the signal (its trap runs only after Python exits); **Python never sees it** and runs until it finishes or is SIGKILLed. | P7b, `rest-chtc` |
| Apptainer | Passes the signal through to the payload. | P7a/P7c container variants |
| `exec torchrun` | torchrun forwards SIGTERM to its workers at once, then **kills them after ~30 s** (default shutdown timeout). A 60 s save was cut off. | P7e, `torchrun` |
| torchrun exit code | Workers' exit 85 becomes **torchrun exit 1** (`ChildFailedError`); HTCondor treats the job as finished. | P7f, `torchrun` |
| `TORCH_ELASTIC_SHUTDOWN_TIMEOUT=120` (or `--shutdown-timeout`) | Works in torch 2.14.1: both workers finished a 60 s save and exited 85, ~61 s after SIGTERM. Version of introduction unknown. | P7g, `torchrun2` |
| Stop-file wrapper ([`run_torchrun_stopfile.sh`](../probes/run_torchrun_stopfile.sh)) | **Works without any torchrun feature.** The wrapper turns SIGTERM into a `STOP_REQUESTED` file (no forwarding), workers see it within ~1 s, finish a 60 s save, append to `RESTART_REQUESTED`, exit; the wrapper maps torchrun's exit 1 to 85. With `ON_EXIT_OR_EVICT` the rescheduled job restored the SIGTERM save (step 84). Planned exit 85 also works through it. | P7h, `torchrun3` |

## 7. Storage and transfer speed

| Measurement | CHTC | OSPool | Source |
|---|---|---|---|
| Local scratch write + fsync, 1 GB | 370–580 MB/s | 760–780 MB/s | P5a |
| `/staging` write + fsync, 1 GB in 1 file | 409 MB/s | n/a | P5a, `rest-chtc` |
| `/staging`, 100 MB in 1 file | 95 MB/s | n/a | P5a |
| `/staging`, **many small files** (64 files) | **11–42 MB/s** (1 GB took 24 s) | n/a | P5a |
| Directory rename on `/staging` | 0.01–0.03 s | n/a | P5a |
| Exit-85 restart gap, 100 MB checkpoint via spool | +1 s | +4 s | P5c |
| Exit-85 restart gap, 1 GB checkpoint via spool | +5 s | +7 s | P5d |
| Restart download from `checkpoint_destination = osdf://` | 3.7 min (once, 1 MB) | ~1 min | P6a |

Single run per number; treat these as orders of magnitude.

## 8. What this means for the recipes

1. **Making a SIGTERM save survive** takes one of two setups:
   - `/staging` (CHTC only), or
   - spool with `checkpoint_exit_code = 85`, `when_to_transfer_output = ON_EXIT_OR_EVICT`, **and** the checkpoint directory in `transfer_output_files`. (HTCondor's default output transfer brings back only new top-level files, not directories. Recipe 0's first vacate test left `transfer_output_files` unset and lost B; with the directory named, the rerun on 2026-10-05 restored B: the save made after SIGTERM at step 722.) This works on every pool tested and falls back to the last planned checkpoint after a hard kill.

   With `checkpoint_exit_code` alone, a SIGTERM save is wasted.
2. **Planned exit-85 checkpoints are cheap** (seconds) and are the only protection against hard kills and OSPool glidein ends. Keep a timed exit (~1 h, per the HTCondor manual's suggestion) in every recipe.
3. **GPU recipes should set `+is_resumable = true`.** On GPU Lab slots it turns the runtime limit into a restartable eviction instead of a hold (inferred from policy), and it makes backfill possible.
4. **Plan on 600 s from SIGTERM to SIGKILL.** Don't ask for more on backfill: it is the owner's time.
5. **Always `exec`** the training process (or use a wrapper that handles the signal). Workers and DataLoader children don't need their own SIGTERM handling under HTCondor.
6. **Multi-process launchers need the stop-file wrapper** (or at least `--shutdown-timeout` plus exit-code mapping). Plain `exec torchrun` breaks both the save time and exit 85.
7. **List exactly one checkpoint directory** in `transfer_checkpoint_files`, and make sure it exists before the first exit 85.
8. **Checkpoints on `/staging` must be few, large files.** Many small files are 10–40× slower to write. The quota also allows only **1,000 files** (and 100 GB) per user. Count files per checkpoint × checkpoints kept, plus temporary directories during a save. A sharded (DCP) checkpoint from 8 ranks with several files per rank, kept 2–3 times, uses a noticeable share of that. Keep retention low and clean up stale `.tmp` directories.
9. **Don't detect restarts with `NumJobStarts`** from the sandbox ad. Use what's on disk (e.g. "a checkpoint exists but my sandbox marker doesn't").

## 9. Open items

| Item | Why it matters | How to close it |
|---|---|---|
| Recipe 3 checkpoint size vs. the default `/staging` quota | A ~100 GB checkpoint (8B model + AdamW) fills the default 100 GB quota before a second one is kept | Users can request a larger `/staging` quota from CHTC. Recipe 3's README should say how much to ask for (checkpoint size × checkpoints kept + one in progress) and how many files |
| A real backfill eviction (P3e) | Confirms the policy reading in section 3 | Opt-in P3e on `chtc_backfill` (holds a GPU up to 6 h) |
| `job_max_vacate_time` above 600 on backfill / GPU Lab | Whether a job's request is capped where retirement is short | P3c on `chtc_backfill` |
| Effective vacate window from the ads at job start | Planned `vacate_budget()` helper | Log the estimate in probe starts; compare to P3 measurements |
| OSPool glidein-end eviction | Whether OSPool jobs ever get SIGTERM in practice | Hard to test on demand; rely on timed exit-85 checkpoints |
| `checkpoint_destination` + `ON_EXIT_OR_EVICT` | Whether the off-AP destination can also carry a SIGTERM save | One P6a variant |
| GPU-enabled PyTorch image, GPU model on GPU Lab slots | Recipes target H200s; P0 did not record the device name | Build a CUDA image; read `GPUs_DeviceName` in the machine ad |
