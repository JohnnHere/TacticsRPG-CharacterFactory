"""Read-only pixel checks for the representative Aseprite exports."""
from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parents[2]
def im(p): return Image.open(ROOT/p).convert('RGBA')
checks=[]
for i in range(13):
    body=im(f'characters/orc-v1/source/complete-v1/back_r/Sword/Attack/layers/body/{i:02d}.png')
    candidate_body=im(f'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack/layers/body/{i:02d}.png')
    native=im(f'characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack/native/{i:02d}.png')
    crop=body.crop((64,64,192,192))
    assert crop.tobytes()==native.tobytes(),f'sword native frame {i} contains composite/weapon pixels or is not body crop'
    assert body.tobytes()==candidate_body.tobytes(),f'sword body layer pixels differ from complete-v1 at {i}'
    checks.append(f'sword native frame {i:02d} is body-only crop; body pixels match complete-v1')
for direction in ('front_r','front_l'):
    for i in (0,1,3,4):
        assert im(f'characters/orc-v1/source/complete-v1/{direction}/Unarmed/{i:02d}.png').tobytes()==im(f'characters/orc-v1/source/rear-recovery-v2/{direction}/Unarmed/{i:02d}.png').tobytes(),f'{direction} Unarmed frame {i} should be preserved byte-for-byte'
    body=im(f'characters/orc-v1/source/rear-recovery-v2/{direction}/Unarmed/02.png')
    native=im(f'characters/orc-v1/source/rear-recovery-v2/{direction}/Unarmed/native/02.png')
    assert body.crop((64,64,192,192)).tobytes()==native.tobytes(),f'{direction} F02 native export does not match composite crop'
    checks.append(f'{direction} Unarmed frames 00/01/03/04 preserved; F02 native export matches composite crop')
report={'status':'PASS','checks':checks,'notes':'No baseline source or production PNG was written by the authoring script.'}
out=ROOT/'experiments/main-orc-rear-recovery-v2/representative-pixel-verification.json'
out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
