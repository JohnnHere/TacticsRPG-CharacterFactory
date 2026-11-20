"""Metadata/provenance for Aseprite-authored rear-Sword and front F02 exports."""
from pathlib import Path
import copy, hashlib, json
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,obj): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def rel(p): return p.relative_to(ROOT).as_posix()

# The Lua authoring script refines each handoff estimate to the nearest opaque
# body pixel in the local arm band. Recompute those coordinates for metadata.
raw_grips=[[164,125],[164,125],[164,125],[178,117],[174,108],[157,94],[145,101],[145,106],[146,106],[150,105],[154,110],[150,133],[150,133]]
angles=[0,0,45,45,15,345,315,270,270,270,135,0,0]
flip_bits=[False,False,False,False,False,False,False,False,True,True,False,False,False]
visible=[False,False,True,True,True,True,True,True,True,True,True,False,False]
behind=[False,False,False,False,True,True,True,True,False,False,False,False,False]
phases=['rest','body-preparation','establish-grip','lift','windup','windup-high','windup-hold','release','slash','follow-through','recovery','action-complete','return-unarmed']
sroot=ROOT/'characters/orc-v1/source'
adir=sroot/'rear-recovery-v2/back_r/Sword/Attack'
clip=read(sroot/'complete-v1/back_r/Sword/Attack/clip.json')
for i,fr in enumerate(clip['frames']):
    old=sroot/'complete-v1/back_r/Sword/Attack/layers/body'/f'{i:02d}.png'
    im=Image.open(old).convert('RGBA'); tx,ty=raw_grips[i]
    candidates=[]
    for y in range(max(64,ty-4),min(170,ty+4)+1):
        for x in range(max(0,tx-4),min(255,tx+4)+1):
            if im.getpixel((x,y))[3]>=128: candidates.append(((x-tx)**2+(y-ty)**2,x,y))
    if not candidates: raise RuntimeError(f'no grip body pixel for {i}')
    _,gx,gy=min(candidates)
    fr['png']=rel(adir/f'{i:02d}.png'); fr['sha256']=sha(adir/f'{i:02d}.png')
    fr['nativePng']=rel(adir/'native'/f'{i:02d}.png'); fr['nativeSha256']=sha(adir/'native'/f'{i:02d}.png')
    fr['phase']=phases[i]; fr['weaponVisible']=visible[i]; fr['rightGrip']=[gx,gy]; fr['rotationDeg']=angles[i]
    fr['flipBit']=flip_bits[i]
    fr['weaponBehindBody']=behind[i]
    for layer in ('weaponBack','body','weaponFront','handFront'):
        p=adir/'layers'/layer/f'{i:02d}.png'
        fr.setdefault('layers',{})[layer]={'png':rel(p),'sha256':sha(p)}
    fr.setdefault('durationMs',clip['durationsMs'][i])
clip['revision']='main-orc-rear-recovery-v2-representative'
clip['master']= 'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-attack.aseprite'
clip['masterSha256']=sha(ROOT/clip['master'])
clip['bodyMaster']='characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-body.aseprite'
clip['bodyMasterSha256']=sha(ROOT/clip['bodyMaster'])
clip['handMaster']='characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-hand-front.aseprite'
clip['handMasterSha256']=sha(ROOT/clip['handMaster'])
clip['nativeMaster']='characters/orc-v1/source/aseprite/rear-recovery-v2/native/sword-back_r.aseprite'
clip['nativeMasterSha256']=sha(ROOT/clip['nativeMaster'])
clip['strip']=rel(adir/'native-strip.png'); clip['stripSha256']=sha(adir/'native-strip.png')
clip['layerOrder']=['weaponBack','body','weaponFront','handFront']
clip['visibleInterval']=[2,10]; clip['weaponVisible']=True; clip['weaponOverlay']=True
clip['contactEvent']={'frame':8,'timeMs':360,'status':'CANDIDATE_VISUAL_ONLY','appliesDamage':False}
clip['technicalStatus']='TECHNICALLY_COMPLETE'; clip['artisticStatus']='ARTISTIC_REVISION_REQUIRED'; clip['artisticApproval']='PENDING_CREATOR'
write(adir/'clip.json',clip)

for direction in ('front_r','front_l'):
    adir=sroot/f'rear-recovery-v2/{direction}/Unarmed'
    clip=read(sroot/f'complete-v1/{direction}/Unarmed/clip.json')
    clip['revision']='main-orc-rear-recovery-v2-F02-surgical'
    clip['master']=f'characters/orc-v1/source/aseprite/rear-recovery-v2/composite/{direction}/unarmed-attack.aseprite'
    clip['masterSha256']=sha(ROOT/clip['master'])
    clip['nativeMaster']=f'characters/orc-v1/source/aseprite/rear-recovery-v2/native/unarmed-{direction}.aseprite'
    clip['nativeMasterSha256']=sha(ROOT/clip['nativeMaster'])
    clip['strip']=f'characters/orc-v1/source/rear-recovery-v2/{direction}/Unarmed/native-strip.png'
    clip['stripSha256']=sha(ROOT/clip['strip'])
    for i,fr in enumerate(clip['frames']):
        p=adir/f'{i:02d}.png'; n=adir/'native'/f'{i:02d}.png'
        fr['png']=rel(p); fr['sha256']=sha(p); fr['nativePng']=rel(n); fr['nativeSha256']=sha(n)
    clip['technicalStatus']='TECHNICALLY_COMPLETE'; clip['artisticStatus']='ARTISTIC_REVISION_REQUIRED'; clip['artisticApproval']='PENDING_CREATOR'
    write(adir/'clip.json',clip)
print('Wrote candidate metadata for 1 layered rear Sword and 2 F02 Unarmed fixes.')
