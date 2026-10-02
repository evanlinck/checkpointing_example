# HTCondor checkpoint probes

These are small test jobs that measure how HTCondor actually treats a self-checkpointing job on our pools (CHTC, CHTC backfill, CHTC GPU, OSPool). The HTCondor manual leaves several things unclear, and the checkpointing recipes depend on them, so we measure them before writing the recipes.

The probes do no ML. `probe.py` pretends to train at one "step" per second and logs everything that happens to it. It uses only the Python standard library.

## What we want to learn

| Test | Question |
|---|---|
| **P0** fingerprint | What does each pool give a job? HTCondor version, `MachineMaxVacateTime` / `MaxJobRetirementTime`, `/staging`, internet, container, `condor_chirp`, GPUs. |
| **P1** voluntary exit 85 | After exit 85, does the job restart in the same sandbox on the same host? Do nested directories transfer? How long is the gap? What happens to stdout? |
| **P2a–d** vacate + spool | **Key test.** A SIGTERM arrives after a voluntary checkpoint (A). The job saves B and exits 85. Does the restart see A or B? Variants add `ON_EXIT_OR_EVICT` (P2b), exit with 0 instead of 85 (P2c), or install no SIGTERM handler (P2d). |
| **P3a–e** grace window | How long between the soft-kill signal and SIGKILL? Is there a retirement delay? Are `job_max_vacate_time` and `kill_sig` honoured? P3e waits for a real backfill eviction (GPU). |
| **P4a–b** staging mode | Is a SIGTERM save written straight to `/staging` durable after the job is rescheduled? Does rename, fsync and the `latest` pointer work there? What does a hard kill in the middle of a save leave behind? |
| **P5a–e** size and speed | Write speed to scratch vs. `/staging`, and the spool-transfer gap for 100 MB, 1 GB and 5 GB checkpoints. |
| **P6a–b** `checkpoint_destination` | Does sending checkpoints to `osdf://` or `file:///staging` work, and does the restart get them back? |
| **P7a–e** signal delivery | Who receives the signal: a wrapper with `exec`, a wrapper without `exec`, child processes, Apptainer, `torchrun`? |
| **P8a–d** failure modes | A missing checkpoint file, exiting 85 every 5 s, no `checkpoint_exit_code`, an empty checkpoint directory. |

> **Before anything else:** `export PROBE_STAGING_DIR=/staging/<username>` (add it to `~/.bashrc` on the access point). `make_dag.py`, `setup.sh` and `cleanup.sh` refuse to run without it, so no personal path has to be stored in the repo.

`python3 make_dag.py --list` prints every test with its sites, triggers and full question.

## Files

| File | Role |
|---|---|
| `probe.py` | The probe that runs on the execute point (EP). |
| `common.sub`, `sites/*.sub`, `tests/*.sub` | Submit-file pieces. A job's `job.sub` = common + site + test. |
| `make_dag.py` | Assembles `runs/<tag>/<site>/<test>/job.sub` and the DAG `runs/<tag>/probes.dag`. |
| `trigger.py` | Runs on the access point (AP) and fires `condor_vacate_job` / `-fast` / `condor_hold` + `condor_release` at the right moment. |
| `analyze.py` | Writes `results/<tag>/<site>/<test>.md` after each job, plus `results/<tag>/summary.md`. |
| `eventlog.py` | Reads HTCondor job event logs (used by `trigger.py` and `analyze.py`). |
| `run_exec.sh`, `run_noexec.sh`, `run_torchrun.sh` | Wrapper variants for P7. |
| `setup.sh`, `build.sub`, `pytorch-cpu.def` | One-time setup: `/staging` dirs and container images. |
| `cleanup.sh` | Deletes probe data from `/staging`. |

## Load on the schedd

Nothing here polls `condor_q`.

- `trigger.py` decides when to fire by re-reading the job's **event log** (`job.log`, a local file) every 15 s. It sends exactly one eviction command (retried up to 3 times if the command fails), and in hold mode one release.
- `analyze.py` makes **one** `condor_history -limit 1 -long <job>` call per job, after the job has left the queue, and caches it in `history_ad.txt`.
- DAGMan follows jobs through their event logs too. `MAXJOBS probes 4` keeps at most four probe jobs in the queue (`--maxjobs` changes this).

## One-time setup

1. **Copy this directory to ap2002**, e.g. `~/ckpt-probes/`.
2. **Tell the tools where your `/staging` directory is.** Every script and `make_dag.py` read it from the environment, so no personal path is stored in the repo:
   ```
   export PROBE_STAGING_DIR=/staging/<user>      # add to ~/.bashrc on ap2002
   ```
3. **Create the staging dirs:** `bash setup.sh dirs`
4. **Build the container image** in an interactive build job, as CHTC requests:
   ```
   condor_submit -i build.sub
   export PROBE_STAGING_DIR=/staging/<user>
   bash setup.sh build                # add --with-torch for the optional P7e test
   exit
   ```
   This puts `python312.sif` (and `pytorch.sif`) in `$PROBE_STAGING_DIR/ckpt-probes/images/`. OSDF caches files by name, so if you ever rebuild an image, give it a **new file name** and update `sites/*.sub`.
5. **Check the placeholders marked CONFIRM:**
   - `sites/chtc_gpu.sub`: the GPU Lab attributes.
   - `sites/chtc_backfill.sub`: is `+is_resumable = true` how to reach backfill?
   - `build.sub`: `+IsBuildJob`.
6. **Record the AP side** (once):
   ```
   (condor_version; condor_config_val MachineMaxVacateTime MaxJobRetirementTime) > ap_info.txt
   ```

## Running

Start small, check the results, then widen.

**Step 1: smoke test (two CHTC jobs plus their bare variants, ~5 min).** This checks the container path, `/staging`, and whether the local universe is allowed.
```
python3 make_dag.py --sites chtc --tests P0,P1 --check --tag smoke
condor_submit_dag runs/smoke/probes.dag
# when it finishes:
cat results/smoke/summary.md
```
`--check` runs `condor_submit -dry-run` on each job and leaves rejected ones out of the DAG. The P2b `ON_EXIT_OR_EVICT` combination may be rejected this way, which is itself an answer.

**Step 2: core questions on CHTC.**
```
python3 make_dag.py --sites chtc --tests P2,P3,P4 --check --tag core-chtc
condor_submit_dag runs/core-chtc/probes.dag
```

**Step 3: everything on CPU sites** (about 50 probe jobs plus their trigger jobs, each under ~15 min, four at a time):
```
python3 make_dag.py --sites chtc,ospool --check --tag full
condor_submit_dag runs/full/probes.dag
```

**Step 4: backfill and GPU (uses GPUs, so it is kept small).** At CHTC, backfill is essentially a GPU-slot matter: CPU slots are plentiful enough that CPU jobs rarely run as backfill. So `chtc_backfill` requests a GPU **and requires `BackfillSlot =?= true`**: `+is_resumable = true` alone only makes a job *eligible* for backfill, and our first run landed on an ordinary GPU Lab slot. Only P0, P2a, P2b, P3a and P4a (plus the opt-in P3e) run there. The probe never touches the GPU. Check P0's `out/machine_ad.txt` for `BackfillSlot = true`.
```
python3 make_dag.py --sites chtc_backfill --triggers vacate --no-bare --check --tag backfill
condor_submit_dag runs/backfill/probes.dag
```
That is four GPU jobs, about 25 GPU-minutes in total. Without `--triggers vacate --no-bare` it is nine jobs (adds vacate-fast and hold-release for P2a, hold-release for P3a, and the bare variants), about an hour. `chtc_gpu` (ordinary GPU Lab slots, for comparison) runs only P0 and P3a:
```
python3 make_dag.py --sites chtc_gpu --triggers vacate --no-bare --check --tag gpu
```

**Opt-in tests** need to be named with `--optin`:
- `P3e`: waits up to 6 h for a real backfill eviction. It holds a GPU the whole time.
- `P5b`: 10 GB writes.
- `P5e`: a 5 GB checkpoint through spool.
- `P7e`: `torchrun`, needs `pytorch.sif`.

For example:
```
python3 make_dag.py --sites chtc_backfill --tests P3e --optin P3e --tag natural
```

### If the AP does not allow local-universe jobs

The trigger and summary DAG nodes run in the local universe on the AP. If those nodes fail to submit, rebuild without them and run the triggers yourself:
```
python3 make_dag.py ... --no-trigger-nodes --tag full
condor_submit_dag runs/full/probes.dag
nohup bash runs/full/run_triggers.sh > runs/full/run_triggers.log 2>&1 &
```

### Running a single test by hand

```
cd runs/<tag>/<site>/<test>
condor_submit job.sub
python3 ../../../../trigger.py --log job.log --action vacate --after 150 &   # only for tests with a trigger
# after the job leaves the queue:
python3 ../../../../analyze.py --test-dir . --job-id <cluster>.0
```

## What to send back

Reports are written with user names, personal paths and IP addresses already replaced (`redact.py`). To clean reports made by an older version, or any other text before sharing it: `python3 redact.py results/` (`--check` lists files without changing them).


The `results/<tag>/` folder: `summary.md` plus one `.md` and `.json` per test, together with `ap_info.txt`. If something looks odd, the matching `runs/<tag>/<site>/<test>/` folder (job.log, job.out, job.err, trigger.jsonl) has the raw data.

## Reading the results

- **Restored step and "saved by".** Each restart reports which checkpoint it found and why it had been saved (`voluntary`, `signal`, `periodic`). In P2, "the SIGTERM save SURVIVED / was LOST" is the answer to the key question.
- **Grace.** For P3, "last sign of life N s after the signal" is the vacate window you actually get. Heartbeats come once a second, so the figure is accurate to about ±1 s.
- **Clocks.** The trigger and event-log times come from the AP. Probe times come from the EP. Small offsets between the two clocks show up in the "signal N s after the trigger" figure.
- **Cost.** P3 deliberately ignores the signal and uses up its full grace period, at most ~10 minutes per job, which is GPU time on `chtc_gpu` and `chtc_backfill`. Every job is removed automatically after 2 h in the queue or 10 min on hold (P3e: 8 h).

## Cleanup

```
bash cleanup.sh          # shows what would be deleted
bash cleanup.sh --yes    # deletes $PROBE_STAGING_DIR/ckpt-probes/runs/* (keeps the images)
```
`runs/` is git-ignored. Delete old run directories whenever you like.
