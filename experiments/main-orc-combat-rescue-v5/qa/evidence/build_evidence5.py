# QA parte 5: valida fixlist Walk back_l contra pixels reais (espaco 256): coords, old, new, arm zonas
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

fx = load_json('experiments/main-orc-combat-rescue-v5/localized/backl_walk_arm_fixlist.json')
v5w = load_json('characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/clip.json')
pw = load_json('characters/orc-v1/source/rear-recovery-v2/back_l/Walk/clip.json')

P = {i: arr(pw['frames'][i]['png']) for i in range(8)}
V = {i: arr(v5w['frames'][i]['png']) for i in range(8)}

res = {'declared_total': fx['total_fixes'], 'entries': len(fx['fixes'])}
mismatch_coord = 0
mismatch_old = 0
mismatch_new = 0
ok_new = 0
arm_zone_violation = []
frame_counts = {}
arm_counts = {}
old_values = {}
for it in fx['fixes']:
    fi, x, y = it['fix_frame'], it['x'], it['y']
    frame_counts[fi] = frame_counts.get(fi, 0) + 1
    arm_counts[it['arm']] = arm_counts.get(it['arm'], 0) + 1
    p, v = P[fi], V[fi]
    if tuple(p[y, x][:3]) != tuple(it['new'][:3]) or v[y, x][3] != 255 or p[y, x][3] != 255:
        # verifica onde falhou
        if tuple(p[y, x][:3]) != tuple(v[y, x][:3]):
            if tuple(p[y, x][:3]) != tuple(it['old'][:3]):
                mismatch_old += 1
            elif tuple(v[y, x][:3]) != tuple(it['new'][:3]):
                mismatch_new += 1
            else:
                mismatch_coord += 1
        else:
            mismatch_new += 1 if tuple(v[y, x][:3]) != tuple(it['new'][:3]) else 0
            ok_new += 1 if tuple(v[y, x][:3]) == tuple(it['new'][:3]) else 0
    else:
        ok_new += 1
    # zona do braco no espaco 256: right x[128,146], left x[108,126]
    if it['arm'] == 'right' and not (128 <= x <= 146):
        arm_zone_violation.append((fi, x, y, 'right'))
    if it['arm'] == 'left' and not (108 <= x <= 126):
        arm_zone_violation.append((fi, x, y, 'left'))
    old_values.setdefault(it['arm'], {}).setdefault(str(it['old'][:3]), 0)
    old_values[it['arm']][str(it['old'][:3])] += 1

res['frame_counts'] = frame_counts
res['arm_counts'] = arm_counts
res['verify_parent_equals_new'] = ok_new
res['mismatch_coord'], res['mismatch_old'], res['mismatch_new'] = mismatch_coord, mismatch_old, mismatch_new
res['arm_zone_violations'] = arm_zone_violation[:10]
res['arm_zone_violation_count'] = len(arm_zone_violation)
res['old_color_distribution'] = old_values

# mudancas reais totais no composto por frame (deve igualar fixlist)
real = {}
for i in range(8):
    mask = (P[i][..., 3] == V[i][..., 3]) & (P[i][..., 3] > 0) & np.any(P[i][..., :3] != V[i][..., :3], axis=-1)
    real[i] = int(np.count_nonzero(mask))
res['real_composite_changes_per_frame'] = real

with open(os.path.join(OUT, 'numeric-checks-part5-fixlist.json'), 'w', encoding='utf-8') as f:
    json.dump(res, f, indent=2)
print('PART5 OK', res['verify_parent_equals_new'], res['mismatch_coord'], res['mismatch_old'], res['mismatch_new'])
