-- Local experiment only. Authorship and raster transformation inside Aseprite.
local E='experiments/main-orc-skeleton-02/stage-bcde/'
local src='characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/'
local pc=app.pixelColor
local function blank()local a=Image(256,256,ColorMode.RGB);a:clear();return a end
local function save(a,p)app.fs.makeAllDirectories(app.fs.filePath(E..p));a:saveAs(E..p)end
local weapon=Image{fromFile='characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/recruit-sword.png'}
local plans={{0,158,145,20},{5,160,81,0},{8,178,131,-138.65},{9,169,159,-131.35},{13,158,145,20}}
for _,q in ipairs(plans)do
 local id=string.format('%02d',q[1]);local body=Image{fromFile=src..'layers/body/'..id..'.png'}
 local hand=Image{fromFile=src..'layers/handFront/'..id..'.png'}
 local wb,wf=blank(),blank();local a=q[4]*math.pi/180;local ca,sa=math.cos(a),math.sin(a)
 for y=0,255 do for x=0,255 do
  local dx,dy=x-q[2],y-q[3];local u=math.floor(ca*dx+sa*dy+48+.5);local v=math.floor(-sa*dx+ca*dy+66+.5)
  if u>=0 and u<96 and v>=0 and v<96 then local c=weapon:getPixel(u,v)
   if pc.rgbaA(c)>0 then (v>=60 and v<=73 and wb or wf):drawPixel(x,y,c)end
  end
 end end
 -- Endpoints were unarmed in runtime. Retain the very same closed glove as
 -- foreground occluder, restricted to the existing glove cluster (no new palette).
 if q[1]==0 or q[1]==13 then
  for y=139,153 do for x=151,163 do local c=body:getPixel(x,y);if pc.rgbaA(c)>0 then hand:drawPixel(x,y,c)end end end
 end
 local w=blank();w:drawImage(wb);w:drawImage(wf)
 local composite=blank();composite:drawImage(wb);composite:drawImage(body);composite:drawImage(wf);composite:drawImage(hand)
 save(body,'body-only/'..id..'.png');save(w,'weapon-only/'..id..'.png');save(composite,'composite/'..id..'.png')
 local sp=Sprite(256,256,ColorMode.RGB)
 for j,n in ipairs({'weaponBack','body','weaponFront','handFront'})do local l=j==1 and sp.layers[1]or sp:newLayer();l.name=n;sp:newCel(l,1,({wb,body,wf,hand})[j],Point(0,0))end
 app.fs.makeAllDirectories(E..'source');sp:saveAs(E..'source/'..id..'.aseprite');sp:close()
 local reopened=app.open(E..'source/'..id..'.aseprite');local r=blank();r:drawSprite(reopened,1);save(r,'composite/'..id..'.png');reopened:close()
end
