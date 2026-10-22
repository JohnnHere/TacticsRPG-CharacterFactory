"""Isolate newly authored turnaround poses and reconstruct the approved native contract.
No mirroring, rigging, concept reduction or artistic approval.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

spec=importlib.util.spec_from_file_location('recover_native',Path(__file__).with_name('recover-native-sprite.py'))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def components(source,expected):
    arr=np.array(Image.open(source).convert('RGBA'))
    count,labels,stats,_=cv2.connectedComponentsWithStats((arr[:,:,3]>=160).astype(np.uint8),8)
    if count<2:raise ValueError('No sprite components')
    max_area=int(stats[1:,cv2.CC_STAT_AREA].max())
    ids=[i for i in range(1,count) if stats[i,cv2.CC_STAT_AREA]>max_area*.2]
    ids.sort(key=lambda i:stats[i,cv2.CC_STAT_LEFT])
    if len(ids)!=expected:raise ValueError(f'Expected {expected} whole figures; got {len(ids)}')
    return arr,labels,stats,ids

def extract(character):
    base=Path('characters')/character;folder=base/'source/directions-v1';sheet=folder/'sheet.png'
    palette=base/'source/native-base-v1/front_r-native.png'
    arr,labels,stats,ids=components(sheet,3);results=[]
    for direction,index in zip(['front_l','back_r','back_l'],ids):
        source=sheet;original=arr;mask=labels==index
        x,y,w,h,area=map(int,stats[index]);box=[x,y,x+w,y+h]
        correction=folder/f'{direction}-corrected.png'
        if correction.exists():
            source=correction;original,lab,st,ii=components(source,1);i=ii[0];mask=lab==i
            x,y,w,h,area=map(int,st[i]);box=[x,y,x+w,y+h]
        selected=np.array(original[y:y+h,x:x+w],copy=True)
        selected[~mask[y:y+h,x:x+w]]=0
        target=folder/direction;target.mkdir(parents=True,exist_ok=True)
        pose=target/'pose-source.png';output=target/'native.png'
        if output.exists():raise ValueError(f'Existing native candidate preserved: {output}')
        Image.fromarray(selected).save(pose)
        recovered=module.recover(pose,output,content_height=100,colors=48,palette_path=palette,quiet=True)
        record={'direction':direction,'source':str(source),'sourceSha256':digest(source),'sourceBounds':box,'componentArea':area,'poseSource':str(pose),'poseSha256':digest(pose),'native':str(output),'nativeSha256':digest(output),'processingReport':str(output.with_suffix('.json')),'paletteSource':str(palette),'paletteSha256':digest(palette),'nativeContentSize':recovered['nativeContentSize'],'partialAlpha':recovered['partialAlphaPixels'],'sourceKind':'newly authored image_gen directional sprite source','transformations':'component isolation and explicit target grid; no mirroring','artisticReview':'PENDING_CREATOR_FOUR_VIEWS'}
        (target/'extraction.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');results.append(record)
    (folder/'extraction.json').write_text(json.dumps({'character':character,'directions':results},indent=2)+'\n',encoding='utf-8')
    print(f'{character}: 3 native directional candidates, 128x128/height100/ground126, approved front palette')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('character');extract(ap.parse_args().character)
