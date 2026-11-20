local root='.'
local out=root..'/characters/orc-v1/source/combat-rescue-v5/body-specialist'
local exp=root..'/experiments/main-orc-combat-rescue-v5/body-specialist'
local names={'01-hoist','02-apex','03-impact'}
for i,name in ipairs(names) do
 local raw=Image{fromFile=exp..(i<3 and '/edited-key-'..i..'.png' or '/raw-key-3.png')}
 local maxY=-1
 for y=0,raw.height-1 do for x=0,raw.width-1 do if app.pixelColor.rgbaA(raw:getPixel(x,y))>0 then maxY=math.max(maxY,y) end end end
 local dy=126-maxY
 local n=Sprite(128,128,ColorMode.RGB)
 n.layers[1].name='body'
 n.frames[1].duration=0.160
 local img=Image(128,128,ColorMode.RGB)
 img:drawImage(raw,Point(0,dy))
 -- Local Aseprite finishing: restore the four-pixel rounded fist outline cap
 -- after whole-sprite ground registration (+2); no limb transform/collage.
 if i==1 then img:drawPixel(26,59+dy,app.pixelColor.rgba(48,39,45,255)) end
 if i==2 then for x=77,80 do img:drawPixel(x,dy-1,app.pixelColor.rgba(12,9,15,255)) end end
 n:newCel(n.layers[1],1,img,Point(0,0))
 n:saveAs(out..'/'..name..'-native.aseprite')
 app.command.SaveFileAs{ui=false,filename=out..'/'..name..'-native.png'}
 local c=Sprite(256,256,ColorMode.RGB)
 c.layers[1].name='body'
 c.frames[1].duration=0.160
 c:newCel(c.layers[1],1,img,Point(64,64))
 c:saveAs(out..'/'..name..'-composite.aseprite')
 app.command.SaveFileAs{ui=false,filename=out..'/'..name..'-composite.png'}
 n:close();c:close()
end
