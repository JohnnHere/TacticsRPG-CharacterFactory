from pathlib import Path
import json,hashlib,datetime
E=Path('experiments/main-orc-rear-reconstruction-v4/dev')
C=Path('characters/orc-v1/source/rear-reconstruction-v4')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
for p,h in read(E/'input-inventory.json').items():assert sha(p)==h,p
m=read(C/'candidate28manifest.json');v=read(E/'verification.json');k=read(E/'checkpoint.json')
assert m['revision']=='main-orc-rear-reconstruction-v4'
assert m['eligibleForIntegration']is False and k['eligibleForIntegration']is False
assert m['technicalStatus']=='NOT_VERIFIED'and m['artisticStatus']=='ARTISTIC_REVISION_REQUIRED'
assert len(m['cells'])==28 and sum(c['frameCount']for c in m['cells'])==210
assert sum(c['isAffected']for c in m['cells'])==8
assert v['status']=='PASS_FOCUSED_MATERIAL_FORK_TECHNICAL_CHECKS'and not v['inputDrift']and not v['failures']
paths=sorted(p for base in [C,E]for p in base.rglob('*')if p.is_file()and 'batch-profile'not in p.parts and p.name!='version-freeze.json')
freeze={'schemaVersion':1,'revision':m['revision'],'createdAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ARTISTIC_REVISION_REQUIRED','eligibleForIntegration':False,'scope':'Immutable owned candidate and DEV handoff. Diagnostic-only; material/scalp partial. No Root review files included.','manifest':str(C/'candidate28manifest.json').replace('\\','/'),'manifestSha256':sha(C/'candidate28manifest.json'),'devReport':str(E/'report.md').replace('\\','/'),'devReportSha256':sha(E/'report.md'),'verification':str(E/'verification.json').replace('\\','/'),'verificationSha256':sha(E/'verification.json'),'inputFilesPreserved':873,'exclusions':['version-freeze.json itself','disposable batch-profile/**'],'fileCount':len(paths),'files':[{'path':str(p).replace('\\','/'),'sizeBytes':p.stat().st_size,'sha256':sha(p)}for p in paths]}
f=E/'version-freeze.json';f.write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all(sha(r['path'])==r['sha256']for r in freeze['files'])
print(json.dumps({k:freeze[k]for k in ['status','eligibleForIntegration','fileCount','manifestSha256','devReportSha256','verificationSha256']}))
print('freezeSha256='+sha(f))
