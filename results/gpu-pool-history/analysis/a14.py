import duckdb,os,pandas as pd
H=os.environ['HOME']+'/gph'; C=os.environ['HOME']+'/mnt/Claude'
c=duckdb.connect(); c.execute(f"set memory_limit='1500MB'; set threads=2; set temp_directory='{H}/tmp'; set preserve_insertion_order=false")
sl=pd.read_csv(C+'/aerie/data/slots.csv'); g=sl[sl.TotalSlotGPUs>0].copy()
g['kind']=g.Slot.str.extract(r'^([a-z]+)')[0]
tot=g[g.kind.isin(['slot','backfill'])].groupby(['Machine','kind']).agg(cpus=('TotalSlotCpus','sum'),mem=('TotalSlotMemory','sum')).unstack()
tot.columns=[f'{a}_{b}' for a,b in tot.columns]; tot=tot.reset_index().rename(columns={'Machine':'m'}); c.register('tot',tot)
inv=pd.read_csv(H+'/inventory_private.csv')[['m','type']]; c.register('inv',inv)
# moments: hourly machine-snapshots with >=4 lab-free (all-open machines) or >=4 bf-free
c.execute(f"""create table mo as select m, ts, typ, open_free, bf_free, n_gpu, n_open, p_free_disk, b_free_disk, excl from '{H}/mm.parquet'
  where ts>=timestamp '2025-09-01' and minute(ts)<5 and (open_free>=4 or bf_free>=4)""")
c.execute(f"""create table jj as select distinct ts, m, p_job job, 'p' k from '{H}/g.parquet' where p_job is not null and minute(ts)<5 and ts>=timestamp '2025-09-01'
  union all select distinct ts, m, b_job, 'b' from '{H}/g.parquet' where b_job is not null and minute(ts)<5 and ts>=timestamp '2025-09-01'""")
c.execute(f"""create table usage as select ts, m, k, count(*) njobs, sum((j.job is null)::int) unk,
   sum(coalesce(mp, rm)) mem_mb, sum(coalesce(cp, rc)) cpus, sum(coalesce(dp, rd)) disk_kb
   from jj left join '{H}/jobs.parquet' j using(job) group by all""")
c.execute(f"""copy (select mo.*, tot.cpus_slot, tot.mem_slot, tot.cpus_backfill, tot.mem_backfill,
   coalesce(p.mem_mb,0) p_mem, coalesce(p.cpus,0) p_cpus, coalesce(p.unk,0) p_unknown, coalesce(p.njobs,0) p_jobs,
   coalesce(b.mem_mb,0) b_mem, coalesce(b.cpus,0) b_cpus, coalesce(b.unk,0) b_unknown
   from mo join tot using(m) left join usage p on p.ts=mo.ts and p.m=mo.m and p.k='p' left join usage b on b.ts=mo.ts and b.m=mo.m and b.k='b') to '{H}/q3.parquet' (format parquet)""")
print(c.sql(f"select count(*), avg((p_unknown>0)::int), avg((b_unknown>0)::int) from '{H}/q3.parquet'").fetchone())
