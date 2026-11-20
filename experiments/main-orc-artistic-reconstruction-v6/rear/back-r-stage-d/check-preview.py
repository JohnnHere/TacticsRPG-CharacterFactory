from pathlib import Path
import json,hashlib
import threading
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from PIL import Image
from playwright.sync_api import sync_playwright
O=Path(__file__).parent.resolve()
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Quiet)
threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True)
 page=b.new_page(viewport={'width':1600,'height':1000})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((O/'preview.html').as_uri())
 page.wait_for_function('current.length===4')
 page.goto(f'http://127.0.0.1:{server.server_port}/experiments/main-orc-artistic-reconstruction-v6/rear/back-r-stage-d/preview.html')
 for kind in ['Sword','Axe']:
  page.select_option('#family',kind)
  page.wait_for_function('current.length===4 && current.every(v=>v.c.category===family.value&&v.imgs.every(i=>i.complete&&i.naturalWidth===256))')
  page.evaluate("playing=true;play.textContent='Pausar';time=0;speed.value='1';zoom.value='1'")
  start=page.evaluate('time');page.wait_for_timeout(3000);delta=page.evaluate('time')-start;assert delta>2800
  page.screenshot(path=str(O/f'{kind.lower()}-playback-1x.png'),full_page=True)
  page.select_option('#zoom','0.5');page.wait_for_timeout(1800)
  page.screenshot(path=str(O/f'{kind.lower()}-playback-tactical.png'),full_page=True)
  page.select_option('#zoom','2');page.select_option('#speed','0.5');page.wait_for_timeout(2400)
  page.screenshot(path=str(O/f'{kind.lower()}-playback-half-speed.png'),full_page=True)
  exact=0
  for i in range(12):
   page.evaluate('(i)=>{playing=false;manual=i;draw()}',i)
   hashes=page.evaluate("async()=>Promise.all(current.slice(2).map(async(v)=>{const d=v.cv.getContext('2d').getImageData(0,0,256,256).data;const h=await crypto.subtle.digest('SHA-256',d);return Array.from(new Uint8Array(h)).map(x=>x.toString(16).padStart(2,'0')).join('')}))")
   for h,mode in zip(hashes,['layers/body','frames']):
    im=Image.open(Path('characters/orc-v1/source/artistic-reconstruction-v6/rear')/f'back_r-{kind.lower()}'/mode/f'{i:02}.png').convert('RGBA')
    assert h==hashlib.sha256(im.tobytes()).hexdigest(),(kind,i,mode)
    exact+=1
  page.click('#step');assert page.evaluate('manual')==0
  results.append({'category':kind,'imagesLoaded':True,'exactCanvasFrames':exact,'oneXClockDeltaMsOver3s':delta,'halfSpeedAndTacticalScale':True,'stepWrap':True})
 assert not errors,errors
 b.close()
(O/'preview-check.json').write_text(json.dumps({'status':'TECHNICALLY_COMPLETE','checks':results,'jsErrors':errors,'note':'Playback was exercised at normal/half speed and native/tactical scale. Functional checks do not grant artistic approval.'},indent=2),encoding='utf-8')
print('Preview checks complete:',results)
