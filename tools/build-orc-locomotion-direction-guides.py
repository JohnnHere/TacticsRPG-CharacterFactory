import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
directions=['front_l','back_r','back_l']
guide=Image.new('RGBA',(768,768))
for n,direction in enumerate(directions):
 for j,(state,count) in enumerate([('Idle',4),('Walk',6)]):
  for i in range(count):
   im=Image.open(f'characters/orc-01/sprites/Animations/{state}/{state.lower()}_{direction}_{i:02d}.png').convert('RGBA')
   a=np.array(im);mask=a[:,:,3]>0;a[mask,:3]=[155,155,155];a[~mask]=0
   guide.paste(Image.fromarray(a),(i*128,(n*2+j)*128))
guide.resize((1536,1536),Image.Resampling.NEAREST).save('characters/orc-locomotion-directions-silhouettes-v1.png')
batch=Path('characters/orc-locomotion-directions-batch-v1.json');batches=json.loads(batch.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for b in batches:
 folder=Path(b['folder']);row=Image.new('RGBA',(384,128))
 for i,d in enumerate(directions):row.paste(Image.open(f"characters/{b['id']}/sprites/Directions/{b['id'].replace('-','_')}_dir_{d}.png"),(i*128,0))
 row.resize((1536,512),Image.Resampling.NEAREST).save(folder/'approved-directions.png')
 Image.open(f"characters/{b['id']}/source/animations-v1/Idle/front_r/native-strip.png").resize((1536,384),Image.Resampling.NEAREST).save(folder/'approved-idle-front.png')
 for ref in b['references']:ref['sha256']=sha(ref['file'])
batch.write_text(json.dumps(batches,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
Path('characters/orc-locomotion-directions-silhouettes-v1.json').write_text(json.dumps({'purpose':'Pose-only guide, never production sprite','source':'approved orc-01 Idle/Walk front_l,back_r,back_l','operation':'native RGBA composition and grey silhouette finishing, nearest preview scale, no mirroring','sha256':sha('characters/orc-locomotion-directions-silhouettes-v1.png')},indent=2)+'\n',encoding='utf-8')
