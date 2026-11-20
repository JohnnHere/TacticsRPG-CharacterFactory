import hashlib, json
from PIL import Image

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
EXPORT_DIR = f"{ROOT}/experiments/main-orc-combat-rescue-v5/localized/master256_export"
COMPOSITE_DIR = f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

# 1. Verify pixels still match composites
print("=== Pixel verification (256 master vs composites) ===")
all_match = True
for i in range(8):
    exp = Image.open(f"{EXPORT_DIR}/m{i:02d}.png").convert("RGBA")
    comp = Image.open(f"{COMPOSITE_DIR}/{i:02d}.png").convert("RGBA")
    ep, cp = exp.load(), comp.load()
    diffs = sum(1 for y in range(256) for x in range(256) if ep[x,y] != cp[x,y])
    if diffs != 0:
        all_match = False
        print(f"  F{i:02d}: {diffs} px DIFFER")
print(f"All 8 frames pixel-identical: {all_match}")

# 2. Compute new master256 hash
master256_path = f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed-256.aseprite"
master256_sha = sha(master256_path)
print(f"\n256 master sha256: {master256_sha}")

# 3. Update clip.json
clip_path = f"{COMPOSITE_DIR}/clip.json"
cj = json.load(open(clip_path))
cj["master"] = "characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed-256.aseprite"
cj["masterSha256"] = master256_sha
json.dump(cj, open(clip_path, "w"), indent=2)
print(f"\nclip.json updated:")
print(f"  master: {cj['master']}")
print(f"  masterSha256: {cj['masterSha256']}")
print(f"  nativeMaster: {cj['nativeMaster']}")
print(f"  nativeMasterSha256: {cj['nativeMasterSha256']}")

# 4. Update patch-manifest.json
pm_path = f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/patch-manifest.json"
pm = json.load(open(pm_path))
pm["changedClips"][0]["master"] = "characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed-256.aseprite"
pm["changedClips"][0]["masterSha256"] = master256_sha
json.dump(pm, open(pm_path, "w"), indent=2)
print(f"\npatch-manifest.json updated:")
print(f"  master: {pm['changedClips'][0]['master']}")
print(f"  masterSha256: {pm['changedClips'][0]['masterSha256']}")

print("\n=== Final metadata state ===")
print(f"  clip.json masterSha256: {cj['masterSha256']}")
print(f"  patch-manifest masterSha256: {pm['changedClips'][0]['masterSha256']}")
print(f"  Match: {cj['masterSha256'] == pm['changedClips'][0]['masterSha256']}")
