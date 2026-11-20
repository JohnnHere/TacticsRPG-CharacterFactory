from PIL import Image,ImageDraw
from pathlib import Path
p=Path('characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/body256')
s=Image.new('RGB',(768,440),(55,60,68));d=ImageDraw.Draw(s)
for j,i in enumerate([9,10]):
 im=Image.open(p/f'{i:02}.png').convert('RGBA').crop((145,130,177,174)).resize((256,352),Image.Resampling.NEAREST);s.paste(im,(j*384,40),im);d.text((j*384,10),f'F{i} x145..176 y130..173, 8x')
s.save('experiments/main-orc-backl-v5base/recovery-hands-inspection.png')
