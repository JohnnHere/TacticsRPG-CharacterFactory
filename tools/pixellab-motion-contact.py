"""Review layout only; source PNGs remain unchanged."""
from pathlib import Path
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parents[1]
out=root/'reports/pixellab-orcs-independent-v1'
out.mkdir(exist_ok=True)
for state in ['Idle','Walk']:
    sheet=Image.new('RGB',(128*8, (128+24)*3),(26,33,35))
    draw=ImageDraw.Draw(sheet)
    for n in range(1,4):
        for f in range(8):
            source=root/f'characters/orc-pixellab-0{n}/source/studies/{state}/{f:02d}.png'
            if not source.exists():continue
            im=Image.open(source).convert('RGBA')
            sheet.paste(im,(128*f,(n-1)*152+24),im)
            draw.text((128*f+4,(n-1)*152+4),f'Orc {n} / {f+1}',fill=(230,220,194))
    sheet.save(out/f'{state.lower()}-contact.png')
