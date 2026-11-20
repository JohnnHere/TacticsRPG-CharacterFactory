"""Independent QA diagnostics for main-orc-combat-rescue-v5. Read-only on production art."""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(r"C:\Users\João Orlando\Documents\Projetos Unity\TacticsRPG-CharacterFactory")
OUT = ROOT / "experiments" / "main-orc-combat-rescue-v5" / "qa-grok" / "evidence"
OUT.mkdir(parents=True, exist_ok=True)
MANIFEST = json.loads((ROOT / "characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json").read_text(encoding="utf-8"))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(rel):
    return Image.open(ROOT / rel).convert("RGBA")


def diff_count(a, b):
    pa, pb = a.getdata(), b.getdata()
    return sum(1 for x, y in zip(pa, pb) if x != y)


def opaque(im):
    return [(i % im.width, i // im.width, p) for i, p in enumerate(im.getdata()) if p[3]]


def bbox(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return [min(xs), min(ys), max(xs), max(ys)] if xs else None


def components(im):
    w, h = im.size
    pix = im.load()
    seen = [[False] * h for _ in range(w)]
    comps = []
    for y in range(h):
        for x in range(w):
            if seen[x][y] or pix[x, y][3] == 0:
                continue
            stack = [(x, y)]
            seen[x][y] = True
            cells = []
            while stack:
                cx, cy = stack.pop()
                cells.append((cx, cy))
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if 0 <= nx < w and 0 <= ny < h and not seen[nx][ny] and pix[nx, ny][3]:
                        seen[nx][ny] = True
                        stack.append((nx, ny))
            comps.append(cells)
    comps.sort(key=len, reverse=True)
    return comps


def min_dist(a_pts, b_set):
    if not a_pts or not b_set:
        return None
    best = 10**9
    for x, y in a_pts:
        for dx in range(-12, 13):
            for dy in range(-12, 13):
                if (x + dx, y + dy) in b_set:
                    best = min(best, max(abs(dx), abs(dy)) if False else (dx * dx + dy * dy) ** 0.5)
                    if best == 0:
                        return 0
        if best == 0:
            return 0
    # fallback exact if not found in 12px window
    if best > 20:
        # sample
        step = max(1, len(a_pts) // 80)
        for x, y in a_pts[::step]:
            for bx, by in list(b_set)[:: max(1, len(b_set) // 400)]:
                d = ((x - bx) ** 2 + (y - by) ** 2) ** 0.5
                if d < best:
                    best = d
    return round(best, 2)


def scale(im, n):
    return im.resize((im.width * n, im.height * n), Image.NEAREST)


def label_row(frames, scale_n, title):
    cell_w = frames[0].width * scale_n
    cell_h = frames[0].height * scale_n
    sheet = Image.new("RGBA", (cell_w * len(frames), cell_h + 16), (20, 28, 32, 255))
    draw = ImageDraw.Draw(sheet)
    draw.text((4, 1), title, fill=(226, 195, 140, 255))
    for i, fr in enumerate(frames):
        sheet.paste(scale(fr, scale_n), (i * cell_w, 16))
        draw.text((i * cell_w + 2, 16), f"F{i:02d}", fill=(255, 220, 80, 255))
    return sheet


def stack(rows):
    w = max(r.width for r in rows)
    h = sum(r.height for r in rows)
    out = Image.new("RGBA", (w, h), (12, 18, 22, 255))
    y = 0
    for r in rows:
        out.paste(r, (0, y))
        y += r.height
    return out


def frozen_view(frame, base):
    out = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    fp, bp = frame.load(), base.load()
    op = out.load()
    same = changed = 0
    for y in range(frame.height):
        for x in range(frame.width):
            a, b = fp[x, y], bp[x, y]
            if a[3] == 0 and b[3] == 0:
                continue
            if a == b and a[3]:
                op[x, y] = (180, 40, 160, 255)  # frozen vs F00
                same += 1
            elif a[3]:
                op[x, y] = a
                changed += 1
            else:
                op[x, y] = (40, 180, 255, 255)  # erased vs F00
    return out, same, changed


report = {"manifestSha256": sha256(ROOT / "characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json")}

# Preservation recheck
pres = json.loads((ROOT / "experiments/main-orc-combat-rescue-v5/input-preservation.json").read_text(encoding="utf-8"))
bad = []
for rel, digest in pres["files"].items():
    path = ROOT / rel
    if not path.exists() or sha256(path) != digest:
        bad.append(rel)
        if len(bad) > 8:
            break
report["preservation"] = {"declared": len(pres["files"]), "mismatchesSampled": bad, "fullPass": not bad}

cells = {f"{c['direction']}/{c['action']}": c for c in MANIFEST["cells"]}
report["matrix"] = {
    "clips": MANIFEST["totalClips"],
    "frames": MANIFEST["totalFrames"],
    "candidates": MANIFEST["activeCandidatesCount"],
    "aliases": MANIFEST["unchangedAliasesCount"],
    "eligibleForIntegration": MANIFEST.get("eligibleForIntegration"),
    "technicalStatus": MANIFEST.get("technicalStatus"),
    "artisticStatus": MANIFEST.get("artisticStatus"),
}

# Alias path/hash vs parent
parent = json.loads((ROOT / MANIFEST["parentManifest"]).read_text(encoding="utf-8"))
parent_cells = {f"{c['direction']}/{c['action']}": c for c in parent["cells"]}
alias_bad = []
for key, cell in cells.items():
    if cell["status"] == "UNCHANGED_ALIAS":
        p = parent_cells[key]
        same_path = cell["clipJson"] == p.get("clipJson")
        same_hash = sha256(ROOT / cell["clipJson"]) == sha256(ROOT / p["clipJson"]) if same_path else False
        if not same_path or not same_hash:
            alias_bad.append({"cell": key, "samePath": same_path, "sameHash": same_hash})
report["aliasPathHashMismatch"] = alias_bad

# Front sword/axe body+timing preservation
front_preserve = {}
for key in ["front_r/Sword", "front_l/Sword", "front_r/Axe", "front_l/Axe"]:
    clip = json.loads((ROOT / cells[key]["clipJson"]).read_text(encoding="utf-8"))
    pclip = json.loads((ROOT / parent_cells[key]["clipJson"]).read_text(encoding="utf-8"))
    body_mismatch = []
    timing_same = [f["durationMs"] for f in clip["frames"]] == [f["durationMs"] for f in pclip["frames"]]
    for i, (fr, pfr) in enumerate(zip(clip["frames"], pclip["frames"])):
        b = sha256(ROOT / fr["layers"]["body"]["png"])
        pb = sha256(ROOT / pfr["layers"]["body"]["png"])
        if b != pb:
            body_mismatch.append(i)
    front_preserve[key] = {
        "timingSame": timing_same,
        "bodyFrameMismatches": body_mismatch,
        "visibleInterval": clip.get("visibleInterval"),
        "parentVisibleInterval": pclip.get("visibleInterval"),
    }
report["frontBodyTiming"] = front_preserve

# Rear weapon inspection
rear_keys = ["back_r/Sword", "back_r/Axe", "back_l/Sword", "back_l/Axe"]
rear_rows = []
frozen_rows = []
rear_metrics = {}
for key in rear_keys:
    direction, action = key.split("/")
    clip = json.loads((ROOT / cells[key]["clipJson"]).read_text(encoding="utf-8"))
    natives = [load(f"characters/orc-v1/source/combat-rescue-v5/combat/{direction}/{action}/native/{i:02d}.png") for i in range(8)]
    bodies = [load(fr["layers"]["body"]["png"]) for fr in clip["frames"]]
    hands = [load(fr["layers"]["handFront"]["png"]) for fr in clip["frames"]]
    wfront = [load(fr["layers"]["weaponFront"]["png"]) for fr in clip["frames"]]
    wback = [load(fr["layers"]["weaponBack"]["png"]) for fr in clip["frames"]]
    base = natives[0]
    diffs_vs_f00 = [diff_count(n, base) for n in natives]
    sword_or_axe_pair = None
    comps = []
    small = []
    halo = []
    seam = []
    frozen_same = []
    torso_changed = []
    views = []
    for i, im in enumerate(natives):
        frozen, same, changed = frozen_view(im, base)
        views.append(frozen)
        frozen_same.append(same)
        cs = components(im)
        comps.append([len(c) for c in cs[:6]])
        small.append([{"n": len(c), "bbox": bbox(c)} for c in cs[1:] if len(c) >= 3])
        pix = im.load()
        halo_n = 0
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = pix[x, y]
                if a and r > 190 and g > 190 and b > 185:
                    halo_n += 1
        halo.append(halo_n)
        # seam at paste boundary
        jumps = 0
        boundary = []
        for y in range(10, 85):
            if direction == "back_r":
                x_b = 45 if y < 50 else (43 if y <= 62 else 42)
            else:
                x_b = 81 if y < 50 else (83 if y <= 62 else 84)
            left, right = pix[x_b, y], pix[x_b + 1, y]
            if left[3] and right[3]:
                delta = abs(left[0] - right[0]) + abs(left[1] - right[1]) + abs(left[2] - right[2])
                if delta > 80:
                    jumps += 1
                    if len(boundary) < 6:
                        boundary.append({"y": y, "x": x_b, "left": left[:3], "right": right[:3], "delta": delta})
        seam.append({"hardJumps": jumps, "samples": boundary})
        # torso core motion, avoiding pasted column
        tchanged = 0
        topaque = 0
        bp = base.load()
        x0, x1 = (50, 88) if direction == "back_r" else (40, 80)
        for y in range(32, 82):
            for x in range(x0, x1):
                if pix[x, y][3] or bp[x, y][3]:
                    topaque += 1
                    if pix[x, y] != bp[x, y]:
                        tchanged += 1
        torso_changed.append(tchanged)
    # weapon outside interval and hand counts
    vis = clip["visibleInterval"]
    outside = []
    grips = []
    for i, fr in enumerate(clip["frames"]):
        ho = opaque(hands[i])
        wo = opaque(wfront[i]) + opaque(wback[i])
        bo = opaque(bodies[i])
        outside.append({
            "frame": i,
            "weaponVisible": fr.get("weaponVisible"),
            "weaponPx": len(wo),
            "handPx": len(ho),
            "inInterval": vis[0] <= i <= vis[1],
        })
        if fr.get("weaponVisible"):
            hset = {(p[0], p[1]) for p in ho}
            bset = {(p[0], p[1]) for p in bo}
            wset = {(p[0], p[1]) for p in wo}
            # touch within 1px
            def touches(src, dst):
                for x, y in src:
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            if (x + dx, y + dy) in dst:
                                return True
                return False
            grips.append({
                "frame": i,
                "handPx": len(ho),
                "handBBox": bbox([(p[0], p[1]) for p in ho]),
                "handTouchesBody": touches(hset, bset) if hset and bset else False,
                "handTouchesWeapon": touches(hset, wset) if hset and wset else False,
                "weaponTouchesBody": touches(wset, bset) if wset and bset else False,
                "grip": fr.get("rightGrip") or fr.get("leftGrip"),
                "phase": fr.get("phase"),
            })
    f07_eq_f00 = diff_count(natives[7], natives[0]) == 0
    rear_metrics[key] = {
        "diffVsF00": diffs_vs_f00,
        "f07EqualsF00": f07_eq_f00,
        "components": comps,
        "extraComponents": small,
        "brightPixels": halo,
        "seamHardJumps": seam,
        "torsoCoreChanged": torso_changed,
        "frozenOpaqueVsF00": frozen_same,
        "layers": outside,
        "grips": grips,
        "durationsMs": clip["durationsMs"],
        "visibleInterval": vis,
    }
    rear_rows.append(label_row(natives, 2, f"{key} layers-off native"))
    frozen_rows.append(label_row(views, 2, f"{key} magenta=identical to F00"))

# sword vs axe diffs
for direction in ("back_r", "back_l"):
    diffs = []
    for i in range(8):
        a = load(f"characters/orc-v1/source/combat-rescue-v5/combat/{direction}/Sword/native/{i:02d}.png")
        b = load(f"characters/orc-v1/source/combat-rescue-v5/combat/{direction}/Axe/native/{i:02d}.png")
        diffs.append(diff_count(a, b))
    rear_metrics[f"{direction}/Sword_vs_Axe"] = diffs

report["rear"] = rear_metrics
stack(rear_rows).save(OUT / "rear_bodies_layers_off.png")
stack(frozen_rows).save(OUT / "rear_frozen_vs_f00.png")

# Unarmed
unarmed_rows = []
unarmed = {}
for direction in ("front_r", "front_l", "back_r", "back_l"):
    key = f"{direction}/Unarmed"
    clip = json.loads((ROOT / cells[key]["clipJson"]).read_text(encoding="utf-8"))
    natives = [load(f"characters/orc-v1/source/combat-rescue-v5/combat/{direction}/Unarmed/native/{i:02d}.png") for i in range(clip["frameCount"])]
    pclip = json.loads((ROOT / parent_cells[key]["clipJson"]).read_text(encoding="utf-8"))
    parent_diffs = []
    for i, fr in enumerate(clip["frames"]):
        # parent may use different layout; compare native if present else body crop
        pfr = pclip["frames"][i]
        ppath = pfr.get("png")
        parent_im = load(ppath)
        cur = load(fr["png"])
        if parent_im.size != cur.size:
            parent_diffs.append({"frame": i, "size": [list(cur.size), list(parent_im.size)]})
        else:
            parent_diffs.append({"frame": i, "diff": diff_count(cur, parent_im)})
    cs = [len(components(im)) for im in natives]
    unarmed[key] = {
        "durations": clip["durationsMs"],
        "parentTiming": pclip["durationsMs"],
        "diffVsParentCompositeOrPng": parent_diffs,
        "componentCounts": cs,
        "f07orLastEqualsF00": diff_count(natives[-1], natives[0]) == 0,
        "diffVsF00": [diff_count(im, natives[0]) for im in natives],
    }
    unarmed_rows.append(label_row(natives, 2, f"{key} native"))
report["unarmed"] = unarmed
stack(unarmed_rows).save(OUT / "unarmed_native.png")

# Grip zooms for visible frames: body+weapon and hand tint
grip_tiles = []
for key in ["front_r/Sword", "front_r/Axe", "front_l/Sword", "front_l/Axe", "back_r/Sword", "back_r/Axe", "back_l/Sword", "back_l/Axe"]:
    clip = json.loads((ROOT / cells[key]["clipJson"]).read_text(encoding="utf-8"))
    shown = 0
    for fr in clip["frames"]:
        if not fr.get("weaponVisible"):
            continue
        if shown >= 3:
            break
        # pick first, middle, last visible
        shown += 1
    vis_frames = [fr for fr in clip["frames"] if fr.get("weaponVisible")]
    picks = []
    if vis_frames:
        picks = [vis_frames[0], vis_frames[len(vis_frames) // 2], vis_frames[-1]]
    for fr in picks:
        body = load(fr["layers"]["body"]["png"])
        hand = load(fr["layers"]["handFront"]["png"])
        wf = load(fr["layers"]["weaponFront"]["png"])
        wb = load(fr["layers"]["weaponBack"]["png"])
        ho = opaque(hand)
        if not ho:
            continue
        bb = bbox([(p[0], p[1]) for p in ho])
        x0 = max(0, bb[0] - 18)
        y0 = max(0, bb[1] - 28)
        x1 = min(body.width, bb[2] + 19)
        y1 = min(body.height, bb[3] + 19)
        crop_b = body.crop((x0, y0, x1, y1))
        crop_w = Image.alpha_composite(wb, wf).crop((x0, y0, x1, y1))
        crop_h = hand.crop((x0, y0, x1, y1))
        comp = Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(wb, body), wf), hand).crop((x0, y0, x1, y1))
        # tint hand magenta on composite for separation
        tint = comp.copy()
        tp, hp = tint.load(), crop_h.load()
        for y in range(tint.height):
            for x in range(tint.width):
                if hp[x, y][3]:
                    tp[x, y] = (255, 40, 180, 255)
        tile = Image.new("RGBA", ((x1 - x0) * 4 * 2 + 8, (y1 - y0) * 4 + 18), (16, 22, 26, 255))
        tile.paste(scale(comp, 4), (0, 18))
        tile.paste(scale(tint, 4), ((x1 - x0) * 4 + 8, 18))
        ImageDraw.Draw(tile).text((2, 1), f"{key} F{fr['index']:02d} {fr.get('phase','')}", fill=(226, 195, 140, 255))
        grip_tiles.append(tile)
if grip_tiles:
    # grid 4 columns
    cols = 4
    tw = max(t.width for t in grip_tiles)
    th = max(t.height for t in grip_tiles)
    rows_n = (len(grip_tiles) + cols - 1) // cols
    grid = Image.new("RGBA", (cols * tw, rows_n * th), (8, 12, 16, 255))
    for i, t in enumerate(grip_tiles):
        grid.paste(t, ((i % cols) * tw, (i // cols) * th))
    grid.save(OUT / "grip_zooms.png")
report["gripTileCount"] = len(grip_tiles)

# Walk back_l color copy visualization
walk_cell = cells["back_l/Walk"]
walk_clip = json.loads((ROOT / walk_cell["clipJson"]).read_text(encoding="utf-8"))
pwalk = json.loads((ROOT / parent_cells["back_l/Walk"]["clipJson"]).read_text(encoding="utf-8"))
walk_rows = []
walk_stats = []
for i in range(8):
    cur = load(walk_clip["frames"][i]["png"])
    old = load(pwalk["frames"][i]["png"])
    # native if present
    native_rel = f"characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/native/{i:02d}.png"
    native = load(native_rel)
    pn = None
    # parent native guess
    pnative_rel = str(Path(pwalk["frames"][i]["png"]).parent / "native" / f"{i:02d}.png")
    if (ROOT / pnative_rel).exists():
        pn = load(pnative_rel)
    changed = 0
    vis = native.copy()
    if pn and pn.size == native.size:
        vp, np_, op = vis.load(), native.load(), pn.load()
        for y in range(native.height):
            for x in range(native.width):
                if np_[x, y] != op[x, y]:
                    changed += 1
                    if np_[x, y][3]:
                        vp[x, y] = (255, 40, 40, 255)
        # also show whether copied color equals F(i-4) at same coord
    copied_from_wrong = None
    if i >= 4 and pn and pn.size == native.size:
        src = load(f"characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/native/{i-4:02d}.png")
        match_src = mismatch_src = 0
        sp, np_, op = src.load(), native.load(), pn.load()
        for y in range(native.height):
            for x in range(native.width):
                if np_[x, y] != op[x, y]:
                    if np_[x, y] == sp[x, y]:
                        match_src += 1
                    else:
                        mismatch_src += 1
        copied_from_wrong = {"matchesEarlierHalf": match_src, "notEqualEarlierHalf": mismatch_src}
    walk_stats.append({
        "frame": i,
        "compositeDiffVsParent": diff_count(cur, old) if cur.size == old.size else "size",
        "nativeChangedVsParent": changed,
        "copyCheck": copied_from_wrong,
        "duration": walk_clip["frames"][i]["durationMs"],
    })
    walk_rows.append(scale(vis, 3))
# pair F00-F03 over F04-F07 highlighted
if walk_rows:
    top = stack([label_row([load(f"characters/orc-v1/source/combat-rescue-v5/localized/back_l/Walk/native/{i:02d}.png") for i in range(8)], 2, "back_l/Walk native fixed")])
    bot = label_row(walk_rows, 1, "red = color changed vs parent native")
    # walk_rows already 3x; label_row will scale again. Save directly.
    sheet = Image.new("RGBA", (max(top.width, 8 * walk_rows[0].width), top.height + walk_rows[0].height + 16), (12, 18, 22, 255))
    sheet.paste(top, (0, 0))
    d = ImageDraw.Draw(sheet)
    d.text((4, top.height), "red marks pixels changed vs parent", fill=(255, 180, 80, 255))
    for i, fr in enumerate(walk_rows):
        sheet.paste(fr, (i * fr.width, top.height + 16))
    sheet.save(OUT / "walk_back_l.png")
report["walkBackL"] = walk_stats

# Other walks: bright outlier scan, no edit expected
walk_keep = {}
for key in ["front_r/Walk", "front_l/Walk", "back_r/Walk"]:
    clip = json.loads((ROOT / cells[key]["clipJson"]).read_text(encoding="utf-8"))
    bright = []
    for i, fr in enumerate(clip["frames"]):
        im = load(fr["png"])
        n = 0
        for p in im.getdata():
            if p[3] and p[0] > 200 and p[1] > 200 and p[2] > 190:
                n += 1
        bright.append(n)
    walk_keep[key] = {"frames": clip["frameCount"], "brightPixelsPerFrame": bright, "alias": cells[key]["status"]}
report["walkKeepBright"] = walk_keep

# Defeat fronts
defeat = {}
defeat_frames = []
for key in ["front_r/Defeat", "front_l/Defeat"]:
    clip = json.loads((ROOT / cells[key]["clipJson"]).read_text(encoding="utf-8"))
    frames = [load(fr["png"]) for fr in clip["frames"]]
    # crop lower body-ish: use native if available
    natives = []
    for i in range(len(frames)):
        nrel = str(Path(clip["frames"][i]["png"]).parent / "native" / f"{i:02d}.png")
        natives.append(load(nrel) if (ROOT / nrel).exists() else frames[i])
    defeat[key] = {
        "status": cells[key]["status"],
        "durations": clip["durationsMs"],
        "aliasOfParent": cells[key]["clipJson"] == parent_cells[key]["clipJson"],
        "sizes": [list(im.size) for im in natives],
    }
    defeat_frames.append(label_row(natives, 2, f"{key}"))
    # hand zoom: upper-middle of last three frames
report["defeat"] = defeat
if defeat_frames:
    stack(defeat_frames).save(OUT / "defeat_front.png")

# Attack-only outside weapon clips: empty weapon layers already in rear metrics.
# Confirm Idle/Hit/rear Defeat are aliases and Unarmed has no weapon files with pixels.
attack_only = {}
for key, cell in cells.items():
    if cell["action"] in ("Sword", "Axe"):
        continue
    clip = json.loads((ROOT / cell["clipJson"]).read_text(encoding="utf-8"))
    weaponish = 0
    for fr in clip["frames"]:
        layers = fr.get("layers") or {}
        for name in ("weaponBack", "weaponFront", "handFront"):
            if name in layers:
                im = load(layers[name]["png"])
                weaponish += sum(1 for p in im.getdata() if p[3])
    attack_only[key] = {"weaponOrHandPixels": weaponish, "status": cell["status"]}
report["nonAttackWeaponPixels"] = attack_only

# Weapon sprite identity vs parent definition if present
weapon_note = {}
for name in ("Sword", "Axe"):
    wpath = ROOT / f"characters/orc-v1/source/combat-rescue-v5/combat/weapons/{name}"
    files = {p.name: sha256(p) for p in wpath.glob("*") if p.is_file()}
    weapon_note[name] = files
report["weaponFiles"] = weapon_note

(OUT / "metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print("wrote", OUT / "metrics.json")
print("preservation mismatches", len(bad), "of", len(pres["files"]))
print("alias mismatches", alias_bad)
print("front body", {k: v["bodyFrameMismatches"] for k, v in front_preserve.items()})
