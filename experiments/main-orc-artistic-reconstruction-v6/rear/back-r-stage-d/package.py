import json,hashlib
from pathlib import Path
from PIL import Image
O=Path(__file__).resolve().relative_to(Path.cwd().resolve()).parent
C=Path('characters/orc-v1/source/artistic-reconstruction-v6/rear')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
r=json.loads((O/'author-result.json').read_text(encoding='utf-8'))
jobs=json.loads((O/'jobs.json').read_text(encoding='utf-8'))
clips=[];patch=[];checks=[]
for kind in ['Sword','Axe']:
 k=kind.lower();dest=C/f'back_r-{k}';d=dest.as_posix()
 master=f'{d}/source/composite.aseprite';native=f'{d}/source/native.aseprite'
 frames=[]
 for f in r[kind]['frames']:
  i=f['index'];fr=dict(f);fr['png']=f'{d}/frames/{i:02}.png';fr['sha256']=sha(fr['png']);fr['nativePng']=f'{d}/native/{i:02}.png';fr['nativeSha256']=sha(fr['nativePng'])
  if not fr['weaponVisible']:fr['rightGrip']=None;fr['rotationDeg']=None
  fr['anatomyPlan']='experiments/main-orc-artistic-reconstruction-v6/rear/back-r-stage-d/anatomy-plan.json'
  fr['layers']={l:{'png':f'{d}/layers/{l}/{i:02}.png','sha256':sha(f'{d}/layers/{l}/{i:02}.png')} for l in ['weaponBack','body','weaponFront','handFront']}
  body=Image.open(fr['layers']['body']['png']).convert('RGBA');n=Image.open(fr['nativePng']).convert('RGBA');assert body.crop((64,64,192,192)).tobytes()==n.tobytes()
  comp=Image.new('RGBA',(256,256))
  for l in fr['layers']:
   im=Image.open(fr['layers'][l]['png']).convert('RGBA');comp=Image.alpha_composite(comp,im)
   if not fr['weaponVisible'] and l!='body':assert im.getbbox() is None
  actual=Image.open(fr['png']).convert('RGBA');assert comp.tobytes()==actual.tobytes()
  assert n.getbbox()[3]-1==126
  assert set(n.getchannel('A').getdata()).issubset({0,255})
  checks.append({'cell':f'back_r/{kind}','frame':i,'nativeBodyCrop':True,'layerComposition':True,'groundY':126,'transparentBookend':not fr['weaponVisible']})
  frames.append(fr)
 c={'schemaVersion':1,'revision':'main-orc-artistic-reconstruction-v6-rear','id':'basic.sword-slash' if kind=='Sword' else 'basic.axe-chop','character':'orc-v1','identity':'Verde Warcraft','direction':'back_r','category':kind,'state':'Attack','frameCount':12,'durationsMs':[f['durationMs'] for f in frames],'totalDurationMs':sum(f['durationMs'] for f in frames),'visibleInterval':[1,9],'canvas':[256,256],'nativeCanvas':[128,128],'bodyOffset':[64,64],'groundY':190,'nativeGroundY':126,'master':master,'masterSha256':sha(master),'nativeMaster':native,'nativeMasterSha256':sha(native),'layerOrder':['weaponBack','body','weaponFront','handFront'],'oneShot':True,'loop':False,'weaponDefinition':f'characters/orc-v1/source/combat-rescue-v5/combat/weapons/{kind}/weapon.json','technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','creatorApproval':'PENDING_CREATOR','runtimeImplemented':False,'provenance':{'authorScript':(O/'author.lua').as_posix(),'authorScriptSha256':sha(O/'author.lua'),'jobId':jobs[k],'seed':63130 if kind=='Sword' else 64130,'request':(O/f'{k}-request.json').as_posix(),'rawFrames':(O/'raw'/k).as_posix(),'method':'PixelLab skeleton_v3 Stage D back_r whole-body poses; Aseprite Lua exterior cleanup, tiny disconnected debris removal, measured per-pose glove occlusion and independent item composition. Bookends inherited V5 unarmed identity. Not manual drawing.','limitation':'Full-body reference candidate: knuckle volume, stance continuity, projected cutting direction and onset/recovery require creator judgment. See anatomy-plan.json and report.md. Boot-contact and knee continuity are specifically reviewed against the V5 back_r defects.'},'frames':frames}
 write(dest/'clip.json',c);clips.append(c)
 patch.append({'direction':'back_r','category':kind,'beforeClip':f'characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/full-back-r-{k}/clip.json','clip':f'{d}/clip.json','clipSha256':sha(dest/'clip.json')})
write(C/'patch-manifest-back-r-stage-d.json',{'schemaVersion':1,'checkpoint':'V6_BACK_R_ADAPTATION_READY','technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','creatorApproval':'PENDING_CREATOR','runtimeImplemented':False,'cells':patch,'blockedStages':[]})
write(O/'technical-checks.json',{'status':'TECHNICALLY_COMPLETE','savedMasterRoundtrip':r,'frameChecks':checks,'semanticNote':'Composition equality does not prove anatomical or artistic validity. Body layers were separately inspected.'})
# Preservation audit is read-only outside the two authorized V6 rear roots.
baseline=json.loads(Path('experiments/main-orc-artistic-reconstruction-v6/input-preservation.json').read_text(encoding='utf-8'))
changed=[];missing=[];same=0
for p,h in baseline['files'].items():
 pp=Path(p)
 if not pp.exists():missing.append(p)
 elif sha(pp)!=h:changed.append(p)
 else:same+=1
write(O/'preservation-check.json',{'compared':len(baseline['files']),'identical':same,'changed':changed,'missing':missing,'note':'Reports observed differences without attributing unrelated work to this rear task.'})
html='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>V6 back_r - referência</title>
<style>body{background:#25252e;color:#eee;font:16px system-ui;margin:24px}button,select,input{font:inherit;padding:6px}header{position:sticky;top:0;background:#25252e;padding:12px;z-index:1}main{display:flex;gap:20px;flex-wrap:wrap}article{background:#36343f;padding:16px;border-radius:8px}canvas{display:block;image-rendering:pixelated;background:repeating-conic-gradient(#514c59 0% 25%,#494550 0% 50%) 0 0/20px 20px}small{display:block;color:#bbb}#status{margin:12px 0}</style>
<h1>Orc V1 · V6 back_r</h1><p>V6_BACK_R_ADAPTATION_READY · VISUAL_REVIEW_REQUIRED · PENDING_CREATOR</p><p>Referência candidata para revisão. Antes: V5 rejeitada. Corpo inteiro sem equipamento e composição em paralelo.</p>
<header><label>Família <select id="family"><option>Sword</option><option>Axe</option></select></label> <button id="play">Pausar</button> <button id="step">Passo +1</button> <button id="restart">Reiniciar</button> <select id="speed"><option value="1">1×</option><option value="0.5">0,5×</option></select> <select id="zoom"><option value="1">Nativo 1×</option><option value="0.5">Tático 0,5×</option><option value="2">Zoom 2×</option><option value="4">Zoom 4×</option></select><input id="frame" type="range" min="0" max="11" value="0"><div id="status"></div></header><main id="views"></main>
<p>Aseprite é o mestre. Uma mão direita por pose; armas independentes somente no ataque. Sem integração ou promoção. Leia <a href="report.md">report.md</a> e <a href="../audit-preview.html">auditoria das quatro células V5</a> e <a href="../preview.html">referência back_l congelada</a>.</p>
<script>const candidates=DATA;const baselinePaths=BASE;const cache={};let playing=true,time=0,last=0,manual=0,current=[],rendered=[];
async function load(){current=[];views.innerHTML='';for(const version of ['V5 rejeitada','V6 candidata']){const c=version.startsWith('V6')?candidates.find(c=>c.category===family.value):await fetch('../../../../'+baselinePaths[family.value]).then(r=>r.json());for(const mode of ['body','composite']){const a=document.createElement('article');a.innerHTML='<h2>'+version+'</h2><small>'+mode+' · '+c.totalDurationMs+' ms</small>';const cv=document.createElement('canvas');cv.width=cv.height=256;a.append(cv);views.append(a);const imgs=await Promise.all(c.frames.map(f=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src='../../../../'+(mode==='body'?f.layers.body.png:f.png)})));current.push({c,cv,imgs,mode,version})}}time=0;manual=0;draw()}
function index(c){if(!playing)return manual;let t=time%c.totalDurationMs;let i=0;while(i<c.frames.length-1&&t>=c.frames[i].durationMs){t-=c.frames[i].durationMs;i++}return i}
function draw(){rendered=[];for(const v of current){let i=index(v.c);const ctx=v.cv.getContext('2d');ctx.clearRect(0,0,256,256);ctx.drawImage(v.imgs[i],0,0);v.cv.style.width=v.cv.style.height=(256*Number(zoom.value))+'px';v.cv.dataset.frame=i;rendered.push({version:v.version,mode:v.mode,frame:i})}if(current.length){const c=current[current.length-1].c;const i=index(c);frame.value=i;status.textContent=family.value+' · V6 F'+String(i).padStart(2,'0')+' · '+c.frames[i].phase+' · '+c.frames[i].durationMs+' ms'}}
play.onclick=()=>{if(playing){manual=current.length?index(current[current.length-1].c):0}else if(current.length){time=current[current.length-1].c.frames.slice(0,manual).reduce((s,f)=>s+f.durationMs,0)}playing=!playing;play.textContent=playing?'Pausar':'Continuar';draw()};step.onclick=()=>{manual=current.length?index(current[current.length-1].c):manual;playing=false;manual=(manual+1)%12;play.textContent='Continuar';draw()};frame.oninput=()=>{playing=false;manual=Number(frame.value);play.textContent='Continuar';draw()};restart.onclick=()=>{time=0;manual=0;draw()};zoom.onchange=draw;family.onchange=load;
function tick(n){if(last&&playing)time+=(n-last)*Number(speed.value);last=n;draw();requestAnimationFrame(tick)}load().then(()=>requestAnimationFrame(tick));</script></html>'''
before={p['category']:json.loads(Path(p['beforeClip']).read_text(encoding='utf-8')) for p in patch}
html=html.replace("await fetch('../../../../'+baselinePaths[family.value]).then(r=>r.json())",'baselinePaths[family.value]').replace("status.textContent=", "document.querySelector('#status').textContent=")
(O/'preview.html').write_text(html.replace('DATA',json.dumps(clips)).replace('BASE',json.dumps(before)),encoding='utf-8')
print('Packaged 2 isolated cells, 24 frames; preservation:',same,'identical;',len(changed),'changed;',len(missing),'missing')
