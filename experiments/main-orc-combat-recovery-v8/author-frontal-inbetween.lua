-- Programmatic pose authorship inside Aseprite. No blending or generated imagery.
local root='characters/orc-v1/source/'
local durations={30,65,35,50,45,35,30,35,35,100,55,80,45,90}
local function layer(s,n) for _,l in ipairs(s.layers) do if l.name==n then return l end end error(n) end
local function raster(s,n,f)
 local im=Image(256,256);im:clear();local c=layer(s,n):cel(f)
 if c then im:drawImage(c.image,c.position) end return im
end
local function save(im,p) app.fs.makeAllDirectories(app.fs.filePath(p));im:saveAs(p) end
local function render(s,i) local im=Image(s.width,s.height);im:clear();im:drawSprite(s,i);return im end
local function rgba(r,g,b) return app.pixelColor.rgba(r,g,b,255) end
for _,d in ipairs({'front_r','front_l'}) do
 local right=d=='front_r'
 local src=root..(right and 'combat-recovery-v7/frontal/full-front-r-sword' or 'combat-recovery-v8/frontal-armpit/front_l-sword')
 local out=root..'combat-recovery-v8/frontal-inbetween/'..d..'-sword'
 app.fs.makeAllDirectories(out..'/source')
 local s=app.open(src..'/source/composite.aseprite');assert(s)
 local b=raster(s,'body',7);local rest=raster(s,'body',1)
 -- Rebuild the cross-body upper limb at a higher elbow/wrist. Same-view torso
 -- restores the old limb footprint; palette and armour clusters stay inherited.
 local limb=Image(256,256);limb:clear()
 local x0=right and 108 or 95;local x1=right and 160 or 147
 for y=96,121 do for x=x0,x1 do
  if y<115 or (right and x>139 or not right and x<116) then
   limb:drawPixel(x,y,b:getPixel(x,y));b:drawPixel(x,y,rest:getPixel(x,y))
  end
 end end
 local dx=right and -20 or 20
 b:drawImage(limb,Point(dx,-12))
 -- Exclude torso/head fragments from the translated donor selection. Restore
 -- the same-view shoulder dome and head rather than retaining a rectangular cut.
 for y=0,95 do for x=0,255 do b:drawPixel(x,y,rest:getPixel(x,y)) end end
 -- Explicitly contour and shade a bent forearm bridge from the retained
 -- shoulder/elbow to the new wrist. Integer clusters, closed dark boundary.
 local shoulder=right and 111 or 144
 local wrist=right and 128 or 127
 for x=math.min(shoulder,wrist),math.max(shoulder,wrist) do
  local t=(x-shoulder)/(wrist-shoulder)
  local cy=math.floor(100+2*t)
  for dy=-4,4 do
   local col=math.abs(dy)==4 and rgba(12,15,18) or (dy==-3 and rgba(116,119,124) or (dy<0 and rgba(65,70,77) or rgba(33,38,45)))
   b:drawPixel(x,cy+dy,col)
  end
 end
 -- Sword is the existing rigid item, rotated by nearest source-pixel lookup
 -- in the editor, with a newly placed glove; no tween/cross-fade of body pixels.
 local oldGrip=right and 98 or 157
 local gx=right and 127 or 128;local gy=101
 local ang=math.rad(right and 16 or -16)
 local function transform(im)
  local o=Image(256,256);o:clear()
  for y=0,255 do for x=0,255 do
   local xx=x-gx;local yy=y-gy
   local sx=math.floor(oldGrip+xx*math.cos(ang)+yy*math.sin(ang)+0.5)
   local sy=math.floor(89-xx*math.sin(ang)+yy*math.cos(ang)+0.5)
   if sx>=0 and sx<256 and sy>=0 and sy<256 then o:drawPixel(x,y,im:getPixel(sx,sy)) end
  end end return o
 end
 local fresh={body=b}
 for _,n in ipairs({'weaponBack','weaponFront','handFront'}) do fresh[n]=transform(raster(s,n,6)) end
 s:newFrame(7)
 for _,n in ipairs({'weaponBack','body','weaponFront','handFront'}) do
  local l=layer(s,n);local c=l:cel(7);if c then s:deleteCel(c) end
  s:newCel(l,7,fresh[n],Point(0,0))
 end
 for i,t in ipairs(durations) do s.frames[i].duration=t/1000 end
 s:saveAs(out..'/source/composite.aseprite');s:close()
 s=app.open(out..'/source/composite.aseprite')
 local body=Sprite(256,256);body.layers[1].name='body'
 local hand=Sprite(256,256);hand.layers[1].name='handFront'
 local nat=Sprite(128,128);nat.layers[1].name='body'
 local cs=Image(256*14,256);cs:clear();local ns=Image(128*14,128);ns:clear()
 for i=1,14 do
  if i>1 then body:newEmptyFrame();hand:newEmptyFrame();nat:newEmptyFrame() end
  for _,v in ipairs({body,hand,nat}) do v.frames[i].duration=durations[i]/1000 end
  local bi=raster(s,'body',i);local hi=raster(s,'handFront',i)
  local ni=Image(128,128);ni:clear();ni:drawImage(bi,Point(-64,-64))
  body:newCel(body.layers[1],i,bi);hand:newCel(hand.layers[1],i,hi);nat:newCel(nat.layers[1],i,ni)
  local ix=string.format('%02d',i-1);local c=render(s,i)
  save(c,out..'/'..ix..'.png');save(c,out..'/frames/'..ix..'.png');save(ni,out..'/native/'..ix..'.png')
  for _,n in ipairs({'weaponBack','body','weaponFront','handFront'}) do save(raster(s,n,i),out..'/layers/'..n..'/'..ix..'.png') end
  cs:drawImage(c,Point((i-1)*256,0));ns:drawImage(ni,Point((i-1)*128,0))
 end
 body:saveAs(out..'/source/body.aseprite');hand:saveAs(out..'/source/hand.aseprite');nat:saveAs(out..'/source/native.aseprite')
 save(cs,out..'/composite-strip.png');save(ns,out..'/native-strip.png')
 body:close();hand:close();nat:close();s:close()
end
