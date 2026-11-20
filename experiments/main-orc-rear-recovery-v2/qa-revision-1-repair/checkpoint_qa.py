exec(open('experiments/main-orc-rear-recovery-v2/qa-revision-1-repair/diagnostics.py',encoding='utf8').read().split('for key,p in specs.items():')[0])
for key in ['SwordL','AxeR','AxeL']:
    sheet=Image.new('RGB',(4*384,2*410),(24,29,33));d=ImageDraw.Draw(sheet)
    for i in range(8):
        im=Image.open(O/'checkpoint'/key/'native'/f'{i:02}.png').convert('RGBA')
        x=i%4*384;y=i//4*410;sheet.paste(qa(im,3),(x,y+24));d.text((x+6,y+6),f'{key} F{i:02} saved source / body only',(245,240,220))
    sheet.save(O/'checkpoint'/f'{key}-wholebody.png')
    for i in range(8):
        im=Image.open(O/'checkpoint'/key/'native'/f'{i:02}.png').convert('RGBA')
        if key=='SwordL':box=(15,15,108,95)
        elif key=='AxeR':box=(70,0,125,85)
        else:box=(75,10,107,40)
        qa(im.crop(box),6).save(O/'checkpoint'/f'{key}-F{i:02}-detail.png')
