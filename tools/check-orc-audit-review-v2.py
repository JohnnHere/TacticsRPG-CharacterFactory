"""Read-only review checks in isolated headless Edge; no desktop interaction."""
from pathlib import Path
import hashlib
import json
import threading
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from PIL import Image
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
audit=json.loads((root/'reports/orc-assets-audit-v2.json').read_text(encoding='utf-8'))
candidates=json.loads((root/'reports/orc-refinement-candidates-v2.json').read_text(encoding='utf-8'))
errors=[]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((root/'reports/orc-audit-v2/review.html').as_uri(),wait_until='networkidle')
    page.wait_for_function('document.body.dataset.ready === "true"')
    # Load every unique PNG referenced by the audit plus all static/direction slots.
    files=sorted({str(x.relative_to(root)).replace('\\','/') for c in audit['classes'] for x in (root/'characters'/c['id']/'sprites').rglob('*.png')} | {f['file'] for c in audit['clips'] for f in c['frames']})
    loaded=page.evaluate('''async paths=>await Promise.all(paths.map(path=>new Promise(resolve=>{let i=new Image();i.onload=()=>resolve({path,width:i.naturalWidth,height:i.naturalHeight});i.onerror=()=>resolve({path,error:true});i.src='../../'+path})))''',files)
    assert len(loaded)==896 and all(x.get('width')==128 and x.get('height')==128 for x in loaded)
    for clip in audit['clips']:
        page.select_option('#job',clip['id']);page.select_option('#state',clip['state']);page.select_option('#view',clip['direction'])
        page.wait_for_function('(s)=>document.querySelector("#currentLabel").textContent.includes(s)',arg=clip['id']+' / '+clip['state']+' / '+clip['direction'])
    # file:// displays images, but browsers forbid reading local canvas pixels.
    # Verify exact pixels separately through a loopback HTTP origin.
    page.goto(f'http://127.0.0.1:{server.server_port}/reports/orc-audit-v2/review.html',wait_until='networkidle')
    page.wait_for_function('document.body.dataset.ready === "true"')
    page.click('#toggle') # pause the study
    exact=0
    for clip in candidates['clips']:
        page.select_option('#study',clip['state'])
        for index,file in enumerate(clip['after']):
            page.locator('#scrub').evaluate('(e,v)=>{e.value=v;e.dispatchEvent(new Event("input"))}',index)
            page.wait_for_timeout(65)
            rgba=bytes(page.evaluate('Array.from(document.querySelector("#after").getContext("2d").getImageData(0,0,128,128).data)'))
            expected=Image.open(root/file).convert('RGBA').tobytes()
            assert hashlib.sha256(rgba).digest()==hashlib.sha256(expected).digest(),file
            exact+=1
    page.select_option('#study','Attack');page.locator('#scrub').evaluate('(e)=>{e.value=2;e.dispatchEvent(new Event("input"))}')
    page.wait_for_timeout(70)
    page.screenshot(path=str(root/'reports/orc-audit-v2/review-screenshot.png'),full_page=True)
    assert not errors,errors
    version=browser.version;browser.close()
server.shutdown();server.server_close()
report={'status':'PASS','browser':'Microsoft Edge headless via Playwright','version':version,'modes':['file:// display and selections','loopback HTTP exact canvas pixels'],'nativeImagesLoaded':len(loaded),'libraryClipSelections':len(audit['clips']),'exactCandidateCanvasRgba':exact,'javascriptErrors':errors,'artisticApproval':'PENDING_CREATOR','UnityPlayMode':'NOT_RUN'}
(root/'reports/orc-audit-review-check-v2.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
