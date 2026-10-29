import duckdb,os
H=os.environ['HOME']+'/gph'
c=duckdb.connect()
c.execute(f"""create view v as select *, (mem_slot-p_mem)/1024.0 lab_mem, cpus_slot-p_cpus lab_cpu, p_free_disk/1048576.0 lab_disk,
  (mem_backfill-b_mem)/1024.0 bf_mem_acct, (mem_backfill-b_mem-p_mem)/1024.0 bf_mem_phys, cpus_backfill-b_cpus bf_cpu_acct, cpus_backfill-b_cpus-p_cpus bf_cpu_phys, b_free_disk/1048576.0 bf_disk
  from '{H}/q3.parquet' where not excl""")
A="('H200','H200 NVL','RTX PRO 6000','A100-80GB','H100')"
for per,cond in [('Apr–Oct 26',"ts>=timestamp '2026-04-01 05:00'"),('Sep 25–Oct 26','true')]:
  print('### GPU Lab moments', per)
  print(c.sql(f"""select typ, count(*) moments, round(median(lab_mem)) "free mem GB p50", round(quantile_cont(lab_mem,0.1)) "p10", round(min(lab_mem)) "min",
   round(median(lab_cpu)) "free CPUs p50", round(quantile_cont(lab_cpu,0.1)) "p10 ", 
   round(100*avg((lab_mem>=200)::int)) "≥200 GB %", round(100*avg((lab_cpu>=16)::int)) "≥16 CPU %",
   round(100*avg((lab_mem>=200 and lab_cpu>=16)::int)) "both %", count(lab_disk) "disk obs", round(median(lab_disk)) "free disk GB p50", round(100*avg((lab_disk>=50)::int)) "disk≥50 %"
   from v where {cond} and open_free>=4 and n_open=n_gpu group by 1 order by 1""").df().to_markdown(index=False))
  print('### Backfill moments', per)
  print(c.sql(f"""select typ, count(*) moments, round(median(bf_mem_acct)) "free mem GB p50 (slot)", round(median(bf_mem_phys)) "p50 after primary jobs", round(quantile_cont(bf_mem_phys,0.1)) "p10 after primary",
   round(median(bf_cpu_acct)) "free CPUs p50 (slot)", round(median(bf_cpu_phys)) "after primary", round(quantile_cont(bf_cpu_phys,0.1)) "p10 after primary",
   round(100*avg((bf_mem_phys>=200 and bf_cpu_phys>=16)::int)) "both ok after primary %", round(median(bf_disk)) "free disk GB p50"
   from v where {cond} and bf_free>=4 group by 1 order by 1""").df().to_markdown(index=False))
