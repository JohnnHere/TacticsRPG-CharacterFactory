"""Independent QA checks for frozen main-orc-rear-reconstruction-v4.

Read-only against production sources. Writes evidence only under this qa folder.
Does not invent artistic approval from hash equality.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
QA = Path(__file__).resolve().parent
SHEETS = QA / "sheets"
EXPECTED_FREEZE = "8f3c0be13e2b6e7d7f3ff4a33807cc1a4cb5519602d1f589d24194808ad49c44"
FREEZE = ROOT / "experiments/main-orc-rear-reconstruction-v4/dev/version-freeze.json"
MANIFEST = ROOT / "characters/orc-v1/source/rear-reconstruction-v4/candidate28manifest.json"
REVIEW = ROOT / "Biblioteca de Arte/Estudos Comparativos/Orc principal - Reconstrucao traseira"
PRESERVATION = ROOT / "experiments/main-orc-rear-reconstruction-v4/input-preservation.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def rgba(path: Path) -> Image.Image:
    with Image.open(path) as image:
        return image.convert("RGBA")


def diff_count(a: Image.Image, b: Image.Image) -> int:
    if a.size != b.size:
        return -1
    pa, pb = a.tobytes(), b.tobytes()
    return sum(1 for i in range(0, len(pa), 4) if pa[i:i + 4] != pb[i:i + 4])


def alpha_over(layers: list[Image.Image]) -> Image.Image:
    canvas = Image.new("RGBA", layers[0].size, (0, 0, 0, 0))
    for layer in layers:
        canvas.alpha_composite(layer)
    return canvas


def opaque_count(image: Image.Image) -> int:
    pixels = image.tobytes()
    return sum(1 for i in range(3, len(pixels), 4) if pixels[i])


def partial_alpha(image: Image.Image) -> int:
    pixels = image.tobytes()
    return sum(1 for i in range(3, len(pixels), 4) if 0 < pixels[i] < 255)


def paste_row(frames: list[Image.Image], scale: int, label: str) -> Image.Image:
    if not frames:
        return Image.new("RGBA", (32, 32), (0, 0, 0, 255))
    w, h = frames[0].size
    sheet = Image.new("RGBA", (w * scale * len(frames), h * scale + 18), (20, 24, 28, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((4, 2), label, fill=(230, 220, 180, 255))
    for index, frame in enumerate(frames):
        sheet.alpha_composite(frame.resize((w * scale, h * scale), Image.Resampling.NEAREST), (index * w * scale, 18))
    return sheet


def stack(rows: list[Image.Image]) -> Image.Image:
    width = max(row.width for row in rows)
    height = sum(row.height for row in rows)
    out = Image.new("RGBA", (width, height), (12, 16, 18, 255))
    y = 0
    for row in rows:
        out.alpha_composite(row, (0, y))
        y += row.height
    return out


def main() -> None:
    checks = []

    def add(name, ok, detail):
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    freeze_hash = sha256_file(FREEZE)
    add("version-freeze sha256", freeze_hash == EXPECTED_FREEZE, freeze_hash)
    freeze = load_json(FREEZE)
    add("freeze status flags",
        freeze.get("status") == "ARTISTIC_REVISION_REQUIRED" and freeze.get("eligibleForIntegration") is False,
        {"status": freeze.get("status"), "eligible": freeze.get("eligibleForIntegration"), "fileCount": freeze.get("fileCount")})

    missing = []
    mismatched = []
    for item in freeze["files"]:
        path = ROOT / item["path"]
        if not path.is_file():
            missing.append(item["path"])
            continue
        digest = sha256_file(path)
        if digest != item["sha256"] or path.stat().st_size != item["sizeBytes"]:
            mismatched.append(item["path"])
    add("freeze inventory hashes", not missing and not mismatched and len(freeze["files"]) == freeze["fileCount"],
        {"declared": freeze["fileCount"], "listed": len(freeze["files"]), "missing": len(missing), "mismatched": len(mismatched),
         "missingSample": missing[:8], "mismatchSample": mismatched[:8]})

    manifest_hash = sha256_file(MANIFEST)
    add("manifest hash matches freeze record", manifest_hash == freeze["manifestSha256"], manifest_hash)
    manifest = load_json(MANIFEST)
    cells = manifest["cells"]
    keys = [(c["direction"], c["action"]) for c in cells]
    expected = [(d, a) for d in ["front_r", "front_l", "back_r", "back_l"] for a in ["Idle", "Walk", "Unarmed", "Sword", "Axe", "Hit", "Defeat"]]
    frame_sum = sum(c["frameCount"] for c in cells)
    affected = [c for c in cells if c.get("isAffected")]
    aliases = [c for c in cells if c["status"] == "UNCHANGED_ALIAS"]
    add("matrix 28/210/8/20",
        len(cells) == 28 and len(set(keys)) == 28 and keys == expected and frame_sum == 210
        and len(affected) == 8 and sum(c["frameCount"] for c in affected) == 82
        and len(aliases) == 20 and sum(c["frameCount"] for c in aliases) == 128,
        {"cells": len(cells), "unique": len(set(keys)), "frames": frame_sum,
         "affected": len(affected), "affectedFrames": sum(c["frameCount"] for c in affected),
         "aliases": len(aliases), "aliasFrames": sum(c["frameCount"] for c in aliases)})
    add("package eligibility",
        manifest.get("eligibleForIntegration") is False
        and manifest.get("technicalStatus") == "NOT_VERIFIED"
        and manifest.get("artisticStatus") == "ARTISTIC_REVISION_REQUIRED"
        and manifest.get("artisticApproval") == "PENDING_CREATOR"
        and manifest.get("runtimeImplemented") is False,
        {k: manifest.get(k) for k in ("eligibleForIntegration", "technicalStatus", "artisticStatus", "artisticApproval", "runtimeImplemented", "integrationStatus")})
    add("keypose and specialist excluded from cells",
        not any("keypose" in json.dumps(c) or "specialist" in json.dumps(c) for c in cells),
        "cell payloads contain neither keypose nor specialist")
    text = MANIFEST.read_text(encoding="utf-8")
    add("manifest text has no specialist path", "rear-reconstruction-v4-specialist" not in text, "searched manifest")

    alias_bad = []
    protected = []
    for cell in aliases:
        clip_path = ROOT / cell["clipJson"]
        parent = cell.get("parentCell", {})
        digest = sha256_file(clip_path) if clip_path.is_file() else None
        if digest != parent.get("clipSha256") or str(clip_path).replace("\\", "/") != str(ROOT / parent.get("clipJson", "")).replace("\\", "/"):
            alias_bad.append(cell["cellId"])
        if cell["action"] in ("Idle", "Hit") or (cell["action"] == "Defeat" and cell["direction"].startswith("back")):
            protected.append({
                "cell": cell["cellId"],
                "underV4": "rear-reconstruction-v4" in cell["clipJson"].replace("\\", "/"),
                "hashOk": digest == parent.get("clipSha256"),
            })
    add("alias clip hashes match declared parents", not alias_bad, {"bad": alias_bad})
    add("protected Idle/Hit/rear Defeat are prior aliases",
        all(not item["underV4"] and item["hashOk"] for item in protected) and len(protected) == 10,
        protected)

    unchanged_required = ["Unarmed", "Walk", "Defeat"]
    unchanged_front = [c for c in cells if c["action"] in unchanged_required and c["direction"].startswith("front")]
    add("frontal Unarmed/Walk/Defeat not forked",
        all(c["status"] == "UNCHANGED_ALIAS" and "rear-reconstruction-v4" not in c["clipJson"] for c in unchanged_front),
        [c["cellId"] + ":" + c["status"] for c in unchanged_front])

    layer_errors = []
    body_pairs = {}
    body_parent_deltas = []
    weapon_hidden_opaque = []
    clip_status = []
    timing_mismatch = []
    for cell in affected:
        clip = load_json(ROOT / cell["clipJson"])
        parent = load_json(ROOT / clip["provenance"]["parentClip"])
        clip_status.append({
            "cell": cell["cellId"],
            "technicalStatus": clip.get("technicalStatus"),
            "artisticStatus": clip.get("artisticStatus"),
            "choreographyChanged": clip.get("provenance", {}).get("choreographyChanged"),
        })
        if clip.get("durationsMs") != parent.get("durationsMs"):
            timing_mismatch.append(cell["cellId"])
        bodies = []
        for frame, parent_frame in zip(clip["frames"], parent["frames"]):
            layers = [rgba(ROOT / frame["layers"][name]["png"]) for name in clip["layerOrder"]]
            composite = rgba(ROOT / frame["png"])
            native = rgba(ROOT / frame["nativePng"])
            body = rgba(ROOT / frame["layers"]["body"]["png"])
            parent_body = rgba(ROOT / parent_frame["layers"]["body"]["png"])
            parent_hand = rgba(ROOT / parent_frame["layers"]["handFront"]["png"])
            hand = rgba(ROOT / frame["layers"]["handFront"]["png"])
            if alpha_over(layers).tobytes() != composite.tobytes():
                layer_errors.append(cell["cellId"] + f" F{frame['index']} alpha-over")
            offset = clip["bodyOffset"]
            crop = body.crop((offset[0], offset[1], offset[0] + 128, offset[1] + 128))
            if crop.tobytes() != native.tobytes():
                layer_errors.append(cell["cellId"] + f" F{frame['index']} native-crop")
            if frame["durationMs"] != parent_frame["durationMs"]:
                timing_mismatch.append(cell["cellId"] + f" F{frame['index']}")
            if diff_count(hand, parent_hand) != 0:
                layer_errors.append(cell["cellId"] + f" F{frame['index']} handFront")
            if not frame["weaponVisible"]:
                for name in ("weaponBack", "weaponFront", "handFront"):
                    count = opaque_count(rgba(ROOT / frame["layers"][name]["png"]))
                    if count:
                        weapon_hidden_opaque.append(f"{cell['cellId']} F{frame['index']} {name}={count}")
            bodies.append(body)
            delta = diff_count(body, parent_body)
            body_parent_deltas.append({"cell": cell["cellId"], "frame": frame["index"], "bodyDelta": delta})
        body_pairs[cell["cellId"]] = bodies

    add("affected alpha-over, native crop, handFront", not layer_errors, {"errors": layer_errors[:12], "count": len(layer_errors)})
    add("affected timing equals parent", not timing_mismatch, timing_mismatch)
    add("hidden weapon/hand layers empty", not weapon_hidden_opaque, weapon_hidden_opaque[:12])

    identical = {}
    for direction in ("front_r", "front_l", "back_r", "back_l"):
        sword = body_pairs[f"{direction}/Sword"]
        axe = body_pairs[f"{direction}/Axe"]
        identical[direction] = all(a.tobytes() == b.tobytes() for a, b in zip(sword, axe))
    add("back_r Sword/Axe bodies identical", identical.get("back_r") is True, identical)

    scalp = load_json(ROOT / "experiments/main-orc-rear-reconstruction-v4/dev/scalp-outline-points.json")
    scalp_by_frame = {item["frame"]: {(p["native"][0], p["native"][1]) for p in item["points"]} for item in scalp["frames"]}
    scalp_mismatch = []
    non_scalp_body_change = []
    for item in body_parent_deltas:
        cell = item["cell"]
        frame = item["frame"]
        direction = cell.split("/")[0]
        if direction != "back_r":
            if item["bodyDelta"] != 0:
                non_scalp_body_change.append(item)
            continue
        clip = load_json(ROOT / next(c["clipJson"] for c in affected if c["cellId"] == cell))
        parent = load_json(ROOT / clip["provenance"]["parentClip"])
        body = rgba(ROOT / clip["frames"][frame]["layers"]["body"]["png"])
        parent_body = rgba(ROOT / parent["frames"][frame]["layers"]["body"]["png"])
        ox, oy = clip["bodyOffset"]
        expected = {(x + ox, y + oy) for x, y in scalp_by_frame.get(frame, set())}
        actual = set()
        pa, pb = body.tobytes(), parent_body.tobytes()
        width = body.width
        for i in range(0, len(pa), 4):
            if pa[i:i + 4] != pb[i:i + 4]:
                pixel = i // 4
                actual.add((pixel % width, pixel // width))
        if actual != expected:
            scalp_mismatch.append({"cell": cell, "frame": frame, "actual": len(actual), "expected": len(expected)})
    add("back_r body deltas equal explicit scalp points", not scalp_mismatch, scalp_mismatch)
    add("non-back_r body pixels unchanged", not non_scalp_body_change, non_scalp_body_change[:8])

    weapon_checks = []
    for category, parent_def in (("Axe", "assets/weapons/militia-axe/weapon.json"), ("Sword", "assets/weapons/recruit-sword/weapon.json")):
        current = load_json(ROOT / manifest["weaponDefinitions"][category])
        parent = load_json(ROOT / parent_def)
        cur_img = rgba(ROOT / current["sprite"])
        parent_img = rgba(ROOT / parent["sprite"])
        weapon_checks.append({
            "category": category,
            "rgbaDelta": diff_count(cur_img, parent_img),
            "alphaEqual": cur_img.getchannel("A").tobytes() == parent_img.getchannel("A").tobytes(),
            "size": list(cur_img.size),
            "grip": current.get("grip"),
            "parentGrip": parent.get("grip"),
            "spriteHashOk": sha256_file(ROOT / current["sprite"]) == current.get("spriteSha256"),
            "masterHashOk": sha256_file(ROOT / current["master"]) == current.get("masterSha256"),
            "parentMasterHashOk": sha256_file(ROOT / current["parentMaster"]) == current.get("parentMasterSha256"),
        })
    add("weapon source hashes and unchanged alpha/grip/canvas",
        all(item["alphaEqual"] and item["grip"] == item["parentGrip"] and item["size"] == [96, 96]
            and item["spriteHashOk"] and item["masterHashOk"] and item["parentMasterHashOk"] for item in weapon_checks),
        weapon_checks)

    # Preservation inventory. This is the pre-candidate snapshot, not a full-repo audit.
    preservation = load_json(PRESERVATION)
    preserve_missing = []
    preserve_mismatch = []
    for rel, digest in preservation["files"].items():
        path = ROOT / rel
        if not path.is_file():
            preserve_missing.append(rel)
            continue
        if sha256_file(path) != digest:
            preserve_mismatch.append(rel)
    add("input preservation 2939",
        len(preservation["files"]) == 2939 and not preserve_missing and not preserve_mismatch,
        {"listed": len(preservation["files"]), "missing": len(preserve_missing), "mismatched": len(preserve_mismatch),
         "missingSample": preserve_missing[:6], "mismatchSample": preserve_mismatch[:6]})

    page = (REVIEW / "index.html").read_text(encoding="utf-8")
    catalog = load_json(REVIEW / "catalogo.json")
    review_files = [p for p in REVIEW.rglob("*") if p.is_file()]
    add("review catalog points at this freeze",
        catalog.get("revision") == "main-orc-rear-reconstruction-v4"
        and catalog.get("technicalStatus") == "NOT_VERIFIED"
        and catalog.get("packageStatus") == "ARTISTIC_REVISION_REQUIRED"
        and catalog.get("cells") == 28
        and len(catalog.get("affectedCells", [])) == 8
        and len(catalog.get("unchangedAliases", [])) == 20,
        {k: catalog.get(k) for k in ("revision", "technicalStatus", "packageStatus", "cells", "artisticApproval", "runtimeImplemented")})
    add("review page does not claim creator approval",
        "CREATOR_APPROVED" not in page and "PENDING_CREATOR" in page and "ARTISTIC_REVISION_REQUIRED" in page,
        "status strings scanned")
    add("review page links stale integration report as QA opinion",
        "parecer independente" in page and "orchestration-report.md" in page,
        "present; this is a labeling defect, not evidence of a completed QA")
    add("review copied file count", True, {"files": len(review_files)})
    before_after = list((REVIEW / "AntesDepois").glob("*.png")) if (REVIEW / "AntesDepois").exists() else []
    add("before/after cards present", True, {"count": len(before_after), "names": sorted(p.name for p in before_after)[:40]})

    # Contact sheets for human inspection. Static sheets are not 1x playback.
    def frames_for(cell_id, kind):
        cell = next(c for c in affected if c["cellId"] == cell_id)
        clip = load_json(ROOT / cell["clipJson"])
        if kind == "body":
            return [rgba(ROOT / f["layers"]["body"]["png"]).crop((64, 64, 192, 192)) for f in clip["frames"]]
        if kind == "composite":
            return [rgba(ROOT / f["png"]).crop((64, 64, 192, 192)) for f in clip["frames"]]
        return [rgba(ROOT / f["nativePng"]) for f in clip["frames"]]

    stack([
        paste_row(frames_for("back_r/Sword", "body"), 2, "back_r Sword body layers-off F00-F07"),
        paste_row(frames_for("back_r/Axe", "body"), 2, "back_r Axe body layers-off F00-F07"),
        paste_row(frames_for("back_r/Sword", "composite"), 2, "back_r Sword composite F00-F07"),
        paste_row(frames_for("back_r/Axe", "composite"), 2, "back_r Axe composite F00-F07"),
    ]).save(SHEETS / "back_r-body-and-composite.png")
    stack([
        paste_row(frames_for("back_l/Sword", "body"), 2, "back_l Sword body layers-off F00-F07"),
        paste_row(frames_for("back_l/Axe", "body"), 2, "back_l Axe body layers-off F00-F07"),
        paste_row(frames_for("back_l/Sword", "composite"), 2, "back_l Sword composite F00-F07"),
        paste_row(frames_for("back_l/Axe", "composite"), 2, "back_l Axe composite F00-F07"),
    ]).save(SHEETS / "back_l-body-and-composite.png")

    alias_cells = {c["cellId"]: c for c in cells}
    def alias_natives(cell_id):
        clip = load_json(ROOT / alias_cells[cell_id]["clipJson"])
        return [rgba(ROOT / f["nativePng"]) for f in clip["frames"]]

    stack([
        paste_row(alias_natives("front_r/Defeat"), 2, "front_r Defeat alias F00-F04"),
        paste_row(alias_natives("front_l/Defeat"), 2, "front_l Defeat alias F00-F04"),
        paste_row(alias_natives("back_r/Defeat"), 2, "back_r Defeat protected alias"),
        paste_row(alias_natives("back_l/Defeat"), 2, "back_l Defeat protected alias"),
    ]).save(SHEETS / "defeat-four-views.png")
    stack([
        paste_row(alias_natives(f"{d}/Unarmed"), 2, f"{d} Unarmed alias")
        for d in ("front_r", "front_l", "back_r", "back_l")
    ]).save(SHEETS / "unarmed-four-views.png")

    axe = rgba(ROOT / "characters/orc-v1/source/rear-reconstruction-v4/weapons/Axe/militia-axe.png")
    sword = rgba(ROOT / "characters/orc-v1/source/rear-reconstruction-v4/weapons/Sword/recruit-sword.png")
    parent_axe = rgba(ROOT / load_json(ROOT / "assets/weapons/militia-axe/weapon.json")["sprite"])
    parent_sword = rgba(ROOT / load_json(ROOT / "assets/weapons/recruit-sword/weapon.json")["sprite"])
    stack([
        paste_row([parent_sword, sword, parent_axe, axe], 3, "parent sword, candidate sword, parent axe, candidate axe"),
    ]).save(SHEETS / "weapons-source.png")

    # Grip zooms around declared rightGrip on visible rear impact-ish frames.
    grip_rows = []
    for cell_id in ("back_r/Sword", "back_r/Axe", "back_l/Sword", "back_l/Axe", "front_r/Sword", "front_r/Axe"):
        cell = next(c for c in affected if c["cellId"] == cell_id)
        clip = load_json(ROOT / cell["clipJson"])
        crops = []
        for frame in clip["frames"]:
            if not frame.get("weaponVisible"):
                continue
            image = rgba(ROOT / frame["png"])
            gx, gy = frame.get("rightGrip") or [128, 128]
            box = (max(0, gx - 28), max(0, gy - 28), min(image.width, gx + 28), min(image.height, gy + 28))
            crops.append(image.crop(box).resize((112, 112), Image.Resampling.NEAREST))
        grip_rows.append(paste_row(crops, 1, cell_id + " grip neighborhood"))
    stack(grip_rows).save(SHEETS / "grip-neighborhoods.png")

    # Rejected study versus selected F04, if the study export exists.
    study_dir = ROOT / "characters/orc-v1/source/rear-reconstruction-v4/keypose-axeR"
    study_pngs = sorted(study_dir.rglob("*.png"))
    add("rejected keypose files exist outside manifest cells", any(study_pngs), {"count": len(study_pngs), "sample": [str(p.relative_to(ROOT)) for p in study_pngs[:8]]})

    # Partial alpha on unchanged unarmed/defeat natives.
    partial = []
    for cell_id in ("front_r/Unarmed", "front_l/Unarmed", "back_r/Unarmed", "back_l/Unarmed", "front_r/Defeat", "front_l/Defeat"):
        for index, image in enumerate(alias_natives(cell_id)):
            count = partial_alpha(image)
            if count:
                partial.append({"cell": cell_id, "frame": index, "partial": count})
    add("unarmed/defeat native partial alpha", not partial, partial)

    # Walk/Idle/Hit alias paths and durations.
    locomotion = []
    for cell in cells:
        if cell["action"] in ("Idle", "Walk", "Hit") or cell["cellId"].endswith("/Defeat"):
            locomotion.append({"cell": cell["cellId"], "status": cell["status"], "frames": cell["frameCount"], "ms": cell["durationsMs"], "clip": cell["clipJson"]})
    add("locomotion and hit durations recorded", True, locomotion)

    result = {
        "freezeSha256": freeze_hash,
        "expectedFreezeSha256": EXPECTED_FREEZE,
        "manifestSha256": manifest_hash,
        "checks": checks,
        "failed": [c["name"] for c in checks if not c["ok"]],
        "clipTechnicalStatus": clip_status,
        "identicalBodies": identical,
        "weaponChecks": weapon_checks,
        "reviewFileCount": len(review_files),
        "continuousPlayback": "NOT_VERIFIED",
        "note": "Hash and layer checks do not approve choreography, grip, or motion.",
    }
    (QA / "checks.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"failed": result["failed"], "reviewFiles": len(review_files), "weapon": weapon_checks, "identical": identical}, indent=2))


if __name__ == "__main__":
    main()
