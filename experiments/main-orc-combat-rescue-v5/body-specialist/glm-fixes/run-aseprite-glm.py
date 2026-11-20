# -*- coding: utf-8 -*-
"""Runner Aseprite batch para glm-fixes (perfil separado tmp/aseprite-glm-body-fixes-profile).
Uso: python run-aseprite-glm.py <script.lua> <result.json>
Garante que os subdiretórios de saída dos ciclos existam antes do script rodar.
"""
import os
import subprocess
import json
from pathlib import Path

root = Path.cwd()
profile = root / "tmp" / "aseprite-glm-body-fixes-profile"
profile.mkdir(parents=True, exist_ok=True)

for sub in [
    "characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/back_r-Sword-full/native",
    "characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/back_r-Sword-full/body256",
    "characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/back_l-Axe-full/native",
    "characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/back_l-Axe-full/body256",
    "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes/back_r-Sword-full/native",
    "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes/back_r-Sword-full/body256",
    "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes/back_l-Axe-full/native",
    "experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes/back_l-Axe-full/body256",
]:
    (root / sub).mkdir(parents=True, exist_ok=True)

script = Path(sys.argv[1]) if (sys := __import__("sys")) and len(sys.argv) > 1 else None
result = Path(sys.argv[2]) if len(sys.argv) > 2 else None
assert script and result, "usage: run-aseprite-glm.py <script.lua> <result.json>"

env = os.environ.copy()
env["ASEPRITE_USER_FOLDER"] = str(profile)
cmd = [
    "F:/SteamLibrary/steamapps/common/Aseprite/Aseprite.exe",
    "--batch", "--noinapp", "--script", str(script.resolve()),
]
r = subprocess.run(cmd, env=env, capture_output=True, text=True,
                   creationflags=subprocess.CREATE_NO_WINDOW, timeout=300)
result.write_text(json.dumps({
    "command": cmd,
    "profile": env["ASEPRITE_USER_FOLDER"],
    "script": str(script),
    "exitCode": r.returncode,
    "stdout": r.stdout,
    "stderr": r.stderr,
}, indent=2), encoding="utf-8")
print("exit", r.returncode)
print(r.stdout)
print(r.stderr)
