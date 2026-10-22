"""Extract the thirteen actual combat drawings; preserve authored relative heights."""
import argparse,contextlib,hashlib,importlib.util,io,json,shutil
from pathlib import Path
import cv2,numpy as np
from PIL import Image
spec=importlib.util.spec_from_file_location('extractor',Path(__file__).with_name('extract-animation-sheet.py'));extractor=importlib.util.module_from_spec(spec);spec.loader.exec_module(extractor)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
ap=argparse.ArgumentParser();ap.add_argument('--id');ap.add_argument('--direction');ap.add_argument('--batch',default='characters/orc-combat-front-batch-v1.json');args=ap.parse_args()
for b in read(args.batch):
 if args.id and args.id!=b['id']:continue
 direction=b.get('direction','front_r')
 if args.direction and direction!=args.direction:continue
 origin=Path(b['folder']);source=origin/'sheet.png'
 if not (origin/'generation.json').exists() or (origin/'extraction.json').exists():continue
 a=np.array(Image.open(source).convert('RGBA'));n,labels,stats,_=cv2.connectedComponentsWithStats((a[:,:,3]>=160).astype(np.uint8),8)
 biggest=stats[1:,4].max();ids=[i for i in range(1,n) if stats[i,4]>=biggest*.15]
 if len(ids)!=13:raise ValueError(f"{b['id']}: expected13 complete drawings, found{len(ids)}; no invented motion")
 ids.sort(key=lambda i:stats[i,1]);groups=[ids[:5],ids[5:8],ids[8:]]
 for i in range(2):
  if max(stats[k,1]+stats[k,3] for k in groups[i])>=min(stats[k,1] for k in groups[i+1]):raise ValueError('Rows overlap')
 g=read(origin/'generation.json');g.update({'sourceSha256':sha(source),'promptSha256':sha(origin/'sheet.prompt.md')});write(origin/'generation.json',g);reports=[]
 for state,row in zip(['Attack','Hit','Defeat'],groups):
  selected=source;aa=a;ll=labels;ss=stats;prompt_source=origin/'sheet.prompt.md'
  correction=next((c for c in g.get('corrections',[]) if c['state']==state),None)
  if correction:
   selected=origin/correction['source'];prompt_source=origin/correction['promptFile'];aa=np.array(Image.open(selected).convert('RGBA'));nn,ll,ss,_=cv2.connectedComponentsWithStats((aa[:,:,3]>=160).astype(np.uint8),8);big=ss[1:,4].max();row=[i for i in range(1,nn) if ss[i,4]>=big*.15]
   if len(row)!=b['states'][state]:raise ValueError('Corrected source count mismatch')
  row.sort(key=lambda i:ss[i,0]);boxes=[[int(ss[i,0]),int(ss[i,1]),int(ss[i,0]+ss[i,2]),int(ss[i,1]+ss[i,3])] for i in row]
  x0=min(r[0] for r in boxes);y0=min(r[1] for r in boxes);x1=max(r[2] for r in boxes);y1=max(r[3] for r in boxes)
  crop=aa[y0:y1,x0:x1].copy();crop[~np.isin(ll[y0:y1,x0:x1],row)]=0
  version=b.get('animationSourceVersions',{}).get(state,'animations-v1')
  target=Path('characters')/b['id']/f'source/{version}/{state}/{direction}';target.mkdir(parents=True,exist_ok=True)
  if (target/'sheet.png').exists():
   prior=read(target/'row-selection.json')
   if prior['originSha256']!=sha(selected) or prior['selectedSheetSha256']!=sha(target/'sheet.png') or sha(prompt_source)!=sha(target/'sheet.prompt.md'):raise ValueError(f'Existing different source preserved: {target}')
   if (target/'clip.json').exists():
    clip=read(target/'clip.json')
    if clip['uniqueRgbaFrames']!=b['states'][state] or any(not (target/f'{state.lower()}_{direction}_{i:02d}.png').exists() for i in range(b['states'][state])):raise ValueError('Incomplete/duplicate clip cannot be resumed as complete')
    reports.append({'state':state,'direction':direction,'frames':clip['frames'],'uniqueFrames':clip['uniqueRgbaFrames'],'folder':target.as_posix()});continue
  else:
   Image.fromarray(crop).save(target/'sheet.png');shutil.copy2(prompt_source,target/'sheet.prompt.md')
  heights=[round((r[3]-r[1])/(boxes[0][3]-boxes[0][1])*100) for r in boxes]
  selection={'origin':selected.as_posix(),'originSha256':sha(selected),'originPrompt':prompt_source.as_posix(),'selectedRow':state,'figureCount':len(row),'originBounds':[x0,y0,x1,y1],'figureBoxes':boxes,'selectedSheetSha256':sha(target/'sheet.png'),'operation':'Exact RGBA component row selection; no mirroring, scaling or invented poses','requestedContentHeights':heights,'heightCalibration':'First authored pose100 native pixels, remaining heights retain source physical scale; arm lifts can exceed100'};write(target/'row-selection.json',selection)
  base=Path('characters')/b['id']/f"sprites/Directions/{b['id'].replace('-','_')}_dir_{direction}.png"
  # Reviewed independent alpha components: extended arms can share X ranges
  # with the next figure's feet without touching or sharing pixels.
  allow_overlap=(b['id'] in ['orc-01-apprentice-mage','orc-01-rogue','orc-01-brawler','orc-01-scout'] and state=='Attack') or state in b.get('visuallyReviewedOverlappingX',[])
  with contextlib.redirect_stdout(io.StringIO()) as log:clip=extractor.extract(target/'sheet.png',state,direction,b['palette'],base,allow_overlapping=allow_overlap,content_heights=heights,registration='pelvis')
  (target/'extraction.log').write_text(log.getvalue(),encoding='utf-8');clip.update({'layerName':f"{b['id']} {state} {direction} - weaponless body raster",'action':b['action'] if state=='Attack' else state,'requestedContentHeights':heights,'loop':False});write(target/'clip.json',clip)
  reports.append({'state':state,'direction':direction,'frames':clip['frames'],'uniqueFrames':clip['uniqueRgbaFrames'],'folder':target.as_posix()})
 write(origin/'extraction.json',{'id':b['id'],'direction':direction,'clips':reports,'artisticApproval':'PENDING_CREATOR_COMBAT_REVIEW'});print(b['id'],direction,'13 native combat frames extracted',flush=True)
