local base='characters/orc-v1/source/combat-recovery-v8/'
local E='experiments/main-orc-combat-recovery-v8/qa-rear-arc/'
local pc=app.pixelColor
local function blank(w,h)local a=Image(w,h,ColorMode.RGB);a:clear();return a end
local function save(a,p)app.fs.makeAllDirectories(app.fs.filePath(p));a:saveAs(p)end
local function raster(s,l,i)local a=blank(256,256);local c=l:cel(i);if c then a:drawImage(c.image,c.position)end;return a end
local plans={back_r={[5]={-6,-3},[8]={9,-20},[9]={0,8}},back_l={[5]={-4,-2},[6]={3,2},[7]={8,6},[8]={5,-14},[9]={5,8}}}
for _,d in ipairs({'back_r','back_l'})do
 local src=base..'rear-inbetween/'..d..'-sword';local out=base..'rear-arc/'..d..'-sword'
 local f=assert(io.open(src..'/clip.json'));local c=json.decode(f:read('*a'));f:close()
 local s=app.open(src..'/source/composite.aseprite')
 for i=1,14 do local delta=plans[d][i-1];if delta then
  local dx,dy=delta[1],delta[2];local g=c.frames[i].rightGrip
  for _,l in ipairs(s.layers)do
   local old=raster(s,l,i);local a=blank(256,256)
   if l.name~='body' then a:drawImage(old,Point(dx,dy)) else
    -- Local, anchored limb repositioning in the editor. The shoulder and torso
    -- stay fixed; the distal gauntlet translates exactly with the sword grip.
    local function weight(x,y)
     if y>145 and x<154 then return 0 end; local r=math.sqrt((x-g[1])^2+(y-g[2])^2)
     if r<=12 then return 1 end
     local t=math.max(0,math.min(1,(r-12)/18));return 1-t*t*(3-2*t)
    end
    for y=0,255 do for x=0,255 do
     local sx,sy=x,y
     for k=1,16 do local w=weight(sx,sy);sx=x-dx*w;sy=y-dy*w end
     sx=math.floor(sx+.5);sy=math.floor(sy+.5)
     if sx>=0 and sx<256 and sy>=0 and sy<256 then a:drawPixel(x,y,old:getPixel(sx,sy))end
    end end
    -- All original light armour clusters are immutable, outside the dark glove.
    for y=0,255 do for x=0,255 do local p=old:getPixel(x,y)
     if pc.rgbaA(p)>0 and .2126*pc.rgbaR(p)+.7152*pc.rgbaG(p)+.0722*pc.rgbaB(p)>=160 then a:drawPixel(x,y,p)end
    end end
   end
   local cel=l:cel(i);if cel then s:deleteCel(cel)end;s:newCel(l,i,a,Point(0,0))
  end
 end end
 app.fs.makeAllDirectories(out..'/source');s:saveAs(out..'/source/composite.aseprite');s:close()
 s=app.open(out..'/source/composite.aseprite')
 local ns=Sprite(128,128);ns.layers[1].name='body'
 local bs=Sprite(256,256);bs.layers[1].name='body'
 local hs=Sprite(256,256);hs.layers[1].name='handFront'
 for i=1,14 do
  if i>1 then ns:newEmptyFrame();bs:newEmptyFrame();hs:newEmptyFrame()end
  for _,v in ipairs({ns,bs,hs})do v.frames[i].duration=s.frames[i].duration end
  for _,l in ipairs(s.layers)do local a=raster(s,l,i)
   if l.name=='body'then local n=blank(128,128);n:drawImage(a,Point(-64,-64));ns:newCel(ns.layers[1],i,n);bs:newCel(bs.layers[1],i,a)end
   if l.name=='handFront'then hs:newCel(hs.layers[1],i,a)end
  end
 end
 ns:saveAs(out..'/source/native.aseprite');bs:saveAs(out..'/source/body.aseprite');hs:saveAs(out..'/source/hand.aseprite');ns:close();bs:close();hs:close()
 ns=app.open(out..'/source/native.aseprite')
 local strip=blank(3584,256);local nstrip=blank(1792,128);local detail=blank(1536,256)
 for i=1,14 do local id=string.format('%02d',i-1);local a=blank(256,256);a:drawSprite(s,i);save(a,out..'/frames/'..id..'.png');strip:drawImage(a,Point((i-1)*256,0))
  if i>=6 and i<=11 then detail:drawImage(a,Point((i-6)*256,0))end
  for _,l in ipairs(s.layers)do save(raster(s,l,i),out..'/layers/'..l.name..'/'..id..'.png')end
  local n=blank(128,128);n:drawSprite(ns,i);save(n,out..'/native/'..id..'.png');nstrip:drawImage(n,Point((i-1)*128,0))
 end
 save(strip,out..'/composite-strip.png');save(nstrip,out..'/native-strip.png');detail:resize(6144,1024);save(detail,E..d..'-F05-F10-4x.png');ns:close();s:close()
end

