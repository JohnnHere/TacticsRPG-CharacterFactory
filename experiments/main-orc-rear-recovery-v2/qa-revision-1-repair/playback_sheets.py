from PIL import Image,ImageDraw
from pathlib import Path
o=Path('experiments/main-orc-rear-recovery-v2/qa-revision-1-repair')
for k in ['SwordL','AxeR','AxeL']:
 out=Image.new('RGB',(1536,720),(30,40,47));d=ImageDraw.Draw(out)
 for j,s in enumerate([1,0.75,0.5]):
  im=Image.open(o/'playback'/f'{k}-{s}.png')
  film=im.crop((8,426,2056,716)).resize((1536,217),Image.Resampling.NEAREST)
  out.paste(film,(0,j*240+20));d.text((5,j*240+3),f'{k} actual RAF @ {s}x',fill=(240,240,240))
 out.save(o/'playback'/f'{k}-all-speeds.png')
