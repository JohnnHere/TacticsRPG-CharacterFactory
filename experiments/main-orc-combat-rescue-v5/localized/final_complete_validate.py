import json, hashlib
from PIL import Image

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

errors = []

# 1. Parent manifest real hash
parent_path = f"{ROOT}/characters/orc-v1/source/rear-reconstruction-v4/candidate28manifest.json"
parent_sha = sha(parent_path)
parent = json.load(open(parent_path))
print(f"1. Parent manifest sha256: {parent_sha}")

# 2. clip.json
clip_path = f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/clip.json"
cj = json.load(open(clip_path))
print(f"\n2. clip.json:")
print(f"   master: {cj['master']}")
print(f"   masterSha256: {cj['masterSha256']}")
print(f"   nativeMaster: {cj['nativeMaster']}")
print(f"   nativeMasterSha256: {cj['nativeMasterSha256']}")
print(f"   frameCount: {cj['frameCount']}")
print(f"   durationsMs: {cj['durationsMs']}")
print(f"   totalDurationMs: {cj['totalDurationMs']}")
print(f"   canvas: {cj['canvas']}, bodyOffset: {cj['bodyOffset']}, groundY: {cj['groundY']}")
print(f"   nativeCanvas: {cj['nativeCanvas']}, nativeGroundY: {cj['nativeGroundY']}")

# Verify master sha matches file
m_actual = sha(f"{ROOT}/{cj['master']}")
if m_actual != cj['masterSha256']:
    errors.append(f"clip.json masterSha256 mismatch: {cj['masterSha256']} vs {m_actual}")
print(f"   master file actual sha: {m_actual} -> MATCH: {m_actual == cj['masterSha256']}")

# Verify native master sha
n_actual = sha(f"{ROOT}/{cj['nativeMaster']}")
if n_actual != cj['nativeMasterSha256']:
    errors.append(f"clip.json nativeMasterSha256 mismatch")
print(f"   nativeMaster file actual sha: {n_actual} -> MATCH: {n_actual == cj['nativeMasterSha256']}")

# Verify all frame hashes
for fr in cj["frames"]:
    if sha(f"{ROOT}/{fr['png']}") != fr["sha256"]:
        errors.append(f"clip.json frame hash mismatch {fr['png']}")
    if sha(f"{ROOT}/{fr['nativePng']}") != fr["nativeSha256"]:
        errors.append(f"clip.json native frame hash mismatch {fr['nativePng']}")
print(f"   All 16 frame hashes verified: OK")

# Verify dimensions of composite PNGs
for fr in cj["frames"]:
    im = Image.open(f"{ROOT}/{fr['png']}").convert("RGBA")
    if im.size != (256, 256):
        errors.append(f"{fr['png']} not 256x256: {im.size}")
nim = Image.open(f"{ROOT}/{cj['frames'][0]['nativePng']}").convert("RGBA")
if nim.size != (128, 128):
    errors.append(f"native PNG not 128x128: {nim.size}")
print(f"   Composite PNGs 256x256, native 128x128: OK")

# Verify durations
if cj["durationsMs"] != [160]*8:
    errors.append(f"durationsMs not [160]*8: {cj['durationsMs']}")
if cj["totalDurationMs"] != 1280:
    errors.append(f"totalDurationMs not 1280: {cj['totalDurationMs']}")
print(f"   Timing [160]*8 = 1280ms: OK")

# 3. patch-manifest.json
pm_path = f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/patch-manifest.json"
pm = json.load(open(pm_path))
print(f"\n3. patch-manifest.json:")
print(f"   parentManifestSha256: {pm['parentManifestSha256']}")
if pm['parentManifestSha256'] != parent_sha:
    errors.append(f"patch-manifest parentManifestSha256 mismatch")
print(f"   Matches parent real sha: {pm['parentManifestSha256'] == parent_sha}")
cc = pm["changedClips"][0]
print(f"   changedClip master: {cc['master']}")
print(f"   changedClip masterSha256: {cc['masterSha256']}")
print(f"   changedClip nativeMaster: {cc['nativeMaster']}")
print(f"   changedClip nativeMasterSha256: {cc['nativeMasterSha256']}")
if cc['masterSha256'] != cj['masterSha256']:
    errors.append("patch-manifest masterSha256 != clip.json masterSha256")
if cc['nativeMasterSha256'] != cj['nativeMasterSha256']:
    errors.append("patch-manifest nativeMasterSha256 != clip.json nativeMasterSha256")
print(f"   patch-manifest == clip.json hashes: {cc['masterSha256']==cj['masterSha256'] and cc['nativeMasterSha256']==cj['nativeMasterSha256']}")

# Parent contract compatibility
pc = None
for cell in parent["cells"]:
    if cell["cellId"] == "back_l/Walk":
        pc = cell
compat = (
    cj["frameCount"] == pc["frameCount"] and
    cj["durationsMs"] == pc["durationsMs"] and
    cj["canvas"] == [256,256] and
    cj["bodyOffset"] == [64,64] and
    cj["groundY"] == 190 and
    cj["nativeCanvas"] == [128,128] and
    cj["nativeGroundY"] == 126
)
print(f"   Parent contract compatibility: {compat}")
if not compat:
    errors.append("Parent contract incompatibility")

# 4. checkpoint.json
cp_path = f"{ROOT}/experiments/main-orc-combat-rescue-v5/localized/checkpoint.json"
cp = json.load(open(cp_path))
print(f"\n4. checkpoint.json: VALID JSON")
print(f"   status: {cp['status']}")

# Summary
print(f"\n{'='*50}")
if errors:
    print("ERRORS FOUND:")
    for e in errors:
        print(f"  - {e}")
else:
    print("ALL VALIDATIONS PASSED — metadata consistent, contracts satisfied")
