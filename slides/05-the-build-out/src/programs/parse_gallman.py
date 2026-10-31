import sys, re, json
lines=open(sys.argv[1]).read().split('\n')
# locate tables
i1=[i for i,l in enumerate(lines) if l.lstrip('\x0c').startswith('TABLE 1: Gallman')][0]
i2=[i for i,l in enumerate(lines) if l.lstrip('\x0c').startswith('TABLE 2: Gallman')][0]
i3=[i for i,l in enumerate(lines) if l.lstrip('\x0c').startswith('TABLE 3: Gallman')][0]
t1={}
for l in lines[i1:i2]:
    tok=l.split()
    if tok and re.fullmatch(r'18[3-5]\d',tok[0]) and len(tok)==15:
        y=int(tok[0]); t1[y]=dict(rr=float(tok[8]),canal=float(tok[9]),gnp=float(tok[14]))
t2={}; corr={}
section='orig'
for l in lines[i2:i3]:
    if l.strip().startswith('As Corrected'): section='corr'; continue
    tok=l.split()
    if not tok or not re.fullmatch(r'(18[6-9]\d|190\d)',tok[0]): continue
    y=int(tok[0])
    if section=='corr':
        corr[y]=dict(rr=float(tok[1]),gnp=float(tok[4])); continue
    n=len(tok)
    d=dict(rr_orig=float(tok[8]),gnp=float(tok[13]))
    if n==17: d['rr_rev']=float(tok[16])
    elif n==15: d['rr_rev']=float(tok[14])
    elif n==14: pass
    else: raise SystemExit(f'bad row {y} n={n}')
    # check construction total = rr + other
    assert abs(float(tok[8])+float(tok[9])-float(tok[10]))<0.6, (y,tok)
    t2[y]=d
for y,c in corr.items():
    t2[y]['rr_orig_uncorrected']=t2[y]['rr_orig']; t2[y]['gnp_uncorrected']=t2[y]['gnp']
    t2[y]['rr_orig']=c['rr']; t2[y]['gnp']=c['gnp']
# checks for table1: total construction = rr+canal+other
json.dump({'t1':t1,'t2':t2},open(sys.argv[2],'w'),indent=1)
print(len(t1),len(t2),sorted(t1)[0],sorted(t1)[-1],sorted(t2)[0],sorted(t2)[-1])
import statistics
sh=[t2[y]['rr_rev']/t2[y]['gnp']*100 for y in range(1870,1891)]
print('mean rev share 1870-1890 %.2f'%statistics.mean(sh))
for y in (1870,1871,1880,1881,1882,1886): print(y, round(t2[y]['rr_rev']/t2[y]['gnp']*100,2), round(t2[y]['rr_orig']/t2[y]['gnp']*100,2))
sho=[t2[y]['rr_orig']/t2[y]['gnp']*100 for y in range(1870,1891)]
print('mean orig share 1870-1890 %.2f'%statistics.mean(sho))
