"""Extract real authored punch poses and create a separate validated action supplement."""
import argparse,contextlib,hashlib,importlib.util,io,json,shutil,subprocess
from pathlib import Path
import cv2,numpy as np
from PIL import Image
root=Path('.').resolve()
def module(name,file):
 s=importlib.util.spec_from_file_location(name,root/'tools'/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
extractor=module('extractor','extract-animation-sheet.py');writer=module('writer','write-animation-editable.py')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
parser=argparse.ArgumentParser();parser.add_argument('--batch',default='characters/orc-unarmed-front-batch-v1.json');parser.add_argument('--report',default='characters/orc-unarmed-front-validation-v1.json');args=parser.parse_args()
registry=read('characters/orc-equipment-actions-v1.json');records=[]
for b in read(args.batch):
 direction=b['direction']
 folder=Path(b['folder']);gpath=folder/'generation.json'
 if not gpath.exists():continue
 previous=next(c for c in registry['characters'] if c['id']==b['id'])['unarmed'][direction]
 if previous.get('artisticReview','').startswith('APPROVED_'):raise ValueError('Approved action cannot be reimported by extraction; use the read-only verifier')
 g=read(gpath);g.update(sourceSha256=sha(folder/'sheet.png'),promptSha256=sha(folder/'sheet.prompt.md'));write(gpath,g)
 for r in g['references']:assert sha(r['file'])==r['sha256']
 if not (folder/'clip.json').exists():
  a=np.array(Image.open(folder/'sheet.png').convert('RGBA'));n,labels,stats,_=cv2.connectedComponentsWithStats((a[:,:,3]>=160).astype(np.uint8),8);big=stats[1:,4].max();ids=[i for i in range(1,n) if stats[i,4]>=big*.15];ids.sort(key=lambda i:stats[i,0]);assert len(ids)==5,'Five authored figures required'
  heights=[round(int(stats[i,3])/int(stats[ids[0],3])*100) for i in ids]
  with contextlib.redirect_stdout(io.StringIO()) as logs:clip=extractor.extract(folder/'sheet.png','Attack',direction,b['palette'],b['base'],allow_overlapping=True,content_heights=heights,registration='pelvis')
  (folder/'extraction.log').write_text(logs.getvalue(),encoding='utf-8');clip.update(actionProfile='basic.unarmed',layerName=f"{b['id']} basic unarmed {direction} - body and outfit raster",requestedContentHeights=heights);write(folder/'clip.json',clip)
 writer.write_clip(folder);ase=folder/f'attack_{direction}.aseprite';sheet=Path('tmp')/f"editor-{b['id']}-basic-unarmed-{direction}.png";data=sheet.with_suffix('.json')
 subprocess.run([str(root/'tmp/tools/libresprite/libresprite.exe'),'-b','--format','json-array','--data',str(data),'--sheet-type','horizontal','--sheet',str(sheet),str(ase)],capture_output=True,check=True)
 ed=read(data);assert len(ed['frames'])==5;exported=Image.open(sheet).convert('RGBA');dest=Path('characters')/b['id']/f"actions/basic-unarmed/{b.get('supplementVersion','v1')}/{direction}";dest.mkdir(parents=True,exist_ok=True)
 palette={tuple(p[:3]) for p in np.array(Image.open(b['palette']).convert('RGBA')).reshape(-1,4) if p[3]}
 frames=[]
 for i,e in enumerate(ed['frames']):
  name=f'attack_{direction}_{i:02d}.png';p=folder/name;im=Image.open(p).convert('RGBA');a=np.array(im);assert im.size==(128,128) and set(np.unique(a[:,:,3]))=={0,255};assert np.where(a[:,:,3]>0)[0].max()==126;assert all(tuple(p[:3]) in palette for p in a.reshape(-1,4) if p[3]);r=e['frame'];assert e['duration']==90 and exported.crop((r['x'],r['y'],r['x']+128,r['y']+128)).tobytes()==im.tobytes()
  if (dest/name).exists():assert sha(dest/name)==sha(p),'Different supplement preserved'
  else:shutil.copy2(p,dest/name)
  frames.append({'file':(dest/name).as_posix(),'sha256':sha(p),'processingReport':p.with_suffix('.json').as_posix()})
 assert len({f['sha256'] for f in frames})==5
 for name in ['native-strip.png']:shutil.copy2(folder/name,dest/name)
 entry={'status':'READY_NATIVE_BODY_CANDIDATE','bodyProfile':'basic.unarmed','frames':frames,'durationMs':90,'loop':False,'weaponOverlay':False,'editable':ase.as_posix(),'editableSha256':sha(ase),'artisticReview':'PENDING_CREATOR_FRONT_BATCH' if direction=='front_r' else 'PENDING_CREATOR_COMPLETE_REVIEW','source':(folder/'sheet.png').as_posix(),'sourceSha256':sha(folder/'sheet.png'),'generation':gpath.as_posix(),'editorSheet':sheet.as_posix(),'editorData':data.as_posix(),'editorRgba':'ALL_RGBA_AND_DURATIONS_IDENTICAL','strip':(dest/'native-strip.png').as_posix()}
 write(dest/'clip-manifest.json',entry);next(c for c in registry['characters'] if c['id']==b['id'])['unarmed'][direction]=entry;records.append({'id':b['id'],'direction':direction,**entry});print(b['id'],direction,'5 unarmed PNGs and real editor roundtrip PASS',flush=True)
write('characters/orc-equipment-actions-v1.json',registry);write(args.report,{'clips':records,'newFrames':len(records)*5,'newEditables':len(records),'artisticReview':'PENDING_CREATOR_COMPLETE_REVIEW','runtimeImplemented':False,'legacyAssetsChanged':False})
