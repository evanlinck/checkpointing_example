import duckdb,os,pandas as pd
H=os.environ['HOME']+'/gph'
exec(open('a3.py').read().split('c.execute(f"""copy')[0].replace("import duckdb,os,pandas as pd\n",""))
inv=pd.read_csv(H+'/inventory_private.csv')[['m','label']]; c.register('inv',inv)
c.execute("""create table runs as with x as (select m,ts, (idle_free=n_gpu) whole_idle, ts - lag(ts) over (partition by m order by ts) dt from s where typ is not null),
 y as (select *, sum(case when (not whole_idle) or dt>interval 20 minute then 1 else 0 end) over (partition by m order by ts) grp from x)
 select m,grp,min(ts) t0,max(ts) t1 from y where whole_idle group by all having max(ts)-min(ts)>=interval 3 day""")
c.execute("create table mm as select s.*, label, exists(select 1 from runs r where r.m=s.m and s.ts between r.t0 and r.t1) excl from s join inv using(m) where typ is not null")
c.execute(f"copy mm to '{H}/mm.parquet' (format parquet)")
c.execute(f"""copy (select ts, typ, max(open_idle) open_idle, max(open_free) open_free, max(bf_free) bf_free,
  max(case when not excl then open_idle else 0 end) c_open_idle, max(case when not excl then open_free else 0 end) c_open_free, max(case when not excl then bf_free else 0 end) c_bf_free
  from mm group by all) to '{H}/ts_type.parquet' (format parquet)""")
print(c.sql("select avg(excl::int) from mm").fetchone())
