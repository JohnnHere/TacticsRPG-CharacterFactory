from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,struct,zlib,numpy as np
E=Path('experiments/main-orc-rear-reconstruction-v4/specialist');R=E/'recovery'
C=Path('characters/orc-v1/source/rear-reconstruction-v4-specialist/impact-recovered')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def delta(a,b):return int(((a!=b).any(2)&((a[:,:,3]>0)|(b[:,:,3]>0))).sum())
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
master=C/'impact-recovered.aseprite';data=master.read_bytes()
count,w,h,depth=struct.unpack_from('<HHHH',data,6);assert(count,w,h,depth)==(1,128,128,32)
ms=struct.unpack_from('<H',data,136)[0];assert ms==80
chunkCount=struct.unpack_from('<H',data,134)[0];chunkCount=struct.unpack_from('<I',data,140)[0]or chunkCount
off=144;layers=[];cels={}
for _ in range(chunkCount):
 length,typ=struct.unpack_from('<IH',data,off);b=data[off+6:off+length]
 if typ==0x2004:
  flags=struct.unpack_from('<H',b,0)[0];nameLen=struct.unpack_from('<H',b,16)[0];layers.append({'name':b[18:18+nameLen].decode('utf8'),'visible':bool(flags&1),'opacity':b[12]})
 elif typ==0x2005:
  li,x,y,op,ct=struct.unpack_from('<HhhBH',b,0);assert ct in [0,2];cw,ch=struct.unpack_from('<HH',b,16)
  buf=b[20:]if ct==0 else zlib.decompress(b[20:]);cels[li]=(Image.frombytes('RGBA',(cw,ch),buf),x,y,op)
 off+=length
full=Image.new('RGBA',(128,128));body=Image.new('RGBA',(128,128));proof=[]
for li,l in enumerate(layers):
 im=Image.new('RGBA',(128,128));cel=cels.get(li)
 if cel:
  raw,x,y,op=cel;assert op==255 and l['opacity']==255;im.paste(raw,(x,y))
 assert delta(np.array(im),arr(C/(l['name']+'.png')))==0
 if l['visible']:full=Image.alpha_composite(full,im)
 if l['name']not in ['weaponBack','weaponFront','handFront']:body=Image.alpha_composite(body,im)
 proof.append({'name':l['name'],'occupiedPixels':int((np.array(im)[:,:,3]>0).sum()),'position':[cel[1],cel[2]]if cel else None,'savedCelMatchesExport':True})
assert delta(np.array(full),arr(C/'impact-recovered-equipped.png'))==0
assert delta(np.array(body),arr(C/'impact-recovered-body.png'))==0
priorE=E/'iter';newBody=arr(C/'impact-recovered-body.png');newEq=arr(C/'impact-recovered-equipped.png')
assert delta(newBody,arr(priorE/'iter02-body.png'))==0
assert delta(newEq,arr(priorE/'iter02-equipped.png'))==0
retained=read(R/'retained-partial-inventory.json');assert all(sha(p)==h for p,h in retained.items())
originalFreeze=read('experiments/main-orc-rear-reconstruction-v4/dev/version-freeze.json')
assert all(sha(r['path'])==r['sha256']for r in originalFreeze['files'])
parent=read('characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/clip.json')
assert sha(parent['nativeMaster'])==parent['nativeMasterSha256']
assert delta(arr(parent['frames'][5]['nativePng']),arr(C/'source-F05.png'))==0
out=Image.new('RGB',(1024,580),(43,44,49));d=ImageDraw.Draw(out)
for col,(label,fp,native)in enumerate([('Current F04',parent['frames'][4]['png'],False),('Current F05',parent['frames'][5]['png'],False),('Prepared alternate F05',str(C/'impact-recovered-equipped.png'),True),('Current F06',parent['frames'][6]['png'],False)]):
 im=Image.open(fp).convert('RGBA');x=col*256
 out.paste(im,(x+64,24+64)if native else(x,24),im);d.text((x+4,5),label,fill='white')
for col,(label,fp)in enumerate([('Current F05 body',parent['frames'][5]['nativePng']),('Alternate F05 body',str(C/'impact-recovered-body.png'))]):
 im=Image.open(fp).convert('RGBA').resize((256,256),Image.Resampling.NEAREST);out.paste(im,(col*256,316),im);d.text((col*256+4,294),label,fill='white')
detail=Image.open(C/'impact-recovered-equipped.png').convert('RGBA').crop((78,40,124,84)).resize((276,264),Image.Resampling.NEAREST)
out.paste(detail,(600,310),detail);d.text((600,292),'Alternate shoulder / elbow / grip',fill='white');out.save(R/'pose-vs-neighbors.png')
result={'scope':'ONE prepared alternative back_r/Axe F05; deterministic script recovery only','asepriteExecutionsInRecovery':1,'syntaxAndInputChecks':'PASS','masterFrameCount':1,'canvas':[128,128],'sourceSlotDurationMs':ms,'masterToLayerBodyCompositeExports':'PASS','layers':proof,'newVsPreparedIter02BodyRgbaDelta':0,'newVsPreparedIter02EquippedRgbaDelta':0,'alternateVsCurrentF05BodyRgbaDelta':delta(newBody,arr(C/'source-F05.png')),'retainedPartialFilesPreserved':len(retained),'originalDiagnosticFreezeFilesUnchanged':len(originalFreeze['files']),'originalDiagnosticFreezeSha256':sha('experiments/main-orc-rear-reconstruction-v4/dev/version-freeze.json'),'masterSha256':sha(master),'newGenerationCalls':0,'artisticStatus':'NOT_VERIFIED_PENDING_LOCAL_INSPECTION','eligibleForIntegration':False}
write(R/'checks.json',result);print(json.dumps(result,indent=2))
