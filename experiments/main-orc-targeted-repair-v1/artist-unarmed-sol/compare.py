from pathlib import Path
from PIL import Image,ImageDraw
E=Path('experiments/main-orc-targeted-repair-v1/artist-unarmed-sol')
S=Path('characters/orc-v1/source/targeted-repair-unarmed-sol-v1')
def qa(im,scale):
 bg=Image.new('RGBA',im.size,(38,46,52,255));bg.alpha_composite(im);return bg.convert('RGB').resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
sheet=Image.new('RGB',(5*384,2*410),(22,30,35));d=ImageDraw.Draw(sheet)
for row,p in enumerate([E/'before/native',S/'native']):
 for i in range(5):
  im=Image.open(p/f'{i:02}.png').convert('RGBA');x=i*384;y=row*410
  sheet.paste(qa(im,3),(x,y+24));d.text((x+6,y+5),f'{"BEFORE" if row==0 else "CANDIDATE"} F{i:02}',fill=(235,235,220))
sheet.save(E/'before-after-ordered.png')
detail=Image.new('RGB',(2*640,600),(22,30,35));d=ImageDraw.Draw(detail)
for j,p in enumerate([E/'before/native/03.png',S/'native/03.png']):
 im=Image.open(p).convert('RGBA');detail.paste(qa(im.crop((10,20,90,90)),8),(j*640,40));d.text((j*640+5,5),'F03 before' if j==0 else 'F03 candidate — actual saved master',fill=(235,235,220))
detail.save(E/'F03-before-after-detail.png')
