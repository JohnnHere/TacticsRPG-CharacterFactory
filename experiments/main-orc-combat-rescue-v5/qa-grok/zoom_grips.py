import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory")
OUT = ROOT / "experiments/main-orc-combat-rescue-v5/qa-grok/evidence"
manifest = json.loads((ROOT / "characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json").read_text(encoding="utf-8"))
cells = {f"{c['direction']}/{c['action']}": c for c in manifest["cells"]}


def load(rel):
    return Image.open(ROOT / rel).convert("RGBA")


picks = [
    ("front_r/Sword", 6),
    ("front_r/Axe", 5),
    ("front_l/Sword", 6),
    ("back_r/Sword", 4),
    ("back_r/Axe", 4),
    ("back_l/Sword", 3),
    ("back_l/Sword", 4),
    ("back_l/Axe", 1),
    ("back_l/Axe", 4),
    ("back_r/Axe", 2),
]
rows = []
notes = []
for key, idx in picks:
    clip = json.loads((ROOT / cells[key]["clipJson"]).read_text(encoding="utf-8"))
    fr = clip["frames"][idx]
    body = load(fr["layers"]["body"]["png"])
    hand = load(fr["layers"]["handFront"]["png"])
    wf = load(fr["layers"]["weaponFront"]["png"])
    wb = load(fr["layers"]["weaponBack"]["png"])
    comp = Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(wb, body), wf), hand)
    pts = [(i % hand.width, i // hand.width, p) for i, p in enumerate(hand.getdata()) if p[3]]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, y0 = max(0, min(xs) - 22), max(0, min(ys) - 34)
    x1, y1 = min(comp.width, max(xs) + 23), min(comp.height, max(ys) + 23)
    crop = comp.crop((x0, y0, x1, y1)).resize(((x1 - x0) * 6, (y1 - y0) * 6), Image.NEAREST)
    bcrop = body.crop((x0, y0, x1, y1)).resize(((x1 - x0) * 6, (y1 - y0) * 6), Image.NEAREST)
    hcrop = hand.crop((x0, y0, x1, y1)).resize(((x1 - x0) * 6, (y1 - y0) * 6), Image.NEAREST)
    tile = Image.new("RGBA", (crop.width * 3 + 12, crop.height + 18), (12, 16, 20, 255))
    tile.paste(bcrop, (0, 18))
    tile.paste(crop, (crop.width + 6, 18))
    tile.paste(hcrop, (crop.width * 2 + 12, 18))
    ImageDraw.Draw(tile).text((2, 1), f"{key} F{idx:02d} body | composite | handFront", fill=(230, 200, 120, 255))
    rows.append(tile)
    colors = {}
    for p in pts:
        colors[str(p[2][:3])] = colors.get(str(p[2][:3]), 0) + 1
    top = sorted(colors.items(), key=lambda kv: -kv[1])[:6]
    notes.append({"clip": key, "frame": idx, "handPx": len(pts), "topColors": top})

w = max(t.width for t in rows)
sheet = Image.new("RGBA", (w, sum(t.height for t in rows)), (8, 10, 14, 255))
y = 0
for t in rows:
    sheet.paste(t, (0, y))
    y += t.height
sheet.save(OUT / "grip_untinted.png")
print(json.dumps(notes, indent=2))
