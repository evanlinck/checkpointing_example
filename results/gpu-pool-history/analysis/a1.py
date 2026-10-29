import duckdb,os
c=duckdb.connect(); c.execute("set memory_limit='2GB'; set threads=4; set preserve_insertion_order=false"); c.execute("set temp_directory='/sessions/rcw-01fkvatdbbzat5a6ufnfnpnu/gph/tmp'")
import sys
M=sys.argv[1]
c.execute(f"create view r0 as select * from read_parquet('gpu_parquets/gpu_state_{M}.parquet', union_by_name=true)")
cols=[x[0] for x in c.sql('describe r0').fetchall()]
c.execute('create view r as select *, '+('Disk' if 'Disk' in cols else 'NULL::bigint')+' DiskX from r0')
c.execute("""copy (
 with x as (select timestamp ts, Machine m, trim(g) gpu, regexp_extract(Name,'^([a-z]+)',1) k, State st,
   GPUs_DeviceName dev, GPUs_GlobalMemoryMb mem, coalesce(PrioritizedProjects,'')<>'' pri, DiskX Disk, GlobalJobId job
   from r, unnest(string_split(AssignedGPUs, ',')) u(g) where trim(g)<>'')
 select ts, m, gpu, any_value(dev) dev, max(mem) mem, bool_or(pri) pri,
  max(case when k='slot' then case st when 'Claimed' then 5 when 'Preempting' then 4 when 'Drained' then 3 when 'Owner' then 2 else 1 end end)::tinyint p_rank,
  max(case when k='backfill' then case st when 'Claimed' then 5 when 'Preempting' then 4 when 'Drained' then 3 when 'Owner' then 2 else 1 end end)::tinyint b_rank,
  max(case when k='interactive' then case st when 'Claimed' then 5 when 'Preempting' then 4 when 'Drained' then 3 when 'Owner' then 2 else 1 end end)::tinyint i_rank,
  max(case when k='slot' and st in ('Claimed','Preempting') then job end) p_job,
  max(case when k='backfill' and st in ('Claimed','Preempting') then job end) b_job,
  max(case when k='slot' and st='Unclaimed' then Disk end) p_free_disk,
  max(case when k='backfill' and st='Unclaimed' then Disk end) b_free_disk
 from x group by all) to 'HOME/gph/ts/gpu_ts_MM.parquet' (format parquet, compression zstd)""".replace('HOME', os.environ['HOME']).replace('MM',M))
print('ok')
