"""Focused regression checks on real saved/exported candidates. No raster edits."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];E=Path(__file__).resolve().parent;B=R/'characters/orc-v1/source/onehanded-polish-v1'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pixels=lambda p:Image.open(p).convert('RGBA').tobytes()
checks=[]
def check(name,ok,detail=None):
 checks.append({'check':name,'pass':bool(ok),'detail':detail});assert ok,(name,detail)
protected=read(E/'protected-art.json');changed=[p for p,h in protected.items() if not (R/p).exists() or sha(R/p)!=h];check('Prior raster/master preservation',not changed,{'files':len(protected),'changed':changed})
for p in ['characters/orc-v1/character.json','characters/orc-v1/assets.json','characters/orc-v1/source/equipment-current.json','assets/weapons/recruit-sword/weapon.json','assets/weapons/militia-axe/weapon.json']:
 check('Active metadata unchanged: '+p,(R/p).read_bytes()==(E/'baseline-metadata'/p).read_bytes())
check('MAIN ORC authority',read(R/'reports/orc-production-current.json')['characterId']=='orc-v1')
plan=read(E/'plan.json');details={}
for c,seq in plan['sequences'].items():
 clip=read(B/c/'Attack/clip.json');profile=read(B/c/'Attack/profile.json');n=len(seq);check(c+' frame counts',n==clip['frameCount']==len(profile['frames']))
 check(c+' canvas/ground/scale',clip['canvas']==[256,256] and clip['groundY']==190 and all(f['scale']==1 for f in profile['frames']))
 check(c+' exact durations',list(q['ms'] for q in seq)==list(f['durationMs'] for f in clip['frames'])==list(f['durationMs'] for f in profile['frames']))
 check(c+' continuous Attack-only visible interval',[i for i,f in enumerate(clip['frames']) if f['weaponVisible']]==list(range(1,9)) and not clip['loop'] and clip['hideAfterAction'])
 for key in ['master','bodyMaster','handMaster']:check(c+' master '+key,sha(R/clip[key])==clip[key+'Sha256'])
 check(c+' unchanged item art',sha(R/clip['weapon']['master'])==clip['weapon']['masterSha256'] and sha(R/clip['weapon']['sprite'])==clip['weapon']['spriteSha256'])
 for i,(q,f,pf) in enumerate(zip(seq,clip['frames'],profile['frames'])):
  check(c+f' frame{i} hashes',sha(R/f['png'])==f['sha256'] and all(sha(R/v['png'])==v['sha256'] for v in f['layers'].values()))
  body=R/f['layers']['body']['png'];original=E/'baseline'/q['from']/'body'/f"{q['index']:02d}.png"
  if c=='Sword' and q['index']==4:
   a=Image.open(original).convert('RGBA');b=Image.open(body).convert('RGBA');delta=[(x,y) for y in range(256) for x in range(256) if a.getpixel((x,y))!=b.getpixel((x,y))]
   check('Sword crossing inherited blade residue erased only',len(delta)>0 and all(((160<=x<=184 and 99<=y<=121) or (x,y)==(181,93)) and b.getpixel((x,y))[3]==0 for x,y in delta),len(delta))
  elif not q.get('patch'):check(c+f' body{i} exact reused source',pixels(body)==pixels(original))
  else:
   a=Image.open(original).convert('RGBA');b=Image.open(body).convert('RGBA');mask=Image.open(E/'inputs'/f'{c}-mask.png').convert('RGB');delta=[]
   for y in range(256):
    for x in range(256):
     if a.getpixel((x,y))!=b.getpixel((x,y)):delta.append((x,y))
   check(c+' masked body edit only',all(64<=x<192 and 64<=y<192 and mask.getpixel((x-64,y-64))==(255,255,255) for x,y in delta),len(delta))
   check(c+' exact head/feet/grip protection',all(not (y<97 or y>=174 or (x-pf['grip'][0])**2+(y-pf['grip'][1])**2<=144) for x,y in delta))
  if not q['visible']:check(c+f' no stale overlays{i}',all(Image.open(R/f['layers'][k]['png']).getbbox() is None for k in ['weaponBack','weaponFront','handFront']))
  if q['visible'] and not q.get('onset'):check(c+f' own original fingers{i}',pixels(R/f['layers']['handFront']['png'])==pixels(E/'baseline'/q['from']/'handFront'/f"{q['index']:02d}.png"))
 check(c+' identical body at appearance',pixels(R/clip['frames'][0]['layers']['body']['png'])==pixels(R/clip['frames'][1]['layers']['body']['png']))
 check(c+' identical body at disappearance',pixels(R/clip['frames'][8]['layers']['body']['png'])==pixels(R/clip['frames'][9]['layers']['body']['png']))
 neutral=pixels(E/'baseline'/c/'body/00.png');check(c+' exact unarmed start/end',pixels(R/clip['frames'][0]['png'])==neutral and pixels(R/clip['frames'][-1]['png'])==neutral)
 check(c+' visual impact only',clip['contactEvent']['frame']==6 and not clip['contactEvent']['appliesDamage'])
 swap=read(R/f'reports/main-orc-polish-v1/reuse/{c}/reuse.json');check(c+' compatible existing item swapped without body redraw',len(swap['frames'])==n and swap['cloudCalls']==swap['bodyRedraws']==0 and all(f['body']==p['body'] and f['handFront']==p['handFront'] and f['durationMs']==p['durationMs'] for f,p in zip(swap['frames'],profile['frames'])))
 details[c]={'frames':n,'durationMs':sum(q['ms'] for q in seq),'impactTimeMs':clip['contactEvent']['timeMs'],'visibleInterval':clip['visibleInterval']}
for state in ['Idle','Walk']:
 a=read(B/state/'clip.json');b=read(R/f'characters/orc-v1/source/onehanded-rescue-v3/{state}/clip.json');check(state+' unchanged approved clip',a==b and all(not f['weaponVisible'] for f in a['frames']))
build=read(E/'build.json');check('Existing exporter verified all candidates',build['summary']=={'jobs':10,'frames':92,'comparedFrames':92})
result={'status':'PASS','checks':checks,'details':details,'artisticApproval':'PENDING_CREATOR','runtimeTest':'NOT_RUN / out of scope'};(E/'technical-qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'status':'PASS','checks':len(checks),'protectedArt':len(protected),'clips':details}))
