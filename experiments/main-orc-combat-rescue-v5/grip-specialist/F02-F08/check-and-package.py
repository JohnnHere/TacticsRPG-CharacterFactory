from pathlib import Path
from PIL import Image
import json,hashlib,struct,zlib,numpy as np
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/F02-F08');C=Path('characters/orc-v1/source/combat-rescue-v5/grip-specialist')
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def delta(a,b):return int(((a!=b).any(2)&((a[:,:,3]>0)|(b[:,:,3]>0))).sum())
def decode(p):
 data=Path(p).read_bytes();frames,w,h,depth=struct.unpack_from('<HHHH',data,6);assert frames==1 and depth==32
 ms=struct.unpack_from('<H',data,136)[0];n=struct.unpack_from('<H',data,134)[0];n=struct.unpack_from('<I',data,140)[0]or n;off=144;layers=[];cels={}
 for _ in range(n):
  length,typ=struct.unpack_from('<IH',data,off);b=data[off+6:off+length]
  if typ==0x2004:
   flags=struct.unpack_from('<H',b,0)[0];ln=struct.unpack_from('<H',b,16)[0];layers.append({'name':b[18:18+ln].decode('utf8'),'visible':bool(flags&1),'opacity':b[12]})
  elif typ==0x2005:
   li,x,y,op,ct=struct.unpack_from('<HhhBH',b,0);assert ct in [0,2];cw,ch=struct.unpack_from('<HH',b,16);raw=b[20:]if ct==0 else zlib.decompress(b[20:]);cels[li]=(Image.frombytes('RGBA',(cw,ch),raw),x,y,op)
  off+=length
 flat=Image.new('RGBA',(w,h));images={};positions=[]
 for li,l in enumerate(layers):
  im=Image.new('RGBA',(w,h));cel=cels.get(li)
  if cel:
   raw,x,y,op=cel;assert op==255 and l['opacity']==255;im.paste(raw,(x,y));positions.append({'layer':l['name'],'position':[x,y],'imageSize':list(raw.size)})
  if l['visible']:flat=Image.alpha_composite(flat,im)
  images[l['name']]=np.array(im)
 return {'canvas':[w,h],'durationMs':ms,'layers':images,'flat':np.array(flat),'celPositions':positions}
snap=read(E/'input-snapshot.json');assert all(sha(p)==h for p,h in snap['files'].items())
oldFreeze=read(snap['F06Freeze']);assert sha(snap['F06Freeze'])==snap['F06FreezeSha256'];assert all(sha(r['path'])==r['sha256']for r in oldFreeze['files'])
parent=read(snap['parentClip']);wd=read(snap['weaponDefinition']);anatomy=read(E/'anatomy.json');item=arr(wd['sprite']);reports=[]
for idx in [2,8]:
 key=f'F{idx:02}';out=C/key;sourceFrame=parent['frames'][idx];t=anatomy[key]['transform'];doc=decode(out/'source/composite.aseprite')
 assert doc['durationMs']==sourceFrame['durationMs']and doc['canvas']==[256,256]
 assert list(doc['layers'])==['weaponBack','body','weaponFront','handFront']
 flat=arr(out/'composite-256.png');body=arr(out/'layers/body.png');original=arr(sourceFrame['layers']['body']['png']);hf=arr(out/'layers/handFront.png');wb=arr(out/'layers/weaponBack.png');wf=arr(out/'layers/weaponFront.png')
 assert delta(flat,doc['flat'])==0 and delta(body,original)==0
 for name,a in [('weaponBack',wb),('body',body),('weaponFront',wf),('handFront',hf)]:assert delta(a,doc['layers'][name])==0 and np.isin(a[:,:,3],[0,255]).all()
 mask=hf[:,:,3]>0;assert np.all(body[mask,3]==255)and np.array_equal(body[mask],hf[mask])
 yy,xx=np.where(mask);hbox=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]
 assert delta(body[64:192,64:192],arr(out/'body-128.png'))==0
 for filename,pixels in [('body-256.aseprite',body),('body-128.aseprite',arr(out/'body-128.png'))]:
  bodyDoc=decode(out/'source'/filename);assert bodyDoc['durationMs']==sourceFrame['durationMs']and delta(bodyDoc['flat'],pixels)==0
 # Independent transform comparison; diagnostic math only, no output raster.
 py,px=np.mgrid[-96:352,-96:352];rad=np.deg2rad(t['angleDeg']);dx=px-t['bodyGrip'][0];dy=py-t['bodyGrip'][1]
 u=np.floor(np.cos(rad)*dx+np.sin(rad)*dy+48+.5).astype(int);v=np.floor(-np.sin(rad)*dx+np.cos(rad)*dy+66+.5).astype(int);valid=(u>=0)&(u<96)&(v>=0)&(v<96)
 prediction=np.zeros((448,448,4),dtype=np.uint8);prediction[valid]=item[v[valid],u[valid]]
 outsideFull=prediction.copy();outsideFull[96:352,96:352]=0;assert not np.any(outsideFull[:,:,3])
 pred=prediction[96:352,96:352];union=np.where((wf[:,:,3]>0)[:,:,None],wf,wb);assert delta(pred,union)==0 and not np.any((wf[:,:,3]>0)&(wb[:,:,3]>0))
 outside=flat.copy();outside[64:192,64:192]=0;outsideCount=int((outside[:,:,3]>0).sum());nativeComplete=outsideCount==0
 if nativeComplete:
  assert delta(flat[64:192,64:192],arr(out/'composite-native-128.png'))==0
 else:assert not(out/'composite-native-128.png').exists(),'Do not deliver clipped native equipment as intact'
 stats={'key':key,'sourceFrameIndex':idx,'status':'TECHNICALLY_COMPLETE','scope':'One static grip representative; no full-clip/anatomical approval','durationMs':sourceFrame['durationMs'],'bodyRgbaDelta':0,'handFrontSourceOnly':True,'handFrontPixelCount':int(mask.sum()),'handFrontBounds':hbox,'handFrontRetouchPixels':0,'masterLayerBodyNativeChecks':'PASS','itemTransform':t,'itemTransformMatchesSourcePixels':True,'complete256Composite':True,'opaqueEquipmentPixelsOutsideBody128':outsideCount,'nativeComposite128Available':nativeComplete,'nativeBody128Complete':True,'compositeRgbaDeltaVsRejected':delta(flat,arr(sourceFrame['png'])),'celPositions':doc['celPositions'],'artisticStatus':'VISUAL_REVIEW_REQUIRED','eligibleForIntegration':False}
 reports.append(stats)
 master=out/'source/composite.aseprite';bm=out/'source/body-256.aseprite';nm=out/'source/body-128.aseprite'
 frame={'index':0,'sourceFrameIndex':idx,'durationMs':sourceFrame['durationMs'],'phase':sourceFrame['phase'],'weaponVisible':True,'rightGrip':t['bodyGrip'],'rotationDeg':t['angleDeg'],'scale':1,'flipBit':False,'png':str(out/'composite-256.png').replace('\\','/'),'sha256':sha(out/'composite-256.png'),'nativePng':str(out/'body-128.png').replace('\\','/'),'nativeSha256':sha(out/'body-128.png'),'layers':{n:{'png':str(out/'layers'/(n+'.png')).replace('\\','/'),'sha256':sha(out/'layers'/(n+'.png'))}for n in ['weaponBack','body','weaponFront','handFront']}}
 if nativeComplete:frame.update(compositeNativePng=str(out/'composite-native-128.png').replace('\\','/'),compositeNativeSha256=sha(out/'composite-native-128.png'))
 rep={'schemaVersion':1,'revision':'main-orc-combat-rescue-v5-grip-specialist-'+key,'character':'orc-v1','category':'Sword','direction':'front_r','state':'Attack','representativeOnly':True,'frameCount':1,'sourceFrameIndices':[idx],'durationsMs':[sourceFrame['durationMs']],'totalDurationMs':sourceFrame['durationMs'],'canvas':[256,256],'nativeCanvas':[128,128],'nativeEquipmentCompositeAvailable':nativeComplete,'nativeEquipmentNote':'Exact central crop complete'if nativeComplete else'Equipment exceeds body128 canvas; use complete256. Body128 is intact. No weapon shrink or clipped native composite delivered.','bodyOffset':[64,64],'groundY':190,'nativeGroundY':126,'ppu':100,'loop':False,'oneShot':True,'terminal':False,'master':str(master).replace('\\','/'),'masterSha256':sha(master),'bodyMaster':str(bm).replace('\\','/'),'bodyMasterSha256':sha(bm),'nativeMaster':str(nm).replace('\\','/'),'nativeMasterSha256':sha(nm),'layerOrder':['weaponBack','body','weaponFront','handFront'],'frames':[frame],'weapon':{k:wd[k]for k in ['id','name','grip','canvas','sprite','master','spriteSha256','masterSha256']},'weaponDefinition':snap['weaponDefinition'],'itemTransform':t,'anatomyEvidence':str(E/'anatomy.json').replace('\\','/'),'sourceParentClip':snap['parentClip'],'sourceParentClipSha256':sha(snap['parentClip']),'sourceBodyFrame':sourceFrame['layers']['body'],'technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','artisticApproval':'PENDING_CREATOR','checkpoint':'GRIP_F02_F08_READY','representativeAcceptableForPropagation':False,'propagationPolicy':'DO_NOT_PROPAGATE_UNTIL_ROOT_GLM5.3_CLINE_QA','eligibleForIntegration':False,'provenance':{'authoring':'Aseprite Lua; exact source body/item; per-pose source-glove rows, no new hand pixels or fixed palm','script':str(E/'author-keys.lua').replace('\\','/'),'scriptSha256':sha(E/'author-keys.lua'),'sourceSnapshot':str(E/'input-snapshot.json').replace('\\','/'),'bodyChoreographyChanged':False,'timingChanged':False,'newPixelLabCalls':0,'runtimeImplemented':False}}
 write(out/'representative.json',rep)
result={'status':'TECHNICALLY_COMPLETE','scope':'Only front_r/Sword F02 and F08 representatives','inputsPreserved':len(snap['files']),'originalF06FreezePreserved':True,'originalF06FilesPreserved':len(oldFreeze['files']),'newPixelLabCalls':0,'nextIndependentQA':'Root-owned GLM5.3/Cline; not run by DEV','representatives':reports}
write(E/'checks.json',result);print(json.dumps(result,indent=2))
