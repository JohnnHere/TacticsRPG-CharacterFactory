from PIL import Image
import os, json, hashlib

ROOT = r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory"
os.chdir(ROOT)
NATIVE_DIR = "characters/orc-v1/source/combat-rescue-v5/localized/frames"
OUT_CLIP = "characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk"
OUT_NATIVE = OUT_CLIP + "/native"
os.makedirs(OUT_CLIP, exist_ok=True)
os.makedirs(OUT_NATIVE, exist_ok=True)

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

frame_infos = []
native_hashes = []
composite_hashes = []
for i in range(8):
    nat = Image.open(f"{NATIVE_DIR}/f{i:02d}.png").convert("RGBA")
    # save native 128
    nat_path = f"{OUT_NATIVE}/{i:02d}.png"
    nat.save(nat_path)
    native_hashes.append(sha(nat_path))
    # composite 256: place native at bodyOffset (64,64)
    comp = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    comp.paste(nat, (64, 64))
    comp_path = f"{OUT_CLIP}/{i:02d}.png"
    comp.save(comp_path)
    composite_hashes.append(sha(comp_path))
    frame_infos.append({
        "index": i,
        "png": f"{OUT_CLIP}/{i:02d}.png",
        "sha256": composite_hashes[-1],
        "nativePng": f"{OUT_NATIVE}/{i:02d}.png",
        "nativeSha256": native_hashes[-1],
        "durationMs": 160,
        "phase": f"stride-step-{i:02d}",
        "weaponVisible": False,
        "groundY": 190,
        "nativeGroundY": 126,
    })

# strip
images = [Image.open(f"{OUT_CLIP}/{i:02d}.png").convert("RGBA") for i in range(8)]
strip = Image.new("RGBA", (256*8, 256), (0,0,0,0))
for i, im in enumerate(images):
    strip.paste(im, (256*i, 0))
strip_path = OUT_CLIP + "/native-strip.png"
strip.save(strip_path)
strip_sha = sha(strip_path)

# clip.json
clip = {
    "schemaVersion": 1,
    "revision": "main-orc-combat-rescue-v5-localized",
    "id": "locomotion.walk-v2-localized",
    "character": "orc-v1",
    "state": "Walk",
    "legacySlotState": "Walk",
    "direction": "back_l",
    "loop": True,
    "oneShot": False,
    "terminal": False,
    "canvas": [256, 256],
    "bodyOffset": [64, 64],
    "groundY": 190,
    "nativeCanvas": [128, 128],
    "nativeGroundY": 126,
    "ppu": 100,
    "frameCount": 8,
    "durationsMs": [160]*8,
    "totalDurationMs": 1280,
    "master": "characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed.aseprite",
    "masterSha256": sha("characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed.aseprite"),
    "nativeMaster": "characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed.aseprite",
    "nativeMasterSha256": sha("characters/orc-v1/source/combat-rescue-v5/localized/walk-back_l-fixed.aseprite"),
    "strip": f"{OUT_CLIP}/native-strip.png",
    "stripSha256": strip_sha,
    "nativeStripSha256": strip_sha,
    "visibilityPolicy": "attack-only-v1",
    "weaponVisible": False,
    "weaponOverlay": False,
    "contactEvent": None,
    "frames": frame_infos,
    "reuseAssessment": "LOCALIZED_CORRECTION",
    "technicalStatus": "TECHNICALLY_COMPLETE",
    "artisticStatus": "VISUAL_REVIEW_REQUIRED",
    "artisticApproval": "PENDING_CREATOR",
    "qualityGatesContract": "config/artistic-quality-gates-v1.json",
    "runtimeImplemented": False,
}

with open(OUT_CLIP + "/clip.json", "w") as f:
    json.dump(clip, f, indent=2)

print("Built fixed back_l/Walk clip in", OUT_CLIP)
print("Native hashes:", native_hashes)
print("Composite hashes:", composite_hashes)
print("Strip sha:", strip_sha)
print("Master sha:", clip["masterSha256"])
