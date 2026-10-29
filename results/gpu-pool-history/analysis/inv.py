import duckdb,os,pandas as pd
H=os.environ['HOME']; C=H+'/mnt/Claude'
c=duckdb.connect(); c.execute(f"set memory_limit='1GB'; set threads=2; set temp_directory='{H}/gph/tmp'")
c.execute(f"create view s as select * from read_parquet('{H}/gph/mts/*.parquet')")
short={'NVIDIA H200':'H200','NVIDIA H200 NVL':'H200 NVL','NVIDIA RTX PRO 6000 Blackwell Server Edition':'RTX PRO 6000','NVIDIA A100-SXM4-80GB':'A100-80GB','NVIDIA H100 80GB HBM3':'H100','NVIDIA L40S':'L40S','NVIDIA L40':'L40','NVIDIA A40':'A40','NVIDIA A100-SXM4-40GB':'A100-40GB','NVIDIA GB10':'GB10','Quadro RTX 8000':'RTX 8000','NVIDIA A100-SXM4-80GB MIG 3g.40gb':'A100-80GB MIG 3g.40gb'}
inv=c.sql(f"""select m, mode(dev) dev, max(mem) mem, approx_quantile(n_gpu,0.95)::int n_gpu,
  max(n_gpu) filter (where ts>=timestamp '2026-09-19') n_gpu_now,
  min(ts) t0, max(ts) t1, avg(pri::int) pri_share, avg(pri::int) filter (where ts>=timestamp '2026-09-19') pri_now,
  max(p_free_disk)/1048576.0 disk_gb_max, max(b_free_disk)/1048576.0 bf_disk_gb_max, count(*) snaps
  from s group by m""").df()
inv['type']=inv.dev.map(short).fillna(inv.dev)
sl=pd.read_csv(C+'/aerie/data/slots.csv')
g=sl[sl.TotalSlotGPUs>0]
prim=g[~g.Slot.str.startswith(('backfill','interactive','build','profiler'))].groupby('Machine').agg(cpus=('TotalSlotCpus','sum'),mem_gb=('TotalSlotMemory',lambda x: x.sum()/1024),cc=('GPUs_Capability','max'),prio=('PrioritizedProjects',lambda x: x.notna().any()))
bf=g[g.Slot.str.startswith('backfill')].groupby('Machine').agg(bf_cpus=('TotalSlotCpus','max'),bf_mem_gb=('TotalSlotMemory',lambda x: x.max()/1024),bf_gpus=('TotalSlotGPUs','max'))
inv=inv.merge(prim,left_on='m',right_index=True,how='left').merge(bf,left_on='m',right_index=True,how='left')
roles=pd.read_csv(C+'/gpu-machines/gpu_hosts.tsv',sep='\t',comment='#',names=['host','gpu_id','gpu_type','role','slot','projects'])
r=roles.groupby('host').role.agg(lambda x: '/'.join(sorted(set(x))))
inv['host_short']=inv.m.str.split('.').str[0]
inv=inv.merge(r.rename('role'),left_on='host_short',right_index=True,how='left')
inv=inv.sort_values(['mem','type','t0','m'],ascending=[False,True,True,True])
inv['label']=inv.groupby('type').cumcount()+1
inv['label']=inv.type+'-'+inv.label.astype(str)
inv.to_csv(H+'/gph/inventory_private.csv',index=False)
cols=['label','mem','n_gpu','n_gpu_now','t0','t1','pri_share','pri_now','role','cpus','mem_gb','bf_cpus','bf_mem_gb','bf_gpus','cc','disk_gb_max','bf_disk_gb_max']
inv['t0']=inv.t0.dt.date; inv['t1']=inv.t1.dt.date
print(inv[inv.mem>=40000][cols].round(2).to_string(index=False))
