from pathlib import Path
from PIL import Image,ImageDraw
import json
E=Path('experiments/main-orc-targeted-repair-v1/artist-sword-sol');S=Path('characters/orc-v1/source/targeted-repair-sword-sol-v1')
def qa(im,scale):
 bg=Image.new('RGBA',im.size,(40,48,55,255));bg.alpha_composite(im);return bg.convert('RGB').resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
sheet=Image.new('RGB',(6*400,2*420),(22,30,35));d=ImageDraw.Draw(sheet)
for row,p in enumerate([E/'fresh-before',S]):
 for col,i in enumerate([4,5,6]):
  im=Image.open(p/'composite'/f'{i:02}.png').convert('RGBA');x=col*400;y=row*420
  sheet.paste(qa(im.crop((84,50,284,250)),2),(x,y+20));d.text((x+5,y+3),f'{"BEFORE" if row==0 else "CANDIDATE"} F{i:02} whole body / blade',fill=(235,235,220))
sheet.crop((0,0,1200,840)).save(E/'F04-F05-F06-before-after.png')
detail=Image.new('RGB',(4*400,2*420),(22,30,35));d=ImageDraw.Draw(detail)
box=(160,112,200,152)
for row,p in enumerate([E/'fresh-before',S]):
 for col,key in enumerate(['body','weapon','handFront','composite']):
  if key=='weapon':
   im=Image.open(p/'layers/weaponBack/05.png').convert('RGBA');im.alpha_composite(Image.open(p/'layers/weaponFront/05.png').convert('RGBA'))
  else:im=Image.open(p/'composite/05.png' if key=='composite' else p/'layers'/key/'05.png').convert('RGBA')
  detail.paste(qa(im.crop(box),10),(col*400,row*420+20));d.text((col*400+5,row*420+3),f'{"BEFORE" if row==0 else "CANDIDATE"} F05 {key}',fill=(235,235,220))
detail.save(E/'F05-before-after-four-layers.png')
