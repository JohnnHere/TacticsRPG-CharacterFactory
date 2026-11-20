from pathlib import Path
from PIL import Image,ImageDraw
import json
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/full-front-r-sword');C=Path('characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword')
a=json.loads((E/'anatomy.json').read_text());p=json.loads(Path('characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword/clip.json').read_text())
o=Image.new('RGB',(1792,564),(43,44,49));d=ImageDraw.Draw(o)
for i,f in enumerate(p['frames']):
 im=Image.open(C/f'{i:02}.png').convert('RGBA');x=i%7*256;y=i//7*282;o.paste(im,(x,y+24),im);d.text((x+4,y+5),f"F{i:02} {f['durationMs']}ms",fill='white')
o.save(E/'all-final-frames.png')
keys=[3,4,5,7,9,10];o=Image.new('RGB',(3*384,2*398),(43,44,49));d=ImageDraw.Draw(o)
ann=Image.new('RGB',(3*384,2*398),(43,44,49));ad=ImageDraw.Draw(ann)
for n,i in enumerate(keys):
 cfg=a['frames'][i];gx,gy=cfg['grip'];box=(gx-24,gy-22,gx+24,gy+22);x=n%3*384;y=n//3*398
 im=Image.open(C/f'{i:02}.png').convert('RGBA').crop(box).resize((384,352),Image.Resampling.NEAREST);o.paste(im,(x,y+30),im);d.text((x+4,y+6),f'F{i:02} real glove {cfg["grip"]}, {cfg["angleDeg"]}deg',fill='white')
 body=Image.open(p['frames'][i]['layers']['body']['png']).convert('RGBA').crop(box).resize((384,352),Image.Resampling.NEAREST);ann.paste(body,(x,y+30),body)
 for name in ['wrist','palm','thumb']:
  point=cfg[name];xx=x+(point[0]-box[0])*8;yy=y+30+(point[1]-box[1])*8;color=(255,202,75)if name=='palm'else(65,220,175)
  ad.ellipse((xx-3,yy-3,xx+3,yy+3),outline=color,width=2);ad.text((xx+4,yy-10),name,fill=color)
 ad.text((x+4,y+6),f'F{i:02} source body - wrist / palm / thumb',fill='white')
o.save(E/'new-grips-final.png');ann.save(E/'new-gloves-source-annotated.png')
print('All13 final frames and six new source/finished grip crops laid out without production raster edits.')
