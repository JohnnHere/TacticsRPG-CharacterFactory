from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np,datetime
E=Path('experiments/main-orc-rear-reconstruction-v4/dev');C=Path('characters/orc-v1/source/rear-reconstruction-v4')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
def delta(a,b):return int(((a!=b).any(2)&((a[:,:,3]>0)|(b[:,:,3]>0))).sum())
clips=read(E/'input-clips.json');classifications=[]
for key,p in clips.items():
 direction,action=key.split('/');rows=[]
 for f in p['frames']:
  i=f['index'];cl='KEEP';reason='Protected or no demonstrated new static defect; no change authorized by an unverified hypothesis.';resolution='UNCHANGED'
  if direction.startswith('back')and action in ['Sword','Axe']:
   if 1<=i<=5:
    cl='REAUTHOR_KEY_POSE';reason='Current poses do not establish a convincing coupled shoulder/torso technique and grip sequence; reconstruction required before interpolation. Static judgment; 1x movement not certified.'
   elif i==6:
    cl='LOCAL_CORRECTION';reason='Recovery-arm/hand path must be reassessed after strike keys; material retouch does not resolve this dependency.'
   else:reason='Preserve rest/return identity as source reference; F07 back_r gets only traced scalp-outline cleanup.'
   if direction=='back_r'and i==7:cl='LOCAL_CORRECTION'
   resolution='WEAPON_MATERIAL_REFINEMENT; BACK_R_SCALP_LOCAL_CLEANUP; BODY_RECONSTRUCTION_UNRESOLVED'
  elif action=='Unarmed':
   if direction.startswith('back')and i==3:
    cl='REAUTHOR_KEY_POSE';reason='Follow-through/retraction needs coherent transition to F04; current extended arm is not proof of natural recovery. Prior isolated donor proposal not blindly integrated.'
   elif direction.startswith('front')and i==3:
    cl='LOCAL_CORRECTION';reason='Creator-reported late hand disappearance requires motion-localization. F03 static body shows limb pixels; import deletion/source smear not demonstrated, no speculative edit.'
  elif action=='Walk':
   cl='LOCAL_CORRECTION';reason='Only shading is in scope. Static sequence inspected, but temporal flicker not localized with reliable continuous visual playback; preserve all silhouette, gait and timing.'
  elif action=='Defeat'and direction.startswith('front'):
   reason='Current source already has head grounded and prone terminal; F02/F03 hands inspect as discrete pixel clusters. No demonstrated smear or new safe correction. Keep pending creator motion review.'
  elif action in ['Sword','Axe']:
   cl='LOCAL_CORRECTION'if f.get('weaponVisible')else'KEEP';reason='Successful frontal body/hand choreography protected; independent weapon material-only refinements applied without silhouette, hand-mask or timing changes.';resolution='MATERIAL_REFINEMENT_EXPORTED'if f.get('weaponVisible')else'UNCHANGED_VISIBLE_PIXELS'
  rows.append({'index':i,'classification':cl,'reason':reason,'resolution':resolution,'durationMs':f['durationMs']})
 classifications.append({'cellId':key,'frames':rows,'evidence':'Static full sequence/contact sheets only; does not assert continuous1x visual evaluation.'})
write(E/'frame-classifications.json',{'stage':'A','framesExamined':210,'classificationScope':'Local developer diagnosis, no independent QA','cells':classifications})
source=rgba(C/'keypose-axeR/source-F04.png');trial=rgba(C/'keypose-axeR/descending-study.png')
mask=(source!=trial).any(2)&((source[:,:,3]>0)|(trial[:,:,3]>0));yy,xx=np.where(mask)
kp={'status':'ARTISTIC_REVISION_REQUIRED','eligibleForIntegration':False,'disposition':'REJECTED_LOCAL_KEYPOSE; NOT_REFERENCED_BY_CANDIDATE_MANIFEST','changedBodyRgbaPixels':int(mask.sum()),'nativeChangeBbox':[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],'sourceFrame':'back_r/Axe F04','nativeToCompositeOffset':[64,64],'componentAuthoring':'Same-view original forearm/bracer and sleeve masks independently reseated; existing scapular plate forward; individually traced elbow fold. No whole-body compression/rotation or new generation.','rejectionReasons':['Forearm became narrow and patch-like at elbow; does not sustain original mass.','Torso/scapular reseating does not establish convincing full-body weight.','F03 to studyF04 to originalF05 creates down-then-up wrist/axe discontinuity.','Grip study is not convincing enough to approve or propagate.'],'sourceScript':str(E/'author-keypose.lua').replace('\\','/'),'nativeMaster':str(C/'keypose-axeR/source/descending-study.aseprite').replace('\\','/'),'equippedMaster':str(C/'keypose-axeR/source/equipped-descending-study.aseprite').replace('\\','/'),'evidence':str(E/'keypose-neighbors-equipped.png').replace('\\','/')}
write(C/'keypose-axeR/rejection.json',kp)
compare=[]
for i in range(8):
 a=rgba(clips['back_r/Sword']['frames'][i]['layers']['body']['png']);b=rgba(clips['back_r/Axe']['frames'][i]['layers']['body']['png']);compare.append(delta(a,b))
verify=read(E/'verification.json')
metrics={'keypose':kp,'back_rSwordVsAxeBodyDeltaByFrame':compare,'back_rSwordVsAxeDurationsEqual':clips['back_r/Sword']['durationsMs']==clips['back_r/Axe']['durationsMs'],'weaponSpriteRgbaDeltas':{w['category']:w['changedRgbaPixels']for w in verify['weaponSources']},'compositeRgbaDeltasByClip':{c['cellId']:sum(f['compositeRgbaDelta']for f in c['frames'])for c in verify['clips']},'changedVisibleFrames':sum(f['compositeRgbaDelta']>0 for c in verify['clips']for f in c['frames']),'producedFrames':82,'unchangedAliasFrames':128,'bodyOutlinePixelsChanged':sum(f['bodyRgbaDelta']for c in verify['clips']for f in c['frames']),'bodyChoreographyHandTimingChanged':False,'inputFilesPreserved':873,'paidGenerationCalls':0}
write(E/'measured-deltas.json',metrics)
history=[{'stage':'ACCESS','status':'ACCESS_CONFIRMED','sourceRead':True,'imagesViewed':True,'batch':'AVAILABLE 1.3.18.6; hidden --batch --noinapp; isolated profile;90s timeout','cwd':str(Path.cwd())},{'stage':'DIAGNOSIS','status':'ARTISTIC_REVISION_REQUIRED','classificationFile':str(E/'frame-classifications.json').replace('\\','/'),'confirmed':'8/8 back_r Sword/Axe body frames identical; same durations. This is source reuse, not distinct cutting/chopping body techniques.','limits':'Walk flicker and frontal hand disappearance not independently motion-localized; no invented cause.'},{'stage':'REPRESENTATIVE_KEYPOSE','status':'ARTISTIC_REVISION_REQUIRED','disposition':'REJECTED; NOT_PROPAGATED','rejection':str(C/'keypose-axeR/rejection.json').replace('\\','/'),'changedBodyRgbaPixels':kp['changedBodyRgbaPixels']},{'stage':'HANDOFF','status':'ARTISTIC_REVISION_REQUIRED','eligibleForIntegration':False,'actualOutput':'2 editable independent material forks coherently associated with8clip forks;82frames;20unchanged aliases/128frames;166scalp outline pixel substitutions across2back_r clips','technicalScope':'PASS focused source/export/body/hand/timing/alpha/association checks; global technicalStatus NOT_VERIFIED','blocker':'Representative local anatomy/weight reconstruction failed visual neighbor inspection. No validated set of distinct rear strike keys exists to propagate. This is an artistic production blocker, not missing permission or paid-generation authorization.','newGenerations':0}]
write(E/'checkpoint-history.json',history);write(E/'checkpoint.json',history[-1])
print(json.dumps(metrics,indent=2))
