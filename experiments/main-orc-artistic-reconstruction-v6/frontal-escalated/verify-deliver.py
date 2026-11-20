from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
E=Path('experiments/main-orc-artistic-reconstruction-v6/frontal-escalated');S=Path('characters/orc-v1/source/artistic-reconstruction-v6/frontal/front_l-Sword-full');D=S.parent.parent/'frontal-escalated'/S.name
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:Image.open(p).convert('RGBA')
checks=[]
for i in range(13):
 a=load(S/f'layers/body/{i:02}.png');b=load(D/f'layers/body/{i:02}.png');pts=[(x,y) for y in range(256) for x in range(256) if a.getpixel((x,y))!=b.getpixel((x,y))];alpha=sum(a.getpixel(p)[3]!=b.getpixel(p)[3] for p in pts)
 assert (bool(pts)==(i in [3,4]));assert all(140<=x<=154 and 108<=y<=127 for x,y in pts)
 for name in ['weaponBack','weaponFront','handFront']:
  assert load(S/f'layers/{name}/{i:02}.png').tobytes()==load(E/f'reopened-layers/{name}/{i:02}.png').tobytes()
 checks.append({'frame':i,'bodyChangedPixels':len(pts),'alphaChangedPixels':alpha,'changedBbox':list(Image.frombytes('RGBA',b.size,b.tobytes()).getbbox()) if False else ([min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)] if pts else None)})
protected=json.loads((E/'protected-before.json').read_text());assert all(h(p)==v for p,v in protected.items())
clip=json.loads((S/'clip.json').read_text());old=S.as_posix();new=D.as_posix()
def paths(v):
 if isinstance(v,str):return v.replace(old,new)
 if isinstance(v,list):return [paths(x) for x in v]
 if isinstance(v,dict):return {k:paths(x) for k,x in v.items()}
 return v
clip=paths(clip)
for k in ['master','bodyMaster','nativeMaster','handMaster','strip','nativeStrip','compositeStrip']:clip[k+'Sha256']=h(clip[k])
for f in clip['frames']:
 f['sha256']=h(f['png']);f['nativeSha256']=h(f['nativePng'])
 for l in f['layers'].values():l['sha256']=h(l['png'])
 f['axillaEscalationChangedPixels']=checks[f['index']]['bodyChangedPixels']
clip.update(revision='main-orc-v6-axilla-escalated',checkpoint='AXILLA_SURGICAL_CANDIDATE',technicalStatus='TECHNICALLY_COMPLETE',artisticStatus='VISUAL_REVIEW_REQUIRED',artisticApproval='PENDING_CREATOR',fullClipIndependentQA='PENDING',sourceParentClip=(S/'clip.json').as_posix(),sourceParentClipSha256=h(S/'clip.json'))
clip['provenance'].update(authoring='Inherited V6 poses; surgical body contour edits only in F03/F04 using Aseprite Lua; saved/reopened/exported in Aseprite 1.3.18.6.',script=(E/'author.lua').as_posix(),scriptSha256=h(E/'author.lua'),bodyRgbaChanged=True,timingChanged=False,newPixelLabCalls=0)
clip['reuseAssessment']['body']='Inherited V6; only axilla contour in F03/F04 changed, no pose translation.'
clip['axillaEscalation']={'plan':(E/'edit-plan.json').as_posix(),'verification':(E/'verification.json').as_posix(),'report':(E/'report.md').as_posix()}
(D/'clip.json').write_text(json.dumps(clip,indent=2,ensure_ascii=False),encoding='utf-8')
verification={'status':'TECHNICALLY_COMPLETE','frames':checks,'sourceFilesPreserved':len(protected),'weaponAndHandLayersUnchanged':True,'timingMs':clip['durationsMs'],'totalDurationMs':730,'masters':json.loads((E/'reopen-result.json').read_text())};(E/'verification.json').write_text(json.dumps(verification,indent=2))
for label,P in [('before',S),('after',D)]:
 for i in [3,4]:
  im=load(P/f'{i:02}.png');im.crop((140,108,155,128)).resize((120,160),Image.Resampling.NEAREST).save(E/f'{label}-F{i:02}-axilla-8x.png')
 sheet=Image.new('RGBA',(7*256,2*280),(45,45,45,255));draw=ImageDraw.Draw(sheet)
 for i in range(13):
  im=load(P/f'{i:02}.png');x=i%7*256;y=i//7*280;sheet.alpha_composite(im,(x,y));draw.text((x+8,y+258),f'F{i:02} {clip["durationsMs"][i]} ms',fill='white')
 sheet.save(E/f'{label}-13-frames.png')
window=Image.new('RGBA',(280,384),(60,60,60,255));draw=ImageDraw.Draw(window)
for row,i in enumerate([3,4]):
 for col,label in enumerate(['before','after']):
  window.alpha_composite(load(E/f'{label}-F{i:02}-axilla-8x.png'),(col*140,row*192+24));draw.text((col*140,row*192+6),f'{label} F{i:02}',fill='white')
window.save(E/'axilla-before-after-8x.png')
manifest={'schemaVersion':1,'revision':clip['revision'],'technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','artisticApproval':'PENDING_CREATOR','runtimeImplemented':False,'cells':[{'direction':'front_l','action':'Sword','clip':(D/'clip.json').as_posix(),'clipSha256':h(D/'clip.json'),'baselineClip':(S/'clip.json').as_posix(),'baselineSha256':h(S/'clip.json'),'framesChanged':[3,4]}]};(E/'patch-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(checks));print('protected',len(protected))
