from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/front-three');E.mkdir(parents=True,exist_ok=True)
assert Path.cwd().name=='TacticsRPG-CharacterFactory'
root=Path('characters/orc-v1/source/combat-rescue-v5/combat');refs=set();clips={}
for key in ['front_l/Sword','front_r/Axe','front_l/Axe']:
 p=root/key/'clip.json';c=json.loads(p.read_text());clips[key]={'path':str(p).replace('\\','/'),'clip':c};refs.add(str(p).replace('\\','/'))
 for n in ['master','bodyMaster','nativeMaster','handMaster']:
  if c.get(n):refs.add(c[n])
 o=Image.new('RGB',(7*256,2*282),(43,44,49));d=ImageDraw.Draw(o)
 for i,f in enumerate(c['frames']):
  refs.update([f['layers']['body']['png'],f['png']]);im=Image.open(f['layers']['body']['png']).convert('RGBA').crop((64,64,192,192)).resize((256,256),Image.Resampling.NEAREST)
  x=i%7*256;y=i//7*282;o.paste(im,(x,y+24),im);d.text((x+3,y+5),f"{key} F{i:02} {f['durationMs']}ms",fill='white')
 o.save(E/(key.replace('/','-')+'-bodies.png'))
for cat in ['Sword','Axe']:
 p=root/'weapons'/cat/'weapon.json';w=json.loads(p.read_text());refs.update([str(p).replace('\\','/'),w['master'],w['sprite']])
full=Path('characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword/clip.json');refs.add(str(full).replace('\\','/'))
fullclip=json.loads(full.read_text());freezePath=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/full-front-r-sword/snapshot/freeze.json');freeze=json.loads(freezePath.read_text())
assert all(hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256']for r in freeze['files'])
# Source-body identity comparisons are diagnostics only, never new mirrored art.
known=json.loads(Path('characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword/clip.json').read_text());knownims=[np.array(Image.open(f['layers']['body']['png']).convert('RGBA'))for f in known['frames']]
matches={}
for key,data in clips.items():
 matches[key]=[]
 for f in data['clip']['frames']:
  a=np.array(Image.open(f['layers']['body']['png']).convert('RGBA'));direct=[];mirror=[]
  for i,b in enumerate(knownims):
   if np.array_equal(a,b):direct.append(i)
   if np.array_equal(a,b[:,::-1]):mirror.append(i)
  matches[key].append({'index':f['index'],'exactKnownBodyFrames':direct,'exactHorizMirrorKnownFrames':mirror})
snapshot={'clips':{k:v['path']for k,v in clips.items()},'fullFrontRSword':str(full).replace('\\','/'),'preservedFullSwordFreeze':str(freezePath).replace('\\','/'),'preservedFullSwordFreezeSha256':hashlib.sha256(freezePath.read_bytes()).hexdigest(),'preservedFullSwordFiles':len(freeze['files']),'files':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest()for p in sorted(refs)}}
(E/'input-snapshot.json').write_text(json.dumps(snapshot,indent=2)+'\n');(E/'source-body-matches.json').write_text(json.dumps(matches,indent=2)+'\n')
print(json.dumps({'sourceFrames':sum(len(v['clip']['frames'])for v in clips.values()),'matches':matches},indent=2))
