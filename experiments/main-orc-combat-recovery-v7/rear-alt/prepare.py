from pathlib import Path
import json,hashlib,math
E=Path('experiments/main-orc-combat-recovery-v7/rear-alt');snapshot={}
roots=['characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword','characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-axe','characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword','characters/orc-v1/source/combat-recovery-v7/rear-r','experiments/main-orc-combat-recovery-v7/rear-r']
for r in roots:
 for p in Path(r).rglob('*'):
  if p.is_file():snapshot[p.as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(E/'protected-input-hashes.json').write_text(json.dumps(snapshot,indent=2))
def measure(s,e,w,p):
 u=math.dist(s,e);f=math.dist(e,w);a=[s[j]-e[j]for j in range(2)];b=[w[j]-e[j]for j in range(2)];ang=math.degrees(math.acos(max(-1,min(1,sum(a[j]*b[j]for j in range(2))/(u*f)))))
 return {'shoulder':s,'elbow':e,'wrist':w,'palm':p,'humerusPx':round(u,3),'forearmPx':round(f,3),'elbowInteriorDeg':round(ang,3)}
candidates=[{'source':'back_l-axe/03','joints':measure([89,39],[99,35],[93,23],[88,17]),'gloveBounds':[82,11,98,24],'decision':'SELECT forearm+closed glove; both bounded and visible; upper arm foreshortened and must be reauthored'}, {'source':'back_l-axe/02','joints':measure([89,39],[101,44],[101,31],[98,27]),'gloveBounds':[94,21,106,32],'decision':'NOT_SELECTED wrist lower; broader bracer and less independent hand'}, {'source':'back_l-sword/03','joints':measure([89,39],[103,39],[101,28],[96,25]),'gloveBounds':[93,20,105,29],'decision':'NOT_SELECTED shortened forearm, cuff blends shoulder'}, {'source':'back_l-sword/04','joints':measure([89,40],[104,43],[104,33],[101,31]),'gloveBounds':[97,26,109,36],'decision':'NOT_SELECTED low wrist/hand and arm overlap'}]
plan={'coordinates':'native128; add [64,64] for composite256','measurementMethod':'Visually identified joint centers on magnified saved body PNGs; +/-1 native px tracing uncertainty; no automatic centroid-as-palm assumption','donors':candidates,'contralateralReference':measure([47,40],[39,62],[35,76],[35,81]),'apex':{'base':'characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword/layers/body/03.png','donor':'characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-axe/layers/body/03.png','translation':[12,2],'joints':measure([88,39],[111,37],[105,25],[100,19]),'grip':[100,19],'weaponAngleDeg':-10,'durationMs':110},'impact':{'state':'NOT_AUTHORED_YET'}}
(E/'joint-plan.json').write_text(json.dumps(plan,indent=2));print('inputs frozen',len(snapshot));print(json.dumps(plan['apex']['joints']))
