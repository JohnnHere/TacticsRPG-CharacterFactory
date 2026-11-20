from pathlib import Path
from PIL import Image
import numpy as np
import json,hashlib,copy,struct,zlib
E=Path('experiments/main-orc-rear-reconstruction-v4/dev')
C=Path('characters/orc-v1/source/rear-reconstruction-v4')
REV='main-orc-rear-reconstruction-v4'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def raster(p):return np.array(Image.open(p).convert('RGBA'))
def diff(a,b):return int(((a!=b).any(2)&((a[:,:,3]>0)|(b[:,:,3]>0))).sum())
def same(a,b):return a.shape==b.shape and diff(a,b)==0
def ase(p):
 """Independent read-only RGB raster decoder; respects trimmed cel positions."""
 data=Path(p).read_bytes();count,w,h,depth=struct.unpack_from('<HHHH',data,6)
 assert depth==32
 layers=[];frames=[];duration=[];pos=128;celdata={};positions=[]
 for fi in range(count):
  size,magic,n=struct.unpack_from('<IHH',data,pos);assert magic==0xf1fa
  ms=struct.unpack_from('<H',data,pos+8)[0];duration.append(ms)
  n2=struct.unpack_from('<I',data,pos+12)[0];n=n2 or n
  off=pos+16
  for _ in range(n):
   length,typ=struct.unpack_from('<IH',data,off);body=data[off+6:off+length]
   if typ==0x2004:
    flags,ltype,child=struct.unpack_from('<HHH',body,0);opacity=body[12];nl=struct.unpack_from('<H',body,16)[0];name=body[18:18+nl].decode('utf8')
    layers.append({'name':name,'visible':bool(flags&1),'opacity':opacity,'type':ltype})
   elif typ==0x2005:
    li,x,y,op,ct=struct.unpack_from('<HhhBH',body,0)
    if ct in [0,2]:
     cw,ch=struct.unpack_from('<HH',body,16);buf=body[20:] if ct==0 else zlib.decompress(body[20:]);im=Image.frombytes('RGBA',(cw,ch),buf)
    elif ct==1:
     linked=struct.unpack_from('<H',body,16)[0];im=celdata[(linked,li)][0].copy()
    else:raise AssertionError(f'Unsupported cel {ct}')
    celdata[(fi,li)]=(im,x,y,op);positions.append({'frame':fi,'layer':li,'position':[x,y],'imageSize':list(im.size),'celType':ct})
   off+=length
  out=Image.new('RGBA',(w,h))
  for li,l in enumerate(layers):
   if not l['visible'] or (fi,li)not in celdata:continue
   im,x,y,op=celdata[(fi,li)];assert op==255 and l['opacity']==255
   canvas=Image.new('RGBA',(w,h));canvas.paste(im,(x,y));out=Image.alpha_composite(out,canvas)
  frames.append(np.array(out));pos+=size
 return {'frames':frames,'durationsMs':duration,'layers':layers,'positions':positions,'canvas':[w,h]}
inventory=read(E/'input-inventory.json');oldm=read(E/'input-manifest.json');clips=read(E/'input-clips.json')
registrations=read(E/'weapon-registration.json');reg={(r['cellId'],r['frame']):r for r in registrations}
scalp={r['frame']:r['points']for r in read(E/'scalp-outline-points.json')['frames']}
composition=read(E/'material-composition-evidence.json')
proof={'scope':'Focused weapon materials and explicit back_r scalp contour only; no artistic motion PASS','inputFiles':len(inventory),'inputDrift':[],'weaponSources':[],'clips':[],'failures':[]}
for p,h in inventory.items():
 if sha(p)!=h:proof['inputDrift'].append(p)
assert not proof['inputDrift']
defs={}
for cat,id in [('Axe','militia-axe'),('Sword','recruit-sword')]:
 old=read(Path('assets/weapons')/id/'weapon.json');new=copy.deepcopy(old)
 d=C/'weapons'/cat;master=str(d/(id+'.aseprite')).replace('\\','/');sprite=str(d/(id+'.png')).replace('\\','/')
 a,b=raster(old['sprite']),raster(sprite);assert np.array_equal(a[:,:,3],b[:,:,3])
 doc=ase(master);assert len(doc['frames'])==1 and same(doc['frames'][0],b)
 new.update(revision=REV,master=master,sprite=sprite,sourceSha256=sha(master),masterSha256=sha(master),spriteSha256=sha(sprite),script=str(E/'author-weapons.lua').replace('\\','/'),parentWeaponDefinition=str(Path('assets/weapons')/id/'weapon.json').replace('\\','/'),parentMaster=old['master'],parentMasterSha256=sha(old['master']),artisticStatus='VISUAL_REVIEW_REQUIRED',artisticApproval='PENDING_CREATOR',authoring='Inherited PixelLab weapon; bounded material clusters authored via Aseprite Lua; no new generation',bindings='Associated with the 4 material-only clip forks in this isolated candidate; choreography/grip unchanged')
 new['compatibility']={**old['compatibility'],'directions':['front_r','front_l','back_r','back_l'],'direction':'per-frame registered; no geometry change'}
 write(d/'weapon.json',new);defs[cat]=str(d/'weapon.json').replace('\\','/')
 proof['weaponSources'].append({'category':cat,'changedRgbaPixels':diff(a,b),'alphaUnchanged':True,'gripUnchanged':old['grip']==new['grip'],'canvasUnchanged':list(b.shape[:2])==[96,96],'freshMasterPixelsMatch':True,'master':master,'sprite':sprite,'layers':doc['layers']})
newm=copy.deepcopy(oldm)
newm.update(manifestId='orc-v1.rear-reconstruction-v4.candidate28',revision=REV,parentManifest='characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json',parentManifestSha256=sha('characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json'),integrationReport='experiments/main-orc-rear-reconstruction-v4/orchestration-report.md',technicalStatus='NOT_VERIFIED',artisticStatus='ARTISTIC_REVISION_REQUIRED',artisticApproval='PENDING_CREATOR',eligibleForIntegration=False,integrationStatus='PARTIAL_MATERIAL_AND_SCALP_REFINEMENT_DO_NOT_PROMOTE',weaponDefinitions=defs,runtimeImplemented=False,scope='8 weapon material forks plus bounded back_r scalp contour correction / 20 truthful aliases. Rear choreography and grip objective remain unresolved. Rejected keypose excluded.',devReport=str(E/'report.md').replace('\\','/'))
for cell in newm['cells']:
 key=cell['cellId'];old=clips[key];cat=cell['action']
 cell['parentCell']={'manifest':newm['parentManifest'],'cellId':key,'clipJson':cell['clipJson'],'clipSha256':sha(cell['clipJson'])}
 if cat not in ['Sword','Axe']:
  cell.update(status='UNCHANGED_ALIAS',isAffected=False,reviewStatus='UNCHANGED_RELATIVE_TO_SESSION_INPUT',notes='Exact prior-candidate clip alias; no art, metadata or timing change in this session',provenance='main-orc-targeted-recovery-v3 exact current input')
  continue
 out=C/key;p=copy.deepcopy(old)
 master=str(out/'source/composite.aseprite').replace('\\','/');bodyMaster=str(out/'source/body.aseprite').replace('\\','/');nativeMaster=str(out/'source/native.aseprite').replace('\\','/')
 p.update(revision=REV,master=master,masterSha256=sha(master),bodyMaster=bodyMaster,bodyMasterSha256=sha(bodyMaster),nativeMaster=nativeMaster,nativeMasterSha256=sha(nativeMaster),nativeCanvas=[128,128],nativeGroundY=126,bodyOffset=[64,64],strip=str(out/'native-strip.png').replace('\\','/'),compositeStrip=str(out/'composite-strip.png').replace('\\','/'),visibilityPolicy='attack-only-v1',hideAfterAction=True,parentClip=cell['clipJson'],parentClipSha256=sha(cell['clipJson']),technicalStatus='TECHNICALLY_COMPLETE',artisticStatus='ARTISTIC_REVISION_REQUIRED'if cell['direction'].startswith('back')else'VISUAL_REVIEW_REQUIRED',artisticApproval='PENDING_CREATOR',eligibleForIntegration=False,integrationStatus='ISOLATED_WEAPON_MATERIAL_ONLY_REAR_CHOREOGRAPHY_UNRESOLVED')
 p['integrationStatus']='ISOLATED_MATERIAL_AND_SCALP_REFINEMENT_RECONSTRUCTION_UNRESOLVED'
 p.pop('reviewEvidence',None)
 wd=read(defs[cat]);p['weapon']={k:wd[k]for k in ['id','name','grip','canvas','sprite','master','spriteSha256','masterSha256']};p['weapon'].update(source=wd['master'],sourceSha256=wd['masterSha256'],definition=defs[cat],scale=1)
 p['provenance']={'parentClip':cell['clipJson'],'parentMaster':old['master'],'parentMasterSha256':sha(old['master']),'authoringScript':str(E/'compose-material-forks.lua').replace('\\','/'),'weaponArtScript':str(E/'author-weapons.lua').replace('\\','/'),'paidGenerationCalls':0,'bodyArtChanged':cell['direction']=='back_r','bodyArtScope':'back_r scalp only:83 traced gray outline pixels per clip acrossF01..07; all other body RGBA exact'if cell['direction']=='back_r'else'body RGBA unchanged','scalpCoordinateEvidence':str(E/'scalp-outline-points.json').replace('\\','/'),'handArtChanged':False,'choreographyChanged':False,'timingChanged':False,'sourceRegistration':str(E/'weapon-registration.json').replace('\\','/'),'priorRearContourOverrides':'Exact old dark weapon pixels retained only where layer differs from raw source; no new luma filter applied. Quantities in material-composition-evidence.json.'}
 docs={part:ase(str(out/'source'/name))for part,name in [('composite','composite.aseprite'),('body','body.aseprite'),('native','native.aseprite')]}
 assert [l['name']for l in docs['composite']['layers']]==['weaponBack','body','weaponFront','handFront']
 for part,doc in docs.items():assert doc['durationsMs']==old['durationsMs'],(key,part,doc['durationsMs'],old['durationsMs'])
 rows=[]
 for i,frame in enumerate(p['frames']):
  n=f'{i:02}.png';oldf=old['frames'][i];fout=out/n;flat=raster(fout);body=raster(out/'layers/body'/n);native=raster(out/'native'/n)
  assert flat.shape==(256,256,4)and native.shape==(128,128,4)
  assert np.isin(flat[:,:,3],[0,255]).all()
  assert same(body[64:192,64:192],native)
  oldbody=raster(oldf['layers']['body']['png']);expected=oldbody.copy()
  if cell['direction']=='back_r'and i>0:
   for point in scalp[i]:
    x,y=point['native'];assert expected[y+64,x+64].tolist()==point['before'];expected[y+64,x+64]=point['after']
  assert same(body,expected)
  assert same(raster(out/'layers/handFront'/n),raster(oldf['layers']['handFront']['png']))
  calc=Image.new('RGBA',(256,256))
  for ln in ['weaponBack','body','weaponFront','handFront']:
   lp=str(out/'layers'/ln/n).replace('\\','/');a=raster(lp);assert np.array_equal(a[:,:,3],raster(oldf['layers'][ln]['png'])[:,:,3])
   calc=Image.alpha_composite(calc,Image.fromarray(a));frame['layers'][ln]={'png':lp,'sha256':sha(lp)}
  assert same(np.array(calc),flat)
  for part,a in [('composite',flat),('body',body),('native',native)]:assert same(docs[part]['frames'][i],a),(key,i,part)
  for part,a in [('body',body),('native',native)]:assert same(raster(E/'fresh-proof'/key/part/n),a)
  if not oldf['weaponVisible']:assert same(flat,expected)
  frame.update(png=str(fout).replace('\\','/'),sha256=sha(fout),nativePng=str(out/'native'/n).replace('\\','/'),nativeSha256=sha(out/'native'/n))
  if oldf['weaponVisible']:
   r=reg[(key,i)];frame.update(rightGrip=r['grip'],rotationDeg=r['angle'],flipBit=r['flip'],registrationEvidence='Exact original occupied mask; source color match before material edit')
  rows.append({'index':i,'compositeRgbaDelta':diff(flat,raster(oldf['png'])),'bodyRgbaDelta':diff(body,oldbody),'bodyChangesOnlyTracedScalp':True,'handFrontRgbaDelta':0,'nativeRgbaDelta':diff(native,oldbody[64:192,64:192]),'durationMs':frame['durationMs'],'weaponAlphaUnchanged':True})
 p['stripSha256']=sha(p['strip']);p['nativeStripSha256']=p['stripSha256'];p['compositeStripSha256']=sha(p['compositeStrip'])
 strip=raster(p['strip']);compositeStrip=raster(p['compositeStrip'])
 assert strip.shape==(128,128*len(p['frames']),4)
 assert compositeStrip.shape==(256,256*len(p['frames']),4)
 for i,frame in enumerate(p['frames']):
  assert same(strip[:,128*i:128*(i+1)],raster(frame['nativePng']))
  assert same(compositeStrip[:,256*i:256*(i+1)],raster(frame['png']))
 write(out/'clip.json',p)
 cell.update(status='ARTISTIC_REVISION_REQUIRED'if cell['direction'].startswith('back')else'ACTIVE_CANDIDATE',isAffected=True,clipJson=str(out/'clip.json').replace('\\','/'),reviewStatus=p['artisticStatus'],masterSha256=p['masterSha256'],bodyMasterSha256=p['bodyMasterSha256'],nativeMasterSha256=p['nativeMasterSha256'],stripSha256=p['stripSha256'],nativeStripSha256=p['stripSha256'],notes='Independent weapon material refinement; back_r scalp contour corrected only at explicit points. HandFront, choreography, timing and alpha/depth masks unchanged. Rear reconstruction unresolved.',provenance=REV+' scoped Aseprite fork; exact prior clip lineage')
 proof['clips'].append({'cellId':key,'frames':rows,'savedMasterPixelsMatch':True,'savedBodyNativePixelsMatch':True,'timingUnchanged':True,'celPositions':{part:doc['positions']for part,doc in docs.items()}})
newm['activeCandidatesCount']=sum(c['status']=='ACTIVE_CANDIDATE'for c in newm['cells'])
newm['inRevisionCount']=sum(c['status']=='ARTISTIC_REVISION_REQUIRED'for c in newm['cells'])
newm['unchangedAliasesCount']=sum(not c['isAffected']for c in newm['cells'])
newm['inProductionCount']=0
newm['affectedCount']=sum(c['isAffected']for c in newm['cells'])
newm['internalIntegrationPassCount']=0
newm['passEvidenceTaxonomyNote']='No Root or QA artistic PASS in this session. Status is relative to the immediate prior candidate; affected weapon materials do not imply repaired choreography.'
newm['comparisonBaselineManifest']=newm['parentManifest']
newm['totalFrames']=210
newm['affectedFramesCount']=sum(c['frameCount']for c in newm['cells']if c['isAffected'])
newm['unchangedFramesCount']=sum(c['frameCount']for c in newm['cells']if not c['isAffected'])
proof['status']='PASS_FOCUSED_MATERIAL_FORK_TECHNICAL_CHECKS'
write(C/'candidate28manifest.json',newm);write(E/'verification.json',proof)
print(json.dumps({'inputsUnchanged':len(inventory),'changedClips':len(proof['clips']),'producedFrames':sum(len(c['frames'])for c in proof['clips']),'affectedFrames':newm['affectedFramesCount'],'aliasFrames':newm['unchangedFramesCount'],'weapons':proof['weaponSources'],'eligibleForIntegration':False},ensure_ascii=False,indent=2))
