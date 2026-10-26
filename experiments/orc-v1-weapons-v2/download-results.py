"""Download original PixelLab results and make QA contact sheets only; no authored raster edits."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
jobs={'sword':('47d29508-88b2-4966-9116-73d3b287ea10',4),'axe':('a60c76e5-b809-4f65-89fa-3bec7d879693',4),'attack':('2a0f483d-fd6d-4894-ade9-48b4027dee0a',12)}
def run(group):
 job,n=jobs[group];out=ROOT/group/'raw';out.mkdir(parents=True,exist_ok=True)
 def get(i):
  p=out/f'{i:02d}.png'
  if not p.exists():urllib.request.urlretrieve(f'https://api.pixellab.ai/mcp/images/{job}/download?index={i}',p)
  with Image.open(p) as im:im.verify()
 with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(get,range(n)))
 size=128 if group=='attack' else 96;scale=3;cell=size*scale+20
 sheet=Image.new('RGB',(cell*4,cell*((n+3)//4)),(35,39,42));draw=ImageDraw.Draw(sheet)
 for i in range(n):
  im=Image.open(out/f'{i:02d}.png').convert('RGBA');im=im.resize((size*scale,size*scale),Image.Resampling.NEAREST)
  x=(i%4)*cell;y=(i//4)*cell;sheet.paste(im,(x,y+20),im);draw.text((x+6,y+3),str(i),fill='white')
 sheet.save(ROOT/f'{group}-contact.png');print(group,n)
if __name__=='__main__':
 import sys
 for group in sys.argv[1:]:run(group)
