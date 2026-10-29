exec(open('q2.py').read().split('out=[]')[0])
sel=['Any ≥75 GB','H200','H100','A100-80GB','RTX PRO 6000','Any 40–75 GB','L40S','L40']
X={g:local(pd.concat([ind(groups[g],4).add_suffix('4'),ind(groups[g],2).add_suffix('2')],axis=1)) for g in sel}
def T(key, col, gs, rec=False):
    return pd.DataFrame({g:(100*(X[g][X[g].index>=RECENT] if rec else X[g])[col].groupby(key((X[g][X[g].index>=RECENT] if rec else X[g]).index)).mean()).round(0) for g in gs})
mon=lambda i:i.strftime('%Y-%m')
m=T(mon,'lab4',sel); m.columns=[c+' lab≥4' for c in m.columns]
m2=pd.DataFrame({'Any ≥75 GB idle≥4':T(mon,'idle4',['Any ≥75 GB']).iloc[:,0],'Any ≥75 GB bf≥4':T(mon,'bf4',['Any ≥75 GB']).iloc[:,0],'Any ≥75 GB lab≥2':T(mon,'lab2',['Any ≥75 GB']).iloc[:,0],'Any 40–75 GB bf≥4':T(mon,'bf4',['Any 40–75 GB']).iloc[:,0]})
M=pd.concat([m,m2],axis=1); M.index.name='month (local)'
print(M.astype('Int64').to_markdown()); M.to_csv(H+'/q2_month.csv')
dn=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
for nm,key in [('dow',lambda i:i.dayofweek),('hour',lambda i:i.hour)]:
    gs=['Any ≥75 GB','H200','H100','Any 40–75 GB']
    a=T(key,'lab4',gs,True).add_suffix(' lab≥4'); b=T(key,'idle4',['Any ≥75 GB'],True).add_suffix(' idle≥4'); bb=T(key,'bf4',['Any ≥75 GB'],True).add_suffix(' bf≥4'); cc=T(key,'lab2',['Any ≥75 GB'],True).add_suffix(' lab≥2')
    D=pd.concat([a,b,bb,cc],axis=1)
    if nm=='dow': D.index=dn
    D.to_csv(f'{H}/q2_{nm}.csv'); print(D.astype('Int64').T.to_markdown() if nm=='hour' else D.astype('Int64').to_markdown())
