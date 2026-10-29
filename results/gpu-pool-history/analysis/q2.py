import pandas as pd, numpy as np, os
H=os.environ['HOME']+'/gph'
d=pd.read_parquet(H+'/ts_type.parquet'); snaps=pd.read_parquet(H+'/snaps.parquet').ts.sort_values().values
A=['H200','H200 NVL','RTX PRO 6000','A100-80GB','H100']; B=['L40S','L40','A40','A100-40GB']
groups={t:[t] for t in A+B}; groups['Any ≥75 GB']=A; groups['Any 40–75 GB']=B; groups['Any ≥40 GB']=A+B
def ind(types, k, pre='c_'):
    x=d[d.typ.isin(types)].groupby('ts')[[pre+'open_idle',pre+'open_free',pre+'bf_free']].max()
    if len(types)>1: x=x.reindex(snaps, fill_value=0)
    x.columns=['idle','lab','bf']
    return (x>=k)
def local(x):
    x=x.copy(); x.index=pd.to_datetime(x.index).tz_localize('UTC').tz_convert('America/Chicago'); return x
RECENT=pd.Timestamp('2026-04-01',tz='America/Chicago')
out=[]
for g,ty in groups.items():
    for pre,lab in [('c_','conservative'),('','raw')]:
        r={'group':g,'version':lab}
        for k in (4,2):
            x=local(ind(ty,k,pre))
            for per,xx in [('all',x),('Apr–Oct 26',x[x.index>=RECENT])]:
                for col in ['idle','lab','bf']: r[f'{col}≥{k} {per}']=round(100*xx[col].mean(),1)
        r['snapshots']=len(x); out.append(r)
o=pd.DataFrame(out); o.to_csv(H+'/q2_overall.csv',index=False)
print(o[o.version=='conservative'].drop(columns='version').to_markdown(index=False))
print(o[o.version=='raw'][['group','lab≥4 all','lab≥4 Apr–Oct 26','idle≥4 all','idle≥4 Apr–Oct 26','bf≥4 all']].to_markdown(index=False))
