"""Inspect local review pixels, playback and layout; no artwork changes."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import json,threading,base64,io
from PIL import Image
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];report=root/'reports/orc-pixellab-refinement-v4';data=json.loads((report/'comparison.json').read_text(encoding='utf-8'));errors=[];compared=0
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='msedge',headless=True);page=browser.new_page(viewport={'width':1440,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)));page.goto(f'http://127.0.0.1:{server.server_port}/reports/orc-pixellab-refinement-v4/review.html',wait_until='networkidle');page.click('#play')
  for i,pair in enumerate(data['pairs']):
   for mode in ['Concept','Idle','Walk']:
    for side in ['before','after']:
     frames=[{'png':pair[side]['concept']}] if mode=='Concept' else pair[side]['clips'][mode]['frames']
     for f,frame in enumerate(frames):
      page.evaluate('async a=>{views[a.i].mode=a.mode;views[a.i][a.side].frame=a.f;await draw(a.i,a.side)}',{'i':i,'mode':mode,'side':side,'f':f})
      png=page.locator(f'#{side}-{i}').evaluate('e=>e.toDataURL().split(",")[1]');actual=Image.open(io.BytesIO(base64.b64decode(png))).convert('RGBA');expected=Image.open(root/frame['png']).convert('RGBA')
      assert actual.size==expected.size==(128,128)
      for a,b in zip(actual.getdata(),expected.getdata()):
       assert a[3]==b[3] and (not b[3] or a[:3]==b[:3]),frame['png']
      compared+=1
  for i in range(len(data["pairs"])):page.select_option(f'#mode-{i}','Walk')
  page.screenshot(path=str(report/'walk-before-after.png'),full_page=True)
  for i in range(len(data["pairs"])):page.select_option(f'#mode-{i}','Idle')
  page.screenshot(path=str(report/'idle-before-after.png'),full_page=True)
  page.click('#play');a=page.evaluate('views[0].after.frame');page.wait_for_timeout(450);b=page.evaluate('views[0].after.frame');assert a!=b,'Playback did not advance';page.click('#play')
  page.click('#step');assert page.locator('#play').inner_text()=='Reproduzir'
  page.set_viewport_size({'width':410,'height':900});assert page.locator('body').evaluate('e=>e.scrollWidth<=innerWidth+1');page.screenshot(path=str(report/'mobile.png'),full_page=True)
  page.goto((report/'review.html').as_uri(),wait_until='networkidle');assert page.locator('img').evaluate_all('es=>es.every(e=>e.complete&&e.naturalWidth>0)');assert not errors,errors
  browser.close()
finally:server.shutdown();server.server_close()
result={'status':'PASS','visibleRgbaComparisons':compared,'playback':'ADVANCED','step':'PASS','mobile':'PASS','fileLoad':'PASS','javascriptErrors':errors,'artisticApproval':'PENDING_CREATOR'};(root/'reports/orc-pixellab-refinement-v4-review-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
