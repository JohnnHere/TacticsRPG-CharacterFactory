-- V6 rear reference2: PixelLab full-body pose authorship; Aseprite surgical finishing.
-- Runs only in Aseprite. No external raster authorship. Coordinates are native.
local E='experiments/main-orc-artistic-reconstruction-v6/rear'
local C='characters/orc-v1/source/artistic-reconstruction-v6/rear'
local function abs(p) return app.fs.joinPath(app.fs.currentPath,p) end
local function read(p) local f=assert(io.open(abs(p),'r'));local s=f:read('*a');f:close();return json.decode(s) end
local function blank(w,h) local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function save(im,p) app.fs.makeAllDirectories(app.fs.filePath(abs(p)));im:saveAs(abs(p)) end
local pc=app.pixelColor
local function rgba(r,g,b) return pc.rgba(r,g,b,255) end
local ink=rgba(12,15,18)
local steel={rgba(24,29,34),rgba(38,43,48),rgba(54,60,64),rgba(74,81,84),rgba(101,108,109)}
local leather={rgba(32,21,23),rgba(49,31,29),rgba(68,43,35),rgba(88,57,43)}
local donor=Image{fromFile=abs('characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/full-back-l-sword/native/00.png')}
local sword={
 {90,76,89,58,0},{95,60,94,45,-30},{101,42,95,42,-25},{99,28,95,47,-15},
 {105,36,98,51,30},{112,50,99,59,70},{108,69,95,58,110},{96,86,88,65,145},
 {86,92,87,68,175},{88,84,89,63,185},{90,78,89,58,0},{90,76,89,58,0}}
local axe={
 {90,76,89,58,0},{99,57,96,43,-25},{102,34,97,50,-25},{93,20,96,43,-15},
 {87,19,95,43,-5},{99,32,98,53,20},{105,58,98,47,65},{95,84,92,62,115},
 {91,91,90,69,145},{93,81,91,61,155},{91,79,90,58,0},{90,76,89,58,0}}
local timings={Sword={90,80,80,110,50,40,40,80,100,90,90,100},Axe={100,100,110,140,150,60,50,100,140,130,110,130}}
local phases={'guard','anticipation-load','anticipation-lift','chamber','loaded-apex','acceleration','descent','impact','follow-through','recovery-release','recovery-settle','guard-return'}
local receipts={}
local anatomy=read(E..'/anatomy-plan.json')
for _,kind in ipairs({'Sword','Axe'}) do
 local k=kind:lower();local dest=C..'/back_l-'..k
 local poses=kind=='Sword' and sword or axe
 local req=read(E..'/'..k..'-reference2-request.json')
 local weaponDef=read('characters/orc-v1/source/combat-rescue-v5/combat/weapons/'..kind..'/weapon.json')
 local wsp=app.open(abs(weaponDef.master));local wi=blank(96,96);wi:drawSprite(wsp,1);wsp:close()
 local baseline=Image{fromFile=abs('characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/full-back-l-sword/native/00.png')}
 local processed={};local frameInfo={};local cleaned=0
 for fi=1,12 do
  local body=Image{fromFile=abs(E..'/raw-reference2/'..k..'/'..string.format('%02d',fi-1)..'.png')}
  if fi==1 or fi==12 then body=Image(baseline) end
  local hfNative=blank(128,128);local p=poses[fi];local wx,wy,ex,ey=p[1],p[2],p[3],p[4]
  if fi>1 and fi<12 then
   -- Extract each genuinely generated pose's own glove. No reused hand stamp.
   local plan=anatomy[kind][fi]
   wx,wy=plan.grip[1],plan.grip[2]
   for _,row in ipairs(plan.rows) do
    for x=row[2],row[3] do
     local pixel=body:getPixel(x,row[1])
     assert(pc.rgbaA(pixel)>0,'Glove mask outside visible anatomy')
     hfNative:drawPixel(x,row[1],pixel)
    end
   end
  end
  -- Surgical edge cleanup inside Aseprite. Reject fractional alpha and darken
  -- generated bright neutral exterior pixels; retain interior metal lighting.
  local original=Image(body)
  for y=0,127 do for x=0,127 do
   local v=original:getPixel(x,y);local a=pc.rgbaA(v)
   if a>0 then
    local r,g,b=pc.rgbaR(v),pc.rgbaG(v),pc.rgbaB(v);local edge=false
    for _,d in ipairs({{-1,0},{1,0},{0,-1},{0,1}}) do local xx,yy=x+d[1],y+d[2];if xx<0 or xx>127 or yy<0 or yy>127 or pc.rgbaA(original:getPixel(xx,yy))==0 then edge=true end end
    if fi>1 and fi<12 and edge and math.max(r,g,b)-math.min(r,g,b)<28 and math.max(r,g,b)>85 then body:drawPixel(x,y,ink);cleaned=cleaned+1
    elseif a<128 then body:drawPixel(x,y,0)
    elseif a<255 then body:drawPixel(x,y,rgba(r,g,b)) end
   end
  end end
  local body256=blank(256,256);body256:drawImage(body,Point(64,64))
  local wb,wf,hf=blank(256,256),blank(256,256),blank(256,256)
  local visible=fi>=2 and fi<=10
  if visible then
   local gx,gy=wx+64,wy+64;local rad=anatomy[kind][fi].angle*math.pi/180;local ca,sa=math.cos(rad),math.sin(rad)
   for y=0,255 do for x=0,255 do
    local dx,dy=x-gx,y-gy;local u=math.floor(ca*dx+sa*dy+weaponDef.grip[1]+.5);local v=math.floor(-sa*dx+ca*dy+weaponDef.grip[2]+.5)
    if u>=0 and u<96 and v>=0 and v<96 then local col=wi:getPixel(u,v);if pc.rgbaA(col)>0 then
     -- Handle behind pose-specific glove, independent blade in front.
     local layer=(v>=weaponDef.grip[2]-7) and wb or wf;layer:drawPixel(x,y,col)
    end end
   end end
   hf:drawImage(hfNative,Point(64,64))
  end
  processed[fi]={wb,body256,wf,hf};frameInfo[fi]={index=fi-1,durationMs=timings[kind][fi],phase=phases[fi],weaponVisible=visible,rightGrip=visible and {wx+64,wy+64} or false,rotationDeg=visible and anatomy[kind][fi].angle or false,provenance=(fi==1 or fi==12) and 'V5 unarmed identity reference preserved' or 'PixelLab '..k..' reference2 frame '..(fi-1)..' + Aseprite edge cleanup and pose-specific glove occlusion'}
 end
 local names={'weaponBack','body','weaponFront','handFront'}
 app.fs.makeAllDirectories(abs(dest..'/source'))
 local sp=Sprite(256,256,ColorMode.RGB);local ls={}
 for i,n in ipairs(names) do local l=i==1 and sp.layers[1] or sp:newLayer();l.name=n;ls[i]=l end
 for fi=1,12 do if fi>1 then sp:newEmptyFrame() end;sp.frames[fi].duration=timings[kind][fi]/1000
  for j=1,4 do sp:newCel(ls[j],fi,processed[fi][j],Point(0,0)) end
 end
 sp:newTag(1,12).name='Attack';sp:saveAs(abs(dest..'/source/composite.aseprite'));sp:close()
 local native=Sprite(128,128,ColorMode.RGB);native.layers[1].name='body'
 for fi=1,12 do if fi>1 then native:newEmptyFrame() end;native.frames[fi].duration=timings[kind][fi]/1000;local crop=blank(128,128);crop:drawImage(processed[fi][2],Point(-64,-64));native:newCel(native.layers[1],fi,crop,Point(0,0)) end
 native:newTag(1,12).name='Attack';native:saveAs(abs(dest..'/source/native.aseprite'));native:close()
 -- Reopen BOTH saved masters; compare RGBA and durations, including cel.position.
 local saved=app.open(abs(dest..'/source/composite.aseprite'));local ns=app.open(abs(dest..'/source/native.aseprite'))
 local function equal(a,b)
  assert(a.width==b.width and a.height==b.height)
  for y=0,a.height-1 do for x=0,a.width-1 do local aa,bb=a:getPixel(x,y),b:getPixel(x,y);assert(aa==bb or (pc.rgbaA(aa)==0 and pc.rgbaA(bb)==0),'RGBA mismatch') end end
 end
 for fi=1,12 do
  assert(math.abs(saved.frames[fi].duration*1000-timings[kind][fi])<.1);assert(math.abs(ns.frames[fi].duration*1000-timings[kind][fi])<.1)
  local ix=string.format('%02d',fi-1);local comp=blank(256,256);comp:drawSprite(saved,fi);save(comp,dest..'/frames/'..ix..'.png')
  for j,l in ipairs(saved.layers) do local im=blank(256,256);local cel=l:cel(fi);if cel then im:drawImage(cel.image,cel.position) end;equal(im,processed[fi][j]);save(im,dest..'/layers/'..l.name..'/'..ix..'.png') end
  local ni=blank(128,128);ni:drawSprite(ns,fi);local crop=blank(128,128);crop:drawImage(processed[fi][2],Point(-64,-64));equal(ni,crop);save(ni,dest..'/native/'..ix..'.png')
 end
 saved:close();ns:close()
 receipts[kind]={frames=frameInfo,cleanedExteriorPixels=cleaned,mastersSavedReopened=true,pixelsAndTimingVerified=true,canvas={256,256},nativeCanvas={128,128}}
end
local f=assert(io.open(abs(E..'/author-result.json'),'w'));f:write(json.encode(receipts));f:close()

