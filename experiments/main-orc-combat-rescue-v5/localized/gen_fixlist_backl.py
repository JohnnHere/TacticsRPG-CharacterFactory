from PIL import Image
import os, json
from collections import Counter

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)

def load(p):
    return Image.open(p).convert("RGBA")

# back_l Walk arms: right arm x in [128,146], left arm x in [108,126], y in [56,102]
# Reference: F(i) for i in 0..3 ; fix F(i+4) to match F(i) at arm pixels where both opaque & differ.
ARM_RIGHT = (128, 56, 147, 103)
ARM_LEFT  = (108, 56, 127, 103)

clip = "characters/orc-v1/source/rear-recovery-v2/back_l/Walk"
frames = [load(f"{clip}/{i:02d}.png") for i in range(8)]

fixes = []  # {frame, x, y, old, new, arm, pair}
for arm_name, (x0,y0,x1,y1) in [("right", ARM_RIGHT), ("left", ARM_LEFT)]:
    for i in range(4):
        j = i + 4
        fa = frames[i].load(); fj = frames[j].load()
        for y in range(y0, y1):
            for x in range(x0, x1):
                va = fa[x, y]; vb = fj[x, y]
                if va[3] > 0 and vb[3] > 0 and va != vb:
                    # Fix frame j to match reference frame i
                    fixes.append({
                        "fix_frame": j,
                        "ref_frame": i,
                        "x": x, "y": y,
                        "old": list(vb), "new": list(va),
                        "arm": arm_name,
                        "pair": f"F{i:02d}/F{j:02d}"
                    })

print(f"Total arm pixels to normalize (back_l Walk): {len(fixes)}")
by_frame = Counter(f["fix_frame"] for f in fixes)
print("By frame:", dict(sorted(by_frame.items())))
by_arm = Counter(f["arm"] for f in fixes)
print("By arm:", dict(by_arm))

# Check: are reference frames F0-F3 free of bright outliers at arms?
print("\nReference frames (F0-F3) bright outlier check at arms (sum>400):")
for i in range(4):
    px = frames[i].load()
    br = [(x,y,px[x,y]) for y in range(56,103) for x in list(range(128,147))+list(range(108,127)) if px[x,y][3]==255 and sum(px[x,y][:3])>400]
    print(f"  F{i:02d}: bright_outliers={br[:6]}")

# Save fix list
out = {
    "clip": clip,
    "direction": "back_l",
    "action": "Walk",
    "defect": "reararm shading flicker between half-cycle frames",
    "total_fixes": len(fixes),
    "fixes": fixes
}
with open("experiments/main-orc-combat-rescue-v5/localized/backl_walk_arm_fixlist.json", "w") as f:
    json.dump(out, f, indent=1)
print("\nSaved fix list to experiments/main-orc-combat-rescue-v5/localized/backl_walk_arm_fixlist.json")
