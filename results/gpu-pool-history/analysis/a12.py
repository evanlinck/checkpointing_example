import duckdb,os,pandas as pd
H=os.environ['HOME']+'/gph'
c=duckdb.connect(); c.execute(f"set memory_limit='1500MB'; set threads=2; set temp_directory='{H}/tmp'; set preserve_insertion_order=false")
c.execute(f"""copy (with x as (select m,gpu,ts,p_rank,b_rank,
   min(case when p_rank>=2 then ts end) over (partition by m,gpu order by ts rows between 1 following and unbounded following) next_p
   from read_parquet('{H}/g.parquet'))
  select * from x where minute(ts)<5 and b_rank=1 and p_rank=1) to '{H}/bfstart.parquet' (format parquet)""")
inv=pd.read_csv(H+'/inventory_private.csv')[['m','type']]; c.register('inv',inv)
c.execute(f"""create table st as select m,ts, list(next_p order by hash(gpu))[1:4] np4, count(*) nfree from '{H}/bfstart.parquet' group by m,ts having count(*)>=4""")
c.execute(f"""copy (select st.m, ts, type, nfree, epoch(coalesce(list_min(np4), timestamp '2099-01-01')-ts)/3600.0 surv_h, list_min(np4) is null cens
  from st join inv using(m)) to '{H}/bfsurv.parquet' (format parquet)""")
print(c.sql(f"select count(*), avg(cens::int) from '{H}/bfsurv.parquet'").fetchone())
