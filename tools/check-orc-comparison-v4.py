"""Validate comparison rendering and art invariants; never edits source art."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import json,threading
from PIL import Image
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'reports/orc-aseprite-comparison-v4.json').read_text(encoding='utf-8'))
def rgba(file):return Image.open(root/file).convert('RGBA').tobytes()
palette=set()
for c in data['clips']:
    for f in c['before']:
        im=Image.open(root/f).convert('RGBA');palette.update(p[:3] for p in im.getdata() if p[3])
for c in data['clips']:
    for index,file in enumerate(c['after']):
        old=Image.open(root/c['before'][index]).convert('RGBA');new=Image.open(root/file).convert('RGBA')
        assert old.size==new.size==(128,128)
        assert {p[:3] for p in new.getdata() if p[3]}<=palette,'New native palette color'
        if not c['analysis'][index]['edits']['canonicalNeutralReuse']:
            assert old.getchannel('A').tobytes()==new.getchannel('A').tobytes(),'Unplanned silhouette edit'
assert rgba(data['clips'][0]['after'][0])==rgba(data['clips'][0]['after'][4])==rgba(data['clips'][1]['after'][2])
old=Image.open(root/data['concept']['before']).convert('RGBA');new=Image.open(root/data['concept']['after']).convert('RGBA')
assert old.size==new.size==(1254,1254)
nonfringe=0
for a,b in zip(old.getdata(),new.getdata()):
    if a!=b:
        if a[3]<=12:assert b==(0,0,0,0)
        else:assert a[3]==b[3];nonfringe+=1
assert nonfringe==6,'Only six selected concept RGB pixels should change'
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
errors=[];exact=0;toggle_checks=0
def canvas(page,selector):return bytes(page.locator(selector).evaluate('e=>Array.from(e.getContext("2d").getImageData(0,0,128,128).data)'))
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge',headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1100},device_scale_factor=1)
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto((root/'reports/orc-aseprite-v4/review.html').as_uri(),wait_until='networkidle')
        page.wait_for_function('document.body.dataset.ready==="true"')
        assert page.locator('#conceptBefore').evaluate('e=>e.complete&&e.naturalWidth===1254')
        assert page.locator('#conceptAfter').evaluate('e=>e.complete&&e.naturalWidth===1254')
        page.goto(f'http://127.0.0.1:{server.server_port}/reports/orc-aseprite-v4/review.html',wait_until='networkidle')
        page.wait_for_function('document.body.dataset.ready==="true"')
        for c in data['clips']:
            page.select_option('#clip',c['state'])
            for i,f in enumerate(c['after']):
                page.locator('#frame').evaluate('(e,i)=>{e.value=i;e.dispatchEvent(new Event("input"))}',i)
                page.wait_for_timeout(100)
                assert canvas(page,'#before')==rgba(c['before'][i])
                assert canvas(page,'#after')==rgba(f);exact+=2
                page.uncheck('#retouch');page.wait_for_timeout(100)
                working=str(Path(f).with_name(f'working_{i:02d}.png')).replace('\\','/')
                assert canvas(page,'#after')==rgba(working);toggle_checks+=1
                page.check('#retouch')
            page.click('#return');page.wait_for_timeout(70)
            assert page.locator('#position').inner_text().startswith('quadro '+str(len(c['after'])-1))
        page.check('#delta');page.wait_for_timeout(120)
        assert canvas(page,'#after')!=rgba(data['clips'][1]['after'][2])
        page.uncheck('#delta');page.select_option('#clip','Attack');page.click('#return');page.select_option('#zoom','4');page.wait_for_timeout(100)
        page.screenshot(path=str(root/'reports/orc-aseprite-v4/review-screenshot.png'),full_page=True)
        page.locator('.pair').nth(1).screenshot(path=str(root/'reports/orc-aseprite-v4/return-comparison.png'))
        page.select_option('#zoom','1');assert page.locator('#after').evaluate('e=>e.style.width')=='128px'
        page.select_option('#speed','0.5');page.click('#background');page.click('#start');page.click('#play');page.wait_for_timeout(170);page.click('#play')
        assert not errors,errors
        version=browser.version;browser.close()
finally:server.shutdown();server.server_close()
report={'status':'PASS','browser':'Microsoft Edge headless','version':version,'modes':['file:// display','loopback HTTP exact canvas'],'exactNativeCanvasComparisons':exact,'retouchLayerToggleChecks':toggle_checks,'newNativePaletteColors':0,'unplannedSilhouetteEdits':0,'canonicalNeutralIdentical':True,'conceptResolutionUnchanged':True,'conceptNonFringeChangedPixels':nonfringe,'javascriptErrors':errors,'artisticApproval':'PENDING_CREATOR','UnityPlayMode':'NOT_RUN'}
(root/'reports/orc-aseprite-comparison-check-v4.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
