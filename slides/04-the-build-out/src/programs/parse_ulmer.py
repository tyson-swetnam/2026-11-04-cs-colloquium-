import sys, re, json
L=open(sys.argv[1]).read().split('\n')
def num(s):
    s=s.replace('—','-').replace(':','.').rstrip('.')
    # OCR: '1,413,2' -> 1413.2 ; '115,6' -> 115.6
    if re.fullmatch(r'-?\d{1,3},\d{3},\d',s): s=s[:-2].replace(',','')+'.'+s[-1]
    elif re.fullmatch(r'-?\d+,\d',s): s=s.replace(',','.')
    s=s.replace(',','')
    return float(s)
def find(title):
    return [i for i,l in enumerate(L) if title in l]
# Table C-10 railroad gross capital expenditures incl/excl land, 1870-1950
s=find('Derivation of Gross Capital Expenditures, Excluding Land,')[0]
e=find('Derivation of Index of Cost of Road and Equipment of Steam Railroads, l840')[0]
c10={}
for l in L[s:e]:
    t=l.split()
    if t and re.fullmatch(r'(18[7-9]\d|19[0-5]\d)',t[0]):
        rest=' '.join(t[1:]).replace('.02 10','.0210').replace('.032 1','.0321').replace('.02 15','.0215').split()
        if len(rest)!=3: print('C10 skip',t); continue
        inc,ratio,exc=num(rest[0]),num(rest[1]),num(rest[2])
        y=int(t[0])
        if abs(inc*(1-ratio)-exc)>1.01: print('C10 check fail',y,inc,ratio,exc)
        c10[y]=dict(incl_land=inc,land_ratio=ratio,excl_land=exc)
# Table C-1 col3 cross-check
s=find('Steam Railroads, Annual Data, 1870')[0]
c1={}
for l in L[s:s+120]:
    t=l.split()
    if t and re.fullmatch(r'(18[7-9]\d|19[0-5]\d)',t[0]) and len(t)>=9:
        c1[int(t[0])]=num(t[3])
mism=[(y,c1[y],c10[y]['excl_land']) for y in c1 if y in c10 and c1[y]!=c10[y]['excl_land']]
print('C1 vs C10 col3 mismatches:',mism, 'n c1',len(c1),'n c10',len(c10))
# Table D-1 electric light & power
s=find('Electric Light and Power, Annual Data, 188')[0]
d1={}
for l in L[s:s+120]:
    t=l.replace('194!','1941').replace('1943.','1943').split()
    if t and re.fullmatch(r'(188\d|189\d|19[0-5]\d)',t[0]) and len(t)>=9:
        y=int(t[0]); g=num(t[3])
        try:
            cc=0.0 if t[5]=='a' else num(t[5]); net=num(t[7])
            if abs(cc+net-g)>0.15: print('D1 identity check fail',y,g,cc,net)
        except Exception as ex: print('D1 check err',y,t,ex)
        d1[y]=g
print('D1 n',len(d1),min(d1),max(d1))
json.dump({'c10':c10,'d1':d1},open(sys.argv[2],'w'),indent=1)
