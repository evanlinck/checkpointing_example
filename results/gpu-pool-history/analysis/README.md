# gpu-pool-history analysis

Scripts behind `../summary.md` (run 2026-10-28 with DuckDB 1.5, pandas, pyarrow). Intermediate files go to `$HOME/gph/` and contain host names; keep them out of the repo.

Order: `a1.py <YYYY-MM>` (per month: one row per GPU per snapshot, primary/backfill state split) → `a2.py` (per machine per snapshot) → `inv.py` (machine inventory and labels; joins `aerie/data/slots.csv` and `gpu-machines/gpu_hosts.tsv`) → `a8.py` (conservative filter, per type per snapshot) → `q2.py`, `q2b.py`, `q4.py` (Q2, Q4) → `a9.py`, `a10.py`, `a11.py`, `q56.py` (claims, Q5, Q6) → `a12.py` (hypothetical backfill survival) → `a13.py`, `a14.py`, `q3.py` (Q3, job-history join) → `q1.py` (Q1 table). Run from `gpu-pool-study/` where a script reads `gpu_parquets/`.
