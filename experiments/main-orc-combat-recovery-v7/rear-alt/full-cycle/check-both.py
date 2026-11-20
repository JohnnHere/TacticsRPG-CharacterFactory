import json,math
from pathlib import Path
from PIL import Image
E=Path('experiments/main-orc-combat-recovery-v7/rear-alt/full-cycle');p=json.loads((E/'plan.json').read_text())
def comps(im):
 pts={(x,y)for y in range(im.height)for x in range(im.width)if im.getpixel((x,y))[3]};r=[]
 while pts:
  q=[pts.pop()]
  for x,y in q:
   for dx in [-1,0,1]:
    for dy in [-1,0,1]:
     a=x+dx,y+dy
     if a in pts:pts.remove(a);q.append(a)
  r.append(q)
 return sorted(r,key=len,reverse=True)
for kind in ['Sword','Axe']:
 cfg=p['clips'][kind];issues=[];rows=[]
 for f in cfg['frames']:
  i=f['index'];dst=Path(cfg['dest']);im=Image.open(dst/f'native/{i:02}.png').convert('RGBA');cc=comps(im);joint={name:bool(im.getpixel(tuple(f[name]))[3])for name in ['shoulder','elbow','wrist','palm']}
  if len(cc)>1:issues.append((i,'components',[(len(c),c[:2])for c in cc]))
  if not all(joint.values()):issues.append((i,'joints',joint))
  rows.append({'index':i,'components':len(cc),'opaqueJoints':joint})
 print(kind,'issues',issues);(E/(kind.lower()+'-structural-check.json')).write_text(json.dumps(rows,indent=2))

