from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw
ROOT=Path.cwd()
assert ROOT.name=='TacticsRPG-CharacterFactory'
E=Path('experiments/main-orc-rear-reconstruction-v4/dev'); E.mkdir(parents=True,exist_ok=True)
C=Path('characters/orc-v1/source/rear-reconstruction-v4'); C.mkdir(parents=True,exist_ok=True)
M='characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json'
m=json.loads(Path(M).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
refs={M}
def collect(v):
 if isinstance(v,dict):
  for x in v.values():collect(x)
 elif isinstance(v,list):
  for x in v:collect(x)
 elif isinstance(v,str) and len(v)<400 and Path(v).is_file():refs.add(v)
clips={}
for c in m['cells']:
 p=json.loads(Path(c['clipJson']).read_text(encoding='utf-8-sig')); clips[c['cellId']]=p
 refs.add(c['clipJson']);collect(p)
for category in ['Sword','Axe']:
 p=f"assets/weapons/{'recruit-sword' if category=='Sword' else 'militia-axe'}/weapon.json"
 refs.add(p);collect(json.loads(Path(p).read_text(encoding='utf-8-sig')))
inventory={p:sha(p) for p in sorted(refs)}
(E/'input-inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
(E/'input-manifest.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
(E/'input-clips.json').write_text(json.dumps(clips,indent=2),encoding='utf-8')
def sheet(keys,name,body=False,scale=2):
 cols=max(len(clips[k]['frames']) for k in keys)
 w=128*scale; h=w+24
 out=Image.new('RGB',(cols*w,len(keys)*h),(42,43,48));d=ImageDraw.Draw(out)
 for ri,k in enumerate(keys):
  p=clips[k]
  for i,f in enumerate(p['frames']):
   fp=f['layers']['body']['png'] if body and 'layers' in f else f['png']
   im=Image.open(fp).convert('RGBA')
   if im.size==(256,256):im=im.crop((64,64,192,192))
   out.paste(im.resize((w,w),Image.Resampling.NEAREST),(i*w,ri*h+24),im.resize((w,w),Image.Resampling.NEAREST))
   d.text((i*w+2,ri*h+5),f"{k} F{i:02} {f['durationMs']}ms",fill='white')
 out.save(E/name)
sheet([d+'/'+a for d in ['back_r','back_l'] for a in ['Sword','Axe']],'rear-weapons-composite.png')
sheet([d+'/'+a for d in ['back_r','back_l'] for a in ['Sword','Axe']],'rear-weapons-body.png',True)
sheet([d+'/Unarmed' for d in ['front_r','front_l','back_r','back_l']],'unarmed.png')
sheet([d+'/Defeat' for d in ['front_r','front_l']],'defeat.png')
sheet([d+'/Walk' for d in ['front_r','front_l','back_r','back_l']],'walk.png',False,1)
print(json.dumps({'inputFiles':len(inventory),'clips':len(clips),'frames':sum(len(p['frames']) for p in clips.values())}))
