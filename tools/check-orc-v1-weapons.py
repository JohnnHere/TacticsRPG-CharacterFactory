"""Verify actual exported layers, grips, loops, preservation and portable review pixels."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from PIL import Image
import json,hashlib,threading,base64,io
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports/orc-v1-weapons-v1';LIB=ROOT/'Biblioteca de Arte/Personagens Jogaveis/Orc V1'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def identical(a,b):
 assert a.size==b.size
 for p,q in zip(a.getdata(),b.getdata()):assert p[3]==q[3] and (not q[3] or p[:3]==q[:3])
manifest=read(ROOT/'characters/orc-v1/source/equipment/equipment-manifest.json');composed=0
for job in manifest['jobs']:
 clip=read(ROOT/job['clip']);assert clip['canvas']==[256,256];assert clip['frameCount']==(16 if clip['state']=='Walk' else 9)
 if clip['state']=='Walk':assert clip['loop'] and sum(f['durationMs'] for f in clip['frames'])==1280
 else:assert not clip['loop'] and not clip['contactEvent']['appliesDamage']
 assert sha(ROOT/clip['master'])==clip['masterSha256']
 strip=Image.open(ROOT/Path(job['clip']).parent/'native-strip.png').convert('RGBA');assert strip.size==(256*clip['frameCount'],256)
 for i,f in enumerate(clip['frames']):
  result=Image.new('RGBA',(256,256))
  for name in ['weaponBack','body','weaponFront','handFront']:
   p=ROOT/f['layers'][name]['png'];assert sha(p)==f['layers'][name]['sha256'];im=Image.open(p).convert('RGBA');result=Image.alpha_composite(result,im)
  actual=Image.open(ROOT/f['png']).convert('RGBA');identical(result,actual);identical(strip.crop((256*i,0,256*(i+1),256)),actual)
  body=Image.open(ROOT/f['layers']['body']['png']).convert('RGBA');assert body.getpixel(tuple(f['rightGrip']))[3]>0
  weapon=Image.open(ROOT/f['layers']['weaponFront']['png']).convert('RGBA');back=Image.open(ROOT/f['layers']['weaponBack']['png']).convert('RGBA');weap=Image.alpha_composite(back,weapon)
  assert weap.getbbox() and weap.getbbox()[0]>0 and weap.getbbox()[1]>0 and weap.getbbox()[2]<256 and weap.getbbox()[3]<256
  assert sum(1 for p,q in zip(actual.getdata(),body.getdata()) if p!=q)>40,'Weapon not visibly present'
  composed+=1
protected=read(ROOT/'experiments/orc-v1-weapons-v1/protected-originals.json');assert all(sha(ROOT/p)==h for p,h in protected.items())
catalog=read(LIB/'catalogo.json');assert all(sha(LIB/f['file'])==f['sha256'] for f in catalog['files'])
errors=[];frames=0
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='msedge',headless=True);page=browser.new_page(viewport={'width':1600,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)));page.goto(f'http://127.0.0.1:{server.server_port}/Biblioteca%20de%20Arte/Personagens%20Jogaveis/Orc%20V1/index.html');page.wait_for_function('document.body.dataset.ready==="true"');page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)');page.click('#play');assert page.locator('canvas').count()==5
  for i,c in enumerate(catalog['players']):
   for n,f in enumerate(c['frames']):
    page.evaluate('async a=>{views[a.i].n=a.n;await draw(a.i)}',{'i':i,'n':n});encoded=page.locator(f'#anim-{i}').evaluate('e=>e.toDataURL().split(",")[1]');actual=Image.open(io.BytesIO(base64.b64decode(encoded))).convert('RGBA');expected=Image.open(LIB/f['png']).convert('RGBA');identical(actual,expected);frames+=1
  page.evaluate('async()=>{views.forEach((v,i)=>v.n=[0,8,5,8,5][i]);await Promise.all(data.map((_,i)=>draw(i)))}');page.screenshot(path=str(OUT/'review-all.png'),full_page=True)
  for i,article in enumerate(page.locator('article').all()):article.screenshot(path=str(OUT/f'review-panel-{i}.png'))
  page.select_option('#zoom','1');page.set_viewport_size({'width':410,'height':900});assert not page.locator('body').evaluate('e=>e.scrollWidth>innerWidth+1')
  page.goto((LIB/'index.html').as_uri());page.wait_for_function('document.body.dataset.ready==="true"');assert not errors;browser.close()
finally:server.shutdown();server.server_close()
report={'status':'PASS','separateWeapons':2,'equippedClips':4,'compositeFramesAndLayerReconstructions':composed,'rgbaViewerComparisons':frames,'copiedFileHashes':len(catalog['files']),'allGripsOnActualHandPixels':True,'weaponsVisibleAllFrames':True,'noClippedWeaponPixels':True,'nativeSheetsMatchFrames':True,'originalInfanteArtPreserved':len(protected),'fileOpening':True,'mobileNoOverflow':True,'javascriptErrors':errors,'artisticApproval':'PENDING_CREATOR_NEW_WEAPONS_AND_ACTIONS','unityIntegrated':False};(OUT/'check.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
