# V6 frontal forensic 5: disconnected components + dot contexts + armpit windows.
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

# 1) disconnected components per frame (body layer)
comp_report = {}
for key, rel in CELLS.items():
    cell = ROOT / rel
    cj = json.loads((cell / 'clip.json').read_text(encoding='utf-8'))
    per = {}
    for f in cj['frames']:
        i = f['index']
        b = raw(load(cell / 'layers' / 'body' / f'{i:02d}.png'))
        seen = bytearray(256 * 256)
        comps = []
        for y0 in range(256):
            for x0 in range(256):
                idx = y0 * 256 + x0
                if seen[idx] or b[idx * 4 + 3] == 0: continue
                q = [(x0, y0)]; seen[idx] = 1; px_list = []
                while q:
                    cx, cy = q.pop()
                    px_list.append((cx, cy))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < 256 and 0 <= ny < 256:
                                k2 = ny * 256 + nx
                                if not seen[k2] and b[k2 * 4 + 3] > 0:
                                    seen[k2] = 1; q.append((nx, ny))
                comps.append(px_list)
        comps.sort(key=len, reverse=True)
        main = comps[0]
        minors = [c for c in comps[1:] if len(c) <= 40]
        if minors:
            per[f'{i:02d}'] = [{'n': len(c),
                                'bbox': [min(p[0] for p in c) - 64, min(p[1] for p in c) - 64,
                                         max(p[0] for p in c) - 64, max(p[1] for p in c) - 64],
                                'rgba': list(pix(b, c[0][0], c[0][1]))} for c in minors]
    if per: comp_report[key] = per

(OUT / 'forensic5-components.json').write_text(json.dumps(comp_report, ensure_ascii=False), encoding='utf-8')
print('=== minor body components (<=40px, not the main silhouette) ===')
for key, per in comp_report.items():
    for fid, lst in per.items():
        print(key, fid, [(c['n'], c['bbox']) for c in lst])

# 2) 5x5 context for F00 dots of each cell
ctx_lines = []
for key, rel in CELLS.items():
    cell = ROOT / rel
    dots = json.loads((OUT / 'forensic4-dots.json').read_text(encoding='utf-8'))['dots'][key]['00']
    b = raw(load(cell / 'layers' / 'body' / '00.png'))
    ctx_lines.append(f'## {key} F00 dots: {len(dots)}')
    for d in dots:
        x, y = d['x'], d['y']
        rows = []
        for yy in range(y - 2, y + 3):
            r = ''
            ls = []
            for xx in range(x - 2, x + 2 + 1):
                p = pix(b, xx, yy)
                r += classify(p)
                ls.append(lum(p) if p[3] > 0 else -1)
            rows.append(r + ' ' + ','.join(map(str, ls)))
        ctx_lines.append(f'-- ({x-64},{y-64})n rgba={d["rgba"]} L={d["L"]}\n' + '\n'.join(rows))
(OUT / 'forensic5-dot-contexts.txt').write_text('\n'.join(ctx_lines), encoding='utf-8')
print('dot contexts written')

# 3) armpit windows (native), attacker side: front_l image-right, front_r image-left
win_lines = []
WINDOWS = {'front_l/Sword': (78, 118, 34, 80), 'front_r/Sword': (10, 50, 34, 80)}
for key, (xa, xb, ya, yb) in WINDOWS.items():
    cell = ROOT / CELLS[key]
    for i in (0, 2, 3, 4, 5):
        b = raw(load(cell / 'layers' / 'body' / f'{i:02d}.png'))
        win_lines.append(f'== {key} F{i:02d} native x[{xa}..{xb}] y[{ya}..{yb}] ==')
        hdr = '     ' + ''.join(str((x // 10) % 10) if x % 5 == 0 else ' ' for x in range(xa, xb + 1))
        win_lines.append(hdr)
        for y in range(ya, yb + 1):
            win_lines.append(f'{y:4d} ' + ''.join(classify(pix(b, x + 64, y + 64)) for x in range(xa, xb + 1)))
(OUT / 'forensic5-armpit-windows.txt').write_text('\n'.join(win_lines), encoding='utf-8')
print('armpit windows written')

