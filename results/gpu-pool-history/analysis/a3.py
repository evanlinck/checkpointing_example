import duckdb,os,pandas as pd
H=os.environ['HOME']+'/gph'
c=duckdb.connect(); c.execute(f"set memory_limit='1GB'; set threads=2; set temp_directory='{H}/tmp'")
TYPE="""case dev when 'NVIDIA H200' then 'H200' when 'NVIDIA H200 NVL' then 'H200 NVL' when 'NVIDIA RTX PRO 6000 Blackwell Server Edition' then 'RTX PRO 6000'
 when 'NVIDIA A100-SXM4-80GB' then 'A100-80GB' when 'NVIDIA H100 80GB HBM3' then 'H100' when 'NVIDIA L40S' then 'L40S' when 'NVIDIA L40' then 'L40'
 when 'NVIDIA A40' then 'A40' when 'NVIDIA A100-SXM4-40GB' then 'A100-40GB' end"""
c.execute(f"create view s as select *, {TYPE} typ from read_parquet('{H}/mts/*.parquet') where n_gpu>=2")
c.execute(f"""copy (select ts, typ, count(*) machines,
  max(open_idle) open_idle, max(open_free) open_free, max(bf_free) bf_free, max(pri_free) pri_free,
  sum(open_idle) sum_open_idle, sum(n_open) sum_open, sum(n_gpu) sum_gpu
  from s where typ is not null group by all) to '{H}/ts_type.parquet' (format parquet)""")
# all snapshots list
c.execute(f"copy (select distinct ts from read_parquet('{H}/mts/*.parquet')) to '{H}/snaps.parquet' (format parquet)")
print(c.sql(f"select typ, count(*) from '{H}/ts_type.parquet' group by 1").df())
