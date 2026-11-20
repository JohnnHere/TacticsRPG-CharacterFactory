# V6 frontal forensic 1: structural contracts + body-vs-parent diff for the 4 frontal cells.
# READ-ONLY diagnostic. Pillow never authors production pixels.
import json, hashlib, sys
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

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return Image.open(p).convert('RGBA')

def diff_count(a, b, max_samples=8):
    """Count differing pixels between two same-size RGBA images; collect samples."""
    if a.size != b.size:
        return None, [('SIZE', str(a.size), str(b.size))]
    ab, bb = a.tobytes(), b.tobytes()
    n = len(ab)
    cnt = 0; samples = []
    for i in range(0, n, 4):
        if ab[i:i+4] != bb[i:i+4]:
            cnt += 1
            if len(samples) < max_samples:
                px = i // 4; x = px % a.width; y = px // a.width
                samples.append({'x': x, 'y': y,
                                'a': list(ab[i:i+4]), 'b': list(bb[i:i+4])})
    return cnt, samples

result = {}
summary = []
for key, rel in CELLS.items():
    cell = ROOT / rel
    cj = json.loads((cell / 'clip.json').read_text(encoding='utf-8'))
    entry = {'cell': key, 'dir': rel,
             'frameCount': cj.get('frameCount'),
             'totalDurationMs': cj.get('totalDurationMs'),
             'visibleInterval': cj.get('visibleInterval'),
             'recordedMasterSha_ok': None, 'recordedFrameSha_ok': 0,
             'recordedFrameSha_bad': 0, 'contractFailures': [],
             'parentDiff': {}}
    # recorded master hash (works only while files are untouched V5)
    if 'masterSha256' in cj:
        entry['recordedMasterSha_ok'] = sha(ROOT / cj['master']) == cj['masterSha256']
    vi = cj.get('visibleInterval')
    parent = cj.get('sourceParentClip')
    parent_cell = Path(parent).parent if parent else None
    for f in cj['frames']:
        i = f['index']
        fpath = ROOT / f['png']
        # recorded hashes still valid?
        if sha(fpath) == f['sha256']: entry['recordedFrameSha_ok'] += 1
        else: entry['recordedFrameSha_bad'] += 1
        comp = load(fpath)
        # layer composition contract
        acc = Image.new('RGBA', comp.size, (0, 0, 0, 0))
        layer_ims = {}
        for l in LAYERS:
            lp = ROOT / f['layers'][l]['png']
            im = load(lp)
            layer_ims[l] = im
            acc = Image.alpha_composite(acc, im)
            if not f['weaponVisible'] and l != 'body' and im.getbbox() is not None:
                entry['contractFailures'].append(f'F{i:02d}: {l} not empty on unarmed frame')
        if acc.tobytes() != comp.tobytes():
            entry['contractFailures'].append(f'F{i:02d}: composite != alpha-over(layers)')
        # native crop contract
        nat = load(ROOT / f['nativePng'])
        if layer_ims['body'].crop((64, 64, 192, 192)).tobytes() != nat.tobytes():
            entry['contractFailures'].append(f'F{i:02d}: native != body.crop(64,64,192,192)')
        # body vs parent baseline body
        if parent_cell:
            pb = parent_cell / 'layers' / 'body' / f'{i:02d}.png'
            if pb.exists():
                cnt, samples = diff_count(layer_ims['body'], load(pb))
                entry['parentDiff'][f'{i:02d}'] = {'diff': cnt, 'samples': samples}
            else:
                entry['parentDiff'][f'{i:02d}'] = {'diff': 'parent frame missing'}
    summary.append({'cell': key,
                    'sha_ok': entry['recordedFrameSha_ok'],
                    'sha_bad': entry['recordedFrameSha_bad'],
                    'master_ok': entry['recordedMasterSha_ok'],
                    'contract_fail': len(entry['contractFailures']),
                    'parent_diff_frames': {k: (v['diff'] if isinstance(v['diff'], int) else v['diff'])
                                            for k, v in entry['parentDiff'].items()}})

OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'forensic1-inventory.json').write_text(json.dumps({'summary': summary}, ensure_ascii=False, indent=1), encoding='utf-8')
# full detail with diffs
detail = {}
for key, rel in CELLS.items():
    cell = ROOT / rel
    cj = json.loads((cell / 'clip.json').read_text(encoding='utf-8'))
    parent = cj.get('sourceParentClip'); parent_cell = Path(parent).parent if parent else None
    det = {'dir': rel, 'visibleInterval': cj.get('visibleInterval'), 'frames': {}}
    for f in cj['frames']:
        i = f['index']
        body = load(ROOT / f['layers']['body']['png'])
        d = {'weaponVisible': f['weaponVisible']}
        if parent_cell and (parent_cell / 'layers' / 'body' / f'{i:02d}.png').exists():
            cnt, samples = diff_count(body, load(parent_cell / 'layers' / 'body' / f'{i:02d}.png'), max_samples=12)
            d['parentBodyDiff'] = cnt
            if cnt: d['parentBodySamples'] = samples
        det['frames'][f'{i:02d}'] = d
    detail[key] = det
(OUT / 'forensic1-detail.json').write_text(json.dumps(detail, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(summary, indent=1))
