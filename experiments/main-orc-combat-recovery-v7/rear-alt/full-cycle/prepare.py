from pathlib import Path
import json,math,hashlib
E=Path('experiments/main-orc-combat-recovery-v7/rear-alt/full-cycle');C=Path('characters/orc-v1/source/combat-recovery-v7/rear-alt')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
snap={}
for root in ['characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword','characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-axe','characters/orc-v1/source/combat-rescue-v5/combat/weapons',str(C/'apex'),str(C/'impact'),'characters/orc-v1/source/combat-recovery-v7/rear-r','experiments/main-orc-combat-recovery-v7/rear-r']:
 for p in Path(root).rglob('*'):
  if p.is_file():snap[p.as_posix()]=sha(p)
(E/'protected-input-hashes.json').write_text(json.dumps(snap,indent=2))
# Explicit per-pose planning; no automated temporal raster interpolation.
phasesS=['rest','body-preparation','establish-grip','anticipation','coil-behind','apex-hold','slash-release','slash-drive','contact','follow-through','recoil','settle-grip','release-grip','return-to-guard']
timesS=[40,60,40,60,50,75,40,40,55,90,65,80,60,85]
sourcesS=[1,1,1,2,3,3,4,5,7,8,9,10,1,1]
palmsS=[[94,81],[99,72],[105,62],[103,44],[101,29],[100,19],[111,38],[117,59],[109,81],[100,87],[96,82],[94,79],[94,81],[94,81]]
anglesS=[None,None,20,0,-15,-10,25,70,115,128,118,100,None,None]
phasesA=['rest','body-preparation','establish-grip','anticipation','hoist','overhead-coil','cleave-drive','downstroke','heavy-impact','weight-settle','wrench-recovery','release-grip','shoulder-reset','return-to-guard']
timesA=[45,65,40,80,95,155,45,45,115,120,140,50,90,100]
sourcesA=[1,1,2,2,3,4,5,6,7,8,9,10,1,1]
palmsA=[[94,80],[97,70],[101,58],[102,43],[100,27],[95,15],[108,36],[112,58],[101,76],[95,77],[99,70],[95,77],[94,80],[94,80]]
anglesA=[None,None,10,-5,-15,-20,20,65,110,120,100,None,None,None]
# Source joint centers selected visually on the already reviewed same-view donors.
donors={
 'raised':{'source':'characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-axe/layers/body/03.png','elbow':[99,35],'wrist':[93,23],'palm':[88,17],'handRowsMax':24,'rows':json.loads(Path('experiments/main-orc-combat-recovery-v7/rear-alt/author-result.json').read_text())['donorRows']},
 'sword-low':{'source':'characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword/layers/body/07.png','elbow':[89,64],'wrist':[95,83],'palm':[94,89],'handRowsMin':83,'rows':json.loads(Path('experiments/main-orc-combat-recovery-v7/rear-alt/impact-author-result.json').read_text())['donorRows']},
 'axe-low':{'source':'characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-axe/layers/body/07.png','elbow':[88,65],'wrist':[94,83],'palm':[94,89],'handRowsMin':82,'rows':[]}}
# Same-view Axe impact forearm has its own outer gauntlet; bound it explicitly.
for y in range(63,95):
 lo=83 if y<=70 else 84 if y<=78 else 87
 hi=101 if y<=72 else 103 if y<=84 else 102
 donors['axe-low']['rows'].append([y,lo,hi])
shouldersS={1:[86,40],2:[88,40],3:[88,39],4:[88,40],5:[85,43],7:[83,48],8:[81,48],9:[82,46],10:[86,42]}
shouldersA={1:[88,41],2:[89,39],3:[89,39],4:[89,39],5:[88,42],6:[84,46],7:[82,49],8:[81,50],9:[83,47],10:[87,43]}
def ik(s,p,L,D):
 dx,dy=p[0]-s[0],p[1]-s[1];d=math.hypot(dx,dy);assert abs(L-D)<d<L+D,(s,p,L,D)
 a=(L*L-D*D+d*d)/(2*d);h=math.sqrt(max(0,L*L-a*a));u=(dx/d,dy/d)
 candidates=[[s[0]+a*u[0]+sg*h*(-u[1]),s[1]+a*u[1]+sg*h*u[0]]for sg in [-1,1]]
 return [round(q)for q in max(candidates,key=lambda q:q[0])]
def mapped_wrist(d,e,p):
 a,b=d['elbow'],d['palm'];dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);u=[dx/length,dy/length];n=[-u[1],u[0]];tx,ty=p[0]-e[0],p[1]-e[1];tl=math.hypot(tx,ty);tu=[tx/tl,ty/tl];tn=[-tu[1],tu[0]];w=d['wrist'];along=sum((w[j]-a[j])*u[j]for j in range(2))*tl/length;perp=sum((w[j]-a[j])*n[j]for j in range(2));return [round(e[j]+along*tu[j]+perp*tn[j])for j in range(2)]
plans={}
for kind,phases,times,sources,palms,angles,shoulders in [('Sword',phasesS,timesS,sourcesS,palmsS,anglesS,shouldersS),('Axe',phasesA,timesA,sourcesA,palmsA,anglesA,shouldersA)]:
 frames=[]
 for i,(phase,ms,src,palm,angle)in enumerate(zip(phases,times,sources,palms,angles)):
  s=shoulders[src];name='raised'if i in [3,4,5,6]else('sword-low'if kind=='Sword'else'axe-low');D=math.dist(donors[name]['elbow'],donors[name]['palm']);distal=D
  if i==6:distal=24
  e=ik(s,palm,23,distal)
  key=None
  if kind=='Sword'and i==5:s=[88,39];e=[111,37];key='apex'
  if kind=='Sword'and i==8:s=[83,48];e=[104,56];key='impact'
  w=mapped_wrist(donors[name],e,palm)
  if key=='apex':w=[105,25]
  if key=='impact':w=[110,75]
  frames.append({'index':i,'phase':phase,'durationMs':ms,'sourceFrame':src,'base':f'characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-{kind.lower()}/layers/body/{src:02}.png','shoulder':s,'elbow':e,'wrist':w,'palm':palm,'donor':name,'weaponAngleDeg':angle,'weaponVisible':angle is not None,'preserveKey':key,'humerusPx':round(math.dist(s,e),3),'forearmPx':round(math.dist(e,w),3),'targetElbowPalmPx':round(math.dist(e,palm),3)})
 plans[kind]={'dest':(C/('back_l-'+kind.lower())).as_posix(),'frames':frames,'durationMs':sum(times),'visibleInterval':[2,11]if kind=='Sword'else[2,10]}
(E/'plan.json').write_text(json.dumps({'donors':donors,'clips':plans},indent=2));print('Sword',sum(timesS),'Axe',sum(timesA));print('donor axes',[(n,round(math.dist(d['elbow'],d['wrist']),3))for n,d in donors.items()])
