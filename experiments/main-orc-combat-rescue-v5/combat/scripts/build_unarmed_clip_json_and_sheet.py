import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

ROOT = Path(".")
OUT_ROOT = ROOT / "characters/orc-v1/source/combat-rescue-v5/combat"
V2_ROOT = ROOT / "characters/orc-v1/source/rear-recovery-v2"
SHEET_PATH = ROOT / "experiments/main-orc-combat-rescue-v5/combat/sheets/unarmed_4views_v5_sheet.png"

def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()

DURATIONS = [80, 110, 50, 90, 120]

# Build contact sheet: 4 rows (front_r, front_l, back_r, back_l), 5 cols (F00..F04), 2x scale (256x256)
cols = 5
rows = 4
cell = 256
sheet = Image.new("RGBA", (cols * cell, rows * cell), (28, 32, 38, 255))
draw = ImageDraw.Draw(sheet)

dirs = ["front_r", "front_l", "back_r", "back_l"]
for r_idx, d in enumerate(dirs):
    clip_dir = OUT_ROOT / d / "Unarmed"
    nat_dir = clip_dir / "native"
    ase_dir = OUT_ROOT / "aseprite" / d
    comp_ase = ase_dir / "unarmed.aseprite"
    nat_ase = ase_dir / "unarmed-native.aseprite"
    strip_png = clip_dir / "native-strip.png"

    frames_meta = []
    for i in range(5):
        f_png = clip_dir / f"{i:02d}.png"
        n_png = nat_dir / f"{i:02d}.png"
        im256 = np.array(Image.open(f_png).convert("RGBA"))
        im128 = np.array(Image.open(n_png).convert("RGBA"))
        # Verify exact crop at [64, 64]
        assert np.array_equal(im256[64:192, 64:192], im128), f"Crop mismatch in {d} F{i:02d}"
        # Verify outside 128x128 is transparent
        mask_out = np.ones((256, 256), dtype=bool)
        mask_out[64:192, 64:192] = False
        assert np.all(im256[mask_out, 3] == 0), f"Non-zero outside native box in {d} F{i:02d}"
        # Verify groundY = 126 in native (190 in composite) and 0 border touches
        vis = im128[:, :, 3] > 0
        ys, xs = np.where(vis)
        assert int(ys.max()) == 126, f"groundY mismatch in {d} F{i:02d}: {ys.max()}"
        assert int(xs.min()) >= 1 and int(xs.max()) <= 126 and int(ys.min()) >= 1, (
            f"Border clip in {d} F{i:02d}: x={xs.min()}..{xs.max()}, y={ys.min()}..{ys.max()}"
        )

        # Draw on sheet
        up = Image.fromarray(im128).resize((cell, cell), Image.NEAREST)
        x0, y0 = i * cell, r_idx * cell
        sheet.alpha_composite(up, (x0, y0))
        draw.rectangle([x0, y0, x0 + cell - 1, y0 + cell - 1], outline=(55, 62, 72, 255), width=1)
        draw.text((x0 + 8, y0 + 8), f"{d}/Unarmed F{i:02d} ({DURATIONS[i]}ms)\nx={xs.min()}..{xs.max()} y={ys.min()}..{ys.max()}", fill=(235, 240, 245, 255))

        frames_meta.append({
            "index": i,
            "durationMs": DURATIONS[i],
            "png": rel(f_png),
            "sha256": sha256_file(f_png),
            "nativePng": rel(n_png),
            "nativeSha256": sha256_file(n_png),
            "weaponVisible": False,
        })

    # Reference parent clip.json for notes/actionId
    parent_clip = json.loads((V2_ROOT / d / "Unarmed" / "clip.json").read_text(encoding="utf-8"))
    if d in ("front_r", "front_l"):
        note = (
            f"V5 Unarmed ({d}): preserved F00/F01/F02/F04 from rear-recovery-v2 and repaired F03 follow-through in Aseprite Lua "
            f"so the punching gauntlet remains clearly visible through recoil/retraction (fixing late fist disappearance) and the "
            f"non-punching guard arm no longer teleports."
        )
    else:
        job_id = "9fdb5943-eeb1-4947-9ce8-b94bd6df7814" if d == "back_r" else "eea7ce3b-bca7-45b4-a6ec-bc17c89a0bea"
        note = (
            f"V5 Unarmed ({d}): genuine whole-body rear brawler punch sequence generated via PixelLab animate_with_skeleton_v3 "
            f"(job {job_id}, 4 active frames + neutral rear base F00) and mastered in Aseprite Lua with counter-balanced off-hand, "
            f"forward punch extension into depth, follow-through retraction, and clean guard recovery."
        )

    clip_obj = {
        "schemaVersion": "orc-complete-clip-v1",
        "characterId": "orc-v1",
        "passId": "main-orc-combat-rescue-v5",
        "direction": d,
        "action": "Unarmed",
        "actionId": parent_clip.get("actionId", "unarmed_attack"),
        "status": "ACTIVE_CANDIDATE",
        "reusedFrom": f"combat-rescue-v5:{d}_Unarmed",
        "master": rel(comp_ase),
        "masterSha256": sha256_file(comp_ase),
        "nativeMaster": rel(nat_ase),
        "nativeMasterSha256": sha256_file(nat_ase),
        "strip": rel(strip_png),
        "stripSha256": sha256_file(strip_png),
        "frameCount": 5,
        "durationsMs": DURATIONS,
        "totalDurationMs": 450,
        "canvas": {
            "composite": [256, 256],
            "native": [128, 128],
            "bodyOffset": [64, 64],
            "groundY": 126,
            "compositeGroundY": 190,
        },
        "weapon": None,
        "frames": frames_meta,
        "notes": note,
    }
    (clip_dir / "clip.json").write_text(json.dumps(clip_obj, indent=2) + "\n", encoding="utf-8")
    print(f"Verified and wrote clip.json for {d}/Unarmed")

sheet.save(SHEET_PATH)
print("Saved sheet:", SHEET_PATH)
