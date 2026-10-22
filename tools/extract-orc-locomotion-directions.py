"""Select two actually drawn rows, reconstruct native frames and preserve provenance."""
import argparse,contextlib,hashlib,importlib.util,io,json,shutil
from pathlib import Path
import cv2,numpy as np
from PIL import Image
spec=importlib.util.spec_from_file_location('extractor',Path(__file__).with_name('extract-animation-sheet.py'));extractor=importlib.util.module_from_spec(spec);spec.loader.exec_module(extractor)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
ap=argparse.ArgumentParser();ap.add_argument('--id');ap.add_argument('--direction');args=ap.parse_args()
for b in read('characters/orc-locomotion-single-view-batch-v1.json'):
 if args.id and b['id']!=args.id or args.direction and b['direction']!=args.direction:continue
 origin=Path(b['folder']);source=origin/'sheet.png'
 if not (origin/'generation.json').exists() or (origin/'extraction.json').exists():continue
 a=np.array(Image.open(source).convert('RGBA'));n,labels,stats,_=cv2.connectedComponentsWithStats((a[:,:,3]>=160).astype(np.uint8),8)
 biggest=stats[1:,4].max();ids=[i for i in range(1,n) if stats[i,4]>=biggest*.15]
 if len(ids)!=10:raise ValueError(f"{b['id']} {b['direction']}: expected10 authored figures, found{len(ids)}")
 ids.sort(key=lambda i:stats[i,1]);groups=[ids[:4],ids[4:]]
 if max(stats[i,1]+stats[i,3] for i in groups[0])>=min(stats[i,1] for i in groups[1]):raise ValueError('Rows overlap')
 g=read(origin/'generation.json');g.update({'sourceSha256':sha(source),'promptSha256':sha(origin/'sheet.prompt.md')});write(origin/'generation.json',g)
 reports=[]
 for state,row in zip(['Idle','Walk'],groups):
  row.sort(key=lambda i:stats[i,0]);boxes=[[int(stats[i,0]),int(stats[i,1]),int(stats[i,0]+stats[i,2]),int(stats[i,1]+stats[i,3])] for i in row]
  x0=min(r[0] for r in boxes);y0=min(r[1] for r in boxes);x1=max(r[2] for r in boxes);y1=max(r[3] for r in boxes)
  crop=a[y0:y1,x0:x1].copy();crop[~np.isin(labels[y0:y1,x0:x1],row)]=0
  target=Path('characters')/b['id']/f"source/animations-v1/{state}/{b['direction']}";target.mkdir(parents=True,exist_ok=True)
  if (target/'sheet.png').exists():raise ValueError(f'Existing candidate preserved: {target}')
  Image.fromarray(crop).save(target/'sheet.png');shutil.copy2(origin/'sheet.prompt.md',target/'sheet.prompt.md')
  selection={'origin':source.as_posix(),'originSha256':sha(source),'originPrompt':(origin/'sheet.prompt.md').as_posix(),'selectedRow':state,'figureCount':len(row),'originBounds':[x0,y0,x1,y1],'figureBoxes':boxes,'selectedSheetSha256':sha(target/'sheet.png'),'operation':'Exact RGBA component row selection; no mirroring, scaling or invented motion'};write(target/'row-selection.json',selection)
  base=Path('characters')/b['id']/f"sprites/Directions/{b['id'].replace('-','_')}_dir_{b['direction']}.png"
  with contextlib.redirect_stdout(io.StringIO()) as log:clip=extractor.extract(target/'sheet.png',state,b['direction'],b['palette'],base)
  (target/'extraction.log').write_text(log.getvalue(),encoding='utf-8');clip['layerName']=f"{b['id']} {state} {b['direction']} - weaponless raster";write(target/'clip.json',clip)
  reports.append({'state':state,'direction':b['direction'],'frames':clip['frames'],'uniqueFrames':clip['uniqueRgbaFrames'],'folder':target.as_posix()})
 write(origin/'extraction.json',{'id':b['id'],'direction':b['direction'],'clips':reports,'artisticApproval':'PENDING_CREATOR_LOCOMOTION_DIRECTIONS_REVIEW'})
 print(b['id'],b['direction'],'10 native frames extracted',flush=True)
