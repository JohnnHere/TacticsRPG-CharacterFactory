from pathlib import Path
from PIL import Image,ImageDraw
import sys
E=Path(__file__).resolve().parent;category=sys.argv[1]
for p in sorted((E/category/'raw').glob('*.png')):
 im=Image.open(p).convert('RGBA');scale=6 if im.width==128 else 3;size=im.width*scale;out=Image.new('RGB',(size+30,size+30),(40,45,49));scaled=im.resize((size,size),Image.Resampling.NEAREST);out.paste(scaled,(30,30),scaled);d=ImageDraw.Draw(out)
 for v in range(0,im.width,10):
  d.line((30+v*scale,30,30+v*scale,size+30),fill=(60,70,75));d.text((30+v*scale,10),str(v),fill='white');d.line((30,30+v*scale,size+30,30+v*scale),fill=(60,70,75));d.text((5,30+v*scale),str(v),fill='white')
 out.save(E/category/f'grid-{p.stem}.png');print(category,p.stem,im.getbbox())
