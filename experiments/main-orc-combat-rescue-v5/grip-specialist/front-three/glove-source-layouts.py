from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/front-three');snap=json.loads((E/'input-snapshot.json').read_text());allclips={k:json.loads(Path(p).read_text())for k,p in snap['clips'].items()}
rough={
 'front_l/Sword':{2:(152,130),3:(165,119),4:(157,100),5:(157,89),6:(100,114),7:(97,132),8:(96,148),9:(121,147),10:(145,150)},
 'front_r/Axe':{2:(103,130),3:(90,119),4:(98,100),5:(160,124),6:(164,147),7:(147,150),8:(134,147)},
 'front_l/Axe':{2:(152,130),3:(165,119),4:(157,100),5:(95,124),6:(91,147),7:(108,150),8:(121,147)}}
bboxes={}
for key,c in allclips.items():
 idxs=list(rough[key]);rows=(len(idxs)+2)//3;o=Image.new('RGB',(1152,rows*420),(43,44,49));d=ImageDraw.Draw(o);bboxes[key]=[]
 for n,i in enumerate(idxs):
  body=Image.open(c['frames'][i]['layers']['body']['png']).convert('RGBA');gx,gy=rough[key][i];box=(gx-24,gy-24,gx+24,gy+24);im=body.crop(box).resize((384,384),Image.Resampling.NEAREST);x=n%3*384;y=n//3*420;o.paste(im,(x,y+30),im);d.text((x+4,y+6),f'{key} F{i:02} crop x{box[0]}..{box[2]} y{box[1]}..{box[3]}',fill='white')
  a=np.array(body);yy,xx=np.where(a[:,:,3]>0);outside=a.copy();outside[64:192,64:192]=0;bboxes[key].append({'frame':i,'bodyBbox':[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],'opaqueBodyOutsideCentral128':int((outside[:,:,3]>0).sum())})
 o.save(E/(key.replace('/','-')+'-gloves-source.png'))
(E/'body-bounds.json').write_text(json.dumps(bboxes,indent=2)+'\n');print(json.dumps(bboxes,indent=2))
