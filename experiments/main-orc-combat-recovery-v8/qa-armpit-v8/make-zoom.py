from pathlib import Path
from PIL import Image
E=Path(__file__).parent
for state,p in [('before','characters/orc-v1/source/combat-recovery-v7/frontal/front_l-Sword-full'),('after','characters/orc-v1/source/combat-recovery-v8/frontal-armpit/front_l-sword')]:
 out=Image.new('RGBA',(960,576),(55,55,60,255))
 for j,i in enumerate([3,4,5]):
  for row,rel in enumerate([f'layers/body/{i:02}.png',f'{i:02}.png']):
   im=Image.open(f'{p}/{rel}');c=im.crop((136,96,176,132)).resize((320,288),Image.Resampling.NEAREST);out.alpha_composite(c,(j*320,row*288))
 out.save(E.parent/f'zoom/armpit-{state}.png')
