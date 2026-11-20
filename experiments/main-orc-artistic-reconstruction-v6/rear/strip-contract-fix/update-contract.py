from pathlib import Path
import json,hashlib
from PIL import Image
C=Path('characters/orc-v1/source/artistic-reconstruction-v6/rear')
O=Path(__file__).resolve().relative_to(Path.cwd().resolve()).parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
before=json.loads((O/'before.json').read_text(encoding='utf-8'))
fields={'strip','stripSha256','nativeStrip','nativeStripSha256','compositeStrip','compositeStripSha256'}
records=[];clip_hashes={}
for path,original in before['clips'].items():
 p=Path(path);cell=p.parent;current=json.loads(p.read_text(encoding='utf-8'));assert current==original
 native=cell/'native-strip.png';comp=cell/'composite-strip.png'
 for strip,size,key in [(native,128,'nativePng'),(comp,256,'png')]:
  im=Image.open(strip).convert('RGBA');assert im.size==(size*current['frameCount'],size)
  for i,f in enumerate(current['frames']):
   assert im.crop((i*size,0,(i+1)*size,size)).tobytes()==Image.open(f[key]).convert('RGBA').tobytes(),(path,i,key)
 updates={'strip':native.as_posix(),'stripSha256':sha(native),'nativeStrip':native.as_posix(),'nativeStripSha256':sha(native),'compositeStrip':comp.as_posix(),'compositeStripSha256':sha(comp)}
 assert not(fields & current.keys()),'Expected missing strip contract; refusing unrelated replacement'
 text=p.read_bytes().decode('utf-8');nl='\r\n' if '\r\n' in text else '\n'
 marker='  "layerOrder":';assert marker in text
 insertion=nl.join('  '+json.dumps(k)+': '+json.dumps(v,ensure_ascii=False)+',' for k,v in updates.items())+nl
 p.write_bytes(text.replace(marker,insertion+marker,1).encode('utf-8'))
 modified=json.loads(p.read_text(encoding='utf-8'));assert {k:v for k,v in modified.items() if k not in fields}==original
 clip_hashes[path]=sha(p);records.append({'cell':cell.name,'clipSha256':sha(p),**updates,'nativeDimensions':[128*current['frameCount'],128],'compositeDimensions':[256*current['frameCount'],256],'individualTilesExact':current['frameCount']*2})
manifests=[C/'patch-manifest-stage-d.json']+list(Path('experiments').rglob('patch-manifest-stage-d.json'))
updated=[]
for p in manifests:
 text=p.read_bytes().decode('utf-8');obj=json.loads(text);changed=0
 for cell in obj.get('cells',[]):
  if cell.get('clip') in clip_hashes:
   old=cell['clipSha256'];new=clip_hashes[cell['clip']]
   needle='"clipSha256": '+json.dumps(old);assert text.count(needle)==1
   text=text.replace(needle,'"clipSha256": '+json.dumps(new),1);changed+=1
 assert changed==4,(str(p),changed)
 p.write_bytes(text.encode('utf-8'));updated.append({'path':p.as_posix(),'sha256':sha(p),'updatedCells':changed})
for p,h in before['protectedFiles'].items():assert sha(p)==h,('Protected file changed',p)
roundtrip=json.loads((O/'aseprite-roundtrip.json').read_text(encoding='utf-8'));assert len(roundtrip)==4
report={'technicalStatus':'TECHNICALLY_COMPLETE','scope':'Strip contract only; art masters/frames/timings/layers preserved. Prior freezes are historical; four clip metadata hashes intentionally changed by explicit instruction.','protectedFilesByteIdentical':len(before['protectedFiles']),'cells':records,'updatedManifests':updated,'asepriteSavedMasterReopenRoundtrip':roundtrip,'artisticStatus':'VISUAL_REVIEW_REQUIRED','creatorApproval':'PENDING_CREATOR'}
(O/'result.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
for r in records:print(r['cell'],'clip',r['clipSha256'],'native',r['nativeStripSha256'],'composite',r['compositeStripSha256'])
print('Protected files unchanged:',len(before['protectedFiles']),'Updated manifests:',len(updated))
