import duckdb,os,pandas as pd,glob
H=os.environ['HOME']+'/gph'
c=duckdb.connect(); c.execute(f"set memory_limit='1500MB'; set threads=2; set temp_directory='{H}/tmp'; set preserve_insertion_order=false")
inv=pd.read_csv(H+'/inventory_private.csv'); q=inv[(inv['mem']>=40000)&(inv.n_gpu>=2)][['m','label','type']]; c.register('q',q)
files=[f for f in sorted(glob.glob(H+'/ts/*.parquet')) if f[-15:-8]>='2025-08']
c.execute(f"""create table g as select ts, m, coalesce(nullif(lower(regexp_extract(gpu,'^GPU[-_]([0-9a-fA-F]{{8}})',1)),''), gpu) gpu,
   max(p_rank) p_rank, max(b_rank) b_rank, max(p_job) p_job, max(b_job) b_job
   from read_parquet({files}) where m in (select m from q) group by all""")
print(c.sql("select count(*) from g").fetchone())
c.execute(f"copy g to '{H}/g.parquet' (format parquet)")
