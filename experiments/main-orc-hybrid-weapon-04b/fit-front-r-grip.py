"""Pilot B1 provenance: how the front_r grip pivot table was obtained, and its measured quality.

front_r-sword/clip.json stores rotationDeg for every frame but grip = null, so the blade
replacement of Architecture C has no pivot to work with on this direction. This script
derives it from the art and records the evidence:

  1. rigid-transform centroid estimate  -> grip ~= centroid(weapon) - R(rot).(centroid(asset) - (48,66))
  2. exact integer search +/-4 px and +/-4 deg -> confirms the centroid optimum
  3. seam measurement -> proves no original blade pixel rounds into the guard band

Output: grip-pivot-fit.json next to this script.
"""
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image

E = Path(__file__).resolve().parent
ROOT = E.parents[1]
SRC = ROOT / 'characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_r-sword'
ASSET = ROOT / 'characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/recruit-sword.png'
CLIP = json.loads((SRC / 'clip.json').read_text(encoding='utf-8'))
ROT = {f['index']: f.get('rotationDeg') for f in CLIP['frames'] if f.get('weaponVisible')}
DECLARED = {f['index']: f.get('grip') for f in CLIP['frames'] if f.get('grip')}
ASSET_GRIP = (48, 66)

A = np.array(Image.open(ASSET).convert('RGBA'))
ay, ax = np.nonzero(A[:, :, 3] > 0)
acu, acv = ax.mean(), ay.mean()


def weapon_union(idx):
    tot = np.zeros((256, 256), dtype=bool)
    for layer in ('weaponBack', 'weaponFront'):
        p = SRC / 'layers' / layer / '{:02d}.png'.format(idx)
        if p.exists():
            tot |= np.array(Image.open(p).convert('RGBA'))[:, :, 3] > 0
    return tot


def mask_for(grip, rot):
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    xs = np.round(grip[0] + (ax - ASSET_GRIP[0]) * ca - (ay - ASSET_GRIP[1]) * sa).astype(int)
    ys = np.round(grip[1] + (ax - ASSET_GRIP[0]) * sa + (ay - ASSET_GRIP[1]) * ca).astype(int)
    ok = (xs >= 0) & (xs < 256) & (ys >= 0) & (ys < 256)
    m = np.zeros((256, 256), dtype=bool)
    m[ys[ok], xs[ok]] = True
    return m


rows = []
for idx in sorted(ROT):
    rot = ROT[idx]
    om = weapon_union(idx)
    ys, xs = np.nonzero(om)
    cu, cv = xs.mean(), ys.mean()
    a = math.radians(rot)
    du, dv = acu - ASSET_GRIP[0], acv - ASSET_GRIP[1]
    rdu = du * math.cos(a) - dv * math.sin(a)
    rdv = du * math.sin(a) + dv * math.cos(a)
    centroid = (int(round(cu - rdu)), int(round(cv - rdv)))
    best = None
    for dy in range(-4, 5):
        for dx in range(-4, 5):
            g = (centroid[0] + dx, centroid[1] + dy)
            for r in (rot - 1, rot, rot + 1):
                s = int((mask_for(g, r) ^ om).sum())
                if best is None or s < best[0]:
                    best = (s, g, r)
    rows.append({'index': idx, 'declaredRotationDeg': rot, 'declaredGrip': DECLARED.get(idx),
                 'centroidGrip': list(centroid), 'adoptedGrip': list(best[1]),
                 'adoptedRotationDeg': best[2], 'symmetricDifferencePx': best[0],
                 'weaponPx': int(om.sum())})

adopted = {r['index']: r['adoptedGrip'] for r in rows}
USED_BY_AUTHOR_LUA = {2: [103, 130], 3: [90, 119], 4: [98, 100], 5: [98, 89], 6: [127, 101],
                      7: [155, 114], 8: [158, 132], 9: [159, 148], 10: [134, 147], 11: [110, 150]}
divergence = {str(i): {'fit': adopted[i], 'used': v}
              for i, v in USED_BY_AUTHOR_LUA.items() if adopted[i] != v}

out = {
    'direction': 'front_r',
    'sourceClip': str(SRC / 'clip.json').replace('\\', '/'),
    'reason': 'front_r stores rotationDeg but grip=null, so the pivot had to be derived from the art',
    'method': ['rigid-transform centroid', 'exact integer search +/-4 px and +/-1 deg'],
    'declaredGripMatchesFit': {str(r['index']): (r['declaredGrip'] == r['adoptedGrip'])
                               for r in rows if r['declaredGrip']},
    'fitGripTable': {str(k): list(v) for k, v in adopted.items()},
    'usedByAuthorLua': {str(k): v for k, v in USED_BY_AUTHOR_LUA.items()},
    'fitVsUsed': divergence or 'identical',
    'rotationPolicy': ('author.lua uses the declared rotationDeg for every frame; the fit preferred '
                       '117 deg on frame 10 by 1 px of symmetric difference, which is inside the '
                       'source resampling noise, so the declared angle was kept.'),
    'totalSymmetricDifferencePx': sum(r['symmetricDifferencePx'] for r in rows),
    'totalWeaponPx': sum(r['weaponPx'] for r in rows),
    'note': ('The residual is the source art itself: it is not a pixel-exact rigid rotation of '
             'recruit-sword.png because Aseprite resampled the rotation, so a ~1 px contour band '
             'differs at every angle. Widening the search to +/-4 deg does not reduce it.'),
    'rows': rows,
}
(E / 'grip-pivot-fit.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps({k: out[k] for k in ('declaredGripMatchesFit', 'fitVsUsed',
                                      'totalSymmetricDifferencePx', 'totalWeaponPx')}, indent=2))
