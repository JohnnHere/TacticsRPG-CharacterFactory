from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
O=Path(__file__).resolve().relative_to(Path.cwd().resolve()).parent
C=Path('characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,j):Path(p).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
before=json.loads((O/'before.json').read_text(encoding='utf-8'));old=before['clip'];clip=json.loads(json.dumps(old))
plan=json.loads((O/'binding-plan.json').read_text(encoding='utf-8'))
after={}
for i in [7,8,9]:
 f=clip['frames'][i];ims=[Image.open(f['layers'][l]['png']).convert('RGBA') for l in ['weaponBack','weaponFront']]
 pts=[(x,y) for y in range(256) for x in range(256) if any(im.getpixel((x,y))[3] for im in ims)]
 low=[p for p in pts if p[1]>190];bbox=lambda a:[min(x for x,y in a),min(y for x,y in a),max(x for x,y in a),max(y for x,y in a)] if a else None
 after[str(i)]={'weaponBboxInclusive':bbox(pts),'weaponPixelsBelowGround':len(low),'belowGroundBboxInclusive':bbox(low),'weaponMaxY':max(y for x,y in pts),'clearancePx':190-max(y for x,y in pts)}
 assert not low and max(y for x,y in pts)<190
 f['rotationDeg']=plan['frames'][i]['angleAfter'];f['sha256']=sha(f['png'])
 for l in ['weaponBack','weaponFront']:f['layers'][l]['sha256']=sha(f['layers'][l]['png'])
 f['bindingRepair']={'finding':'V6-QA-02','plan':(O/'binding-plan.json').as_posix(),'gripPreserved':True,'scale':1}
clip['masterSha256']=sha(clip['master']);clip['compositeStripSha256']=sha(clip['compositeStrip'])
clip['weaponMaster']=(C/'source/weapon-binding.aseprite').as_posix();clip['weaponMasterSha256']=sha(clip['weaponMaster'])
clip['provenance']['bindingRepair']={'finding':'V6-QA-02','authorScript':(O/'repair.lua').as_posix(),'authorScriptSha256':sha(O/'repair.lua'),'originalClipSha256':before['clipSha256'],'report':(O/'report.md').as_posix(),'preview':(O/'preview.html').as_posix(),'pixelLabCalls':0,'method':'Only weaponBack/weaponFront cels F07-F09 re-bound at the unchanged palm; angle 145/175/185 to 125/120/110 degrees; scale 1; body and glove unchanged.','independentQaReReview':'REQUIRED'}
for p,h in before['protectedFiles'].items():assert sha(p)==h,('Protected file changed',p)
for i,f in enumerate(clip['frames']):
 comp=Image.new('RGBA',(256,256))
 for l in clip['layerOrder']:comp=Image.alpha_composite(comp,Image.open(f['layers'][l]['png']).convert('RGBA'))
 assert comp.tobytes()==Image.open(f['png']).convert('RGBA').tobytes(),('Composition',i)
 if i not in [7,8,9]:assert f==old['frames'][i]
 else:
  assert f['rightGrip']==old['frames'][i]['rightGrip'] and f['durationMs']==old['frames'][i]['durationMs']
  for l in ['body','handFront']:assert f['layers'][l]==old['frames'][i]['layers'][l]
strip=Image.open(clip['compositeStrip']).convert('RGBA');assert strip.size==(3072,256)
for i,f in enumerate(clip['frames']):assert strip.crop((i*256,0,(i+1)*256,256)).tobytes()==Image.open(f['png']).convert('RGBA').tobytes()
assert clip['durationsMs']==old['durationsMs'] and clip['layerOrder']==old['layerOrder'] and clip['visibleInterval']==old['visibleInterval']
write(C/'clip.json',clip);newsha=sha(C/'clip.json')
updates=[]
for path,snapshot in before['manifests'].items():
 p=Path(path);assert sha(p)==snapshot['sha256'],('Manifest changed concurrently',path)
 raw=p.read_bytes().decode('utf-8');j=snapshot['json'];target=next(c for c in j['cells'] if c.get('clip',c.get('clipJson'))==(C/'clip.json').as_posix())
 changes={'clipSha256':newsha,'masterSha256':clip['masterSha256'],'compositeStripSha256':clip['compositeStripSha256'],'weaponMasterSha256':clip['weaponMasterSha256']}
 changed=[]
 for key,value in changes.items():
  if key in target and target[key]!=value:
   needle=json.dumps(key)+': '+json.dumps(target[key]);assert raw.count(needle)==1,(path,key)
   raw=raw.replace(needle,json.dumps(key)+': '+json.dumps(value),1);changed.append(key)
 p.write_bytes(raw.encode('utf-8'));updated=json.loads(raw)
 for a,b in zip(j['cells'],updated['cells']):
  if a is not target:assert a==b,('Other manifest cell changed',path)
 updates.append({'path':path,'sha256':sha(p),'changedTargetFields':changed})
write(O/'patch-manifest.json',{'schemaVersion':1,'finding':'V6-QA-02','technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'ARTISTIC_REVISION_REQUIRED','creatorApproval':'PENDING_CREATOR','cells':[{'direction':'back_l','category':'Sword','clip':(C/'clip.json').as_posix(),'clipSha256':newsha,'masterSha256':clip['masterSha256'],'weaponMasterSha256':clip['weaponMasterSha256'],'compositeStripSha256':clip['compositeStripSha256'],'changedFrames':[7,8,9]}],'scope':'Only binding repair; same independent QA must re-review. Other finding V6-QA-01 is outside this repair.'})
result={'finding':'V6-QA-02','technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'ARTISTIC_REVISION_REQUIRED','creatorApproval':'PENDING_CREATOR','pixelLabCalls':0,'bodyPixelsChanged':0,'glovePixelsChanged':0,'gripChanged':False,'scaleChanged':False,'durationsAndBookendsPreserved':True,'protectedFilesByteIdentical':len(before['protectedFiles']),'before':before['beforeMeasurements'],'after':after,'clipSha256':newsha,'masterSha256':clip['masterSha256'],'weaponMasterSha256':clip['weaponMasterSha256'],'nativeMasterSha256':clip['nativeMasterSha256'],'nativeStripSha256':clip['nativeStripSha256'],'compositeStripSha256':clip['compositeStripSha256'],'updatedManifests':updates,'roundtrip':json.loads((O/'roundtrip.json').read_text(encoding='utf-8'))}
write(O/'result.json',result)
# Diagnostic sheet only: all artwork was already exported by Aseprite.
sheet=Image.new('RGB',(3*512,2*536),(65,62,72));draw=ImageDraw.Draw(sheet)
for col,i in enumerate([7,8,9]):
 for row,path in enumerate([O/'before/frames'/f'{i:02}.png',Path(clip['frames'][i]['png'])]):
  im=Image.open(path).convert('RGBA').resize((512,512),Image.Resampling.NEAREST);x=col*512;y=row*536;sheet.paste(im,(x,y+24),im);draw.text((x,y),f'F{i:02} '+('ANTES' if row==0 else 'DEPOIS'),fill='white');draw.line((x,y+24+190*2,x+512,y+24+190*2),fill=(120,140,165))
sheet.save(O/'before-after.png')
html='''<!doctype html><meta charset="utf-8"><title>V6-QA-02 · back_l/Sword groundfix</title><style>body{background:#25252e;color:#eee;font:16px system-ui;margin:24px}button,select,input{font:inherit}main{display:flex;gap:20px;flex-wrap:wrap}article{background:#36343f;padding:16px}.box{position:relative}canvas{display:block;image-rendering:pixelated;background:#514c59}.floor{position:absolute;top:74.21875%;height:1px;background:#a6b7cb;width:100%;pointer-events:none}small{display:block}header{position:sticky;top:0;background:#25252e;padding:12px;z-index:2}</style><h1>V6-QA-02 · back_l/Sword</h1><p>TECHNICALLY_COMPLETE · ARTISTIC_REVISION_REQUIRED · PENDING_CREATOR · re-revisão QA pendente</p><p>Corpo e luva preservados. Binding F07–F09: 145°/175°/185° → 125°/120°/110°. Palma e escala 1 mantidas.</p><header><button id="play">Pausar</button> <button id="step">Passo</button> <select id="speed"><option value="1">1×</option><option value="0.5">0,5×</option></select> <select id="zoom"><option value="1">Nativo 1×</option><option value="0.5">Tático 0,5×</option><option value="2">Zoom 2×</option></select> <input id="frame" type="range" min="0" max="11" value="0"><p id="readout"></p></header><main id="views"></main><p>Linha de referência: groundY=190, sobreposição de interface. <a href="report.md">Relatório</a> · <a href="result.json">Bboxes e hashes</a></p><script>
const clip=DATA;const durations=clip.durationsMs;let playing=true,time=0,last=0,manual=0,current=[];
async function load(){for(const mode of ['Antes','Depois','Corpo preservado']){const a=document.createElement('article');a.innerHTML='<h2>'+mode+'</h2><div class="box"><canvas width="256" height="256"></canvas><div class="floor"></div></div>';views.append(a);const cv=a.querySelector('canvas');const imgs=await Promise.all(clip.frames.map((f,i)=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=mode==='Antes'?'before/frames/'+String(i).padStart(2,'0')+'.png':'../../../../'+(mode==='Depois'?f.png:f.layers.body.png)})));current.push({mode,cv,imgs})}}
function index(){if(!playing)return manual;let t=time%clip.totalDurationMs,i=0;while(i<11&&t>=durations[i]){t-=durations[i];i++}return i}
function draw(){const i=index();for(const v of current){const x=v.cv.getContext('2d');x.clearRect(0,0,256,256);x.drawImage(v.imgs[i],0,0);v.cv.style.width=v.cv.style.height=(256*Number(zoom.value))+'px';v.cv.dataset.frame=i}frame.value=i;readout.textContent='F'+String(i).padStart(2,'0')+' · '+durations[i]+' ms · '+clip.frames[i].phase}
play.onclick=()=>{if(playing)manual=index();else time=durations.slice(0,manual).reduce((s,t)=>s+t,0);playing=!playing;play.textContent=playing?'Pausar':'Continuar';draw()};step.onclick=()=>{manual=index();playing=false;manual=(manual+1)%12;play.textContent='Continuar';draw()};frame.oninput=()=>{playing=false;manual=Number(frame.value);play.textContent='Continuar';draw()};zoom.onchange=draw;
function tick(t){if(last&&playing)time+=(t-last)*Number(speed.value);last=t;draw();requestAnimationFrame(tick)}load().then(()=>requestAnimationFrame(tick));</script>'''
(O/'preview.html').write_text(html.replace('DATA',json.dumps(clip)),encoding='utf-8')
print(json.dumps(result,indent=2,ensure_ascii=False))
