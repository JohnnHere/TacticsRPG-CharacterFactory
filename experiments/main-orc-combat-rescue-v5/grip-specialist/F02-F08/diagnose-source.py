from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/F02-F08');E.mkdir(parents=True,exist_ok=True)
assert Path.cwd().name=='TacticsRPG-CharacterFactory'
parent='characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword/clip.json'
clip=json.loads(Path(parent).read_text(encoding='utf-8-sig'));refs={parent,clip['bodyMaster'],clip['nativeMaster']}
wdp='characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/weapon.json';wd=json.loads(Path(wdp).read_text(encoding='utf-8-sig'));refs.update([wdp,wd['master'],wd['sprite']])
for idx in [2,8]:
 f=clip['frames'][idx];refs.update([f['layers']['body']['png'],f['png']])
 body=Image.open(f['layers']['body']['png']).convert('RGBA')
 crop=(88,87,172,159)if idx==2 else(96,94,180,166)
 out=Image.new('RGB',(1200,620),(43,44,49));d=ImageDraw.Draw(out)
 full=body.crop((64,64,192,192)).resize((512,512),Image.Resampling.NEAREST);out.paste(full,(0,26),full)
 arm=body.crop(crop).resize((672,576),Image.Resampling.NEAREST);out.paste(arm,(528,26),arm)
 d.text((6,5),f'F{idx:02} corpo sem arma -4x',fill='white');d.text((534,5),'Bracos e luvas reais -8x',fill='white')
 out.save(E/f'F{idx:02}-body-source.png')
 box=(91,119,115,145)if idx==2 else(140,131,166,155)
 scale=24;im=body.crop(box).resize(((box[2]-box[0])*scale,(box[3]-box[1])*scale),Image.Resampling.NEAREST)
 grid=Image.new('RGB',(im.width+95,im.height+90),(43,44,49));grid.paste(im,(55,45),im);gd=ImageDraw.Draw(grid)
 for x in range(box[0],box[2]+1):
  xx=55+(x-box[0])*scale;gd.line((xx,45,xx,45+im.height),fill=(68,69,74));gd.text((xx,24),str(x),fill='white')
 for y in range(box[1],box[3]+1):
  yy=45+(y-box[1])*scale;gd.line((55,yy,55+im.width,yy),fill=(68,69,74));gd.text((24,yy),str(y),fill='white')
 grid.save(E/f'F{idx:02}-palm-grid.png')
f06freeze=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/snapshot/freeze.json')
frozen=json.loads(f06freeze.read_text(encoding='utf-8-sig'));assert all(hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256']for r in frozen['files'])
snap={'cwd':str(Path.cwd()),'parentClip':parent,'weaponDefinition':wdp,'F06Freeze':str(f06freeze).replace('\\','/'),'F06FreezeSha256':hashlib.sha256(f06freeze.read_bytes()).hexdigest(),'preservedF06FreezeFiles':len(frozen['files']),'files':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest()for p in sorted(refs)}}
(E/'input-snapshot.json').write_text(json.dumps(snap,indent=2)+'\n',encoding='utf-8')
print('Body sources laid out; original F06 freeze verified unchanged.')
