"""Select authored rows from a 4+6 pose source and use the existing native extractor."""
import argparse,hashlib,importlib.util,json,shutil
from pathlib import Path
import cv2,numpy as np
from PIL import Image

spec=importlib.util.spec_from_file_location('animation_extract',Path(__file__).with_name('extract-animation-sheet.py'))
extractor=importlib.util.module_from_spec(spec);spec.loader.exec_module(extractor)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def extract(character):
    base=Path('characters')/character;origin=base/'source/locomotion-front-v1';source=origin/'sheet.png'
    a=np.array(Image.open(source).convert('RGBA'));n,labels,stats,_=cv2.connectedComponentsWithStats((a[:,:,3]>=160).astype(np.uint8),8)
    if n<=1:raise ValueError('Empty sheet')
    biggest=stats[1:,4].max();ids=[i for i in range(1,n) if stats[i,4]>=biggest*.15]
    if len(ids)!=10:raise ValueError(f'Expected 10 authored poses, got {len(ids)}; no invented frames')
    ids.sort(key=lambda i:stats[i,1]);groups=[ids[:4],ids[4:]]
    if max(stats[i,1]+stats[i,3] for i in groups[0])>=min(stats[i,1] for i in groups[1]):raise ValueError('Idle/Walk rows overlap or counts are wrong')
    reports=[]
    for state,row in zip(['Idle','Walk'],groups):
        selected_origin=source;aa=a;ll=labels;ss=stats;prompt_source=origin/'sheet.prompt.md'
        correction=origin/'walk-corrected-v2.png'
        if state=='Walk' and correction.exists():
            selected_origin=correction;aa=np.array(Image.open(correction).convert('RGBA'))
            nn,ll,ss,_=cv2.connectedComponentsWithStats((aa[:,:,3]>=160).astype(np.uint8),8)
            big=ss[1:,4].max();row=[i for i in range(1,nn) if ss[i,4]>=big*.15]
            if len(row)!=6:raise ValueError('Corrected Walk must contain exactly six complete poses')
            prompt_source=origin/'walk-corrected-v2.prompt.md'
        row.sort(key=lambda i:ss[i,0]);boxes=[[int(ss[i,0]),int(ss[i,1]),int(ss[i,0]+ss[i,2]),int(ss[i,1]+ss[i,3])] for i in row]
        x0=min(b[0] for b in boxes);y0=min(b[1] for b in boxes);x1=max(b[2] for b in boxes);y1=max(b[3] for b in boxes)
        cropped=aa[y0:y1,x0:x1].copy();keep=np.isin(ll[y0:y1,x0:x1],row);cropped[~keep]=0
        target=base/f'source/animations-v1/{state}/front_r';target.mkdir(parents=True,exist_ok=True)
        sheet=target/'sheet.png'
        if sheet.exists():raise ValueError(f'Existing selected source preserved: {sheet}')
        Image.fromarray(cropped).save(sheet);shutil.copyfile(prompt_source,target/'sheet.prompt.md')
        selection={'origin':str(selected_origin),'originSha256':sha(selected_origin),'originPrompt':str(prompt_source),'selectedRow':state,'figureCount':len(row),'originBounds':[x0,y0,x1,y1],'figureBoxes':boxes,'selectedSheetSha256':sha(sheet),'operation':'Exact RGBA row crop and alpha component selection, no mirroring/scaling or generated motion'}
        (target/'row-selection.json').write_text(json.dumps(selection,indent=2)+'\n',encoding='utf-8')
        palette=base/'source/native-base-v1/front_r-native.png';native_base=base/f'sprites/Directions/{character.replace("-","_")}_dir_front_r.png'
        checks=extractor.extract(sheet,state,'front_r',palette,native_base)
        checks['layerName']=f'{character} {state} front_r - weaponless raster'
        (target/'clip.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
        reports.append({'state':state,'frames':checks['frames'],'uniqueFrames':checks['uniqueRgbaFrames'],'selectedSource':str(sheet),'originSha256':sha(selected_origin)})
    (origin/'extraction.json').write_text(json.dumps({'character':character,'clips':reports},indent=2)+'\n',encoding='utf-8')
    print(f'{character}: 4 Idle + 6 Walk front_r native frames reconstructed')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('character');extract(ap.parse_args().character)
