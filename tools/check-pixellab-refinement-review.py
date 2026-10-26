"""Review presentation and native visible pixels; never modify source artwork."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json, threading
from PIL import Image
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
errors=[];exact=0
def compare(page,selector,png):
    global exact
    actual=bytes(page.locator(selector).evaluate('e=>Array.from(e.getContext("2d").getImageData(0,0,128,128).data)'))
    expected=Image.open(root/png).convert('RGBA').tobytes()
    assert len(actual)==len(expected)==128*128*4
    for p in range(0,len(actual),4):
        assert actual[p+3]==expected[p+3],(png,p,'alpha')
        if expected[p+3]: assert actual[p:p+3]==expected[p:p+3],(png,p,'visible RGB')
    exact+=1
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge',headless=True)
        page=browser.new_page(viewport={'width':1680,'height':1050},device_scale_factor=1)
        page.on('pageerror',lambda e:errors.append(str(e)))
        gallery='reports/orc-pixellab-v4-comparison'
        data=json.loads((root/gallery/'comparison.json').read_text(encoding='utf-8'))
        page.goto(f'http://127.0.0.1:{server.server_port}/{gallery}/review.html',wait_until='networkidle')
        page.wait_for_function('document.body.dataset.ready==="true"')
        assert page.locator('img').evaluate_all('es=>es.every(e=>e.complete&&e.naturalWidth>0)')
        page.click('#play')
        for i,card in enumerate(data['cards']):
            for state,clip in card['clips'].items():
                if not clip: continue
                for f,frame in enumerate(clip['frames']):
                    page.evaluate('async a=>{views[a.i]={mode:a.state,frame:a.f,elapsed:0};await draw(a.i)}',{'i':i,'state':state,'f':f})
                    compare(page,f'#anim-{i}',frame['png'])
        for i in range(len(data['cards'])):
            page.select_option(f'#mode-{i}','Concept')
        page.select_option('#bg','checker')
        page.screenshot(path=str(root/gallery/'refined-gallery.png'),full_page=True)
        page.select_option('#zoom','1')
        page.select_option('#mode-3','Walk')
        assert page.locator('#anim-3').evaluate('e=>e.getBoundingClientRect().width')==128
        page.select_option('#bg','light');assert page.locator('body').evaluate('e=>e.classList.contains("light")')
        refinement='reports/orc-pixellab-refinement-v2'
        pairs=json.loads((root/refinement/'comparison.json').read_text(encoding='utf-8'))['pairs']
        page.goto(f'http://127.0.0.1:{server.server_port}/{refinement}/review.html',wait_until='networkidle');page.click('#play')
        for i,pair in enumerate(pairs):
            for mode in ['Concept','Idle','Walk']:
                for side in ['before','after']:
                    version=pair[side]
                    frames=[{'png':version['concept']}] if mode=='Concept' else version['clips'][mode]['frames']
                    for f,frame in enumerate(frames):
                        page.evaluate('async a=>{views[a.i].mode=a.mode;views[a.i][a.side].frame=a.f;await draw(a.i,a.side)}',{'i':i,'mode':mode,'side':side,'f':f})
                        compare(page,f'#{side}-{i}',frame['png'])
        for i in range(len(pairs)): page.select_option(f'#mode-{i}','Walk')
        page.screenshot(path=str(root/refinement/'before-after-walk.png'),full_page=True)
        for i in range(len(pairs)): page.select_option(f'#mode-{i}','Idle')
        page.set_viewport_size({'width':410,'height':900})
        assert page.locator('body').evaluate('e=>e.scrollWidth<=innerWidth+1')
        page.screenshot(path=str(root/refinement/'mobile-idle.png'),full_page=True)
        page.goto((root/refinement/'review.html').as_uri(),wait_until='networkidle')
        assert page.locator('canvas').count()==8
        assert not errors,errors
        browser.close()
finally:
    server.shutdown();server.server_close()
result={'status':'PASS','visibleRgbaCanvasComparisons':exact,'galleryCards':len(data['cards']),'beforeAfterPairs':len(pairs),'javascriptErrors':errors,'mobileLayout':'PASS','filePageLoad':'PASS','artisticApproval':'PENDING_CREATOR'}
(root/'reports/orc-pixellab-refinement-review-check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
