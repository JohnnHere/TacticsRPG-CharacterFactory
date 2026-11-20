from PIL import Image,ImageDraw
from pathlib import Path
out=Path('experiments/main-orc-rear-recovery-v2/E/qa-revision-1-inspection/pixel-crops')
for f in (4,5):
 p=Path(f'characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/layers/body/{f:02d}.png')
 im=Image.open(p).convert('RGBA').crop((128,72,196,148)).resize((544,608),Image.Resampling.NEAREST)
 base=Image.new('RGBA',(544,630),(25,25,25,255));base.alpha_composite(im,(0,22));ImageDraw.Draw(base).text((4,4),f'AxeR F{f:02d}, composite layer coords x128..195 y72..147',fill='white')
 base.convert('RGB').save(out/f'axeR-F{f:02d}-zoom.png')
