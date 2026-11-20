from pathlib import Path
from PIL import Image, ImageChops, ImageDraw
import json,hashlib,struct
E=Path('experiments/main-orc-backl-v5base'); configs=json.loads((E/'author-config.json').read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rgba(p):return Image.open(p).convert('RGBA')
def equal(a,b):
 def canonical(im):return bytes(v for px in im.getdata() for v in (px if px[3] else (0,0,0,0)))
 return canonical(a)==canonical(b)
def shift(im,dx,dy):
 r=Image.new('RGBA',(256,256));r.paste(im,(dx,dy));return r
def entry(p):return {'png':str(p).replace('\\','/'),'sha256':sha(p)}
def ase_times(p):
 data=Path(p).read_bytes();count=struct.unpack_from('<H',data,6)[0];pos=128;ds=[]
 for i in range(count):
  size,magic,chunks,duration=struct.unpack_from('<IHHH',data,pos);assert magic==0xf1fa;ds.append(duration);pos+=size
 return ds
checks=[]; pose=['# Mapa semântico v5 → grade atual\n\nÍndices F00 são zero-based. Corpo completo v5; sem transplante de membros. Translações são inteiras em X, mantendo todos os pixels da mão.\n']; protected={}; decisions=[]
for c in configs:
 n=c['name'];out=E/n; before=json.loads(Path(c['beforeClip']).read_text(encoding='utf-8-sig'));(E/'before-after'/n).mkdir(parents=True,exist_ok=True);(E/'hands-8x'/n).mkdir(parents=True,exist_ok=True)
 pose+=['\n## '+c['category']+'\n\nFonte corporal: `'+c['bodySource']+'`.\n\n| Alvo | Fase | Fonte v5 | Operação | Motivo |\n|---|---|---|---|---|\n'];frames=[];pairs=[];prev=None;all_hand=True;cropped=[]
 for f in c['frames']:
  i=f['index'];fn=f'{i:02}.png';body=rgba(out/'layers/body'/fn);src=rgba(f['sourceBody']);assert equal(body,shift(src,f['dx'],f['dy'])),(n,i,'body')
  protected[f['sourceBody']]=sha(f['sourceBody']); layers={k:rgba(out/'layers'/k/fn) for k in ['weaponBack','body','weaponFront','handFront']};comp=Image.new('RGBA',(256,256))
  for im in layers.values():comp=Image.alpha_composite(comp,im)
  actual=rgba(out/'frames'/fn);assert equal(comp,actual),(n,i,'composition')
  assert equal(rgba(out/'native'/fn),actual.crop((64,64,192,192)))
  for k,im in layers.items():assert set(im.getchannel('A').getdata()).issubset({0,255})
  if not f['weaponVisible']:
   for k in ['weaponBack','weaponFront','handFront']:assert layers[k].getbbox() is None
  else:
   assert layers['weaponBack'].getbbox() or layers['weaponFront'].getbbox()
   if prev is not None and prev[0] and actual.tobytes()==prev[1]:pairs.append([i-1,i])
   hf=layers['handFront'];bbox=hf.getbbox();assert bbox is not None
   if n=='sword':
    for y in range(256):
     for x in range(256):
      if hf.getpixel((x,y))[3]:assert hf.getpixel((x,y))==body.getpixel((x,y))==actual.getpixel((x,y))
   else:
    for k in ['weaponBack','weaponFront','handFront']:
     p=f['sourceLayers'][k]['png'];protected[p]=sha(p);assert equal(layers[k],shift(rgba(p),f['dx'],f['dy']))
    for y in range(bbox[1],bbox[3]):
     for x in range(bbox[0],bbox[2]):
      if hf.getpixel((x,y))[3]:assert hf.getpixel((x,y))==actual.getpixel((x,y))
   box=(bbox[0]-3,bbox[1]-3,bbox[2]+3,bbox[3]+3)
   donor=shift(src,f['dx'],f['dy']) if n=='sword' else shift(rgba(Path(c['bodySource'])/f'{f["sourceIndex"]:02}.png'),f['dx'],f['dy'])
   donorbox=(box[0]-f['dx'],box[1],box[2]-f['dx'],box[3]); donor=src if n=='sword' else rgba(Path(c['bodySource'])/f'{f["sourceIndex"]:02}.png')
   ims=[donor.crop(donorbox),body.crop(box),actual.crop(box)];w=(box[2]-box[0])*8;h=(box[3]-box[1])*8
   sheet=Image.new('RGB',(w*3,h+30),(55,60,68));d=ImageDraw.Draw(sheet)
   for j,(im,label) in enumerate(zip(ims,['v5 original','corpo layers-off','composto'])):
    im=im.resize((w,h),Image.Resampling.NEAREST);sheet.paste(im,(j*w,30),im);d.text((j*w+3,7),label)
   sheet.save(E/'hands-8x'/n/fn)
   outside=actual.copy();outside.paste((0,0,0,0),(64,64,192,192));lost=sum(a>0 for a in outside.getchannel('A').getdata())
   if lost:cropped.append({'frame':i,'opaquePixelsOutsideNative':lost})
  prev=(f['weaponVisible'],actual.tobytes())
  oldf=before['frames'][i];oldp=oldf.get('png') or oldf.get('compositePng');oldp=oldp.get('path') if isinstance(oldp,dict) else oldp
  old=rgba(oldp);assert old.size==(256,256),(oldp,old.size)
  sheet=Image.new('RGBA',(512,256));sheet.paste(old,(0,0));sheet.paste(actual,(256,0));sheet.save(E/'before-after'/n/fn)
  frames.append({**f,**entry(out/'frames'/fn),'layers':{k:entry(out/'layers'/k/fn)for k in layers},'nativePng':str(out/'native'/fn).replace('\\','/'),'sourceBodySha256':sha(f['sourceBody'])})
  pose.append(f'| F{i:02} | {f["phase"]} | F{f["sourceIndex"]:02} | {f["operation"]} | {f["reason"]} |\n')
 assert not pairs
 bytepairs=[[i-1,i] for i in range(1,len(c['frames'])) if c['frames'][i-1]['weaponVisible'] and c['frames'][i]['weaponVisible'] and sha(out/'frames'/f'{i-1:02}.png')==sha(out/'frames'/f'{i:02}.png')]
 assert not bytepairs
 for master in ['composite','body','native']:assert ase_times(out/'source'/f'{master}.aseprite')==c['durationsMs']
 clip={'schemaVersion':1,'revision':'main-orc-backl-v5base','character':'orc-v1','direction':'back_l','category':c['category'],'state':'Attack','canvas':[256,256],'nativeCanvas':[128,128],'bodyOffset':[64,64],'groundY':190,'nativeGroundY':126,'loop':False,'oneShot':True,'frameCount':len(frames),'durationsMs':c['durationsMs'],'totalDurationMs':sum(c['durationsMs']),'visibleInterval':c['visibleInterval'],'contactEvent':c['contactEvent'],'layerOrder':list(layers),'technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','artisticApproval':'PENDING_CREATOR','runtimeImplemented':False,'propagationAllowed':False,'paidGenerations':0,'weaponDefinition':c['weaponDefinition'],'beforeClip':c['beforeClip'],'frames':frames}
 for field,file in [('master','source/composite.aseprite'),('bodyMaster','source/body.aseprite'),('nativeMaster','source/native.aseprite'),('compositeStrip','composite-strip.png'),('nativeStrip','native-strip.png')]:clip[field]=str(out/file).replace('\\','/');clip[field+'Sha256']=sha(out/file)
 (out/'clip.json').write_text(json.dumps(clip,indent=2,ensure_ascii=False),encoding='utf-8')
 checks.append({'category':c['category'],'frameCount':len(frames),'durationsMs':c['durationsMs'],'phases':c['phases'],'totalDurationMs':sum(c['durationsMs']),'contactEvent':c['contactEvent'],'visibleInterval':c['visibleInterval'],'needsDecisionFrames':[f['index'] for f in c['frames'] if f.get('decisionStatus')=='NEEDS_DECISION'],'armedIdenticalAdjacentBytePairs':bytepairs,'armedIdenticalAdjacentPairs':pairs,'armedIdenticalAdjacentPairCount':len(pairs),'bodySourcePixelsExactAfterDeclaredTranslation':True,'handPixelsPreserved':True,'compositionExact':True,'savedMasterDurationsVerified':True,'nativeIsExactCrop':True,'nativeCropClipping':cropped})
(E/'pose-map.md').write_text(''.join(pose),encoding='utf-8');(E/'temporal-check.json').write_text(json.dumps({'technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','clips':checks},indent=2),encoding='utf-8');(E/'source-hashes.json').write_text(json.dumps(protected,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False))

