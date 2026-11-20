"""Read-only pixel registration diagnostic; emits transforms, never production rasters."""
from pathlib import Path
from PIL import Image
import numpy as np
import math,json
E=Path('experiments/main-orc-rear-reconstruction-v4/dev')
clips=json.loads((E/'input-clips.json').read_text())
results=[]
for cell,p in clips.items():
 cat=cell.split('/')[1]
 if cat not in ['Axe','Sword']:continue
 id='militia-axe' if cat=='Axe' else 'recruit-sword'
 w=json.loads(Path('assets/weapons',id,'weapon.json').read_text())
 item=np.array(Image.open(w['sprite']).convert('RGBA'))
 # Render only diagnostic predicted pixels in memory. This is registration,
 # not an exported/edited raster. Source alpha must fit exactly.
 for f in p['frames']:
  if not f.get('weaponVisible'):continue
  back=np.array(Image.open(f['layers']['weaponBack']['png']).convert('RGBA'))
  front=np.array(Image.open(f['layers']['weaponFront']['png']).convert('RGBA'))
  actual=np.where((front[:,:,3]>0)[:,:,None],front,back)
  ay,ax=np.where(actual[:,:,3]>0)
  angle=f['rotationDeg'];rad=angle*math.pi/180;c,s=math.cos(rad),math.sin(rad)
  candidates=[]
  for flip in [False,True]:
   yy,xx=np.mgrid[-100:101,-100:101]
   rx=c*xx+s*yy;ry=-s*xx+c*yy
   if flip:rx=-rx
   u=np.floor(rx+w['grip'][0]+.5).astype(int);v=np.floor(ry+w['grip'][1]+.5).astype(int)
   valid=(u>=0)&(u<96)&(v>=0)&(v<96)
   valid &= item[v.clip(0,95),u.clip(0,95),3]>0
   py,px=np.where(valid);localx=xx[valid];localy=yy[valid];q=item[v[valid],u[valid]]
   guess=[int(ax.min()-localx.min()),int(ay.min()-localy.min())]
   for dy in range(-2,3):
    for dx in range(-2,3):
     gx,gy=guess[0]+dx,guess[1]+dy;tx=localx+gx;ty=localy+gy
     inside=(tx>=0)&(tx<256)&(ty>=0)&(ty<256)
     if not inside.all():continue
     overlap=(actual[ty,tx,3]>0)
     union=len(ax)+len(tx)-int(overlap.sum());iou=float(overlap.sum()/union)
     match=int(np.all(actual[ty,tx]==q,axis=1).sum())
     candidates.append((iou,match,flip,gx,gy,len(tx),int(overlap.sum())))
  best=max(candidates)
  record={'cellId':cell,'frame':f['index'],'angle':angle,'flip':best[2],'grip':[best[3],best[4]],'alphaIoU':best[0],'sourceColorMatches':best[1],'weaponPixels':best[5],'overlap':best[6],'originalDeclaredGrip':f.get('rightGrip')}
  results.append(record)
  print(cell,f['index'],'IoU',round(best[0],5),'color',best[1],'/'+str(best[5]),'flip',best[2],'grip',record['grip'])
(E/'weapon-registration.json').write_text(json.dumps(results,indent=2))
assert all(r['alphaIoU']==1 for r in results),'Registration requires review'
