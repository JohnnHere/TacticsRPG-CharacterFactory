from pathlib import Path
from PIL import Image
import json,hashlib,shutil,copy
S=Path('characters/orc-v1/source/combat-recovery-v7/rear-r');C=S.parent/'rear-r-flashfixed';E=Path('experiments/main-orc-combat-recovery-v7/rear-r-flashfixed');N=S.parent/'bookends/back_r-sword/layers/body'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def im(p):return Image.open(p).convert('RGBA')
def diff(a,b):return sum(x!=y for x,y in zip(a.getdata(),b.getdata()))
def bright(a):return sum(c[3]>0 and .299*c[0]+.587*c[1]+.114*c[2]>=145 for c in a.getdata())
def remap(v):
 if isinstance(v,str):return v.replace(S.as_posix()+'/',C.as_posix()+'/')
 if isinstance(v,list):return [remap(x)for x in v]
 if isinstance(v,dict):return {k:remap(x)for k,x in v.items()}
 return v
results={};deliver=[]
for kind in ['sword','axe']:
 src=S/f'back_r-{kind}';dst=C/src.name;old=json.loads((src/'clip.json').read_text());clip=remap(copy.deepcopy(old))
 for i in [0,11]:
  # Byte-exact reuse of approved mechanical donor PNGs, no raster processing.
  shutil.copy2(N/f'{i:02}.png',dst/f'layers/body/{i:02}.png');shutil.copy2(N/f'{i:02}.png',dst/f'frames/{i:02}.png')
 clip['revision']='main-orc-combat-recovery-v7-back-r-flash-fixed';clip['checkpoint']='V7_BACK_R_FLASH_FIXED';clip['sourceParentClip']=(src/'clip.json').as_posix();clip['sourceParentClipSha256']=sha(src/'clip.json');clip['technicalStatus']='TECHNICALLY_COMPLETE';clip['artisticStatus']='VISUAL_REVIEW_REQUIRED';clip['creatorApproval']='PENDING_CREATOR';clip['eligibleForIntegration']=False
 inherited=copy.deepcopy(old['provenance']);clip['provenance']={'method':'Mechanical Aseprite transplant of existing normalized body bookends F00/F11; inherited V7 grip/choreography unchanged','authorScript':(E/'transplant.lua').as_posix(),'authorScriptSha256':sha(E/'transplant.lua'),'normalizedBodySources':[{'png':(N/f'{i:02}.png').as_posix(),'sha256':sha(N/f'{i:02}.png')}for i in [0,11]],'newPixelLabCalls':0,'mastersSavedReopened':True,'rgbaAndTimingVerified':True,'inheritedProvenance':inherited}
 clip['bodyMaster']=(dst/'source/body.aseprite').as_posix()
 for key in ['master','nativeMaster','bodyMaster','strip','nativeStrip','compositeStrip']:clip[key+'Sha256']=sha(clip[key])
 rows=[];layerChanges=[];pngByteUnchanged=0;frameChecks=[]
 for i,(f,of)in enumerate(zip(clip['frames'],old['frames'])):
  f['sha256']=sha(f['png']);f['nativeSha256']=sha(f['nativePng'])
  for name,layer in f['layers'].items():
   layer['sha256']=sha(layer['png']);a,b=im(of['layers'][name]['png']),im(layer['png']);count=diff(a,b)
   if count:layerChanges.append({'frame':i,'layer':name,'changedPixels':count})
   assert count==0 or(i in [0,11]and name=='body'),(kind,i,name,count)
  layers={n:im(v['png'])for n,v in f['layers'].items()};render=Image.new('RGBA',(256,256))
  for name in clip['layerOrder']:render=Image.alpha_composite(render,layers[name])
  assert diff(render,im(f['png']))==0;assert diff(layers['body'].crop((64,64,192,192)),im(f['nativePng']))==0
  re=E/f'master-reexport/{kind}';assert diff(im(re/f'frames/{i:02}.png'),im(f['png']))==0;assert diff(im(re/f'native/{i:02}.png'),im(f['nativePng']))==0;assert diff(im(re/f'body/{i:02}.png'),layers['body'])==0
  for n in clip['layerOrder']:assert diff(im(re/f'layers/{n}/{i:02}.png'),layers[n])==0
  if i in [0,11]:
   assert all(layers[n].getbbox()is None for n in ['weaponBack','weaponFront','handFront']);assert diff(im(f['png']),layers['body'])==0;assert sha(f['layers']['body']['png'])==sha(N/f'{i:02}.png')
   rows.append({'frame':i,'brightPixelsBefore':bright(im(of['layers']['body']['png'])),'brightPixelsAfter':bright(layers['body']),'changedBodyPixels':diff(im(of['layers']['body']['png']),layers['body']),'normalizedPngSha256':sha(N/f'{i:02}.png')});f['provenance']='Existing normalized bookend body transplanted byte-exactly; no new artistic choice; source in provenance.normalizedBodySources'
  else:
   assert sha(f['png'])==sha(of['png'])and sha(f['nativePng'])==sha(of['nativePng'])
  frameChecks.append({'index':i,'alphaOverMismatchPixels':0,'nativeBodyMismatchPixels':0,'masterReexportMismatchPixels':0,'durationMs':f['durationMs']})
 assert len(clip['frames'])==old['frameCount']==12 and clip['durationsMs']==old['durationsMs']and clip['totalDurationMs']==old['totalDurationMs'];assert clip['visibleInterval']==old['visibleInterval']
 for p in src.rglob('*.png'):
  rel=p.relative_to(src).as_posix();isAllowed=rel in ['layers/body/00.png','layers/body/11.png','frames/00.png','frames/11.png','native/00.png','native/11.png','native-strip.png','composite-strip.png']
  if not isAllowed:assert sha(p)==sha(dst/rel),(kind,rel);pngByteUnchanged+=1
 # Verify every strip tile against the declared frame, not just its hash.
 ns,cs=im(clip['nativeStrip']),im(clip['compositeStrip']);assert ns.size==(12*128,128)and cs.size==(12*256,256)
 for i,f in enumerate(clip['frames']):assert diff(ns.crop((128*i,0,128*(i+1),128)),im(f['nativePng']))==0 and diff(cs.crop((256*i,0,256*(i+1),256)),im(f['png']))==0
 (dst/'clip.json').write_text(json.dumps(clip,indent=2),encoding='utf-8');results[kind]={'bookends':rows,'neighbors':{str(i):bright(im(clip['frames'][i]['layers']['body']['png']))for i in [1,10]},'layerChanges':layerChanges,'otherPngsByteIdentical':pngByteUnchanged,'frameChecks':frameChecks,'durationMs':clip['totalDurationMs'],'visibleInterval':clip['visibleInterval']};deliver.append({'direction':'back_r','action':clip['category'],'clip':(dst/'clip.json').as_posix(),'clipSha256':sha(dst/'clip.json')})
protected=json.loads((E/'protected-input-hashes.json').read_text());assert all(sha(p)==h for p,h in protected.items());(E/'verification.json').write_text(json.dumps({'checkpoint':'V7_BACK_R_FLASH_FIXED','clips':results,'protectedFilesUnchanged':len(protected),'newPixelLabCalls':0},indent=2))
report=['# V7 back_r — bookends normalizados','', '`V7_BACK_R_FLASH_FIXED` · `TECHNICALLY_COMPLETE` · `VISUAL_REVIEW_REQUIRED` · `PENDING_CREATOR`','', '[Preview antes/depois](preview.html) · [Verificação completa](verification.json)','', 'Transplante mecânico no Aseprite batch, perfil tmp/aseprite-v7-rearr-profile. As duas versões em rear-r permanecem intactas; cópias novas em characters/orc-v1/source/combat-recovery-v7/rear-r-flashfixed/. Os PNGs normalizados existentes de bookends/back_r-sword foram reutilizados byte a byte, sem nova decisão artística e sem geração.','', '| Clipe | F | Claros antes → depois (luma ≥145) | Pixels corporais alterados |','|---|---|---|---:|']
for k,r in results.items():
 for row in r['bookends']:report.append(f"| {k} | {row['frame']:02} | {row['brightPixelsBefore']} → {row['brightPixelsAfter']} | {row['changedBodyPixels']} |")
report+=['', 'Luma BT.601 = 0,299R + 0,587G + 0,114B; somente pixels opacos. F01/F10 não mudaram: '+', '.join(f"{k}: {r['neighbors']['1']}/{r['neighbors']['10']} pixels claros"for k,r in results.items())+'.','', 'Diff nas camadas: somente body/00 e body/11, nos dois clipes. Todos os outros quadros/camadas e PNGs fora dos derivados necessários são byte-idênticos aos pais. Compostos/nativos dos bookends, tiras e mestres mudam exclusivamente como derivados dessas duas camadas. Bookends continuam sem armas e composto igual ao corpo.','', 'Preservados 12 quadros por clipe, Sword 950 ms, Axe 1320 ms, durações individuais, intervalo armado, pegada, posições, trajetória e demais pixels. Mestres composto256 e nativo128 atualizados, mais mestre body256 explícito; os três por clipe foram reabertos/reexportados, comparados em pixels e timing (cel.position real). Recorte body→native e alpha-over conferem com zero diferenças; cada tile das tiras confere com seu PNG. Hashes reais atualizados em clip.json. Não existia nativeComposite no contrato de origem.','', f'{len(protected)} arquivos protegidos conferidos por SHA-256; rear-r, rear-alt e doadores bookends permanecem byte-idênticos. Sem escritas em frontal, V5/V6, Unity ou commits. Zero chamadas PixelLab. Evidência de pegada anterior espelhada e identificada como herdada; ela não foi alterada neste passe.','', 'Parada em V7_BACK_R_FLASH_FIXED. Sem aprovação artística nova ou promoção automática.']
(E/'report.md').write_text('\n'.join(report),encoding='utf-8');(E/'handoff.json').write_text(json.dumps({'checkpoint':'V7_BACK_R_FLASH_FIXED','technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','creatorApproval':'PENDING_CREATOR','newPixelLabCalls':0,'clips':deliver,'report':(E/'report.md').as_posix(),'preview':(E/'preview.html').as_posix(),'runtimeImplemented':False},indent=2))
print(json.dumps({k:r['bookends']for k,r in results.items()}))
