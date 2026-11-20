# -*- coding: utf-8 -*-
"""FIX B — driver PixelLab MCP (chamada real, condicionada apenas a F02).
Passos:
 1) Constrói request inpaint_image_pro_flash a partir do PNG nativo 02.png de repair1
    (base64 vai apenas para ARQUIVO; nunca para o chat).
 2) Chama tools/pixellab-mcp.py --call ... --input ... --output (recibo em arquivo).
 3) Poll get_image(job_id) até terminal, salvando cada poll em arquivo.
 4) Extrai o PNG resultado dos blocos base64 do recibo final -> pixellab-f02-edit1.png.
 5) Imprime SOMENTE resumo textual (status, cobrado, dimensões); nenhum base64 no chat.
Prompt SEM palavras de arma/equipamento (nem negativas): somente anatomia/pose/mãos vazias.
"""
import base64
import json
import subprocess
import time
from pathlib import Path
from PIL import Image

ROOT = Path.cwd()
G = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes"
SRC_PNG = ROOT / "characters/orc-v1/source/combat-rescue-v5/body-specialist/final-cycles/repair1/back_l-Axe-full/native/02.png"
PY = str(ROOT / "tmp/pixel-venv/Scripts/python.exe")
MCP = str(ROOT / "tools/pixellab-mcp.py")

DESCRIPTION = (
    "Bulky green orc warrior seen from the back-left, bald green skull, black iron armor, "
    "large round pauldron on the right shoulder, grey chainmail skirt, red-brown leather "
    "tassets and boots. Right arm in mid-lift: shoulder flexed, elbow bent close to the "
    "torso, forearm rising diagonally, closed leather gauntlet fist beside the head at "
    "cheek height, hand completely empty and bare. Completely bare, clean neck, trapezius "
    "and shoulder line, unobstructed silhouette. Same individual, same armor materials, "
    "same palette, same lighting, same scale; keep the left arm, torso, legs, boots and "
    "the transparent background exactly as they are."
)

MASK = {"mask_x": 68, "mask_y": 8, "mask_width": 33, "mask_height": 26}
SEED = 20261029

def call(tool, req_path, out_path):
    r = subprocess.run([PY, MCP, "--call", tool, "--input", str(req_path), "--output", str(out_path)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("CALL FAILED", tool, r.returncode)
        print(r.stdout)
        print(r.stderr)
        raise SystemExit(1)
    return json.loads(Path(out_path).read_text(encoding="utf-8"))

# 1) request
b64 = base64.b64encode(SRC_PNG.read_bytes()).decode("ascii")
req = {"description": DESCRIPTION, "image_base64": b64, "seed": SEED}
req.update(MASK)
req_path = G / "pixellab-inpaint-f02-request.json"
req_path.write_text(json.dumps(req), encoding="utf-8")
print("request built (base64 em arquivo):", req_path.name, "| png bytes:", len(b64) * 3 // 4)

# 2) chamada
receipt = call("inpaint_image_pro_flash", req_path, G / "pixellab-inpaint-f02-receipt.json")
sc = receipt.get("structuredContent") or {}
job_id = sc.get("job_id")
if not job_id:
    for blk in receipt.get("content", []):
        t = blk.get("text", "")
        for line in t.splitlines():
            if line.startswith("id:"):
                job_id = line.split(":", 1)[1].strip()
print("job_id:", job_id, "| isError:", receipt.get("isError"))
if receipt.get("isError"):
    print(json.dumps(sc, indent=2)[:2000])
    raise SystemExit(1)

# 3) poll
poll_path_req = G / "pixellab-inpaint-f02-poll-req.json"
poll_path_req.write_text(json.dumps({"job_id": job_id}), encoding="utf-8")
status, poll = None, None
for attempt in range(1, 25):
    time.sleep(10)
    poll = call("get_image", poll_path_req, G / ("pixellab-inpaint-f02-poll-%02d.json" % attempt))
    psc = poll.get("structuredContent") or {}
    status = psc.get("status")
    print("poll %02d: %s" % (attempt, status))
    if status in ("completed", "failed", "error"):
        break
if status != "completed":
    print("JOB NOT COMPLETED:", status)
    raise SystemExit(1)

# 4) extrair resultado (base64 -> arquivo)
saved = []
for idx, blk in enumerate(poll.get("content", [])):
    if blk.get("type") == "image" and blk.get("data"):
        out = G / ("pixellab-f02-edit1.png" if idx == 0 else ("pixellab-f02-edit1-%d.png" % idx))
        out.write_bytes(base64.b64decode(blk["data"]))
        saved.append(out.name)
psc = poll.get("structuredContent") or {}
print("saved:", saved, "| charged_generations:", psc.get("charged_generations"),
      "| download:", str(psc.get("download_url"))[:80])
for name in saved:
    im = Image.open(G / name)
    print(name, "size:", im.size, "mode:", im.mode)
