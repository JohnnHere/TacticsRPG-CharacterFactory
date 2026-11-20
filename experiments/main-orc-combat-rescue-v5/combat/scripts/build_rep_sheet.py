from PIL import Image, ImageDraw
from pathlib import Path
import json

ROOT = Path(".")
EXP_DIR = ROOT / "experiments/main-orc-combat-rescue-v5/combat"
RAW_DIR = EXP_DIR / "raw/back_r_sword_v1"
SHEET_DIR = EXP_DIR / "sheets"

base_f00 = Image.open(EXP_DIR / "raw/back_r_base_128.png").convert("RGBA")
frames = [base_f00] + [Image.open(RAW_DIR / f"{i:02d}.png").convert("RGBA") for i in range(7)]

# Build 2x zoom sheet of all 8 frames (F00 base + 00..06 generated)
sheet = Image.new("RGBA", (8 * 256 + 16, 300), (24, 28, 34, 255))
draw = ImageDraw.Draw(sheet)

for idx, im in enumerate(frames):
    x0 = 8 + idx * 256
    y0 = 32
    draw.rectangle([x0, y0, x0 + 255, y0 + 255], fill=(42, 46, 54, 255), outline=(90, 98, 110, 255))
    # ground line y=126 -> y0 + 126*2 = y0 + 252
    draw.line([(x0, y0 + 252), (x0 + 255, y0 + 252)], fill=(180, 80, 80, 180), width=1)
    z = im.resize((256, 256), Image.NEAREST)
    sheet.alpha_composite(z, (x0, y0))
    lbl = "F00 (Base)" if idx == 0 else f"F0{idx} (raw {idx-1:02d})"
    draw.text((x0 + 6, 8), lbl, fill=(235, 240, 245, 255))

sheet_path = SHEET_DIR / "rep_back_r_sword_v1_sheet.png"
sheet.save(sheet_path)
print("Saved sheet:", sheet_path)

# Write milestone checkpoint.json
checkpoint = {
    "stage": "representative_wholebody_sequence_ready",
    "status": "IN_PROGRESS",
    "representativeJob": {
        "clip": "back_r/Sword",
        "jobId": "06c2d829-7b45-4d6f-b64e-ce7db44ffac1",
        "assetId": "3db3ade5-9cad-53a0-94cc-e228871f38b0",
        "tool": "animate_with_skeleton_v3",
        "generationsCharged": 3,
        "requestPath": "experiments/main-orc-combat-rescue-v5/combat/requests/req_back_r_sword_v1.json",
        "receiptPath": "experiments/main-orc-combat-rescue-v5/combat/receipts/poll_back_r_sword_v1_res.json",
        "rawFramesDir": "experiments/main-orc-combat-rescue-v5/combat/raw/back_r_sword_v1",
        "contactSheet": "experiments/main-orc-combat-rescue-v5/combat/sheets/rep_back_r_sword_v1_sheet.png"
    },
    "balanceBaseline": 1403.70,
    "generationsUsedByThisTaskSoFar": 3
}
(EXP_DIR / "checkpoint.json").write_text(json.dumps(checkpoint, indent=2), encoding="utf-8")
(ROOT / "characters/orc-v1/source/combat-rescue-v5/combat/checkpoint.json").write_text(json.dumps(checkpoint, indent=2), encoding="utf-8")
print("Wrote checkpoint.json")
