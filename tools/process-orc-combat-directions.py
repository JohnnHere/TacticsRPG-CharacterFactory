"""Resume native extraction from actual returned sources, retaining all attempts."""
import hashlib,json,subprocess,os
from pathlib import Path
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
batch='characters/orc-combat-directions-batch-v2.json';results=[]
for b in read(batch):
 folder=Path(b['folder']);gfile=folder/(b['generationName']+'.generation.json' if b['preserveReactionSource'] else 'generation.json')
 if not gfile.exists():continue
 g=read(gfile);g.update(sourceSha256=sha(folder/g['source']),promptSha256=sha(folder/g['promptFile']))
 for ref in g['references']:assert sha(ref['file'])==ref['sha256']
 write(gfile,g)
 if b['preserveReactionSource']:
  primary=read(folder/'generation.json')
  if not primary.get('corrections'):primary['corrections']=[g];write(folder/'generation.json',primary)
 if (folder/'extraction.json').exists():continue
 p=subprocess.run([str(Path('tmp/pixel-venv/Scripts/python.exe')),'tools/extract-orc-combat-front.py','--batch',batch,'--id',b['id'],'--direction',b['direction']],capture_output=True,text=True,encoding='utf-8',errors='replace',env={**os.environ,'PYTHONUTF8':'1'})
 results.append({'id':b['id'],'direction':b['direction'],'exit':p.returncode,'output':p.stdout,'error':p.stderr})
 print(b['id'],b['direction'],'PASS' if p.returncode==0 else p.stderr[-650:],flush=True)
write('characters/orc-combat-directions-extraction-attempts-v1.json',results)
