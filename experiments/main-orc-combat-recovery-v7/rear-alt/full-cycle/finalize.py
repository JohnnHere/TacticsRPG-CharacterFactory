from pathlib import Path
from PIL import Image
import json,hashlib,math,copy
E=Path('experiments/main-orc-combat-recovery-v7/rear-alt/full-cycle');plan=json.loads((E/'plan.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def eq(a,b):return sum(u!=v for u,v in zip(a.getdata(),b.getdata()))
def body(src,i):return Image.open(Path(src)/f'layers/body/{i:02}.png').convert('RGBA')
def luma(c):return .299*c[0]+.587*c[1]+.114*c[2] if c[3] else 0
# Left pauldron material ROI, in native coordinates.
roi=(35,25,61,53)
def stats(im):
 im=im.crop((64,64,192,192)).crop(roi);colors=list(im.getdata());return {'peakLuma':round(max(map(luma,colors)),3),'meanLumaIncludingAlpha':round(sum(map(luma,colors))/len(colors),3),'brightNeutralPixels145':sum(c[3]>0 and min(c[:3])>=140 and max(c[:3])-min(c[:3])<30 for c in colors)}
all_checks={};flash={};matrices={};allmetrics={}
for kind,cfg in plan['clips'].items():
 dst=Path(cfg['dest']);source=Path(f'characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-{kind.lower()}');old=json.loads((source/'clip.json').read_text());logs=json.loads((E/(kind.lower()+'-author-result.json')).read_text());dur=[f['durationMs']for f in cfg['frames']]
 clip={'schemaVersion':1,'revision':'main-orc-combat-recovery-v7-back-l-full-manual','checkpoint':'V7_BACK_L_FULL_MANUAL_READY','id':'basic.sword-slash'if kind=='Sword'else'basic.axe-chop','character':'orc-v1','identity':'Verde Warcraft','direction':'back_l','category':kind,'state':'Attack','frameCount':len(dur),'durationsMs':dur,'totalDurationMs':sum(dur),'visibleInterval':cfg['visibleInterval'],'canvas':[256,256],'nativeCanvas':[128,128],'bodyOffset':[64,64],'groundY':190,'nativeGroundY':126,'layerOrder':['weaponBack','body','weaponFront','handFront'],'oneShot':True,'loop':False,'runtimeImplemented':False,'technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','creatorApproval':'PENDING_CREATOR','eligibleForIntegration':False,'visibilityPolicy':'attack-only-v1','weaponDefinition':f'characters/orc-v1/source/combat-rescue-v5/combat/weapons/{kind}/weapon.json','sourceParentClip':(source/'clip.json').as_posix(),'sourceParentClipSha256':sha(source/'clip.json'),'provenance':{'authoring':'Programmatic manual pose construction inside Aseprite Lua; per-pose humerus/sleeve drawing and joint-measured same-view forearm/glove articulation; no generative calls or external raster edits','authorScript':(E/'author.lua').as_posix(),'authorScriptSha256':sha(E/'author.lua'),'plan':(E/'plan.json').as_posix(),'planSha256':sha(E/'plan.json'),'donorJointMeasurementUncertaintyPx':1,'newPixelLabCalls':0,'bodySources':'V6 attack-body frames 01..10 only; V6 Idle bookends 00/11 explicitly excluded','mastersSavedReopened':True,'rgbaAndTimingVerified':True},'frames':[]}
 for key,file in [('master','source/composite.aseprite'),('nativeMaster','source/native.aseprite'),('strip','native-strip.png'),('nativeStrip','native-strip.png'),('compositeStrip','composite-strip.png')]:clip[key]=(dst/file).as_posix();clip[key+'Sha256']=sha(dst/file)
 checks=[];metrics=[];rois=[]
 for i,f in enumerate(cfg['frames']):
  sf={'index':i,'durationMs':f['durationMs'],'phase':f['phase'],'weaponVisible':f['weaponVisible'],'rightGrip':[q+64 for q in f['palm']]if f['weaponVisible']else None,'rotationDeg':f['weaponAngleDeg'],'png':(dst/f'frames/{i:02}.png').as_posix(),'nativePng':(dst/f'native/{i:02}.png').as_posix(),'layers':{},'sourceBody':f['base'],'sourceBodySha256':sha(f['base']),'manualJointsNative':{k:f[k]for k in ['shoulder','elbow','wrist','palm']},'donor':f['donor'],'donorAxialProjection':logs['frames'][i]['axialProjectionScale'],'preservedManualKey':f['preserveKey'],'provenance':'Exact four-layer selected key'if f['preserveKey']else'V6 attack torso/legs; old active arm fully removed; manual proximal arm and articulated same-view donor; surgical detached debris cleanup'}
  sf['sha256']=sha(sf['png']);sf['nativeSha256']=sha(sf['nativePng']);ims={}
  for n in clip['layerOrder']:
   p=dst/f'layers/{n}/{i:02}.png';sf['layers'][n]={'png':p.as_posix(),'sha256':sha(p)};ims[n]=Image.open(p).convert('RGBA')
  comp=Image.new('RGBA',(256,256))
  for im in ims.values():comp=Image.alpha_composite(comp,im)
  native=Image.open(sf['nativePng']).convert('RGBA');render=Image.open(sf['png']).convert('RGBA');assert eq(comp,render)==0;assert eq(ims['body'].crop((64,64,192,192)),native)==0
  weapon=Image.alpha_composite(ims['weaponBack'],ims['weaponFront']);below=sum(1 for y in range(191,256)for x in range(256)if weapon.getpixel((x,y))[3]);assert below==0,(kind,i,below)
  if not sf['weaponVisible']:assert all(ims[n].getbbox()is None for n in ['weaponBack','weaponFront','handFront'])
  hand=ims['handFront'];overlap=sum(1 for y in range(256)for x in range(256)if hand.getpixel((x,y))[3]and weapon.getpixel((x,y))[3]);assert overlap>0 or not sf['weaponVisible'],(kind,i)
  # Exact selected-key raster identity, independent of changed playback duration.
  keydiff=0
  if f['preserveKey']:
   for n in clip['layerOrder']:keydiff+=eq(ims[n],Image.open(Path('characters/orc-v1/source/combat-recovery-v7/rear-alt')/f['preserveKey']/f'layers/{n}.png').convert('RGBA'))
   assert keydiff==0
  s,e,w,p=[f[k]for k in ['shoulder','elbow','wrist','palm']];u=[s[z]-e[z]for z in range(2)];v=[w[z]-e[z]for z in range(2)];ul=math.dist(s,e);fl=math.dist(e,w);angle=math.degrees(math.acos(max(-1,min(1,sum(u[z]*v[z]for z in range(2))/(ul*fl)))))
  checks.append({'index':i,'alphaOverMismatchPixels':0,'nativeBodyMismatchPixels':0,'weaponBelowGround':0,'handOverItemPixels':overlap,'preservedKeyMismatchPixels':keydiff})
  metrics.append({'index':i,'phase':f['phase'],'durationMs':f['durationMs'],'joints':sf['manualJointsNative'],'humerusPx':round(ul,3),'forearmPx':round(fl,3),'elbowInteriorDeg':round(angle,3),'donor':f['donor'],'axialProjection':sf['donorAxialProjection'],'weaponAngleDeg':f['weaponAngleDeg']})
  rois.append(stats(ims['body']));clip['frames'].append(sf)
 # Master exports and strips are declared from real files, not aliases.
 assert Image.open(clip['nativeStrip']).size==(128*len(dur),128);assert Image.open(clip['compositeStrip']).size==(256*len(dur),256)
 first,last=body(dst,0),body(dst,len(dur)-1);assert eq(first,last)==0
 old0,old1,old10,old11=[body(source,z)for z in [0,1,10,11]]
 idle=json.loads(Path('characters/orc-v1/source/complete-v1/back_l/Idle/clip.json').read_text());idlepng=Path(idle['frames'][0]['png'])
 oldTop=[]
 for y in range(roi[1]+64,roi[3]+64):
  for x in range(roi[0]+64,roi[2]+64):
   c0=old0.getpixel((x,y));c1=old1.getpixel((x,y));delta=luma(c0)-luma(c1)
   if delta>=30 and c0[3]:oldTop.append({'native':[x-64,y-64],'rgbaBefore':list(c0),'attackAdjacent':list(c1),'lumaJump':round(delta,3)})
 flash[kind]={'roiNative':roi,'oldBookendEqualsIdleBytes':sha(source/'layers/body/00.png')==sha(idlepng),'oldBookendEqualsIdleDecodedPixels':eq(old0,Image.open(idlepng).convert('RGBA'))==0,'oldFrame00':stats(old0),'oldFrame01':stats(old1),'oldFrame10':stats(old10),'oldFrame11':stats(old11),'oldPositiveJumpAtLeast30':sorted(oldTop,key=lambda a:-a['lumaJump']),'newPerFrame':rois,'newLastToFirstBodyMismatchPixels':0,'newFirstToPreparationShoulderMismatchPixels':eq(first.crop((roi[0]+64,roi[1]+64,roi[2]+64,roi[3]+64)),body(dst,1).crop((roi[0]+64,roi[1]+64,roi[2]+64,roi[3]+64))),'newLastPreviousShoulderMismatchPixels':eq(last.crop((roi[0]+64,roi[1]+64,roi[2]+64,roi[3]+64)),body(dst,len(dur)-2).crop((roi[0]+64,roi[1]+64,roi[2]+64,roi[3]+64))),'newBookendEqualsOldIdle':eq(first,old0)==0}
 assert flash[kind]['newFirstToPreparationShoulderMismatchPixels']==0 and flash[kind]['newLastPreviousShoulderMismatchPixels']==0 and not flash[kind]['newBookendEqualsOldIdle']
 clip['bookendPolicy']={'sourceAttackFrame':1,'idleBodies00And11Excluded':True,'lastToFirstBodyMismatchPixels':0,'shoulderAtEntryAndExitUnchanged':True,'diagnostic':(E/'bookend-flash-audit.json').as_posix()}
 (dst/'clip.json').write_text(json.dumps(clip,indent=2),encoding='utf-8');all_checks[kind]=checks;allmetrics[kind]=metrics
(E/'raster-verification.json').write_text(json.dumps({'checkpoint':'V7_BACK_L_FULL_MANUAL_READY','clips':all_checks,'newPixelLabCalls':0},indent=2));(E/'bookend-flash-audit.json').write_text(json.dumps(flash,indent=2));(E/'joint-metrics.json').write_text(json.dumps(allmetrics,indent=2))
protected=json.loads((E/'protected-input-hashes.json').read_text());assert all(sha(q)==h for q,h in protected.items());(E/'preservation.json').write_text(json.dumps({'filesVerifiedUnchanged':len(protected),'historicalManualKeysPreserved':True,'protectedInputManifest':(E/'protected-input-hashes.json').as_posix()},indent=2))
print('30 frames verified; protected files',len(protected))
for k,f in flash.items():print(k,'old peak 00/01',f['oldFrame00']['peakLuma'],f['oldFrame01']['peakLuma'],'old bright',f['oldFrame00']['brightNeutralPixels145'],f['oldFrame01']['brightNeutralPixels145'],'new boundary zero',f['newLastToFirstBodyMismatchPixels'])
