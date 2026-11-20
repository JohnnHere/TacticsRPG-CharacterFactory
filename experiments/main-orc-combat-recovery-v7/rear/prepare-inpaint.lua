local p='experiments/main-orc-combat-recovery-v7/rear'
local im=Image{fromFile=p..'/raw/sword2/05.png'}
local s=Sprite(128,128,ColorMode.RGB);s:newCel(s.layers[1],1,im,Point(0,0));app.activeSprite=s;app.command.SpriteSize{ui=false,width=256,height=256,method='nearest-neighbor'};s:saveCopyAs(p..'/inpaint-reference-256.png');s:close()

