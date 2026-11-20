# V6 frontal forensic 2: per-frame geometry, armpit ASCII maps, halo scan, grip check.
# READ-ONLY diagnostic.
import json
from pathlib import Path
from PIL import Image

ROOT = Path.cwd()
CELLS = {
    'front_l/Sword': 'characters/orc-v1/source/combat-rescue-v5/grip-specialist/front_l-Sword-full',
    'front_r/Sword': 'characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword',
    'front_r/Axe':   'characters/orc-v1/source/combat-rescue-v5/grip-specialist/front_r-Axe-full',
    'front_l/Axe':   'characters/orc-v1/source/combat-rescue-v5/grip-specialist/front_l-Axe-full',
}
LAYERS = ['weaponBack', 'body', 'weaponFront', 'handFront']
OUT = Path('experiments/main-orc-artistic-reconstruction-v6/frontal')

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

def bbox(im):
    bb = im.getbbox()
    return list(bb) if bb else None

def halo_scan(pixels, weapon_mask):
    """Bright clusters (L>=185) not in weapon layers; classify rim vs interior."""
    W = H = 256
    seen = [[False] * W for _ in range(H)]
    clusters = []
    for y in range(H):
        for x in range(W):
            if seen[y][x]: continue
            px = pixels[y][x]
            if px[3] == 0 or lum(px) < 185 or weapon_mask[y][x]:
                seen[y][x] = True; continue
            q = [(x, y)]; seen[y][x] = True; comp = []
            while q:
                cx, cy = q.pop()
                comp.append((cx, cy))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < W and 0 <= ny < H and not seen[ny][nx]:
                        seen[ny][nx] = True
                        p2 = pixels[ny][nx]
                        if p2[3] > 0 and lum(p2) >= 185 and not weapon_mask[ny][nx]:
                            q.append((nx, ny))
            xs = [c[0] for c in comp]; ys = [c[1] for c in comp]
            rim = False
            for (cx, cy) in comp:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if not (0 <= nx < W and 0 <= ny < H) or pixels[ny][nx][3] == 0:
                        rim = True; break
                if rim: break
            clusters.append({'n': len(comp), 'bbox': [min(xs), min(ys), max(xs), max(ys)],
                             'rim': rim,
                             'samples': [[c[0], c[1], list(pixels[c[1]][c[0]])] for c in comp[:4]]})
    return clusters

report = {'geometry': {}, 'halos_body': {}, 'halos_composite': {}, 'grip': {}}
maps = []
for key, rel in CELLS.items():
    cell = ROOT / rel
    cj = json.loads((cell / 'clip.json').read_text(encoding='utf-8'))
    geo = {}
    for f in cj['frames']:
        i = f['index']
        ims = {l: load(cell / 'layers' / l / f'{i:02d}.png') for l in LAYERS}
        comp = load(cell / f'{i:02d}.png')
        gp = f.get('grip')
        g = {'weaponVisible': f['weaponVisible'],
             'bodyBbox': bbox(ims['body']),
             'handFrontBbox': bbox(ims['handFront']),
             'weaponBackBbox': bbox(ims['weaponBack']),
             'weaponFrontBbox': bbox(ims['weaponFront']),
             'meta': {k2: f.get(k2) for k2 in ('grip', 'rotationDeg', 'handFrontPixels', 'weaponBbox', 'phase')}}
        geo[f'{i:02d}'] = g
        if f['weaponVisible'] and gp:
            gx, gy = gp[0], gp[1]
            wb, wf, hf = raw(ims['weaponBack']), raw(ims['weaponFront']), raw(ims['handFront'])
            handle = [(x, y) for y in range(max(0, gy - 14), min(256, gy + 14))
                      for x in range(max(0, gx - 14), min(256, gx + 14))
                      if pix(wb, x, y)[3] > 0 or
                      (pix(wf, x, y)[3] > 0 and abs(x - gx) <= 8 and abs(y - gy) <= 8)]
            glove = [(x, y) for y in range(max(0, gy - 16), min(256, gy + 16))
                     for x in range(max(0, gx - 16), min(256, gx + 16))
                     if pix(hf, x, y)[3] > 0]
            if handle and glove:
                overlap = sum(1 for p in glove if pix(wb, p[0], p[1])[3] > 0 or pix(wf, p[0], p[1])[3] > 0)
                mind = min(abs(hx - px2) + abs(hy - py2) for (hx, hy) in glove for (px2, py2) in handle)
                report['grip'].setdefault(key, {})[f'{i:02d}'] = {
                    'grip': gp, 'handle_px': len(handle), 'glove_px': len(glove),
                    'overlap': overlap, 'min_manhattan': mind}
            else:
                report['grip'].setdefault(key, {})[f'{i:02d}'] = {
                    'grip': gp, 'handle_px': len(handle), 'glove_px': len(glove), 'MISSING': True}
        wbb, wfb = raw(ims['weaponBack']), raw(ims['weaponFront'])
        wmask = [[(pix(wbb, x, y)[3] > 0 or pix(wfb, x, y)[3] > 0) for x in range(256)] for y in range(256)]
        compb = comp.tobytes()
        comp_px = [[pix(compb, x, y) for x in range(256)] for y in range(256)]
        bodyb = ims['body'].tobytes()
        body_px = [[pix(bodyb, x, y) for x in range(256)] for y in range(256)]
        hb = halo_scan(body_px, wmask)
        hc = halo_scan(comp_px, wmask)
        if hb: report['halos_body'].setdefault(key, {})[f'{i:02d}'] = hb
        if hc: report['halos_composite'].setdefault(key, {})[f'{i:02d}'] = hc
        if key == 'front_l/Sword' and f['weaponVisible'] and gp:
            gx, gy = gp[0] - 64, gp[1] - 64
            x0, y0 = max(0, gx - 22), max(0, gy - 22)
            rows = []
            for y in range(y0, min(128, y0 + 45)):
                row = ''.join(classify(pix(bodyb, x + 64, y + 64)) for x in range(x0, x0 + 45))
                rows.append(f'{y:3d} {row}')
            maps.append(f'== {key} F{i:02d} native window x[{x0}..{x0+44}] y[{y0}..{y0+len(rows)-1}] gripN=({gx},{gy}) ==\n' + '\n'.join(rows))
    report['geometry'][key] = geo

(OUT / 'forensic2-geometry.json').write_text(json.dumps(report, ensure_ascii=False), encoding='utf-8')
(OUT / 'forensic2-armpit-maps.txt').write_text('\n'.join(maps), encoding='utf-8')
print('=== GEOMETRY ===')
for key in CELLS:
    print(f'-- {key}')
    for fid, g in report['geometry'][key].items():
        m = g['meta']
        print(f" {fid} vis={g['weaponVisible']} grip={m['grip']} rot={m['rotationDeg']} body={g['bodyBbox']} hf={g['handFrontBbox']} wb={g['weaponBackBbox']} wf={g['weaponFrontBbox']}")
print('=== HALOS body (clusters rim or n>=2) ===')
for key, frames in report['halos_body'].items():
    for fid, cl in frames.items():
        sig = [c for c in cl if c['n'] >= 2 or c['rim']]
        if sig:
            print(key, fid, [(c['n'], c['bbox'], c['rim']) for c in sig][:8])
print('=== GRIP ===')
for key, frames in report['grip'].items():
    print(key, {fid: (v.get('overlap'), v.get('min_manhattan'), v.get('MISSING', False)) for fid, v in frames.items()})
