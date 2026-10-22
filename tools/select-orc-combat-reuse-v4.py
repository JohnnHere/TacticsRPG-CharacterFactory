"""Select actual corrected calls and retain unimported failed candidates."""
import hashlib,json,shutil
from pathlib import Path
root=Path('.').resolve()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
batches=read('characters/orc-combat-directions-batch-v2.json')
for b in batches:
 folder=Path(b['folder']);corrected=folder/'attack-reuse-v4.generation.json'
 if b['id'] in ['orc-01-squire','orc-01-archer']:b['visuallyReviewedOverlappingX']=['Attack']
 if not corrected.exists():continue
 g=read(corrected);g.update(sourceSha256=sha(folder/g['source']),promptSha256=sha(folder/g['promptFile']))
 for r in g['references']:r['sha256']=sha(r['file'])
 write(corrected,g)
 current=read(folder/'generation.json')
 if any(c.get('sourceSha256')==g['sourceSha256'] for c in current.get('corrections',[])):continue
 attack=root/'characters'/b['id']/f"source/animations-v1/Attack/{b['direction']}"
 if attack.exists():
  # Only unpublished new directions are candidates; approved runtime files are protected.
  runtime=root/'characters'/b['id']/f"sprites/Animations/Attack/attack_{b['direction']}_00.png"
  assert not runtime.exists(),f'Already imported candidate requires explicit version handling: {runtime}'
  archive=root/'characters'/b['id']/f"source/animations-rejected-v2/Attack/{b['direction']}"
  assert attack.resolve().is_relative_to(root) and archive.resolve().is_relative_to(root) and not archive.exists()
  archive.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(attack),str(archive))
 if (folder/'extraction.json').exists():shutil.move(str(folder/'extraction.json'),str(folder/'extraction.pre-reuse-v4.json'))
 current['corrections']=[c for c in current.get('corrections',[]) if c['state']!='Attack']+[g];write(folder/'generation.json',current)
 print(b['id'],b['direction'],'selected corrected Attack; other states retained')
write('characters/orc-combat-directions-batch-v2.json',batches)
