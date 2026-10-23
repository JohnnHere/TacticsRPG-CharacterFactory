"""Review-page rendering and integrity checks; source art is read only."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json, threading
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
report = json.loads((root/'reports/orc-art-lab-v5.json').read_text(encoding='utf-8'))
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(root)))
threading.Thread(target=server.serve_forever, daemon=True).start()
errors = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport={'width': 1840, 'height': 1200}, device_scale_factor=1)
        page.on('pageerror', lambda e: errors.append(str(e)))
        modes = []
        for url in [(root/'reports/orc-art-lab-v5/review.html').as_uri(), f'http://127.0.0.1:{server.server_port}/reports/orc-art-lab-v5/review.html']:
            page.goto(url, wait_until='networkidle')
            page.wait_for_function('document.body.dataset.ready === "true"')
            assert page.locator('.card').count() == 5
            assert page.locator('.card img').evaluate_all('imgs=>imgs.every(i=>i.complete&&i.naturalWidth===1254&&i.naturalHeight===1254)')
            for i in range(5):
                page.select_option('#option', str(i))
                page.locator('#chosen').evaluate('i=>i.decode()')
                assert report['variants'][i]['title'] in page.locator('#chosenTitle').inner_text()
                assert page.locator('#chosen').get_attribute('src').endswith(report['variants'][i]['concept'])
            modes.append(url.split(':')[0])
        for bg in ['light', 'checker', 'dark']:
            page.select_option('#background', bg)
            assert page.locator('body').evaluate('(e,b)=>b==="dark"?e.className==="":e.classList.contains(b)', bg)
        page.check('#native')
        assert page.locator('#chosen').evaluate('e=>e.getBoundingClientRect().width') == 1254
        page.uncheck('#native')
        for i in range(5):
            page.locator(f'[data-index="{i}"]').click()
            assert page.locator('#option').input_value() == str(i)
        page.select_option('#option', '0')
        page.evaluate('window.scrollTo(0,0)')
        page.screenshot(path=str(root/'reports/orc-art-lab-v5/review-screenshot.png'), full_page=True)
        page.locator('#options').screenshot(path=str(root/'reports/orc-art-lab-v5/five-options.png'))
        page.set_viewport_size({'width': 390, 'height': 844})
        page.evaluate('window.scrollTo(0,0)')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert not errors, errors
        version = browser.version
        browser.close()
finally:
    server.shutdown()
    server.server_close()
result = {'status': 'PASS', 'browser': 'Microsoft Edge headless', 'version': version, 'loadedConcepts': 5, 'comparisonOptionsCheckedPerMode': 5, 'modes': modes, 'backgrounds': 3, 'nativeConceptZoom': True, 'cardControls': 5, 'mobileLayout': 'PASS', 'javascriptErrors': errors, 'artisticApproval': 'PENDING_CREATOR', 'screenshotsAreReviewDerivatives': True}
(root/'reports/orc-art-lab-v5-preview-check.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
