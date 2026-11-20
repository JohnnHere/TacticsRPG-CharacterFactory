"""Preserve provider PNGs verbatim; Pillow is only used for inspection sheets."""
from pathlib import Path
import json,urllib.request,concurrent.futures
from PIL import Image,ImageDraw
O=Path(__file__).resolve().relative_to(Path.cwd().resolve()).parent
jobs=json.loads((O/'jobs.json').read_text(encoding='utf-8'))
def get(t):
 k,j,i=t;p=O/'raw'/k/f'{i:02}.png';p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():
  with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{j}/download?index={i}',timeout=50) as r:data=r.read()
  p.write_bytes(data)
 return p
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 list(ex.map(get,[(k,j,i) for k,j in jobs.items() for i in range(12)]))
diagnostics=[]
for k in jobs:
 sheet=Image.new('RGB',(4*512,3*536),(68,65,75));draw=ImageDraw.Draw(sheet)
 legs=Image.new('RGB',(4*384,3*174),(68,65,75));ld=ImageDraw.Draw(legs)
 for i in range(12):
  im=Image.open(O/'raw'/k/f'{i:02}.png').convert('RGBA')
  x=i%4*512;y=i//4*536;big=im.resize((512,512),Image.Resampling.NEAREST);sheet.paste(big,(x,y+24),big);draw.text((x,y),f'F{i:02}',fill='white')
  x=i%4*384;y=i//4*174;crop=im.crop((0,78,128,128)).resize((384,150),Image.Resampling.NEAREST);legs.paste(crop,(x,y+24),crop);ld.text((x,y),f'F{i:02} legs',fill='white')
  boots=[]
  for x0,x1 in [(0,64),(64,128)]:
   pts=[(x,y) for y in range(114,128) for x in range(x0,x1) if im.getpixel((x,y))[3]>127]
   boots.append({'bbox':[min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)] if pts else None,'opaquePixels':len(pts)})
  diagnostics.append({'category':k,'frame':i,'bodyBbox':im.getbbox(),'lowerBootRegions':boots,'note':'Region occupancy is diagnostic, not an anatomical length or artistic gate.'})
 sheet.save(O/f'{k}-raw-grid.png');legs.save(O/f'{k}-legs-grid.png')
(O/'raw-diagnostics.json').write_text(json.dumps(diagnostics,indent=2),encoding='utf-8')
print('24 provider frames preserved verbatim; whole-body and leg inspection sheets saved.')
