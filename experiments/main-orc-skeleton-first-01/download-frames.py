"""Downloads every generated frame with the same MCP credential the client already uses.

The tool only inlines the first few images, so the rest come from the download
endpoint named in the job response. Credentials stay in the Codex config; nothing
is printed.
"""
import json
import os
import sys
import tomllib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXP = Path(__file__).resolve().parent
JOB = "ead91ded-b485-4197-89c6-79bccda527ea"
FRAMES = 14

config = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "config.toml"
settings = tomllib.loads(config.read_text(encoding="utf-8"))["mcp_servers"]["pixellab"]
headers = dict(settings.get("http_headers", {}))
if settings.get("bearer_token_env_var"):
    headers["Authorization"] = "Bearer " + os.environ[settings["bearer_token_env_var"]]

out = EXP / "pixellab-frames"
out.mkdir(exist_ok=True)

saved = []
for index in range(FRAMES):
    url = f"https://api.pixellab.ai/mcp/images/{JOB}/download?index={index}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=180) as response:
        body = response.read()
        kind = response.headers.get("Content-Type", "")
    if not body.startswith(b"\x89PNG"):
        print(f"index {index}: resposta não é PNG ({kind}, {len(body)} bytes)", file=sys.stderr)
        continue
    path = out / f"{index:02d}.png"
    path.write_bytes(body)
    saved.append((index, len(body)))

print(json.dumps({"job": JOB, "saved": len(saved), "frames": [{"index": i, "bytes": b} for i, b in saved]}, indent=1))
