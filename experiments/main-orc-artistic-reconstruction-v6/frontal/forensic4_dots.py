# V6 frontal forensic 4: isolated bright dots + armpit windows.
# READ-ONLY diagnostic.
import json
from pathlib import Path
from PIL import Image

ROOT = Path.cwd()
OUT = Path('experiments/main-orc-artistic-reconstruction-v6/frontal')
CELLS = {
    'front_l/Sword': 'characters/orc-v1/source/combat-rescue-v5/grip-specialist/front_l-Sword-full',
    'front_r/Sword': 'characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword',
    'front_r/Axe':   'characters/orc-v1/source/combat-rescue-v5/grip-specialist/front_r-Axe-full',
    'front_l/Axe':   'characters/orc-v1/source/combat-rescue-v5/grip-specialist/front_l-Axe-full',
}

def load(p): return Image.open(p).convert('RGBA')
def raw(im): return im.tobytes()
def pix(b, x, y, w=256):
    i = (y * w + x) * 4
    return (b[i], b[i+1], b[i+2], b[i+3])
def lum(p): return (p[0] * 299 + p[1] * 587 + p[2] * 114) // 1000
def classify(px):
    r, g, b, a = px
    if a == 0: return '.'
    mx, mn = max(r, g, b), min(r, g, b)
    if mx >= 200 and mx - mn < 40: return 'W'
    if mx - mn >= 30 and r > g and r > b: return 'r' if lum(px) < 90 else 'R'
    if mx - mn >= 25 and g > r and g > b: return 'g'
    L = lum(px)
    if L < 40: return 'k'
    if L < 80: return 'd'
    if L < 140: return 'm'
    return 'l'

res = {}
dots_all = {}
for key, rel in CELLS.items():
    cell = ROOT / rel
    cj = json.loads((cell / 'clip.json').read_text(encoding='utf-8'))
    per = {}
    for f in cj['frames']:
        i = f['index']
        b = raw(load(cell / 'layers' / 'body' / f'{i:02d}.png'))
        dots = []
        for y in range(256):
            for x in range(256):
                p = pix(b, x, y)
                if p[3] == 0: continue
                L = lum(p)
                if L < 170: continue
                mx, mn = max(p[0], p[1], p[2]), min(p[0], p[1], p[2])
                neutral = mx - mn < 45
                if not neutral: continue
                # isolated: no 4-neighbour with L>=120
                bright_nb = 0
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 256 and 0 <= ny < 256:
                        q = pix(b, nx, ny)
                        if q[3] > 0 and lum(q) >= 120:
                            bright_nb += 1
                if bright_nb == 0:
                    dots.append({'x': x, 'y': y, 'rgba': list(p), 'L': L})
        if dots:
            per[f'{i:02d}'] = dots
            dots_all.setdefault(key, {}).setdefault('byCoord', {})
            for d in dots:
                dots_all[key]['byCoord'].setdefault((d['x'], d['y']), []).append(i)
    res[key] = per

# persistence: coords appearing in >=3 frames per cell
persist = {}
for key, info in dots_all.items():
    persist[key] = [{'x': c[0], 'y': c[1], 'frames': v} for c, v in info['byCoord'].items() if len(v) >= 3]
    persist[key].sort(key=lambda e: -len(e['frames']))

(OUT / 'forensic4-dots.json').write_text(json.dumps({'dots': res, 'persistent': persist}, ensure_ascii=False), encoding='utf-8')
print('=== isolated bright dots per frame (L>=170 neutral, 0 bright neighbours) ===')
for key, per in res.items():
    print(key, {k: len(v) for k, v in per.items()})
print('=== persistent coords (>=3 frames) ===')
for key, plist in persist.items():
    print(key, [(e['x'], e['y'], len(e['frames'])) for e in plist][:30])
