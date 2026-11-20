"""Read-only diagnostic sheets and bounds for the selected Aseprite exports."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
O=Path(__file__).resolve().relative_to(Path.cwd().resolve()).parent
C=Path('characters/orc-v1/source/artistic-reconstruction-v6/rear')
rows=[]
for k in ['sword','axe']:
 sheet=Image.new('RGB',(6*384,2*404),(65,62,72));draw=ImageDraw.Draw(sheet)
 layers=Image.new('RGB',(6*256,4*276),(65,62,72));ld=ImageDraw.Draw(layers)
 legs=Image.new('RGB',(4*384,3*174),(65,62,72));lg=ImageDraw.Draw(legs)
 for i in range(12):
  comp=Image.open(C/f'back_r-{k}'/'frames'/f'{i:02}.png').convert('RGBA')
  x=i%6*384;y=i//6*404;big=comp.resize((384,384),Image.Resampling.NEAREST);sheet.paste(big,(x,y+20),big);draw.text((x,y),f'F{i:02}',fill='white');draw.line((x,y+20+190*1.5,x+384,y+20+190*1.5),fill=(70,90,110))
  body=Image.open(C/f'back_r-{k}'/'layers'/'body'/f'{i:02}.png').convert('RGBA')
  x=i%6*256;y=i//6*552
  for n,im in enumerate([body,comp]):layers.paste(im,(x,y+20+n*276),im);ld.text((x,y+n*276),f'F{i:02} '+('body' if n==0 else 'composite'),fill='white')
  native=Image.open(C/f'back_r-{k}'/'native'/f'{i:02}.png').convert('RGBA');crop=native.crop((0,78,128,128)).resize((384,150),Image.Resampling.NEAREST);x=i%4*384;y=i//4*174;legs.paste(crop,(x,y+24),crop);lg.text((x,y),f'F{i:02}',fill='white')
  wb=Image.open(C/f'back_r-{k}'/'layers'/'weaponBack'/f'{i:02}.png').getbbox();wf=Image.open(C/f'back_r-{k}'/'layers'/'weaponFront'/f'{i:02}.png').getbbox()
  rows.append({'category':k,'frame':i,'bodyGroundY':body.getbbox()[3]-1,'weaponBackBbox':wb,'weaponFrontBbox':wf,'visibleItemBottomY':max(b[3]-1 for b in [wb,wf] if b) if wb or wf else None,'note':'Projected bounds are contextual diagnostics; not an artistic acceptance rule.'})
 sheet.save(O/f'{k}-selected-contact.png');layers.save(O/f'{k}-selected-layers-off.png');legs.save(O/f'{k}-selected-legs.png')
(O/'selected-diagnostics.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
