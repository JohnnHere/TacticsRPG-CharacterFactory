from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/full-front-r-sword');E.mkdir(parents=True,exist_ok=True)
assert Path.cwd().name=='TacticsRPG-CharacterFactory'
parent='characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword/clip.json';clip=json.loads(Path(parent).read_text(encoding='utf-8-sig'))
refs={parent,clip['bodyMaster'],clip['nativeMaster']}
out=Image.new('RGB',(7*256,2*282),(43,44,49));d=ImageDraw.Draw(out)
for i,f in enumerate(clip['frames']):
 refs.add(f['layers']['body']['png']);refs.add(f['png']);im=Image.open(f['layers']['body']['png']).convert('RGBA').crop((64,64,192,192)).resize((256,256),Image.Resampling.NEAREST)
 x=(i%7)*256;y=(i//7)*282;out.paste(im,(x,y+24),im);d.text((x+4,y+5),f"F{i:02} {f['durationMs']}ms {f['phase']}",fill='white')
out.save(E/'all-body-source.png')
for key,fp in [('F03',(82,93,113,131)),('F04',(80,73,116,111)),('F05',(81,65,118,105)),('F07',(136,116,171,148)),('F09',(109,128,148,165)),('F10',(91,125,127,161))]:
 i=int(key[1:]);im=Image.open(clip['frames'][i]['layers']['body']['png']).convert('RGBA');scale=18
 crop=im.crop(fp).resize(((fp[2]-fp[0])*scale,(fp[3]-fp[1])*scale),Image.Resampling.NEAREST)
 grid=Image.new('RGB',(crop.width+90,crop.height+85),(43,44,49));grid.paste(crop,(50,42),crop);gd=ImageDraw.Draw(grid)
 for x in range(fp[0],fp[2]+1):
  xx=50+(x-fp[0])*scale;gd.line((xx,42,xx,42+crop.height),fill=(65,66,72))
  if x%2==0:gd.text((xx,23),str(x),fill='white')
 for y in range(fp[1],fp[3]+1):
  yy=42+(y-fp[1])*scale;gd.line((50,yy,50+crop.width,yy),fill=(65,66,72))
  if y%2==0:gd.text((19,yy),str(y),fill='white')
 grid.save(E/(key+'-source-grid.png'))
for key in ['F02','F06','F08']:
 rp=Path('characters/orc-v1/source/combat-rescue-v5/grip-specialist')/key/'representative.json';rep=json.loads(rp.read_text());refs.update([str(rp),rep['master']])
 for f in rep['frames']:
  for v in f['layers'].values():refs.add(v['png'])
defs='characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/weapon.json';wd=json.loads(Path(defs).read_text());refs.update([defs,wd['master'],wd['sprite']])
freezes=['experiments/main-orc-combat-rescue-v5/grip-specialist/snapshot/freeze.json','experiments/main-orc-combat-rescue-v5/grip-specialist/F02-F08/snapshot/freeze.json']
for p in freezes:
 f=json.loads(Path(p).read_text());assert all(hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256']for r in f['files'])
snapshot={'parentClip':parent,'weaponDefinition':defs,'files':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest()for p in sorted(refs)},'preservedFreezes':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest()for p in freezes}}
(E/'input-snapshot.json').write_text(json.dumps(snapshot,indent=2)+'\n',encoding='utf-8')
print('13 body poses laid out; prior representative freezes preserved.')
