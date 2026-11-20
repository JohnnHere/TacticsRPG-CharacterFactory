local root='experiments/main-orc-combat-recovery-v7/rear'
local body=Image{fromFile=root..'/raw/sword2/04.png'}
local donor=Image{fromFile=root..'/raw/sword2/05.png'}
local s=Sprite(128,128,ColorMode.RGB);s.layers[1].name='body'
-- Replace the distal same-view arm region as an editable layer, including removal of the old region.
for y=3,32 do for x=92,108 do body:drawPixel(x,y,0) end end
s:newCel(s.layers[1],1,body,Point(0,0))
local l=s:newLayer();l.name='same-view-arm-donor'
local part=Image(128,128,ColorMode.RGB);part:clear()
for y=3,32 do for x=92,108 do part:drawPixel(x,y,donor:getPixel(x,y)) end end
s:newCel(l,1,part,Point(0,0))
s:saveAs(root..'/local-apex-test.aseprite');s:saveCopyAs(root..'/local-apex-test.png');app.activeSprite=s;app.command.SpriteSize{ui=false,width=512,height=512,method='nearest-neighbor'};s:saveCopyAs(root..'/local-apex-test-4x.png');s:close()
