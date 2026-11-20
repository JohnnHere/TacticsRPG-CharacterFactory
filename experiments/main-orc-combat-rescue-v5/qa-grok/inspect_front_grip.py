import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory")
CLIP = ROOT / "characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword/clip.json"
OUT = ROOT / "experiments/main-orc-combat-rescue-v5/qa-grok/evidence"
OUT.mkdir(parents=True, exist_ok=True)
OLD = ROOT / "characters/orc-v1/source/combat-rescue-v5/combat/front_r/Sword"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path):
    return Image.open(path).convert("RGBA")


clip = json.loads(CLIP.read_text(encoding="utf-8"))
old = json.loads((OLD / "clip.json").read_text(encoding="utf-8"))
report = {
    "clipPath": str(CLIP.relative_to(ROOT)).replace("\\", "/"),
    "clipSha256": sha256(CLIP),
    "frameCount": clip["frameCount"],
    "durationsMs": clip["durationsMs"],
    "oldDurationsMs": old["durationsMs"],
    "timingMatchRejectedV5": clip["durationsMs"] == old["durationsMs"],
    "visibleInterval": clip["visibleInterval"],
    "oldVisibleInterval": old.get("visibleInterval"),
}
stale = []
for field, hfield in (
    ("master", "masterSha256"),
    ("bodyMaster", "bodyMasterSha256"),
    ("handMaster", "handMasterSha256"),
    ("nativeMaster", "nativeMasterSha256"),
    ("strip", "stripSha256"),
    ("compositeStrip", "compositeStripSha256"),
):
    actual = sha256(ROOT / clip[field])
    if actual != clip[hfield]:
        stale.append({"field": field, "declared": clip[hfield], "actual": actual})
report["masterHashMismatches"] = stale
report["bodyMasterMatchesRejectedV5"] = clip["bodyMasterSha256"] == old.get("bodyMasterSha256")
report["nativeMasterMatchesRejectedV5"] = clip["nativeMasterSha256"] == old.get("nativeMasterSha256")

body_mismatch = []
native_mismatch = []
layers = []
for i, fr in enumerate(clip["frames"]):
    body = load(ROOT / fr["layers"]["body"]["png"])
    old_body = load(ROOT / old["frames"][i]["layers"]["body"]["png"])
    if list(body.getdata()) != list(old_body.getdata()):
        body_mismatch.append(i)
    native = load(ROOT / fr["nativePng"])
    crop = body.crop((64, 64, 192, 192))
    if list(native.getdata()) != list(crop.getdata()):
        native_mismatch.append(i)
    hand = load(ROOT / fr["layers"]["handFront"]["png"])
    wf = load(ROOT / fr["layers"]["weaponFront"]["png"])
    wb = load(ROOT / fr["layers"]["weaponBack"]["png"])
    def count(im):
        return sum(1 for p in im.getdata() if p[3])
    declared_files = {
        "png": sha256(ROOT / fr["png"]) == fr["sha256"],
        "body": sha256(ROOT / fr["layers"]["body"]["png"]) == fr["layers"]["body"]["sha256"],
        "hand": sha256(ROOT / fr["layers"]["handFront"]["png"]) == fr["layers"]["handFront"]["sha256"],
        "weaponFront": sha256(ROOT / fr["layers"]["weaponFront"]["png"]) == fr["layers"]["weaponFront"]["sha256"],
        "weaponBack": sha256(ROOT / fr["layers"]["weaponBack"]["png"]) == fr["layers"]["weaponBack"]["sha256"],
        "native": sha256(ROOT / fr["nativePng"]) == fr["nativeSha256"],
    }
    layers.append({
        "frame": i,
        "phase": fr.get("phase"),
        "weaponVisible": fr.get("weaponVisible"),
        "durationMs": fr["durationMs"],
        "handPx": count(hand),
        "weaponFrontPx": count(wf),
        "weaponBackPx": count(wb),
        "hashOk": all(declared_files.values()),
        "hashBad": [k for k, v in declared_files.items() if not v],
        "palm": fr.get("anatomy", {}).get("palm"),
        "wrist": fr.get("anatomy", {}).get("wrist"),
    })
report["bodyMismatchVsRejectedV5"] = body_mismatch
report["nativeNotBodyCrop"] = native_mismatch
report["frames"] = layers

# Zooms of equipped frames: body | composite | hand
tiles = []
for fr in clip["frames"]:
    if not fr.get("weaponVisible") and fr["index"] not in (0, 11, 12):
        continue
    if fr["index"] not in (2, 4, 6, 7, 8, 10, 0, 12):
        continue
    body = load(ROOT / fr["layers"]["body"]["png"])
    hand = load(ROOT / fr["layers"]["handFront"]["png"])
    wf = load(ROOT / fr["layers"]["weaponFront"]["png"])
    wb = load(ROOT / fr["layers"]["weaponBack"]["png"])
    comp = Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(wb, body), wf), hand)
    pts = [(i % hand.width, i // hand.width) for i, p in enumerate(hand.getdata()) if p[3]]
    wpts = [(i % wf.width, i // wf.width) for i, p in enumerate(wf.getdata()) if p[3]]
    wpts += [(i % wb.width, i // wb.width) for i, p in enumerate(wb.getdata()) if p[3]]
    focus = pts or wpts
    if not focus:
        bb = [90, 100, 120, 150]
    else:
        xs = [p[0] for p in focus]
        ys = [p[1] for p in focus]
        bb = [min(xs), min(ys), max(xs), max(ys)]
    x0, y0 = max(0, bb[0] - 28), max(0, bb[1] - 36)
    x1, y1 = min(256, bb[2] + 29), min(256, bb[3] + 29)
    def sc(im):
        c = im.crop((x0, y0, x1, y1))
        return c.resize((c.width * 5, c.height * 5), Image.NEAREST)
    b, c, h = sc(body), sc(comp), sc(hand)
    tile = Image.new("RGBA", (b.width * 3 + 8, b.height + 16), (12, 16, 20, 255))
    tile.paste(b, (0, 16))
    tile.paste(c, (b.width + 4, 16))
    tile.paste(h, (b.width * 2 + 8, 16))
    ImageDraw.Draw(tile).text((2, 1), f"F{fr['index']:02d} {fr.get('phase')} body|comp|hand", fill=(230, 200, 120, 255))
    tiles.append(tile)
w = max(t.width for t in tiles)
sheet = Image.new("RGBA", (w, sum(t.height for t in tiles)), (8, 10, 14, 255))
y = 0
for t in tiles:
    sheet.paste(t, (0, y))
    y += t.height
sheet.save(OUT / "repair1_front_r_sword_grips.png")
(OUT / "repair1_front_r_sword_metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print("clip", report["clipSha256"])
print("stale", stale)
print("bodyMismatch", body_mismatch, "nativeMismatch", native_mismatch)
print("timing", report["timingMatchRejectedV5"])
for row in layers:
    print(row["frame"], row["phase"], "vis", row["weaponVisible"], "hand", row["handPx"], "wf", row["weaponFrontPx"], "wb", row["weaponBackPx"], "hash", row["hashOk"], row["hashBad"])
