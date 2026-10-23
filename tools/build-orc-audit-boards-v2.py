"""Contact boards only: exact native images composited for visual inspection."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'reports/orc-assets-audit-v2.json').read_text(encoding='utf-8'))
dest=root/'reports/orc-audit-v2';dest.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
for c in data['classes']:
    for group,states in [('locomotion',['Idle','Walk']),('combat',['Attack','Unarmed','Hit','Defeat'])]:
        clips=[x for x in data['clips'] if x['id']==c['id'] and x['state'] in states]
        out=Image.new('RGBA',(970,50+len(clips)*132),(27,32,40,255));d=ImageDraw.Draw(out);d.text((12,12),c['id']+' / '+group,fill='white',font=font)
        for row,clip in enumerate(clips):
            y=48+row*132;d.text((8,y+12),clip['state']+'\n'+clip['direction'],fill=(190,205,218),font=font)
            for i,f in enumerate(clip['frames']):
                tile=Image.new('RGBA',(128,128),(58,63,72,255));tile.alpha_composite(Image.open(root/f['file']).convert('RGBA'));out.alpha_composite(tile,(168+i*132,y))
        out.save(dest/(c['id']+'-'+group+'.png'))
concepts=Image.new('RGBA',(1600,1000),(27,32,40,255));d=ImageDraw.Draw(concepts)
for index,c in enumerate(data['classes']):
    chosen=('characters/'+c['id']+'/'+c['selectedConcept']['file']) if c['selectedConcept'] else c['concepts'][-1]
    image=Image.open(root/chosen).convert('RGBA')
    box=image.getbbox()
    if box:image=image.crop(box)
    image.thumbnail((370,440),Image.Resampling.NEAREST)
    x=(index%4)*400;y=(index//4)*500
    d.text((x+12,y+10),c['job']+' / vigente',fill='white',font=font)
    concepts.alpha_composite(image,(x+(400-image.width)//2,y+45+(440-image.height)//2))
concepts.save(dest/'concepts-current.png')
print(dest)
