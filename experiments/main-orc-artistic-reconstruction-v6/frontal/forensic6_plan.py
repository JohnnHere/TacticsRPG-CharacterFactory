# V6 frontal forensic 6: fix plan generation (dots + islands) + quasi-floating observations.
# READ-ONLY: computes deterministic fills; does not touch sources.
import json, statistics
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

def median_fill(b, x, y):
    groups = [
        [(px2) for dx2 in (-1, 0, 1) for dy2 in (-1, 0, 1)
         for px2 in [pix(b, x + dx2, y + dy2)]
         if 0 <= x + dx2 < 256 and 0 <= y + dy2 < 256 and px2[3] > 0 and lum(px2) < 120],
        [(px2) for dx2 in (-1, 0, 1) for dy2 in (-1, 0, 1)
         for px2 in [pix(b, x + dx2, y + dy2)]
         if 0 <= x + dx2 < 256 and 0 <= y + dy2 < 256 and px2[3] > 0 and lum(px2) < 160],
    ]
    for g in groups:
        if g:
            r = int(statistics.median(p[0] for p in g))
            gg = int(statistics.median(p[1] for p in g))
            b2 = int(statistics.median(p[2] for p in g))
            f = (r, gg, b2, 255)
            if lum(f) < 120:
                return list(f), 'median-dark'
            return list(f), 'median-mid'
    return [12, 15, 18, 255], 'ink-fallback'

dots = json.loads((OUT / 'forensic4-dots.json').read_text(encoding='utf-8'))['dots']
plan = {}
quasi = {}
for key, rel in CELLS.items():
    cell = ROOT / rel
    cj = json.loads((cell / 'clip.json').read_text(encoding='utf-8'))
    per = {}
    qper = {}
    for f in cj['frames']:
        i = f['index']
        b = raw(load(cell / 'layers' / 'body' / f'{i:02d}.png'))
        edits = []
        fdots = dots.get(key, {}).get(f'{i:02d}', [])
        for d in fdots:
            fill, how = median_fill(b, d['x'], d['y'])
            edits.append({'x': d['x'] - 64, 'y': d['y'] - 64, 'from': d['rgba'], 'to': fill, 'rule': how, 'kind': 'dot'})
        # islands (0,0,1) known coords per view side; detect generically: opaque pixel, 8-conn none
        for y in range(256):
            for x in range(256):
                p = pix(b, x, y)
                if p[3] == 0: continue
                n8 = 0; n4 = 0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0: continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 256 and 0 <= ny < 256:
                            q = pix(b, nx, ny)
                            if q[3] > 0:
                                n8 += 1
                                if dx == 0 or dy == 0: n4 += 1
                if n8 == 0:
                    edits.append({'x': x - 64, 'y': y - 64, 'from': list(p), 'to': [0, 0, 0, 0], 'rule': 'island-remove', 'kind': 'island'})
                elif n4 == 0:
                    qper.setdefault(f'{i:02d}', []).append({'x': x - 64, 'y': y - 64, 'rgba': list(p), 'L': lum(p)})
        if edits:
            per[f'{i:02d}'] = edits
    plan[key] = per
    if qper: quasi[key] = qper

(OUT / 'fixes-plan.json').write_text(json.dumps({'plan': plan, 'quasiFloatingObservations': quasi}, ensure_ascii=False), encoding='utf-8')
total = {k: sum(len(v) for v in per.values()) for k, per in plan.items()}
isl = {k: sum(1 for v in per.values() for e in v if e['kind'] == 'island') for k, per in plan.items()}
print('total edits per cell:', total)
print('island removals per cell:', isl)
print('frames with edits:', {k: sorted(per.keys()) for k, per in plan.items()})
qcount = {k: {fid: len(v) for fid, v in q.items()} for k, q in quasi.items()}
print('quasi-floating (report only):', qcount)
