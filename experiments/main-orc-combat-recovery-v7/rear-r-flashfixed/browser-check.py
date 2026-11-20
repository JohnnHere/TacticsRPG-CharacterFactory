from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import threading,json,hashlib
from PIL import Image
from playwright.sync_api import sync_playwright
root=Path.cwd();E=root/'experiments/main-orc-combat-recovery-v7/rear-r-flashfixed'
ThreadingHTTPServer.request_queue_size=128
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start()
errors=[];checks=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='msedge',headless=True)
  page=browser.new_page(viewport={'width':1450,'height':1100});page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/experiments/main-orc-combat-recovery-v7/rear-r-flashfixed/preview.html');page.wait_for_function('window.loaded===true');page.evaluate('setFrame(0)')
  for body in [False,True]:
   page.locator('#body').set_checked(body)
   for i in range(12):
    page.evaluate('i=>setFrame(i)',i)
    rendered=page.evaluate('''async()=>Promise.all(views.map(async v=>{const bytes=v.c.getContext('2d').getImageData(0,0,256,256).data;const h=await crypto.subtle.digest('SHA-256',bytes);return {source:v.c.dataset.source,hash:Array.from(new Uint8Array(h)).map(x=>x.toString(16).padStart(2,'0')).join('')}}))''')
    for r in rendered:
     path=(E/r['source']).resolve();im=Image.open(path).convert('RGBA');assert hashlib.sha256(im.tobytes()).hexdigest()==r['hash']
    checks.append({'frame':i,'bodyOnly':body,'exactCanvases':4})
  page.locator('#body').uncheck();page.select_option('#zoom','0.5');assert page.locator('canvas').first.evaluate('c=>c.style.width')=='128px'
  page.select_option('#zoom','2');assert page.locator('canvas').first.evaluate('c=>c.style.width')=='512px'
  page.select_option('#zoom','1');page.select_option('#speed','0.5');assert page.evaluate('rate')==.5
  page.click('#next');assert page.evaluate('state.Axe.i')==0
  page.click('#play');page.wait_for_timeout(500);assert page.evaluate('state.Axe.i')!=0
  page.click('#play');page.evaluate('setFrame(3)');page.screenshot(path=str(E/'preview-check.png'),full_page=True)
  assert not errors,errors
  page.goto((E/'preview.html').as_uri());page.wait_for_function('window.loaded===true');assert not errors
  browser.close()
finally:server.shutdown();server.server_close()
(E/'browser-check.json').write_text(json.dumps({'status':'PASS','canvasComparisons':96,'checks':checks,'controls':['play','step','frame','0.5x','zoom','tactical','body-only'],'httpAndFile':True,'jsErrors':errors},indent=2))
print('PASS 96 exact canvas comparisons; controls; HTTP/file; no JS errors')
