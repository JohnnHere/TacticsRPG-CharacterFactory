import json
from pathlib import Path
from PIL import Image

ROOT = Path(r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory")
proof = ROOT / "experiments/main-orc-combat-rescue-v5/qa-grok/aseprite-proof"
meta = json.loads((proof / "back_r_sword_native.json").read_text(encoding="utf-8"))
sheet = Image.open(proof / "back_r_sword_native_sheet.png").convert("RGBA")
print("sheet", sheet.size, "frames", len(meta.get("frames", [])))
frames = meta["frames"]
if isinstance(frames, dict):
    items = list(frames.values())
else:
    items = frames
mism = []
for i, fr in enumerate(items):
    box = fr["frame"]
    crop = sheet.crop((box["x"], box["y"], box["x"] + box["w"], box["y"] + box["h"]))
    native = Image.open(ROOT / f"characters/orc-v1/source/combat-rescue-v5/combat/back_r/Sword/native/{i:02d}.png").convert("RGBA")
    if crop.size != native.size or list(crop.getdata()) != list(native.getdata()):
        mism.append(i)
print("mismatched frames", mism, "of", len(items))
print("durations", [fr.get("duration") for fr in items])
