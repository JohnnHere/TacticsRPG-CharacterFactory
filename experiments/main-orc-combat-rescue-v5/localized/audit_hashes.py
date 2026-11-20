import hashlib, json, os

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

files = [
    # parent manifest (must match real value)
    ("PARENT manifest rear-reconstruction-v4/candidate28manifest.json",
     f"{ROOT}/characters/orc-v1/source/rear-reconstruction-v4/candidate28manifest.json"),
    # my patch manifest
    ("patch-manifest.json",
     f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/patch-manifest.json"),
    # my clip.json
    ("clip.json",
     f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/clip.json"),
    # my native master aseprite
    ("native master walk-back_l-fixed.aseprite",
     f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed.aseprite"),
    # my strip
    ("native-strip.png",
     f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/native-strip.png"),
]

for label, p in files:
    print(f"{label}:")
    print(f"  path: {p}")
    print(f"  sha256: {sha(p)}")
    print()

# Also verify all composite PNGs and native PNGs hashes match what clip.json claims
print("=== Verifying clip.json frame hashes against actual files ===")
cj = json.load(open(f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/clip.json"))
all_ok = True
for fr in cj["frames"]:
    p = f"{ROOT}/{fr['png']}"
    actual = sha(p)
    ok = actual == fr["sha256"]
    if not ok:
        all_ok = False
    print(f"  {fr['png']}: claimed={fr['sha256'][:12]}... actual={actual[:12]}... {'OK' if ok else 'MISMATCH'}")
    np = f"{ROOT}/{fr['nativePng']}"
    actual_n = sha(np)
    ok_n = actual_n == fr["nativeSha256"]
    if not ok_n:
        all_ok = False
    print(f"    native {fr['nativePng']}: claimed={fr['nativeSha256'][:12]}... actual={actual_n[:12]}... {'OK' if ok_n else 'MISMATCH'}")
print(f"\nAll clip frame hashes match: {all_ok}")

# Verify master sha in clip.json matches actual master file
master_actual = sha(f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed.aseprite")
print(f"\nclip.json masterSha256: {cj['masterSha256']}")
print(f"master file actual:     {master_actual}")
print(f"match: {master_actual == cj['masterSha256']}")

# Verify strip sha
strip_actual = sha(f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/native-strip.png")
print(f"\nclip.json stripSha256: {cj['stripSha256']}")
print(f"strip file actual:     {strip_actual}")
print(f"match: {strip_actual == cj['stripSha256']}")
