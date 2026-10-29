import duckdb,os
H=os.environ['HOME']+'/gph'; D=os.environ['HOME']+'/mnt/Claude/gpu-pool-study/data'
c=duckdb.connect(); c.execute(f"set memory_limit='1500MB'; set threads=2; set temp_directory='{H}/tmp'; set preserve_insertion_order=false")
c.execute(f"""copy (select GlobalJobId job, any_value(RequestCpus) rc, any_value(RequestMemory) rm, any_value(RequestDisk) rd,
  any_value(CpusProvisioned) cp, any_value(MemoryProvisioned) mp, any_value(DiskProvisioned) dp, any_value(RequestGpus) rg
  from read_parquet(['{D}/chtc_gpu_2025-09_2026-10.parquet','{D}/chtc_gpu_180d.parquet'], union_by_name=true) group by 1) to '{H}/jobs.parquet' (format parquet)""")
print(c.sql(f"select count(*) from '{H}/jobs.parquet'").fetchone())
print(c.sql(f"""select split_part(job,'#',1) ap, count(*) claims, avg((j.job is not null)::int) found from '{H}/claims_prim.parquet' p left join '{H}/jobs.parquet' j using(job)
  where t0>='2025-09-01' group by 1 order by 2 desc limit 8""").df())
