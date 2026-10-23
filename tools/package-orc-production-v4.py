"""ZIP packaging only; verifies every staged file and archive member."""
from pathlib import Path
import json,hashlib,zipfile
root=Path(__file__).resolve().parents[1]
report_file=root/'reports/orc-production-v4-export.json'
report=json.loads(report_file.read_text(encoding='utf-8'))
archive=root/report['zip'];archive.parent.mkdir(parents=True,exist_ok=True)
entries={}
for p in report['packages']:
    folder=root/p['path'];inventory=json.loads((folder/'package-hashes.json').read_text(encoding='utf-8'))
    for f in inventory:
        data=(folder/f['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==f['sha256']
        entries[p['id']+'/'+f['path']]=data
    entries[p['id']+'/package-hashes.json']=(folder/'package-hashes.json').read_bytes()
if not archive.exists():
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,data in sorted(entries.items()):z.writestr(name,data)
with zipfile.ZipFile(archive) as z:
    assert sorted(z.namelist())==sorted(entries)
    assert z.testzip() is None
    for name,data in entries.items():assert z.read(name)==data
result={'status':'PASS','zip':report['zip'],'entries':len(entries),'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
(root/'reports/orc-production-v4-zip-check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
