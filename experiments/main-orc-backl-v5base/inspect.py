from PIL import Image,ImageDraw
from pathlib import Path
r=Path('.')
out=r/'experiments/main-orc-backl-v5base'
paths=[r/'characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/native',r/'characters/orc-v1/source/combat-rescue-v5/combat/back_l/Axe/native']
for name,p in zip(['sword','axe'],paths):
 fs=sorted(p.glob('*.png')); sheet=Image.new('RGB',(4*384,((len(fs)+3)//4)*410),(50,55,64)); d=ImageDraw.Draw(sheet)
 for i,f in enumerate(fs):
  im=Image.open(f).convert('RGBA'); tile=im.resize((384,384),Image.Resampling.NEAREST); x=(i%4)*384;y=(i//4)*410;sheet.paste(tile,(x,y+24),tile);d.text((x+8,y+6),f.name)
 sheet.save(out/(name+'-v5-inspection.png'))
