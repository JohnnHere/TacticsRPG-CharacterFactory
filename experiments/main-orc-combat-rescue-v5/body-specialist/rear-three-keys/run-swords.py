import os,subprocess,json
from pathlib import Path
root=Path.cwd();p=root/'experiments/main-orc-combat-rescue-v5/body-specialist/rear-three-keys'
env=os.environ.copy();env['ASEPRITE_USER_FOLDER']=str(root/'tmp/aseprite-body-specialist-profile')
Path(env['ASEPRITE_USER_FOLDER']).mkdir(parents=True,exist_ok=True)
cmd=['F:/SteamLibrary/steamapps/common/Aseprite/Aseprite.exe','--batch','--noinapp','--script',str(p/'import-swords.lua')]
r=subprocess.run(cmd,env=env,capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=120)
(p/'aseprite-swords-result.json').write_text(json.dumps(dict(command=cmd,profile=env['ASEPRITE_USER_FOLDER'],exitCode=r.returncode,stdout=r.stdout,stderr=r.stderr),indent=2))
print(r.returncode,r.stdout,r.stderr)
