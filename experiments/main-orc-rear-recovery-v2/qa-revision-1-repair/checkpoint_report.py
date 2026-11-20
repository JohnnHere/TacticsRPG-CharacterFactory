from pathlib import Path
import hashlib,json,datetime
from PIL import Image
E=Path('experiments/main-orc-rear-recovery-v2');O=E/'qa-revision-1-repair'
def sha(p):return hashlib.sha256(Path('\\\\?\\'+str(Path(p).resolve())).read_bytes()).hexdigest()
old=json.loads((E/'E/rejected/qa-revision-1-before/backup-inventory.json').read_text('utf8'))
backup=[]
for r in old['files']:
 p=E/'E/rejected/qa-revision-1-before'/r['backup']
 assert sha(p)==r['sha256'],p
 backup.append(str(p))
specs=[('SwordL','back_l','Sword'),('AxeR','back_r','Axe'),('AxeL','back_l','Axe')]
rows=[]
for key,d,a in specs:
 frames=[]
 for i in range(8):
  before=Path(f'characters/orc-v1/source/rear-recovery-v2/{d}/{a}/Attack-representative-v1/layers/body/{i:02}.png')
  after=O/'checkpoint'/key/'body'/f'{i:02}.png'
  b=Image.open(before).convert('RGBA');v=Image.open(after).convert('RGBA')
  changes=[(j%256,j//256) for j,(p,q) in enumerate(zip(b.getdata(),v.getdata())) if p!=q]
  frames.append(dict(index=i,changedPixels=len(changes),nativeChangeBbox=[min(x for x,y in changes)-64,min(y for x,y in changes)-64,max(x for x,y in changes)-64,max(y for x,y in changes)-64] if changes else None,before=str(before),beforeSha256=sha(before),after=str(after),afterSha256=sha(after)))
 rows.append(dict(cell=f'{d}/{a}',key=key,frames=frames,source256=dict(path=str(O/'checkpoint/source'/f'{key}-body-256.aseprite'),sha256=sha(O/'checkpoint/source'/f'{key}-body-256.aseprite')),source128=dict(path=str(O/'checkpoint/source'/f'{key}-body-128.aseprite'),sha256=sha(O/'checkpoint/source'/f'{key}-body-128.aseprite'))))
r=dict(createdAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='VISUAL_REVIEW_REQUIRED',rootCheckpoint='PENDING_REVIEW',canonicalMutation=False,coordinateRegistration='all authored masks native128; +64,+64 to composite256',source='Actual saved and reopened Aseprite body masters',backup=dict(path=str(E/'E/rejected/qa-revision-1-before/backup-inventory.json'),verifiedFiles=len(backup),allHashesMatch=True),cells=rows)
(O/'checkpoint/checkpoint.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf8')
html='<!doctype html><meta charset="utf-8"><title>QA revision 1 — actual Aseprite body checkpoint</title><style>body{background:#172027;color:#ddd;font:16px sans-serif}img{max-width:100%;image-rendering:pixelated}a{color:#9ce}</style><h1>VISUAL_REVIEW_REQUIRED — body-only checkpoint</h1><p>Saved masters reopened in Aseprite; no equipment overlay. Canonical sources unchanged at checkpoint. PENDING_CREATOR.</p>'
for key,d,a in specs:
 html+=f'<h2>{d}/{a}</h2><img src="{key}-wholebody.png"><p>'
 for i in range(8):html+=f'<a href="{key}-F{i:02}-detail.png">F{i:02} detail</a> '
 html+='</p>'
(O/'checkpoint/index.html').write_text(html,encoding='utf8')
print(json.dumps({'backupVerified':len(backup),'changedPixels':{x['cell']:[f['changedPixels'] for f in x['frames']] for x in rows}},indent=2))
