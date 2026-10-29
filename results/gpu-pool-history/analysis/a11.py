import duckdb,os,pandas as pd
H=os.environ['HOME']+'/gph'
c=duckdb.connect(); c.execute(f"set memory_limit='1500MB'; set threads=2; set temp_directory='{H}/tmp'")
inv=pd.read_csv(H+'/inventory_private.csv')[['m','label','type','pri_now']]; c.register('inv',inv)
for K in ['b','p']:
  c.execute(f"""create table c{K} as select job, m, t0, max(t1) t1, count(*) n_gpu, bool_or(saw_preempting) saw_pre,
    bool_or(np>=4) next_primary, bool_or(np in (2,3) or nb in (2,3)) next_owner_drain,
    bool_or(nts is null or nts-t1>interval 20 minute) censored
    from '{H}/seg_{K}.parquet' group by job,m,t0""")
  c.execute(f"""create table d{K} as select a.*, epoch(t1-t0)/3600.0+5/60.0 hrs, i.type, i.label,
     exists(select 1 from c{K} b where b.job=a.job and b.t0>a.t1) seen_later,
     exists(select 1 from cp b where b.job=a.job and b.t0>a.t1) seen_later_primary
     from c{K} a join inv i using(m)""") if K=='p' else None
c.execute("""create table db as select a.*, epoch(t1-t0)/3600.0+5/60.0 hrs, i.type, i.label,
     exists(select 1 from cb b where b.job=a.job and b.t0>a.t1) or exists(select 1 from cp b where b.job=a.job and b.t0>a.t1) seen_later
     from cb a join inv i using(m)""")
c.execute("""create table dp2 as select a.*, epoch(t1-t0)/3600.0+5/60.0 hrs, i.type, i.label,
     exists(select 1 from cb b where b.job=a.job and b.t0>a.t1) or exists(select 1 from cp b where b.job=a.job and b.t0>a.t1) seen_later
     from cp a join inv i using(m)""")
c.execute(f"copy db to '{H}/claims_bf.parquet' (format parquet)"); c.execute(f"copy dp2 to '{H}/claims_prim.parquet' (format parquet)")
print(c.sql("select count(*), avg(censored::int), avg(next_primary::int), avg(saw_pre::int), avg(seen_later::int) from db").df())
print(c.sql("select count(*), avg(censored::int), avg(next_primary::int), avg(seen_later::int) from dp2").df())
