# V6 frontal forensic 3: mirror consistency, body sharing, low-threshold halo, full ASCII.
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

def mirror_bytes(b, w=256, h=256):
    out = bytearray(len(b))
    for y in range(h):
        for x in range(w):
            si = (y * w + x) * 4
            di = (y * w + (w - 1 - x)) * 4
            out[di:di+4] = b[si:si+4]
    return bytes(out)

res = {'mirror': {}, 'bodySharing': {}, 'halo150': {}, 'front_r_sword_grip': {}}
ascii_out = []
bodies = {}
for key, rel in CELLS.items():
    cell = ROOT / rel
    cj = json.loads((cell / 'clip.json').read_text(encoding='utf-8'))
    bodies[key] = {}
    for f in cj['frames']:
        bodies[key][f['index']] = load(cell / 'layers' / 'body' / f"{f['index']:02d}.png")

# (a) mirror consistency front_l vs front_r per family
for fam in ['Sword', 'Axe']:
    Lb = bodies[f'front_l/{fam}']; Rb = bodies[f'front_r/{fam}']
    per = {}
    for i in sorted(Lb):
        if i not in Rb: continue
        mb = mirror_bytes(raw(Lb[i])); rb = raw(Rb[i])
        diffs = [((k // 4) % 256, (k // 4) // 256) for k in range(0, len(mb), 4) if mb[k:k+4] != rb[k:k+4]]
        per[f'{i:02d}'] = {'n': len(diffs), 'first': diffs[:10]}
    res['mirror'][fam] = per

# (b) body sharing Sword vs Axe same direction
for dirn in ['front_l', 'front_r']:
    Sb = bodies[f'{dirn}/Sword']; Ab = bodies[f'{dirn}/Axe']
    per = {}
    for i in sorted(Ab):
        if i not in Sb: continue
        sb, ab = raw(Sb[i]), raw(Ab[i])
        per[f'{i:02d}'] = sum(1 for k in range(0, len(sb), 4) if sb[k:k+4] != ab[k:k+4])
    res['bodySharing'][dirn] = per

# (c) low-threshold halo scan on body: L>=150 pixel with 4-neighbour L<=70 (both opaque)
for key, rel in CELLS.items():
    per = {}
    for i, im in bodies[key].items():
        b = raw(im)
        hits = []
        for y in range(256):
            for x in range(256):
                p = pix(b, x, y)
                if p[3] == 0 or lum(p) < 150: continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 256 and 0 <= ny < 256:
                        q = pix(b, nx, ny)
                        if q[3] > 0 and lum(q) <= 70:
                            hits.append((x, y, list(p), list(q)))
                            break
        if hits:
            per[f'{i:02d}'] = {'n': len(hits), 'hits': hits[:40]}
    if per: res['halo150'][key] = per

# (d) front_r/Sword grip overlap via handFront bbox center
cell = ROOT / CELLS['front_r/Sword']
cj = json.loads((cell / 'clip.json').read_text(encoding='utf-8'))
for f in cj['frames']:
    if not f['weaponVisible']: continue
    i = f['index']
    hfim = load(cell / 'layers' / 'handFront' / f'{i:02d}.png')
    hf, wb, wf = raw(hfim), raw(load(cell / 'layers' / 'weaponBack' / f'{i:02d}.png')), raw(load(cell / 'layers' / 'weaponFront' / f'{i:02d}.png'))
    hb = hfim.getbbox()
    if not hb: continue
    gx, gy = (hb[0] + hb[2]) // 2, (hb[1] + hb[3]) // 2
    handle = [(x, y) for y in range(max(0, gy - 14), min(256, gy + 14))
              for x in range(max(0, gx - 14), min(256, gx + 14))
              if pix(wb, x, y)[3] > 0 or (pix(wf, x, y)[3] > 0 and abs(x - gx) <= 8 and abs(y - gy) <= 8)]
    glove = [(x, y) for y in range(max(0, gy - 16), min(256, gy + 16))
             for x in range(max(0, gx - 16), min(256, gx + 16)) if pix(hf, x, y)[3] > 0]
    if handle and glove:
        ov = sum(1 for p in glove if pix(wb, p[0], p[1])[3] > 0 or pix(wf, p[0], p[1])[3] > 0)
        md = min(abs(a - c) + abs(bb - d) for (a, bb) in glove for (c, d) in handle)
        res['front_r_sword_grip'][f'{i:02d}'] = {'center': [gx, gy], 'overlap': ov, 'min_manhattan': md}

# (e) full-body ASCII front_l/Sword F02, F05, F06 + front_r/Sword F02 (native 128)
for key, idxs in [('front_l/Sword', (2, 5, 6)), ('front_r/Sword', (2,))]:
    for i in idxs:
        b = raw(bodies[key][i])
        rows = [f'{y:3d} ' + ''.join(classify(pix(b, x + 64, y + 64)) for x in range(128)) for y in range(128)]
        ascii_out.append(f'== {key} F{i:02d} body native full ==\n' + '\n'.join(rows))

(OUT / 'forensic3.json').write_text(json.dumps(res, ensure_ascii=False), encoding='utf-8')
(OUT / 'forensic3-fullbody.txt').write_text('\n'.join(ascii_out), encoding='utf-8')
print('=== MIRROR front_l vs mirrored front_r (body) ===')
for fam, per in res['mirror'].items():
    print(fam, {k: v['n'] for k, v in per.items()})
print('=== BODY SHARING Sword vs Axe (0 = identical) ===')
print(json.dumps(res['bodySharing']))
print('=== HALO150 counts ===')
for key, per in res['halo150'].items():
    print(key, {k: v['n'] for k, v in per.items()})
print('=== front_r/Sword grip ===')
print(json.dumps(res['front_r_sword_grip']))
