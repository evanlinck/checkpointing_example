# Notes for user guidance

Points to carry into the guidance for people training ML models on CHTC (`docs/checkpointing-guide.md` and CHTC's own pages). Each note has the advice in a form close to what users will read, then the evidence behind it, so it can be checked or updated when the pool changes.

## Resuming on a different GPU type

**Advice for users:**

A checkpointed job can resume on a different type of GPU than the one it started on (after an eviction, a hold, or a timed exit that gets rescheduled). That's normal, and it doesn't hurt your results:

- **Your training continues exactly where it stopped.** The checkpoint restores the weights, the optimizer state, the learning-rate schedule (from the step) and the position in the data, so no batch is repeated or skipped.
- **The numbers won't match bit for bit** what the old GPU would have produced. Different GPU types run different low-level kernels (matrix-multiply algorithms, `torch.compile`'s tuning, bf16/TF32 rounding), and tiny differences grow as training goes on. The effect is the size of the normal noise between two identical runs, not a change in quality.
- **Two identical runs differ slightly even on the same GPU type,** unless deterministic algorithms are on, because some GPU operations add numbers in varying order.

What *does* change results, and how to avoid it:

- **GPUs without bf16** (compute capability below 8.0) would need fp16, with different numerics and a `GradScaler` whose state must also be checkpointed. Exclude them: `gpus_minimum_capability = 8.0`.
- **A different number of GPUs after a restart** changes how each step's data is split across GPUs. Keep the GPU count fixed for a run (`request_gpus`).
- **Changing settings between restarts** (batch size, learning rate, model shape) changes the training itself. Use a new run name instead.
- **Keep the global batch fixed when you change the per-GPU batch.** If you lower the per-GPU batch so the job fits smaller GPUs, raise gradient accumulation to match: then the optimizer sees the same batch.

If you need bit-for-bit reproducibility (debugging a divergence, a paper that must be rerun exactly): pin the GPU type with `require_gpus = DeviceName == "<GPU name>"`, turn on deterministic algorithms, and expect longer waits in the queue. On a single GPU type, a resumed run can match an uninterrupted one exactly.

**Short version:** *A checkpointed run may resume on a different GPU type. That changes its numbers only at the level of run-to-run noise, not its quality. If you need exact reproducibility, pin the GPU type, at the cost of longer waits.*

**Evidence:**

- **Recipe 1, CPU** (`test_local.py`): with deterministic settings, losses after several SIGTERM interruptions and resumes matched an uninterrupted run **bit for bit**, in both checkpointing modes.
- **Recipe 1, GPUs** (`compare_runs.py`, 2026-10-19): two uninterrupted runs on different GPUs (H200, RTX PRO 6000 Blackwell) differed by up to **0.0053** in validation loss (0.0001 at the end). A run resumed 4 times on an H100 stayed within that (0.0068 at most, 0.0009–0.0010 at the end). Even the two uninterrupted runs differed from step 50 on.
- **Recipe 2, GPUs** (`test_htcondor.sh`, 2026-10-22, identical 300-step settings, 2 GPUs): `vacate` on H200s ended at val loss **5.9419**, `-fast` on H200s at **5.9458**, and `hold`, which started on L40S and finished on A100-SXM4-40GB, at **5.9455**. The run that changed GPU type sits inside the spread of the two that didn't. (Informal: not the two-reference comparison.)
- **Recipe 2, two references and a resumed run** (`compare_runs.py`, 2026-10-23, 300 steps, 2 GPUs, `deterministic: false`): two uninterrupted runs on the **same** GPU type (H100) differed from step 30 on, by up to **0.0061** in val loss. A run on another type (A100-SXM4-40GB) with 5 restarts differed from them by up to **0.0090**, within twice that noise floor. So run-to-run noise exists even without a change of GPU, and a resume on another GPU type stays within about twice it.
- **Recipe 2, 1 vs 4 GPUs** (smoke runs, 2026-10-22, A100-SXM4-80GB): with the same global batch, val loss 6.3194 vs. 6.3262 after 200 steps (0.0068 apart).

## Checkpointing on the OSPool

Written for OSPool users at any access point, not just CHTC's. It will become a standalone document, so it leaves out CHTC-specific storage and policy.

**Advice for users:**

**Checkpoint on a timer: it's your main protection.** HTCondor on the OSPool almost never evicts a job by its own policy. Interruptions come from the pilot job your work runs in (the "glidein") reaching the end of its time at the remote site, or from the site itself. These can arrive **with no warning signal**. So treat any interruption as a hard kill that sends you back to your last planned checkpoint:
- Have your code stop itself after a fixed runtime, save, and exit with code **85** ("state saved, restart me"). Add `checkpoint_exit_code = 85` to the submit file.
- A good interval is **every 4–6 hours (up to 8)**. The interval is the most work an interruption can take from you.
- Planned checkpoints are cheap. The job usually restarts on the same machine, in the same directory, within a few seconds. A 1 GB checkpoint adds about 7 s. Measure your own cost (save, transfer, start-up, `torch.compile`) and keep it small compared with the interval.
- **Checkpoint before your glidein ends.** A glidein is killed shortly after the time in `GLIDEIN_ToDie`, which your job can read from its machine ad (`$_CONDOR_MACHINE_AD`). It sends no warning signal, so everything since your last checkpoint is lost. Most glideins stop taking new jobs 10 h before that, so a job usually gets about 10 h. Read `GLIDEIN_ToDie` at start-up, and take your timed checkpoint before it (15 minutes before is plenty for small checkpoints) if that comes sooner than your interval. `htcondor_ckpt.stop.runtime_limit()` does this.

**Use all of these submit lines:**
```
checkpoint_exit_code      = 85              # exit 85 = "saved, restart me"
transfer_checkpoint_files = checkpoints     # one directory, holding everything needed to resume
when_to_transfer_output   = ON_EXIT_OR_EVICT
transfer_output_files     = checkpoints     # without this, an eviction brings back no directories
kill_sig                  = SIGTERM         # the signal your code handles
```
- With `checkpoint_exit_code` alone, a save made after a warning signal is **lost**, and the job restarts from the previous planned checkpoint.
- With `ON_EXIT_OR_EVICT` **and** the directory named in `transfer_output_files`, that save is kept.
- **Create the checkpoint directory before the first possible exit 85.** If a listed path doesn't exist, the job goes on hold. An empty directory is fine.

**Still handle the warning signal when it comes.** When the OSPool does send a warning, it behaves like other HTCondor pools: SIGTERM within about a second, then a hard kill **600 s** later.
- In the signal handler, only set a flag. The training loop checks it at each step, saves the state after the last finished step, and exits 85.
- **Never exit 0 because of a signal.** HTCondor requeues the job anyway, but exit 0 should mean "training finished".
- **Plan for 600 s.** A longer `job_max_vacate_time` may be granted, but warnings are rare on the OSPool, so it buys little.

**Make your program the process HTCondor signals.** HTCondor signals only the top process. Start the job with `shell = exec python3 train.py ...`, or a `run.sh` whose last line `exec`s Python. Without `exec`, the shell gets the signal and Python never does. Multi-GPU launchers like `torchrun` need a wrapper (see the recipes).

**Write checkpoints safely, and find them from what's on disk.**
- Write each checkpoint to a temporary directory, then rename it. A transfer then only ever contains complete checkpoints.
- On start-up, resume from the newest complete checkpoint if one exists; otherwise start fresh. The same command then works for the first start and every restart.
- Don't use `NumJobStarts` from the job ad to detect a restart: it isn't updated on exit-85 restarts.

**Keep checkpoints small.** HTCondor stores them on the access point and moves them on every planned checkpoint. Up to about 1–2 GB works well.
- **Spool holds one copy of whatever is in your checkpoint directory.** Keeping two checkpoints in the directory doubles your spool use, so keep only the newest.
- **Your access point may limit input size, and a checkpoint counts.** After an eviction, the restarted job receives its checkpoint from spool as input. If the checkpoint plus your other plain inputs is over the limit, the job is **held** ("max total upload bytes exceeded"). ap40 sets `MAX_TRANSFER_INPUT_MB = 5000` and doesn't let users change it. Restarts after a planned exit 85 re-transfer nothing, so the problem only appears after an eviction, maybe days into a run. Keep checkpoints well under your AP's limit (`condor_config_val MAX_TRANSFER_INPUT_MB`). Inputs read through `osdf://` don't count.
- **Check how much spool your job uses:** `du -sb $(condor_config_val SPOOL)/<cluster mod 10000>/<proc>/`, or the size of the last upload in `condor_q <job> -af TransferOutputStats` (`CedarSizeBytesLastRun`).

**Your checkpoints disappear when the job leaves the queue.** HTCondor deletes stored checkpoints when the job finishes or is removed, by you or by a removal policy. Don't remove a long run you want to keep. When the job ends, copy the final checkpoint and exported model somewhere safe. To keep a copy that outlives the job, end it with the checkpoint remapped to OSDF (see the 14-day limit below); HTCondor doesn't copy to OSDF at timed checkpoints.
- **Don't leave a checkpointing job on hold.** Its checkpoint occupies the access point's shared spool the whole time, and access points remove long-held jobs, checkpoint and all. ap40 does it after 30 days. Fix and release the job, or remove it on purpose.

**Know your access point's time limits.** OSPool access points can cap how long a job runs. On ap40:
- **Each execution may run 20 h** (40 h with `+JobDurationCategory = "Long"`), after which the job is held. Every exit 85 starts a new execution, so a timed checkpoint every 4–6 hours keeps you well inside that.
- **A self-checkpointing job may run 14 days in total.** Training that needs longer has to continue in a new job. HTCondor sends files to OSDF (`transfer_output_remaps = "checkpoints = osdf:///..."`) only when a job *ends*, not at its checkpoints. So end the job yourself before the limit: save, exit with a code of your own (we use 86, "continue in a new job"; keep 0 for "finished") with the checkpoint directory remapped to a new OSDF path, and start the next job from that copy (listed as an `osdf://` input). This is also the safe way to copy a checkpoint out of a job you are about to remove.
- Look for `AllowedExecuteDuration` and `AllowedJobDuration` in `condor_q <job> -l` to see the limits your job got. Your job can read them too, in `$_CONDOR_JOB_AD`: the total limit runs from `JobStartDate`, so the job can plan its hand-off (`htcondor_ckpt.stop.job_time_left()`). A job held for the total limit (code 46) isn't released automatically, so hand off before it.

**Keep your CPU use within `request_cpus`.** Some access points hold jobs that use more CPUs than they requested: ap40 holds a job after an hour above 1.8 × `request_cpus`. On ap40 this is the most common reason self-checkpointing jobs are held, GPU jobs included ("Job used 22 CPUs, while request_cpus=4"). HTCondor already sets `OMP_NUM_THREADS` to your `request_cpus`, and PyTorch's main thread pool follows it. A plain PyTorch GPU training job used well under one CPU (recipe 1 asks for 4). The extra CPUs come from what you add:
- **DataLoader workers:** each is a process with its own threads, so keep `num_workers` below `request_cpus` and request a CPU for each.
- **Process pools and other libraries:** `multiprocessing`, joblib, tokenizers and NumPy builds that ignore `OMP_NUM_THREADS`. Cap them explicitly, or request the CPUs they use.
- **Check:** `condor_q <job> -af RequestCpus CpusUsage` while the job runs. Your job is fine if `CpusUsage` stays below `RequestCpus`.

**Get large inputs through OSDF.**
- Load the container with `container_image = osdf:///<your access point's namespace>/...sif`, and list data files as `osdf:///` URLs in `transfer_input_files`. Put them in your access point's OSDF area (e.g. `/ospool/ap40/data/<user>/` on ap40), as OSPool advises for files over 1 GB.
- **Inputs read through OSDF don't count against your access point's input limit,** so large model weights are fine there. The same files sent from your home directory would count.
- OSDF caches by file name: give a rebuilt image or changed dataset a **new file name**.
- Don't send checkpoints through OSDF with `checkpoint_destination = osdf://...`. It works, but restores are slower and a save made after a warning signal is lost.

**Describe the GPU you need by its properties.** OSPool GPUs vary widely.
- `gpus_minimum_memory`: your measured peak GPU memory plus headroom. Without it, a job can land on a GPU that is too small and run out of memory.
- `gpus_minimum_capability = 8.0` if you train in bf16. Older GPUs would need fp16, and a `GradScaler` whose state you'd also have to checkpoint.
- A resumed job may run on a different GPU type. That's fine (see "Resuming on a different GPU type" above).

**Smaller things:**
- `export HOME=$PWD` before `exec` if you use `torch.compile`: the container is read-only, and its caches go under `$HOME`.
- Set `request_disk` to cover your data, the checkpoint you keep and one being written.

**Short version:** *On the OSPool, interruptions often come with no warning, so a timed save-and-exit-85 every 4–6 hours is what protects your work. Use the four spool lines plus `kill_sig`, `exec` your program, keep checkpoints small and your threads within `request_cpus`, check your access point's time and size limits, and copy your results off before the job leaves the queue.*

**Evidence:** probe jobs and recipe tests submitted to the OSPool, 2026-10 (from a CHTC access point; what's measured is the execute side, which is the same for every OSPool access point). Details in `environment.md`.
- **Eviction policy:** `MaxJobRetirementTime` is ~10⁷ s on OSPool slots; the machine ad carries `GLIDEIN_ToRetire` (glidein end). A real glidein-end eviction hasn't been observed, so whether it ever sends SIGTERM is unknown (§3, §9; P0, `ospool`).
- **Signal and grace:** SIGTERM 0.1–0.6 s after `condor_vacate_job` (once 4.9 s), SIGKILL after 600 s; `condor_hold` the same; `-fast` kills at once. `job_max_vacate_time = 900` was granted (§3; P2, P3a–c, `ospool`).
- **Durability:** `checkpoint_exit_code` alone lost the SIGTERM save; with `ON_EXIT_OR_EVICT` it survived; a hard kill resumed from the last planned checkpoint (§4; P2a, P2b, `ospool`). The `transfer_output_files` requirement was found in recipe 0 (§8).
- **Missing checkpoint path → hold; empty directory accepted** (§4; P8a, P8d).
- **Restarts:** exit 85 restarted in place after ~2 s (P1, `ospool`). Restart gap +4 s for 100 MB, +7 s for 1 GB (P5c, P5d). Local scratch writes ~770 MB/s (P5a). One timed checkpoint cost 18–20 s in all for recipe 1 (615 MB), measured outside the OSPool.
- **`checkpoint_destination = osdf://`:** works; restore ~1 min; SIGTERM save lost (§4, §7; P6a, `ospool`).
- **`NumJobStarts` not updated on exit-85 restarts** (§2; P1). **Only the top process is signaled; `exec` needed** (§6; measured outside the OSPool, same HTCondor mechanism).
- **Exit 0 on a vacate is requeued** (P2c, `ospool`).
- **Recipe tests on the OSPool:** recipe 0 timed exit; recipe 1 timed exit and `condor_vacate_job` passed. Recipe 1 ran out of memory on an 11 GB GPU before `gpus_minimum_memory` was set (outside the OSPool, same risk).
- **Access point survey** (2026-10-23, `probes/ap_survey.sh` on ap40 and ap2002; details in `environment.md` §10):
  - spool holds one copy of the checkpoint directory and is freed when the job finishes;
  - users can read their own job's spool directory;
  - ap40's limits: input 5,000 MB (locked), 20 h per execution, 14 days in total for self-checkpointing jobs, held jobs removed after 30 days, and a hold above 1.8 × `request_cpus` for an hour;
  - the excess-CPU hold is the most common hold of self-checkpointing jobs on ap40 (484 holds on 554 GPU self-checkpointing jobs in 30 days);
  - for 83% of OSPool slots, a glidein stops taking jobs 10 h before it is killed.
- **CPU use of a PyTorch GPU job** (recipe 1, `request_cpus = 4`, no DataLoader workers, 2026-10-23): `OMP_NUM_THREADS` = 4 set by HTCondor, `torch.get_num_threads()` = 4; 0.34 CPUs while training on CHTC (L40S) and 0.52–0.70 on the OSPool (H100, 5 executions) (`environment.md` §10).
- **Input limit, glidein end, OSDF backups** (probes P11d, P12a, P13, 2026-10-26; `environment.md` §10):
  - with `max_transfer_input_mb = 50`, a 100 MB checkpoint restored after a vacate was held ("max total upload bytes exceeded"); with 200 it resumed;
  - a 100 MB `osdf://` input ran under the 50 MB limit;
  - five jobs on glideins that reached `GLIDEIN_ToDie` got no SIGTERM and were killed 104–355 s after it;
  - a directory remapped to `osdf://` arrived only when the job ended, not at its two exits 85; ending with exit 86 instead of 0 works the same (P13b).
  - time caps shrunk to minutes (P14a/b, `timecaps`): an exit 85 every 60 s kept a job under a 150 s per-execution cap; a 240 s total cap held the job 240 s after its first start (code 46), a deadline the job could compute from `JobStartDate + AllowedJobDuration` in its ad.
- **Not tested on the OSPool:** multi-GPU jobs, copies that outlive the job (OSDF uploads), `condor_chirp` in a container. Multi-GB checkpoints near an access point's input limit.
