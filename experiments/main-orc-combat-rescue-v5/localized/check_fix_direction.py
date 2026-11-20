from PIL import Image
import os

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)
ED = "characters/orc-v1/source/combat-rescue-v5/localized/frames"
ORIG_CLIP = "characters/orc-v1/source/rear-recovery-v2/back_l/Walk"

def load(p):
    return Image.open(p).convert("RGBA")

fixed = [load(f"{ED}/f{i:02d}.png") for i in range(8)]
orig = [load(f"{ORIG_CLIP}/{i:02d}.png") for i in range(8)]

# For the sample points, show F0-F3 (reference half) colors at same native coord
# and F4-F7 (fixed half) BEFORE (from orig composite) vs AFTER.
samples = [
    (4, 64, 9), (4, 64, 10), (4, 65, 10), (4, 64, 11),
]
print("native coord -> F0,F1,F2,F3 (reference) colors ; F4 before/after ; F5,F6,F7")
for (fi, nx, ny) in samples:
    refs = [tuple(orig[i].load()[nx+64, ny+64]) for i in range(4)]
    before4 = tuple(orig[4].load()[nx+64, ny+64])
    after4 = tuple(fixed[4].load()[nx, ny])
    f567 = [tuple(fixed[i].load()[nx, ny]) for i in (5, 6, 7)]
    print(f"  ({nx},{ny}): F0-F3={refs} | F4 before={before4} after={after4} | F5,F6,F7={f567}")

print()
print("=== Check: is the reference half (F0-F3) internally consistent at arm? ===")
print("(Compare F0 vs F2 at same arm coords where both opaque - should match if consistent phase)")
# Actually F0 and F2 are NOT same phase (arm moves). Skip.
print("Key question: does F0-F3 have consistent shading, and F4-F7 was the inconsistent half?")
print("The fix normalized F4-F7 -> F0-F3. Verify F0-F3 reference frames have the SAME color")
print("at a given arm coord across... they don't need to (arm moves).")

# Better: confirm the bright outlier (184,186,185) that was at F04 composite (137,84) = native (73,20)
print()
print("Bright outlier check: composite (137,84) = native (73,20)")
for i in range(8):
    v = orig[i].load()[137, 84]
    print(f"  F{i} composite(137,84) = {v}  -> native(73,20)")
print("  FIXED F4 native(73,20) =", tuple(fixed[4].load()[73, 20]))
