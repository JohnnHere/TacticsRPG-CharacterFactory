"""Build the Pilot B1 review images and the front_r grip profile, from the authored output."""
import json
from pathlib import Path

import numpy as np
from PIL import Image

E = Path(__file__).resolve().parent
ROOT = E.parents[1]
SRC = ROOT / 'characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_r-sword'
CLIP = json.loads((SRC / 'clip.json').read_text(encoding='utf-8'))
VER = json.loads((E / 'verification.json').read_text(encoding='utf-8'))
FIT = json.loads((E / 'grip-pivot-fit.json').read_text(encoding='utf-8'))
STATS = json.loads((E / 'blade-repaint-stats.json').read_text(encoding='utf-8'))
FRAMES = [2, 8, 11]

# grip profile for this direction, mirroring the Experiment 04 contract
grip_by_index = {s['frame']: s for s in STATS}
profile = {
    'schemaVersion': 1,
    'family': 'Sword/basic.sword-slash',
    'direction': 'front_r',
    'animationSource': str(SRC / 'clip.json').replace('\\', '/'),
    'sourceSha256': VER['sourceClipSha256'],
    'hand': 'anatomical right hand; original body glove + original handFront per frame',
    'canvas': list(CLIP.get('canvas', [256, 256])),
    'assetCanvas': [96, 96],
    'assetGrip': [48, 66],
    'pivotSource': 'grip-pivot-fit.json (front_r declares rotationDeg but grip=null)',
    'pivot': {str(k): v for k, v in grip_by_index.items()},
    'layerOrder': CLIP['layerOrder'],
    'occlusion': {
        'weaponBack': 'original per-frame mask, cleared only where the blade is repainted',
        'weaponFront': 'original guard/pommel preserved; blade rewritten from sword-b',
        'handFront': 'original traced glove, unchanged, overlays the front weapon',
    },
    'bladeRule': ('original weapon pixels whose inverse asset coordinate is v <= 54 are repainted '
                  'with sword-b, with u clamped to the opaque extent of that row so B follows the '
                  'original blade silhouette instead of leaving a rim of the old blade'),
    'visibleInterval': CLIP['visibleInterval'],
    'contactEvent': CLIP['contactEvent'],
    'durationsMs': CLIP['durationsMs'],
    'totalDurationMs': CLIP['totalDurationMs'],
    'reuseFrom': 'experiments/main-orc-hybrid-weapon-04 (same sword-a and sword-b assets, byte-identical)',
}
(E / 'grip-profile-front-r.json').write_text(json.dumps(profile, indent=2), encoding='utf-8')

# representative comparison, 2x: original / A / B / body only
rows = [('ORIGINAL', SRC / 'frames'),
        ('A - espada do recruta', E / 'full/a/composite'),
        ('B - aco claro', E / 'full/b/composite'),
        ('SOMENTE CORPO', E / 'full/a/body-only')]
Z, GAP = 2, 10
tiles = []
for label, base in rows:
    for idx in FRAMES:
        name = '{:02d}.png'.format(idx) if base.name == 'frames' else 'F{:02d}.png'.format(idx)
        im = Image.open(base / name).convert('RGBA')
        tiles.append(im.resize((im.width * Z, im.height * Z), Image.NEAREST))
tw, th = tiles[0].size
sheet = Image.new('RGBA', (tw * len(FRAMES) + GAP * (len(FRAMES) + 1),
                           th * len(rows) + GAP * (len(rows) + 1)), (32, 34, 42, 255))
for i, im in enumerate(tiles):
    r, c = divmod(i, len(FRAMES))
    sheet.paste(im, (GAP + c * (tw + GAP), GAP + r * (th + GAP)))
sheet.save(E / 'representative-review-2x.png')

# grip zoom at 10x, A vs B, around the hand of the contact frame
hand = np.array(Image.open(E / 'full/a/layers/handFront/F08.png').convert('RGBA'))
ys, xs = np.nonzero(hand[:, :, 3] > 0)
cx, cy = int(xs.mean()), int(ys.mean())
box = (cx - 20, cy - 20, cx + 20, cy + 20)
Z2 = 10
crops = []
for v in ('a', 'b'):
    im = Image.open(E / 'full/{}/composite/F08.png'.format(v)).convert('RGBA').crop(box)
    crops.append(im.resize((im.width * Z2, im.height * Z2), Image.NEAREST))
cw, ch = crops[0].size
out = Image.new('RGBA', (cw * 2 + 30, ch + 20), (32, 34, 42, 255))
out.paste(crops[0], (10, 10))
out.paste(crops[1], (cw + 20, 10))
out.save(E / 'grip-10x-both.png')
print('images + profile written; grip box', box)
