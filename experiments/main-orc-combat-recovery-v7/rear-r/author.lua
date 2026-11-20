-- Programmatic surgical pixel authorship in Aseprite; V6 pixels inherited.
local root=app.fs.currentPath
local E='experiments/main-orc-combat-recovery-v7/rear-r'
local function abs(p)return app.fs.joinPath(root,p)end
local function read(p)local f=assert(io.open(abs(p),'r'));local v=json.decode(f:read('*a'));f:close();return v end
local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function save(im,p)app.fs.makeAllDirectories(app.fs.filePath(abs(p)));im:saveAs(abs(p))end
local function load(p)return Image{fromFile=abs(p)}end
local pc=app.pixelColor
local function col(r,g,b)return pc.rgba(r,g,b,255)end
local ink=col(12,15,18);local shadow=col(31,22,24);local leather=col(65,39,35);local ridge=col(91,56,45);local metal=col(38,43,48)
local plan=read(E..'/plan.json');local results={}
local names={'weaponBack','body','weaponFront','handFront'}
local function eq(a,b)
 for y=0,a.height-1 do for x=0,a.width-1 do local u,v=a:getPixel(x,y),b:getPixel(x,y);assert(u==v or(pc.rgbaA(u)==0 and pc.rgbaA(v)==0),'RGBA mismatch')end end
end
for _,kind in ipairs({'Sword','Axe'}) do
 local v=plan[kind];local dst=v.dest;local processed={};local log={}
 for fi,f in ipairs(v.clip.frames)do
  local p=v.frames[fi];local ims={}
  for j,n in ipairs(names)do ims[j]=load(f.layers[n].png)end
  local body=ims[2];local edits={};local rad=p.angle*math.pi/180;local ca,sa=math.cos(rad),math.sin(rad)
  if f.weaponVisible then
   -- Translate item only to the observed palm interior; retain exact angle/geometry.
   for _,j in ipairs({1,3})do local shifted=blank(256,256);shifted:drawImage(ims[j],Point(p.shift[1],p.shift[2]));ims[j]=shifted end
   local gx,gy=p.grip[1],p.grip[2]
   -- Per-pose existing anatomical glove rows bound every edit, preserving cuff,
   -- elbow and the entire rest of the body. Curl profiles follow each hand's
   -- own silhouette; three narrow knuckle ridges cross the haft, thumb hooks.
   local mask={}
   for _,r in ipairs(p.rows)do for x=r[2],r[3]do mask[(r[1]+64)*256+x+64]=true end end
   for y=gy-7,gy+7 do for x=gx-8,gx+8 do
    local dx,dy=x-gx,y-gy;local n=ca*dx+sa*dy;local t=-sa*dx+ca*dy
    if mask[y*256+x] and pc.rgbaA(body:getPixel(x,y))>0 then
     -- Rounded closed fingers across both sides; no detached rectangular stamp.
     local radius=kind=='Axe' and 4.3 or 3.8
     if n*n/(radius*radius)+t*t/7.8<=1 then
      local c=leather
      if math.abs(n)>radius-1 or t>1.8 then c=shadow end
      if (math.floor(t+3)%2==0)and n> -2.5 and n<2.8 then c=ridge end
      if n>1.6 and t<0 then c=shadow end
      -- Thumb closes diagonally across finger pads at the blade side.
      if n>=0 and n<=3 and t>=-2.2 and t<=-.5 and n+t<1.8 then c=ridge end
      if c~=body:getPixel(x,y)then edits[#edits+1]={x,y,body:getPixel(x,y),c};body:drawPixel(x,y,c)end
     end
    end
   end end
   -- Rebuild handFront from this finished hand, never copy raw bright pixels.
   local hf=blank(256,256)
   for _,r in ipairs(p.rows)do for x=r[2],r[3]do hf:drawPixel(x+64,r[1]+64,body:getPixel(x+64,r[1]+64))end end
   ims[4]=hf
  end
  local halo={}
  for _,xy in ipairs(p.bodyHaloCandidates)do
   local x,y=xy[1],xy[2];halo[#halo+1]={layer='body',x=x,y=y,before=body:getPixel(x,y),after=ink};body:drawPixel(x,y,ink)
   if pc.rgbaA(ims[4]:getPixel(x,y))>0 then ims[4]:drawPixel(x,y,ink)end
  end
  -- Semantic weapon silhouette only: a bright exposed perimeter is re-inked,
  -- leaving all interior metal highlights unchanged. Snapshot avoids cascading.
  for _,j in ipairs({1,3})do local original=Image(ims[j])
   for y=1,254 do for x=1,254 do local c=original:getPixel(x,y)
    if pc.rgbaA(c)>0 and math.min(pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c))>=140 then
     local edge=false
     for _,d in ipairs({{-1,0},{1,0},{0,-1},{0,1}})do
      if pc.rgbaA(original:getPixel(x+d[1],y+d[2]))==0 then edge=true end
     end
     if edge then halo[#halo+1]={layer=names[j],x=x,y=y,before=c,after=metal};ims[j]:drawPixel(x,y,metal)end
    end
   end end
  end
  processed[fi]=ims;log[fi]={index=fi-1,grip=p.grip,bodyGripEdits=edits,contourEdits=halo}
 end
 app.fs.makeAllDirectories(abs(dst..'/source'))
 local sp=Sprite(256,256,ColorMode.RGB);local ls={}
 for j,n in ipairs(names)do local l=j==1 and sp.layers[1]or sp:newLayer();l.name=n;ls[j]=l end
 for fi,f in ipairs(v.clip.frames)do if fi>1 then sp:newEmptyFrame()end;sp.frames[fi].duration=f.durationMs/1000
  for j=1,4 do sp:newCel(ls[j],fi,processed[fi][j],Point(0,0))end
 end
 sp:newTag(1,#v.clip.frames).name='Attack';sp:saveAs(abs(dst..'/source/composite.aseprite'));sp:close()
 local ns=Sprite(128,128,ColorMode.RGB);ns.layers[1].name='body'
 for fi,f in ipairs(v.clip.frames)do if fi>1 then ns:newEmptyFrame()end;ns.frames[fi].duration=f.durationMs/1000;local im=blank(128,128);im:drawImage(processed[fi][2],Point(-64,-64));ns:newCel(ns.layers[1],fi,im,Point(0,0))end
 ns:newTag(1,#v.clip.frames).name='Attack';ns:saveAs(abs(dst..'/source/native.aseprite'));ns:close()
 sp=app.open(abs(dst..'/source/composite.aseprite'));ns=app.open(abs(dst..'/source/native.aseprite'))
 local strip=blank(256*#v.clip.frames,256);local nstrip=blank(128*#v.clip.frames,128)
 for fi,f in ipairs(v.clip.frames)do
  assert(math.abs(sp.frames[fi].duration*1000-f.durationMs)<.1);assert(math.abs(ns.frames[fi].duration*1000-f.durationMs)<.1)
  local id=string.format('%02d',fi-1);local im=blank(256,256);im:drawSprite(sp,fi);save(im,dst..'/frames/'..id..'.png');strip:drawImage(im,Point((fi-1)*256,0))
  for j,l in ipairs(sp.layers)do local c=l:cel(fi);local a=blank(256,256);if c then a:drawImage(c.image,c.position)end;eq(a,processed[fi][j]);save(a,dst..'/layers/'..l.name..'/'..id..'.png')end
  local ni=blank(128,128);ni:drawSprite(ns,fi);local crop=blank(128,128);crop:drawImage(processed[fi][2],Point(-64,-64));eq(ni,crop);save(ni,dst..'/native/'..id..'.png');nstrip:drawImage(ni,Point((fi-1)*128,0))
  if f.weaponVisible then
   local p=v.frames[fi];local gx,gy=p.grip[1],p.grip[2]
   if kind=='Axe' and(fi==4 or fi==5 or fi==8)then
    for _,which in ipairs({'before','after'})do
     local source=which=='before'and load(f.png)or im
     local cx,cy=gx,gy;if which=='before'then cx,cy=f.rightGrip[1],f.rightGrip[2]end
     local crop=blank(40,40);crop:drawImage(source,Point(20-cx,20-cy));crop:resize(640,640);save(crop,E..'/grip-'..id..'-'..which..'.png')
    end
   end
  end
 end
 save(strip,dst..'/composite-strip.png');save(nstrip,dst..'/native-strip.png');sp:close();ns:close()
 results[kind]={frames=log,mastersSavedReopened=true,rgbaAndDurationVerified=true,authoring='Aseprite Lua over inherited V6 pixels; zero PixelLab calls'}
end
local f=assert(io.open(abs(E..'/author-result.json'),'w'));f:write(json.encode(results));f:close()
