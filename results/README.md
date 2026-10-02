# Probe results

Summaries from the probe runs in [`../probes/`](../probes/), cited by [`../docs/environment.md`](../docs/environment.md) by run tag. Only the Markdown summaries are kept in git. The raw job files (`job.out`, `job.log`, ads, checkpoints) stay on the maintainer's machine and on ap2002.

| Tag | Date | Sites | Tests |
|---|---|---|---|
| `smoke` | 2026-10-01 | chtc | P0, P1 |
| `core-chtc` | 2026-10-01 | chtc | P2a–d, P3a–d, P4a–b |
| `rest-chtc` | 2026-10-02 | chtc | P2b (all triggers), P5, P6, P7a–c, P8 |
| `backfill` | 2026-10-02 | chtc_backfill | P0, P2a, P2b, P3a, P4a. **Actually landed on ordinary GPU Lab slots** (`+is_resumable` alone doesn't select backfill) |
| `backfill2` | 2026-10-02 | chtc_backfill (`BackfillSlot =?= true`) | P0, P2a, P2b, P3a, P4a |
| `ospool` | 2026-10-02 | ospool | P0, P1, P2a–d, P3a–d, P5, P6a, P8b–d |
| `p7-rerun` | 2026-10-02 | chtc | P7a (container rerun), P7e first attempt (probe bug) |
| `torchrun` | 2026-10-02 | chtc | P7e, P7f |
| `torchrun2` | 2026-10-02 | chtc | P7g, P7h first attempt |
| `torchrun3` | 2026-10-02 | chtc | P7h |

**Reading the `torchrun` reports** (`p7-rerun` P7e, `torchrun`, `torchrun2`, `torchrun3`): `analyze.py` assumes one process per execution. With two workers per execution, its "Restart after …" lines (negative gaps, "restored step None") and some "SIGTERM save was LOST" or "NO signal" verdicts are wrong. For example, in `torchrun3` the wrapper received SIGTERM and the workers deliberately never did. The correct readings, taken from the raw timelines, are in `docs/environment.md` §6:
- **P7g:** workers finished a 60 s save after SIGTERM.
- **P7h:** the save made after SIGTERM survived on a new host, at step 84.

All reports here have user names, personal paths and IP addresses replaced (`probes/redact.py`).
