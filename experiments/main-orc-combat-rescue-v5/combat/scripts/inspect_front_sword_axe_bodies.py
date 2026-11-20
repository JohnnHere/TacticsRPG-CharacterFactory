from PIL import Image, ImageDraw
from pathlib import Path
import json

ROOT = Path(".")
EXP_DIR = ROOT / "experiments/main-orc-combat-rescue-v5/combat"
SHEET_DIR = EXP_DIR / "sheets"

BASELINE = json.loads((ROOT / "experiments/main-orc-combat-rescue-v5/combat/stage-a-baseline-inspection.json").read_text(encoding="utf-8"))

for act in ["Sword", "Axe"]:
    cdir = (ROOT / BASELINE[f"front_r/{act}"]["clipJson"]).parent
    p = cdir / "layers/body"
    frames = sorted(p.glob("*.png"))
    sheet = Image.new("RGBA", (len(frames) * 192 + 16, 224), (24, 28, 34, 255))
    draw = ImageDraw.Draw(sheet)
    for i, fp in enumerate(frames):
        im = Image.open(fp).convert("RGBA")
        crop = im.crop((64, 64, 192, 192)).resize((192, 192), Image.NEAREST)
        x0 = 8 + i * 192
        draw.rectangle([x0, 24, x0 + 191, 215], fill=(40, 44, 52, 255), outline=(80, 88, 100, 255))
        sheet.alpha_composite(crop, (x0, 24))
        draw.text((x0 + 6, 6), f"{act} B{i:02d}", fill=(240, 240, 240, 255))
    out = SHEET_DIR / f"front_r_{act.lower()}_bodies.png"
    sheet.save(out)
    print("Saved:", out)
