exec(open('q2.py').read().split('out=[]')[0])
def runs(s):
    s=s.sort_index(); t=s.index.to_series()
    brk=(t.diff()>pd.Timedelta('20min'))|(s!=s.shift())
    g=brk.cumsum(); r=pd.DataFrame({'v':s,'t':t,'g':g}).groupby('g').agg(v=('v','first'),t0=('t','first'),t1=('t','last'),n=('t','size'))
    r['h']=((r.t1-r.t0)+pd.Timedelta('5min')).dt.total_seconds()/3600; return r
def wait(s):
    s=s.sort_index(); t=pd.Series(s.index,index=s.index)
    nxt=t.where(s).bfill(); return ((nxt-t).dt.total_seconds()/3600)
q=[.25,.5,.75,.9]
rows=[]
for g in ['Any ≥75 GB','H200','H100','A100-80GB','RTX PRO 6000','Any 40–75 GB','L40S','L40','Any ≥40 GB']:
  for col,k in [('lab',4),('idle',4),('bf',4),('lab',2)]:
    for per in ['Aug 25–Oct 26','Apr–Oct 26']:
        x=local(ind(groups[g],k)); x=x[x.index>=(RECENT if per.startswith('Apr') else pd.Timestamp('2025-08-01',tz='America/Chicago'))]
        s=x[col]; r=runs(s); up=r[r.v].h; dn=r[~r.v].h; w=wait(s).dropna()
        if len(up)==0: rows.append({'group':g,'free':f'{col}≥{k}','period':per,'windows':0}); continue
        rows.append({'group':g,'free':f'{col}≥{k}','period':per,'windows':len(up),
          'window h p25/p50/p75/p90':'/'.join(f'{v:.1f}' for v in up.quantile(q)),
          'gap h p25/p50/p75/p90':'/'.join(f'{v:.1f}' for v in dn.quantile(q)) if len(dn) else '',
          'longest gap d':round(dn.max()/24,1) if len(dn) else 0,
          'wait from random time h p50/p75/p90':'/'.join(f'{v:.1f}' for v in w.quantile([.5,.75,.9])),
          'P(wait>24h) %':round(100*(w>24).mean(),0)})
o=pd.DataFrame(rows); o.to_csv(H+'/q4.csv',index=False); print(o.to_markdown(index=False))
