from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import threading,json,hashlib
from PIL import Image
from playwright.sync_api import sync_playwright
root=Path.cwd();E=root/'experiments/main-orc-combat-recovery-v7/rear-alt/full-cycle';P=E.parent
ThreadingHTTPServer.request_queue_size=128
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start();errors=[];checks=[];exact=0
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='msedge',headless=True);page=browser.new_page(viewport={'width':1500,'height':1150});page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/experiments/main-orc-combat-recovery-v7/rear-alt/preview.html',wait_until='networkidle');page.wait_for_function('window.loaded===true');page.evaluate('setFrame(0)')
  for kind in ['Sword','Axe']:
   page.select_option('#kind',kind)
   for body in [False,True]:
    page.locator('#body').set_checked(body)
    for i in range(15):
     page.evaluate('i=>setFrame(i)',i)
     rendered=page.evaluate('''async()=>Promise.all(views.map(async v=>{const bytes=v.c.getContext('2d').getImageData(0,0,256,256).data;const h=await crypto.subtle.digest('SHA-256',bytes);return {role:v.role,frame:+v.c.dataset.frame,source:v.c.dataset.source,hash:Array.from(new Uint8Array(h)).map(x=>x.toString(16).padStart(2,'0')).join('')}}))''')
     for r in rendered:
      im=Image.open((P/r['source']).resolve()).convert('RGBA');assert im.size==(256,256);assert hashlib.sha256(im.tobytes()).hexdigest()==r['hash'],(kind,i,r['role']);exact+=1
     checks.append({'kind':kind,'candidateFrame':i,'bodyOnly':body,'exactCanvases':4})
   page.locator('#body').uncheck();page.select_option('#sync','own');page.evaluate('setFrame(9)');assert page.locator('canvas[data-role=candidate]').get_attribute('data-frame')=='9'
   page.select_option('#sync','phase');page.select_option('#zoom','0.5');assert page.locator('canvas').first.evaluate('c=>c.style.width')=='128px';page.screenshot(path=str(E/(kind.lower()+'-tactical-check.png')))
   page.select_option('#zoom','2');assert page.locator('canvas').first.evaluate('c=>c.style.width')=='512px';page.select_option('#zoom','1');page.locator('#joints').check();page.evaluate('setFrame(6)');page.wait_for_function('Array.from(document.images).every(im=>im.complete && im.naturalWidth>0)');page.screenshot(path=str(E/(kind.lower()+'-joints-check.png')));page.locator('#joints').uncheck()
   page.evaluate('setFrame(0)');page.select_option('#speed','0.5');page.click('#play');page.wait_for_timeout(400);elapsed=page.evaluate('elapsed');assert 120<=elapsed<=290,elapsed;page.click('#play');page.select_option('#speed','1')
   page.evaluate('setFrame(0)');page.locator('#repeat').uncheck();page.click('#play');page.wait_for_function('playing===false',timeout=4000);assert page.evaluate('index()')==14
   page.locator('#repeat').check();page.click('#next');assert page.evaluate('index()')==0;page.click('#prev');assert page.evaluate('index()')==14
   page.evaluate('setFrame(6)');page.screenshot(path=str(E/(kind.lower()+'-preview-check.png')),full_page=True)
  assert not errors,errors
  page.goto((P/'preview.html').as_uri(),wait_until='networkidle');page.wait_for_function('window.loaded===true');assert not errors
  browser.close()
finally:server.shutdown();server.server_close()
(E/'browser-check.json').write_text(json.dumps({'status':'PASS','exactCanvasComparisons':exact,'checks':checks,'phaseAlignedAndOwnTiming':True,'normalAndHalfSpeed':True,'oneShotHoldAndRepeatBoundary':True,'stepZoomTacticalBodyAndComposite':True,'jointsAnnotation':True,'allEvidenceImagesLoaded':True,'httpAndFile':True,'jsErrors':errors},indent=2))
print('PASS',exact,'exact canvas comparisons; all controls, timings, HTTP/file; no JS errors')
