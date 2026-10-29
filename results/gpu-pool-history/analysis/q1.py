import duckdb,os,pandas as pd
H=os.environ['HOME']+'/gph'
c=duckdb.connect()
inv=pd.read_csv(H+'/inventory_private.csv')
acc=c.sql(f"select label, avg(n_open::double/n_gpu) ofn from '{H}/mm.parquet' where ts>=timestamp '2026-09-19' group by 1").df()
acc_all=c.sql(f"select label, avg(n_open::double/n_gpu) ofa from '{H}/mm.parquet' group by 1").df()
inv=inv.merge(acc,on='label',how='left').merge(acc_all,on='label',how='left')
drv={'H200':'570 (12.8) / 590 (13.1)','H200 NVL':'not tested','RTX PRO 6000':'590 (13.1)','A100-80GB':'570 (12.8)','H100':'570 (12.8)','L40S':'570 (12.8) / 590 (13.1)','L40':'570 (12.8)','A40':'not tested','A100-40GB':'570 (12.8)'}
q=inv[(inv['mem']>=40000)&(inv.n_gpu>=2)&inv.type.isin(drv.keys())].copy()
def access(f):
    if pd.isna(f): return 'removed'
    return 'GPU Lab' if f>0.95 else ('prioritized' if f<0.05 else f'mixed ({f*100:.0f}% Lab)')
q['Access now']=q['ofn'].map(access)
q['GPU Lab share of period %']=(100*q.ofa).round(0).astype(int)
q['label']=q.label.str.replace(r'\.0$','',regex=True)
q['GPU mem GB']=(q['mem']/1024).round(0).astype(int)
q['GPUs']=q.n_gpu_now.fillna(q.n_gpu).astype(int)
q['Host mem GB']=q.mem_gb.round(0).astype('Int64'); q['CPUs']=q.cpus.astype('Int64')
q['Max free disk TB']=(q.disk_gb_max/1024).round(1)
q['Driver (CUDA), by type']=q.type.map(drv); q['CC']=q.cc
q['Seen']=q.t0.str[:7]+' → '+q.t1.str[:7].where(q.t1<'2026-10-15','now')
q['num']=q.label.str.extract(r'-(\d+)$')[0].astype(int)
q=q.sort_values(['GPU mem GB','type','num'],ascending=[False,True,True])
cols=['label','GPU mem GB','GPUs','Host mem GB','CPUs','Max free disk TB','Driver (CUDA), by type','CC','Access now','GPU Lab share of period %','Seen']
print(q[cols].to_markdown(index=False))
q[cols].to_csv(H+'/q1_table.csv',index=False)
now=q[q['Access now']!='removed']
print(now.groupby('type').agg(machines=('label','size'),gpus=('GPUs','sum'),m4=('GPUs',lambda s:(s>=4).sum()),
  lab_m=('Access now',lambda s:(s=='GPU Lab').sum()), lab4=('Access now',lambda s:((s=='GPU Lab')&(now.loc[s.index,'GPUs']>=4)).sum()), pri_m=('Access now',lambda s:(s=='prioritized').sum())).to_markdown())
