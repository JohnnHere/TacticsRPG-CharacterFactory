from PIL import Image, ImageDraw
from pathlib import Path
import hashlib,json,math
E=Path('experiments/main-orc-anatomy-pass-08')
S=Path('experiments/main-orc-skeleton-02/stage-bcde/body-only/08.png')
a=Image.open(S).convert('RGBA'); b=Image.open(E/'candidate-08.png').convert('RGBA')
pts=[(x,y) for y in range(256) for x in range(256) if a.getpixel((x,y))!=b.getpixel((x,y))]
print('bounds',min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts),'changed',len(pts))
print('outside',[(x,y) for x,y in pts if x<147 or y<111][:30])
palette=set(a.getdata()); print('newcolors',len(set(b.getdata())-palette))
