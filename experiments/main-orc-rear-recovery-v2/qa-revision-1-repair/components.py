from PIL import Image
from pathlib import Path
P=Path('experiments/main-orc-rear-recovery-v2/qa-revision-1-repair/checkpoint')
for k,i in [('SwordL',5),('SwordL',4),('AxeR',3),('AxeR',4),('AxeR',5),('AxeL',2),('AxeL',3)]:
 im=Image.open(P/k/'native'/f'{i:02}.png').convert('RGBA');pts={(x,y) for y in range(128) for x in range(128) if im.getpixel((x,y))[3]};cs=[]
 while pts:
  p=pts.pop();q=[p];c=[p]
  while q:
   x,y=q.pop()
   for dx in [-1,0,1]:
    for dy in [-1,0,1]:
     a=(x+dx,y+dy)
     if a in pts:pts.remove(a);q.append(a);c.append(a)
  cs.append((len(c),(min(x for x,y in c),min(y for x,y in c),max(x for x,y in c),max(y for x,y in c)),c if len(c)<20 else []))
 print(k,i,sorted(cs,reverse=True))
