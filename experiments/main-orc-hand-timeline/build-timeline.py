"""Builds the hand timeline across every historical back_l Sword version.

For each era: pick the contact frame, crop around the hand (handFront layer bbox
expanded), magnify at 8x, and compose a labeled timeline sheet. Also saves each
full contact frame so the creator can open any era directly.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

ERAS = [
    ("complete-v1 (baseline original)", "characters/orc-v1/source/complete-v1/back_l/Sword/Attack/clip.json", "crossing"),
    ("rear-recovery-v2", "characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack/clip.json", "crossing"),
    ("v5 resgate", "characters/orc-v1/source/combat-rescue-v5/combat/back_l/Sword/clip.json", "slash-contact"),
    ("v5 final-cycles", "characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/back_l-Sword-full/clip.json", "contact"),
    ("v6 reconstrucao artistica", "characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-sword/clip.json", "impact"),
    ("v7 recuperacao", "characters/orc-v1/source/combat-recovery-v7/rear-alt/back_l-sword/clip.json", "contact"),
    ("v8 rear", "characters/orc-v1/source/combat-recovery-v8/rear/back_l-sword/clip.json", "contact"),
    ("v8 rear-arc (atual)", "characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/clip.json", "contact"),
]
FALLBACKS = ["contact", "heavy-impact", "slash-contact", "impact", "crossing", "drive"]

SCALE = 8
CROP = 44  # half-width of the hand crop in canvas px

rows = []
for label, rel, phase in ERAS:
    clip = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    frames = clip["frames"]
    frame = next((f for f in frames if f.get("phase") == phase), None)
    if frame is None:
        for candidate in FALLBACKS:
            frame = next((f for f in frames if f.get("phase") == candidate), None)
            if frame:
                break
    if frame is None:
        armed = [f for f in frames if f.get("weaponVisible")]
        frame = armed[len(armed) // 2] if armed else frames[len(frames) // 2]

    def frame_image(f):
        for key in ("png", "compositePng", "nativePng"):
            value = f.get(key)
            if value is None:
                continue
            if isinstance(value, dict):
                value = value.get("png") or value.get("path")
            if value:
                return ROOT / value
        raise KeyError("nenhum campo de imagem no quadro")

    image = Image.open(frame_image(frame)).convert("RGBA")

    hand_layer = frame.get("layers", {}).get("handFront")
    if hand_layer:
        h = Image.open(ROOT / hand_layer["png"]).convert("RGBA")
        bbox = h.getbbox()
        if bbox:
            cx, cy = (bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2
        else:
            cx, cy = 178, 131
    else:
        cx, cy = 170, 130
    x0, y0 = max(0, cx - CROP), max(0, cy - CROP)
    x1, y1 = min(256, cx + CROP), min(256, cy + CROP)
    crop = image.crop((x0, y0, x1, y1)).resize(((x1 - x0) * SCALE, (y1 - y0) * SCALE), Image.NEAREST)

    rows.append((label, f"F{frame['index']:02d} · {frame.get('phase', '?')}", crop, rel, frame["index"]))

cw = max(r[2].width for r in rows)
ch = max(r[2].height for r in rows)
PAD, LABEL_H = 14, 34
sheet = Image.new("RGBA", (cw * 4 + PAD * 5, (ch + LABEL_H + PAD) * 2 + PAD), (18, 18, 22, 255))
draw = ImageDraw.Draw(sheet)
for i, (label, sub, crop, rel, index) in enumerate(rows):
    col, row = i % 4, i // 4
    x = PAD + col * (cw + PAD)
    y = PAD + row * (ch + LABEL_H + PAD)
    sheet.alpha_composite(crop, (x, y + LABEL_H))
    draw.text((x + 2, y + 2), label, fill=(232, 233, 238))
    draw.text((x + 2, y + 18), sub, fill=(150, 200, 150))
sheet.save(OUT / "hand-timeline.png")

manifest = []
for label, sub, crop, rel, index in rows:
    clip = json.loads((ROOT / rel).read_text(encoding="utf-8"))
    frame = clip["frames"][index]
    base = (ROOT / rel).parent
    full = base / "frames" / f"{index:02d}.png"
    if not full.exists():
        full = base / f"{index:02d}.png"
    if not full.exists():
        for key in ("png", "compositePng", "nativePng"):
            value = frame.get(key)
            if isinstance(value, dict):
                value = value.get("png") or value.get("path")
            if value:
                full = ROOT / value
                break
    manifest.append({"era": label, "contactFrame": str(index), "clip": rel, "fullFrame": str(full)})
(OUT / "timeline-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"hand-timeline.png ({sheet.width}x{sheet.height}) com {len(rows)} eras")
for m in manifest:
    print(f"  {m['era']}: F{m['contactFrame']} -> {m['fullFrame']}")
