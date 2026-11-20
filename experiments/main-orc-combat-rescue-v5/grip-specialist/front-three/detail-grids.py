from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/front-three');snap=json.loads((E/'input-snapshot.json').read_text())
configs={('front_r/Axe',5):(137,118,158,145),('front_r/Axe',6):(140,132,162,157),('front_r/Axe',7):(129,134,153,158),('front_l/Axe',5):(97,118,118,145),('front_l/Axe',6):(93,132,115,157),('front_l/Axe',7):(102,134,126,158)}
for (key,i),box in configs.items():
 c=json.loads(Path(snap['clips'][key]).read_text());im=Image.open(c['frames'][i]['layers']['body']['png']).convert('RGBA');s=24;crop=im.crop(box).resize(((box[2]-box[0])*s,(box[3]-box[1])*s),Image.Resampling.NEAREST)
 o=Image.new('RGB',(crop.width+90,crop.height+85),(50,54,59));o.paste(crop,(52,42),crop);d=ImageDraw.Draw(o)
 for x in range(box[0],box[2]+1):
  xx=52+(x-box[0])*s;d.line((xx,42,xx,42+crop.height),fill=(74,77,83));d.text((xx,22),str(x),fill='white')
 for y in range(box[1],box[3]+1):
  yy=42+(y-box[1])*s;d.line((52,yy,52+crop.width,yy),fill=(74,77,83));d.text((20,yy),str(y),fill='white')
 o.save(E/(key.replace('/','-')+f'-F{i:02}-grid.png'))
print('Six independent Axe drive/impact/settle source grids saved.')
