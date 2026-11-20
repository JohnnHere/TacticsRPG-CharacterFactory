from PIL import Image,ImageDraw
from pathlib import Path
cases=[
('swordL-f05-shoulder','characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/body/05.png',(120,80,185,125)),
('axeR-f01','characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/layers/body/01.png',(140,60,190,115)),
('axeR-f02','characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/layers/body/02.png',(142,24,190,82)),
('axeR-f03','characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/layers/body/03.png',(142,24,190,82)),
('axeL-f02-hook','characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/layers/body/02.png',(142,70,194,115)),
('axeL-f03-hook','characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/layers/body/03.png',(142,70,194,115)),
]
out=Path('experiments/main-orc-rear-recovery-v2/E/qa-revision-1-inspection/pixel-crops');out.mkdir(parents=True,exist_ok=True)
for name,p,box in cases:
 im=Image.open(p).convert('RGBA').crop(box).resize(((box[2]-box[0])*10,(box[3]-box[1])*10),Image.Resampling.NEAREST)
 canvas=Image.new('RGBA',(im.width,im.height+24),(24,24,24,255));canvas.alpha_composite(im,(0,24));ImageDraw.Draw(canvas).text((4,4),f'{name} x{box[0]} y{box[1]}',fill='white');canvas.convert('RGB').save(out/f'{name}-zoom.png')
