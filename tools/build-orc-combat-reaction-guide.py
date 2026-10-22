import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
out=Image.new('RGBA',(640,256));refs=[]
for row,(state,count) in enumerate([('Hit',3),('Defeat',5)]):
 for i in range(count):
  p=Path(f'characters/orc-01/sprites/Animations/{state}/{state.lower()}_front_r_{i:02d}.png');im=Image.open(p).convert('RGBA');a=np.array(im);a[a[:,:,3]>0,:3]=[155,155,155];a[a[:,:,3]==0]=0;out.paste(Image.fromarray(a),(128*i,128*row));refs.append({'file':p.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
target=Path('characters/orc-combat-hit-defeat-pose-guide-v1.png');out.resize((1920,768),Image.Resampling.NEAREST).save(target)
target.with_suffix('.json').write_text(json.dumps({'purpose':'Reaction/fall pose reference ONLY, not new production art','sources':refs,'operation':'Native RGBA composition and neutral grey silhouettes; no mirroring','sha256':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
p=Path('characters/orc-combat-front-batch-v1.json');batches=json.loads(p.read_text(encoding='utf-8'))
for b in batches:
 for ref in b['references']:ref['sha256']=hashlib.sha256(Path(ref['file']).read_bytes()).hexdigest()
p.write_text(json.dumps(batches,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
