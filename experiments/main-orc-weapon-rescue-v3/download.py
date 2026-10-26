"""Unchanged official results + QA contact sheets only."""
from pathlib import Path
from PIL import Image,ImageDraw
from concurrent.futures import ThreadPoolExecutor
import urllib.request,sys
E=Path(__file__).resolve().parent
category,job,count=sys.argv[1],sys.argv[2],int(sys.argv[3]);out=E/category/'raw';out.mkdir(parents=True,exist_ok=True)
def get(i):
 p=out/f'{i:02d}.png'
 if not p.exists():urllib.request.urlretrieve(f'https://api.pixellab.ai/mcp/images/{job}/download?index={i}',p)
 with Image.open(p) as im:im.verify()
with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(get,range(count)))
cell=404;sheet=Image.new('RGB',(cell*3,cell*((count+2)//3)),(37,44,47));d=ImageDraw.Draw(sheet)
for i in range(count):
 im=Image.open(out/f'{i:02d}.png').convert('RGBA');im=im.resize((384,384),Image.Resampling.NEAREST);x=(i%3)*cell;y=(i//3)*cell;sheet.paste(im,(x,y+20),im);d.text((x+6,y+4),str(i),fill='white')
sheet.save(E/f'{category}-contact.png');print(category,count)
