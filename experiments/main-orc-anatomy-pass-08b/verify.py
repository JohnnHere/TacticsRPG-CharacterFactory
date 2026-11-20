from PIL import Image,ImageDraw
from pathlib import Path
import json,hashlib
E=Path('experiments/main-orc-anatomy-pass-08b');S=Path('experiments/main-orc-skeleton-02/stage-bcde/body-only')
a=Image.open(S/'08.png').convert('RGBA');b=Image.open(E/'candidate-08b.png').convert('RGBA')
pts=[(x,y) for y in range(256) for x in range(256) if a.getpixel((x,y))!=b.getpixel((x,y))]
assert all(147<=x<=188 and 111<=y<=151 for x,y in pts)
assert b.tobytes()==Image.open(E/'master-roundtrip.png').convert('RGBA').tobytes()
assert set(b.getdata())<=set(a.getdata())
boxes=[]
for name,y0,y1 in [('sleeve-junction',111,123),('elbow',124,133),('forearm-cuff',134,145),('fist',146,151)]:
 p=[(x,y) for x,y in pts if y0<=y<=y1];boxes.append(dict(name=name,xyxyInclusive=[min(x for x,y in p),min(y for x,y in p),max(x for x,y in p),max(y for x,y in p)],changedPixels=len(p)))
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
doc=dict(technicalStatus='TECHNICALLY_COMPLETE',artisticStatus='VISUAL_REVIEW_REQUIRED',changedPixels=len(pts),unchangedPixels=65536-len(pts),boxes=boxes,scopeMask=[147,111,188,151],outsideChangedPixels=0,masterReopenedRGBAIdentical=True,newPaletteColors=0,handPivot=[174,148],sourceSHA256=h(S/'08.png'),candidateSHA256=h(E/'candidate-08b.png'),masterSHA256=h(E/'master-08b.aseprite'))
(E/'pixel-diff.json').write_text(json.dumps(doc,indent=2))
# Presentation only; no art editing outside Aseprite.
def paste(c,im,pos,scale=1):
 im=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST);c.paste(im,pos,im)
c=Image.new('RGB',(1220,820),(20,21,24));d=ImageDraw.Draw(c)
for i,(im,title) in enumerate([(a,'ANTES'),(b,'08b')]):
 x=20+i*600;d.text((x,10),title+' 1x',fill='white');paste(c,im,(x,30));d.text((x,300),title+' 8x - braco e juncao',fill='white');paste(c,im.crop((139,96,194,156)),(x,325),8)
c.save(E/'before-after.png')
c=Image.new('RGB',(1480,780),(20,21,24));d=ImageDraw.Draw(c)
for im,box,x,title in [(b,(139,96,190,155),15,'08b direito'),(a,(81,109,115,164),455,'08 esquerdo'),(Image.open(S/'05.png').convert('RGBA'),(140,66,179,123),755,'05 direito'),(Image.open(S/'09.png').convert('RGBA'),(144,110,187,173),1090,'09 direito')]:
 d.text((x,12),title+' 8x',fill='white');paste(c,im.crop(box),(x,40),8)
c.save(E/'comparison.png')
c=Image.new('RGB',(768,768),(20,21,24));paste(c,b,(0,0),3);d=ImageDraw.Draw(c)
for x,y in pts:d.rectangle((x*3,y*3,x*3+2,y*3+2),fill=(255,100,50))
c.save(E/'changed-regions.png')
print(json.dumps(doc))
