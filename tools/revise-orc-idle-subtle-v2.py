"""Apply imagegen chest corrections to frame 03 only; preserve every other frame."""
import hashlib, importlib.util, json, shutil, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT=Path('.').resolve()
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v): Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def module(name,file):
    s=importlib.util.spec_from_file_location(name,ROOT/'tools'/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
native=module('native','recover-native-sprite.py');extract=module('extract','extract-animation-sheet.py');editable=module('editable','write-animation-editable.py')
editor=read(ROOT/'characters/orc-front-locomotion-editor-verification-v1.json')
feedback='Walk está ótimo. Idle de "respiração", no quadro 3, parece que o peitoral expande muito, ficando exagerado, gostaria que fosse mais sutil, fora isso está muito bom'
summary=[]
for b in read(ROOT/'characters/orc-front-locomotion-batch-v1.json'):
    package=ROOT/'characters'/b['id'];folder=package/'source/animations-v1/Idle/front_r';revision=package/'source/idle-subtle-v2'
    old=revision/'previous-idle'
    if old.exists() and '--refine' not in sys.argv: raise ValueError('Immutable snapshot already exists; use --refine')
    if not old.exists(): shutil.copytree(folder,old)
    runtime=package/'sprites/Animations';before={p.relative_to(package).as_posix():sha(p) for p in runtime.rglob('*.png')}
    for i in range(4): before[f'sprites/Animations/Idle/idle_front_r_{i:02d}.png']=sha(old/f'idle_front_r_{i:02d}.png')
    review={'evidence':feedback,'scope':'Idle and Walk front_r only','Walk':{'status':'APPROVED_BY_CREATOR','frames':{p:h for p,h in before.items() if '/Walk/' in p},'editableSha256':sha(package/'source/animations-v1/Walk/front_r/walk_front_r.aseprite')},'Idle':{'status':'CHANGES_REQUESTED','frames':{p:h for p,h in before.items() if '/Idle/' in p},'requestedChange':'Reduce chest expansion of third frame only'}}
    write(package/'source/locomotion-front-v1/review.json',review)
    output=revision/'generated-native.png'
    native.recover(revision/'generated.png',output,100,48,ROOT/b['palette'],quiet=True)
    raw=np.array(Image.open(output).convert('RGBA'));original=np.array(Image.open(old/'idle_front_r_02.png').convert('RGBA'))
    dx=round(extract.head_x(original)-extract.head_x(raw));raw=np.roll(raw,dx,axis=1)
    # Native pixel finishing: target only upper torso, taper to unchanged neck/belt.
    # No runtime deformation, new motion, mirroring, or static-figure animation.
    result=original.copy();neutral=np.array(Image.open(old/'idle_front_r_00.png').convert('RGBA'))
    for y in range(47,74):
        taper=min((y-46)/6,(74-y)/8,1)
        ox=np.where(original[y,:,3]>0)[0];nx=np.where(neutral[y,:,3]>0)[0];rx=np.where(raw[y,:,3]>0)[0]
        left=round(ox.min()+taper*(max(ox.min(),nx.min()-1)-ox.min()))
        right=round(ox.max()+taper*(min(ox.max(),nx.max()+1)-ox.max()))
        # At peak, neutral silhouette plus at most one native pixel per side.
        result[y,24:104]=0
        source_row=Image.fromarray(raw[y:y+1,rx.min():rx.max()+1])
        result[y,left:right+1]=np.array(source_row.resize((right-left+1,1),Image.Resampling.NEAREST))[0]
    # Head, wrists, belt and lower body are from the original frame.
    target=folder/'idle_front_r_02.png';Image.fromarray(result).save(target)
    Image.fromarray(result).resize((512,512),Image.Resampling.NEAREST).save(folder/'idle_front_r_02-4x.png')
    changed=np.any(original!=result,axis=2);ys,xs=np.where(changed)
    assert len(xs)>0 and xs.min()>=24 and xs.max()<104 and ys.min()>=47 and ys.max()<74
    report=read(revision/'generated-native.json')
    report.update({'source':(revision/'generated.png').relative_to(ROOT).as_posix(),'output':target.relative_to(ROOT).as_posix(),'outputSha256':sha(target),'method':'image_gen chest edit + own-palette native grid finishing + local torso composition constrained to neutral silhouette plus one pixel per side','originalNative':(old/'idle_front_r_02.png').relative_to(ROOT).as_posix(),'originalNativeSha256':sha(old/'idle_front_r_02.png'),'neutralNative':(old/'idle_front_r_00.png').relative_to(ROOT).as_posix(),'neutralNativeSha256':sha(old/'idle_front_r_00.png'),'nativeHeadTranslationX':dx,'editRegion':[24,47,104,74],'changedPixels':len(xs),'artisticApproval':'PENDING_CREATOR_REVISED_IDLE_REVIEW'})
    write(folder/'idle_front_r_02.json',report)
    frames=[Image.open(folder/f'idle_front_r_{i:02d}.png').convert('RGBA') for i in range(4)]
    strip=Image.new('RGBA',(512,128))
    for i,im in enumerate(frames): strip.paste(im,(i*128,0))
    strip.save(folder/'native-strip.png');frames[0].save(folder/'preview.png',save_all=True,append_images=frames[1:],duration=240,loop=0,disposal=0,blend=0)
    clip=read(folder/'clip.json');clip.update({'revision':'idle-subtle-v2','mixedSourceFrames':{'02':'../../../idle-subtle-v2/generation.json'},'uniqueRgbaFrames':len({im.tobytes() for im in frames})});assert clip['uniqueRgbaFrames']==4;write(folder/'clip.json',clip)
    editable.write_clip(folder)
    subprocess.run(['node','src/cli.mjs','import','--id',b['id'],'--input',str(target),'--kind','sprite','--slot','Animations/Idle/idle_front_r_02.png','--provider','OpenAI image_gen + local native torso finishing','--model','image model not exposed','--force'],check=True,capture_output=True)
    assets=read(package/'assets.json');asset=next(a for a in reversed(assets) if a['file']=='sprites/Animations/Idle/idle_front_r_02.png' and a['sha256']==sha(target))
    asset.update({'processingReport':'source/animations-v1/Idle/front_r/idle_front_r_02.json','generationPromptFile':'source/idle-subtle-v2/correction.prompt.md','generationPromptSha256':sha(revision/'correction.prompt.md'),'artSource':'source/idle-subtle-v2/generated.png','artSourceSha256':sha(revision/'generated.png'),'artisticApproval':'PENDING_CREATOR_REVISED_IDLE_REVIEW'})
    write(package/'assets.json',assets)
    item=next(e for e in editor['clips'] if e['id']==b['id'] and e['state']=='Idle');ase=folder/'idle_front_r.aseprite';sheet=ROOT/item['editorSheet'];data=ROOT/item['editorData']
    subprocess.run([str(ROOT/'tmp/tools/libresprite/libresprite.exe'),'-b','--format','json-array','--data',str(data.relative_to(ROOT)),'--sheet-type','horizontal','--sheet',str(sheet.relative_to(ROOT)),str(ase.relative_to(ROOT))],check=True,capture_output=True)
    exported=Image.open(sheet).convert('RGBA');ed=read(data)
    for i,f in enumerate(ed['frames']):
        r=f['frame'];assert f['duration']==240 and exported.crop((r['x'],r['y'],r['x']+128,r['y']+128)).tobytes()==frames[i].tobytes()
    item['editableSha256']=sha(ase)
    changedFiles=[p for p,h in before.items() if sha(package/p)!=h];assert changedFiles==['sprites/Animations/Idle/idle_front_r_02.png'],changedFiles
    assert review['Walk']['editableSha256']==sha(package/'source/animations-v1/Walk/front_r/walk_front_r.aseprite')
    evidence={'id':b['id'],'modifiedFrame':'idle_front_r_02.png','changedRegion':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'changedPixels':len(xs),'unchangedOtherFrames':9,'walkApproval':'APPROVED_BY_CREATOR','idleApproval':'PENDING_CREATOR_REVISED_IDLE_REVIEW','editorRoundtrip':'4/4 RGBA and durations identical','newSha256':sha(target),'oldSha256':before[changedFiles[0]]}
    write(revision/'revision.json',evidence);summary.append(evidence)
write(ROOT/'characters/orc-front-locomotion-editor-verification-v1.json',editor)
write(ROOT/'characters/orc-idle-subtle-v2-validation.json',{'classes':summary,'summary':{'correctedFrames':7,'otherFramesUnchanged':63,'walkFramesApprovedAndUnchanged':42,'FAIL':0},'artisticApproval':'PENDING_CREATOR_REVISED_IDLE_REVIEW'})
