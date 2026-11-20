# V6 frontal verification: new-vs-before diff must equal the plan exactly; contracts re-checked.
import json
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path.cwd()
OUT = Path('experiments/main-orc-artistic-reconstruction-v6/frontal')
CELLS = {
    'front_l/Sword': 'front_l-Sword-full',
    'front_r/Sword': 'full-front-r-sword',
    'front_r/Axe':   'front_r-Axe-full',
    'front_l/Axe':   'front_l-Axe-full',
}
NEW = ROOT / 'characters/orc-v1/source/artistic-reconstruction-v6/frontal'
BEF = OUT / 'before'
LAYERS = ['weaponBack', 'body', 'weaponFront', 'handFront']

plan = json.loads((OUT / 'fixes-plan.json').read_text(encoding='utf-8'))['plan']
res = {}
ok_all = True
for key, slug in CELLS.items():
    cplan = plan[key]
    v6 = {'cells_checked': 0, 'frameResults': {}, 'layerBytesEqual': True, 'contractFail': []}
    cj_frames = {}
    for fid_str, edits in cplan.items():
        i = int(fid_str)
        fr = {}
        for kind, sub in (('composite', NEW / slug / f'{i:02d}.png'), ('native', NEW / slug / 'native' / f'{i:02d}.png'), ('body', NEW / slug / 'layers' / 'body' / f'{i:02d}.png')):
            bef_path = BEF / slug / (('' if kind == 'composite' else ('native/' if kind == 'native' else 'layers/body/')) + f'{i:02d}.png')
            a = np.array(Image.open(sub).convert('RGBA'), dtype=np.int16)
            b = np.array(Image.open(bef_path).convert('RGBA'), dtype=np.int16)
            assert a.shape == b.shape
            diffmask = np.any(a != b, axis=2)
            ys, xs = np.nonzero(diffmask)
            got = {(int(x) - (0 if kind != 'native' else 0), int(y)) for x, y in zip(xs, ys)}
            want = set()
            for e in edits:
                x, y = e['x'], e['y']
                if kind != 'native':
                    x, y = x + 64, y + 64
                want.add((x, y))
            vals_ok = True
            for e in edits:
                x, y = e['x'], e['y']
                if kind != 'native':
                    x, y = x + 64, y + 64
                if list(a[y, x]) != e['to']:
                    vals_ok = False
            fr[kind] = {'diffSetEqualsPlan': got == want, 'valuesMatchPlan': vals_ok,
                        'nDiff': len(got), 'nPlan': len(want)}
            ok_all = ok_all and got == want and vals_ok
        # weapon/handFront layer bytes unchanged vs before
        for l in LAYERS:
            if l == 'body': continue
            p1 = NEW / slug / 'layers' / l / f'{i:02d}.png'
            p2 = BEF / slug / 'layers' / l / f'{i:02d}.png'
            if p1.read_bytes() != p2.read_bytes():
                v6['layerBytesEqual'] = False
                ok_all = False
        # contracts on new files
        comp = Image.open(NEW / slug / f'{i:02d}.png').convert('RGBA')
        acc = Image.new('RGBA', comp.size, (0, 0, 0, 0))
        wv = None
        for l in LAYERS:
            im = Image.open(NEW / slug / 'layers' / l / f'{i:02d}.png').convert('RGBA')
            acc = Image.alpha_composite(acc, im)
        if acc.tobytes() != comp.tobytes():
            v6['contractFail'].append(f'F{i:02d} composite!=alpha-over')
        nat = Image.open(NEW / slug / 'native' / f'{i:02d}.png').convert('RGBA')
        body = Image.open(NEW / slug / 'layers' / 'body' / f'{i:02d}.png').convert('RGBA')
        if body.crop((64, 64, 192, 192)).tobytes() != nat.tobytes():
            v6['contractFail'].append(f'F{i:02d} native!=crop')
        if nat.getbbox() and nat.getbbox()[3] != 127:
            v6['contractFail'].append(f'F{i:02d} groundY moved: {nat.getbbox()}')
        v6['cells_checked'] += 1
        v6['frameResults'][fid_str] = fr
    res[key] = v6

(OUT / 'verify-result.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print('ALL_OK' if ok_all else 'FAILURES_PRESEN')
for key, v6 in res.items():
    bad = [f for f, r in v6['frameResults'].items() if not all(x['diffSetEqualsPlan'] and x['valuesMatchPlan'] for x in r.values())]
    print(key, 'frames', v6['cells_checked'], 'layerBytesEqual', v6['layerBytesEqual'], 'contractFail', v6['contractFail'], 'badFrames', bad)
