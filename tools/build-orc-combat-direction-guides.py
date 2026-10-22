import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for d in ['front_l','back_r','back_l']:
 out=Image.new('RGBA',(640,256));refs=[]
 for row,(state,count) in enumerate([('Hit',3),('Defeat',5)]):
  for i in range(count):
   p=Path(f'characters/orc-01/sprites/Animations/{state}/{state.lower()}_{d}_{i:02d}.png');a=np.array(Image.open(p).convert('RGBA'));a[a[:,:,3]>0,:3]=[155,155,155];a[a[:,:,3]==0]=0;out.paste(Image.fromarray(a),(128*i,128*row));refs.append({'file':p.as_posix(),'sha256':sha(p)})
 target=Path(f'characters/orc-combat-{d}-reaction-guide-v1.png');out.resize((1920,768),Image.Resampling.NEAREST).save(target);target.with_suffix('.json').write_text(json.dumps({'purpose':'Pose-only Hit/Defeat guide, not production art','sources':refs,'operation':'Exact RGBA composition, grey silhouette finishing, no mirroring','sha256':sha(target)},indent=2)+'\n',encoding='utf-8')
batch=Path('characters/orc-combat-directions-batch-v1.json');batches=json.loads(batch.read_text(encoding='utf-8'))
for id in sorted({b['id'] for b in batches}):
 out=Image.new('RGBA',(640,384))
 for row,state in enumerate(['Attack','Hit','Defeat']):out.paste(Image.open(f'characters/{id}/source/animations-v1/{state}/front_r/native-strip.png').convert('RGBA'),(0,128*row))
 out.resize((1280,768),Image.Resampling.NEAREST).save(f'characters/{id}/source/combat-directions-v1/approved-front-combat.png')
for b in batches:
 for r in b['references']:r['sha256']=sha(r['file'])
batch.write_text(json.dumps(batches,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
