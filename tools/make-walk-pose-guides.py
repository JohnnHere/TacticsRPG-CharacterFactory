"""Rough 2D pose guides ONLY, never exported/imported as character sprites.
Image_gen must redraw the legs in the approved character's materials/anatomy.
No approved source sprite, runtime asset or Unity file is modified.
"""
from pathlib import Path
from PIL import Image,ImageDraw

root=Path("characters/orc-01")
for view,near_x,far_x in [("front_l",56,67),("back_l",55,67),("back_r",69,57)]:
    sign=-1 if view.endswith("_l") else 1
    base=Image.open(root/f"sprites/Directions/orc_01_dir_{view}.png").convert("RGBA")
    frames=[]
    for phase in range(6):
        na,fa=[(16,120),(-15,118)] if phase==0 else ([(4,120),(-8,112)] if phase==1 else ([(-12,118),(10,120)] if phase==2 else ([(-15,118),(16,120)] if phase==3 else ([(-8,112),(4,120)] if phase==4 else [(10,120),(-12,118)]))))
        na=(64+sign*na[0],na[1]);fa=(64+sign*fa[0],fa[1])
        nk=((near_x+na[0])//2,98 if phase==4 else 101)
        fk=((far_x+fa[0])//2,98 if phase==1 else 101)
        im=Image.new("RGBA",(128,128));d=ImageDraw.Draw(im)
        for hip,knee,ankle,near in [((far_x,87),fk,fa,False),((near_x,87),nk,na,True)]:
            d.line([hip,knee],fill=(22,20,22,255),width=12)
            d.line([hip,knee],fill=(55,52,57,255),width=8)
            d.line([knee,ankle],fill=(22,20,22,255),width=10)
            d.line([knee,ankle],fill=(116,96,78,255),width=6)
            x,y=knee;d.polygon([(x-4,y-4),(x+3,y-4),(x+5,y+2),(x,y+6),(x-5,y+2)],fill=(154,148,143,255) if near else (107,103,103,255),outline=(29,25,28,255))
            x,y=ankle;d.polygon([(x-4*sign,y-3),(x+3*sign,y-3),(x+6*sign,y+1),(x+12*sign,y+2),(x+12*sign,y+6),(x-5*sign,y+6)],fill=(124,75,44,255),outline=(24,19,18,255))
        for y in range(128):
            for x in range(128):
                p=base.getpixel((x,y))
                cloth=view.startswith("front") and y<105 and 54<x<75 and p[0]>p[1]*2.1
                if p[3] and (y<87 or (y<106 and (x<42 or x>83)) or cloth):im.putpixel((x,y),p)
        frames.append(im)
    sheet=Image.new("RGBA",(128*6,128))
    for i,im in enumerate(frames):sheet.paste(im,(i*128,0))
    folder=root/f"source/animations-v1/Walk/{view}";folder.mkdir(parents=True,exist_ok=True)
    sheet.resize((2304,384),Image.Resampling.NEAREST).save(folder/"pose-guide.png")
    print(folder/"pose-guide.png")
