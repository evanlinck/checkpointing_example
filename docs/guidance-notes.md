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
