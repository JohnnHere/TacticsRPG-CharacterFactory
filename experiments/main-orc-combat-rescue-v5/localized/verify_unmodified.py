from PIL import Image
import os, hashlib

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)

def sha(p):
    h = hashlib.sha256()
    with open(p,"rb") as f: h.update(f.read())
    return h.hexdigest()

ORIG = "characters/orc-v1/source/rear-recovery-v2/back_l/Walk"
FIXED = "characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk"
print("F | origCompositeSha | fixedCompositeSha | identical?")
all_ok = True
for i in range(8):
    o = sha(f"{ORIG}/{i:02d}.png")
    fx = sha(f"{FIXED}/{i:02d}.png")
    ok = (o == fx)
    if not ok: all_ok = False
    print(f"{i:02d} | {o} | {fx} | {ok}")
print("\nUnmodified F0-F3 identical:", all_ok and True)
# Check specifically F0-F3
f03_ok = all(sha(f"{ORIG}/{i:02d}.png") == sha(f"{FIXED}/{i:02d}.png") for i in range(4))
print("F0-F3 byte-identical to original:", f03_ok)
print("F4-F7 intentionally differ (fixed):", all(sha(f"{ORIG}/{i:02d}.png") != sha(f"{FIXED}/{i:02d}.png") for i in range(4,8)))
