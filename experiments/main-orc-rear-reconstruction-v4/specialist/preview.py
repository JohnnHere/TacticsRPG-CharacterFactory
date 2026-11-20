import sys
from PIL import Image, ImageDraw
B='characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/native/'
name=sys.argv[1]; O='experiments/main-orc-rear-reconstruction-v4/specialist/iter/'
box=(24,0,128,128); S=3
def load(p): return Image.open(p).convert('RGBA').crop(box)
tiles=[('F03 cur',load(B+'03.png')),('F04 cur',load(B+'04.png')),('F05 cur',load(B+'05.png')),('F05 NEW body',load(O+name+'-body.png')),('F05 NEW equip',load(O+name+'-equipped.png')),('F06 cur',load(B+'06.png'))]
w,h=tiles[0][1].size
sh=Image.new('RGBA',(3*(w*S+8)+8,2*(h*S+18)+8),(60,80,60,255));dr=ImageDraw.Draw(sh)
for i,(t,im) in enumerate(tiles):
    x=8+(i%3)*(w*S+8);y=8+(i//3)*(h*S+18)
    dr.text((x,y),t,fill=(255,255,0,255));sh.alpha_composite(im.resize((w*S,h*S),Image.NEAREST),(x,y+14))
sh.save(O+name+'-compare.png')
