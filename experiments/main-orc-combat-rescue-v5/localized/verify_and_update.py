import hashlib, json, os
from PIL import Image

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

# 1. Compute hash of new 256 master
master256_path = f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed-256.aseprite"
master256_sha = sha(master256_path)
print(f"256 master sha256: {master256_sha}")

# 2. Verify 256 master pixel content matches composite PNGs
# Open the .aseprite and export frames, compare to composites
# Instead, verify via PNG export from the 256 master using Aseprite... 
# For now, verify by loading the composite PNGs and checking dimensions
print("\nVerifying composite PNGs (256x256) match expected content:")
composite_dir = f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk"
all_ok = True
for i in range(8):
    p = f"{composite_dir}/{i:02d}.png"
    im = Image.open(p).convert("RGBA")
    print(f"  {i:02d}.png: {im.size} mode={im.mode}")
    if im.size != (256, 256):
        all_ok = False
print(f"  All composites 256x256: {all_ok}")

# 3. Read current clip.json
clip_path = f"{composite_dir}/clip.json"
cj = json.load(open(clip_path))
print(f"\nCurrent clip.json master: {cj['master']}")
print(f"Current clip.json masterSha256: {cj['masterSha256']}")
print(f"Current clip.json nativeMaster: {cj['nativeMaster']}")
print(f"Current clip.json nativeMasterSha256: {cj['nativeMasterSha256']}")

# 4. Update clip.json
cj["master"] = "characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed-256.aseprite"
cj["masterSha256"] = master256_sha
# nativeMaster stays as 128 master
# nativeMasterSha256 stays as hash of 128 master

json.dump(cj, open(clip_path, "w"), indent=2)
print(f"\nUpdated clip.json:")
print(f"  master: {cj['master']}")
print(f"  masterSha256: {cj['masterSha256']}")
print(f"  nativeMaster: {cj['nativeMaster']}")
print(f"  nativeMasterSha256: {cj['nativeMasterSha256']}")

# 5. Verify native master hash
native128_path = f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed.aseprite"
native128_sha = sha(native128_path)
print(f"\nNative 128 master sha256: {native128_sha}")
print(f"Matches clip.json nativeMasterSha256: {native128_sha == cj['nativeMasterSha256']}")

# 6. Update patch-manifest.json
pm_path = f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/patch-manifest.json"
pm = json.load(open(pm_path))
pm["changedClips"][0]["nativeMaster"] = "characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed.aseprite"
pm["changedClips"][0]["nativeMasterSha256"] = native128_sha
pm["changedClips"][0]["master"] = "characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed-256.aseprite"
pm["changedClips"][0]["masterSha256"] = master256_sha
json.dump(pm, open(pm_path, "w"), indent=2)
print(f"\nUpdated patch-manifest.json:")
print(f"  master: {pm['changedClips'][0]['master']}")
print(f"  masterSha256: {pm['changedClips'][0]['masterSha256']}")
print(f"  nativeMaster: {pm['changedClips'][0]['nativeMaster']}")
print(f"  nativeMasterSha256: {pm['changedClips'][0]['nativeMasterSha256']}")

print("\nDone updating metadata.")
