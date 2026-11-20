from pathlib import Path
from PIL import Image
import json,hashlib,struct,zlib,numpy as np
E=Path('experiments/main-orc-combat-rescue-v5/grip-specialist/full-front-r-sword');C=Path('characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword');BASE=C.parent
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def delta(a,b):return int(((a!=b).any(2)&((a[:,:,3]>0)|(b[:,:,3]>0))).sum())
def decode(p):
 data=Path(p).read_bytes();count,w,h,depth=struct.unpack_from('<HHHH',data,6);assert depth==32
 layers=[];cels={};frames=[];durations=[];positions=[];pos=128
 for fi in range(count):
  length,magic,n=struct.unpack_from('<IHH',data,pos);assert magic==0xf1fa;durations.append(struct.unpack_from('<H',data,pos+8)[0]);n=struct.unpack_from('<I',data,pos+12)[0]or n;off=pos+16
  for _ in range(n):
   size,typ=struct.unpack_from('<IH',data,off);b=data[off+6:off+size]
   if typ==0x2004:
    flags=struct.unpack_from('<H',b,0)[0];ln=struct.unpack_from('<H',b,16)[0];layers.append({'name':b[18:18+ln].decode('utf8'),'visible':bool(flags&1),'opacity':b[12]})
   elif typ==0x2005:
    li,x,y,op,ct=struct.unpack_from('<HhhBH',b,0)
    if ct in [0,2]:
     cw,ch=struct.unpack_from('<HH',b,16);raw=b[20:]if ct==0 else zlib.decompress(b[20:]);im=Image.frombytes('RGBA',(cw,ch),raw)
    elif ct==1:
     linked=struct.unpack_from('<H',b,16)[0];im=cels[(linked,li)][0].copy()
    else:raise AssertionError('Unsupported cel')
    cels[(fi,li)]=(im,x,y,op);positions.append({'frame':fi,'layer':layers[li]['name'],'position':[x,y],'imageSize':list(im.size),'celType':ct})
   off+=size
  flat=Image.new('RGBA',(w,h));ims={}
  for li,l in enumerate(layers):
   im=Image.new('RGBA',(w,h));cel=cels.get((fi,li))
   if cel:
    raw,x,y,op=cel;assert op==255 and l['opacity']==255;im.paste(raw,(x,y))
   if l['visible']:flat=Image.alpha_composite(flat,im)
   ims[l['name']]=np.array(im)
  frames.append({'flat':np.array(flat),'layers':ims});pos+=length
 return {'canvas':[w,h],'durationsMs':durations,'frames':frames,'positions':positions}
snap=read(E/'input-snapshot.json');assert all(sha(p)==h for p,h in snap['files'].items())
preserved=0
for fp,h in snap['preservedFreezes'].items():
 assert sha(fp)==h;f=read(fp);assert all(sha(r['path'])==r['sha256']for r in f['files']);preserved+=len(f['files'])
parent=read(snap['parentClip']);anatomy=read(E/'anatomy.json');wd=read(snap['weaponDefinition']);item=arr(wd['sprite'])
docs={part:decode(C/'source'/name)for part,name in [('composite','composite.aseprite'),('body','body.aseprite'),('native','native.aseprite'),('hand','hand.aseprite')]}
assert all(d['durationsMs']==parent['durationsMs']for d in docs.values())and sum(parent['durationsMs'])==730
nativeStrip=arr(C/'native-strip.png');compositeStrip=arr(C/'composite-strip.png');assert nativeStrip.shape==(128,1664,4)and compositeStrip.shape==(256,3328,4)
records=[];frames=[]
for i,old in enumerate(parent['frames']):
 cfg=anatomy['frames'][i];n=f'{i:02}.png';flat=arr(C/n);body=arr(C/'layers/body'/n);hf=arr(C/'layers/handFront'/n);wb=arr(C/'layers/weaponBack'/n);wf=arr(C/'layers/weaponFront'/n);native=arr(C/'native'/n)
 assert delta(body,arr(old['layers']['body']['png']))==0 and delta(body[64:192,64:192],native)==0
 assert all(np.isin(a[:,:,3],[0,255]).all()for a in [flat,body,hf,wb,wf])
 assert delta(docs['composite']['frames'][i]['flat'],flat)==0
 for name,im in [('weaponBack',wb),('body',body),('weaponFront',wf),('handFront',hf)]:assert delta(docs['composite']['frames'][i]['layers'][name],im)==0
 assert delta(docs['body']['frames'][i]['flat'],body)==0 and delta(docs['native']['frames'][i]['flat'],native)==0 and delta(docs['hand']['frames'][i]['flat'],hf)==0
 assert delta(nativeStrip[:,i*128:(i+1)*128],native)==0 and delta(compositeStrip[:,i*256:(i+1)*256],flat)==0
 handMask=hf[:,:,3]>0;assert np.all(body[handMask,3]>0)
 bodyHandOnly=np.where(handMask[:,:,None],body,0).astype('uint8');handRetouch=delta(hf,bodyHandOnly)
 record={'index':i,'durationMs':old['durationMs'],'bodyRgbaDelta':0,'weaponVisible':cfg['weaponVisible'],'handFrontPixels':int(handMask.sum()),'handRetouchPixels':handRetouch}
 if cfg['weaponVisible']:
  assert i in range(2,11)and handMask.any()
  gx,gy=cfg['grip'];angle=cfg['angleDeg'];r=np.deg2rad(angle);yy,xx=np.mgrid[-96:352,-96:352];dx=xx-gx;dy=yy-gy
  u=np.floor(np.cos(r)*dx+np.sin(r)*dy+48+.5).astype(int);v=np.floor(-np.sin(r)*dx+np.cos(r)*dy+66+.5).astype(int);valid=(u>=0)&(u<96)&(v>=0)&(v<96)
  pred=np.zeros((448,448,4),dtype=np.uint8);pred[valid]=item[v[valid],u[valid]];outside=pred.copy();outside[96:352,96:352]=0;assert not np.any(outside[:,:,3])
  union=np.where((wf[:,:,3]>0)[:,:,None],wf,wb);assert delta(pred[96:352,96:352],union)==0 and not np.any((wf[:,:,3]>0)&(wb[:,:,3]>0))
  if 'reuseRepresentative'in cfg:
   rep=read(BASE/cfg['reuseRepresentative']/'representative.json');rf=rep['frames'][0];assert delta(flat,arr(rf['png']))==0
   for name in ['weaponBack','body','weaponFront','handFront']:assert delta(arr(C/'layers'/name/n),arr(rf['layers'][name]['png']))==0
   record['validatedRepresentativeReusedExact']=cfg['reuseRepresentative']
  else:assert handRetouch==0
  record['grip']=cfg['grip'];record['angleDeg']=angle;record['unwrappedAngleDeg']=cfg['unwrappedAngleDeg']
  sy,sx=np.where(union[:,:,3]>0);record['weaponBbox']=[int(sx.min()),int(sy.min()),int(sx.max()),int(sy.max())]
 else:
  assert not np.any(wb[:,:,3])and not np.any(wf[:,:,3])and not handMask.any();assert delta(flat,body)==0
 records.append(record)
 frame={**{k:old[k]for k in ['index','durationMs','phase']},'png':str(C/n).replace('\\','/'),'sha256':sha(C/n),'nativePng':str(C/'native'/n).replace('\\','/'),'nativeSha256':sha(C/'native'/n),'weaponVisible':cfg['weaponVisible'],'rightGrip':cfg.get('grip'),'rotationDeg':cfg.get('angleDeg'),'unwrappedAngleDeg':cfg.get('unwrappedAngleDeg'),'scale':1,'flipBit':False,'handSource':'No overlay outsideAttack'if not cfg['weaponVisible']else('Exact validated '+cfg['reuseRepresentative']+' layers'if'reuseRepresentative'in cfg else'Individually traced source-glove pixels from this exact body frame; no fixed palm or new cuff'),'layers':{name:{'png':str(C/'layers'/name/n).replace('\\','/'),'sha256':sha(C/'layers'/name/n)}for name in ['weaponBack','body','weaponFront','handFront']}}
 frames.append(frame)
master=C/'source/composite.aseprite';bm=C/'source/body.aseprite';nm=C/'source/native.aseprite';hm=C/'source/hand.aseprite'
clip={'schemaVersion':1,'revision':'main-orc-combat-rescue-v5-grip-specialist-full-front-r-sword','id':'basic.sword-slash','character':'orc-v1','category':'Sword','state':'Attack','direction':'front_r','frameCount':13,'durationsMs':parent['durationsMs'],'totalDurationMs':730,'canvas':[256,256],'nativeCanvas':[128,128],'bodyOffset':[64,64],'groundY':190,'nativeGroundY':126,'ppu':100,'loop':False,'oneShot':True,'terminal':False,'master':str(master).replace('\\','/'),'masterSha256':sha(master),'bodyMaster':str(bm).replace('\\','/'),'bodyMasterSha256':sha(bm),'nativeMaster':str(nm).replace('\\','/'),'nativeMasterSha256':sha(nm),'handMaster':str(hm).replace('\\','/'),'handMasterSha256':sha(hm),'strip':str(C/'native-strip.png').replace('\\','/'),'stripSha256':sha(C/'native-strip.png'),'nativeStrip':str(C/'native-strip.png').replace('\\','/'),'nativeStripSha256':sha(C/'native-strip.png'),'compositeStrip':str(C/'composite-strip.png').replace('\\','/'),'compositeStripSha256':sha(C/'composite-strip.png'),'layerOrder':['weaponBack','body','weaponFront','handFront'],'frames':frames,'weapon':{k:wd[k]for k in ['id','name','grip','canvas','sprite','master','spriteSha256','masterSha256']},'weaponDefinition':snap['weaponDefinition'],'visibilityPolicy':'attack-only-v1','visibleInterval':[2,10],'hideAfterAction':True,'weaponDepthPolicy':'Grip leather v60..70 behind body; blade/guard/pommel front; per-frame original glove in handFront','contactEvent':parent.get('contactEvent'),'technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','artisticApproval':'PENDING_CREATOR','eligibleForIntegration':False,'checkpoint':'GRIP_FRONT_R_SWORD_FULL_READY','fullClipIndependentQA':'PENDING_ROOT_SOL_CODEX_NO_COPILOT','sourceParentClip':snap['parentClip'],'sourceParentClipSha256':sha(snap['parentClip']),'provenance':{'authoring':'Aseprite Lua only. Exact validated F02/F06/F08 layers retained; other6 visible gloves traced separately on original body; no body/timing change.','script':str(E/'author.lua').replace('\\','/'),'scriptSha256':sha(E/'author.lua'),'anatomy':str(E/'anatomy.json').replace('\\','/'),'inputSnapshot':str(E/'input-snapshot.json').replace('\\','/'),'bodyRgbaChanged':False,'timingChanged':False,'newPixelLabCalls':0,'runtimeImplemented':False},'reuseAssessment':{'body':'REUSE_DIRECT exact13 body poses/times','item':'REUSE_DIRECT exact independent Sword','validatedKeys':'REUSE_DIRECT exact F02/F06/F08 layers','remainingBindings':'REUSE_ADAPTED per-pose observed glove and wrist orientation','risk':'Full-cycle grip/occlusion/wrist trajectory and tactical-scale motion need independent QA; static key verdicts do not approve the cycle'}}
clip['weapon'].update(definition=snap['weaponDefinition'],source=wd['master'],sourceSha256=wd['masterSha256'],scale=1)
clip['fullClipIndependentQA']='PENDING_ROOT_NO_COPILOT'
write(C/'clip.json',clip)
result={'status':'TECHNICALLY_COMPLETE','scope':'ONLY full front_r/Sword13f/730ms; not other grips or matrix','frameCount':13,'durationMs':730,'allBodyRgbaDelta':0,'sourceItemUnchanged':True,'savedMastersAndExportsMatch':True,'stripsMatchFrames':True,'nativePngContract':'Exact BODY crop64,64 size128; equipment always complete256','hiddenFrames':[0,1,11,12],'visibleFrames':list(range(2,11)),'validatedKeyLayersExact':[2,6,8],'priorFrozenFilesPreserved':preserved,'inputFilesPreserved':len(snap['files']),'newPixelLabCalls':0,'frames':records,'celPositions':{k:d['positions']for k,d in docs.items()},'artisticStatus':'VISUAL_REVIEW_REQUIRED','fullCycleArtisticQA':'PENDING_ROOT','eligibleForIntegration':False}
write(E/'checks.json',result);print(json.dumps({'status':result['status'],'frameCount':13,'durationMs':730,'bodyRgbaDelta':0,'keyLayersReusedExact':[2,6,8],'preservedFrozenFiles':preserved,'inputsPreserved':len(snap['files']),'frames':records},indent=2))
