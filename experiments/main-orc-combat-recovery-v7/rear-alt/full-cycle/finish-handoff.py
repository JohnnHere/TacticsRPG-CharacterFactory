from pathlib import Path
from PIL import Image
import json,hashlib
E=Path('experiments/main-orc-combat-recovery-v7/rear-alt/full-cycle');P=E.parent;plan=json.loads((E/'plan.json').read_text());report=P/'report.md'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
checks=json.loads((E/'browser-check.json').read_text());assert checks['status']=='PASS'and checks['exactCanvasComparisons']==240
alpha={}
for kind,cfg in plan['clips'].items():
 clip=json.loads((Path(cfg['dest'])/'clip.json').read_text());actual=set();bounds=[]
 for f in clip['frames']:
  for key,hkey in [('png','sha256'),('nativePng','nativeSha256')]:assert sha(f[key])==f[hkey]
  for n,v in f['layers'].items():assert sha(v['png'])==v['sha256']
  im=Image.open(f['nativePng']).convert('RGBA');actual.update(im.getchannel('A').getdata());b=im.getbbox();assert b[0]>0 and b[1]>0 and b[2]<128 and b[3]<=127,(kind,f['index'],b);bounds.append(b)
 assert actual=={0,255};alpha[kind]={'nativeAlphaLevels':sorted(actual),'bodyBoundsByFrame':bounds}
 for key in ['master','nativeMaster','strip','nativeStrip','compositeStrip']:assert sha(clip[key])==clip[key+'Sha256']
(E/'final-contract-check.json').write_text(json.dumps({'status':'PASS','clips':alpha,'allDeclaredAssetHashesVerified':True},indent=2))
protected=json.loads((E/'protected-input-hashes.json').read_text());assert all(sha(p)==h for p,h in protected.items())
report.write_text(report.read_text(encoding='utf-8')+'\n\nPlayer conferido em Edge/Chromium headless: 240 comparações canvas↔PNG exatas (15 quadros × 2 famílias × body/composto × 4 painéis), alinhamento por fase e tempos próprios, relógio 1×/0,5×, pausa terminal sem repetir, passo/zoom/tático, juntas e HTTP/file. Nenhum erro JavaScript. browser-check.json e capturas *-preview-check.png/*-tactical-check.png registram a verificação. Contrato final: todos os hashes declarados conferem, alfa nativo binário {0,255}, corpo sem corte nas bordas do canvas e mestres separados 256/128.\n',encoding='utf-8')
old=P/'handoff.json'
if old.exists()and not(P/'pose-stage-handoff.json').exists():(P/'pose-stage-handoff.json').write_bytes(old.read_bytes())
clips=[]
for kind,cfg in plan['clips'].items():
 p=Path(cfg['dest'])/'clip.json';c=json.loads(p.read_text());clips.append({'direction':'back_l','action':kind,'clip':p.as_posix(),'clipSha256':sha(p),'frameCount':c['frameCount'],'totalDurationMs':c['totalDurationMs'],'visibleInterval':c['visibleInterval'],'master':c['master'],'masterSha256':c['masterSha256'],'nativeMaster':c['nativeMaster'],'nativeMasterSha256':c['nativeMasterSha256']})
handoff={'checkpoint':'V7_BACK_L_FULL_MANUAL_READY','technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','creatorApproval':'PENDING_CREATOR','runtimeImplemented':False,'eligibleForIntegration':False,'newPixelLabCalls':0,'clips':clips,'report':report.as_posix(),'reportSha256':sha(report),'preview':(P/'preview.html').as_posix(),'previewSha256':sha(P/'preview.html'),'phaseComparison':(E/'phase-comparison.json').as_posix(),'jointMetrics':(E/'joint-metrics.json').as_posix(),'bookendAudit':(E/'bookend-flash-audit.json').as_posix(),'browserCheck':(E/'browser-check.json').as_posix(),'protectedFilesUnchanged':len(protected),'historicalManualKeysPreserved':True,'reviewNote':'Full-cycle manual candidates; no creator approval, no canonical matrix promotion, no Unity writes.'}
old.write_text(json.dumps(handoff,indent=2),encoding='utf-8')
print('V7_BACK_L_FULL_MANUAL_READY; 30 frames; 240 browser comparisons; protected files:',len(protected))
