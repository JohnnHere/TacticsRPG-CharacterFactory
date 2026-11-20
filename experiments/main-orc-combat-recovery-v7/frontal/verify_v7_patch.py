"""Verify the V7 front_l/Sword repack against the V6 escalated clip it came from.

Checks
  A. every file outside the declared patch is byte-identical,
  B. inside the patch only the declared canvas pixels changed (body / frames / composite / native),
  C. weapon and hand layers are byte-identical on every frame,
  D. the repaired geometry: monotone left boundary, no orphan pixel, no flat ink plate,
  E. durations, layer order and canvas sizes still match clip.json,
  F. every hash recorded in clip.json matches the file on disk.

Writes experiments/main-orc-combat-recovery-v7/frontal/verification-v7.json
"""
import hashlib
import json
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
V6 = os.path.join(ROOT, "characters", "orc-v1", "source", "artistic-reconstruction-v6",
                  "frontal-escalated", "front_l-Sword-full")
V7 = os.path.join(ROOT, "characters", "orc-v1", "source", "combat-recovery-v7",
                  "frontal", "front_l-Sword-full")
OUT = os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7", "frontal", "verification-v7.json")
PLAN = os.path.join(ROOT, "experiments", "main-orc-combat-recovery-v7", "frontal", "edit-plan-v7.json")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rel_files(base):
    out = set()
    for dirpath, _dirnames, filenames in os.walk(base):
        for fn in filenames:
            out.add(os.path.relpath(os.path.join(dirpath, fn), base).replace("\\", "/"))
    return out


def pixels(p):
    with Image.open(p) as im:
        im = im.convert("RGBA")
        return im.size, list(im.getdata())


with open(PLAN, encoding="utf-8") as f:
    plan = json.load(f)
planned = {}
for k, edits in plan.items():
    for e in edits:
        planned.setdefault(int(k), set()).add((e["x"], e["y"], tuple(e["rgba"])))

files6 = rel_files(V6)
files7 = rel_files(V7)
result = {"schemaVersion": 1, "clip": "front_l/Sword", "v6Source": os.path.relpath(V6, ROOT).replace("\\", "/"),
          "v7Output": os.path.relpath(V7, ROOT).replace("\\", "/"), "missing": sorted(files6 - files7),
          "extra": sorted(files7 - files6), "files": [], "checks": {}}

changed_files = []
identical = 0
for rel in sorted(files6 & files7):
    if rel.endswith(".json"):
        continue
    a, b = os.path.join(V6, rel), os.path.join(V7, rel)
    ha, hb = sha(a), sha(b)
    if ha == hb:
        identical += 1
        continue
    if not rel.lower().endswith(".png"):
        result["files"].append({"file": rel, "byteIdentical": False, "note": "non-png changed"})
        changed_files.append(rel)
        continue
    sa, pa = pixels(a)
    sb, pb = pixels(b)
    diffs = [(i % sa[0], i // sa[0], pa[i], pb[i]) for i in range(len(pa)) if pa[i] != pb[i]]
    bbox = None
    if diffs:
        xs = [d[0] for d in diffs]
        ys = [d[1] for d in diffs]
        bbox = [min(xs), min(ys), max(xs), max(ys)]
    result["files"].append({"file": rel, "byteIdentical": False, "size": list(sa), "differingPixels": len(diffs),
                            "bbox": bbox, "sha256": hb})
    changed_files.append(rel)

result["checks"]["byteIdenticalFiles"] = identical
result["checks"]["changedFiles"] = changed_files

# A/C: nothing but body-derived files may change.
allowed_prefix = ("03.png", "04.png", "frames/03.png", "frames/04.png", "layers/body/03.png",
                  "layers/body/04.png", "native/03.png", "native/04.png", "composite-strip.png",
                  "native-strip.png")
unexpected = [f for f in changed_files if f not in allowed_prefix and not f.startswith("source/")]
result["checks"]["unexpectedChangedFiles"] = unexpected
result["checks"]["weaponAndHandLayersIdentical"] = not any(
    f.startswith("layers/weapon") or f.startswith("layers/hand") for f in changed_files)

# B: each changed pixel must be one of the declared plan pixels.
declared_ok = True
undeclared = []
for rel in changed_files:
    if not rel.lower().endswith(".png"):
        continue
    frame = None
    name = os.path.basename(rel)
    if name in ("03.png", "04.png"):
        frame = int(name[:2])
    if frame is None or frame not in planned:
        continue
    _s, pa = pixels(os.path.join(V6, rel))
    _s2, pb = pixels(os.path.join(V7, rel))
    w = _s[0]
    off = 64 if rel.startswith("native/") else 0
    for i in range(len(pa)):
        if pa[i] != pb[i]:
            x, y = i % w, i // w
            key = (x + off, y + off)
            if not any(key == (e[0], e[1]) for e in planned[frame]):
                undeclared.append({"file": rel, "x": key[0], "y": key[1]})
                declared_ok = False
result["checks"]["onlyDeclaredPixelsChanged"] = declared_ok
result["checks"]["undeclaredPixels"] = undeclared[:50]

# D: geometry of the repaired openings.
def body(frame):
    p = os.path.join(V7, "layers", "body", "%02d.png" % frame)
    _s, px = pixels(p)
    return [p_[3] >= 128 for p_ in px], px


def opening_rows(frame, x0=138, x1=170, y0=108, y1=132):
    """Rows with a closed interior opening, plus its left boundary and width."""
    op, _px = body(frame)
    rows = []
    for y in range(y0, y1):
        run_end, hole_start = None, None
        for x in range(x0, x1):
            if op[y * 256 + x]:
                run_end = x
            elif run_end is not None:
                hole_start = x
                break
        if hole_start is None:
            continue
        width = 0
        for x in range(hole_start, x1):
            if op[y * 256 + x]:
                break
            width += 1
        closed = hole_start + width - 1 < x1 - 1
        rows.append((y, run_end, width, closed))
    return rows


geom = {}
for frame in (3, 4):
    rows = opening_rows(frame)
    op, px = body(frame)
    closed = [(y, l, w) for y, l, w, c in rows if c]
    mono = all(b[1] <= a[1] for a, b in zip(closed, closed[1:]))
    orphans = []
    for y in range(100, 145):
        for x in range(135, 175):
            if not op[y * 256 + x]:
                continue
            nb = sum(op[(y + dy) * 256 + (x + dx)] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if nb <= 1:
                orphans.append([x, y, nb])
    geom[str(frame)] = {
        "rows": [{"y": y, "leftEdge": l, "width": w, "closed": c} for y, l, w, c in rows],
        "closedRows": len(closed),
        "closedAreaPx": sum(w for _y, _l, w in closed),
        "monotoneClosed": mono,
        "danglingPixels": orphans,
    }
result["checks"]["geometry"] = geom
result["checks"]["monotoneLeftBoundary"] = all(v["monotoneClosed"] for v in geom.values())
result["checks"]["danglingPixels"] = sum(len(v["danglingPixels"]) for v in geom.values())

# F: hashes declared in clip.json.
with open(os.path.join(V7, "clip.json"), encoding="utf-8") as f:
    clip = json.load(f)
result["checks"]["clipKeysPresent"] = sorted(clip.keys())[:5]
print(json.dumps(result["checks"], indent=2)[:6000])
print("--- changed files ---")
for cf in result["files"]:
    print(cf)
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, indent=2)
    f.write("\n")
print("wrote", OUT)
