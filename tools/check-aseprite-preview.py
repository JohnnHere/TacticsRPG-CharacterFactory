"""Verify editor previews in isolated headless Edge without touching the desktop."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json
import threading
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass
    def do_GET(self):
        try:
            super().do_GET()
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            pass

server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(root)))
threading.Thread(target=server.serve_forever, daemon=True).start()
results = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        try:
            for label, report_path in [('production', 'reports/aseprite-production-audit-v1.json'), ('capabilities', 'reports/aseprite-capabilities-v1.json')]:
                report = json.loads((root / report_path).read_text(encoding='utf-8'))
                build = json.loads((root / report['build'] / 'build.json').read_text(encoding='utf-8'))
                page = browser.new_page(viewport={'width': 1400, 'height': 950})
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.goto(f'http://127.0.0.1:{server.server_port}/{report["preview"]}', wait_until='networkidle')
                exact = 0
                for ji, job in enumerate(build['jobs']):
                    page.select_option('#clip', str(ji))
                    page.wait_for_function('id => document.querySelector("#view").dataset.job === id', arg=job['id'])
                    for fi, frame in enumerate(job['frames']):
                        page.locator('#frame').evaluate('(e,v) => {e.value=v;e.dispatchEvent(new Event("input"))}', str(fi))
                        rendered = page.evaluate('''async () => {
                          const c=document.querySelector('#view');
                          const data=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
                          const digest=await crypto.subtle.digest('SHA-256',data);
                          return {width:c.width,height:c.height,sha256:Array.from(new Uint8Array(digest)).map(x=>x.toString(16).padStart(2,'0')).join('')};
                        }''')
                        assert rendered['width'] == frame['width'] and rendered['height'] == frame['height']
                        assert rendered['sha256'] == frame['rgbaSha256'], (job['id'], fi)
                        exact += 1
                    if (ji + 1) % 48 == 0:
                        print(label, ji + 1, 'clips checked', flush=True)
                page.select_option('#zoom', '3')
                assert page.locator('#view').evaluate('c => c.style.width === c.width*3+"px"')
                assert page.locator('#play').inner_text() == 'Continuar'
                page.click('#play')
                assert page.evaluate('playing') is True
                page.click('#play')
                assert page.evaluate('playing') is False
                # Rapid changes must leave the final selection on screen.
                page.evaluate('''() => {const c=document.querySelector('#clip');for(const value of [0,jobs.length-1,0]){c.value=value;c.dispatchEvent(new Event('change'))}}''')
                page.wait_for_function('id => document.querySelector("#view").dataset.job === id', arg=build['jobs'][0]['id'])
                screenshot = f'reports/aseprite-{label}-preview-v1.png'
                page.screenshot(path=str(root / screenshot))
                assert not errors, errors
                page.close()
                # Local-file display is tested separately; canvas readback is intentionally HTTP-only.
                local = browser.new_page()
                local.on('pageerror', lambda e: errors.append(str(e)))
                local.goto((root / report['preview']).as_uri(), wait_until='networkidle')
                local.wait_for_function('document.querySelector("#view").dataset.job.length > 0')
                local.select_option('#clip', str(len(build['jobs'])-1))
                local.wait_for_function('id => document.querySelector("#view").dataset.job === id', arg=build['jobs'][-1]['id'])
                assert not errors, errors
                local.close()
                results.append({'scope': label, 'status': 'PASS', 'exactRgbaFrames': exact, 'clips': len(build['jobs']), 'http': 'PASS', 'fileDisplay': 'PASS', 'controlsAndRapidSelection': 'PASS', 'jsErrors': errors, 'screenshot': screenshot, 'build': report['build']})
        finally:
            browser.close()
finally:
    server.shutdown()
    server.server_close()
(root / 'reports/aseprite-preview-validation-v1.json').write_text(json.dumps({'status': 'PASS', 'results': results}, indent=2) + '\n', encoding='utf-8')
print(json.dumps(results, indent=2))
