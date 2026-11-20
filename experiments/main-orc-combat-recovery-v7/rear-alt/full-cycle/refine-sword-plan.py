import json,math
from pathlib import Path
E=Path('experiments/main-orc-combat-recovery-v7/rear-alt/full-cycle');p=json.loads((E/'plan.json').read_text());c=p['clips']['Sword'];f=c['frames']
# Explicit joint choreography supersedes the first geometric blocking pass.
# Keep the two selected keys. Add an outward opening pose to avoid an elbow flip.
f.insert(3,dict(f[3],phase='anticipation-open',sourceFrame=2,base='characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword/layers/body/02.png',preserveKey=None))
points=[([102,57],[94,81]),([108,48],[99,72]),([109,37],[110,58]),([106,39],[119,50]),([108,51],[118,35]),([111,44],[108,24]),([111,37],[100,19]),([109,44],[116,32]),([108,43],[120,56]),([104,56],[109,81]),([100,62],[100,87]),([102,57],[96,82]),([104,56],[94,79]),([102,57],[94,81]),([102,57],[94,81])]
angles=[None,None,20,10,0,-15,-10,25,70,115,128,118,100,None,None]
times=[40,55,35,45,55,45,70,40,40,55,90,65,80,60,85]
for i,(a,(e,palm),ang,ms)in enumerate(zip(f,points,angles,times)):
 a.update(index=i,elbow=e,palm=palm,weaponAngleDeg=ang,weaponVisible=ang is not None,durationMs=ms)
 a['donor']='raised'if 3<=i<=7 else'sword-low'
 a['preserveKey']='apex'if i==6 else'impact'if i==9 else None
 if a['preserveKey']=='apex':a['shoulder']=[88,39]
 if a['preserveKey']=='impact':a['shoulder']=[83,48]
 c['visibleInterval']=[2,12]
c['durationMs']=sum(times)
# Axis-aligned donor measurement projected onto the manually placed elbow/palm.
def wrist(d,e,palm):
 a,b=d['elbow'],d['palm'];l=math.dist(a,b);u=[(b[j]-a[j])/l for j in range(2)];n=[-u[1],u[0]];tl=math.dist(e,palm);tu=[(palm[j]-e[j])/tl for j in range(2)];tn=[-tu[1],tu[0]];w=d['wrist'];along=sum((w[j]-a[j])*u[j]for j in range(2))*tl/l;perp=sum((w[j]-a[j])*n[j]for j in range(2));return[round(e[j]+along*tu[j]+perp*tn[j])for j in range(2)]
for k,clip in p['clips'].items():
 for a in clip['frames']:
  if k!='Sword':continue
  a['wrist']=wrist(p['donors'][a['donor']],a['elbow'],a['palm']);a['humerusPx']=round(math.dist(a['shoulder'],a['elbow']),3);a['forearmPx']=round(math.dist(a['elbow'],a['wrist']),3);a['targetElbowPalmPx']=round(math.dist(a['elbow'],a['palm']),3)
(E/'plan.json').write_text(json.dumps(p,indent=2));print('Sword manual plan',c['durationMs'],len(f))
author=E/'author.lua';s=author.read_text(encoding='utf-8-sig');s=s.replace('local contact=blank(128*7,128*2)','local contact=blank(128*5,128*math.ceil(#cfg.frames/5))').replace('((fi-1)%7)*128,math.floor((fi-1)/7)*128','((fi-1)%5)*128,math.floor((fi-1)/5)*128').replace('contact:resize(1792,512)','contact:resize(1280,256*math.ceil(#cfg.frames/5))');s=s.replace('if fi==1 or fi==2 or fi==6 or fi==7 or fi==8 or fi==9 or fi==12 or fi==14 then','if true then');author.write_text(s,encoding='utf-8')
