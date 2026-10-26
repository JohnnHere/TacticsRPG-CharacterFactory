local root=assert(app.params.root);local function file(p)return app.fs.joinPath(root,p)end
local function inside(x,y,pts)local c=false;local j=#pts;for i=1,#pts do local a,b=pts[i],pts[j];if(a[2]>y)~=(b[2]>y)and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1]then c=not c end;j=i end;return c end
local E='experiments/main-orc-weapon-rescue-v3';local mask=Image(128,128,ColorMode.RGB);mask:clear(app.pixelColor.rgba(0,0,0,255));local pts={{53,76},{108,76},{119,73},{122,73},{122,79},{115,84},{53,88}}
for y=0,127 do for x=0,127 do if inside(x,y,pts)then mask:drawPixel(x,y,app.pixelColor.rgba(255,255,255,255))end end end
mask:saveAs(file(E..'/sword-recovery-mask.png'))
local strikeMask=Image(128,128,ColorMode.RGB);strikeMask:clear(app.pixelColor.rgba(0,0,0,255))
local regions={{{98,57},{127,16},{128,16},{128,36},{105,66}},{{85,55},{108,69},{106,74},{84,60}},{{92,68},{99,73},{86,90},{78,87}}}
local hand={{89,64},{96,64},{99,69},{97,77},{89,77},{87,71}}
for y=0,127 do for x=0,127 do local covered=false;for _,poly in ipairs(regions)do if inside(x,y,poly)then covered=true end end;if covered and not inside(x,y,hand)then strikeMask:drawPixel(x,y,app.pixelColor.rgba(255,255,255,255))end end end
strikeMask:saveAs(file(E..'/sword-strike-mask.png'))
local sprite=Sprite(128,128,ColorMode.RGB);sprite.layers[1].name='Raw PixelLab posed output; NOT production selection'
for i=0,7 do local s=app.open(file(E..string.format('/sword-posed/raw/%02d.png',i)));local im=Image(128,128,ColorMode.RGB);im:clear();im:drawSprite(s,1);s:close();if i>0 then sprite:newEmptyFrame()end;sprite:newCel(sprite.layers[1],i+1,im,Point(0,0))end
sprite:saveAs(file(E..'/sword-posed/raw.aseprite'));sprite:close()
