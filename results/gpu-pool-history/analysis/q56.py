import duckdb,os,pandas as pd
H=os.environ['HOME']+'/gph'
c=duckdb.connect(); c.execute(f"set memory_limit='1500MB'; set threads=2; set temp_directory='{H}/tmp'")
A="('H200','H200 NVL','RTX PRO 6000','A100-80GB','H100')"
TIER=f"case when type in {A} then '≥75 GB' else '40–75 GB' end"
NB="case when n_gpu=1 then '1' when n_gpu<4 then '2–3' else '≥4' end"
for per,cond in [('Apr–Oct 26',"t0>=timestamp '2026-04-01 05:00'"),('Aug 25–Oct 26','true')]:
  print('## backfill',per)
  print(c.sql(f"""select {TIER} tier, {NB} gpus, count(*) claims,
    round(quantile_cont(hrs,0.25),1)||'/'||round(median(hrs),1)||'/'||round(quantile_cont(hrs,0.75),1)||'/'||round(quantile_cont(hrs,0.9),1) "h p25/p50/p75/p90",
    round(100*avg((next_primary or saw_pre)::int)) "% ended by primary claim",
    round(100*avg((not (next_primary or saw_pre) and next_owner_drain)::int)) "% owner/drain",
    round(100*avg(seen_later::int)) "% job ran again later",
    round(100*avg(censored::int)) "% censored",
    round(100*sum(((next_primary or saw_pre) and not censored)::int)/sum(hrs),2) "primary-ends per 100 claim-h"
    from '{H}/claims_bf.parquet' where {cond} group by all order by 1 desc,2""").df().to_markdown(index=False))
  print(c.sql(f"""select type, count(*) claims, round(median(hrs),1) p50h, round(quantile_cont(hrs,0.9),1) p90h,
    round(100*avg((next_primary or saw_pre)::int)) pct_primary_end, round(100*sum(((next_primary or saw_pre) and not censored)::int)/sum(hrs),2) per100h
    from '{H}/claims_bf.parquet' where {cond} and n_gpu>=2 group by all order by 1""").df().to_markdown(index=False))
  print('## primary multi-GPU',per)
  print(c.sql(f"""select {TIER} tier, type, {NB} gpus, count(*) claims,
    round(quantile_cont(hrs,0.25),1)||'/'||round(median(hrs),1)||'/'||round(quantile_cont(hrs,0.75),1)||'/'||round(quantile_cont(hrs,0.9),1) "h p25/p50/p75/p90",
    round(max(hrs)/24,1) max_d, round(sum(hrs*n_gpu)) gpu_h
    from '{H}/claims_prim.parquet' where {cond} group by all order by 1 desc,2,3""").df().to_markdown(index=False))
