from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
E=Path('experiments/main-orc-targeted-repair-v1/artist-sword-sol')
S=Path('characters/orc-v1/source/targeted-repair-sword-sol-v1')
P=Path('characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2')
E.mkdir(parents=True,exist_ok=True);S.mkdir(parents=True,exist_ok=True)
clip=json.loads((P/'clip.json').read_text('utf8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
records=[]
for p in [P/'clip.json',Path(clip['master']),Path(clip['bodyMaster']),Path(clip['nativeMaster']),Path(clip['weapon']['source'])]+[Path(f[k]) for f in clip['frames'] for k in ['png','nativePng']]+[Path(v['png']) for f in clip['frames'] for v in f['layers'].values()]:
 if p.is_relative_to(P):dest=E/'before/package'/p.relative_to(P)
 elif p.suffix=='.aseprite':dest=E/'before/source'/p.name
 else:dest=E/'before/weapon'/p.name
 dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists():assert sha(p)==sha(dest),(p,dest)
 else:shutil.copy2(p,dest)
 records.append(dict(source=p.as_posix(),backup=dest.as_posix(),sha256=sha(p)))
unarmed=Path('experiments/main-orc-targeted-repair-v1/artist-unarmed-sol/hashes.json')
guarded=[dict(path=unarmed.as_posix(),sha256=sha(unarmed))]
for r in json.loads(unarmed.read_text('utf8'))['files']:guarded.append(dict(path=r['path'],sha256=sha(r['path'])))
def qa(im,scale):
 bg=Image.new('RGBA',im.size,(40,48,55,255));bg.alpha_composite(im);return bg.convert('RGB').resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
for name in ['composite','body']:
 sheet=Image.new('RGB',(4*512,2*540),(22,30,35));d=ImageDraw.Draw(sheet)
 for i,f in enumerate(clip['frames']):
  im=Image.open(f['png'] if name=='composite' else f['layers']['body']['png']).convert('RGBA')
  sheet.paste(qa(im,2),(i%4*512,i//4*540+24));d.text((i%4*512+5,i//4*540+5),f'F{i:02} {f["phase"]} {f["durationMs"]}ms',fill=(235,235,220))
 sheet.save(E/f'before-{name}-whole.png')
# Grip comparisons contain body, independent weapon, occluding hand, final.
hands=Image.new('RGB',(6*320,4*350),(22,30,35));d=ImageDraw.Draw(hands)
for i in range(1,7):
 f=clip['frames'][i];gx,gy=f['rightGrip'];box=(gx-20,gy-20,gx+20,gy+20)
 for row,key in enumerate(['body','weapon','handFront','composite']):
  if key=='weapon':
   im=Image.open(f['layers']['weaponBack']['png']).convert('RGBA');im.alpha_composite(Image.open(f['layers']['weaponFront']['png']).convert('RGBA'))
  else:im=Image.open(f['png'] if key=='composite' else f['layers'][key]['png']).convert('RGBA')
  x=(i-1)*320;y=row*350;hands.paste(qa(im.crop(box),8),(x,y+28));d.text((x+5,y+5),f'F{i:02} {key} grip({gx},{gy}) {f["rotationDeg"]}deg',fill=(235,235,220))
hands.save(E/'before-grips-four-representations.png')
weapon=Image.open(clip['weapon']['source']).convert('RGBA');out=qa(weapon,10);d=ImageDraw.Draw(out)
for x in range(0,96,5):d.text((x*10,0),str(x),fill=(255,140,70))
for y in range(0,96,5):d.text((0,y*10),str(y),fill=(255,140,70))
out.save(E/'sword-source-coordinates.png')
(E/'before-inventory.json').write_text(json.dumps(dict(files=records,protectedUnarmed=guarded,durationsMs=clip['durationsMs']),indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(backupFiles=len(records),unarmedProtectedFiles=len(guarded),masterSha256=sha(clip['master']))))
