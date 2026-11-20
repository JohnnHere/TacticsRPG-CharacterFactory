from pathlib import Path
import json,hashlib
E=Path('experiments/main-orc-combat-recovery-v8/rear')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
spec=json.loads((E/'temporal-spec.json').read_text());manifest=json.loads((E/'candidate4manifest.json').read_text());browser=json.loads((E/'browser-check.json').read_text());assert browser['status']=='PASS'and browser['exactCanvasComparisons']==200
for cell in manifest['cells']:
 cp=Path(cell['clip']);c=json.loads(cp.read_text());s=spec[cell['action']];assert sha(cp)==cell['clipSha256'];assert c['durationsMs']==s['durationsMs']and c['contactEvent']['timeMs']==s['impactStartMs'];assert sum(c['durationsMs'][:c['contactEvent']['frame']])==c['contactEvent']['timeMs']
 for k in ['master','nativeMaster','strip','nativeStrip','compositeStrip']:assert sha(c[k])==c[k+'Sha256']
 for f in c['frames']:
  assert sha(f['png'])==f['sha256']and sha(f['nativePng'])==f['nativeSha256'];assert all(sha(a['png'])==a['sha256']for a in f['layers'].values())
protected=json.loads((E/'protected-input-hashes.json').read_text());assert all(sha(p)==h for p,h in protected.items())
r=E/'report.md';r.write_text(r.read_text(encoding='utf-8')+'\n\nPlayer conferido em Edge/Chromium headless: 200 comparações canvas↔PNG exatas (25 posições de quadro por família somadas × 4 direções × body/composto), rótulos de fase coincidentes, verificações antes/no/depois do impacto em 325/410 ms, velocidades 1×/0,5×, passo/zoom/tático, pausa terminal e repetição, HTTP/file e zero erro JavaScript. Evidência em browser-check.json e capturas *-impact-1x.png/*-impact-tactical.png. Hashes declarados dos 50 quadros, camadas, oito mestres e oito tiras reconferidos no freeze final.\n',encoding='utf-8')
h={'checkpoint':'V8_REAR_ALIGNED','technicalStatus':'TECHNICALLY_COMPLETE','artisticStatus':'VISUAL_REVIEW_REQUIRED','creatorApproval':'PENDING_CREATOR','runtimeImplemented':False,'eligibleForIntegration':False,'newPixelLabCalls':0,'clips':manifest['cells'],'canonicalGrids':{k:{'frames':s['frameCount'],'durationMs':s['durationMs'],'impactFrame':s['impactFrame'],'impactStartMs':s['impactStartMs']}for k,s in spec.items()},'impactAuthority':'Frontal phase by frame index + cumulative durations; protected legacy contactEvent divergences documented, not edited','report':r.as_posix(),'reportSha256':sha(r),'phaseTable':(E/'phase-comparison.md').as_posix(),'phaseCsv':(E/'phase-comparison.csv').as_posix(),'preview':(E/'preview.html').as_posix(),'previewSha256':sha(E/'preview.html'),'browserCheck':(E/'browser-check.json').as_posix(),'protectedFilesUnchanged':len(protected)}
(E/'handoff.json').write_text(json.dumps(h,indent=2),encoding='utf-8');print('V8_REAR_ALIGNED — four clips, canonical grids, protected files:',len(protected))
