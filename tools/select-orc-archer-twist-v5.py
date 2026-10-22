import json,hashlib,shutil
from pathlib import Path
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
batch=Path('characters/orc-combat-directions-batch-v2.json');bs=read(batch);b=next(b for b in bs if b['id']=='orc-01-archer' and b['direction']=='back_r');folder=Path(b['folder'])
g=read(folder/'attack-twist-v5.generation.json');g.update(sourceSha256=sha(folder/g['source']),promptSha256=sha(folder/g['promptFile']))
for r in g['references']:r['sha256']=sha(r['file'])
write(folder/'attack-twist-v5.generation.json',g)
primary=read(folder/'generation.json');primary['corrections']=[g];write(folder/'generation.json',primary)
if (folder/'extraction.json').exists():shutil.move(str(folder/'extraction.json'),str(folder/'extraction.pre-twist-v5.json'))
b['animationSourceVersions']={'Attack':'animations-v2'};b['replaceUnapprovedStates']=['Attack'];write(batch,bs)
report=Path('characters/orc-combat-directions-editor-v1.json');e=read(report);target=lambda c:c['id']=='orc-01-archer' and c['direction']=='back_r' and c['state']=='Attack'
old=next(c for c in e['clips'] if target(c));assert old['editable'].endswith('source/animations-v1/Attack/back_r/attack_back_r.aseprite')
assets=read('characters/orc-01-archer/assets.json')
for i in range(5):
 file=f'sprites/Animations/Attack/attack_back_r_{i:02d}.png';a=next(a for a in reversed(assets) if a.get('file')==file);assert a['artisticApproval']=='PENDING_CREATOR_COMPLETE_REVIEW'
write('characters/orc-01-archer/source/combat-directions-v1/back_r/rejected-editor-v2.json',old)
e['clips']=[c for c in e['clips'] if not target(c)];write(report,e)
