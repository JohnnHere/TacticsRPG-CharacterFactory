from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist');E.mkdir(parents=True,exist_ok=True)
C=Path('characters/orc-v1/source/combat-rescue-v5/grip-specialist');C.mkdir(parents=True,exist_ok=True)
assert Path.cwd().name=='TacticsRPG-CharacterFactory'
paths=['characters/orc-v1/source/combat-rescue-v5/combat/front_r/Sword/clip.json','characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword/clip.json']
clips=[json.loads(Path(p).read_text(encoding='utf-8-sig'))for p in paths]
refs=set(paths)
for c in clips:
 for key in ['master','nativeMaster','bodyMaster','handMaster']:refs.add(c[key])
 for i in [2,6,8]:
  for val in c['frames'][i]['layers'].values():refs.add(val['png'])
  refs.add(c['frames'][i]['png'])
defs='characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/weapon.json';w=json.loads(Path(defs).read_text(encoding='utf-8-sig'));refs.update([defs,w['master'],w['sprite']])
(E/'input-snapshot.json').write_text(json.dumps({'cwd':str(Path.cwd()),'clips':paths,'weapon':defs,'files':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest()for p in sorted(refs)}},indent=2),encoding='utf-8')
body=Image.open(clips[1]['frames'][6]['layers']['body']['png']).convert('RGBA')
assert np.array_equal(np.array(body),np.array(Image.open(clips[0]['frames'][6]['layers']['body']['png']).convert('RGBA')))
out=Image.new('RGB',(1024,700),(43,44,49));d=ImageDraw.Draw(out)
full=body.crop((64,64,192,192)).resize((512,512),Image.Resampling.NEAREST);out.paste(full,(0,24),full);d.text((4,4),'F06 CORPO REAL sem arma - native128 em4x',fill='white')
box=(96,92,172,154);im=body.crop(box).resize((456,372),Image.Resampling.NEAREST);out.paste(im,(540,24),im);d.text((540,4),'Ombros / bracos / maos -6x',fill='white')
for x in range(96,173,4):
 xx=540+(x-96)*6;d.line((xx,24,xx,396),fill=(69,70,76));d.text((xx,400),str(x),fill='white')
for y in range(92,155,4):
 yy=24+(y-92)*6;d.line((540,yy,996,yy),fill=(69,70,76));d.text((1000,yy),str(y),fill='white')
item=Image.open(w['sprite']).convert('RGBA');item=item.resize((384,384),Image.Resampling.NEAREST);out.paste(item,(540,300),item)
out.save(E/'body-F06-anatomy-source.png')
body.crop((90,84,174,156)).resize((672,576),Image.Resampling.NEAREST).save(E/'body-F06-arms-8x.png')
print('F06 body pixels identical across both rejected clips. Snapshot written; art unchanged.')
