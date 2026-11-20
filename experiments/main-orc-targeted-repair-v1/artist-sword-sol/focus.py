from pathlib import Path
from PIL import Image,ImageDraw
import json
E=Path('experiments/main-orc-targeted-repair-v1/artist-sword-sol')
clip=json.loads((E/'before/package/clip.json').read_text('utf8'))
def qa(im,scale):
 bg=Image.new('RGBA',im.size,(40,48,55,255));bg.alpha_composite(im);return bg.convert('RGB').resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
for i in [4,5,6]:
 f=clip['frames'][i];gx,gy=f['rightGrip'];box=(gx-17,gy-17,gx+18,gy+18)
 for kind in ['body','composite']:
  im=Image.open(f['png'] if kind=='composite' else f['layers']['body']['png']).convert('RGBA')
  out=qa(im.crop(box),20);d=ImageDraw.Draw(out)
  for x in range(box[0],box[2]):
   if x%2==0:d.text(((x-box[0])*20,0),str(x),fill=(255,140,70))
  for y in range(box[1],box[3]):
   if y%2==0:d.text((0,(y-box[1])*20),str(y),fill=(255,140,70))
  out.save(E/f'F{i:02}-{kind}-grip-source-grid.png')
  if kind=='body':
   im2=Image.open(f['layers']['body']['png']).convert('RGBA');qa(im2.crop((125,80,192,150)),7).save(E/f'F{i:02}-shoulder-elbow-wrist.png')
