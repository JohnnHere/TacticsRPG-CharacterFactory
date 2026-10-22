"""Hand-specified 2D leg-position GUIDE for image_gen, never a runtime asset.
The approved upper-body pixels locate the individual; rough leg blocks show
the missing opposite stride. The final legs must be artistically redrawn.
"""
from pathlib import Path
from PIL import Image,ImageDraw

root=Path(__file__).parents[3]
base=Image.open(root/"pixel-grid-v1/front-r-native.png").convert("RGBA")
poses=[((54,88),(72,100),(80,119),(63,88),(53,103),(43,120)),
       ((54,88),(66,100),(70,120),(63,88),(52,102),(45,114)),
       ((54,88),(62,101),(63,120),(63,88),(63,97),(61,108))]
sheet=Image.new("RGBA",(384,128))
for i,(fh,fk,fa,nh,nk,na) in enumerate(poses):
    im=Image.new("RGBA",(128,128));d=ImageDraw.Draw(im)
    for hip,knee,ankle,near in [(fh,fk,fa,False),(nh,nk,na,True)]:
        d.line([hip,knee],fill=(22,20,22,255),width=12)
        d.line([hip,knee],fill=(55,52,57,255),width=8)
        d.line([knee,ankle],fill=(22,20,22,255),width=10)
        d.line([knee,ankle],fill=(104,91,80,255),width=6)
        x,y=knee;d.polygon([(x-4,y-4),(x+3,y-4),(x+5,y+2),(x,y+6),(x-5,y+2)],fill=(150,145,140,255),outline=(29,25,28,255))
        x,y=ankle;d.polygon([(x-4,y-3),(x+3,y-3),(x+6,y+1),(x+12,y+2),(x+12,y+6),(x-5,y+6)],fill=(124,75,44,255),outline=(24,19,18,255))
    for y in range(128):
        for x in range(128):
            p=base.getpixel((x,y))
            if p[3] and (y<87 or (y<106 and (x<40 or x>81)) or (y<105 and 56<x<74 and p[0]>p[1]*2.1)):
                im.putpixel((x,y),p)
    sheet.paste(im,(i*128,0))
sheet.resize((1536,512),Image.Resampling.NEAREST).save(Path(__file__).with_name("opposite-pose-guide.png"))
