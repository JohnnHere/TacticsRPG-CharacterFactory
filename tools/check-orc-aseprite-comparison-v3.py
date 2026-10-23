"""Inspect the comparison in isolated Edge; validation only, no art editing."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import hashlib,json,threading
from PIL import Image
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'reports/orc-aseprite-comparison-v3.json').read_text(encoding='utf-8'))
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
def pixels(page,selector):return bytes(page.locator(selector).evaluate('e=>Array.from(e.getContext("2d").getImageData(0,0,128,128).data)'))
def expected(file):return Image.open(root/file).convert('RGBA').tobytes()
errors=[];exact=0;layer_checks=0
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge',headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto((root/'reports/orc-aseprite-v3/review.html').as_uri(),wait_until='networkidle')
        page.wait_for_function('document.body.dataset.ready==="true"')
        assert page.locator('#conceptBefore').evaluate('e=>e.complete&&e.naturalWidth>0')
        assert page.locator('#conceptAfter').evaluate('e=>e.complete&&e.naturalWidth===128')
        page.select_option('#clip','Hit');page.wait_for_function('document.querySelector("#frame").max==="2"')
        page.goto(f'http://127.0.0.1:{server.server_port}/reports/orc-aseprite-v3/review.html',wait_until='networkidle')
        page.wait_for_function('document.body.dataset.ready==="true"')
        components=sorted((root/'characters/orc-01-aseprite-v3/source/aseprite/components').rglob('*.png'))
        paths=[str(f.relative_to(root)).replace('\\','/') for f in components]
        loaded=page.evaluate('''async paths=>await Promise.all(paths.map(p=>new Promise(resolve=>{const i=new Image();i.onload=()=>resolve([i.naturalWidth,i.naturalHeight]);i.onerror=()=>resolve(null);i.src='../../'+p})))''',paths)
        assert len(loaded)==81 and all(x==[128,128] for x in loaded)
        for clip in data['clips']:
            page.select_option('#clip',clip['state'])
            for index,file in enumerate(clip['after']):
                page.locator('#frame').evaluate('(e,v)=>{e.value=v;e.dispatchEvent(new Event("input"))}',index)
                page.wait_for_timeout(100)
                assert pixels(page,'#after')==expected(file),file
                assert pixels(page,'#before')==expected(clip['before'][index]),clip['before'][index]
                exact+=2
        page.select_option('#clip','Attack')
        page.locator('#frame').evaluate('(e)=>{e.value=2;e.dispatchEvent(new Event("input"))}')
        page.click('#onlyHead');page.wait_for_timeout(120)
        assert pixels(page,'#after')==expected('characters/orc-01-aseprite-v3/source/aseprite/components/attack/layer-07-frame-02.png');layer_checks+=1
        page.click('#onlyArm');page.wait_for_timeout(120)
        assert pixels(page,'#after')==expected('characters/orc-01-aseprite-v3/source/aseprite/components/attack/layer-09-frame-02.png');layer_checks+=1
        page.click('#all');page.wait_for_timeout(100)
        assert pixels(page,'#after')==expected(data['clips'][0]['after'][2]);layer_checks+=1
        page.select_option('#zoom','1');assert page.locator('#after').evaluate('e=>e.style.width')=='128px'
        page.select_option('#zoom','4');page.select_option('#speed','0.5');page.click('#background');page.click('#background')
        page.screenshot(path=str(root/'reports/orc-aseprite-v3/review-screenshot.png'),full_page=True)
        page.locator('.pair').nth(1).screenshot(path=str(root/'reports/orc-aseprite-v3/native-comparison.png'))
        page.click('#play');page.wait_for_timeout(130);page.click('#play')
        assert not errors,errors
        version=browser.version;browser.close()
finally:server.shutdown();server.server_close()
report={'status':'PASS','browser':'Microsoft Edge headless','version':version,'modes':['file:// display','loopback HTTP exact canvas pixels'],'layerImagesLoaded':len(loaded),'exactNativeComparisons':exact,'layerCompositionsExact':layer_checks,'controls':['clip','pause/play','frame','zoom1x/4x','speed','background','head only','arm only','all layers'],'javascriptErrors':errors,'V3ArtisticApproval':'PENDING_CREATOR','UnityPlayMode':'NOT_RUN'}
(root/'reports/orc-aseprite-comparison-check-v3.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
