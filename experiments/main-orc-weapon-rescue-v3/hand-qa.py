from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[2];E=Path(__file__).resolve().parent;p=json.loads((E/'composition-plan.json').read_text(encoding='utf-8'))
for category,c in p['profiles'].items():
 frames=[(i,f) for i,f in enumerate(c['frames']) if f['visible']];cell=264;out=Image.new('RGB',(cell*3,cell*((len(frames)+2)//3)),(45,54,58));d=ImageDraw.Draw(out)
 for n,(i,f) in enumerate(frames):
  im=Image.open(R/p['output']/category/'Attack'/f'{i:02d}.png').convert('RGBA');x,y=[v+64 for v in f['grip']];crop=im.crop((x-12,y-12,x+12,y+12)).resize((240,240),Image.Resampling.NEAREST);xx=(n%3)*cell;yy=(n//3)*cell;out.paste(crop,(xx,yy+24),crop);d.text((xx+5,yy+5),f'{i} {f["phase"]}',fill='white')
 out.save(E/f'{category.lower()}-hands.png');print(category,len(frames))
