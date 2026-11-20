from PIL import Image

k1 = Image.open('experiments/main-orc-rear-recovery-v2/walk_back_r_key_contact1.png')
k2 = Image.open('experiments/main-orc-rear-recovery-v2/walk_back_r_key_contact2.png')
base = Image.open('experiments/main-orc-complete-v1/pixellab-recovery/back_r_base.png')

print("=== Foot bounds at y=115..126 ===")
for name, im in [("Base", base), ("K1 (Contact 1)", k1), ("K2 (Contact 2)", k2)]:
    pts = [(x, y) for y in range(115, 127) for x in range(128) if im.getpixel((x, y))[3] > 128]
    xs = [p[0] for p in pts]
    print(f"{name}: min_x={min(xs)}, max_x={max(xs)}, foot_span={max(xs)-min(xs)+1}")
    # find left foot (x < 64) and right foot (x >= 64)
    l_pts = [p for p in pts if p[0] < 64]
    r_pts = [p for p in pts if p[0] >= 64]
    l_box = (min(p[0] for p in l_pts), max(p[0] for p in l_pts), min(p[1] for p in l_pts), max(p[1] for p in l_pts)) if l_pts else None
    r_box = (min(p[0] for p in r_pts), max(p[0] for p in r_pts), min(p[1] for p in r_pts), max(p[1] for p in r_pts)) if r_pts else None
    print(f"  Left foot box (x_min, x_max, y_min, y_max): {l_box}")
    print(f"  Right foot box: {r_box}")
