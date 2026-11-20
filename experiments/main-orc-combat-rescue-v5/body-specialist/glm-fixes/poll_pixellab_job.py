# -*- coding: utf-8 -*-
"""Retomada de poll do job PixelLab FIX B (executar em background com redirect).
Lê o job_id do recibo, continua pollando (get_image) a partir de poll-03, salva
recibos em arquivo e, ao completar, extrai o PNG (base64->arquivo) e imprime
resumo textual. Nunca imprime base64.
"""
import base64
import json
import subprocess
import time
from pathlib import Path
from PIL import Image

ROOT = Path.cwd()
G = ROOT / "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes"
PY = str(ROOT / "tmp/pixel-venv/Scripts/python.exe")
MCP = str(ROOT / "tools/pixellab-mcp.py")

receipt = json.loads((G / "pixellab-inpaint-f02-receipt.json").read_text(encoding="utf-8"))
job_id = (receipt.get("structuredContent") or {}).get("job_id")
print("resuming job:", job_id)

req_path = G / "pixellab-inpaint-f02-poll-req.json"
req_path.write_text(json.dumps({"job_id": job_id}), encoding="utf-8")

status, poll = None, None
for attempt in range(3, 30):
    out = G / ("pixellab-inpaint-f02-poll-%02d.json" % attempt)
    r = subprocess.run([PY, MCP, "--call", "get_image", "--input", str(req_path), "--output", str(out)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("poll call failed", r.returncode, r.stderr[:200])
    else:
        try:
            poll = json.loads(out.read_text(encoding="utf-8"))
            status = (poll.get("structuredContent") or {}).get("status")
        except Exception as e:
            print("poll parse error", e)
    print("poll %02d: %s" % (attempt, status), flush=True)
    if status in ("completed", "failed", "error"):
        break
    time.sleep(10)

if status != "completed" or poll is None:
    print("JOB NOT COMPLETED:", status)
    raise SystemExit(1)

saved = []
for idx, blk in enumerate(poll.get("content", [])):
    if blk.get("type") == "image" and blk.get("data"):
        name = "pixellab-f02-edit1.png" if not saved else "pixellab-f02-edit1-%d.png" % idx
        (G / name).write_bytes(base64.b64decode(blk["data"]))
        saved.append(name)
psc = poll.get("structuredContent") or {}
print("saved:", saved)
print("charged_generations:", psc.get("charged_generations"))
print("asset:", (psc.get("asset") or {}).get("id"))
for name in saved:
    im = Image.open(G / name)
    print(name, "size:", im.size, "mode:", im.mode)
print("DONE")
