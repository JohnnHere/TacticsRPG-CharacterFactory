from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil
E=Path('experiments/main-orc-targeted-repair-v1/artist-unarmed-sol')
S=Path('characters/orc-v1/source/targeted-repair-unarmed-sol-v1')
box=(42,50,65,81);out=Image.new('RGB',(2*460,660),(22,30,35));d=ImageDraw.Draw(out)
for j,p in enumerate([E/'before/native/03.png',S/'native/03.png']):
 im=Image.open(p).convert('RGBA');bg=Image.new('RGBA',im.size,(38,46,52,255));bg.alpha_composite(im)
 tile=bg.crop(box).convert('RGB').resize((460,620),Image.Resampling.NEAREST);out.paste(tile,(j*460,40))
 d.text((j*460+5,5),'F03 ORIGINAL' if j==0 else 'F03 CANDIDATE',fill=(235,235,220))
 for x in range(box[0],box[2]):
  if x%2==0:d.text((j*460+(x-box[0])*20,40),str(x),fill=(255,130,90))
 for y in range(box[1],box[3]):
  if y%2==0:d.text((j*460,(y-box[1])*20+40),str(y),fill=(255,130,90))
out.save(E/'F03-elbow-source-coordinate-trace.png')
im=Image.open(S/'native/03.png').convert('RGBA');points=[]
for y in range(59,77):
 for x in range(43,57):
  r,g,b,a=im.getpixel((x,y))
  if a and max(r,g,b)>=110:points.append(dict(x=x,y=y,rgba=[r,g,b,a],sameAsOriginal=im.getpixel((x,y))==Image.open(E/'before/native/03.png').convert('RGBA').getpixel((x,y))))
(E/'elbow-bright-pixels.json').write_text(json.dumps(points,indent=2)+'\n',encoding='utf8')
trial=E/'rejected/attempt-01';trial.mkdir(parents=True,exist_ok=True)
for p in [S/'native/03.png',S/'composite/03.png',S/'source/unarmed-back_l-f03-retraction-native.aseprite',S/'source/unarmed-back_l-f03-retraction-composite.aseprite',E/'author_f03.lua']:
 dest=trial/(p.parent.name+'-'+p.name)
 if not dest.exists():shutil.copy2(p,dest)
print(json.dumps(points,indent=2))
