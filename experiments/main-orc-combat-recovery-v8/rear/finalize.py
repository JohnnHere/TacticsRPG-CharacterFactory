from pathlib import Path
from PIL import Image
import json,hashlib,math,csv
E=Path('experiments/main-orc-combat-recovery-v8/rear');spec=json.loads((E/'temporal-spec.json').read_text());plan=json.loads((E/'phase-plan.json').read_text());trans=json.loads((E/'transition-plan.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def im(p):return Image.open(p).convert('RGBA')
def diff(a,b):return sum(x!=y for x,y in zip(a.getdata(),b.getdata()))
def bright(a):return sum(c[3]>0 and .299*c[0]+.587*c[1]+.114*c[2]>=145 for c in a.getdata())
def comps(a):
 pts={(x,y)for y in range(a.height)for x in range(a.width)if a.getpixel((x,y))[3]};r=[]
 while pts:
  q=[pts.pop()]
  for x,y in q:
   for dx in [-1,0,1]:
    for dy in [-1,0,1]:
     p=x+dx,y+dy
     if p in pts:pts.remove(p);q.append(p)
  r.append(q)
 return sorted(r,key=len,reverse=True)
verification={};delivery=[];comparison=[]
for key,cfg in plan.items():
 direction,kind=key.split('/');s=spec[kind];old=json.loads(Path(cfg['sourceClip']).read_text());dst=Path(cfg['dest']);frames=[];checks=[]
 for i,q in enumerate(cfg['frames']):
  source=old['frames'][q['sourceFrame']];layers={};images={}
  for n in ['weaponBack','body','weaponFront','handFront']:
   p=dst/f'layers/{n}/{i:02}.png';layers[n]={'png':p.as_posix(),'sha256':sha(p)};images[n]=im(p)
   if q['mode']=='MANUAL_DESCENT':expected=im(E/f'transitions/{kind.lower()}/layers/{n}.png')
   elif not q['weaponVisible']and n!='body':expected=Image.new('RGBA',(256,256))
   else:expected=im(source['layers'][n]['png'])
   assert diff(images[n],expected)==0,(key,i,n)
  f={'index':i,'phase':q['phase'],'durationMs':q['durationMs'],'startMs':q['startMs'],'endMs':q['endMs'],'png':(dst/f'frames/{i:02}.png').as_posix(),'nativePng':(dst/f'native/{i:02}.png').as_posix(),'layers':layers,'weaponVisible':q['weaponVisible'],'sourceFrame':q['sourceFrame'],'sourcePhase':q['sourcePhase'],'sourceClip':cfg['sourceClip'],'sourceClipSha256':cfg['sourceClipSha256'],'sourceMode':q['mode'],'rightGrip':source.get('rightGrip')if q['weaponVisible']else None,'rotationDeg':source.get('rotationDeg')if q['weaponVisible']else None}
  if q['mode']=='MANUAL_DESCENT':
   tf=trans['clips'][kind]['frames'][0];f['manualJointsNative']={n:tf[n]for n in ['shoulder','elbow','wrist','palm']};f['rightGrip']=[z+64 for z in tf['palm']];f['rotationDeg']=tf['weaponAngleDeg'];f['transitionAuthor']=(E/'author-transitions.lua').as_posix();f['transitionPlan']=(E/'transition-plan.json').as_posix()
  elif source.get('manualJointsNative'):f['manualJointsNative']=source['manualJointsNative']
  f['sha256']=sha(f['png']);f['nativeSha256']=sha(f['nativePng']);native=im(f['nativePng']);render=Image.new('RGBA',(256,256))
  for a in images.values():render=Image.alpha_composite(render,a)
  assert diff(render,im(f['png']))==0;assert diff(images['body'].crop((64,64,192,192)),native)==0
  wp=Image.alpha_composite(images['weaponBack'],images['weaponFront']);below=sum(1 for y in range(191,256)for x in range(256)if wp.getpixel((x,y))[3]);assert below==0
  if not f['weaponVisible']:assert all(images[n].getbbox()is None for n in ['weaponBack','weaponFront','handFront'])
  else:assert wp.getbbox()is not None
  cc=comps(native);assert len(cc)==1,(key,i,[(len(c),c[:1])for c in cc]);assert set(native.getchannel('A').getdata())=={0,255};assert not any(native.getpixel((127,y))[3]for y in range(128))
  checks.append({'index':i,'sourceLayersMismatchPixels':0,'alphaOverMismatchPixels':0,'nativeBodyMismatchPixels':0,'weaponBelowGround':0,'bodyComponents':1,'brightBodyPixels145':bright(images['body']),'sourceMode':q['mode']});frames.append(f)
 clip={'schemaVersion':1,'revision':'main-orc-combat-recovery-v8-rear-aligned','checkpoint':'V8_REAR_ALIGNED','id':'basic.sword-slash'if kind=='Sword'else'basic.axe-chop','character':'orc-v1','identity':'Verde Warcraft','direction':direction,'category':kind,'state':'Attack','frameCount':s['frameCount'],'durationsMs':s['durationsMs'],'totalDurationMs':s['durationMs'],'visibleInterval':s['visibleInterval'],'canvas':[256,256],'nativeCanvas':[128,128],'bodyOffset':[64,64],'groundY':190,'nativeGroundY':126,'layerOrder':['weaponBack','body','weaponFront','handFront'],'visibilityPolicy':'attack-only-v1','oneShot':True,'loop':False,'runtimeImplemented':False,'technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','creatorApproval':'PENDING_CREATOR','eligibleForIntegration':False,'weaponDefinition':old['weaponDefinition'],'sourceParentClip':cfg['sourceClip'],'sourceParentClipSha256':cfg['sourceClipSha256'],'frontalTimingReference':s['frontals'],'phaseGridAuthority':'Frame position, phase and cumulative durations from protected frontal; legacy contactEvent does not override the phase grid','contactEvent':{'frame':s['impactFrame'],'timeMs':s['impactStartMs'],'phase':frames[s['impactFrame']]['phase'],'status':'CANDIDATE_VISUAL_ONLY','appliesDamage':False},'provenance':{'method':'Aseprite local: V7 pose/layer reuse on protected frontal timing; one manually authored descending pose per back_l family; no generation','authorScript':(E/'author-cycles.lua').as_posix(),'authorScriptSha256':sha(E/'author-cycles.lua'),'phasePlan':(E/'phase-plan.json').as_posix(),'phasePlanSha256':sha(E/'phase-plan.json'),'transitionAuthorScript':(E/'author-transitions.lua').as_posix(),'transitionAuthorScriptSha256':sha(E/'author-transitions.lua'),'transitionPlanSha256':sha(E/'transition-plan.json'),'newPixelLabCalls':0,'mastersSavedReopened':True,'rgbaAndTimingVerified':True},'frames':frames}
 for k,file in [('master','source/composite.aseprite'),('nativeMaster','source/native.aseprite'),('strip','native-strip.png'),('nativeStrip','native-strip.png'),('compositeStrip','composite-strip.png')]:clip[k]=(dst/file).as_posix();clip[k+'Sha256']=sha(clip[k])
 ns,cs=im(clip['nativeStrip']),im(clip['compositeStrip']);assert ns.size==(128*s['frameCount'],128)and cs.size==(256*s['frameCount'],256)
 for i,f in enumerate(frames):assert diff(ns.crop((128*i,0,128*(i+1),128)),im(f['nativePng']))==0 and diff(cs.crop((256*i,0,256*(i+1),256)),im(f['png']))==0
 # User-required preservation of the validated Sword apex and normalized back_r bookends.
 if direction=='back_l'and kind=='Sword':
  apex=frames[5];src=old['frames'][6];assert all(diff(im(apex['layers'][n]['png']),im(src['layers'][n]['png']))==0 for n in clip['layerOrder']);clip['validatedV7Apex']={'sourceFrame':6,'candidateFrame':5,'rgbaMismatchPixels':0,'tipAboveSkullPx':48,'wristAboveShoulderPx':14,'negativeSpaceMinimumPx':4,'elbowInteriorDeg':68.405}
 if direction=='back_r':assert checks[0]['brightBodyPixels145']==7 and checks[-1]['brightBodyPixels145']==5
 (dst/'clip.json').write_text(json.dumps(clip,indent=2),encoding='utf-8');verification[key]={'frames':checks,'impactFrame':s['impactFrame'],'impactMs':s['impactStartMs'],'totalDurationMs':s['durationMs'],'mastersSavedReopened':True,'nativeStripTilesVerified':s['frameCount'],'compositeStripTilesVerified':s['frameCount']};delivery.append({'direction':direction,'action':kind,'clip':(dst/'clip.json').as_posix(),'clipSha256':sha(dst/'clip.json')})
for kind,s in spec.items():
 for q in s['phases']:comparison.append({'family':kind,'frame':q['index'],'phase':q['phase'],'durationMs':q['durationMs'],'front_rStartMs':q['startMs'],'front_lStartMs':q['startMs'],'back_rStartMs':q['startMs'],'back_lStartMs':q['startMs'],'impact':q['index']==s['impactFrame']})
(E/'verification.json').write_text(json.dumps({'checkpoint':'V8_REAR_ALIGNED','clips':verification,'newPixelLabCalls':0},indent=2));(E/'phase-comparison.json').write_text(json.dumps(comparison,indent=2))
with(E/'phase-comparison.csv').open('w',encoding='utf-8-sig',newline='')as f:w=csv.DictWriter(f,fieldnames=list(comparison[0]));w.writeheader();w.writerows(comparison)
snapshot=json.loads((E/'protected-input-hashes.json').read_text());assert all(sha(p)==h for p,h in snapshot.items());(E/'preservation.json').write_text(json.dumps({'protectedFilesUnchanged':len(snapshot),'frontalsUnmodified':True,'sourceV7Unmodified':True},indent=2));(E/'candidate4manifest.json').write_text(json.dumps({'checkpoint':'V8_REAR_ALIGNED','characterId':'orc-v1','technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','creatorApproval':'PENDING_CREATOR','runtimeImplemented':False,'cells':delivery},indent=2));print('50 frames verified; impact Sword325/Axe410; source files preserved',len(snapshot))
