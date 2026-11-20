# QA-only magnification helper (no art authoring; analysis/inspection).
# Usage: venv python qa_zoom.py
from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "qa-zoom"
OUT.mkdir(exist_ok=True)
BG = (70, 70, 78, 255)  # neutral mid-gray backdrop so alpha content is visible


def load_rgba(rel):
    img = Image.open(ROOT / rel).convert("RGBA")
    return img


def flatten(img):
    base = Image.new("RGBA", img.size, BG)
    base.alpha_composite(img)
    return base


def zoom(img, factor):
    return img.resize((img.width * factor, img.height * factor), Image.NEAREST)


def save(img, name):
    img.convert("RGB").save(OUT / name)
    print("saved", name, img.size)


def crop_zoom(rel, box, factor, name, grid=None):
    img = flatten(load_rgba(rel)).crop(box)
    img = zoom(img, factor)
    if grid:
        px = img.load()
        step = box_step = grid * factor
        for gx in range(0, img.width, step):
            for y in range(img.height):
                if px[gx, y][0] > 100:
                    px[gx, y] = (255, 255, 0)
        for gy in range(0, img.height, step):
            for x in range(img.width):
                if px[x, gy][2] < 150:
                    px[x, gy] = (255, 255, 0)
    save(img, name)
    return img


# 1. New rear sword key (128x128, weapon baked) full at 3x with 16px grid
crop_zoom("experiments/main-orc-rear-recovery-v2/raw/clean_sword_slash_r.png",
          (0, 0, 128, 128), 3, "key-sword-r-3x-grid16.png", grid=16)

# 2. Old empty-hand body layer, sword keyframe 07 (256x256) at 2x
crop_zoom("characters/orc-v1/source/complete-v1/back_r/Sword/Attack/layers/body/07.png",
          (0, 0, 256, 256), 2, "old-body-07-2x.png")

# 3. Old weaponBack layer 07 at 2x
crop_zoom("characters/orc-v1/source/complete-v1/back_r/Sword/Attack/layers/weaponBack/07.png",
          (0, 0, 256, 256), 2, "old-weaponBack-07-2x.png")

# 4. Old composite frame 07 at 2x
crop_zoom("characters/orc-v1/source/complete-v1/back_r/Sword/Attack/07.png",
          (0, 0, 256, 256), 2, "old-composite-07-2x.png")

# 5. Front unarmed right-arm region: frames 01/02/03 cropped (x 90..210, y 70..170) at 4x
for f in ("01", "02", "03"):
    crop_zoom(f"characters/orc-v1/source/complete-v1/front_r/Unarmed/{f}.png",
              (90, 70, 210, 170), 4, f"front-unarmed-{f}-arm-4x.png", grid=16)


# ---- part 2: cycle strips, axe key, front_l defect ----

def strip(rels, factor, name):
    imgs = [flatten(load_rgba(r)) for r in rels]
    w = sum(i.width for i in imgs)
    h = max(i.height for i in imgs)
    s = Image.new("RGBA", (w, h), BG)
    x = 0
    for i in imgs:
        s.alpha_composite(i, (x, 0))
        x += i.width
    save(zoom(s, factor), name)


D = "characters/orc-v1/source/complete-v1/back_r/Sword/Attack"
strip([f"{D}/%02d.png" % i for i in range(13)], 1, "old-sword-composites-strip.png")
strip([f"{D}/layers/body/%02d.png" % i for i in range(13)], 1, "old-sword-bodies-strip.png")

crop_zoom("experiments/main-orc-rear-recovery-v2/raw/clean_sword_slash_r.png",
          (96, 30, 128, 74), 8, "key-sword-r-hand-8x.png")

crop_zoom("experiments/main-orc-rear-recovery-v2/test_axe_r_clean.png",
          (0, 0, 128, 128), 3, "key-axe-r-3x-grid16.png", grid=16)

for f in ("01", "02", "03"):
    crop_zoom(f"characters/orc-v1/source/complete-v1/front_l/Unarmed/{f}.png",
              (46, 70, 166, 170), 4, f"front_l-unarmed-{f}-arm-4x.png", grid=16)

# QA-only analysis: measure hand clusters on old rear weapon-cycle bodies,
# verify axe/sword body equality, and emit marked strips + JSON (analysis only).
from PIL import Image
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "qa-zoom"
D = "characters/orc-v1/source/complete-v1/back_r"
sys.path.insert(0, str(Path(__file__).resolve().parent))

BG = (70, 70, 78, 255)


def load_rgba(rel):
    return Image.open(ROOT / rel).convert("RGBA")


def opaque_mask(img):
    px = img.load()
    w, h = img.size
    m = [[(px[x, y][3] > 40) for x in range(w)] for y in range(h)]
    return m, px, w, h


def rightmost_cluster_centroid(img, x_min=120):
    """Largest connected opaque cluster whose centroid x is >= x_min (arm/hand side)."""
    m, px, w, h = opaque_mask(img)
    seen = [[False] * w for _ in range(h)]
    best = None
    for yy in range(h):
        for xx in range(x_min, w):
            if m[yy][xx] and not seen[yy][xx]:
                stack = [(xx, yy)]
                seen[yy][xx] = True
                pts = []
                while stack:
                    cx, cy = stack.pop()
                    pts.append((cx, cy))
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and m[ny][nx] and not seen[ny][nx]:
                            seen[ny][nx] = True
                            stack.append((nx, ny))
                if len(pts) >= 12:
                    sx = sum(p[0] for p in pts) / len(pts)
                    sy = sum(p[1] for p in pts) / len(pts)
                    maxx = max(p[0] for p in pts)
                    if sx >= x_min and (best is None or maxx > best[0]):
                        best = (maxx, sx, sy, len(pts), pts)
    if best is None:
        return None
    return {"tipX": best[0], "cx": round(best[1], 1), "cy": round(best[2], 1), "px": best[3]}


def marked(img, hand, radius=2):
    base = Image.new("RGBA", img.size, BG)
    base.alpha_composite(img)
    px = base.load()
    if hand:
        cx, cy = int(round(hand["cx"])), int(round(hand["cy"]))
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x, y = cx + dx, cy + dy
                if 0 <= x < base.width and 0 <= y < base.height and dx * dx + dy * dy <= radius * radius:
                    px[x, y] = (255, 80, 255, 255)
    return base


def hand_extremity(img):
    """Erode the silhouette to strip the torso; the surviving arm appendage's
    farthest point from the body centroid is the hand. Returns hand centroid."""
    from PIL import ImageFilter
    alpha = img.getchannel("A")
    solid = alpha.point(lambda a: 255 if a > 40 else 0)
    er = solid
    for _ in range(3):
        er = er.filter(ImageFilter.MinFilter(5))
    w, h = img.size
    sp, ep = solid.load(), er.load()
    pts = [(x, y) for y in range(h) for x in range(w) if sp[x, y] and not ep[x, y]]
    if not pts:
        return None
    # body centroid from eroded core
    core = [(x, y) for y in range(h) for x in range(w) if ep[x, y]]
    bcx = sum(p[0] for p in core) / len(core)
    bcy = sum(p[1] for p in core) / len(core)
    tip = max(pts, key=lambda p: (p[0] - bcx) ** 2 + (p[1] - bcy) ** 2)
    near = [p for p in pts if (p[0] - tip[0]) ** 2 + (p[1] - tip[1]) ** 2 <= 64]
    cx = sum(p[0] for p in near) / len(near)
    cy = sum(p[1] for p in near) / len(near)
    return {"cx": round(cx, 1), "cy": round(cy, 1), "tip": list(tip), "armPx": len(pts)}


out = {}
for weapon, n in (("Sword", 13), ("Axe", 12)):
    hands = []
    for i in range(n):
        rel = "%s/%s/Attack/layers/body/%02d.png" % (D, weapon, i)
        img = load_rgba(rel)
        hand = hand_extremity(img)
        hands.append(hand)
    out["back_r/%s" % weapon] = hands

# axe body == sword body? (compare bytes for overlapping frames)
import hashlib
same = []
for i in range(12):
    ra = "%s/Sword/Attack/layers/body/%02d.png" % (D, i)
    rb = "%s/Axe/Attack/layers/body/%02d.png" % (D, i)
    a = (ROOT / ra).read_bytes()
    b = (ROOT / rb).read_bytes()
    same.append(a == b)
out["bodyEquality_sword_vs_axe_0_11"] = same

# marked strips
for weapon, n in (("Sword", 13), ("Axe", 12)):
    imgs = [marked(load_rgba(f"{D}/{weapon}/Attack/layers/body/%02d.png" % i), out[f"back_r/{weapon}"][i]) for i in range(n)]
    w, h = imgs[0].width, imgs[0].height
    strip = Image.new("RGBA", (w * n, h), BG)
    for i, im in enumerate(imgs):
        strip.alpha_composite(im, (i * w, 0))
    strip.convert("RGB").save(OUT / f"marked-hands-{weapon.lower()}-strip.png")
    print("saved marked strip", weapon)

# weapon layers content bboxes (old placements) for sword and axe
bboxes = {}
for weapon, n in (("Sword", 13), ("Axe", 12)):
    for layer in ("weaponBack", "weaponFront"):
        for i in range(n):
            rel = f"{D}/{weapon}/Attack/layers/{layer}/%02d.png" % i
            img = load_rgba(rel)
            bbox = img.getbbox()
            if bbox:
                bboxes[f"{weapon}/{layer}/{i:02d}"] = list(bbox)
# gridded sword body halves for direct visual grip reading
from PIL import ImageDraw
raw = [load_rgba("%s/Sword/Attack/layers/body/%02d.png" % (D, i)) for i in range(13)]
for half in (0, 1):
    frames = raw[half * 7: half * 7 + 7]
    idxs = list(range(half * 7, half * 7 + 7))
    w, h = 256, 256
    strip = Image.new("RGBA", (w * len(frames), h), BG)
    for k, im in enumerate(frames):
        strip.alpha_composite(im, (k * w, 0))
    strip = strip.convert("RGB")
    dr = ImageDraw.Draw(strip)
    for gx in range(0, strip.width, 32):
        col = (255, 255, 0) if (gx // 256) % 2 == 0 else (0, 255, 255)
        dr.line([(gx, 0), (gx, h)], fill=col, width=1)
    for gy in range(0, h, 32):
        dr.line([(0, gy), (strip.width, gy)], fill=(0, 255, 0), width=1)
    for k, fi in enumerate(idxs):
        for vx in range(0, 256, 64):
            dr.text((k * 256 + vx + 2, 2), str(vx), fill=(255, 255, 0))
        for vy in range(0, 256, 64):
            dr.text((k * 256 + 2, vy + 2), str(vy), fill=(0, 255, 0))
        dr.text((k * 256 + 2, h - 12), "f%02d" % fi, fill=(255, 120, 255))
    save(zoom(strip, 2), "sword-bodies-grid-half%d.png" % half)

