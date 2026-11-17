import sys
S="<<<<<<<<FFFFFFFF>>@BB@>>==>AA>==<<<@@<<<=;:<<:;==>>88>>=<<<<<<<<2466664248<==<846=>??>=66<?@@?<66=?@@?=66<>??><648<<<<84246666428::::::8:<<<<<<::<=>>=<::==>>==::<>>>><::>>>>>>::=<<<<=:8::::::8<<<==<<<;<<<<<<;;<<<<<<;;<<<<<<;;<<<<<<;;<<<<<<;=>>>>>>=<<<<<<<<8::;;::8:<<<<<<::<====<:;<====<;<<====<;:=====<::<=<<<<:8::;;::8@B><<>B@@@<<<<@@:888888:86644668644224466442244664422446644224462468864268:<<:866:@BB@:66:BDDB:66:BDDB:66:@BB@:666<<<<6626666662"
def pv(p,s):return(ord(S[(p-1)*64+(7-(s>>4))*8+(s&7)])-60)*5
def ag(s):return S[384+(7-(s>>4))*8+(s&7)]
V=[0,100,320,330,500,900,0]
N=[31,33,14,18,-31,-33,-14,-18]
G=[1,15,16,17,-1,-15,-16,-17]
B=[15,17,-15,-17]
R=[1,16,-1,-16]
Q=B+R
M=99999
BU=25000
T=[[0]*128 for _ in range(7)]
E=[0]*128
for s in range(128):
 if s&0x88:continue
 for p in range(1,7):T[p][s]=V[p]+pv(p,s)
 E[s]=(ord(S[384+(7-(s>>4))*8+(s&7)])-60)*5
b=[0]*128
sc=0
ca=0
ep=-1
sd=1
qn=0
hc=0
hs=[0]
K=[-1,-1]
U=[]
Z=[]
for i in range(128):
 for j in range(15):
  Z.append(((i*16777619+j*2166136261+2654435761)**3)%4294967296)
CS=[0]*16
for i in range(16):
 CS[i]=((i*2654435761+97531)**3)%4294967296
def hsh():
 return hs[0]^(1 if sd>0 else 2)^CS[ca]^((ep+999)*7919 if ep>=0 else 0)
def at(s,y):
 if s<0 or s>127:return 0
 if y>0:
  if not (s-15)&0x88 and b[s-15]==1:return 1
  if not (s-17)&0x88 and b[s-17]==1:return 1
 else:
  if not (s+15)&0x88 and b[s+15]==-1:return 1
  if not (s+17)&0x88 and b[s+17]==-1:return 1
 for d in N:
  t=s+d
  if not t&0x88 and b[t]==2*y:return 1
 for d in G:
  t=s+d
  if not t&0x88 and b[t]==6*y:return 1
 for d in B:
  t=s+d
  while not t&0x88:
   x=b[t]
   if x:
    if x==3*y or x==5*y:return 1
    break
   t+=d
 for d in R:
  t=s+d
  while not t&0x88:
   x=b[t]
   if x:
    if x==4*y or x==5*y:return 1
    break
   t+=d
 return 0
def lf(fen):
 global sc,ca,ep,sd,qn,hc
 p=fen.split()
 for i in range(128):b[i]=0
 hs[0]=0
 sc=0
 qn=0
 for i,y in enumerate(p[0].split("/")):
  r=7-i;f=0
  for c in y:
   if c.isdigit():f+=int(c)
   else:
    x="PNBRQK".find(c.upper())+1
    v=x if c.isupper() else -x
    b[r*16+f]=v
    hs[0]^=Z[(r*16+f)*15+v+7]
    if x==5:qn+=1
    if x==6:K[0]=r*16+f
    if v==-6:K[1]=r*16+f
    f+=1
 sd=1 if p[1]=="w" else -1
 ca=0
 if p[2]!="-":
  if "K"in p[2]:ca|=1
  if "Q"in p[2]:ca|=2
  if "k"in p[2]:ca|=4
  if "q"in p[2]:ca|=8
 ep=-1
 if len(p)>3 and p[3]!="-":ep=(int(p[3][1])-1)*16+ord(p[3][0])-97
 hc=int(p[4]) if len(p)>4 else 0
 for s in range(128):
  x=b[s]
  if x:sc+=T[x][s] if x>0 else -T[-x][s^0x70]
def st(s,x):
 o=b[s]
 if o:hs[0]^=Z[s*15+o+7]
 if x:hs[0]^=Z[s*15+x+7]
 b[s]=x
def mk(m):
 global sc,ca,ep,sd,qn,hc
 f,t,p,k=m
 x=b[f];cp=b[t]
 U.append((x,cp,ca,ep,f,t,sc,hs[0],qn,hc))
 if cp:
  st(t,0)
  sc+=T[-cp][t^0x70] if cp<0 else -T[cp][t]
  if cp==5 or cp==-5:qn-=1
 elif (x==1 or x==-1)and t==ep:
  c=t-16 if x>0 else t+16
  st(c,0)
  sc+=T[1][c^0x70] if x>0 else -T[1][c]
 sc-=T[x][f] if x>0 else -T[-x][f^0x70]
 st(f,0)
 nx=p*(1 if x>0 else -1) if p else x
 st(t,nx)
 sc+=T[nx][t] if nx>0 else -T[-nx][t^0x70]
 if p and p!=0 and (nx==5 or nx==-5) and not cp:qn+=1
 if (x==6 or x==-6)and(t-f==2 or f-t==2):
  if t>f:rf=t+1;rt=t-1
  else:rf=t-2;rt=t+1
  r=b[rf];st(rf,0);st(rt,r)
  sc+=T[4][rt]-T[4][rf] if r>0 else -(T[4][rt^0x70]-T[4][rf^0x70])
 if x==6 or x==-6:
  ca&=~(3 if x>0 else 12)
  K[0 if x>0 else 1]=t
 if f==7 or t==7:ca&=~1
 if f==0 or t==0:ca&=~2
 if f==119 or t==119:ca&=~4
 if f==112 or t==112:ca&=~8
 ep=(f+t)>>1 if (x==1 or x==-1)and(t-f==32 or f-t==32) else -1
 hc=0 if (cp or x==1 or x==-1) else hc+1
 sd=-sd
def um():
 global sc,ca,ep,sd,qn,hc
 x,cp,ca,ep,f,t,s0,h0,q0,c0=U.pop()
 sd=-sd
 hs[0]=h0
 sc=s0
 qn=q0
 hc=c0
 b[f]=x
 b[t]=cp
 if (x==1 or x==-1)and t==ep and not cp:b[t-16 if x>0 else t+16]=0
 if (x==6 or x==-6)and(t-f==2 or f-t==2):
  if t>f:b[t+1]=b[t-1];b[t-1]=0
  else:b[t-2]=b[t+1];b[t+1]=0
 if x==6 or x==-6:K[0 if x>0 else 1]=f
def gn(q):
 m=[]
 for s in range(128):
  if s&0x88:continue
  x=b[s]
  if x*q<=0:continue
  p=x if x>0 else -x
  if p==1:
   d=16*q;t=s+d
   if not t&0x88 and b[t]==0:
    if (t>>4)==(7 if q>0 else 0):
     for z in(5,4,3,2):m.append((s,t,z,0))
    else:
     m.append((s,t,0,0))
     if (s>>4)==(1 if q>0 else 6) and not (t+d)&0x88 and b[t+d]==0:m.append((s,t+d,0,0))
   for dd in(d-1,d+1):
    t=s+dd
    if t&0x88:continue
    y=b[t]
    if y*q<0:
     if (t>>4)==(7 if q>0 else 0):
      for z in(5,4,3,2):m.append((s,t,z,0))
     else:m.append((s,t,0,0))
    elif t==ep and y==0:m.append((s,t,0,1))
  elif p==2:
   for d in N:
    t=s+d
    if not t&0x88 and b[t]*q<=0:m.append((s,t,0,0))
  elif p==6:
   for d in G:
    t=s+d
    if not t&0x88 and b[t]*q<=0:m.append((s,t,0,0))
   if q>0:
    if ca&1 and b[4]==6 and b[7]==4 and b[5]==0 and b[6]==0 and not at(4,-1) and not at(5,-1) and not at(6,-1):m.append((4,6,0,2))
    if ca&2 and b[4]==6 and b[0]==4 and b[3]==0 and b[2]==0 and b[1]==0 and not at(4,-1) and not at(3,-1) and not at(2,-1):m.append((4,2,0,2))
   else:
    if ca&4 and b[116]==-6 and b[119]==-4 and b[117]==0 and b[118]==0 and not at(116,1) and not at(117,1) and not at(118,1):m.append((116,118,0,2))
    if ca&8 and b[116]==-6 and b[112]==-4 and b[115]==0 and b[114]==0 and b[113]==0 and not at(116,1) and not at(115,1) and not at(114,1):m.append((116,114,0,2))
  else:
   for d in(B if p==3 else R if p==4 else Q):
    t=s+d
    while not t&0x88:
     y=b[t]
     if y==0:m.append((s,t,0,0))
     elif y*q<0:
      m.append((s,t,0,0));break
     else:break
     t+=d
 return m
def sn(s):return chr(97+(s&7))+str((s>>4)+1)
def ui(m):
 f,t,p,_=m
 s=sn(f)+sn(t)
 if p:s+={5:"q",4:"r",3:"b",2:"n"}[p]
 return s
def pu(u):return((int(u[1])-1)*16+ord(u[0])-97,(int(u[3])-1)*16+ord(u[2])-97,0 if len(u)<5 else{"q":5,"r":4,"b":3,"n":2}[u[4]],0)
TT={}
KL=[set() for _ in range(72)]
ns=[0]
HP=[]
class O(Exception):pass
def od(ms,ply,h):
 kl=KL[ply] if ply<72 else set()
 p=TT.get(h)
 def k(m):
  f,t,q,_=m
  if p is not None and (m[0],m[1],m[2])==p:return 1<<30
  y=b[t]
  if y:return 100000+V[y if y>0 else -y]*10-V[b[f] if b[f]>0 else -b[f]]//10+(90000 if q else 0)
  if q:return 80000
  if (f,t,q) in kl:return 70000
  return 0
 ms.sort(key=k,reverse=True)
def qs(a,be,ply):
 ns[0]+=1
 if ns[0]>BU:raise O
 me=sd
 ck=at(K[0 if me>0 else 1],-me)
 if not ck:
  v=sc if sd>0 else -sc
  if v>=be:return be
  if v>a:a=v
 ms=gn(me)
 od(ms,ply,0)
 lg=0
 for m in ms:
  f,t,p,_=m
  if not ck and not p and b[t]==0 and t!=ep:continue
  mk(m)
  try:
   if at(K[0 if me>0 else 1],-me):continue
   lg+=1
   v=-qs(-be,-a,ply+1)
  finally:
   um()
  if v>=be:return be
  if v>a:a=v
 if ck and not lg:return -M+ply
 return a
def se(d,a,be,ply):
 ns[0]+=1
 if ns[0]>BU:raise O
 if hc>=100:return 0
 h=hsh()
 if h in HP:return 0
 if d<=0:return qs(a,be,ply)
 e=TT.get(h)
 if e is not None and e[1]>=d:
  if e[2]==0:return e[0]
  if e[2]==1:
   if e[0]>=be:return e[0]
  elif e[0]<=a:return e[0]
 me=sd
 ck=at(K[0 if me>0 else 1],-me)
 ms=gn(me)
 if not ms:return -M+ply if ck else 0
 od(ms,ply,h)
 bv=-M-1
 lg=0
 a0=a
 HP.append(h)
 try:
  for m in ms:
   q=bool(m[2]) or b[m[1]]!=0 or m[1]==ep
   mk(m)
   try:
    if at(K[0 if me>0 else 1],-me):continue
    lg+=1
    v=-se(d-1,-be,-a,ply+1)
   finally:
    um()
   if v>bv:
    bv=v
    if v>a:
     a=v
     if a>=be:
      if not q and ply<72:KL[ply].add((m[0],m[1],m[2]))
      TT[h]=(bv,d,1,m[0],m[1],m[2])
      return bv
 finally:
  HP.pop()
 if not lg:return -M+ply if ck else 0
 TT[h]=(bv,d,0 if bv>a0 else 2,m[0],m[1],m[2])
 if len(TT)>200000:TT.clear()
 return bv
def bm(root):
 ns[0]=0
 TT.clear()
 HP.clear()
 for s in KL:s.clear()
 rs=[pu(u) for u in root]
 bst=rs[0]
 d=1
 try:
  while d<30:
   a=-M
   cb=None
   cv=-M-1
   od(rs,0,hsh())
   for m in rs:
    mk(m)
    try:
     v=-se(d-1,-M,-a,1)
    finally:
     um()
    if v>cv:cv=v;cb=m
    if v>a:a=v
   if cb is not None:bst=cb
   d+=1
 except O:pass
 return ui(bst)
def main():
 import os,json
 import urllib.request as u
 import urllib.error as er
 UU=os.environ["MAKEFUN_ENV_URL"]
 def po(p,o):
  r=u.Request(UU+p,data=json.dumps(o).encode(),headers={"content-type":"application/json"})
  try:
   with u.urlopen(r) as x:return json.load(x)
  except er.HTTPError as ex:sys.exit("%s HTTP %d"%(p,ex.code))
 sys.setrecursionlimit(9000)
 while True:
  g=po("/game",{})
  if g["status"]=="done":break
  while g["status"]=="your_move":
   lf(g["fen"])
   mv=bm(g["legal_moves"])
   print(g["game"],mv,file=sys.stderr)
   g=po("/move",{"game":g["game"],"move":mv})
  print(g["game"],g["outcome"],g["reason"],file=sys.stderr)
if __name__=="__main__":main()
