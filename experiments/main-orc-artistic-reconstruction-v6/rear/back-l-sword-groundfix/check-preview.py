from pathlib import Path
import json,hashlib,threading
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from PIL import Image
from playwright.sync_api import sync_playwright
O=Path(__file__).resolve().relative_to(Path.cwd().resolve()).parent
C=Path('characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword')
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Quiet);threading.Thread(target=server.serve_forever,daemon=True).start()
errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True);page=b.new_page(viewport={'width':1300,'height':900})
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((O/'preview.html').resolve().as_uri());page.wait_for_function('current.length===3')
 page.goto(f'http://127.0.0.1:{server.server_port}/{O.as_posix()}/preview.html')
 page.wait_for_function('current.length===3 && current.every(v=>v.imgs.every(i=>i.complete&&i.naturalWidth===256))')
 start=page.evaluate('time');page.wait_for_timeout(2400);normal=page.evaluate('time')-start;assert normal>2200
 page.select_option('#speed','0.5');start=page.evaluate('time');page.wait_for_timeout(1600);half=page.evaluate('time')-start;assert 700<half<950
 exact=0
 for i in range(12):
  page.evaluate('(i)=>{playing=false;manual=i;draw()}',i)
  hashes=page.evaluate("async()=>Promise.all(current.map(async(v)=>{const d=v.cv.getContext('2d').getImageData(0,0,256,256).data;const h=await crypto.subtle.digest('SHA-256',d);return Array.from(new Uint8Array(h)).map(x=>x.toString(16).padStart(2,'0')).join('')}))")
  paths=[O/'before/frames'/f'{i:02}.png',C/'frames'/f'{i:02}.png',C/'layers/body'/f'{i:02}.png']
  for h,path in zip(hashes,paths):assert h==hashlib.sha256(Image.open(path).convert('RGBA').tobytes()).hexdigest();exact+=1
  if i in [7,8,9]:page.screenshot(path=str(O/f'preview-F{i:02}.png'),full_page=True)
 page.click('#step');assert page.evaluate('manual')==0
 page.select_option('#zoom','0.5');page.screenshot(path=str(O/'preview-tactical.png'),full_page=True)
 assert not errors,errors
 b.close()
(O/'preview-check.json').write_text(json.dumps({'technicalStatus':'TECHNICALLY_COMPLETE','normalClockMsOver2400ms':normal,'halfClockMsOver1600ms':half,'exactCanvasRenders':exact,'localFileDisplay':True,'stepWrap':True,'tacticalScale':True,'jsErrors':errors,'note':'Functional playback and exact pixel checks; independent temporal QA remains required.'},indent=2),encoding='utf-8')
server.shutdown();server.server_close();print('Preview verified:',exact,'renders; normal',normal,'half',half)
