import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory")
OUT = ROOT / "experiments/main-orc-combat-rescue-v5/qa-grok/evidence"


def load(rel):
    return Image.open(ROOT / rel).convert("RGBA")


def crop_scale(im, box, n, title):
    x0, y0, x1, y1 = box
    c = im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * n, (y1 - y0) * n), Image.NEAREST)
    tile = Image.new("RGBA", (c.width, c.height + 14), (10, 14, 18, 255))
    tile.paste(c, (0, 14))
    ImageDraw.Draw(tile).text((2, 0), title, fill=(230, 200, 120, 255))
    return tile


def stack(tiles):
    w = sum(t.width for t in tiles)
    h = max(t.height for t in tiles)
    sheet = Image.new("RGBA", (w, h), (8, 10, 14, 255))
    x = 0
    for t in tiles:
        sheet.paste(t, (x, 0))
        x += t.width
    return sheet


# Attacking-arm zooms on native 128. back_r arm is screen-right; back_l is screen-left.
rows = []
specs = [
    ("back_r/Sword", 3, (78, 8, 127, 70)),
    ("back_r/Sword", 4, (78, 8, 127, 78)),
    ("back_r/Axe", 1, (70, 0, 120, 55)),
    ("back_r/Axe", 2, (70, 0, 120, 55)),
    ("back_r/Axe", 4, (70, 40, 127, 100)),
    ("back_l/Sword", 2, (0, 0, 50, 60)),
    ("back_l/Sword", 3, (0, 8, 55, 70)),
    ("back_l/Sword", 4, (0, 20, 55, 80)),
    ("back_l/Axe", 1, (8, 0, 60, 50)),
    ("back_l/Axe", 2, (8, 0, 60, 50)),
    ("back_l/Axe", 4, (0, 40, 55, 95)),
]
for key, idx, box in specs:
    direction, action = key.split("/")
    im = load(f"characters/orc-v1/source/combat-rescue-v5/combat/{direction}/{action}/native/{idx:02d}.png")
    rows.append(crop_scale(im, box, 5, f"{key} F{idx:02d}"))
# two rows
mid = 6
r1 = stack(rows[:mid])
r2 = stack(rows[mid:])
sheet = Image.new("RGBA", (max(r1.width, r2.width), r1.height + r2.height), (8, 10, 14, 255))
sheet.paste(r1, (0, 0))
sheet.paste(r2, (0, r1.height))
sheet.save(OUT / "rear_arm_zooms.png")

# Front unarmed F02 vs F03 fist side
urows = []
for direction, box in (("front_r", (70, 30, 120, 90)), ("front_l", (8, 30, 58, 90))):
    tiles = []
    for idx in (2, 3):
        im = load(f"characters/orc-v1/source/combat-rescue-v5/combat/{direction}/Unarmed/native/{idx:02d}.png")
        tiles.append(crop_scale(im, box, 5, f"{direction} Unarmed F{idx:02d}"))
    urows.append(stack(tiles))
sheet = Image.new("RGBA", (max(t.width for t in urows), sum(t.height for t in urows)), (8, 10, 14, 255))
y = 0
for t in urows:
    sheet.paste(t, (0, y))
    y += t.height
sheet.save(OUT / "unarmed_f02_f03.png")

# Defeat hand zooms F02 F03 F04. Alias lives in rear-recovery-v2; frame png may be 256.
drows = []
for direction in ("front_r", "front_l"):
    clip = json.loads((ROOT / f"characters/orc-v1/source/rear-recovery-v2/{direction}/Defeat/clip.json").read_text(encoding="utf-8"))
    tiles = []
    for idx, box in ((2, (40, 90, 200, 230)), (3, (30, 100, 210, 240)), (4, (20, 80, 230, 250))):
        im = load(clip["frames"][idx]["png"])
        if im.size == (128, 128):
            box = tuple(v // 2 for v in box)
        x0, y0, x1, y1 = box
        x1, y1 = min(x1, im.width), min(y1, im.height)
        tiles.append(crop_scale(im, (x0, y0, x1, y1), 3, f"{direction} Defeat F{idx:02d}"))
    drows.append(stack(tiles))
sheet = Image.new("RGBA", (max(t.width for t in drows), sum(t.height for t in drows)), (8, 10, 14, 255))
y = 0
for t in drows:
    sheet.paste(t, (0, y))
    y += t.height
sheet.save(OUT / "defeat_hands.png")

# Walk back_l arm before/after using parent rear-recovery-v2
parent = json.loads((ROOT / "characters/orc-v1/source/rear-recovery-v2/back_l/Walk/clip.json").read_text(encoding="utf-8"))
tiles = []
for idx in range(8):
    new = load(f"characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/native/{idx:02d}.png")
    old_rel = Path(parent["frames"][idx]["png"]).parent / "native" / f"{idx:02d}.png"
    if not (ROOT / old_rel).exists():
        old_rel = Path(parent["frames"][idx]["png"])
    old = load(old_rel)
    if old.size != new.size:
        # 256 composite: crop the native window
        old = old.crop((64, 64, 192, 192))
    box = (30, 18, 100, 70)
    pair = stack([
        crop_scale(old, box, 4, f"parent F{idx:02d}"),
        crop_scale(new, box, 4, f"v5 F{idx:02d}"),
    ])
    tiles.append(pair)
sheet = Image.new("RGBA", (tiles[0].width * 4, tiles[0].height * 2), (8, 10, 14, 255))
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % 4) * t.width, (i // 4) * t.height))
sheet.save(OUT / "walk_arms_before_after.png")
print("walk parent frame0", parent["frames"][0]["png"])
print("saved zooms")
