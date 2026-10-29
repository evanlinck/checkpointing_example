import duckdb,os,glob
H=os.environ['HOME']+'/gph'
c=duckdb.connect(); c.execute(f"set memory_limit='1GB'; set threads=2; set temp_directory='{H}/tmp'; set preserve_insertion_order=false")
for f in sorted(glob.glob(H+'/ts/*.parquet')):
  o=H+'/mts/'+os.path.basename(f)
  if os.path.exists(o): continue
  c.execute(f"""copy (select ts, m, mode(dev) dev, max(mem) mem, count(distinct gpu)::int n_gpu, bool_or(pri) pri,
 sum((p_rank=1)::int)::int lab_free,
 sum((p_rank is not null and not pri)::int)::int n_open,
 sum((p_rank=1 and not pri)::int)::int open_free,
 sum((p_rank=1 and not pri and coalesce(b_rank,1)=1)::int)::int open_idle,
 sum((p_rank=1 and pri)::int)::int pri_free,
 sum((p_rank=1 and coalesce(b_rank,1)=1)::int)::int idle_free,
 sum((b_rank=1 and coalesce(p_rank,1)=1)::int)::int bf_free,
 sum((p_rank=1 and b_rank>=4)::int)::int bf_on_free_primary,
 sum((p_rank>=4)::int)::int prim_claimed,
 sum((p_rank in (2,3) or (p_rank is null and b_rank in (2,3)))::int)::int owner_drained,
 max(p_free_disk) p_free_disk, max(b_free_disk) b_free_disk,
 count(distinct p_job)::int n_prim_jobs, count(distinct b_job)::int n_bf_jobs
 from (select ts, m, coalesce(nullif(lower(regexp_extract(gpu,'^GPU[-_]([0-9a-fA-F]{{8}})',1)),''), gpu) gpu, any_value(dev) dev, max(mem) mem, bool_or(pri) pri,
   max(p_rank) p_rank, max(b_rank) b_rank, max(p_job) p_job, max(b_job) b_job, max(p_free_disk) p_free_disk, max(b_free_disk) b_free_disk
   from read_parquet('{f}') where mem>=40000 or dev is null group by all) group by ts, m) to '{o}' (format parquet)""")
  print(o)
