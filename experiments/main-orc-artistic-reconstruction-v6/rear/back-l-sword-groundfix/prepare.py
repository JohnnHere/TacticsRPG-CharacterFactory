from pathlib import Path
import json,hashlib,shutil
from PIL import Image
O=Path(__file__).resolve().relative_to(Path.cwd().resolve()).parent
C=Path('characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword')
O.mkdir(parents=True,exist_ok=True);(O/'before/frames').mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
clip=json.loads((C/'clip.json').read_text(encoding='utf-8'))
allowed={(C/'clip.json').as_posix(),clip['master'],clip['compositeStrip']}
for i in [7,8,9]:
 f=clip['frames'][i];allowed.add(f['png'])
 for l in ['weaponBack','weaponFront']:allowed.add(f['layers'][l]['png'])
protected={}
for cell in ['back_l-sword','back_l-axe','back_r-sword','back_r-axe']:
 for p in (C.parent/cell).rglob('*'):
  if p.is_file() and p.as_posix() not in allowed:protected[p.as_posix()]=sha(p)
for p in Path('characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword').rglob('*'):
 if p.is_file():protected[p.as_posix()]=sha(p)
shutil.copyfile(C/'clip.json',O/'before/clip.json');shutil.copyfile(clip['master'],O/'before/composite.aseprite')
for i,f in enumerate(clip['frames']):shutil.copyfile(f['png'],O/'before/frames'/f'{i:02}.png')
def metrics(f):
 ims=[Image.open(f['layers'][l]['png']).convert('RGBA') for l in ['weaponBack','weaponFront']]
 pts=[(x,y) for y in range(256) for x in range(256) if any(im.getpixel((x,y))[3] for im in ims)]
 low=[(x,y) for x,y in pts if y>190]
 bbox=lambda a:[min(x for x,y in a),min(y for x,y in a),max(x for x,y in a),max(y for x,y in a)] if a else None
 return {'weaponBboxInclusive':bbox(pts),'weaponPixelsBelowGround':len(low),'belowGroundBboxInclusive':bbox(low),'weaponMaxY':max(y for x,y in pts)}
measured={str(i):metrics(clip['frames'][i]) for i in [7,8,9]}
plans=[]
for f in clip['frames']:
 i=f['index'];plans.append({'index':i,'grip':f['rightGrip'],'angleBefore':f['rotationDeg'],'angleAfter':{7:125,8:120,9:110}.get(i,f['rotationDeg']),'scale':1,'durationMs':f['durationMs'],'modified':i in [7,8,9]})
(O/'binding-plan.json').write_text(json.dumps({'finding':'V6-QA-02','bodyMutation':False,'gripMutation':False,'itemGeometryMutation':False,'frames':plans},indent=2),encoding='utf-8')
manifests=list(C.parent.glob('*manifest*.json'))+[C.parent.parent/'weapon-patch.json',C.parent.parent/'candidate28manifest.json']
manifests+=list(Path('experiments/main-orc-artistic-reconstruction-v6').rglob('*manifest*.json'))
snap={}
for p in manifests:
 if O in p.parents:continue
 j=json.loads(p.read_text(encoding='utf-8'))
 if any(c.get('clip',c.get('clipJson'))==str(C/'clip.json').replace('\\','/') for c in j.get('cells',[])):
  snap[p.as_posix()]={'sha256':sha(p),'json':j}
(O/'before.json').write_text(json.dumps({'clip':clip,'clipSha256':sha(C/'clip.json'),'protectedFiles':protected,'allowedChangedExistingFiles':sorted(allowed),'beforeMeasurements':measured,'manifests':snap},indent=2,ensure_ascii=False),encoding='utf-8')
print('Protected',len(protected),'files; before:',measured,'manifests',list(snap))
