from pathlib import Path
import concurrent.futures,urllib.request
from PIL import Image,ImageDraw
O=Path(__file__).parent
jobs={'sword':'61ca245f-d86e-4ca8-a8eb-7886f5732df7','axe':'8e309cdd-cd08-45e6-a0d7-2825842e286e'}
def get(t):
 k,j,i=t;p=O/'raw-reference2'/k/f'{i:02}.png';p.parent.mkdir(parents=True,exist_ok=True)
 with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{j}/download?index={i}',timeout=50) as r:d=r.read()
 p.write_bytes(d)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:list(ex.map(get,[(k,j,i) for k,j in jobs.items() for i in range(12)]))
for k in jobs:
 s=Image.new('RGB',(4*512,3*536),(68,65,75));d=ImageDraw.Draw(s)
 for i in range(12):
  im=Image.open(O/'raw-reference2'/k/f'{i:02}.png').convert('RGBA').resize((512,512),Image.Resampling.NEAREST);x=(i%4)*512;y=(i//4)*536;s.paste(im,(x,y+24),im);d.text((x,y),f'F{i:02}',fill='white')
 s.save(O/f'{k}-reference2-grid.png')
print('24 raw reference2 frames preserved')
