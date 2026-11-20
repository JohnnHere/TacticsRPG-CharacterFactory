from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
E=Path('experiments/main-orc-targeted-repair-v1/artist-unarmed-sol')
S=Path('characters/orc-v1/source/targeted-repair-unarmed-sol-v1')
E.mkdir(parents=True,exist_ok=True);S.mkdir(parents=True,exist_ok=True)
P=Path('characters/orc-v1/source/rear-recovery-v2/back_l/Unarmed')
clip=json.loads((P/'clip.json').read_text('utf8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
records=[]
for p in [P/'clip.json',Path(clip['master']),Path(clip['nativeMaster'])]+[Path(f[k]) for f in clip['frames'] for k in ['png','nativePng']]:
 dest=E/'before'/p.name if p.suffix=='.aseprite' or p.name=='clip.json' else E/'before'/('native' if p.parent.name=='native' else 'composite')/p.name
 dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists():assert sha(p)==sha(dest),(p,dest)
 else:shutil.copy2(p,dest)
 records.append(dict(source=p.as_posix(),backup=dest.as_posix(),sha256=sha(p)))
f03=Path(clip['frames'][3]['png']);b03=Path('characters/orc-v1/source/complete-v1/back_l/Unarmed/03.png')
comps=[Image.open(f['png']).convert('RGBA') for f in clip['frames']]
nat=[Image.open(f['nativePng']).convert('RGBA') for f in clip['frames']]
identical=[]
for i in range(5):
 assert nat[i].tobytes()==comps[i].crop((64,64,192,192)).tobytes()
 for j in range(i):
  if comps[i].tobytes()==comps[j].tobytes():identical.append([j,i])
def qa(im,scale):
 bg=Image.new('RGBA',im.size,(38,46,52,255));bg.alpha_composite(im);return bg.convert('RGB').resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
sheet=Image.new('RGB',(5*384,410),(22,30,35));d=ImageDraw.Draw(sheet)
for i,im in enumerate(nat):sheet.paste(qa(im,3),(i*384,24));d.text((i*384+5,5),f'F{i:02} — {clip["frames"][i]["durationMs"]} ms',fill=(235,235,220))
sheet.save(E/'before-ordered-wholebody.png')
for i in [1,2,3,4]:
 im=nat[i];box=(0,15,80,90);out=qa(im.crop(box),8);d=ImageDraw.Draw(out)
 for x in range(0,80,5):d.text((x*8,0),str(x),fill=(255,140,90))
 for y in range(15,90,5):d.text((0,(y-15)*8),str(y),fill=(255,140,90))
 out.save(E/f'before-F{i:02}-arm-grid.png')
report=dict(files=records,F03ByteIdenticalBaseline=sha(f03)==sha(b03),allNativeExactCenterCrops=True,identicalFramePairs=identical,durationsMs=clip['durationsMs'],totalMs=450)
(E/'before-inventory.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
