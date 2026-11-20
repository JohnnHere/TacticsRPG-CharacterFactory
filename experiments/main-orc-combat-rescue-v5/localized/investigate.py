from PIL import Image
import os, sys, hashlib

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)

def load(p):
    return Image.open(p).convert("RGBA")

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def frame_diff(a, b):
    """Return count of differing pixels and list of (x,y) where alpha>0 in either."""
    pa = a.load(); pb = b.load()
    w, h = a.size
    diffs = []
    for y in range(h):
        for x in range(w):
            ra, ga, ba, aa = pa[x, y]
            rb, gb, bb, ab = pb[x, y]
            if (ra, ga, ba, aa) != (rb, gb, bb, ab):
                diffs.append((x, y))
    return diffs

# ---- WALK investigation ----
walk_clips = {
    "front_r": ("characters/orc-v1/source/complete-v1/front_r/Walk", 16),
    "front_l": ("characters/orc-v1/source/complete-v1/front_l/Walk", 16),
    "back_r":  ("characters/orc-v1/source/rear-recovery-v2/back_r/Walk", 8),
    "back_l":  ("characters/orc-v1/source/rear-recovery-v2/back_l/Walk", 8),
}

print("=" * 70)
print("WALK frame-by-frame investigation (neighbor diffs)")
print("=" * 70)
for direction, (clipdir, nframes) in walk_clips.items():
    print(f"\n--- {direction} Walk ({nframes} frames) ---")
    frames = []
    for i in range(nframes):
        p = f"{clipdir}/{i:02d}.png"
        im = load(p)
        frames.append(im)
        print(f"  F{i:02d}: {p} size={im.size} sha={sha(p)[:12]}")
    # Compare each frame to its successor (and wrap last->first for loop)
    for i in range(nframes):
        j = (i + 1) % nframes
        diffs = frame_diff(frames[i], frames[j])
        # Separate alpha-only changes vs color changes
        alpha_only = 0
        color_changes = 0
        pa = frames[i].load(); pb = frames[j].load()
        for (x, y) in diffs:
            ra, ga, ba, aa = pa[x, y]
            rb, gb, bb, ab = pb[x, y]
            if (ra, ga, ba) == (rb, gb, bb):
                alpha_only += 1
            else:
                color_changes += 1
        print(f"  F{i:02d}->F{j:02d}: {len(diffs):4d} px differ (color={color_changes}, alpha-only={alpha_only})")

# ---- DEFEAT investigation ----
defeat_clips = {
    "front_r": "characters/orc-v1/source/rear-recovery-v2/front_r/Defeat",
    "front_l": "characters/orc-v1/source/rear-recovery-v2/front_l/Defeat",
}

print("\n" + "=" * 70)
print("DEFEAT frame investigation (hands F02/F03, terminal F04)")
print("=" * 70)
for direction, clipdir in defeat_clips.items():
    print(f"\n--- {direction} Defeat ---")
    for i in range(5):
        p = f"{clipdir}/{i:02d}.png"
        im = load(p)
        print(f"  F{i}: {p} size={im.size} sha={sha(p)[:12]}")
    # Compare F02->F03->F04 for hand smear
    f2 = load(f"{clipdir}/02.png")
    f3 = load(f"{clipdir}/03.png")
    f4 = load(f"{clipdir}/04.png")
    d23 = frame_diff(f2, f3)
    d34 = frame_diff(f3, f4)
    print(f"  F02->F03: {len(d23)} px differ")
    print(f"  F03->F04: {len(d34)} px differ")
    # Check for partial alpha (smear indicator) in F02/F03
    for fi in [2, 3]:
        im = load(f"{clipdir}/{fi:02d}.png")
        px = im.load()
        partial = 0
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                a = px[x, y][3]
                if 0 < a < 255:
                    partial += 1
        print(f"  F{fi}: partial-alpha pixels = {partial}")

print("\nInvestigation complete.")
