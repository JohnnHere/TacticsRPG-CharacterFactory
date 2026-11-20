"""Stage D ledger, combined patch and freeze; never writes the back_l freeze."""
from pathlib import Path
import json,hashlib,re,datetime
O=Path(__file__).resolve().relative_to(Path.cwd().resolve()).parent
R=O.parent;C=Path('characters/orc-v1/source/artistic-reconstruction-v6/rear')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
old=json.loads((R/'checkpoint.json').read_text(encoding='utf-8'))
before=json.loads((O/'back-l-freeze-before.json').read_text(encoding='utf-8'))
bad=[p for p,h in old['files'].items() if not Path(p).exists() or sha(p)!=h]
assert not bad,bad
assert sha(R/'checkpoint.json')==before['checkpointFileSha256']
write(O/'back-l-freeze-after.json',{'originalFreezeSha256':old['freezeSha256'],'verifiedFiles':len(old['files']),'changed':bad,'checkpointFileByteIdentical':True,'note':'All frozen artwork and supporting evidence preserved, not only PNGs.'})
jobs=[]
for k in ['sword','axe']:
 sub=json.loads((O/f'{k}-submit.json').read_text(encoding='utf-8'));text='\n'.join(x.get('text','') for x in sub['content'])
 req=json.loads((O/f'{k}-request.json').read_text(encoding='utf-8'))
 jobs.append({'category':k.title(),'jobId':re.search(r'job_id: ([\w-]+)',text)[1],'seed':req['seed'],'costGenerationsFromReceipt':int(re.search(r'cost: (\d+) generations',text)[1]),'frames':12,'tool':'animate_with_skeleton_v3','receipt':(O/f'{k}-submit.json').as_posix(),'request':(O/f'{k}-request.json').as_posix(),'rawFrames':(O/'raw'/k).as_posix()})
snapshots=[]
for name in ['balance-before','balance-after']:
 rr=json.loads((O/f'{name}.json').read_text(encoding='utf-8'));text='\n'.join(x.get('text','') for x in rr['content'])
 snapshots.append({'receipt':(O/f'{name}.json').as_posix(),'generationsRemaining':float(re.search(r'generations_remaining: ([\d.]+)',text)[1])})
own=sum(j['costGenerationsFromReceipt'] for j in jobs);delta=round(snapshots[0]['generationsRemaining']-snapshots[1]['generationsRemaining'],2)
write(O/'pixellab-ledger.json',{'jobs':jobs,'jobCount':len(jobs),'outputFrames':24,'ownGenerationsFromReceipts':own,'snapshots':snapshots,'observedAccountDelta':delta,'unattributedDifference':round(delta-own,2),'attributionNote':'Only these two receipts are charged to this Stage D report. Additional account changes are not attributed without receipts. Previous back_l accounting remains frozen.','purchases':False,'tokensOrMonetaryCost':'NOT_ESTIMATED'})
left=json.loads((C/'patch-manifest.json').read_text(encoding='utf-8'))
right=json.loads((C/'patch-manifest-back-r-stage-d.json').read_text(encoding='utf-8'))
cells=left['cells']+right['cells'];assert len(cells)==4
for cell in cells:assert sha(cell['clip'])==cell['clipSha256']
write(C/'patch-manifest-stage-d.json',{'schemaVersion':1,'checkpoint':'V6_BACK_R_ADAPTATION_READY','technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','creatorApproval':'PENDING_CREATOR','runtimeImplemented':False,'scope':'Four rear cells; back_l points to the immutable reviewed reference, back_r is the Stage D adaptation.','backLReferenceFreeze':old['freezeSha256'],'authorization':'Stage C accepted and Stage D released by orchestrator in user instruction.','cells':cells,'integrationStatus':'NOT_PROMOTED'})
files={}
for cell in right['cells']:
 for p in sorted(Path(cell['clip']).parent.rglob('*')):
  if p.is_file():files[p.as_posix()]=sha(p)
for p in sorted(O.rglob('*')):
 if p.is_file() and p.name!='checkpoint.json':files[p.as_posix()]=sha(p)
files[(C/'patch-manifest-back-r-stage-d.json').as_posix()]=sha(C/'patch-manifest-back-r-stage-d.json')
files[(C/'patch-manifest-stage-d.json').as_posix()]=sha(C/'patch-manifest-stage-d.json')
freeze=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
write(O/'checkpoint.json',{'checkpoint':'V6_BACK_R_ADAPTATION_READY','technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','creatorApproval':'PENDING_CREATOR','capturedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'freezeSha256':freeze,'backLReferenceFreezeSha256':old['freezeSha256'],'backLReferenceFilesVerified':len(old['files']),'runtimeImplemented':False,'files':files,'nextStep':'Orchestrator reviews the exact Stage D back_r adaptation; creator artistic review remains pending. No promotion or Unity integration.'})
print('V6_BACK_R_ADAPTATION_READY',freeze,'Stage D cost',own,'generations; original freeze',len(old['files']),'files intact')
