"""Asset presentation inspection: all native PNGs, real playback and all candidates."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import json,base64,io,threading
from PIL import Image
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];lib=root/'Biblioteca de Arte';out=root/'reports/orc-athletic-feet-v2';catalog=json.loads((lib/'catalogo.json').read_text(encoding='utf-8'));data={'cards':catalog['current']};errors=[];compared=0

import hashlib
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
for asset in catalog['files']:
 if hashlib.sha256((lib/asset['file']).read_bytes()).hexdigest()!=asset['sha256']:raise RuntimeError('Library copy hash mismatch '+asset['file'])
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  for key,value in attrs:
   if key in ['href','src'] and value:self.links.append(value)
linkCount=0
for pageFile in lib.rglob('*.html'):
 links=Links();links.feed(pageFile.read_text(encoding='utf-8'))
 for value in links.links:
  url=urlsplit(value)
  if url.scheme or not url.path:continue
  target=(pageFile.parent/unquote(url.path)).resolve()
  if not target.exists():raise RuntimeError('Broken library link '+str(pageFile)+' '+value)
  if not target.is_relative_to(lib.resolve()):raise RuntimeError('Library link requires external workspace '+value)
  linkCount+=1

class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  b=p.chromium.launch(channel='msedge',headless=True);page=b.new_page(viewport={'width':1460,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)));page.goto(f'http://127.0.0.1:{server.server_port}/Biblioteca%20de%20Arte/index.html',wait_until='networkidle');page.wait_for_function('document.body.dataset.ready==="true"');page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)');page.click('#play')
  for i,c in enumerate(data['cards']):
   for state,clip in c['clips'].items():
    if not clip:continue
    for n,f in enumerate(clip['frames']):
     page.evaluate('async a=>{const v=views.find(v=>v.i===a.i&&v.state===a.state);v.frame=a.n;await draw(v)}',{'i':i,'state':state,'n':n})
     encoded=page.locator(f'#anim-{i}-{state}').evaluate('e=>e.toDataURL().split(",")[1]');a=Image.open(io.BytesIO(base64.b64decode(encoded))).convert('RGBA');z=Image.open(lib/f['png']).convert('RGBA')
     if a.size!=z.size:raise RuntimeError('Canvas dimensions changed')
     for aa,zz in zip(a.getdata(),z.getdata()):
      if aa[3]!=zz[3] or (zz[3] and aa[:3]!=zz[:3]):raise RuntimeError('Canvas pixel mismatch '+f['png'])
     compared+=1
  page.evaluate('async()=>{for(const v of views){v.frame=0;v.time=0;}await Promise.all(views.map(draw))}');page.click('#play');page.wait_for_timeout(390);page.click('#play');page.locator('#orc-pixellab-11').screenshot(path=str(out/'library-athletic.png'));page.locator('#orc-pixellab-10').screenshot(path=str(out/'library-long-haired.png'));page.screenshot(path=str(out/'library-all-orcs.png'),full_page=True)
  if len(data['cards'])!=len(json.loads((root/'reports/orc-study-selection.json').read_text(encoding='utf-8'))['currentCandidates']) or page.locator('canvas').count()!=sum(bool(v) for c in data['cards'] for v in c['clips'].values()) or page.locator('img').count()!=len(data['cards']):raise RuntimeError('Missing candidate/state in combined review')
  page.set_viewport_size({'width':410,'height':900});page.locator('#orc-pixellab-11').scroll_into_view_if_needed();page.locator('#orc-pixellab-11').screenshot(path=str(out/'library-mobile.png'))
  if page.locator('body').evaluate('e=>e.scrollWidth>innerWidth+1'):raise RuntimeError('Mobile overflow')
  if any(c['id'] in ['orc-01','orc-pixellab-07','orc-pixellab-08','orc-pixellab-09'] for c in data['cards']):raise RuntimeError('Discarded or reserved idea in current gallery')
  page.goto(f'http://127.0.0.1:{server.server_port}/Biblioteca%20de%20Arte/Ideias%20Futuras/index.html',wait_until='networkidle');page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
  if page.locator('img').count()!=2:raise RuntimeError('Reserved ideas missing')
  page.goto((lib/'index.html').as_uri(),wait_until='networkidle');page.wait_for_function('document.body.dataset.ready==="true"')
  if errors:raise RuntimeError(str(errors))
  b.close()
finally:server.shutdown();server.server_close()
report={'status':'PASS','options':len(data['cards']),'concepts':len(data['cards']),'animatedClips':sum(bool(v) for c in data['cards'] for v in c['clips'].values()),'rgbaComparisons':compared,'includesLongHairedInfante':True,'reservedUniqueCharactersSeparate':True,'discardedV4Hidden':True,'unproducedAnimationsSimulated':False,'javascriptErrors':errors,'fileOpening':'PASS','selfContained':True,'copiedAssetHashesVerified':len(catalog['files']),'localLinksVerified':linkCount,'mobileLayout':'PASS','artisticApproval':'PENDING_CREATOR'};(root/'reports/art-library-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
