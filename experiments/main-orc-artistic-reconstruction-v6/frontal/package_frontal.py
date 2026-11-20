# V6 frontal package: clip.json per cell + patch-manifest + preservation + strip checks.
import json, hashlib
from pathlib import Path
from PIL import Image

ROOT = Path.cwd()
OUT = Path('experiments/main-orc-artistic-reconstruction-v6/frontal')
V5BASE = 'characters/orc-v1/source/combat-rescue-v5/grip-specialist'
V6BASE = 'characters/orc-v1/source/artistic-reconstruction-v6/frontal'
CELLS = {
    'front_l/Sword': 'front_l-Sword-full',
    'front_r/Sword': 'full-front-r-sword',
    'front_r/Axe':   'front_r-Axe-full',
    'front_l/Axe':   'front_l-Axe-full',
}
LAYERS = ['weaponBack', 'body', 'weaponFront', 'handFront']

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, v): Path(p).write_text(json.dumps(v, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
plan = json.loads((OUT / 'fixes-plan.json').read_text(encoding='utf-8'))['plan']
n_edits = {k: sum(len(v) for v in plan[k].values()) for k in plan}
n_isl = {k: sum(1 for v in plan[k].values() for e in v if e['kind'] == 'island') for k in plan}

pres = {'v5Untouched': True, 'files': 0}
patch = []
for key, slug in CELLS.items():
    v5 = json.loads((ROOT / V5BASE / slug / 'clip.json').read_text(encoding='utf-8'))
    # preservation: every hash recorded in V5 clip.json still valid (sources untouched)
    def check_hash(rec_path, rec_sha):
        nonlocal_ok = sha(ROOT / rec_path) == rec_sha
        if not nonlocal_ok: pres['v5Untouched'] = False
        pres['files'] += 1
        return nonlocal_ok
    check_hash(v5['master'], v5['masterSha256'])
    check_hash(v5['bodyMaster'], v5['bodyMasterSha256'])
    check_hash(v5['nativeMaster'], v5['nativeMasterSha256'])
    check_hash(v5['handMaster'], v5['handMasterSha256'])
    for f in v5['frames']:
        check_hash(f['png'], f['sha256']); check_hash(f['nativePng'], f['nativeSha256'])
        for l in LAYERS: check_hash(f['layers'][l]['png'], f['layers'][l]['sha256'])
    # build V6 clip: rewrite cell-local paths, recompute hashes; keep everything else
    c = json.loads(json.dumps(v5))
    def rw(p):
        return p.replace(f'{V5BASE}/{slug}/', f'{V6BASE}/{slug}/')
    c['revision'] = 'main-orc-artistic-reconstruction-v6-frontal'
    c['checkpoint'] = 'V6_FRONTAL_LOCAL_FIXES_READY'
    c['technicalStatus'] = 'TECHNICALLY_COMPLETE'
    c['artisticStatus'] = 'VISUAL_REVIEW_REQUIRED'
    c['artisticApproval'] = 'PENDING_CREATOR'
    c['eligibleForIntegration'] = False
    c['runtimeImplemented'] = False
    c['fullClipIndependentQA'] = 'PENDING_QA_V6_ORCHESTRATOR_HANDOFF'
    for k in ('master', 'bodyMaster', 'nativeMaster', 'handMaster', 'strip', 'nativeStrip', 'compositeStrip'):
        c[k] = rw(c[k]); c[k + 'Sha256'] = sha(ROOT / c[k])
    # strips aliases: V5 had strip==nativeStrip pointing to same file; keep semantics
    for f in c['frames']:
        f['png'] = rw(f['png']); f['sha256'] = sha(ROOT / f['png'])
        f['nativePng'] = rw(f['nativePng']); f['nativeSha256'] = sha(ROOT / f['nativePng'])
        for l in LAYERS:
            f['layers'][l]['png'] = rw(f['layers'][l]['png'])
            f['layers'][l]['sha256'] = sha(ROOT / f['layers'][l]['png'])
        fidk = f"{f['index']:02d}"
        f['v6FrontalFixEdits'] = len(plan[key].get(fidk, []))
        if f['v6FrontalFixEdits']:
            f['v6FrontalFixIslands'] = sum(1 for e in plan[key][fidk] if e['kind'] == 'island')
    c['v6FrontalFix'] = {
        'script': 'experiments/main-orc-artistic-reconstruction-v6/frontal/fix-frontal.lua',
        'reexportScript': 'experiments/main-orc-artistic-reconstruction-v6/frontal/export-fix.lua',
        'plan': 'experiments/main-orc-artistic-reconstruction-v6/frontal/fixes-plan.json',
        'verification': 'experiments/main-orc-artistic-reconstruction-v6/frontal/verify-result.json',
        'report': 'experiments/main-orc-artistic-reconstruction-v6/frontal/report.md',
        'rule': 'Isolated neutral bright pixels (L>=170, neutral, zero bright 4-neighbours) refilled with median of opaque dark neighbours (fallback ink 12,15,18); fully disconnected rgba(0,0,1) islands made transparent. Single-pixel edits only; no other pixel touched (verified vs before snapshot).',
        'editsApplied': n_edits[key], 'islandRemovals': n_isl[key],
        'bodyTimingChanged': False, 'weaponLayersChanged': False,
        'visualLimitation': 'DEV worked without image perception (textual/Pillow forensics); independent visual QA still required.'}
    dest = ROOT / V6BASE / slug / 'clip.json'
    write(dest, c)
    patch.append({'direction': v5['direction'], 'category': v5['category'],
                  'beforeClip': f'{V5BASE}/{slug}/clip.json',
                  'clip': f'{V6BASE}/{slug}/clip.json',
                  'clipSha256': sha(dest), 'edits': n_edits[key]})

# strips: tiles must equal frame pixels
strips = {'ok': True, 'cells': {}}
for key, slug in CELLS.items():
    c = json.loads((ROOT / V6BASE / slug / 'clip.json').read_text(encoding='utf-8'))
    n = c['frameCount']
    for kind, strip_rel, fw, fh in (('composite', c['compositeStrip'], 256, 256), ('native', c['nativeStrip'], 128, 128)):
        st = Image.open(ROOT / strip_rel).convert('RGBA')
        assert st.size == (n * fw, fh), (strip_rel, st.size)
        for i in range(n):
            f = c['frames'][i]
            fr = Image.open(ROOT / (f['png'] if kind == 'composite' else f['nativePng'])).convert('RGBA')
            tile = st.crop((i * fw, 0, (i + 1) * fw, fh))
            if tile.tobytes() != fr.tobytes():
                strips['ok'] = False
                strips['cells'].setdefault(key, []).append(f'{kind} F{i:02d} mismatch')

write(OUT / 'patch-manifest.json', {
    'schemaVersion': 1, 'checkpoint': 'V6_FRONTAL_LOCAL_FIXES_READY',
    'technicalStatus': 'TECHNICALLY_COMPLETE', 'artisticStatus': 'VISUAL_REVIEW_REQUIRED',
    'creatorApproval': 'PENDING_CREATOR', 'runtimeImplemented': False,
    'cells': patch,
    'preservation': pres, 'strips': strips})
print('preservation v5 untouched:', pres['v5Untouched'], 'files checked:', pres['files'])
print('strips ok:', strips['ok'], strips['cells'])
print('patch cells:', [(p['direction'] + '/' + p['category'], p['edits']) for p in patch])
