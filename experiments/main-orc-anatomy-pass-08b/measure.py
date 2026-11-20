from PIL import Image
from pathlib import Path
import math,json
E=Path('experiments/main-orc-anatomy-pass-08b');S=Path('experiments/main-orc-skeleton-02/stage-bcde/body-only')
def width(im,c,t):
 n=(-t[1],t[0]);l=math.hypot(*n);n=(n[0]/l,n[1]/l)
 def ok(d):return im.getpixel((round(c[0]+n[0]*d),round(c[1]+n[1]*d)))[3]>0
 vals=[]
 for sign in [-1,1]:
  d=0
  while d<22 and ok(sign*d):d+=.25
  vals.append(d)
 return round(sum(vals),1)
a=Image.open(S/'08.png').convert('RGBA');b=Image.open(E/'candidate-08b.png').convert('RGBA')
rows=[]
for label,c,t in [('08b superior',(155,120),(12,14)),('08b cotovelo',(163,130),(10,13)),('08b antebraco',(171,139),(8,12)),('08b punho',(174,147),(3,8)),('08 esquerdo superior',(102,121),(-5,16)),('08 esquerdo antebraco',(97,140),(-5,16)),('08 esquerdo mao',(93,154),(-3,10)),('05 direito antebraco',(166,97),(0,-12)),('09 direito antebraco',(174,143),(4,17))]:
 im=b if label.startswith('08b') else a if label.startswith('08 ') else Image.open(S/('05.png' if label.startswith('05') else '09.png')).convert('RGBA')
 rows.append(dict(section=label,center=c,tangent=t,opaqueCrossSectionPx=width(im,c,t)))
(E/'measurements.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows))
