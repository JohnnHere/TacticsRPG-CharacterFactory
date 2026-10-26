"""Validate generated-art presentation; no source pixels are modified."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json, threading
from PIL import Image
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'reports/pixellab-orcs-independent-v1.json').read_text(encoding='utf-8'))
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
errors=[];exact=0
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge',headless=True)
        page=browser.new_page(viewport={'width':1500,'height':1100},device_scale_factor=1)
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(f'http://127.0.0.1:{server.server_port}/reports/pixellab-orcs-independent-v1/review.html',wait_until='networkidle')
        page.wait_for_function('document.body.dataset.ready==="true"')
        page.click('#pause')
        for i,c in enumerate(data['cards']):
            rgba=bytes(page.locator(f'#canvas-{i}').evaluate('e=>Array.from(e.getContext("2d").getImageData(0,0,128,128).data)'))
            assert rgba==Image.open(root/c['concept']).convert('RGBA').tobytes();exact+=1
        page.locator('#options').screenshot(path=str(root/'reports/pixellab-orcs-independent-v1/three-concepts.png'))
        for i,c in enumerate(data['cards']):
            for state,clip in c['clips'].items():
                page.select_option(f'#state-{i}',state)
                for frame in clip['frames']:
                    rgba=bytes(page.locator(f'#canvas-{i}').evaluate('e=>Array.from(e.getContext("2d").getImageData(0,0,128,128).data)'))
                    assert rgba==Image.open(root/frame['png']).convert('RGBA').tobytes();exact+=1
                    page.click('#step')
        for i,c in enumerate(data['cards']):
            if 'Walk' in c['clips']:page.select_option(f'#state-{i}','Walk')
        page.screenshot(path=str(root/'reports/pixellab-orcs-independent-v1/review-screenshot.png'),full_page=True)
        page.select_option('#zoom','1')
        assert page.locator('#canvas-0').evaluate('e=>e.getBoundingClientRect().width')==128
        page.select_option('#background','checker');assert page.locator('body').evaluate('e=>e.classList.contains("checker")')
        assert not errors,errors
        browser.close()
finally:
    server.shutdown();server.server_close()
result={'status':'PASS','concepts':3,'animationStudies':data['animationStudies'],'exactCanvasComparisons':exact,'javascriptErrors':errors,'artisticApproval':'PENDING_CREATOR'}
(root/'reports/pixellab-orcs-review-check.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
