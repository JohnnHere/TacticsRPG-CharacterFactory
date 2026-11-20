# QA parte 3: preservacao frontal Sword/Axe vs pai + separacao corpo Sword/Axe traseiro
import json, os
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
OUT = os.path.join(ROOT, 'experiments', 'main-orc-combat-rescue-v5', 'qa', 'evidence')

def rp(rel):
    return os.path.join(ROOT, rel.replace('/', os.sep))

def load_json(rel):
    with open(rp(rel), 'r', encoding='utf-8') as f:
        return json.load(f)

def arr(rel):
    return np.array(Image.open(rp(rel)).convert('RGBA'), dtype=np.int16)

def pixel_diffs(a, b):
    da = (a[..., 3] > 0) != (b[..., 3] > 0)
    rgb = np.any(a[..., :3] != b[..., :3], axis=-1) & (a[..., 3] > 0) & (b[..., 3] > 0)
    return int(np.count_nonzero(da)), int(np.count_nonzero(rgb))

report = {}

pres = {}
for cell in ['front_r/Sword', 'front_l/Sword', 'front_r/Axe', 'front_l/Axe']:
    v5 = load_json('characters/orc-v1/source/combat-rescue-v5/combat/%s/clip.json' % cell)
    pa = load_json('characters/orc-v1/source/rear-reconstruction-v4/%s/clip.json' % cell)
    body_a = body_c = hand_a = hand_c = 0
    dur_ok = len(v5['frames']) == len(pa['frames']) and all(
        v5['frames'][i]['durationMs'] == pa['frames'][i]['durationMs'] for i in range(len(v5['frames'])))
    for i in range(len(v5['frames'])):
        fv, fp = v5['frames'][i], pa['frames'][i]
        bva, bpa = arr(fv['layers']['body']['png']), arr(fp['layers']['body']['png'])
        hva, hpa = arr(fv['layers']['handFront']['png']), arr(fp['layers']['handFront']['png'])
        da, dc = pixel_diffs(bva, bpa); body_a += da; body_c += dc
        da, dc = pixel_diffs(hva, hpa); hand_a += da; hand_c += dc
    pres[cell] = {'frames': len(v5['frames']), 'durationsIdentical': dur_ok,
                  'bodyAlphaDiffs': body_a, 'bodyColorDiffs': body_c,
                  'handAlphaDiffs': hand_a, 'handColorDiffs': hand_c}
report['front_weapon_preservation_vs_parent'] = pres

sep = {}
bboxes = {}
for direction in ['back_r', 'back_l']:
    s = load_json('characters/orc-v1/source/combat-rescue-v5/combat/%s/Sword/clip.json' % direction)
    a = load_json('characters/orc-v1/source/combat-rescue-v5/combat/%s/Axe/clip.json' % direction)
    per = []
    bb_s, bb_a = [], []
    for i in range(8):
        bs = arr(s['frames'][i]['layers']['body']['png'])[64:192, 64:192]
        ba = arr(a['frames'][i]['layers']['body']['png'])[64:192, 64:192]
        da, dc = pixel_diffs(bs, ba)
        per.append(da + dc)
        for store, img in ((bb_s, bs), (bb_a, ba)):
            ys, xs = np.where(img[..., 3] > 0)
            store.append([int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None)
    sep[direction] = per
    bboxes[direction] = {'Sword': bb_s, 'Axe': bb_a}
report['sword_vs_axe_body_diffs_native'] = sep
report['rear_body_bboxes_native'] = bboxes

with open(os.path.join(OUT, 'numeric-checks-part3.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)
print('PART3 OK')
