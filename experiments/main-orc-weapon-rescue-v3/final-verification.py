"""Final metadata/hash verification after documentation packaging, no artwork or renderer changes."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];E=Path(__file__).resolve().parent;O=R/'reports/main-orc-weapon-rescue-v3';L=R/'Biblioteca de Arte/Personagens Jogaveis/Orc V1'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
protected=read(E/'protected-art.json');assert all(sha(R/p)==h for p,h in protected.items())
locks=read(E/'authored-master-lock.json');assert len(locks)==10 and all(sha(R/p)==h for p,h in locks.items())
catalog=read(L/'catalogo.json');assert all(sha(L/f['file'])==f['sha256'] for f in catalog['files'])
for category in ['Sword','Axe']:
 clip=read(R/f'characters/orc-v1/source/onehanded-rescue-v3/{category}/Attack/clip.json');alt=read(O/f'reuse/{category}/reuse.json')
 for a,b in zip(alt['frames'],clip['frames']):assert a['retainedBodySha256']==b['layers']['body']['sha256'] and a['retainedHandSha256']==b['layers']['handFront']['sha256'] and a['durationMs']==b['durationMs']
for name in ['Espada do Recruta','Machado de Milícia']:
 for state in ['Idle','Walk']:assert not (L/'Armas'/name/state).exists()
assert (R/'README.md').read_text(encoding='utf-8').count('**Orc principal — revisão candidata')==1
result={'status':'PASS','pipeline':{'command':'node --test --test-concurrency=1','passed':14,'failed':0,'initialParallelRun':{'passed':13,'failed':1,'issue':'Windows EPERM moving temporary test build; exact contention source unconfirmed','evidence':'tmp/aseprite/test-editor-d70e8f508a-normal-0w4onG/failure.json'}},'artifacts':'reports/main-orc-weapon-rescue-v3/check.json','library':'reports/art-library-check.json','finalHashVerification':{'protectedPriorArt':len(protected),'lockedCurrentMasters':len(locks),'portableCopies':len(catalog['files'])},'reusableReplacementFrames':18,'oldArmedIdleWalkAbsentFromCurrentFolders':True,'artisticApproval':'PENDING_CREATOR','runtimeImplemented':False};(O/'validation-summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
