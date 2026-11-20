# QA parte 4: fixlist Walk back_l vs diff real; duracoes 13 candidatas vs pai
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

report = {}
changed_pixels = {}
walk = {}
v5w = load_json('characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/clip.json')
pw = load_json('characters/orc-v1/source/rear-recovery-v2/back_l/Walk/clip.json')

def arr_native(clip, i):
    fr = clip['frames'][i]
    if fr.get('nativePng'):
        return arr(fr['nativePng'])
    return arr(fr['png'])[64:192, 64:192]

for i in range(8):
    pn = arr_native(pw, i)
    vn = arr_native(v5w, i)
    mask = (pn[..., 3] == vn[..., 3]) & (pn[..., 3] > 0) & np.any(pn[..., :3] != vn[..., :3], axis=-1)
    ys, xs = np.where(mask)
    changed_pixels[i] = set(zip(xs.tolist(), ys.tolist()))
    walk['F0%d' % i] = {'colorChanged': len(ys),
                        'alphaMismatches': int(np.count_nonzero(pn[..., 3] != vn[..., 3]))}
report['walk_backl_actual_diff'] = walk

fixlist = load_json('experiments/main-orc-combat-rescue-v5/localized/backl_walk_arm_fixlist.json')
report['fixlist_type'] = type(fixlist).__name__
if isinstance(fixlist, list):
    report['fixlist_len'] = len(fixlist)
    report['fixlist_sample'] = fixlist[:3]
    frames_fix = {}
    for item in fixlist:
        fi = None
        for k in ('frame', 'targetFrame', 'f', 'index'):
            if isinstance(item, dict) and k in item:
                fi = item[k]; break
        x = y = None
        if isinstance(item, dict):
            x, y = item.get('x'), item.get('y')
            if x is None:
                for kx, ky in (('px', 'py'), ('col', 'row')):
                    if kx in item:
                        x, y = item[kx], item[ky]; break
        if fi is not None and x is not None:
            frames_fix.setdefault(int(fi), []).append((int(x), int(y)))
    report['fixlist_perframe'] = {str(k): len(v) for k, v in sorted(frames_fix.items())}
    anomalies = []
    matched = 0
    for fi, pixels in frames_fix.items():
        real = changed_pixels.get(fi, set())
        miss = [p for p in pixels if p not in real]
        matched += len(pixels) - len(miss)
        if miss:
            anomalies.append({'frame': fi, 'missing': len(miss), 'sample': miss[:5]})
    extra = {}
    for fi, real in changed_pixels.items():
        fix = set(frames_fix.get(fi, []))
        ex = [p for p in real if p not in fix]
        if ex:
            extra[str(fi)] = {'count': len(ex), 'sample': ex[:5]}
    report['fixlist_matched_real'] = matched
    report['fixlist_anomalies'] = anomalies
    report['fixlist_extra_changes_not_in_list'] = extra
elif isinstance(fixlist, dict):
    report['fixlist_keys'] = list(fixlist.keys())[:20]

dur = {}
subs = ['combat/%s/%s' % (d, a) for a in ('Unarmed', 'Sword', 'Axe') for d in ('front_r', 'front_l', 'back_r', 'back_l')]
subs.append('localized/back_l/Walk')
for sub in subs:
    v5 = load_json('characters/orc-v1/source/combat-rescue-v5/%s/clip.json' % sub)
    parent_path = v5.get('provenance', {}).get('parentClip') or ''
    entry = {'v5': [f['durationMs'] for f in v5['frames']], 'parentPath': parent_path}
    if parent_path and os.path.exists(rp(parent_path)):
        pp = load_json(parent_path)
        entry['parent'] = [f['durationMs'] for f in pp['frames']]
        entry['identical'] = entry['v5'] == entry['parent']
    dur[sub] = entry
report['candidate_durations_vs_parent'] = dur

with open(os.path.join(OUT, 'numeric-checks-part4.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)
print('PART4 OK')
