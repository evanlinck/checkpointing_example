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
| HTCondor Python bindings in the shared recipes image (htcondor 25.14.1) | **Work on CHTC CPU, CHTC GPU and the OSPool.** The modules are `classad2` and `htcondor2` (no `classad`/`htcondor`). `classad2` evaluated `MachineMaxVacateTime = 600` from the machine ad. `htcondor2.htchirp.HTChirp()` (with `+WantIOProxy = true`) read `ClusterId`, set `LastCheckpointStep` / `LastCheckpointReason` in 1–100 ms, and both appeared in the event log (`033 attribute_update`) and in `condor_history`. | P16a, `bindings`, 2026-10-28 |
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

### Observed: a real backfill eviction (recipe 1 tests, 2026-10-19)

Two recipe 1 test jobs ran on backfill slots of the same machine (`backfill1_5` and `backfill1_7`, both `BackfillSlot = true`). About 75 s after they started, both were evicted in the same second, without any command from us:

- **Event log:** `004 Job was evicted. Code 1011`, `Reason: PREEMPT expression evaluated to True`. This confirms the policy row above: the backfill `PREEMPT` fired because the GPU's owner needed it. For comparison, our `condor_vacate_job` gives `Code 1022`, "Job vacated by schedd" (P2a, P3a in `backfill2`, and the same tests).
- **In the job:** SIGTERM arrived; `vacate_budget()` reported a 600 s window from `MachineMaxVacateTime`.
  - Both jobs saved (615 MB, 2 files) and exited 85 well inside the window.
  - With spool + `ON_EXIT_OR_EVICT` + the checkpoint directory in `transfer_output_files`, both saves came back.
  - Both jobs resumed from them: one ~1.5 min later on another backfill slot of the same machine, the other on a different machine.
  - The grace period itself wasn't measured: the jobs exited long before SIGKILL.
- **Save time doubled:** these two saves took 12.4 and 12.5 s, against 2.5–5.6 s for every other save in the same tests. Both jobs wrote at the same moment on the same machine, which is the likely cause. Expect slower saves when one eviction hits several jobs on a node.
- **A third job never started:** it was evicted during input transfer (`Code 1008`) and ran elsewhere.

Source: recipe 1 `test_htcondor.sh` runs, jobs 6799595–6799597, on ap2002.

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
| Exception | Once (P7a, `rest-chtc`) HTCondor rescheduled to a new host after exit 85: "Rescheduling self-checkpoint job after checkpoint upload because reactivating the claim would have failed" (code 1025). **Never assume the same sandbox.** Seen again in recipe 2's full run (2026-10-22, `/staging` mode, 4 GPUs): after one of five timed exits the job was rescheduled (`Code 1025`) and restarted on the same machine **18 minutes** later; the other four restarted in place within ~8 s. | P7a, recipe 2 full run |
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
| Same two findings, torch **2.8.0** (the recipe images' version) | A 40 s save under plain `torchrun` was cut off (no save completed) and torchrun exited **1**; the same save under `launch.py` completed and the job exited 85. Local CPU run (2 `gloo` workers, macOS), not yet on GPUs or HTCondor. | recipe 2 `test_local.py --ddp`, 2026-10-21 |
| Stop-file wrapper `htcondor_ckpt/launch.py`, 2 GPUs, NCCL, under HTCondor | **Works.** A SIGTERM during the first step reached launch.py. Both ranks saw the stop file and stopped at the same step (mid-accumulation, partial step discarded). Rank 0 saved in 2.1 s with 598 s of the window left, and both NCCL communicators closed cleanly. torchrun exited 1; launch.py found both ranks' restart notes and exited 85. (The SIGTERM was a backfill eviction: event log `Code 1011`.) | recipe 2 `test_htcondor.sh comm`, L40 machine, torch 2.8, 2026-10-22 |
| Recipe 2 interruption tests, 2 × H200 (backfill slot), NCCL, under launch.py | **`condor_vacate_job`:** the stop arrived mid-accumulation; both ranks stopped at the same step, rank 0 saved 1.5 GB in 5.2 s (595 s of the window left), and the job resumed from that save (`saved because: stop_file`). **`-fast`:** no save; resumed from the last periodic save. Both also went through 2 timed exits each, every rank stopping at the same step, and finished. Two ranks' output lines can run together in the job's `.out` (fixed in `train.py`: one write per line). | recipe 2 `test_htcondor.sh vacate` / `fast`, 2026-10-22 |
| NCCL direct GPU-to-GPU copies over PCIe | **L40 (2 GPUs, no NVLink): work.** With `NCCL_P2P_LEVEL=SYS`, NCCL chose `P2P/CUMEM` (`isAllDirectP2p 1`, `GDR 1`), and an all-reduce took 0.1 s. **RTX PRO 6000 Blackwell (2 GPUs): direct PCIe copies hang.** On two of the four machines, with direct copies allowed (the default, and `NCCL_P2P_LEVEL=SYS`: NCCL chose `P2P/CUMEM`, `isAllDirectP2p 1`), the first all-reduce never completed; NCCL's watchdog aborted it after its timeout (600 s default, 300 s as set by recipe 2). On a third machine, **`NCCL_P2P_LEVEL=NVL` worked**: the all-reduce took 0.0 s and the job trained and saved. So the cause is direct GPU-to-GPU copies over PCIe on these machines (likely their IOMMU/ACS settings), not PCIe in general (they work on L40). Not yet tested: `NVL` and `SYS` on the *same* RTX PRO 6000 machine, and the fourth machine. | recipe 2 smoke run and three `test_htcondor.sh comm` runs, 2026-10-22 |
| `TORCH_ELASTIC_SHUTDOWN_TIMEOUT=120` (or `--shutdown-timeout`) | Works in torch 2.14.1: both workers finished a 60 s save and exited 85, ~61 s after SIGTERM. Version of introduction unknown. | P7g, `torchrun2` |
| Stop-file wrapper ([`run_torchrun_stopfile.sh`](../probes/run_torchrun_stopfile.sh)) | **Works without any torchrun feature.** The wrapper turns SIGTERM into a `STOP_REQUESTED` file (no forwarding), workers see it within ~1 s, finish a 60 s save, append to `RESTART_REQUESTED`, exit; the wrapper maps torchrun's exit 1 to 85. With `ON_EXIT_OR_EVICT` the rescheduled job restored the SIGTERM save (step 84). Planned exit 85 also works through it. | P7h, `torchrun3` |
| GPU-to-GPU speed, H100 (SXM) machine, torch 2.8 / NCCL 2.27.3, shared recipes image | All 8 benchmark jobs landed on the **same** 8-GPU H100 backfill machine. NCCL copied directly between GPUs (`P2P/CUMEM`) with and without `NCCL_P2P_LEVEL=NVL`, so the GPUs are NVLink-connected. Bus bandwidth at 1 GB shards: 340 GB/s (4 GPUs), 270–280 GB/s (2 GPUs), the same with and without `NVL`. Estimated FSDP communication for a 7.3B model: ~0.13 s per step on 4 GPUs (negligible). `nvidia-smi` is not in the container, so the topology wasn't printed. **To check:** the 2-GPU jobs saw 4 GPUs (`torch.cuda.device_count()` = 4); the next run records `CUDA_VISIBLE_DEVICES` and `_CONDOR_AssignedGPUs` | `probes/gpu_comm/`, 2026-10-28 |

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

**Parallel writes and reads on `/staging` (P15, 2026-10-28; 3 rounds about 6 h apart, CHTC CPU and GPU machines, `/staging` mounted as `fuse.ceph-fuse`).** Write = write + fsync of the whole set; read right after writing (an upper bound for a resume on another machine). Rounds 1–2 were similar; round 3 hit a slow period on every machine.

| | Rounds 1–2 | Round 3 (slow period) |
|---|---|---|
| Write 20 GB, 1 writer | 300–480 MB/s | 95–250 MB/s |
| Write 20 GB, 4 or 8 writers | 430–560 MB/s | 190–360 MB/s |
| Read 20 GB, 1 reader | 100–140 MB/s | 13–82 MB/s (one read took 26 min) |
| Read 20 GB, 4 readers | 280–500 MB/s | 56–260 MB/s |
| Read 20 GB, 8 readers | 560–770 MB/s | 31–200 MB/s |
| **Write 90 GB, 4–8 writers** (GPU machines) | **153–169 s** (530–590 MB/s) | **230–330 s** (270–390 MB/s) |
| **Read 90 GB, 8 readers** / 4 readers | **105–114 s** / 168–175 s | 233–328 s / 303–316 s |
| Delete 4–32 files (20–90 GB) | 2–14 s | 2–6 s |

- **Writes top out around 0.5–0.6 GB/s per job.** More writers add only 10–25 %; 1 vs several files per writer makes no consistent difference. The network links were 10–100 Gbit/s, so the limit is `/staging` (or its client), not the network.
- **Reads need parallel streams.** One reader gets 100–140 MB/s; 8 readers get 5–6× that. A resume should read with several readers (or threads).
- **Speed varies a lot with time.** The slow round was 2–10× slower, worst for single-stream reads. Plan with the slow numbers.
- **Free space on `/staging` reports the whole filesystem** (~2.5 PB), not the user's quota, so a job can't check its quota with `statvfs`/`df`.
- **The machines:** memlock limit 8 MB (`ulimit -l`), `/dev/shm` 270–1,076 GB, 40–256 CPUs, 540–2,150 GB of memory. The probe couldn't read its own memory use from inside the container (cgroup files not visible).


## 8. What this means for the recipes

1. **Making a SIGTERM save survive** takes one of two setups:
   - `/staging` (CHTC only), or
   - spool with `checkpoint_exit_code = 85`, `when_to_transfer_output = ON_EXIT_OR_EVICT`, **and** the checkpoint directory in `transfer_output_files`. (HTCondor's default output transfer brings back only new top-level files, not directories. Recipe 0's first vacate test left `transfer_output_files` unset and lost B; with the directory named, the rerun on 2026-10-05 restored B: the save made after SIGTERM at step 722.) This works on every pool tested and falls back to the last planned checkpoint after a hard kill.

   With `checkpoint_exit_code` alone, a SIGTERM save is wasted.
2. **Planned exit-85 checkpoints are cheap** (seconds) and are the only protection against hard kills and OSPool glidein ends. Keep a timed exit in every recipe. CHTC usually suggests 4–6 h on the OSPool (up to 8) and 6–10 h on CHTC backfill. That's longer than the manual's generic "about once an hour", because evictions with SIGTERM get their own save.
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
| ~~A real backfill eviction (P3e)~~ | Closed: observed in recipe 1's tests (section 3, "Observed"). Still unmeasured: the grace period on a real eviction, and SIGKILL timing for a job that doesn't exit | Optional: P3e on `chtc_backfill` (holds a GPU up to 6 h) |
| `job_max_vacate_time` above 600 on backfill / GPU Lab | Whether a job's request is capped where retirement is short | P3c on `chtc_backfill` |
| Effective vacate window from the ads at job start | Planned `vacate_budget()` helper | Log the estimate in probe starts; compare to P3 measurements |
| ~~OSPool glidein-end eviction~~ | Closed by P12a (§10): no SIGTERM; a hard kill 104–355 s after `GLIDEIN_ToDie` | – |
| `checkpoint_destination` + `ON_EXIT_OR_EVICT` | Whether the off-AP destination can also carry a SIGTERM save | One P6a variant |
| ~~Parallel write and read speed on `/staging` (P15)~~ Closed: §7 (2026-10-28). Left: memory use during big writes (not visible in the container) | Recipe 3's ~88 GB sharded checkpoint must be saved well inside the 600 s window; §7 has only single-writer numbers (409 MB/s, 1 GB). Also: host memory, memlock and `/dev/shm` on GPU machines, and whether the page cache counts against the job's memory | `probes/` P15a (20 GB, 1/4/8 writers); P15b at 90 GB after a quota increase |
| ~~HTCondor's Python bindings in a container (P16)~~ Closed: §2 (works on CHTC and the OSPool) | The 25.x bindings name their modules `classad2` / `htcondor2` (no `classad` module), so `vacate_budget()` silently fell back to plain arithmetic; `stop.py` now tries `classad2` first. Planned `chirp.py` needs `htcondor2.htchirp` to work in a container, on CHTC and the OSPool | `probes/` P16a with the shared recipes image |
| GPU machines for recipe 3 (answered by §11), and GPU-to-GPU speed (partly: only one H100 machine so far, §6; PCIe machines still to measure) | Which machines have 4 GPUs of ≥ 40–80 GB, their host memory, how often 4 GPUs are free; how fast all-gather / reduce-scatter run with and without NVLink (FSDP moves ~60 GB per GPU per step for a 7B model) | `probes/gpu_machines.sh` (no jobs), `probes/gpu_comm/` |
| GPU-enabled PyTorch image, GPU model on GPU Lab slots | Recipes target H200s; P0 did not record the device name | Build a CUDA image; read `GPUs_DeviceName` in the machine ad |

## 10. Access points: spool, limits and policy (surveyed)

Read-only survey with [`probes/ap_survey.sh`](../probes/ap_survey.sh) on 2026-10-23: **ap40** (`ap40.uw.osg-htc.org`, an OSPool access point, host `ospool-ap2140`) and **ap2002** (CHTC, which flocks to the OSPool). Both run HTCondor 26.1.0. Summaries: `results/ap-survey/{ospool-ap2140,ap2002}/summary.md`. These are configuration snapshots; other OSPool access points may be set differently, so the guidance tells users to check their own.

### Configuration

| | ap40 (OSPool) | ap2002 (CHTC) |
|---|---|---|
| `SPOOL` | `/var/lib/condor/spool`, own 1.9 TB filesystem, 3% used | same layout, 9% used |
| `MAX_TRANSFER_INPUT_MB` | **5000, and users may not change it** (submit requirement `cant_change_maxtransferinputmb`) | −1 (no limit) |
| `MAX_TRANSFER_OUTPUT_MB` | −1 | −1 |
| `MAX_CONCURRENT_UPLOADS` / `DOWNLOADS` | 500 / 500; matchmaking is curbed above 500 waiting uploads | 500 / 100 |
| Held jobs removed after | **30 days** (`SYSTEM_PERIODIC_REMOVE_LongHold`) | 90 days |
| Time per execution | **20 h** (`JobDurationCategory = "Medium"`, the default) or 40 h (`"Long"`), via `AllowedExecuteDuration`; exceeding it holds the job (`JobExecuteExceeded`) | no transform |
| Total time, self-checkpointing jobs | **14 days** (`AllowedJobDuration`, `CKPT_JOB_DURATION`); exceeding it holds the job (`JobDurationExceeded`) | no transform |
| Excess CPU | **hold** after 1 h above 1.8 × `request_cpus` (`SYSTEM_PERIODIC_HOLD_CpuUsage`, code 26, subcode 102) | not configured |
| Restart-count holds | `NumJobStarts > 10` / shadow exceptions > 10 hold a job, **except self-checkpointing jobs** | – |
| `periodic_release` | capped at 4 holds by a transform | – |
| `CHECKPOINT_DESTINATION_MAPFILE` | set, but the file doesn't exist | same |

### Spool behavior (ap2002, `probes/spool_check/`, job 6965222)

A job adding 1 MB to its checkpoint directory per exit 85, inspected while running and after it finished:
- **Spool holds one copy of the checkpoint.** 4.19 MB checkpoint → 4.21 MB in the job's spool directory; 7.34 MB → 7.36 MB. Earlier checkpoints are not kept.
- **A `cluster<C>.proc<P>.subproc0.tmp` directory sits beside it** (empty between uploads). New checkpoints are probably received there and swapped in, so the peak may briefly be twice the checkpoint. Not yet measured (P9a).
- **Spool is freed when the job finishes.** After exit 0, the job's spool directory no longer existed.
- **Users can see their own spool use.** The job's directories are owned by the user (`JOB_SPOOL_PERMISSIONS = user` on both APs) under world-readable parents: `du -sb $(condor_config_val SPOOL)/<cluster mod 10000>/<proc>/`. Without file access, `TransferOutputStats.CedarSizeBytesLastRun` in the job ad gives the size of the last checkpoint upload. (`DiskUsage` is the execute-side sandbox, not spool.)

### Glideins (OSPool collector, as seen from ap40)

- **For 83% of slots, `GLIDEIN_ToDie − GLIDEIN_ToRetire` = 10 h** (34,288 of 41,404 slots with both values). A glidein stops accepting jobs 10 h before it is killed, so a job normally gets about 10 h or more on a glidein. `GLIDEIN_Max_Walltime` was 71.5 h on the slot inspected.
- `GLIDEIN_ToDie` and `GLIDEIN_ToRetire` are in the machine ad.
- **The slot's `MaxJobRetirementTime` is −1 on memory overuse** (immediate eviction); disk overuse counts only on data slots (`IsDataSlot`). `SiteWMS_WN_Preempt` was false on the sites listed.
- **Multi-GPU slots are scarce** (slot counts, one snapshot): A40 × 4 (42), RTX A5000 × 4 (12), RTX 3060 × 4 (7), L40 × 2 (6), H100 × 2 or 3 (8), plus about 200 2–4-GPU slots without a device name. Most GPU slots have one GPU.

### Job history, last 30 days

| | ap40: jobs | interrupted ≥ 1× | ap2002: jobs | interrupted ≥ 1× |
|---|---|---|---|---|
| CPU, self-checkpointing | 226,818 | 12.8% | 177,595 | 9.6% |
| GPU, self-checkpointing | 554 | 38.6% | 3,854 | 16.0% |

ap2002 mixes CHTC and OSPool runs (`ap_survey.sh` now records `MachineAttrGLIDEIN_Site0` to separate them). "Interrupted" counts executions beyond the first, from `NumJobStarts`, which doesn't count in-place exit-85 restarts (§2).

- **On ap40, the excess-CPU hold dominates for self-checkpointing jobs.** `SystemPolicy` holds: 13,353 on CPU jobs, and **484 on the 554 GPU jobs**. 107 of 166 held checkpointing jobs in the queue were held for it. Sample messages: "Job used 22 CPUs, while request_cpus=4". How many users this covers is not known yet (the survey now counts distinct submitters among held jobs).
- **Other ap40 holds:** `MaxTransferInputSizeExceeded` (4,502 on CPU jobs that don't checkpoint; 2 on GPU self-checkpointing jobs) and `JobExecuteExceeded` (3,255 on CPU jobs that don't checkpoint).
- **Interruptions of self-checkpointing jobs on ap40,** by `NumVacatesByReason`: `ClaimDeactivated` 14,533 (likely the rescheduled exit-85 restarts of §5), `StartdShutdown` 6,357 (glidein or machine ends), and `StarterError` 6,272.
- **On ap2002, failed checkpoint uploads dominate.** The most common hold of self-checkpointing CPU jobs was `TransferOutputError` (18,489). Jobs held in the queue include code 12 subcode 2 ("file not found", the P8a failure) left on hold 44–55 days.
- **What a PyTorch GPU job actually uses (recipe 1, 2026-10-23,** `train.py`'s new `CPU threads` and `CPUs used` lines; `request_cpus = 4`, no DataLoader workers):
  - **HTCondor sets `OMP_NUM_THREADS` to `request_cpus` (4) on CHTC and the OSPool, and PyTorch's main thread pool follows it** (`torch.get_num_threads()` = 4). The inter-op pool is not capped: it was the machine's full size (192 on a CHTC L40S machine; 64 usable of 128 on an OSPool H100 machine at NCSU).
  - **Measured use was 0.34 CPUs while training on CHTC, and 0.52–0.70 on the OSPool,** far below the 1.8 × 4 = 7.2 that ap40's hold needs. These averages count child processes once they exit, so `torch.compile`'s worker pool is only partly counted; it works during start-up, not during training.
  - So the excess-CPU holds come from something PyTorch's defaults don't do on their own: DataLoader workers, a process pool, other libraries' thread pools, or CPU-side work. Recipe 2 also uses no DataLoader workers.
- **Transfer queue on ap40:** a peak of 257 uploads waiting (the limit is 500); about 440 MB/s sent to jobs averaged over a day.

### Input limits, glidein ends and OSDF backups (probes, 2026-10-26)

Run tags `ospool-r4` (P11d, P13; chtc and ospool from ap2002) and `glidein-end` (P12a; ospool). Summaries: `results/{ospool-r4,glidein-end}/summary.md`.

- **A checkpoint restored on a new host counts against the input-size limit (P11d).**
  - The setup: `max_transfer_input_mb = 50`, a 100 MB spooled checkpoint, then `condor_vacate_job`.
  - The probe saved after SIGTERM and exited 85, as usual. But the restart in a new sandbox was **held**: *"sending file …/spool/…/ckpt/step_…/payload_000.bin: max total upload bytes exceeded (max=50 MB …)"*. Same result on CHTC (bare and container) and the OSPool.
  - With a 200 MB limit, the same jobs resumed from the SIGTERM save.
  - Restarts in place after a planned exit 85 re-transfer nothing, so they aren't affected. **The hold appears only after an eviction**, possibly days into a run.
  - On ap40 (`MAX_TRANSFER_INPUT_MB = 5000`, locked), a job whose spooled checkpoint, plus its other plain inputs, is over ~5 GB can't be restored after an eviction.
- **`osdf://` inputs don't count against it (P11d).** A 100 MB `osdf://` input ran under a 50 MB limit, with and without a container. A job with a container image read through OSDF also started normally under the 50 MB limit. Large base-model weights and containers read through OSDF are therefore unaffected.
- **A glidein end is a hard kill without warning, shortly after `GLIDEIN_ToDie` (P12a).** Five jobs ran on OSPool glideins until those ended:
  - sites: UChicago (2), FANDM-ITS, Michigan and BEOCAT-SLATE;
  - each started 9.7–10.5 h before `ToDie`;
  - **none received SIGTERM**: each was killed **104–355 s after `ToDie`**, by its last heartbeat (5 s apart, streamed to the AP);
  - each was rescheduled to another host 34–70 s later.
  
  So `GLIDEIN_ToDie` in `$_CONDOR_MACHINE_AD` is a dependable deadline: a timed checkpoint that ends before it loses nothing. `htcondor_ckpt.stop.runtime_limit()` uses it.
- **`transfer_output_remaps` to `osdf://` applies only at the job's final exit (P13).**
  - The setup: a directory in both `transfer_checkpoint_files` and `transfer_output_files`, remapped to `osdf:///chtc/staging/...`.
  - It was restored normally at each in-place restart.
  - It reached OSDF **only when the job ended**: all three files (from steps 30, 60, 90) arrived together, 3 s after exit 0, and none at the two exits 85. Same on CHTC and the OSPool.
  - So HTCondor won't make OSDF backups at timed checkpoints. A job can still hand its checkpoint to OSDF by *ending*, and a new job can resume from it.
- **Ending with exit 86 works the same (P13b, run tag `handoff`, 2026-10-27).** The job left the queue with "Normal termination (return value 86)", with no hold and no requeue. The remapped directory reached OSDF 3–8 s after the exit, on CHTC and the OSPool. A dedicated code can therefore mean "continue in a new job", keeping exit 0 for "training finished".
- **Each exit-85 restart starts a new execution for `AllowedExecuteDuration` (P14a, run tag `timecaps`, 2026-10-27).** With `allowed_execute_duration = 150` and an exit 85 every 60 s, the job ran 6 minutes to completion, never held, on CHTC and the OSPool. A timed checkpoint shorter than the cap (ap40: 20 h) keeps a job under it.
- **`AllowedJobDuration` counts wall-clock time from the job's first start, across restarts (P14b).**
  - With `allowed_job_duration = 240` and exits every 60 s, the job was held **240 s after its first start**.
  - The message: "The job exceeded allowed job duration of 04:00", **code 46**. ap40's release transform excludes codes 46 and 47, so such a hold is not released automatically.
  - The job ad at start had `JobStartDate` and `AllowedJobDuration`. Their sum came 14 s before the hold, so a job can compute its own deadline (`htcondor_ckpt.stop.job_time_left()`).
  - `JobStartDate` is when HTCondor started the job, a few seconds to minutes before the program ran (input transfer, container).
  - On ap2002, jobs get `AllowedExecuteDuration = 259200` (72 h) when they set none.

## 11. GPU pool history (May 2025 – Oct 2026, analyzed 2026-10-28)

From 18 months of 5-minute GPU pool snapshots; full tables, method and caveats in [`results/gpu-pool-history/summary.md`](../results/gpu-pool-history/summary.md). Figures are for Apr–Oct 2026 (85–89 % of the pool claimed) and are upper bounds on availability: "unclaimed" doesn't prove a job could match, and competing jobs are ignored.

| Question | Finding |
|---|---|
| Machines a GPU Lab job can use with 4 GPUs of ≥ 75 GB | About 9–11: H200 (8-GPU machines), one H100 machine, four 4-GPU A100-80GB machines, one RTX PRO 6000 machine (Blackwell, PCIe only). The set changes often (A100-80GB machines removed or split into MIG this year; machines moving between GPU Lab and prioritized) |
| Host resources on those machines | Every one has ≥ 500 GB of host memory and ≥ 48 CPUs. Whenever 4 GPUs were free, ≥ 400 GB of memory and (except one 48-CPU machine) 85+ CPUs were free too. So free memory and CPUs were there; whether large requests take longer to *match* the data can't show, and in the maintainer's experience they do. Keep requests small |
| How often 4 such GPUs were free on one machine | 18 % of snapshots (GPU Lab), 16 % (backfill); 2 GPUs: 38 %. Month to month 3–34 %; hour of day and weekday matter little (best overnight: 21 % vs 15 % mid-afternoon) |
| Wait for 4 free GPUs, from a random time | Median ~14 h, 41 % > 1 day, 10 % > 5 days (ignoring competition, so real waits are longer). Free windows last a median 20 min, so the job must already be queued. 2 GPUs: median ~1 h. Requiring one GPU model: 2–3× longer |
| A 4-GPU job on backfill | Evicted (a primary job takes one of its GPUs) after a median ~14 h on ≥ 75 GB machines (H200 ~10 h); 13 % within 1 h, 28 % within 4 h |
| CUDA drivers | 570 (CUDA 12.8) or 590 (13.1) on every ≥ 75 GB type seen (Sep–Oct 2026 only; the snapshots have no driver attribute). Some RTX 2080 Ti machines have 550 (12.4). Images must be CUDA ≤ 12.8 builds |
| MIG | One A100-80GB machine has been split into 8 × 3g.40gb instances since 2026-03-30 (`GPUs_DeviceName` contains "MIG", 40 GB): a ≥ 79 GB memory floor excludes them |
| Not in the data | Whether a job could match, NVLink, `HasCHTCStaging`, driver history |

**Consequence for multi-GPU jobs:** losing a 4-GPU claim can cost a day of waiting, so every exit 85 carries a small risk (recipe 2: 1 of 5 timed exits was rescheduled instead of restarting in place, §5). Recipe 3 therefore saves in place on `/staging` and, on GPU Lab, makes one timed exit at the end of its job-length window (see `docs/03-fsdp-dcp-finetune.md`).

