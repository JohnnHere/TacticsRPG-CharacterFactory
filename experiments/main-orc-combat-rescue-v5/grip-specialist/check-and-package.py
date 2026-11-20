from pathlib import Path
from PIL import Image
import json,hashlib,struct,zlib,numpy as np
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist');C=Path('characters/orc-v1/source/combat-rescue-v5/grip-specialist/F06')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def delta(a,b):return int(((a!=b).any(2)&((a[:,:,3]>0)|(b[:,:,3]>0))).sum())
def decode(p):
 data=Path(p).read_bytes();frames,w,h,depth=struct.unpack_from('<HHHH',data,6);assert frames==1 and depth==32
 ms=struct.unpack_from('<H',data,136)[0];n=struct.unpack_from('<H',data,134)[0];n=struct.unpack_from('<I',data,140)[0]or n
 layers=[];cels={};off=144
 for _ in range(n):
  length,typ=struct.unpack_from('<IH',data,off);b=data[off+6:off+length]
  if typ==0x2004:
   flags=struct.unpack_from('<H',b,0)[0];ln=struct.unpack_from('<H',b,16)[0];layers.append({'name':b[18:18+ln].decode('utf8'),'visible':bool(flags&1),'opacity':b[12]})
  elif typ==0x2005:
   li,x,y,op,ct=struct.unpack_from('<HhhBH',b,0);assert ct in [0,2];cw,ch=struct.unpack_from('<HH',b,16)
   raw=b[20:]if ct==0 else zlib.decompress(b[20:]);cels[li]=(Image.frombytes('RGBA',(cw,ch),raw),x,y,op)
  off+=length
 out=Image.new('RGBA',(w,h));images={};positions=[]
 for li,l in enumerate(layers):
  canvas=Image.new('RGBA',(w,h));cel=cels.get(li)
  if cel:
   im,x,y,op=cel;assert op==255 and l['opacity']==255;canvas.paste(im,(x,y));positions.append({'layer':l['name'],'position':[x,y],'imageSize':list(im.size)})
  if l['visible']:out=Image.alpha_composite(out,canvas)
  images[l['name']]=np.array(canvas)
 return {'canvas':[w,h],'durationMs':ms,'layers':images,'flat':np.array(out),'celPositions':positions}
snap=read(E/'input-snapshot.json');assert all(sha(p)==h for p,h in snap['files'].items())
parentPath=snap['clips'][1];parent=read(parentPath);old=parent['frames'][6];wd=read(snap['weapon']);anatomy=read(E/'anatomy.json')
body=arr(C/'layers/body.png');original=arr(old['layers']['body']['png']);flat=arr(C/'composite-256.png');hf=arr(C/'layers/handFront.png');wb=arr(C/'layers/weaponBack.png');wf=arr(C/'layers/weaponFront.png')
assert delta(body,original)==0
assert all(np.isin(a[:,:,3],[0,255]).all()for a in [body,flat,hf,wb,wf])
assert np.all(body[hf[:,:,3]>0,3]==255)
assert not np.any((hf[:,:,3]>0)&((np.indices((256,256))[1]<152)|(np.indices((256,256))[1]>157)|(np.indices((256,256))[0]<110)|(np.indices((256,256))[0]>117)))
retouchDelta=delta(hf,np.where((hf[:,:,3]>0)[:,:,None],body,0).astype('uint8'));assert retouchDelta==9
doc=decode(C/'source/composite.aseprite');assert doc['durationMs']==35 and list(doc['layers'])==['weaponBack','body','weaponFront','handFront']
assert delta(doc['flat'],flat)==0
for n,a in [('weaponBack',wb),('body',body),('weaponFront',wf),('handFront',hf)]:
 assert delta(doc['layers'][n],a)==0
 assert delta(a[64:192,64:192],arr(C/'native/layers'/(n+'.png')))==0
assert delta(body[64:192,64:192],arr(C/'body-128.png'))==0
assert delta(flat[64:192,64:192],arr(C/'composite-native-128.png'))==0
outside=flat.copy();outside[64:192,64:192]=0;assert int((outside[:,:,3]>0).sum())==0,'Native composite crop would cut content'
for filename,im in [('body-256.aseprite',body),('body-128.aseprite',arr(C/'body-128.png'))]:
 q=decode(C/'source'/filename);assert q['durationMs']==35 and delta(q['flat'],im)==0
# Independently reproduce item raster transform for verification only. This
# code does not write or author any production raster.
item=arr(wd['sprite']);pred=np.zeros((256,256,4),dtype=np.uint8);yy,xx=np.mgrid[0:256,0:256];r=np.deg2rad(32);dx=xx-155;dy=yy-114
u=np.floor(np.cos(r)*dx+np.sin(r)*dy+48+.5).astype(int);v=np.floor(-np.sin(r)*dx+np.cos(r)*dy+66+.5).astype(int)
valid=(u>=0)&(u<96)&(v>=0)&(v<96);pred[valid]=item[v[valid],u[valid]]
union=np.where((wf[:,:,3]>0)[:,:,None],wf,wb);assert delta(pred,union)==0
assert not np.any((wb[:,:,3]>0)&(wf[:,:,3]>0))
result={'status':'TECHNICALLY_COMPLETE','scope':'ONE F06 representative only; source/export checks, not anatomical or artistic approval','inputFilesPreserved':len(snap['files']),'bodyVisibleRgbaDelta':0,'handFrontPixels':int((hf[:,:,3]>0).sum()),'handFrontLocalRetouchDelta':9,'handFrontSourceExtent':[152,110,157,117],'bodyAlphaUnchanged':True,'handRetouchExtendsBodySilhouette':False,'durationMs':35,'sourceItemUnchanged':True,'exactIndependentWeaponTransform':'PASS','itemTransform':anatomy['itemTransformProposal'],'allMasterLayerExportComparisons':'PASS','native128CropComplete':True,'opaqueContentOutsideNativeCrop':0,'bodyNativeMasterAndExports':'PASS','celPositions':doc['celPositions'],'compositeDeltaVsRejectedRepair1':delta(flat,arr(old['png'])),'newPixelLabCalls':0,'artisticStatus':'VISUAL_REVIEW_REQUIRED','independentQA':'PENDING_ROOT_SAME_QA','eligibleForIntegration':False}
write(E/'checks.json',result)
master=C/'source/composite.aseprite';bm=C/'source/body-256.aseprite';nm=C/'source/body-128.aseprite'
frame={'index':0,'sourceFrameIndex':6,'durationMs':35,'phase':'slash-release','weaponVisible':True,'rightGrip':[155,114],'rotationDeg':32,'scale':1,'flipBit':False,'png':str(C/'composite-256.png').replace('\\','/'),'sha256':sha(C/'composite-256.png'),'nativePng':str(C/'body-128.png').replace('\\','/'),'nativeSha256':sha(C/'body-128.png'),'compositeNativePng':str(C/'composite-native-128.png').replace('\\','/'),'compositeNativeSha256':sha(C/'composite-native-128.png'),'layers':{n:{'png':str(C/'layers'/(n+'.png')).replace('\\','/'),'sha256':sha(C/'layers'/(n+'.png'))}for n in ['weaponBack','body','weaponFront','handFront']}}
clip={'schemaVersion':1,'revision':'main-orc-combat-rescue-v5-grip-specialist-F06','character':'orc-v1','category':'Sword','direction':'front_r','state':'Attack','representativeOnly':True,'frameCount':1,'sourceFrameIndices':[6],'durationsMs':[35],'totalDurationMs':35,'canvas':[256,256],'nativeCanvas':[128,128],'bodyOffset':[64,64],'groundY':190,'nativeGroundY':126,'ppu':100,'loop':False,'oneShot':True,'terminal':False,'master':str(master).replace('\\','/'),'masterSha256':sha(master),'bodyMaster':str(bm).replace('\\','/'),'bodyMasterSha256':sha(bm),'nativeMaster':str(nm).replace('\\','/'),'nativeMasterSha256':sha(nm),'layerOrder':['weaponBack','body','weaponFront','handFront'],'frames':[frame],'weapon':{k:wd[k]for k in ['id','name','grip','canvas','sprite','master','spriteSha256','masterSha256']},'weaponDefinition':snap['weapon'],'itemTransform':anatomy['itemTransformProposal'],'anatomyEvidence':str(E/'anatomy.json').replace('\\','/'),'sourceParentClip':parentPath,'sourceParentClipSha256':sha(parentPath),'sourceBodyFrame':old['layers']['body'],'sourceTimingClip':parentPath,'technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','artisticApproval':'PENDING_CREATOR','checkpoint':'GRIP_F06_READY','representativeAcceptableForPropagation':False,'propagationPolicy':'DO_NOT_PROPAGATE_UNTIL_SAME_QA_VERDICT_FROM_ROOT','eligibleForIntegration':False,'provenance':{'authoring':'Aseprite Lua; exact source body and item; hand source traced from actual glove plus9 local interior highlight/crease pixels','script':str(E/'author-F06.lua').replace('\\','/'),'scriptSha256':sha(E/'author-F06.lua'),'sourceSnapshot':str(E/'input-snapshot.json').replace('\\','/'),'bodyChoreographyChanged':False,'timingChanged':False,'newPixelLabCalls':0,'runtimeImplemented':False}}
clip['weapon']['definition']=snap['weapon'];write(C/'representative.json',clip)
print(json.dumps(result,indent=2))
