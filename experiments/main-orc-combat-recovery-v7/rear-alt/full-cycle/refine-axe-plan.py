from pathlib import Path
import json,math
E=Path('experiments/main-orc-combat-recovery-v7/rear-alt/full-cycle');p=json.loads((E/'plan.json').read_text());c=p['clips']['Axe'];f=c['frames'];f.insert(4,dict(f[4],phase='hoist-transition',sourceFrame=3,base='characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-axe/layers/body/03.png'))
points=[([104,57],[94,80]),([110,49],[97,70]),([110,37],[110,58]),([104,34],[119,45]),([108,48],[116,31]),([111,43],[103,24]),([110,31],[95,15]),([109,46],[116,32]),([107,45],[119,57]),([105,52],[101,76]),([104,54],[95,77]),([106,46],[99,70]),([107,55],[95,77]),([104,57],[94,80]),([104,57],[94,80])]
angles=[None,None,10,-5,-10,-15,-20,20,65,110,120,100,None,None,None];times=[45,65,40,80,45,95,155,45,45,115,120,140,50,90,100]
for i,(a,(e,palm),ang,ms)in enumerate(zip(f,points,angles,times)):
 a.update(index=i,elbow=e,palm=palm,weaponAngleDeg=ang,weaponVisible=ang is not None,durationMs=ms,donor='raised'if 3<=i<=7 else'axe-low')
 d=p['donors'][a['donor']];s0,p0=d['elbow'],d['palm'];sl=math.dist(s0,p0);u=[(p0[j]-s0[j])/sl for j in range(2)];n=[-u[1],u[0]];tl=math.dist(e,palm);tu=[(palm[j]-e[j])/tl for j in range(2)];tn=[-tu[1],tu[0]];w=d['wrist'];along=sum((w[j]-s0[j])*u[j]for j in range(2))*tl/sl;perp=sum((w[j]-s0[j])*n[j]for j in range(2));a['wrist']=[round(e[j]+along*tu[j]+perp*tn[j])for j in range(2)];a['humerusPx']=round(math.dist(a['shoulder'],e),3);a['forearmPx']=round(math.dist(e,a['wrist']),3);a['targetElbowPalmPx']=round(tl,3)
c['visibleInterval']=[2,11];c['durationMs']=sum(times);(E/'plan.json').write_text(json.dumps(p,indent=2));print('Axe',sum(times),len(f))
