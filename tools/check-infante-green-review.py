from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from PIL import Image
import json,hashlib,threading,base64,io
root=Path(__file__).resolve().parents[1];folder=root/'Biblioteca de Arte/Estudos Comparativos/Infante de Ferro - Pele Verde';data=json.loads((folder/'catalogo.json').read_text(encoding='utf-8'));out=root/'reports/infante-green-skin-v1';errors=[];compared=0
for f in data['files']:
 assert hashlib.sha256((folder/f['file']).read_bytes()).hexdigest()==f['sha256']
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='msedge',headless=True);page=browser.new_page(viewport={'width':1450,'height':900});page.on('pageerror',lambda e:errors.append(str(e)));page.goto(f'http://127.0.0.1:{server.server_port}/Biblioteca%20de%20Arte/Estudos%20Comparativos/Infante%20de%20Ferro%20-%20Pele%20Verde/index.html');page.wait_for_function('document.body.dataset.ready==="true"');page.click('#play');assert page.locator('canvas').count()==4
  for i,c in enumerate(data['variants']):
   for n,f in enumerate(c['frames']):
    page.evaluate('async a=>{views[a.i].frame=a.n;await draw(a.i)}',{'i':i,'n':n});encoded=page.locator(f'#anim-{i}').evaluate('e=>e.toDataURL().split(",")[1]');actual=Image.open(io.BytesIO(base64.b64decode(encoded))).convert('RGBA');expected=Image.open(folder/f['png']).convert('RGBA');assert actual.size==expected.size
    for a,b in zip(actual.getdata(),expected.getdata()):assert a[3]==b[3] and (not b[3] or a[:3]==b[:3])
    compared+=1
  page.evaluate('async()=>{views.forEach((v,i)=>v.frame=2);await Promise.all(data.map((_,i)=>draw(i)))}');page.screenshot(path=str(out/'comparison.png'),full_page=True);page.select_option('#zoom','1');assert page.locator('canvas').first.evaluate('e=>e.getBoundingClientRect().width')==128;page.screenshot(path=str(out/'native-size.png'),full_page=True)
  page.set_viewport_size({'width':410,'height':900});assert not page.locator('body').evaluate('e=>e.scrollWidth>innerWidth+1')
  page.goto((folder/'index.html').as_uri());page.wait_for_function('document.body.dataset.ready==="true"');assert not errors;browser.close()
finally:server.shutdown();server.server_close()
report={'status':'PASS','variants':4,'frames':[len(c['frames']) for c in data['variants']],'cyclesMs':[c['cycleMs'] for c in data['variants']],'rgbaComparisons':compared,'copiedArtHashes':len(data['files']),'native128Preview':True,'fileOpening':True,'mobileNoOverflow':True,'javascriptErrors':errors,'artisticApproval':'APPROVED_CREATOR_IDLE_REFERENCE' if any(c.get('selected') for c in data['variants']) else 'PENDING_CREATOR'};(out/'viewer-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
