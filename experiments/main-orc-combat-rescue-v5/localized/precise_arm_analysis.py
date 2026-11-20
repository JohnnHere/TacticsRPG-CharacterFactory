from PIL import Image
import os

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)

def load(p):
    return Image.open(p).convert("RGBA")

def px(im, x, y):
    return im.load()[x, y]

# For rear walk, compare F(i) vs F(i+half) at the arm pixel locations.
# The arm is roughly at x in [30,100] of the 128 canvas region... but these are 256x256
# composites with bodyOffset [64,64]. Let me sample the left arm (image-left) and right arm
# (image-right) regions of each composite.
# Let me instead diff the whole frame and list differing pixel coords clustered by region,
# focusing on the arm area, between F(i) and F(i+half).

def diff_pixels(a, b):
    pa = a.load(); pb = b.load()
    w, h = a.size
    diffs = []
    for y in range(h):
        for x in range(w):
            if pa[x, y] != pb[x, y]:
                diffs.append((x, y, pa[x, y], pb[x, y]))
    return diffs

def cluster_regions(diffs, label):
    # Group differing pixels into rough bands: left arm x<120, center 120-136, right arm x>136
    left = [d for d in diffs if d[0] < 120]
    center = [d for d in diffs if 120 <= d[0] <= 136]
    right = [d for d in diffs if d[0] > 136]
    print(f"  {label}: total={len(diffs)}  leftArm={len(left)}  center={len(center)}  rightArm={len(right)}")
    # Show a few samples per region
    for region_name, region in [("leftArm", left), ("center", center), ("rightArm", right)]:
        if region:
            # count alpha-only vs color
            alpha_only = sum(1 for d in region if d[2][:3] == d[3][:3])
            color = len(region) - alpha_only
            print(f"     {region_name}: alpha-only={alpha_only} color={color}")
            # show up to 3 distinct color transitions
            shown = 0
            seen = set()
            for d in region:
                key = (d[2], d[3])
                if key not in seen:
                    seen.add(key)
                    print(f"       @({d[0]},{d[1]}): {d[2]} -> {d[3]}")
                    shown += 1
                    if shown >= 3:
                        break

print("=" * 70)
print("REAR WALK: F(i) vs F(i+half) arm flicker analysis (same arm pose)")
print("=" * 70)
for direction, clipdir, nframes in [
    ("back_r", "characters/orc-v1/source/rear-recovery-v2/back_r/Walk", 8),
    ("back_l", "characters/orc-v1/source/rear-recovery-v2/back_l/Walk", 8),
]:
    print(f"\n=== {direction} Walk ===")
    half = nframes // 2
    for i in range(half):
        a = load(f"{clipdir}/{i:02d}.png")
        b = load(f"{clipdir}/{i+half:02d}.png")
        diffs = diff_pixels(a, b)
        cluster_regions(diffs, f"F{i:02d} vs F{i+half:02d}")

print("\n" + "=" * 70)
print("FRONT WALK: F(i) vs F(i+half) cloth flicker analysis (between legs)")
print("=" * 70)
for direction, clipdir, nframes in [
    ("front_r", "characters/orc-v1/source/complete-v1/front_r/Walk", 16),
    ("front_l", "characters/orc-v1/source/complete-v1/front_l/Walk", 16),
]:
    print(f"\n=== {direction} Walk ===")
    half = nframes // 2
    for i in range(half):
        a = load(f"{clipdir}/{i:02d}.png")
        b = load(f"{clipdir}/{i+half:02d}.png")
        diffs = diff_pixels(a, b)
        cluster_regions(diffs, f"F{i:02d} vs F{i+half:02d}")
