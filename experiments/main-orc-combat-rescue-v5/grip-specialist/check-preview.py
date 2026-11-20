from pathlib import Path
from playwright.sync_api import sync_playwright
import json
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist')
with sync_playwright()as p:
 edge=Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')
 browser=p.chromium.launch(headless=True,**({'executable_path':str(edge)}if edge.is_file()else{}))
 page=browser.new_page(viewport={'width':1400,'height':1040});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((E/'index.html').resolve().as_uri());page.wait_for_function('window.previewReady===true',timeout=15000)
 # File URLs display correctly but forbid JS getImageData on cross-directory
 # images. Compare rendered canvas screenshots without weakening browser rules.
 initial=page.locator('#after').screenshot()
 page.locator('[data-layer="weaponFront"]').uncheck();without=page.locator('#after').screenshot();assert initial!=without
 page.locator('#restore').click();restored=page.locator('#after').screenshot();assert initial==restored
 page.locator('#scale').select_option('0.5');assert page.locator('#after').bounding_box()['width']==128
 page.locator('#scale').select_option('1');assert page.locator('#after').bounding_box()['width']==256
 assert not errors;page.screenshot(path=str(E/'preview-native.png'))
 browser.close()
(E/'preview-check.json').write_text(json.dumps({'status':'PASS','scope':'One-frame preview only; no motion QA','imageLoad':True,'weaponLayerToggleChangesCanvas':True,'restoreExact':True,'canvasScales':[128,256],'pageErrors':errors},indent=2)+'\n')
print('PASS: representative loaded, layer toggles/restoration and128/256 display verified. No artistic approval.')
