-- V6 rear: PixelLab whole-body foundations + local articulated arm pixel authorship.
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
local function inside(x,y,p)
 local yes=false;local j=#p
 for i=1,#p do local a,b=p[i],p[j];if ((a[2]>y)~=(b[2]>y)) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then yes=not yes end;j=i end
 return yes
end
local function poly(im,points,colors,mask)
 local minx,miny,maxx,maxy=127,127,0,0
 for _,p in ipairs(points) do minx=math.min(minx,p[1]);maxx=math.max(maxx,p[1]);miny=math.min(miny,p[2]);maxy=math.max(maxy,p[2]) end
 for y=math.max(0,math.floor(miny)-1),math.min(127,math.ceil(maxy)+1) do
  for x=math.max(0,math.floor(minx)-1),math.min(127,math.ceil(maxx)+1) do
   if inside(x+.5,y+.5,points) then
    local edge=not inside(x-1+.5,y+.5,points) or not inside(x+1+.5,y+.5,points) or not inside(x+.5,y-1+.5,points) or not inside(x+.5,y+1+.5,points)
    local n=1+((x*7+y*3)%#colors)
    im:drawPixel(x,y,edge and ink or colors[n]);if mask then mask:drawPixel(x,y,rgba(255,255,255)) end
   end
  end
 end
end
local function axis(a,b)
 local dx,dy=b[1]-a[1],b[2]-a[2];local len=math.sqrt(dx*dx+dy*dy)
 return dx/len,dy/len,-dy/len,dx/len
end
local function segment(im,a,b,wa,wb,cols)
 local ux,uy,nx,ny=axis(a,b)
 poly(im,{{a[1]+nx*wa,a[2]+ny*wa},{b[1]+nx*wb,b[2]+ny*wb},{b[1]-nx*wb,b[2]-ny*wb},{a[1]-nx*wa,a[2]-ny*wa}},cols)
 -- Reuse actual same-view arm material clusters, posed inside the new limb
 -- volume. This preserves the established mail/bracer material vocabulary.
 local length=math.sqrt((b[1]-a[1])^2+(b[2]-a[2])^2)
 for y=math.max(0,math.floor(math.min(a[2],b[2])-wa-2)),math.min(127,math.ceil(math.max(a[2],b[2])+wa+2)) do
  for x=math.max(0,math.floor(math.min(a[1],b[1])-wa-2)),math.min(127,math.ceil(math.max(a[1],b[1])+wa+2)) do
   local t=((x-a[1])*ux+(y-a[2])*uy)/length
   local cross=(x-a[1])*nx+(y-a[2])*ny;local width=wa+(wb-wa)*t
   if t>.06 and t<.94 and math.abs(cross)<width-1.4 then
    local sx=math.floor(88+cross*.7+.5)
    local sy=math.floor((cols==steel and 58 or 43)+t*(cols==steel and 16 or 15)+.5)
    local v=donor:getPixel(sx,sy)
    if pc.rgbaA(v)>0 then im:drawPixel(x,y,v) end
   end
  end
 end
 -- Directional steel facet, not a light exterior outline.
 if cols==steel then
  local aa={a[1]-nx*(wa-2),a[2]-ny*(wa-2)};local bb={b[1]-nx*(wb-2),b[2]-ny*(wb-2)}
  local len=math.sqrt((bb[1]-aa[1])^2+(bb[2]-aa[2])^2)
  for t=1,math.floor(len)-1 do local q=t/len;local x=math.floor(aa[1]+(bb[1]-aa[1])*q+.5);local y=math.floor(aa[2]+(bb[2]-aa[2])*q+.5);if x>=0 and x<128 and y>=0 and y<128 and pc.rgbaA(im:getPixel(x,y))>0 then im:drawPixel(x,y,steel[4]) end end
 end
end
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
for _,kind in ipairs({'Sword','Axe'}) do
 local k=kind:lower();local dest=C..'/back_l-'..k
 local poses=kind=='Sword' and sword or axe
 local req=read(E..'/'..k..'-request.json')
 local weaponDef=read('characters/orc-v1/source/combat-rescue-v5/combat/weapons/'..kind..'/weapon.json')
 local wsp=app.open(abs(weaponDef.master));local wi=blank(96,96);wi:drawSprite(wsp,1);wsp:close()
 local baseline=Image{fromFile=abs('characters/orc-v1/source/combat-rescue-v5/rear-grip-flash/full-back-l-sword/native/00.png')}
 local processed={};local frameInfo={};local cleaned=0
 for fi=1,12 do
  local body=Image{fromFile=abs(E..'/raw/'..k..'/'..string.format('%02d',fi-1)..'.png')}
  if fi==1 or fi==12 then body=Image(baseline) end
  local hfNative=blank(128,128);local p=poses[fi];local wx,wy,ex,ey=p[1],p[2],p[3],p[4]
  if fi>1 and fi<12 then
   -- Remove the generated RIGHT arm in exposed silhouette only. Preserve dorsal,
   -- skull and left anatomy. Native right dorsal boundary is x=79 at waist.
   for y=0,91 do for x=0,127 do
    local erase=(y<28 and x>=75) or (y>=28 and y<43 and x>=91) or (y>=43 and y<55 and x>=85) or (y>=55 and y<=86 and x>=80)
    if erase then body:drawPixel(x,y,0) end
   end end
   local shoulder={84,44}
   -- Whole-body PixelLab pose supplies torso/pelvis/knees. Upper arm and
   -- bracer are reconstructed as connected volumes under preserved pauldron.
   segment(body,shoulder,{ex,ey},5.6,4.6,{rgba(34,26,28),rgba(63,34,36),rgba(88,42,43),rgba(46,38,39)})
   segment(body,{ex,ey},{wx,wy},5.1,3.5,steel)
   local ux,uy,nx,ny=axis({ex,ey},{wx,wy})
   local glove={{wx+ux*4+nx*3.5,wy+uy*4+ny*3.5},{wx+ux*4-nx*3.5,wy+uy*4-ny*3.5},{wx-ux*4-nx*4,wy-uy*4-ny*4},{wx-ux*5+nx*3,wy-uy*5+ny*3}}
   local mask=blank(128,128);poly(body,glove,leather,mask)
   -- Knuckle ridge and thumb fold depend on this pose's forearm direction.
   local tx,ty=math.floor(wx+nx*2+.5),math.floor(wy+ny*2+.5)
   if tx>=0 and tx<128 and ty>=0 and ty<128 then body:drawPixel(tx,ty,leather[4]) end
   for y=0,127 do for x=0,127 do if pc.rgbaA(mask:getPixel(x,y))>0 then hfNative:drawPixel(x,y,body:getPixel(x,y)) end end end
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
   local gx,gy=wx+64,wy+64;local rad=p[5]*math.pi/180;local ca,sa=math.cos(rad),math.sin(rad)
   for y=0,255 do for x=0,255 do
    local dx,dy=x-gx,y-gy;local u=math.floor(ca*dx+sa*dy+weaponDef.grip[1]+.5);local v=math.floor(-sa*dx+ca*dy+weaponDef.grip[2]+.5)
    if u>=0 and u<96 and v>=0 and v<96 then local col=wi:getPixel(u,v);if pc.rgbaA(col)>0 then
     -- Handle behind pose-specific glove, independent blade in front.
     local layer=(v>=weaponDef.grip[2]-7) and wb or wf;layer:drawPixel(x,y,col)
    end end
   end end
   hf:drawImage(hfNative,Point(64,64))
  end
  processed[fi]={wb,body256,wf,hf};frameInfo[fi]={index=fi-1,durationMs=timings[kind][fi],phase=phases[fi],weaponVisible=visible,rightGrip=visible and {wx+64,wy+64} or false,rotationDeg=visible and p[5] or false,provenance=(fi==1 or fi==12) and 'V5 unarmed identity reference preserved' or 'PixelLab '..k..' raw frame '..(fi-1)..' + Aseprite local right-arm reauthor and edge cleanup'}
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

