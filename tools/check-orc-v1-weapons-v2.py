"""Artifact QA: independent items, shared motion, layer registration and actual portable playback."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from PIL import Image
import json,hashlib,threading,base64,io
R=Path(__file__).resolve().parents[1];E=R/'experiments/orc-v1-weapons-v2';B=R/'characters/orc-v1/source/equipment-v2';L=R/'Biblioteca de Arte/Personagens Jogaveis/Orc V1';O=R/'reports/orc-v1-weapons-v2';O.mkdir(exist_ok=True,parents=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
im=lambda p:Image.open(p).convert('RGBA')
def equal(a,b):
 assert a.size==b.size
 for p,q in zip(a.getdata(),b.getdata()):assert p[3]==q[3] and (not p[3] or p[:3]==q[:3])
manifest=read(B/'equipment-manifest.json');assert len(manifest['jobs'])==6
rig=read(E/'binding-rig.json');count=0;shared={};reference=im(R/'characters/orc-v1/concepts/concept-selected.png')
for job in manifest['jobs']:
 c=read(R/job['clip']);s=c['state'];n={'Idle':5,'Walk':16,'Attack':12}[s];assert len(c['frames'])==n
 assert c['loop']==(s!='Attack')
 assert sha(R/c['master'])==c['masterSha256']
 if s=='Idle':assert [f['durationMs'] for f in c['frames']]==[400,450,500,450,400]
 if s=='Walk':assert sum(f['durationMs'] for f in c['frames'])==1280
 if s=='Attack':assert sum(f['durationMs'] for f in c['frames'])==1315 and not c['contactEvent']['appliesDamage']
 sheet=im((R/job['clip']).parent/'native-strip.png');assert sheet.size==(256*n,256)
 for i,f in enumerate(c['frames']):
  g=rig['states'][s]['frames'][i];assert f['rightGrip']==g['grip'] and f['rotationDeg']==g['angle'] and f['durationMs']==g['durationMs']
  actual=im(R/f['png']);assert sha(R/f['png'])==f['sha256'];result=Image.new('RGBA',(256,256));layers={}
  for name in c['layerOrder']:
   p=R/f['layers'][name]['png'];assert sha(p)==f['layers'][name]['sha256'];layers[name]=im(p);result=Image.alpha_composite(result,layers[name])
  equal(actual,result);equal(actual,sheet.crop((256*i,0,256*(i+1),256)))
  for name in ['body','palmBack','fingersFront']:
   equal(layers[name],im(R/g[name]));key=(s,i,name)
   if key in shared:assert shared[key]==f['layers'][name]['sha256'],'Per-item body/hand drift'
   shared[key]=f['layers'][name]['sha256']
  weapon=layers['weapon'];box=weapon.getbbox();assert box and min(box[:2])>0 and max(box[2:])<256
  x,y=f['rightGrip'];assert weapon.getpixel((x,y))[3]>0,'Grip is not on actual handle'
  covered=sum(p[3]>0 and q[3]>0 for p,q in zip(weapon.getdata(),layers['fingersFront'].getdata()));assert covered>=8,'Fingers do not cross actual handle'
  contact=sum(p[3]>0 and q[3]>0 for p,q in zip(layers['body'].getdata(),layers['palmBack'].getdata()));assert contact>=12,'Palm disconnected from source body'
  if s=='Attack':
   equal(layers['body'].crop((64,163,192,192)),reference.crop((0,99,128,128)))
   equal(layers['body'].crop((122,151,152,162)),reference.crop((58,87,88,98)))
  count+=1
for wid in ['recruit-sword','militia-axe']:
 w=read(R/f'assets/weapons/{wid}/weapon.json');assert w['canvas']==[96,96];assert im(R/w['sprite']).getpixel(tuple(w['grip']))[3]>0
 if wid=='recruit-sword':assert im(R/w['sprite']).getbbox()[3]-im(R/w['sprite']).getbbox()[1]>=80
protected=read(R/'experiments/orc-v1-weapons-v1/protected-originals.json');assert all(sha(R/p)==h for p,h in protected.items())
for group,current in [('equipment','characters/orc-v1/source/equipment'),('masters','characters/orc-v1/source/aseprite/equipment')]:
 for p in (E/'preserved-v1'/group).rglob('*'):
  if p.is_file():assert sha(p)==sha(R/current/p.relative_to(E/'preserved-v1'/group))
catalog=read(L/'catalogo.json');assert all(sha(L/f['file'])==f['sha256'] for f in catalog['files']);assert len(catalog['players'])==7
errors=[];viewed=0
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='msedge',headless=True);page=browser.new_page(viewport={'width':2100,'height':1200});page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/Biblioteca%20de%20Arte/Personagens%20Jogaveis/Orc%20V1/index.html');page.wait_for_function('document.body.dataset.ready==="true"');page.click('#play');assert page.locator('canvas').count()==7
  for i,c in enumerate(catalog['players']):
   for n,f in enumerate(c['frames']):
    page.evaluate('async a=>{views[a.i].n=a.n;await draw(a.i)}',{'i':i,'n':n});encoded=page.locator(f'#anim-{i}').evaluate('e=>e.toDataURL().split(",")[1]');equal(Image.open(io.BytesIO(base64.b64decode(encoded))).convert('RGBA'),im(L/f['png']));viewed+=1
  page.evaluate('async()=>{views.forEach((v,i)=>v.n=[0,0,7,6,0,7,6][i]);await Promise.all(data.map((_,i)=>draw(i)))}');page.screenshot(path=str(O/'review-all.png'),full_page=True)
  for i,article in enumerate(page.locator('article').all()):article.screenshot(path=str(O/f'review-panel-{i}.png'))
  page.select_option('#zoom','1');page.set_viewport_size({'width':410,'height':900});assert not page.locator('body').evaluate('e=>e.scrollWidth>innerWidth+1')
  page.goto((L/'index.html').as_uri());page.wait_for_function('document.body.dataset.ready==="true"');assert not errors;browser.close()
finally:server.shutdown();server.server_close()
report={'status':'TECHNICAL_PASS_ART_REVIEW_PENDING','compositesAndLayerReconstructions':count,'viewerFramesComparedRGBA':viewed,'copiedHashes':len(catalog['files']),'sharedBodyPalmFingersAndClocksVerified':True,'handleUnderGripAndFingersEveryFrame':True,'frozenLowerGarmentRegionAndLegs':True,'protectedOriginalInfanteFiles':len(protected),'v1ArtAndMastersUnchanged':True,'weaponClipping':False,'armedIdleStandardMs':2200,'runtimeImplemented':False,'artisticApproval':'PENDING_CREATOR','javascriptErrors':errors,'limits':'Pixel overlap and exact exports verify registration, not believable grip, motion quality or artistic approval.'}
(O/'check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
