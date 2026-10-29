# CHTC GPU pool history: can a 4 × 80 GB job run on one machine?

For recipe 3 (full fine-tune of a 7B model with FSDP and DCP). It needs one machine with 4 GPUs of ≥ 75 GB (fallback: 2), 150–200 GB host memory, about 16 CPUs, about 50 GB disk, CUDA driver ≥ 12.8 and `/staging`.

Analysis run 2026-10-28. No host names, user names or projects appear below. Machines are labelled `<type>-<n>`. Times are US Central (America/Chicago). Unless a table says otherwise, the planning numbers are for **Apr 1 – Oct 19, 2026**, when the pool was 85–89 % claimed. Earlier months were emptier and overstate availability.

## The data

| | |
|---|---|
| Source | `gpu-pool-study/gpu_parquets/gpu_state_YYYY-MM.parquet` (iross/gpureports pool snapshots), 18 monthly files, 75.4 M rows |
| Time range | 2025-05-07 → 2026-10-19 |
| Snapshot interval | Every 15 min until Jul 2025, every 5 min from Aug 2025. 130,836 snapshots. Gaps: Mar 30–31 2026, Apr 30 – May 5 2026, end of Jul 31 2026 |
| One record = | One GPU in one slot at one snapshot |
| Attributes | `timestamp`, `Name` (slot name), `Machine`, `State` (Claimed / Unclaimed / Owner / Drained / Preempting), `AssignedGPUs`, `AvailableGPUs`, `GPUs_DeviceName`, `GPUs_GlobalMemoryMb`, `PrioritizedProjects`, `GlobalJobId`, `RemoteOwner`, `GPUsAverageUsage`, `PreventJobsReason`. `Disk` (KB, per slot) only from 2026-08-19 |
| GPU Lab vs backfill | **Separate records.** The same GPU appears once under its primary slot (`slot2`/`slot3`…) and once under `backfill1` (and `interactive3` on some machines). A GPU running a backfill job shows **Unclaimed** on its primary slot and **Claimed** on `backfill1`. A primary claim has no backfill row. GPU Lab vs prioritized is **not** recorded directly (no `IsGPULabSlot`); I took "GPU Lab" to mean a primary slot with an empty `PrioritizedProjects` |
| Free vs claimed | Yes, per GPU per slot (`State`). There is no `Activity`, no multi-GPU hold-timer state and no `START` expression. "Unclaimed" therefore doesn't prove that a job could match |
| Memory, CPUs per machine | **Not in the snapshots.** Totals come from `aerie/data/slots.csv` (`TotalSlotCpus`, `TotalSlotMemory`, `GPUs_Capability`), a single collector snapshot from 2026-10-15 applied to the whole period. Used memory and CPUs at a given moment are estimated by joining `GlobalJobId` to the ap2001/ap2002 job history (`MemoryProvisioned`, `CpusProvisioned`). This covers 95–98 % of primary claims. Jobs from other APs and CPU-only jobs are not visible |
| Disk | In the snapshots from 2026-08-19 (an Unclaimed partitionable slot's `Disk` = free disk) |
| Not recorded anywhere in this data | `CUDADriverVersion`, `HasCHTCStaging`, NVLink/interconnect, and history of compute capability |

Definitions used in the tables:

- **lab ≥ k**: a GPU Lab (non-prioritized) primary slot on one machine had ≥ k GPUs Unclaimed. Some of those GPUs may have been running backfill jobs, which a GPU Lab job would evict (30 s retirement). This is what a GPU Lab job can claim.
- **idle ≥ k**: the same, but the GPUs were also not running backfill (completely idle).
- **bf ≥ k**: the `backfill1` slot had ≥ k GPUs Unclaimed, and those GPUs were not claimed by a primary job (any machine, including prioritized ones).
- **Conservative** (used throughout): drops machine-snapshots inside runs of ≥ 3 days where the whole machine sat idle. Those are probably machines that no job could match (the pool study found such cases, e.g. one machine unmatched for 111 days). This removes 4.7 % of machine-snapshots.
- Tier **≥ 75 GB** = H200, H200 NVL, RTX PRO 6000 (96 GB), A100-80GB, H100. Tier **40–75 GB** = L40S, L40, A40, A100-40GB. Only machines with ≥ 2 GPUs are counted.

## 1. Which machines qualify

Driver and CC: the snapshots record neither. CC comes from `slots.csv` (Oct 2026). Drivers are the versions the compatibility-matrix jobs saw on each GPU **type** (Sep 22 – Oct 23 2026). They are not per machine, and there is no history before that. "Max free disk" is the largest free disk seen on the primary slot since Aug 19 2026, used as a stand-in for the machine's execute disk. `HasCHTCStaging` isn't in the data. The probes (`environment.md` §1) found it true on every CHTC GPU Lab and backfill slot they tested.

| label          |   GPU mem GB |   GPUs | Host mem GB   | CPUs   | Max free disk TB   | Driver (CUDA) seen on type   | CC   | Access now           |   GPU Lab % of period | Seen              |
|:---------------|-------------:|-------:|:--------------|:-------|:-------------------|:-----------------------------|:-----|:---------------------|----------------------:|:------------------|
| H200-1         |          140 |      4 | 1005          | 96     | 26.4               | 570 (12.8) / 590 (13.1)      | 9.0  | prioritized          |                     0 | 2025-05 → now     |
| H200-2         |          140 |      8 | 2012          | 192    | 27.7               | 570 (12.8) / 590 (13.1)      | 9.0  | GPU Lab              |                    68 | 2025-07 → now     |
| H200-3         |          140 |      8 | 2012          | 192    | 20.8               | 570 (12.8) / 590 (13.1)      | 9.0  | mixed (75% Lab)      |                    81 | 2025-08 → now     |
| H200-4         |          140 |      8 | 2012          | 192    | 27.7               | 570 (12.8) / 590 (13.1)      | 9.0  | prioritized          |                    22 | 2025-08 → now     |
| H200-5         |          140 |      8 | –             | –      | –                  | 570 (12.8) / 590 (13.1)      | –    | removed              |                   100 | 2025-09 → 2025-09 |
| H200-6         |          140 |      8 | 2012          | 192    | 7.7                | 570 (12.8) / 590 (13.1)      | 9.0  | prioritized          |                    10 | 2025-09 → now     |
| H200-7         |          140 |      8 | 1004          | 192    | 14.0               | 570 (12.8) / 590 (13.1)      | 9.0  | mixed (50% Lab)      |                    50 | 2026-06 → now     |
| H200-8         |          140 |      8 | 1004          | 192    | 27.9               | 570 (12.8) / 590 (13.1)      | 9.0  | GPU Lab              |                   100 | 2026-06 → now     |
| H200-9         |          140 |      8 | 1004          | 192    | 27.9               | 570 (12.8) / 590 (13.1)      | 9.0  | GPU Lab              |                   100 | 2026-06 → now     |
| H200 NVL-1     |          140 |      4 | 1508          | 256    | 14.0               | not tested                   | 9.0  | prioritized          |                     3 | 2025-12 → now     |
| RTX PRO 6000-1 |           95 |      8 | 752           | 192    | 27.9               | 590 (13.1)                   | 12.0 | prioritized          |                     0 | 2026-06 → now     |
| RTX PRO 6000-2 |           95 |      8 | 752           | 192    | 27.9               | 590 (13.1)                   | 12.0 | prioritized          |                     0 | 2026-06 → now     |
| RTX PRO 6000-3 |           95 |      8 | 752           | 192    | 27.9               | 590 (13.1)                   | 12.0 | mixed (40% Lab)      |                    40 | 2026-09 → now     |
| RTX PRO 6000-4 |           95 |      8 | 753           | 48     | 27.9               | 590 (13.1)                   | 12.0 | GPU Lab              |                   100 | 2026-09 → now     |
| A100-80GB-1    |           79 |      4 | 500           | 128    | 1.4                | 570 (12.8)                   | 8.0  | prioritized          |                    55 | 2025-05 → now     |
| A100-80GB-2    |           79 |      3 | 500           | 128    | 5.6                | 570 (12.8)                   | 8.0  | GPU Lab              |                    49 | 2025-05 → now     |
| A100-80GB-3    |           79 |      8 | 1005          | 96     | 13.2               | 570 (12.8)                   | 8.0  | prioritized          |                     0 | 2025-05 → now     |
| A100-80GB-4    |           79 |      4 | –             | –      | –                  | 570 (12.8)                   | –    | removed              |                   100 | 2025-05 → 2026-08 |
| A100-80GB-5    |           79 |      4 | –             | –      | –                  | 570 (12.8)                   | –    | removed              |                   100 | 2025-05 → 2026-08 |
| A100-80GB-6    |           79 |      4 | 500           | 128    | 2.5                | 570 (12.8)                   | 8.0  | GPU Lab              |                   100 | 2025-05 → now     |
| A100-80GB-7    |           79 |      4 | 500           | 128    | 5.5                | 570 (12.8)                   | 8.0  | GPU Lab              |                   100 | 2025-05 → now     |
| A100-80GB-8    |           79 |      4 | 500           | 128    | 5.5                | 570 (12.8)                   | 8.0  | GPU Lab              |                   100 | 2025-05 → now     |
| A100-80GB-9    |           79 |      4 | 500           | 128    | 5.5                | 570 (12.8)                   | 8.0  | MIG since 2026-03-30 |                    61 | 2025-05 → now     |
| A100-80GB-10   |           79 |      4 | 500           | 128    | 5.6                | 570 (12.8)                   | 8.0  | GPU Lab              |                   100 | 2025-05 → now     |
| A100-80GB-11   |           79 |      4 | –             | –      | –                  | 570 (12.8)                   | –    | removed              |                   100 | 2025-05 → 2025-11 |
| H100-1         |           79 |      8 | 2013          | 160    | 27.9               | 570 (12.8)                   | 9.0  | GPU Lab              |                   100 | 2025-05 → now     |
| H100-2         |           79 |      8 | 2013          | 160    | 13.2               | 570 (12.8)                   | 9.0  | prioritized          |                     3 | 2025-05 → now     |
| L40S-1         |           45 |      8 | 469           | 96     | 26.4               | 570 (12.8) / 590 (13.1)      | 8.9  | prioritized          |                     0 | 2025-05 → now     |
| L40S-2         |           45 |      8 | 501           | 96     | 26.4               | 570 (12.8) / 590 (13.1)      | 8.9  | prioritized          |                     0 | 2025-05 → now     |
| L40S-3         |           45 |      8 | 485           | 96     | 21.7               | 570 (12.8) / 590 (13.1)      | 8.9  | prioritized          |                     0 | 2025-05 → now     |
| L40S-4         |           45 |      8 | 469           | 96     | 26.4               | 570 (12.8) / 590 (13.1)      | 8.9  | prioritized          |                     6 | 2025-05 → now     |
| L40S-5         |           45 |      8 | 501           | 96     | 14.0               | 570 (12.8) / 590 (13.1)      | 8.9  | prioritized          |                     0 | 2025-07 → now     |
| L40S-6         |           45 |      8 | 752           | 192    | 11.9               | 570 (12.8) / 590 (13.1)      | 8.9  | prioritized          |                     0 | 2025-07 → now     |
| L40S-7         |           45 |      8 | 753           | 192    | 27.9               | 570 (12.8) / 590 (13.1)      | 8.9  | GPU Lab              |                    56 | 2025-09 → now     |
| L40S-8         |           45 |      8 | 752           | 192    | 27.9               | 570 (12.8) / 590 (13.1)      | 8.9  | GPU Lab              |                    92 | 2025-09 → now     |
| L40S-9         |           45 |      8 | 1131          | 96     | 8.5                | 570 (12.8) / 590 (13.1)      | 8.9  | prioritized          |                     0 | 2025-09 → now     |
| L40S-10        |           45 |      8 | 1131          | 96     | 8.5                | 570 (12.8) / 590 (13.1)      | 8.9  | prioritized          |                     0 | 2025-10 → now     |
| L40S-11        |           44 |      8 | 753           | 192    | 27.9               | 570 (12.8) / 590 (13.1)      | 8.9  | prioritized          |                    12 | 2025-10 → now     |
| L40S-12        |           44 |      8 | 752           | 192    | 21.0               | 570 (12.8) / 590 (13.1)      | 8.9  | mixed (75% Lab)      |                    75 | 2026-06 → now     |
| L40S-13        |           44 |      8 | 752           | 192    | 27.9               | 570 (12.8) / 590 (13.1)      | 8.9  | prioritized          |                     0 | 2026-06 → now     |
| A40-1          |           44 |      8 | 500           | 96     | 7.0                | not tested                   | 8.6  | prioritized          |                     0 | 2025-05 → now     |
| L40-1          |           44 |     10 | 501           | 96     | 11.3               | 570 (12.8)                   | 8.9  | prioritized          |                     0 | 2025-05 → now     |
| L40-2          |           44 |     10 | 501           | 96     | 11.3               | 570 (12.8)                   | 8.9  | prioritized          |                     0 | 2025-05 → now     |
| L40-3          |           44 |     10 | 501           | 96     | 11.3               | 570 (12.8)                   | 8.9  | prioritized          |                     0 | 2025-05 → now     |
| L40-4          |           44 |     10 | 501           | 96     | 14.0               | 570 (12.8)                   | 8.9  | GPU Lab              |                    94 | 2025-05 → now     |
| L40-5          |           44 |      9 | 484           | 96     | 14.0               | 570 (12.8)                   | 8.9  | GPU Lab              |                    95 | 2025-05 → now     |
| L40-6          |           44 |      9 | 500           | 96     | 14.0               | 570 (12.8)                   | 8.9  | GPU Lab              |                   100 | 2025-05 → now     |
| L40-7          |           44 |     10 | 500           | 96     | 6.0                | 570 (12.8)                   | 8.9  | prioritized          |                     0 | 2025-05 → now     |
| L40-8          |           44 |      9 | 500           | 96     | 0.9                | 570 (12.8)                   | 8.9  | prioritized          |                     0 | 2025-05 → now     |
| L40-9          |           44 |      9 | 501           | 96     | 14.0               | 570 (12.8)                   | 8.9  | prioritized          |                     0 | 2025-05 → now     |
| A100-40GB-1    |           39 |      4 | 2001          | 96     | 13.2               | 570 (12.8)                   | 8.0  | prioritized          |                     0 | 2025-05 → now     |
| A100-40GB-2    |           39 |      4 | 1501          | 72     | 2.6                | 570 (12.8)                   | 8.0  | mixed (75% Lab)      |                    33 | 2025-05 → now     |
| A100-40GB-3    |           39 |      4 | 2001          | 96     | 1.2                | 570 (12.8)                   | 8.0  | GPU Lab              |                    99 | 2025-05 → now     |
| A100-40GB-4    |           39 |      4 | 1005          | 96     | 26.4               | 570 (12.8)                   | 8.0  | prioritized          |                     0 | 2025-05 → now     |
| A100-40GB-5    |           39 |      8 | 1005          | 96     | 41.3               | 570 (12.8)                   | 8.0  | prioritized          |                     0 | 2025-05 → now     |
| A100-40GB-6    |           39 |      4 | –             | –      | 3.3                | 570 (12.8)                   | –    | prioritized          |                     0 | 2025-05 → now     |

"Mixed" means part of the machine's GPUs are in a GPU Lab slot and the rest are prioritized. A general user's job can only use the GPU Lab part (or backfill). The GB10 (2 single-GPU machines, 124 GB unified memory, ARM) and the single-GPU RTX 8000 have only 1 GPU each and are left out.

**What a GPU Lab 4-GPU job can use today (≥ 75 GB):** 3 H200 machines fully in GPU Lab plus the GPU Lab part of 2 mixed ones, 1 H100 machine (8 GPUs), 4 A100-80GB machines with 4 GPUs, and 1 RTX PRO 6000 machine (Blackwell). That's about 9–11 machines. Backfill reaches every machine in the table.

**Changes over the period:**

- **H200:** 1 machine in May 2025. Three added Jul–Aug 2025, one (H200-5) present for one week in Sept 2025, one in Sept 2025, the H200 NVL in Dec 2025, three in Jun 2026.
- **RTX PRO 6000:** two machines from Jun 30 2026, two more Sept 24/30 2026.
- **A100-80GB:** 11 machines, then one removed Nov 2025 and two removed Aug 2026. A100-80GB-9 was split into 8 MIG 3g.40gb instances on Mar 30 2026.
- **Access changes:** several machines moved between GPU Lab and prioritized. A100-80GB-1 became prioritized in Mar 2026; H100-2 in Mar 2026; H200-2 left GPU Lab Feb 2026 and came back Jul 2026; H200-4/H200-6 became prioritized Oct–Nov 2025.
- **Drivers:** the data can't show driver upgrades.

**What this means for the 4 × 80 GB job:** about 9–11 machines can take a 4-GPU GPU Lab job: H200, H100, A100-80GB and one RTX PRO 6000. Every one of them has ≥ 500 GB of host memory, ≥ 48 CPUs and terabytes of disk, so the host requirements don't narrow the list. The list does change often: the A100-80GB set lost 3 machines and one to MIG this year. A requirement on GPU memory (≥ 79 GB) fits better than a list of model names.

## 2. How often were 4 (or 2) GPUs free on one qualifying machine

Share of snapshots in which at least one machine of the group had ≥ k GPUs free at once. Conservative version.

| group        | lab ≥4 Apr–Oct 26 | idle ≥4 Apr–Oct 26 | bf ≥4 Apr–Oct 26 | lab ≥2 Apr–Oct 26 | bf ≥2 Apr–Oct 26 | lab ≥4 May 25–Oct 26 | bf ≥4 May 25–Oct 26 |
|:-------------|------:|------:|------:|------:|------:|------:|------:|
| H200         | 13.1 | 10.4 | 13.3 | 24.2 | 25.9 | 18.0 | 19.6 |
| H200 NVL     |  0.0 |  0.0 |  0.0 |  0.0 |  1.4 |  2.6 |  1.4 |
| RTX PRO 6000 |  1.0 |  0.5 |  4.2 |  4.0 |  8.2 |  1.0 |  4.2 |
| A100-80GB    |  1.7 |  0.2 |  0.4 | 16.8 |  9.6 | 39.9 | 16.8 |
| H100         |  7.1 |  2.1 |  3.2 | 12.2 |  4.5 |  8.0 | 11.7 |
| L40S         |  9.4 |  6.2 | 15.3 | 14.5 | 27.0 | 10.2 | 43.5 |
| L40          | 19.1 |  8.4 | 25.6 | 25.9 | 35.5 | 20.0 | 45.5 |
| A40          |  0.0 |  0.0 |  1.1 |  0.0 | 22.5 |  0.0 | 14.4 |
| A100-40GB    |  0.1 |  0.0 |  6.4 |  8.1 | 12.2 |  4.5 | 19.6 |
| **Any ≥ 75 GB** | **18.2** | **11.5** | **16.0** | **38.4** | **33.7** | 49.1 | 34.9 |
| Any 40–75 GB | 22.6 | 13.3 | 39.8 | 34.8 | 68.2 | 25.6 | 62.7 |
| Any ≥ 40 GB  | 32.6 | 20.5 | 48.1 | 53.0 | 77.7 | 57.2 | 68.0 |

By month (% of snapshots, conservative):

| month   | ≥75 lab≥4 | H200 lab≥4 | H100 lab≥4 | A100-80 lab≥4 | RTX6000 lab≥4 | 40–75 lab≥4 | L40S lab≥4 | L40 lab≥4 | ≥75 idle≥4 | ≥75 bf≥4 | ≥75 lab≥2 | 40–75 bf≥4 |
|:--------|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2025-05 | 99 |  0 |  9 | 99 | – | 38 |  4 | 34 | 22 | 72 | 100 |  99 |
| 2025-06 |  9 |  0 |  1 |  8 | – | 14 |  2 |  4 |  6 | 81 |  31 | 100 |
| 2025-07 | 80 |  2 |  4 | 78 | – | 21 |  7 | 15 | 65 | 84 |  86 | 100 |
| 2025-08 | 72 | 14 |  9 | 67 | – | 21 |  0 | 21 | 46 | 59 |  77 | 100 |
| 2025-09 | 82 | 27 |  8 | 76 | – | 17 |  0 | 12 | 65 | 79 |  91 | 100 |
| 2025-10 | 96 | 54 | 28 | 95 | – | 66 | 55 | 36 | 50 | 61 |  96 |  98 |
| 2025-11 |100 | 30 |  8 |100 | – | 31 | 20 | 20 | 18 | 18 | 100 |  75 |
| 2025-12 | 44 | 14 |  0 | 30 | – | 17 |  1 | 17 | 25 | 40 |  48 |  42 |
| 2026-01 | 68 | 44 |  8 | 65 | – | 35 | 11 | 28 | 38 | 45 |  76 |  78 |
| 2026-02 | 82 |  1 |  2 | 82 | – |  9 |  0 |  9 |  2 | 35 |  82 |  68 |
| 2026-03 | 33 |  0 |  9 | 28 | – | 29 |  2 | 26 |  9 | 16 |  81 |  53 |
| 2026-04 |  7 |  5 |  3 |  2 | – | 14 |  7 | 12 |  3 |  7 |  18 |  81 |
| 2026-05 |  3 |  0 |  3 |  0 | – | 16 |  9 | 11 |  2 |  3 |  11 |  32 |
| 2026-06 | 32 | 19 | 15 |  2 | 0 | 14 |  8 |  6 | 15 | 25 |  61 |  29 |
| 2026-07 | 34 | 32 |  3 |  1 | 0 | 30 |  2 | 29 | 26 | 27 |  76 |  48 |
| 2026-08 |  8 |  6 |  6 |  1 | 0 | 14 |  8 | 13 |  6 | 15 |  15 |  11 |
| 2026-09 | 28 | 19 | 14 |  5 | 0 | 55 | 26 | 49 | 17 | 22 |  53 |  39 |
| 2026-10 | 11 |  6 |  4 |  0 | 6 |  9 |  4 |  8 |  8 |  9 |  28 |  37 |

Until Feb 2026, almost all of the "≥ 75 GB lab ≥ 4" figure comes from a single GPU Lab A100-80GB machine, A100-80GB-1. From Jun 2025 to Jan 2026 it had all 4 GPUs idle in 30–94 % of snapshots in most months (11 % in Nov 2025), while still running occasional jobs. In Mar 2026 it became prioritized. That pattern looks like a machine most jobs couldn't match. The conservative filter only removes multi-day stretches of complete idleness, so this machine's partly-busy time stays in. **Treat the 2025 to early-2026 A100-80GB and "any ≥ 75 GB" figures as overstated.**

By day of week, Apr–Oct 2026 (% of snapshots):

| day | ≥75 lab≥4 | H200 lab≥4 | H100 lab≥4 | 40–75 lab≥4 | ≥75 idle≥4 | ≥75 bf≥4 | ≥75 lab≥2 |
|:----|---:|---:|---:|---:|---:|---:|---:|
| Mon | 21 | 16 | 7 | 19 |  8 | 11 | 37 |
| Tue | 23 | 19 | 6 | 15 | 14 | 18 | 38 |
| Wed | 19 | 14 | 5 | 20 | 13 | 15 | 40 |
| Thu | 13 |  8 | 6 | 23 |  8 | 15 | 40 |
| Fri | 20 | 11 | 9 | 27 | 14 | 24 | 41 |
| Sat | 16 | 10 | 8 | 29 | 11 | 17 | 40 |
| Sun | 15 | 13 | 8 | 23 | 11 | 13 | 32 |

By hour of day (Central), Apr–Oct 2026 (% of snapshots):

| hour | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| ≥75 lab≥4  | 19 | 20 | 20 | 19 | 20 | 20 | 21 | 21 | 19 | 18 | 19 | 16 | 15 | 17 | 17 | 15 | 14 | 16 | 17 | 17 | 20 | 20 | 19 | 19 |
| H200 lab≥4 | 14 | 14 | 15 | 15 | 15 | 15 | 14 | 13 | 13 | 13 | 13 | 11 |  9 | 11 | 12 | 11 | 11 | 12 | 12 | 13 | 13 | 15 | 14 | 14 |
| H100 lab≥4 |  8 |  9 |  9 |  7 |  9 |  9 |  8 |  8 |  8 |  7 |  8 |  6 |  5 |  5 |  6 |  5 |  4 |  6 |  6 |  6 |  8 |  8 |  8 |  8 |
| 40–75 lab≥4 | 26 | 25 | 24 | 25 | 25 | 24 | 25 | 22 | 22 | 20 | 18 | 16 | 16 | 17 | 20 | 22 | 23 | 24 | 24 | 25 | 26 | 24 | 24 | 25 |
| ≥75 idle≥4 | 14 | 13 | 12 | 11 | 13 | 13 | 13 | 12 | 12 | 12 | 12 |  9 |  8 | 10 | 10 | 10 | 10 | 11 | 11 | 11 | 11 | 12 | 12 | 13 |
| ≥75 bf≥4   | 18 | 17 | 17 | 15 | 16 | 16 | 18 | 17 | 17 | 16 | 16 | 14 | 13 | 17 | 16 | 16 | 15 | 15 | 16 | 15 | 15 | 16 | 16 | 18 |
| ≥75 lab≥2  | 42 | 39 | 37 | 37 | 39 | 40 | 40 | 38 | 38 | 40 | 38 | 36 | 34 | 39 | 35 | 35 | 35 | 36 | 37 | 40 | 41 | 39 | 40 | 43 |

**What this means for the 4 × 80 GB job:** in the busy months since April, 4 free ≥ 75 GB GPU Lab GPUs on one machine showed up in about 1 snapshot in 5 (18 %), mostly on H200 and H100. 2 free GPUs showed up twice as often (38 %). Month-to-month swings (3 % to 34 %) are much larger than the effect of weekday or hour. The A100-80GB machines, which recipe 3's README lists first, almost never had 4 free GPU Lab GPUs after March 2026 (1.7 %).

## 3. When 4 GPUs were free, was the rest of the machine free?

These are hourly samples of the moments in Q2 (Sep 2025 – Oct 2026; the table shows Apr–Oct 2026). Free memory/CPUs = the slot's total from the Oct 2026 `slots.csv` minus the provisioned memory/CPUs of the GPU jobs running on it. Jobs from other APs (about 2–5 %) and CPU-only jobs are not counted, so these are upper bounds. Free disk is measured directly (from Aug 19 2026 only).

GPU Lab moments (≥ 4 GPU Lab GPUs free; machines that are fully GPU Lab), Apr–Oct 2026:

| type         | moments | free mem GB p50 | p10 | min | free CPUs p50 | p10 | ≥ 200 GB % | ≥ 16 CPUs % | both % | free disk GB p50 | ≥ 50 GB disk % |
|:-------------|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| A100-80GB    |    88 |   500 |   500 |   500 |   128 |   128 |   100 |   100 |   100 |  5705 | 100 |
| H100         |   334 |  1821 |  1674 |  1201 |   144 |   132 |   100 |   100 |   100 | 28463 | 100 |
| H200         |   561 |  1004 |   776 |   404 |   182 |   170 |   100 |   100 |   100 | 28412 | 100 |
| RTX PRO 6000 |    27 |   703 |   562 |   485 |    37 |    18 |   100 |    93 |    93 | 28526 | 100 |
| L40S         |   402 |   656 |   544 |   240 |   180 |   168 |   100 |   100 |   100 | 28503 | 100 |
| L40          |  1133 |   428 |   281 |   105 |    83 |    63 |    98 |   100 |    98 | 14156 | 100 |

Backfill moments (≥ 4 backfill GPUs free), Apr–Oct 2026. "After primary" also subtracts the primary-slot jobs that share the machine:

| type         | moments | free mem GB p50 (backfill slot) | p50 after primary | p10 after primary | free CPUs p50 (slot) | after primary | p10 after primary | 200 GB + 16 CPUs free % | free disk GB p50 |
|:-------------|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| A100-40GB    |   285 |  2001 |  2001 |  2001 |  96 |  96 |  96 | 100 |  3577 |
| A100-80GB    |    30 |   941 |   500 |   493 |  96 |  95 |  85 | 100 |   – |
| A40          |    49 |   500 |   400 |   180 |  96 |  82 |  51 |  88 |  7154 |
| H100         |   209 |  2013 |  1821 |  1653 | 160 | 150 | 128 | 100 | 28616 |
| H200         |   782 |  1005 |  1005 |   784 | 192 | 181 | 167 | 100 | 28612 |
| L40          |  1566 |   501 |   309 |    85 |  96 |  56 |   0 |  51 | 11547 |
| L40S         |   924 |   752 |   616 |    35 | 192 | 164 |   0 |  82 | 28612 |
| RTX PRO 6000 |   166 |   752 |   721 |   656 | 188 | 188 | 128 |  99 | 28606 |

**What this means for the 4 × 80 GB job:** on the ≥ 75 GB machines, memory and CPUs never ran out before the GPUs did. Whenever 4 GPUs were free, at least 400 GB of host memory, 85+ CPUs (except RTX PRO 6000-4, which has 48 in total) and terabytes of disk were free with them. A request of 150–200 GB and 16 CPUs is not what limits this job. Host resources only get tight on L40/L40S machines, and only on backfill.

## 4. How long 4 free GPUs stayed free, and the gaps between

A "window" is a run of consecutive snapshots with the condition true (a break of more than 20 min in the data ends it). "Wait from a random time" is the time from a random snapshot to the next snapshot where the condition is true. It ignores other jobs competing for the same GPUs, so real waits are longer. Apr–Oct 2026, conservative:

| group        | free   | windows | window h p25/p50/p75/p90 | gap h p25/p50/p75/p90 | longest gap d | wait from random time h p50/p75/p90 | P(wait > 24 h) % |
|:-------------|:-------|------:|:----------------|:-----------------|-----:|:----------------|---:|
| Any ≥75 GB   | lab≥4  | 476 | 0.1/0.3/1.0/3.2 | 0.1/0.7/3.9/16.3 | 13.3 | 13.8/57.2/128.3 | 41 |
| Any ≥75 GB   | idle≥4 | 363 | 0.1/0.3/0.9/2.6 | 0.2/0.7/5.8/25.6 | 16.4 | 24.5/88.5/214.7 | 50 |
| Any ≥75 GB   | bf≥4   |1023 | 0.1/0.1/0.3/1.0 | 0.1/0.3/2.2/11.3 |  7.0 | 5.8/17.4/43.0   | 19 |
| Any ≥75 GB   | lab≥2  | 835 | 0.1/0.2/0.7/3.9 | 0.2/0.7/2.8/8.1  |  6.7 | 1.2/8.9/34.7    | 14 |
| H200         | lab≥4  | 302 | 0.1/0.3/1.1/4.1 | 0.1/0.8/5.3/19.5 | 21.1 | 40.9/127.5/383.8 | 57 |
| H200         | lab≥2  | 455 | 0.1/0.3/1.0/3.4 | 0.3/1.2/4.3/13.4 | 17.5 | 9.2/62.8/175.6  | 37 |
| H100         | lab≥4  | 186 | 0.2/0.6/1.7/4.5 | 0.4/1.5/10.7/69.8| 21.3 | 72.2/181.8/287.8 | 68 |
| A100-80GB    | lab≥4  | 119 | 0.2/0.3/0.5/1.3 | 0.2/5.2/30.4/83.5| 19.1 | 77.5/230.8/377.1 | 73 |
| A100-80GB    | lab≥2  | 696 | 0.1/0.2/0.6/2.3 | 0.1/0.4/3.0/11.8 | 14.7 | 9.2/33.3/92.4   | 32 |
| Any 40–75 GB | lab≥4  | 314 | 0.1/0.3/1.2/11.9| 0.1/0.5/5.5/25.5 |  8.5 | 21.0/72.4/132.9 | 48 |
| Any 40–75 GB | bf≥4   | 907 | 0.1/0.1/0.3/1.3 | 0.2/0.5/2.8/7.6  |  4.9 | 0.9/6.8/20.5    |  8 |
| L40S         | lab≥4  | 166 | 0.3/0.9/3.1/7.1 | 0.3/2.2/7.7/61.4 | 20.7 | 76.9/181.7/292.3 | 69 |
| L40S         | bf≥4   | 747 | 0.1/0.1/0.3/1.0 | 0.2/0.8/5.1/14.2 |  5.4 | 5.8/17.9/37.0   | 18 |

Over Aug 2025 – Oct 2026 the same "any ≥ 75 GB, lab ≥ 4" wait is p50 0.2 h, p75 21 h, p90 73 h. That longer period benefits from the overstated A100 months.

**What this means for the 4 × 80 GB job:** free 4-GPU windows are short (median 20 min). Some job takes the GPUs soon after they free up, so a 4-GPU job has to already be in the queue when they do. Even ignoring competition, a job submitted at a random time since April would have waited a median of about 14 h for 4 GPU Lab GPUs. In 41 % of cases it would have waited more than a day, and in 10 % more than 5 days. For 2 GPUs the median was about 1 h, and 14 % waited more than a day. Tie a 4-GPU job to one card type (only H200, only A100-80GB) and the median wait becomes 2–3 days.

## 5. Backfill

How often 4 backfill GPUs were free is in Q2 (any ≥ 75 GB: 16 % of snapshots Apr–Oct 2026, 35 % over the whole period; 40–75 GB: 40 %).

**Backfill claims on qualifying machines, Apr–Oct 2026.** A claim is one job on a set of GPUs from its first to its last snapshot. "Ended by a primary claim" means that in the next snapshot the primary slot had claimed one of the job's GPUs, or the slot showed Preempting: a likely owner preemption. "Ran again later" means the same `GlobalJobId` appeared again afterwards, so the job didn't finish there (evicted, or held and released). A claim with neither probably finished or was removed. The two can't be told apart with certainty: a primary job can also land on a GPU right after a backfill job ended on its own.

| tier     | GPUs per claim | claims | h p25/p50/p75/p90 | % ended by primary claim | % owner/drain | % ran again later | % censored | primary-claim ends per 100 claim-h |
|:---------|:---|-------:|:----------------|---:|---:|---:|---:|------:|
| ≥75 GB   | 1   | 185,430 | 0.1/0.2/0.7/1.4 |  7 | 0 | 22 | 0 |  7.8 |
| ≥75 GB   | 2–3 |     617 | 0.2/0.5/4.0/7.8 | 20 | 0 | 25 | 4 |  4.9 |
| ≥75 GB   | ≥4  |     136 | 0.1/0.3/1.5/3.1 | 38 | 0 | 29 | 1 | 29.1 |
| 40–75 GB | 1   | 414,409 | 0.1/0.1/0.3/1.9 |  6 | 0 | 26 | 0 |  5.5 |
| 40–75 GB | 2–3 |     469 | 0.2/0.3/0.5/3.0 | 74 | 0 | 65 | 1 | 76.4 |
| 40–75 GB | ≥4  |      92 | 0.1/0.3/2.3/6.0 | 29 | 0 | 38 | 0 | 13.4 |

Few multi-GPU jobs run on backfill, and those that do run briefly. So the observed claims say little about how long a long job would survive there. A more direct estimate: **start a hypothetical 4-GPU backfill job** at every hourly snapshot where a machine had ≥ 4 backfill GPUs free, on 4 of those GPUs chosen at random. Then measure the time until any of the 4 is claimed by the primary slot, or the machine goes Owner/Drained (= eviction).

| group (Apr–Oct 26) | starts | h to eviction p10/p25/p50/p75 | survive ≥1 h % | ≥2 h % | ≥4 h % | ≥8 h % | ≥24 h % | ≥72 h % |
|:-------------|-----:|:--------------------|---:|---:|---:|---:|---:|---:|
| All ≥ 75 GB  | 1549 | 0.7/3.5/13.8/97.8   | 87 | 81 | 72 | 61 | 43 | 32 |
| H200         |  873 | 0.6/2.2/10.3/59.8   | 83 | 75 | 67 | 55 | 32 | 22 |
| H100         |  442 | 2.2/7.4/41.1/139.5  | 94 | 90 | 84 | 73 | 57 | 40 |
| A100-80GB    |   66 | 0.5/1.0/2.9/5.9     | 74 | 61 | 38 | 18 | 12 | 12 |
| RTX PRO 6000 |  166 | 2.3/23.6/91.1/332.8 | 94 | 91 | 84 | 81 | 75 | 70 |
| All 40–75 GB | 3367 | 1.3/7.2/46.2/269.4  | 91 | 88 | 82 | 73 | 56 | 44 |
| L40S         |  923 | 0.5/2.5/10.5/62.5   | 84 | 77 | 68 | 56 | 35 | 20 |
| L40          | 2238 | 2.4/10.4/112.4/374.0| 93 | 91 | 87 | 79 | 64 | 55 |

Over Aug 2025 – Oct 2026, all ≥ 75 GB: p25 4.4 h, p50 26.5 h, 76 % survive 4 h, 51 % survive 24 h.

**What this means for the 4 × 80 GB job:** backfill offers 4 free ≥ 75 GB GPUs about as often as GPU Lab does (16 % vs 18 % of snapshots), and the backfill waits are shorter. The cost is eviction. On ≥ 75 GB machines, about 1 start in 8 is evicted within an hour, 1 in 4 within 4 hours, and the median run lasts about 14 hours before a primary job takes one of the 4 GPUs. H200 backfill is the most contested, at a median of 10 h. A long fine-tune on backfill will be evicted several times. It only works with frequent checkpoints and automatic resubmission, so backfill is better as an optional fast lane than the default.

## 6. Multi-GPU claims (competition)

Primary-slot claims on qualifying machines, Apr–Oct 2026. This includes prioritized slots, which compete for the same machines. Hours run from the first to the last snapshot.

| type         | GPUs | claims | h p25/p50/p75/p90 | max d | GPU-h | share of type's primary GPU-h in ≥2-GPU / ≥4-GPU claims |
|:-------------|:----|------:|:-----------------|----:|------:|:----|
| H200         | 2–3 | 1,579 | 0.3/1.1/3.5/7.8  |  3.9 | 11,208 | 17 % / 8 % |
| H200         | ≥4  |   896 | 0.1/0.3/0.9/3.6  | 12.4 |  9,966 | |
| H100         | 2–3 |   639 | 0.3/1.0/4.4/11.4 | 10.4 |  7,066 | 22 % / 9 % |
| H100         | ≥4  |   478 | 0.1/0.5/2.1/6.4  |  2.8 |  4,873 | |
| A100-80GB    | 2–3 | 1,231 | 0.1/0.3/2.8/11.3 |  7.8 | 10,243 | 10 % / 3 % |
| A100-80GB    | ≥4  |   140 | 0.1/0.2/4.3/26.4 |  9.2 |  4,255 | |
| RTX PRO 6000 | 2–3 |   181 | 0.2/0.4/1.7/8.9  |  2.2 |  1,117 | 64 % / 57 % |
| RTX PRO 6000 | ≥4  |   163 | 0.3/4.3/16.5/38.8|  4.4 |  8,827 | |
| H200 NVL     | 2–3 |    27 | 0.2/1.5/31.6/71.9 |  3.0 |    954 | 28 % / 15 % |
| H200 NVL     | ≥4  |    31 | 0.1/0.6/3.8/31.0 |  3.0 |  1,085 | |
| L40S         | 2–3 |   345 | 0.2/0.6/5.5/18.2 | 14.3 |  5,069 | 41 % / 38 % |
| L40S         | ≥4  |   797 | 0.3/0.4/12.0/23.1| 13.5 | 54,047 | |
| L40          | ≥4  |   243 | 0.2/5.4/20.0/32.7|  3.1 | 19,241 | 9 % / 8 % |

Over Aug 2025 – Oct 2026, ≥ 4-GPU claims ran p50/p90: A100-80GB 3.0/24.6 h, H100 0.6/16.1 h, H200 0.2/2.1 h, L40S 2.7/25.6 h. Of ≥ 2-GPU primary claims on ≥ 75 GB machines, 0.1–0.3 % ended with the machine going Owner/Drained.

**What this means for the 4 × 80 GB job:** most of the GPU time on ≥ 75 GB machines goes to single-GPU jobs. On H200, H100 and A100-80GB, ≥ 2-GPU claims hold only 10–22 % of GPU-hours, so the competition is mainly many short single-GPU jobs filling GPUs as they free up. Most ≥ 4-GPU claims are short (median under 1 h, which includes failed starts). A tail of multi-day ones also exists: p90 of 1–4 days on A100-80GB, L40S and RTX PRO 6000. The rare RTX PRO 6000 GPU Lab machine is already mostly used by ≥ 4-GPU jobs. On a GPU Lab slot, a running multi-GPU job is almost never evicted. What ends it is the job-length limit (12/24/72/168 h, `environment.md` §3).

## 7. Compatibility

| question | answer | source |
|---|---|---|
| CUDA driver versions; any below 12.8? | The snapshots have no driver attribute. The compat-matrix jobs (Sep 22 – Oct 23 2026) saw 550.54.14 (CUDA 12.4) on some RTX 2080 Ti machines (**below 12.8**), 570.195.03 (12.8) on A100-40/80GB, H100, H200, L40, L40S, RTX 8000, P100 and other 2080 Ti machines, and 590.48.01 (13.1) on some H200 and L40S machines and on the RTX PRO 6000. GB10's configuration lists 580.159.03 (13.0); no job ran there. Every ≥ 75 GB type seen is ≥ 12.8. H200 NVL and A40 weren't tested. Driver changes over the period can't be seen | `ml-gpu-compat-matrix/outputs/jobs.csv` |
| Any on 13.x? | Yes: 590.48.01 (CUDA 13.1) on part of the H200 and L40S fleet and on RTX PRO 6000; 580 (13.0) on GB10 | same |
| Blackwell (CC 12.0) | **4 machines × 8 RTX PRO 6000 Blackwell Server Edition = 32 GPUs** (2 since Jun 30 2026, 2 since Sept 24/30 2026). 1 is GPU Lab, 1 is mixed, 2 are prioritized. The 2 GB10 machines are CC 12.1, single GPU | snapshots + `slots.csv` |
| MIG | 1 machine: the 4 A100-80GB GPUs of A100-80GB-9 have been split into **8 MIG 3g.40gb instances** since Mar 30 2026. They appear as `GPUs_DeviceName = "NVIDIA A100-SXM4-80GB MIG 3g.40gb"`, `GPUs_GlobalMemoryMb = 40100`, with IDs `MIG-<36-char UUID>` (not `GPU-xxxxxxxx`), on a non-prioritized primary slot and on backfill. They have a device name here. Separately, 50 ordinary GPU IDs on 15 machines sometimes appear with **no** device name or memory (113k rows) | snapshots |
| NVLink / interconnect | No attribute anywhere in the data. Inference from model names only, unverified: A100-SXM4 and H100 HBM3 (SXM) and H200 normally have NVLink; RTX PRO 6000, L40/L40S and A40 are PCIe. Measured: NCCL direct P2P hangs on 2 of 4 RTX PRO 6000 machines unless `NCCL_P2P_LEVEL=NVL` is set | `environment.md` §6 |
| `HasCHTCStaging` | Not in the data. The probes found it true on CHTC GPU Lab and backfill slots | `environment.md` §1 |

**What this means for the 4 × 80 GB job:** a driver requirement of ≥ 12.8 costs nothing on ≥ 75 GB machines, since they're all ≥ 12.8. Use a CUDA 12.8 build of PyTorch: a cu13 build would see no GPU on the 570 machines. A 79 GB GPU memory floor admits RTX PRO 6000 (Blackwell), which needs a cu12.8+ PyTorch build and `NCCL_P2P_LEVEL=NVL`. Without those, cap capability at 9.0. The MIG instances (40 GB) are excluded by the memory floor anyway. The data says nothing about NVLink. `probes/gpu_comm/` is still the way to measure it.

## 8. Best and worst times to submit

From Q2 (Apr–Oct 2026, any ≥ 75 GB, lab ≥ 4):

- **Best:** overnight and early morning, 20:00–08:00 Central, 19–21 % of snapshots. Tuesday (23 %) and Monday/Friday (20–21 %).
- **Worst:** 11:00–17:00 (14–17 %, lowest at 16:00). Thursday (13 %) and Sunday (15 %).
- **H200 alone:** best 01:00–05:00 (15 %), worst noon (9 %).

The months differ far more: Apr, May and Aug 2026 were 3–8 %, Jun, Jul and Sep 2026 were 28–34 %.

**What this means for the 4 × 80 GB job:** submission time matters little. A queued job waits for the next window whenever it opens, and the hour-to-hour difference is only about 15 % vs 21 %. If there's a choice, submit in the evening so the job is waiting when the overnight windows open, and expect weeks of waiting in busy months. Don't plan around a particular weekday.

## Where the data can't answer

- **Matchability:** "Unclaimed" ≠ matchable. `START` expressions, job-length rules, the multi-GPU hold timer and user priority are not in the snapshots. Q2 and Q4 are upper bounds on availability and lower bounds on waits. The waits also ignore competing jobs.
- **Host memory and CPUs:** come from one Oct 2026 snapshot of totals plus ap2001/ap2002 job requests. Jobs from other APs and CPU-only jobs are invisible.
- **Drivers:** known per GPU type for Sep–Oct 2026 only, with no per-machine history. `CUDADriverVersion`, `HasCHTCStaging` and NVLink aren't recorded at all. Running `probes/gpu_machines.sh` (which records them) for a day would fill this gap going forward.
- **Backfill end reason:** inferred, not recorded. A preemption and a job that finished just before a primary job arrived look the same.

## For recipe 3's defaults (my reading)

| decision | suggestion from this data |
|---|---|
| GPU memory | `gpus_minimum_memory = 79000M` (with the unit) over a list of models. Pair it with `gpus_maximum_capability = 9.0` unless the image is cu12.8+ and sets `NCCL_P2P_LEVEL=NVL` for Blackwell. Requiring a single model makes the 4-GPU wait 2–3× longer. Make L40S (48 GB) opt-in |
| `request_memory` | 160–200 GB is safe: every ≥ 75 GB machine had ≥ 400 GB free whenever 4 GPUs were free. Memory isn't the constraint; size it to the measured peak (P15) |
| 4 vs 2 GPUs | 4 GPUs is realistic but slow: median ~14 h wait from a random time, 41 % > 1 day, 10 % > 5 days. 2 GPUs starts about 10× sooner (median ~1 h, p90 ~35 h) but needs ~70 GB per GPU (tight on 80 GB cards, roomy on H200). Default to 4 if the README sets expectations of hours to days; offer 2 × ≥ 80 GB as the "start today" option |
| Backfill | Not as the default. Offer it as an opt-in second route (it has 4 free GPUs about as often as GPU Lab). Expect an eviction within 4 h for about 1 start in 4 and a median of ~14 h before eviction (H200 ~10 h) |
| Timed checkpoint interval | GPU Lab: evictions are rare, and the job-length limit is known in advance. Checkpoint every ~60 min, plus a save before the job-length limit. Backfill: ~20–30 min. Young's rule with an assumed ~3 min save and a 3.5–14 h typical time to eviction gives 35–70 min, and the heavy early evictions (p10 = 0.7 h) push it lower. Check against the measured P15 save time |

---

Method and scripts: `results/gpu-pool-history/analysis/` (DuckDB, run on the snapshots in `gpu-pool-study/gpu_parquets/`). The private machine-label key (labels → host names) was kept outside the repository.
