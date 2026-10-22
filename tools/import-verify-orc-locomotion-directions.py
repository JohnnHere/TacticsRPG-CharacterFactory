"""Import only new directional clips and demonstrate real editor compatibility."""
import argparse,hashlib,importlib.util,json,subprocess
from pathlib import Path
from PIL import Image
root=Path('.').resolve()
spec=importlib.util.spec_from_file_location('editable',root/'tools/write-animation-editable.py');editable=importlib.util.module_from_spec(spec);spec.loader.exec_module(editable)
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
ap=argparse.ArgumentParser();ap.add_argument('--batch',default='characters/orc-locomotion-single-view-batch-v1.json');ap.add_argument('--report',default='characters/orc-locomotion-directions-editor-v1.json');args=ap.parse_args()
report=root/args.report;evidence=read(report) if report.exists() else {'editor':'LibreSprite 1.3','clips':[]}
for b in read(root/args.batch):
 origin=root/b['folder']
 if not (origin/'extraction.json').exists():continue
 for state,count in b.get('states',{'Idle':4,'Walk':6}).items():
  ms={'Idle':240,'Walk':73,'Attack':90,'Hit':80,'Defeat':120}[state]
  if any(e['id']==b['id'] and e['direction']==b['direction'] and e['state']==state for e in evidence['clips']):continue
  version=b.get('animationSourceVersions',{}).get(state,'animations-v1')
  folder=root/'characters'/b['id']/f"source/{version}/{state}/{b['direction']}";rel=folder.relative_to(root/'characters'/b['id']).as_posix()
  replace=['--replace'] if state in b.get('replaceUnapprovedStates',[]) else []
  subprocess.run(['node','tools/import-animation-clip.mjs',b['id'],state,b['direction'],rel,*replace],check=True,capture_output=True)
  editable.write_clip(folder);ase=folder/f"{state.lower()}_{b['direction']}.aseprite";sheet=root/'tmp'/f"editor-{b['id']}-{state}-{b['direction']}.png";data=sheet.with_suffix('.json')
  subprocess.run([str(root/'tmp/tools/libresprite/libresprite.exe'),'-b','--format','json-array','--data',str(data.relative_to(root)),'--sheet-type','horizontal','--sheet',str(sheet.relative_to(root)),str(ase.relative_to(root))],check=True,capture_output=True)
  e=read(data);assert len(e['frames'])==count;im=Image.open(sheet).convert('RGBA')
  for i,f in enumerate(e['frames']):
   r=f['frame'];assert f['duration']==ms;out=im.crop((r['x'],r['y'],r['x']+128,r['y']+128));native=Image.open(folder/f"{state.lower()}_{b['direction']}_{i:02d}.png").convert('RGBA');assert out.tobytes()==native.tobytes()
  evidence['clips'].append({'id':b['id'],'state':state,'direction':b['direction'],'frames':count,'durationMs':ms,'editable':ase.relative_to(root).as_posix(),'editableSha256':sha(ase),'editorSheet':sheet.relative_to(root).as_posix(),'editorData':data.relative_to(root).as_posix(),'roundtrip':'ALL_RGBA_AND_DURATIONS_IDENTICAL'})
  report.write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8');print(b['id'],state,b['direction'],'native/editor RGBA and timing identical',flush=True)
