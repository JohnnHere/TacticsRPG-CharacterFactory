"""Import authored front locomotion and verify real LibreSprite RGBA/timing exports."""
import hashlib,json,subprocess
from pathlib import Path
from PIL import Image

root=Path('.').resolve();python=root/'tmp/pixel-venv/Scripts/python.exe';editor=root/'tmp/tools/libresprite/libresprite.exe';reports=[]
if (root/'characters/orc-idle-subtle-v2-validation.json').exists():
    raise RuntimeError('Mixed-source Idle v2 exists. Do not overwrite frame provenance with v1 whole-sheet importer; use verify-orc-front-locomotion.mjs.')
for b in json.loads((root/'characters/orc-front-locomotion-batch-v1.json').read_text(encoding='utf-8')):
    for state,count,ms in [('Idle',4,240),('Walk',6,73)]:
        folder=root/'characters'/b['id']/f'source/animations-v1/{state}/front_r';stem=f'{state.lower()}_front_r'
        subprocess.run(['node','tools/import-animation-clip.mjs',b['id'],state,'front_r',f'source/animations-v1/{state}/front_r'],check=True,capture_output=True,text=True)
        subprocess.run([str(python),'tools/write-animation-editable.py',str(folder)],check=True,capture_output=True)
        ase=folder/f'{stem}.aseprite';sheet=root/'tmp'/f"editor-{b['id']}-{state}-front_r.png";data=sheet.with_suffix('.json')
        # LibreSprite applies export options in order: set format before data/input.
        subprocess.run([str(editor),'-b','--format','json-array','--data',str(data.relative_to(root)),'--sheet-type','horizontal','--sheet',str(sheet.relative_to(root)),str(ase.relative_to(root))],check=True,capture_output=True)
        e=json.loads(data.read_text(encoding='utf-8'));assert len(e['frames'])==count
        img=Image.open(sheet).convert('RGBA')
        for i,f in enumerate(e['frames']):
            assert f['duration']==ms,(b['id'],state,i,'duration')
            r=f['frame'];out=img.crop((r['x'],r['y'],r['x']+r['w'],r['y']+r['h']))
            native=Image.open(folder/f'{stem}_{i:02d}.png').convert('RGBA')
            assert out.size==native.size==(128,128) and out.tobytes()==native.tobytes(),(b['id'],state,i,'RGBA')
        reports.append({'id':b['id'],'state':state,'direction':'front_r','frames':count,'durationMs':ms,'editable':ase.relative_to(root).as_posix(),'editableSha256':hashlib.sha256(ase.read_bytes()).hexdigest(),'editorSheet':sheet.relative_to(root).as_posix(),'editorData':data.relative_to(root).as_posix(),'librespriteExportRgba':'ALL_FRAMES_IDENTICAL'})
        print(b['id'],state,f'{count} frames: imported, editable export RGBA and timing identical',flush=True)
(root/'characters/orc-front-locomotion-editor-verification-v1.json').write_text(json.dumps({'editor':'LibreSprite 1.3','clips':reports,'summary':'14/14 clips; 70/70 frames RGBA identical; durations identical'},indent=2)+'\n',encoding='utf-8')
