from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
for i in [0,1,2,3,4,5,6,7,8,9,10,11]:
 im=Image.open(R/f'attack/raw/{i:02d}.png').convert('RGBA').resize((768,768),Image.Resampling.NEAREST)
 out=Image.new('RGB',(800,800),(40,45,49));out.paste(im,(30,30),im);d=ImageDraw.Draw(out)
 for v in range(0,128,10):
  d.line((30+v*6,30,30+v*6,798),fill=(60,70,75));d.text((30+v*6,12),str(v),fill='white')
  d.line((30,30+v*6,798,30+v*6),fill=(60,70,75));d.text((6,30+v*6),str(v),fill='white')
 out.save(R/f'attack/grid-{i:02d}.png')
