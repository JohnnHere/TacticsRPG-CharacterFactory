from PIL import Image
import os, json

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)
ED = "characters/orc-v1/source/combat-rescue-v5/localized/frames"
ORIG_CLIP = "characters/orc-v1/source/rear-recovery-v2/back_l/Walk"

def load(p):
    return Image.open(p).convert("RGBA")

# Load fix list
with open("experiments/main-orc-combat-rescue-v5/localized/backl_walk_arm_fixlist.json") as f:
    fixdata = json.load(f)
fixes = fixdata["fixes"]

# Load fixed frames
fixed = [load(f"{ED}/f{i:02d}.png") for i in range(8)]
# Load original composites (before)
orig = [load(f"{ORIG_CLIP}/{i:02d}.png") for i in range(8)]

alpha_changed = 0
color_only_changed = 0
not_opposite_opaque = 0
entries = []

for fx in fixes:
    cx, cy = fx["x"], fx["y"]              # composite coord (as stored)
    nx, ny = fx["x"] - 64, fx["y"] - 64    # native coord
    fi = fx["fix_frame"]
    ov = orig[fi].load()[cx, cy]           # before (composite)
    fv = fixed[fi].load()[nx, ny]          # after (fixed native)
    new_rgba = fx["new"]
    entries.append({
        "frame": fi, "composite_x": cx, "composite_y": cy,
        "native_x": nx, "native_y": ny,
        "before": list(ov), "after": list(fv),
        "arm": fx["arm"], "pair": fx["pair"],
    })
    if ov[3] != fv[3]:
        alpha_changed += 1
    if ov[3] > 0 and fv[3] > 0 and ov[:3] != fv[:3] and ov[3] == fv[3]:
        color_only_changed += 1

print("Total fix entries:", len(entries))
print("Entries where ALPHA changed (should be 0):", alpha_changed)
print("Entries where only COLOR changed, alpha preserved:", color_only_changed)

# Sample a few entries
print()
print("Sample before/after (color changes, alpha preserved):")
shown = 0
for e in entries:
    if e["before"][:3] != e["after"][:3] and e["before"][3] == e["after"][3]:
        print(f"  F{e['frame']} ({e['native_x']},{e['native_y']}) arm={e['arm']} {e['pair']}:")
        print(f"    before={tuple(e['before'])}  after={tuple(e['after'])}")
        shown += 1
        if shown >= 8:
            break

# Save inventory
inv = {
    "clip": ORIG_CLIP,
    "direction": "back_l",
    "action": "Walk",
    "defect": "reararm shading flicker between half-cycle frames",
    "total_fixes": len(entries),
    "alpha_changed_count": alpha_changed,
    "color_only_changed_count": color_only_changed,
    "entries": entries,
}
with open("experiments/main-orc-combat-rescue-v5/localized/before_after_inventory.json", "w") as f:
    json.dump(inv, f, indent=1)
print("\nSaved before_after_inventory.json")

# Also verify mask: are all fixed pixels opaque in BOTH before and after?
mask_ok = True
for e in entries:
    if e["before"][3] == 0 or e["after"][3] == 0:
        mask_ok = False
        print("NON-OPAQUE FOUND:", e)
print("Mask OK (all fixed pixels opaque before+after):", mask_ok)
