"""Chronologically select six separately authored poses; never mirror/warp.
The original row repeated a leading leg. Its first three poses in contact /
weight / passing order are paired with the guided opposite-leg half-cycle.
Only RGBA cropping and integer placement occur before grid reconstruction.
"""
import hashlib,json
from pathlib import Path
import cv2,numpy as np
from PIL import Image

folder=Path(__file__).parent
out=folder/"curated-v2"
out.mkdir(exist_ok=True)
selected=[];records=[]
for name,expected,indices in [("sheet.png",6,[2,0,1]),("opposite-guided.png",3,[0,1,2])]:
    data=(folder/name).read_bytes()
    im=np.array(Image.open(folder/name).convert("RGBA"))
    mask=(im[:,:,3]>=160).astype(np.uint8)
    n,lab,stats,_=cv2.connectedComponentsWithStats(mask,8)
    maxarea=stats[1:,cv2.CC_STAT_AREA].max()
    ids=sorted([i for i in range(1,n) if stats[i,cv2.CC_STAT_AREA]>=maxarea*.15],key=lambda i:stats[i,0])
    if len(ids)!=expected:raise ValueError("Unexpected authored figure count")
    for i in indices:
        k=ids[i];x,y,w,h,_=map(int,stats[k]);crop=im[y:y+h,x:x+w].copy()
        crop[lab[y:y+h,x:x+w]!=k]=0
        selected.append(Image.fromarray(crop))
        records.append({"source":name,"sourceSha256":hashlib.sha256(data).hexdigest(),"figureIndex":i,"box":[x,y,x+w,y+h]})
w=max(i.width for i in selected)+100;h=max(i.height for i in selected)+60
sheet=Image.new("RGBA",(w*6,h))
for index,im in enumerate(selected):sheet.paste(im,(index*w+(w-im.width)//2,h-30-im.height))
sheet.save(out/"sheet.png")
(out/"curation.json").write_text(json.dumps({"state":"Walk","direction":"front_r","method":"Chronological RGBA pose selection; no mirroring or scaling", "frames":records,"rejected":["original complete cycle repeated leading leg","opposite-half.png failed leg swap; not used"]},indent=2),encoding="utf-8")
prompts="# Curated six-frame Walk front_r source\n\nNot one generation: exact prompts for the two image_gen calls used below. Model not exposed.\nSelection/unchanged pixel boxes are recorded in curation.json. No guide pixels are promoted as final art.\n\n"+(folder/"sheet.prompt.md").read_text(encoding="utf-8")+"\n\n---\n\n"+(folder/"opposite-guided.prompt.md").read_text(encoding="utf-8")
(out/"sheet.prompt.md").write_text(prompts,encoding="utf-8")
print(f"Curated six-frame source {sheet.size}: {out}")
