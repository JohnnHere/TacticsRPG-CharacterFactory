from pathlib import Path
from playwright.sync_api import sync_playwright
import json
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/full-front-r-sword')
with sync_playwright()as p:
 edge=Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe');browser=p.chromium.launch(headless=True,**({'executable_path':str(edge)}if edge.is_file()else{}));page=browser.new_page(viewport={'width':1440,'height':1050});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((E/'index.html').resolve().as_uri());page.wait_for_function('window.reviewReady===true',timeout=15000)
 traces={}
 for speed in [1,.5]:
  page.evaluate('(speed)=>{reviewApi.setPlaying(false);reviewApi.setSpeed(speed);reviewApi.setLoop(true);reviewApi.seek(0);reviewApi.resetTrace();reviewApi.restart()}',speed)
  page.wait_for_timeout(1700 if speed==1 else 3100);trace=page.evaluate('window.reviewTrace');seen=sorted(set(r['frame']for r in trace));assert seen==list(range(13)),(speed,seen)
  traces[str(speed)]={'seenFrames':seen,'trace':trace}
 page.evaluate('reviewApi.setPlaying(false);reviewApi.seek(6)');initial=page.locator('#after').screenshot();page.locator('#bodyOnly').click();body=page.locator('#after').screenshot();assert body!=initial;page.locator('#restore').click();assert page.locator('#after').screenshot()==initial
 page.locator('#next').click();assert page.evaluate('reviewApi.state().frame')==7;page.locator('#prev').click();assert page.evaluate('reviewApi.state().frame')==6
 page.locator('#scale').select_option('0.5');assert page.locator('#after').bounding_box()['width']==128;page.screenshot(path=str(E/'preview-tactical.png'));page.locator('#scale').select_option('1');assert page.locator('#after').bounding_box()['width']==256
 page.evaluate('reviewApi.setSpeed(1);reviewApi.setLoop(false);reviewApi.restart()');page.wait_for_timeout(1100);state=page.evaluate('reviewApi.state()');assert state['frame']==12 and state['playing']is False;assert page.locator('#play').inner_text()=='Reproduzir';end=page.locator('#after').screenshot();page.wait_for_timeout(200);assert page.locator('#after').screenshot()==end
 page.evaluate('reviewApi.seek(7)');page.screenshot(path=str(E/'preview-native.png'));assert not errors;browser.close()
result={'status':'PASS','scope':'Functional player tests only, not eye-in-loop artistic approval','loadedFrames':13,'sourceDurationMs':730,'playback':traces,'nativeCanvasCss':256,'tacticalCanvasCss':128,'bodyOnlyAndRestore':'PASS','frameStep':'PASS','oneShotTerminalHold':'F12 stable, stopped, source equipment empty','pageErrors':errors}
(E/'preview-check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print('PASS:13/13 frames at1x and0.5x, native/tactical scales, frame step, body-only and one-shot hold. No artistic approval.')
