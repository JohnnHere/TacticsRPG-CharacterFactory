from PIL import Image, ImageDraw
from pathlib import Path
root=Path('.')
out=Path('experiments/main-orc-rear-recovery-v2/E/qa-revision-1-inspection/pixel-crops')
out.mkdir(parents=True,exist_ok=True)
cases=[
('swordL', 'characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/body', [1,5,7], (146,112,180,160)),
('axeR','characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/layers/body',[1,2,3,4,5],(128,24,196,148)),
('axeL','characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/layers/body',[2,3],(142,70,194,115)),
]
for name,d,frames,box in cases:
 imgs=[]
 for f in frames:
  p=Path(d)/f'{f:02d}.png'
  im=Image.open(p).convert('RGBA').crop(box)
  im=im.resize((im.width*8,im.height*8),Image.Resampling.NEAREST)
  canvas=Image.new('RGBA',(im.width,im.height+22),(30,30,30,255)); canvas.alpha_composite(im,(0,22)); ImageDraw.Draw(canvas).text((4,4),f'{name} F{f:02d} crop={box}',fill='white')
  imgs.append(canvas)
 cols=1 if name!='axeR' else 2
 cw=max(i.width for i in imgs); ch=max(i.height for i in imgs)
 sheet=Image.new('RGBA',(cols*cw,((len(imgs)+cols-1)//cols)*ch),(50,50,50,255))
 for j,i in enumerate(imgs): sheet.alpha_composite(i,((j%cols)*cw,(j//cols)*ch))
 sheet.convert('RGB').save(out/f'{name}-pixel-crops.png')
