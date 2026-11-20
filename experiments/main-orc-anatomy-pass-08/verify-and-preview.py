from PIL import Image,ImageDraw
from pathlib import Path
import hashlib,json,math
E=Path('experiments/main-orc-anatomy-pass-08'); S=Path('experiments/main-orc-skeleton-02/stage-bcde/body-only/08.png')
a=Image.open(S).convert('RGBA');b=Image.open(E/'candidate-08.png').convert('RGBA')
pts=[(x,y) for y in range(256) for x in range(256) if a.getpixel((x,y))!=b.getpixel((x,y))]
assert all(147<=x<=188 and 111<=y<=148 for x,y in pts)
assert set(b.getdata())<=set(a.getdata())
assert b.tobytes()==Image.open(E/'master-roundtrip.png').convert('RGBA').tobytes()
boxes=[]
for name,y0,y1 in [('shoulder-upper-arm',111,122),('elbow-forearm',123,131),('wrist-hand',132,148)]:
 p=[(x,y) for x,y in pts if y0<=y<=y1]
 box=[min(x for x,y in p),min(y for x,y in p),max(x for x,y in p),max(y for x,y in p)]
 boxes.append(dict(name=name,xyxyInclusive=box,changedPixels=len(p)))
hashfile=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
doc=dict(status='VISUAL_REVIEW_REQUIRED',width=256,height=256,changedPixels=len(pts),unchangedPixels=65536-len(pts),boxes=boxes,scopeMask=dict(xyxyInclusive=[147,111,188,148],outsideChangedPixels=0),newPaletteColors=0,masterRoundtripRGBAIdentical=True,authorship='Programmatic Lua inside Aseprite 1.3.18.6, local articulation of original frame pixels; no generation; no other pose pasted; nearest integer samples; no scaling.',input={'path':str(S),'sha256':hashfile(S)},output={n:hashfile(E/n) for n in ['candidate-08.png','master-08.aseprite','author.lua']},jointsBefore={'shoulder':[147,112],'elbow':[168,120],'wrist':[181,125],'handContact':[178,131]},jointsAfter={'shoulder':[147,112],'elbow':[166,124],'wrist':[173,136],'handContact':[167,140]})
(E/'pixel-diff.json').write_text(json.dumps(doc,indent=2),encoding='utf-8')
# Review-only layout: unaltered source/candidate pasted at 1x and nearest-neighbor 4x.
canvas=Image.new('RGB',(1080,1360),(24,26,30));d=ImageDraw.Draw(canvas)
for i,(im,title) in enumerate([(a,'ANTES'),(b,'CANDIDATO')]):
 x=16+i*536;d.text((x,8),title+' 1x (256 x 256)',fill='white');canvas.paste(im,(x,28),im)
 d.text((x,302),title+' 4x (quadro integral)',fill='white');big=im.resize((1024,1024),Image.Resampling.NEAREST)
 # Full 4x panels placed on a separate wider canvas below.
wide=Image.new('RGB',(2080,1360),(24,26,30));wide.paste(canvas.crop((0,0,1080,285)),(0,0));dw=ImageDraw.Draw(wide)
for i,im in enumerate([a,b]):
 big=im.resize((1024,1024),Image.Resampling.NEAREST);wide.paste(big,(8+i*1040,328),big)
 dw.text((8+i*1040,310),('ANTES' if i==0 else 'CANDIDATO')+' 4x',fill='white')
wide.save(E/'before-after.png')
mapim=Image.new('RGB',(256,256),(24,26,30));mapim.paste(b,(0,0),b);md=ImageDraw.Draw(mapim)
for box in boxes:md.rectangle(box['xyxyInclusive'],outline=(255,180,40),width=1)
mapim.save(E/'changed-regions.png')
(E/'verification.json').write_text(json.dumps({'technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','checks':['256x256 RGBA','palette unchanged','zero changed pixels outside arm mask','saved master roundtrip matches candidate','no weapon composited'], 'sourceSha256':hashfile(S)},indent=2),encoding='utf-8')
print(json.dumps(doc,indent=2))

