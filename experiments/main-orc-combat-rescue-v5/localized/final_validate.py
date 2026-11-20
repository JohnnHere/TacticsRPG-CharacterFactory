import json, hashlib, re

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

print("=== 1. patch-manifest.json valid JSON? ===")
pm = json.load(open(f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/patch-manifest.json"))
print("  VALID JSON")
print("  parentManifestSha256:", pm["parentManifestSha256"])

# Verify parent manifest real hash
parent_real = sha(f"{ROOT}/characters/orc-v1/source/rear-reconstruction-v4/candidate28manifest.json")
print("  parent manifest real sha256:", parent_real)
print("  MATCH:", pm["parentManifestSha256"] == parent_real)

print("\n=== 2. clip.json valid JSON & hashes match? ===")
cj = json.load(open(f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/clip.json"))
print("  VALID JSON")
master_ok = sha(f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed.aseprite") == cj["masterSha256"]
strip_ok = sha(f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/native-strip.png") == cj["stripSha256"]
print("  master sha match:", master_ok)
print("  strip sha match:", strip_ok)
frame_ok = all(
    sha(f"{ROOT}/{fr['png']}") == fr["sha256"] and
    sha(f"{ROOT}/{fr['nativePng']}") == fr["nativeSha256"]
    for fr in cj["frames"]
)
print("  all 16 frame hashes match:", frame_ok)

print("\n=== 3. report.md — checking for stale parentManifestSha256 ===")
report = open(f"{ROOT}/experiments/main-orc-combat-rescue-v5/localized/report.md", encoding="utf-8").read()
stale = "51f18754dbb588d9c2c5571b03ca92d5dac8236432137cf14dd5a0976df30e18"
if stale in report:
    print("  FOUND stale hash in report.md — needs correction")
else:
    print("  No stale hash found in report.md")

print("\n=== 4. checkpoint.json valid JSON? ===")
cp = json.load(open(f"{ROOT}/experiments/main-orc-combat-rescue-v5/localized/checkpoint.json"))
print("  VALID JSON")

print("\n=== SUMMARY ===")
all_good = (
    pm["parentManifestSha256"] == parent_real and
    master_ok and strip_ok and frame_ok
)
print("All metadata correct:", all_good)
