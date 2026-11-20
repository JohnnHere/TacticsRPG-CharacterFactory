from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import threading,json,hashlib
from PIL import Image
from playwright.sync_api import sync_playwright
root=Path.cwd();E=root/'experiments/main-orc-combat-recovery-v8/rear';spec=json.loads((E/'temporal-spec.json').read_text())
ThreadingHTTPServer.request_queue_size=128
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start();errors=[];checks=[];exact=0;boundaries=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='msedge',headless=True);page=browser.new_page(viewport={'width':1500,'height':1100});page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/experiments/main-orc-combat-recovery-v8/rear/preview.html',wait_until='networkidle');page.wait_for_function('window.loaded===true');page.evaluate('setFrame(0)')
  for kind,s in spec.items():
   page.select_option('#kind',kind)
   for body in [False,True]:
    page.locator('#body').set_checked(body)
    for i in range(s['frameCount']):
     page.evaluate('i=>setFrame(i)',i)
     rendered=page.evaluate('''async()=>Promise.all(views.map(async v=>{const bytes=v.c.getContext('2d').getImageData(0,0,256,256).data;const h=await crypto.subtle.digest('SHA-256',bytes);return{direction:v.dir,frame:+v.c.dataset.frame,phase:v.c.dataset.phase,source:v.c.dataset.source,hash:Array.from(new Uint8Array(h)).map(x=>x.toString(16).padStart(2,'0')).join('')}}))''')
     for r in rendered:
      assert r['frame']==i and r['phase']==s['phases'][i]['phase'];assert hashlib.sha256(Image.open((E/r['source']).resolve()).convert('RGBA').tobytes()).hexdigest()==r['hash'];exact+=1
     checks.append({'kind':kind,'frame':i,'bodyOnly':body,'exactCanvases':4,'phaseAndIndexMatch':True})
   page.locator('#body').uncheck()
   for t,want in [(s['impactStartMs']-.001,s['impactFrame']-1),(s['impactStartMs'],s['impactFrame']),(s['phases'][s['impactFrame']]['endMs'],s['impactFrame']+1)]:
    page.evaluate('t=>setTime(t)',t);got=page.locator('canvas').evaluate_all('(cs)=>cs.map(c=>+c.dataset.frame)');assert got==[want]*4,(kind,t,got);boundaries.append({'kind':kind,'timeMs':t,'allFourFrames':got})
   page.click('#impact');assert page.locator('canvas.impact').count()==4;page.screenshot(path=str(E/(kind.lower()+'-impact-1x.png')))
   page.select_option('#zoom','0.5');assert page.locator('canvas').first.evaluate('c=>c.style.width')=='128px';page.screenshot(path=str(E/(kind.lower()+'-impact-tactical.png')))
   page.select_option('#zoom','2');assert page.locator('canvas').first.evaluate('c=>c.style.width')=='512px';page.select_option('#zoom','1')
   page.evaluate('setFrame(0)');page.select_option('#speed','0.5');page.click('#play');page.wait_for_timeout(400);assert 110<=page.evaluate('elapsed')<=290;page.click('#play');page.select_option('#speed','1');page.evaluate('setFrame(0)');page.click('#play');page.wait_for_timeout(300);assert 190<=page.evaluate('elapsed')<=450;page.click('#play')
   page.evaluate('setFrame(0)');page.locator('#repeat').uncheck();page.click('#play');page.wait_for_function('playing===false',timeout=3500);assert page.evaluate('index()')==s['frameCount']-1;page.locator('#repeat').check();page.click('#next');assert page.evaluate('index()')==0;page.click('#prev');assert page.evaluate('index()')==s['frameCount']-1
   page.click('#impact');page.wait_for_function('Array.from(document.images).every(im=>im.complete&&im.naturalWidth>0)');page.screenshot(path=str(E/(kind.lower()+'-preview-check.png')),full_page=True)
  assert not errors,errors
  page.goto((E/'preview.html').as_uri(),wait_until='networkidle');page.wait_for_function('window.loaded===true');assert not errors
  browser.close()
finally:server.shutdown();server.server_close()
(E/'browser-check.json').write_text(json.dumps({'status':'PASS','exactCanvasComparisons':exact,'checks':checks,'impactBoundaryChecks':boundaries,'sharedClockFourDirections':True,'normalAndHalfSpeed':True,'stepZoomTacticalBodyAndComposite':True,'oneShotAndRepeat':True,'httpAndFile':True,'jsErrors':errors},indent=2))
print('PASS',exact,'canvas comparisons; impact325/410 synchronized in four directions; controls and HTTP/file')
