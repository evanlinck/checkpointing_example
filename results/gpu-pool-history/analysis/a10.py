import duckdb,os
H=os.environ['HOME']+'/gph'
c=duckdb.connect(); c.execute(f"set memory_limit='1500MB'; set threads=2; set temp_directory='{H}/tmp'; set preserve_insertion_order=false")
for K in ['b','p']:
  c.execute(f"""copy (with x as (select m,gpu,ts,{K}_job job, {K}_rank rk, p_rank, b_rank,
     lag(ts) over w pts, lag({K}_job) over w pjob, lead(ts) over w nts, lead(p_rank) over w np, lead(b_rank) over w nb, lead({K}_job) over w njob
     from read_parquet('{H}/g.parquet') window w as (partition by m,gpu order by ts)),
   y as (select *, sum(case when pjob is distinct from job or ts-pts>interval 20 minute then 1 else 0 end) over (partition by m,gpu order by ts) seg from x)
   select m,gpu,job,seg,min(ts) t0,max(ts) t1, bool_or(rk=4) saw_preempting,
     arg_max(nts,ts) nts, arg_max(np,ts) np, arg_max(nb,ts) nb, arg_max(njob,ts) njob
   from y where job is not null group by m,gpu,job,seg) to '{H}/seg_{K}.parquet' (format parquet)""")
  print(K, c.sql(f"select count(*) from '{H}/seg_{K}.parquet'").fetchone())
