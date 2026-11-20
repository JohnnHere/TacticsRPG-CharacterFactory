from pathlib import Path
from playwright.sync_api import sync_playwright
import json
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/F02-F08')
with sync_playwright()as p:
 edge=Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe');browser=p.chromium.launch(headless=True,**({'executable_path':str(edge)}if edge.is_file()else{}))
 page=browser.new_page(viewport={'width':1400,'height':1300});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto((E/'index.html').resolve().as_uri());page.wait_for_function('window.previewReady===true',timeout=15000)
 initial={k:page.locator('#'+k+'-after').screenshot()for k in ['F02','F08']}
 page.locator('[data-layer="weaponFront"]').uncheck()
 assert all(page.locator('#'+k+'-after').screenshot()!=initial[k]for k in initial)
 page.locator('#restore').click();assert all(page.locator('#'+k+'-after').screenshot()==initial[k]for k in initial)
 page.locator('#scale').select_option('0.5');assert all(page.locator('#'+k+'-after').bounding_box()['width']==128 for k in initial)
 page.locator('#scale').select_option('1');assert all(page.locator('#'+k+'-after').bounding_box()['width']==256 for k in initial)
 assert not errors;page.screenshot(path=str(E/'preview-native.png'),full_page=True);browser.close()
(E/'preview-check.json').write_text(json.dumps({'status':'PASS','scope':'Two static representatives; no motion/independent QA','imageLoad':True,'layerTogglesChangeBoth':True,'restoreExact':True,'canvasScales':[128,256],'pageErrors':errors},indent=2)+'\n',encoding='utf-8')
print('PASS: F02/F08 preview images, layer toggles, exact restoration,128/256 displays. No artistic approval.')
