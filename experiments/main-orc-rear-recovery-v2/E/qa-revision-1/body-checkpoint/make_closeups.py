from PIL import Image,ImageDraw
from pathlib import Path
cases=[
('swordL-f05','experiments/main-orc-rear-recovery-v2/E/qa-revision-1/body-checkpoint/exports/back_l-sword/body/05.png',(120,78,184,126)),
('axeR-f01','experiments/main-orc-rear-recovery-v2/E/qa-revision-1/body-checkpoint/exports/back_r-axe/body/01.png',(140,60,190,115)),
('axeR-f02','experiments/main-orc-rear-recovery-v2/E/qa-revision-1/body-checkpoint/exports/back_r-axe/body/02.png',(142,24,190,82)),
('axeR-f03','experiments/main-orc-rear-recovery-v2/E/qa-revision-1/body-checkpoint/exports/back_r-axe/body/03.png',(142,24,190,82)),
('axeR-f04','experiments/main-orc-rear-recovery-v2/E/qa-revision-1/body-checkpoint/exports/back_r-axe/body/04.png',(128,72,196,148)),
('axeR-f05','experiments/main-orc-rear-recovery-v2/E/qa-revision-1/body-checkpoint/exports/back_r-axe/body/05.png',(128,72,196,148)),
('axeL-f02','experiments/main-orc-rear-recovery-v2/E/qa-revision-1/body-checkpoint/exports/back_l-axe/body/02.png',(142,70,194,115)),
]
out=Path('experiments/main-orc-rear-recovery-v2/E/qa-revision-1/body-checkpoint/closeups');out.mkdir(parents=True,exist_ok=True)
for name,p,box in cases:
 im=Image.open(p).convert('RGBA').crop(box).resize(((box[2]-box[0])*8,(box[3]-box[1])*8),Image.Resampling.NEAREST)
 # grid every source pixel; darker lines, stronger every 4 pixels
 d=ImageDraw.Draw(im,'RGBA')
 for x in range(0,im.width,8): d.line((x,0,x,im.height),fill=(220,220,220,80) if (x//8)%4==0 else (150,150,150,35),width=1)
 for y in range(0,im.height,8): d.line((0,y,im.width,y),fill=(220,220,220,80) if (y//8)%4==0 else (150,150,150,35),width=1)
 base=Image.new('RGBA',(im.width,im.height+24),(24,24,24,255));base.alpha_composite(im,(0,24));ImageDraw.Draw(base).text((4,4),f'{name} source x{box[0]} y{box[1]}; grid=1px, major=4px',fill='white');base.convert('RGB').save(out/f'{name}.png')
