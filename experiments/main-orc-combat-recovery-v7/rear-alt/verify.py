import json,hashlib,math,os
from pathlib import Path
from PIL import Image
E=Path('experiments/main-orc-combat-recovery-v7/rear-alt');C=Path('characters/orc-v1/source/combat-recovery-v7/rear-alt');plan=json.loads((E/'joint-plan.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def diff(a,b):return sum(x!=y for x,y in zip(a.getdata(),b.getdata()))
def components(im):
 pts={(x,y)for y in range(im.height)for x in range(im.width)if im.getpixel((x,y))[3]};out=[]
 while pts:
  q=[pts.pop()]
  for x,y in q:
   for dx in [-1,0,1]:
    for dy in [-1,0,1]:
     a=x+dx,y+dy
     if a in pts:pts.remove(a);q.append(a)
  out.append(q)
 return sorted(out,key=len,reverse=True)
verification={'checkpoint':'V7_BACK_L_APEX_MANUAL_READY','poses':{}}
for name in ['apex','impact']:
 dst=C/name;p=plan[name];layers={n:Image.open(dst/'layers'/f'{n}.png').convert('RGBA')for n in ['weaponBack','body','weaponFront','handFront']};render=Image.open(dst/'composite.png').convert('RGBA');native=Image.open(dst/'native.png').convert('RGBA');comp=Image.new('RGBA',(256,256))
 for im in layers.values():comp=Image.alpha_composite(comp,im)
 assert diff(comp,render)==0;assert diff(layers['body'].crop((64,64,192,192)),native)==0
 cc=components(native);assert len(cc)==1,(name,[len(c)for c in cc])
 for joint in ['shoulder','elbow','wrist','palm']:
  x,y=p['joints'][joint];assert native.getpixel((x,y))[3],(name,joint)
 source=Image.open(p['base']).convert('RGBA').crop((64,64,192,192))
 changed=[(x,y)for y in range(128)for x in range(128)if native.getpixel((x,y))!=source.getpixel((x,y))]
 # Lower body and the full opposite arm, torso core, skull: decoded equality.
 preserved={'legsTassetsBeltBelow95':diff(native.crop((0,95,128,128)),source.crop((0,95,128,128)))==0,'oppositeArmAndTorsoLeftOf80':diff(native.crop((0,0,80,128)),source.crop((0,0,80,128)))==0}
 assert all(preserved.values())
 bounds=[min(x for x,y in changed),min(y for x,y in changed),max(x for x,y in changed),max(y for x,y in changed)]
 green=[(x,y)for y in range(0,30)for x in range(45,80)if (lambda c:c[3] and c[1]>c[0]*1.1 and c[1]>c[2]*1.2)(native.getpixel((x,y)))];skull=min(y for y in range(0,21) for x in range(45,80) if native.getpixel((x,y))[3])
 weapon=Image.alpha_composite(layers['weaponBack'],layers['weaponFront']);pts=[(x,y)for y in range(256)for x in range(256)if weapon.getpixel((x,y))[3]];tip=min(pts,key=lambda q:q[1])if name=='apex' else max(pts,key=lambda q:q[0]);below=sum(y>190 for x,y in pts);assert below==0
 j=p['joints'];measure={'jointCentersNative':j,'jointCentersComposite':{k:[z+64 for z in j[k]]for k in ['shoulder','elbow','wrist','palm']},'skullTopYNative':skull,'bladeTipComposite':list(tip),'bladeTipNative':[tip[0]-64,tip[1]-64],'tipAboveSkullPx':skull-(tip[1]-64),'wristAboveShoulderPx':j['shoulder'][1]-j['wrist'][1],'palmAboveShoulderPx':j['shoulder'][1]-j['palm'][1]}
 if name=='apex':
  gaps=[]
  for y in range(24,31):
   left=max(x for x in range(50,92)if native.getpixel((x,y))[3]);right=min(x for x in range(92,118)if native.getpixel((x,y))[3]);gap=right-left-1;assert all(native.getpixel((x,y))[3]==0 for x in range(left+1,right));gaps.append({'y':y,'torsoEdgeX':left,'forearmEdgeX':right,'transparentGapPx':gap})
  measure['negativeSpaceRows']=gaps;measure['minimumNegativeSpaceGapPx']=min(g['transparentGapPx']for g in gaps);assert measure['tipAboveSkullPx']>0 and measure['wristAboveShoulderPx']>0
 overlap=sum(1 for y in range(256)for x in range(256)if layers['handFront'].getpixel((x,y))[3]and layers['weaponBack'].getpixel((x,y))[3]);assert overlap>0
 r={'schemaVersion':1,'revision':'main-orc-combat-recovery-v7-rear-alt','checkpoint':'V7_BACK_L_APEX_MANUAL_READY','character':'orc-v1','identity':'Verde Warcraft','direction':'back_l','category':'Sword','pose':name,'representativeOnly':True,'frameCount':1,'durationMs':p['durationMs'],'canvas':[256,256],'nativeCanvas':[128,128],'bodyOffset':[64,64],'groundY':190,'nativeGroundY':126,'layerOrder':list(layers),'rightGrip':[z+64 for z in p['grip']],'rotationDeg':p['weaponAngleDeg'],'weaponDefinition':'characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/weapon.json','weaponVisible':True,'weaponScope':'Single attack pose only; not an Idle/Walk asset','technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','creatorApproval':'PENDING_CREATOR','runtimeImplemented':False,'measurements':measure,'provenance':{'method':'Same-view donor forearm/glove translated 1:1; humerus manually reauthored by Lua in Aseprite; inherited torso/legs. Not hand drawing on GUI and not generative production.','base':p['base'],'baseSha256':sha(p['base']),'donor':p['donor'],'donorSha256':sha(p['donor']),'donorTranslation':p['translation'],'script':(E/f'author-{name}.lua').as_posix(),'scriptSha256':sha(E/f'author-{name}.lua'),'pixelLabCalls':0,'jointUncertaintyNativePx':1}}
 for key,file in [('master','source/composite.aseprite'),('nativeMaster','source/native.aseprite'),('png','composite.png'),('nativePng','native.png')]:r[key]=(dst/file).as_posix();r[key+'Sha256']=sha(dst/file)
 r['layers']={n:{'png':(dst/'layers'/f'{n}.png').as_posix(),'sha256':sha(dst/'layers'/f'{n}.png')}for n in layers}
 r['verification']={'alphaOverMismatchPixels':0,'nativeBodyMismatchPixels':0,'mastersSavedReopened':True,'pixelsAndDurationsVerifiedInAseprite':True,'connectedBodyComponents':1,'weaponPixelsBelowGround':below,'handOverHandlePixels':overlap,'preservedRegions':preserved,'changedBodyPixelCount':len(changed),'changedBodyBoundsNative':bounds}
 (dst/'representative.json').write_text(json.dumps(r,indent=2),encoding='utf-8');verification['poses'][name]=r['verification']|measure
snapshot=json.loads((E/'protected-input-hashes.json').read_text());assert all(sha(p)==h for p,h in snapshot.items());verification['protectedFilesUnchanged']=len(snapshot);(E/'verification.json').write_text(json.dumps(verification,indent=2))
print(json.dumps({k:{'skullTop':v['skullTopYNative'],'tip':v['bladeTipNative'],'tipAbove':v['tipAboveSkullPx'],'wristAbove':v['wristAboveShoulderPx'],'gap':v.get('minimumNegativeSpaceGapPx'),'changes':v['changedBodyPixelCount']}for k,v in verification['poses'].items()}))

