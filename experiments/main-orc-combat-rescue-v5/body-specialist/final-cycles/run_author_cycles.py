import os, subprocess, json
from pathlib import Path

root = Path.cwd()
p = root / 'experiments/main-orc-combat-rescue-v5/body-specialist/final-cycles'
profile = root / 'tmp/aseprite-final-body-flash-profile'
profile.mkdir(parents=True, exist_ok=True)

env = os.environ.copy()
env['ASEPRITE_USER_FOLDER'] = str(profile)

lua_script = p / 'author-all-cycles.lua'

cmd = [
    'F:/SteamLibrary/steamapps/common/Aseprite/Aseprite.exe',
    '--batch',
    '--noinapp',
    '--script',
    str(lua_script)
]

print("Running command:", cmd)
r = subprocess.run(
    cmd,
    env=env,
    cwd=str(root),
    capture_output=True,
    text=True,
    creationflags=subprocess.CREATE_NO_WINDOW,
    timeout=180
)

result = {
    'command': cmd,
    'profile': str(profile),
    'exitCode': r.returncode,
    'stdout': r.stdout,
    'stderr': r.stderr
}

(p / 'aseprite-run-result.json').write_text(json.dumps(result, indent=2))
print("Exit code:", r.returncode)
print("Stdout:", r.stdout)
print("Stderr:", r.stderr)
