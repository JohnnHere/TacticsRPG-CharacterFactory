from PIL import Image,ImageDraw
from pathlib import Path
for n in ['sword','axe']:
 p=Path('experiments/main-orc-backl-v5base')/n
 fs=sorted((p/'frames').glob('*.png')); s=Image.new('RGB',(4*512,((len(fs)+3)//4)*540),(45,50,59));d=ImageDraw.Draw(s)
 for i,f in enumerate(fs):
  im=Image.open(f).convert('RGBA').resize((512,512),Image.Resampling.NEAREST);x=i%4*512;y=i//4*540;s.paste(im,(x,y+24),im);d.text((x+10,y+6),f'F{i:02d}')
 s.save(p/'inspection-2x.png')
