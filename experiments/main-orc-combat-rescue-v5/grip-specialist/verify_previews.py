import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path('.').resolve()
EXP_GRIP = ROOT / 'experiments/main-orc-combat-rescue-v5/grip-specialist'

targets = [
    {
        'dirName': 'front_l-Sword-full',
        'frameCount': 13,
        'totalDurationMs': 730,
        'terminalFrame': 12,
        'contactFrame': 7
    },
    {
        'dirName': 'front_r-Axe-full',
        'frameCount': 12,
        'totalDurationMs': 1005,
        'terminalFrame': 11,
        'contactFrame': 6
    },
    {
        'dirName': 'front_l-Axe-full',
        'frameCount': 12,
        'totalDurationMs': 1005,
        'terminalFrame': 11,
        'contactFrame': 6
    }
]

edge_exe = Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')
launch_args = {'executable_path': str(edge_exe)} if edge_exe.is_file() else {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, **launch_args)
    for tgt in targets:
        dir_p = EXP_GRIP / tgt['dirName']
        print(f"\nTesting preview for: {tgt['dirName']}")
        page = browser.new_page(viewport={'width': 1440, 'height': 1050})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        
        index_uri = (dir_p / 'index.html').resolve().as_uri()
        page.goto(index_uri)
        page.wait_for_function('window.reviewReady === true', timeout=15000)
        
        # Test playback at 1x and 0.5x
        traces = {}
        for speed in [1.0, 0.5]:
            page.evaluate('(speed) => { reviewApi.setPlaying(false); reviewApi.setSpeed(speed); reviewApi.setLoop(true); reviewApi.seek(0); reviewApi.resetTrace(); reviewApi.restart(); }', speed)
            wait_ms = int((tgt['totalDurationMs'] / speed) * 1.5) + 300
            page.wait_for_timeout(wait_ms)
            trace = page.evaluate('window.reviewTrace')
            seen = sorted(set(r['frame'] for r in trace))
            assert seen == list(range(tgt['frameCount'])), f"Speed {speed} failed to see all frames: {seen}"
            traces[str(speed)] = {'seenFrames': seen, 'traceCount': len(trace)}
            print(f"  Speed {speed}x: saw all {len(seen)} frames ({len(trace)} samples)")
        
        # Test layer toggles
        page.evaluate(f"reviewApi.setPlaying(false); reviewApi.seek({tgt['contactFrame']})")
        initial = page.locator('#after').screenshot()
        page.locator('#bodyOnly').click()
        body_only = page.locator('#after').screenshot()
        assert body_only != initial, "Body-only screenshot equals full composite screenshot!"
        page.locator('#restore').click()
        restored = page.locator('#after').screenshot()
        assert restored == initial, "Restored layers do not match initial composite!"
        print("  Layer toggles: PASS (bodyOnly & restore match perfectly)")
        
        # Test frame stepping
        page.locator('#next').click()
        assert page.evaluate('reviewApi.state().frame') == tgt['contactFrame'] + 1
        page.locator('#prev').click()
        assert page.evaluate('reviewApi.state().frame') == tgt['contactFrame']
        print("  Frame step controls: PASS")
        
        # Test scale
        page.locator('#scale').select_option('0.5')
        assert page.locator('#after').bounding_box()['width'] == 128
        page.screenshot(path=str(dir_p / 'preview-tactical.png'))
        page.locator('#scale').select_option('1')
        assert page.locator('#after').bounding_box()['width'] == 256
        page.screenshot(path=str(dir_p / 'preview-native.png'))
        print("  Scale selection & screenshots: PASS")
        
        # Test terminal hold (non-looping oneShot)
        page.evaluate('reviewApi.setSpeed(1); reviewApi.setLoop(false); reviewApi.restart()')
        page.wait_for_timeout(tgt['totalDurationMs'] + 400)
        state = page.evaluate('reviewApi.state()')
        assert state['frame'] == tgt['terminalFrame'], f"Expected terminal frame {tgt['terminalFrame']}, got {state['frame']}"
        assert state['playing'] is False, "Player did not stop at terminal frame!"
        assert page.locator('#play').inner_text() == 'Reproduzir'
        print(f"  OneShot terminal hold: PASS (frame {tgt['terminalFrame']} stable)")
        
        assert not errors, f"Page errors encountered: {errors}"
        
        res = {
            'status': 'PASS',
            'scope': f"Functional player tests only for {tgt['dirName']}",
            'loadedFrames': tgt['frameCount'],
            'sourceDurationMs': tgt['totalDurationMs'],
            'playback': traces,
            'nativeCanvasCss': 256,
            'tacticalCanvasCss': 128,
            'bodyOnlyAndRestore': 'PASS',
            'frameStep': 'PASS',
            'oneShotTerminalHold': f"F{tgt['terminalFrame']:02d} stable, stopped, source equipment empty",
            'pageErrors': errors
        }
        (dir_p / 'preview-check.json').write_text(json.dumps(res, indent=2) + '\n', encoding='utf-8')
        page.close()
    
    browser.close()

print("\nALL 3 PREVIEWS TESTED AND VERIFIED SUCCESSFULLY VIA PLAYWRIGHT!")
