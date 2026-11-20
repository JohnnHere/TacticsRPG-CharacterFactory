from PIL import Image
import hashlib

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
EXPORT_DIR = f"{ROOT}/experiments/main-orc-combat-rescue-v5/localized/master256_export"
COMPOSITE_DIR = f"{ROOT}/characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

print("Comparing 256 master exported frames vs composite PNGs:")
all_match = True
for i in range(8):
    exp = Image.open(f"{EXPORT_DIR}/m{i:02d}.png").convert("RGBA")
    comp = Image.open(f"{COMPOSITE_DIR}/{i:02d}.png").convert("RGBA")
    if exp.size != comp.size:
        print(f"  F{i:02d}: SIZE MISMATCH master={exp.size} composite={comp.size}")
        all_match = False
        continue
    ep = exp.load(); cp = comp.load()
    diffs = 0
    for y in range(256):
        for x in range(256):
            if ep[x,y] != cp[x,y]:
                diffs += 1
    status = "MATCH" if diffs == 0 else f"{diffs} px DIFFER"
    if diffs != 0:
        all_match = False
    print(f"  F{i:02d}: {status}")
print(f"\nAll 8 frames pixel-identical: {all_match}")
