from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from PIL import Image
import threading,json,hashlib
root=Path.cwd();E=root/'experiments/main-orc-combat-recovery-v7/rear-alt'
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start();errors=[];checks=[]
try:
 with sync_playwright() as p:
  b=p.chromium.launch(channel='msedge',headless=True);page=b.new_page(viewport={'width':1500,'height':1100});page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/experiments/main-orc-combat-recovery-v7/rear-alt/preview.html');page.wait_for_function('loaded===true')
  for pose in ['apex','impact']:
   page.select_option('#pose',pose)
   for mode in ['body','composite']:
    page.select_option('#mode',mode)
    rendered=page.evaluate('''async()=>Promise.all(['before','after'].map(async id=>{const c=document.querySelector('#'+id),bytes=c.getContext('2d').getImageData(0,0,256,256).data;const h=await crypto.subtle.digest('SHA-256',bytes);return {source:c.dataset.source,hash:Array.from(new Uint8Array(h)).map(x=>x.toString(16).padStart(2,'0')).join('')}}))''')
    for r in rendered:assert hashlib.sha256(Image.open((E/r['source']).resolve()).convert('RGBA').tobytes()).hexdigest()==r['hash']
    checks.append({'pose':pose,'mode':mode,'exactRgbaCanvases':2})
   page.wait_for_function('Array.from(document.images).every(im=>im.complete && im.naturalWidth>0)')
  page.select_option('#zoom','0.5');assert page.locator('#after').evaluate('c=>c.style.width')=='128px'
  page.select_option('#zoom','2');assert page.locator('#after').evaluate('c=>c.style.width')=='512px'
  page.select_option('#zoom','1');page.select_option('#pose','apex');page.screenshot(path=str(E/'preview-check.png'),full_page=True)
  assert not errors,errors
  page.goto((E/'preview.html').as_uri());page.wait_for_function('loaded===true');assert not errors
  b.close()
finally:server.shutdown();server.server_close()
(E/'browser-check.json').write_text(json.dumps({'status':'PASS','canvasComparisons':8,'checks':checks,'allAnnotationsLoaded':True,'httpAndFile':True,'zoomAndTactical':True,'jsErrors':errors},indent=2))
print('PASS 8 exact canvas comparisons, annotations, HTTP/file, zoom/tactical')
