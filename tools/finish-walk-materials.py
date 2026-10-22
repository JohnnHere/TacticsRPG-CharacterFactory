"""Native material finishing on authored Walk frames, not motion synthesis.

Preserves every alpha/pose pixel and all body/face/arm asymmetries. Rough rear
knee placeholders become leather; front metal gets upper-left facets. Every
changed RGB pixel is recorded, and previous native frames are preserved.
"""
import hashlib,json,sys
from pathlib import Path
import cv2,numpy as np
from PIL import Image

root=Path("characters/orc-01/source/animations-v1/Walk")
for direction in ["front_l","back_r","back_l"]:
    folder=root/direction;backup=folder/"before-material-finishing";backup.mkdir(exist_ok=True)
    edits=[];frames=[]
    for index in range(6):
        target=folder/f"walk_{direction}_{index:02d}.png"
        old=target.read_bytes();archive=backup/target.name
        if archive.exists():
            if '--revise' not in sys.argv:raise ValueError("Finishing already applied; use stored patches/review version")
            old=archive.read_bytes()
        else:archive.write_bytes(old)
        arr=np.array(Image.open(archive).convert("RGBA"));original=arr.copy()
        rgb=arr[:,:,:3].astype(int);yy,xx=np.indices(arr.shape[:2])
        rear=direction.startswith("back")
        mask=((abs(rgb[:,:,0]-rgb[:,:,1])<(32 if rear else 22))&(abs(rgb[:,:,1]-rgb[:,:,2])<(36 if rear else 26))&(rgb[:,:,0]>80)&(rgb[:,:,0]<(255 if rear else 200))&(arr[:,:,3]>0)&(yy>=91)&(yy<112)&(xx>45)&(xx<83)).astype(np.uint8)
        count,labels,stats,_=cv2.connectedComponentsWithStats(mask,8)
        for c in range(1,count):
            x,y,w,h,area=map(int,stats[c])
            if area<8:continue
            for py,px in zip(*np.where(labels==c)):
                u=(px-x)/max(w-1,1);v=(py-y)/max(h-1,1)
                if direction.startswith("back"):
                    color=(173,97,55) if v<.23 else ((110,58,35) if u>.65 or v>.7 else (136,72,41))
                else:
                    color=(205,182,156) if v<.3 and u<.6 else ((84,78,80) if v>.7 else tuple(arr[py,px,:3]))
                arr[py,px,:3]=color
        changed=np.any(arr!=original,axis=2)
        patch=[{"x":int(x),"y":int(y),"before":original[y,x,:3].tolist(),"after":arr[y,x,:3].tolist()} for y,x in zip(*np.where(changed))]
        assert np.array_equal(arr[:,:,3],original[:,:,3])
        Image.fromarray(arr).save(target)
        Image.fromarray(arr).resize((512,512),Image.Resampling.NEAREST).save(target.with_name(target.stem+"-4x.png"))
        report_path=target.with_suffix(".json");report=json.loads(report_path.read_text(encoding="utf-8"))
        report["outputSha256"]=hashlib.sha256(target.read_bytes()).hexdigest()
        report["nativeMaterialFinishing"]={"beforeSha256":hashlib.sha256(old).hexdigest(),"method":"rear leather palette / front upper-left metal facets, RGB-only native finishing","pixelPatch":patch}
        report_path.write_text(json.dumps(report,indent=2),encoding="utf-8")
        edits.append({"frame":target.name,"changedRgbPixels":len(patch),"alphaChanged":False})
        frames.append(Image.fromarray(arr))
    strip=Image.new("RGBA",(768,128))
    for i,frame in enumerate(frames):strip.paste(frame,(i*128,0))
    strip.save(folder/"native-strip.png")
    frames[0].save(folder/"preview.png",save_all=True,append_images=frames[1:],duration=73,loop=0,disposal=0,blend=0)
    (folder/"material-finishing.json").write_text(json.dumps({"direction":direction,"sourceMotionUnchanged":True,"frames":edits},indent=2),encoding="utf-8")
    print(direction,edits)
