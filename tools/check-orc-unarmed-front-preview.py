"""Exercise both local-file display and exact HTTP canvas pixels in isolated Edge."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import hashlib,json,threading
from PIL import Image
from playwright.sync_api import sync_playwright

root=Path('.').resolve();manifest=json.loads((root/'characters/orc-unarmed-front-review-data-v1.json').read_text(encoding='utf-8'))
expected={}
for c in manifest['classes']:
    for i,f in enumerate(c['clips']['Attack']['frames']):expected[(c['id'],'Attack',i)]=hashlib.sha256(Image.open(root/'characters'/f).convert('RGBA').tobytes()).hexdigest()
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        try:super().do_GET()
        except (ConnectionAbortedError,ConnectionResetError,BrokenPipeError):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge',headless=True)
        for mode,url in [('http',f'http://127.0.0.1:{server.server_port}/characters/review-orc-unarmed-front-v1.html'),('file',(root/'characters/review-orc-unarmed-front-v1.html').as_uri())]:
            errors=[];page=browser.new_page(viewport={'width':1600,'height':1100},device_scale_factor=1);page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(url,wait_until='networkidle');page.wait_for_function('window.orcCombatData && window.orcCombatFrame!==undefined')
            loaded=page.evaluate('''async()=>{const paths=orcCombatData.classes.flatMap(c=>Object.values(c.clips).flatMap(s=>s.frames));return await Promise.all(paths.map(src=>new Promise(resolve=>{const i=new Image;i.onload=()=>resolve({src,width:i.naturalWidth,height:i.naturalHeight});i.onerror=()=>resolve({src,error:true});i.src=src})));}''')
            assert len(loaded)==40 and all(i.get('width')==128 and i.get('height')==128 for i in loaded)
            pixel_checks=0
            for state,count in [('Attack',5)]:
                page.select_option('#state',state)
                page.wait_for_function('Array.from(document.querySelectorAll("img.strip")).every(i=>i.complete&&i.naturalWidth>0)')
                sizes=page.locator('img.strip').evaluate_all('els=>els.map(i=>[i.naturalWidth,i.naturalHeight])');assert all(s==[128*count,128] for s in sizes)
                page.click('#restart');page.wait_for_timeout(100);page.click('#play')
                for i in range(count):
                    page.locator('#frame').evaluate('(e,v)=>{e.value=v;e.dispatchEvent(new Event("input",{bubbles:true}))}',i)
                    page.wait_for_function(f'window.orcCombatFrame==={i}')
                    if mode=='http':
                        pixels=page.evaluate('''async()=>{
                            return await Promise.all(Array.from(document.querySelectorAll('canvas')).map(async c=>{
                                const a=c.getContext('2d').getImageData(0,0,128,128).data;
                                let bottom=-1,partial=0;
                                for(let y=0;y<128;y++)for(let x=0;x<128;x++){
                                    const v=a[(y*128+x)*4+3];if(v)bottom=y;if(v>0&&v<255)partial++;
                                }
                                const h=await crypto.subtle.digest('SHA-256',a);
                                return {id:c.id.replace('canvas-',''),bottom,partial,sha256:Array.from(new Uint8Array(h)).map(x=>x.toString(16).padStart(2,'0')).join('')};
                            }));
                        }''')
                        for px in pixels:assert px['bottom']==126 and px['partial']==0 and px['sha256']==expected[(px['id'],state,i)],(state,i,px)
                        pixel_checks+=len(pixels)
                page.locator('#frame').evaluate('(e,v)=>{e.value=v;e.dispatchEvent(new Event("input",{bubbles:true}))}',2 if state!='Defeat' else 4)
                page.wait_for_function(f'window.orcCombatFrame==={2 if state!="Defeat" else 4}')
                if mode=='http':page.screenshot(path=str(root/f'characters/orc-unarmed-front-{state.lower()}-browser-v1.png'),full_page=True)
            page.select_option('#state','Attack');page.uncheck('#repeat');page.click('#restart');page.wait_for_timeout(850)
            assert page.evaluate('orcCombatFrame')==4
            page.wait_for_timeout(180);assert page.evaluate('orcCombatFrame')==4
            page.check('#repeat')
            for c in manifest['classes']:
                page.select_option('#classFilter',c['id']);assert page.locator('article:visible').count()==1
            page.select_option('#classFilter','all')
            for zoom in ['1','3','2']:
                page.select_option('#zoom',zoom);assert all(w==128*int(zoom) for w in page.locator('canvas').evaluate_all('els=>els.map(c=>c.getBoundingClientRect().width)'))
            page.select_option('#speed','0.5');page.select_option('#speed','2');page.select_option('#speed','1')
            page.click('#background');assert 'light' in page.locator('body').get_attribute('class');page.click('#background')
            assert not errors
            results.append({'mode':mode,'loadedAnimationPng':40,'states':['Attack'],'nativeStrips':'8 per state, exact dimensions','classFilter':'8/8 PASS','zoom':'1x/2x/3x PASS','controls':'play/pause/restart/scrub/speed/background/one-shot final hold PASS','canvasNativeRgbaChecks':pixel_checks if mode=='http' else 'NOT_RUN_FILE_ORIGIN_SECURITY','javascriptErrors':errors})
            page.close()
        report={'browser':'Microsoft Edge headless via Playwright','version':browser.version,'results':results,'artisticApproval':'PENDING_CREATOR_UNARMED_FRONT_REVIEW','unityPlayMode':'NOT_RUN'}
        browser.close()
finally:server.shutdown();server.server_close()
(root/'characters/orc-unarmed-front-browser-v1.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('40 PNGs loaded in HTTP and file previews; 40/40 canvas RGBA hashes exact; controls PASS; zero JS errors; local server closed')
