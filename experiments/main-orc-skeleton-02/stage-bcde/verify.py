from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math
E=Path('experiments/main-orc-skeleton-02/stage-bcde');S=Path('characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword')
plans=[(0,158,145,20),(5,160,81,0),(8,178,131,-138.65),(9,169,159,-131.35),(13,158,145,20)]
(E/'evidence').mkdir(exist_ok=True)
a=Image.new('RGB',(1280,812),(58,62,69));d=ImageDraw.Draw(a)
checks=[]
for k,(i,x,y,ang) in enumerate(plans):
 id=f'{i:02}'
 for r,n in enumerate(['body-only','weapon-only','composite']):
  im=Image.open(E/n/f'{id}.png').convert('RGBA');a.paste(im,(k*256,r*266+24),im);d.text((k*256+6,r*266+4),f'{id} {n} / Aseprite Lua',fill='white')
  alpha=im.getchannel('A');colors=set(im.getdata());partial=sum(1 for c in im.getdata() if 0<c[3]<255)
  checks.append(dict(image=f'{n}/{id}.png',size=list(im.size),partialAlphaPixels=partial,opaquePixels=sum(c[3]>0 for c in im.getdata()),paleNeutralPixels=sum(c[3]>0 and min(c[:3])>=180 and max(c[:3])-min(c[:3])<=18 for c in im.getdata())))
  crop=im.crop((x-20,y-20,x+20,y+20)).resize((320,320),Image.Resampling.NEAREST)
  crop.save(E/'evidence'/f'{id}-{n}-hand-wrist-8x.png')
 original=Image.open(S/'layers/body'/f'{id}.png').convert('RGBA');actual=Image.open(E/'body-only'/f'{id}.png').convert('RGBA');assert original.tobytes()==actual.tobytes()
a.save(E/'evidence/overview.png')
json.dump(checks,open(E/'pixel-checks.json','w'),indent=2)
