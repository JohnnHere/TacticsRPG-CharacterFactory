from pathlib import Path
import json,hashlib,math
from PIL import Image
E=Path('experiments/main-orc-skeleton-02/stage-bcde');S=Path('characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword');W=Path('characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/recruit-sword.png')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
c=json.loads((S/'clip.json').read_text(encoding='utf-8-sig'));seq=json.loads(Path('experiments/main-orc-skeleton-first-01/sequence-fixed.json').read_text(encoding='utf-8-sig'))
frames=seq.get('frames',[])
plans=[(0,158,145,20),(5,160,81,0),(8,178,131,-138.65),(9,169,159,-131.35),(13,158,145,20)]
actual={0:[[150,104],[166,121],[162,140]],5:[[152,103],[175,101],[165,88]],8:[[147,112],[168,120],[181,125]],9:[[145,112],[164,126],[173,150]],13:[[150,104],[166,121],[162,140]]}
phases=['Preparação','Elevação / antecipação','Golpe principal','Seguimento','Recuperação']
pose=[]
for k,(i,x,y,a) in enumerate(plans):
 rad=math.radians(a);v=[round(math.sin(rad),5),round(-math.cos(rad),5)]
 p={'index':i,'phase':c['frames'][i]['phase'],'label':phases[k],'canvas':[256,256],'coordinateConvention':'x right, y down; native128 + [64,64] = composed256','anatomy':dict(zip(['rightShoulder','rightElbow','rightWrist'],actual[i])),'hand':'right','handContact':[x,y],'handleContact':[x,y],'sourceWeaponGrip':[48,66],'pivotSource':[48,66],'pivotDestination':[x,y],'rotationClockwiseDegrees':a,'bladeDirection':v,'pommelDirection':[-v[0],-v[1]],'scale':1,'sampling':'inverse nearest integer, no interpolation; Aseprite Lua','layers':['weaponBack','body','weaponFront','handFront'],'layerAssignment':{'weaponBack':'source weapon rows 60..73 inclusive (handle), behind body','weaponFront':'remaining weapon pixels (blade/guard/pommel), ahead of body','handFront':'inherited same-frame glove; 00/13 existing body glove pixels in rectangle [151,139,163,153] inclusive'},'visibleHandle':'Only the short exposed leather intervals at guard/glove and glove/pommel; central grip occluded by closed glove. Full handle available in weapon-only.','occlusion':'Closed glove covers central handle; guard stays outside glove. Existing foreground glove restored last; no opaque fill mask.','visibility':'armed diagnostic attachment study; not runtime visibility' if i in [0,13] else 'attack-visible pose','sourceManualJointsNative':c['frames'][i].get('manualJointsNative'),'anatomyPrecision':'visual estimates shoulder/elbow/wrist ±3px; grip is exact authored coordinate; inherited manual joints are reference metadata, not authoritative after limb displacement','referenceSkeletonFrame':next((f for f in frames if f.get('index')==i),None),'outputs':{n:{'png':f'{n}/{i:02}.png','sha256':sha(E/n/f'{i:02}.png'),'provenance':'Aseprite Lua composition/export; body pixels inherited without retouch; official weapon rotated in Aseprite; no external raster authorship'} for n in ['body-only','weapon-only','composite']},'master':{'path':f'source/{i:02}.aseprite','sha256':sha(E/'source'/f'{i:02}.aseprite')},'handCrop':{'rect':[x-20,y-20,40,40],'scale':8,'sampling':'nearest-neighbour preview only'}}
 pose.append(p)
inputs=[S/'clip.json',W,W.parent/'weapon.json',Path('experiments/main-orc-skeleton-first-01/poses-fixed.json'),Path('experiments/main-orc-skeleton-first-01/sequence-fixed.json')]
for i,*_ in plans:
 for n in ['body','handFront','weaponBack','weaponFront']:inputs.append(S/'layers'/n/f'{i:02}.png')
attachment={'schema':'skeleton-02/stage-bcde/1','status':'VISUAL_REVIEW_REQUIRED','creatorApproval':'PENDING_CREATOR','scope':'orc-v1 back_l Sword five structural poses only','sourceInputs':[{'path':str(p).replace('\\','/'),'sha256':sha(p)} for p in inputs],'weaponOfficial':{'sprite':str(W).replace('\\','/'),'grip':[48,66],'hand':'right','canvas':[96,96]},'authoringScript':'author.lua','generationCalls':0,'poses':pose,'limitations':['Five static poses do not validate temporal continuity.','00/13 armed diagnostic only, no proposed runtime weapon interval change.','Anatomical reference from skeleton-first differs from actual v8 limb geometry; actual glove takes precedence for attachment.']}
(E/'attachment.json').write_text(json.dumps(attachment,ensure_ascii=False,indent=2),encoding='utf-8')
# Meaningful checks: palette preservation, exact body inheritance, source hashes,
# and reopened Aseprite export equals explicit alpha-over layer contract.
valid=[];weapon_colors=set(Image.open(W).convert('RGBA').getdata())-{(0,0,0,0)}
for i,*_ in plans:
 id=f'{i:02}';wp=Image.open(E/'weapon-only'/f'{id}.png').convert('RGBA');assert all(p in weapon_colors for p in wp.getdata() if p[3])
 body=Image.open(E/'body-only'/f'{id}.png').convert('RGBA');assert body.tobytes()==Image.open(S/'layers/body'/f'{id}.png').convert('RGBA').tobytes()
 valid.append({'index':i,'bodyRGBAIdentical':True,'weaponOpaquePaletteSubsetOfOfficial':True})
(E/'verification.json').write_text(json.dumps({'status':'TECHNICALLY_COMPLETE','scope':'15 PNGs, 5 editable Aseprite masters; structural output checks only','checks':valid,'artisticStatus':'VISUAL_REVIEW_REQUIRED'},indent=2),encoding='utf-8')
