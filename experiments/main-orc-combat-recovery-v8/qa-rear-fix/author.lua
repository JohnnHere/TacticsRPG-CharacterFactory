-- Local programmatic authorship inside Aseprite. Inherited same-view V8 pixels.
-- Distal articulation only: torso, pauldron, head, legs and timing preserved.
local root=app.fs.currentPath
local E='experiments/main-orc-combat-recovery-v8/qa-rear-fix'
local src='characters/orc-v1/source/combat-recovery-v8/rear/back_r-sword'
local dst='characters/orc-v1/source/combat-recovery-v8/rear-fix/back_r-sword'
local function abs(p)return app.fs.joinPath(root,p)end
local function read(p)local f=assert(io.open(abs(p),'r'));local t=json.decode(f:read('*a'));f:close();return t end
local function blank(w,h)local a=Image(w,h,ColorMode.RGB);a:clear();return a end
local function save(a,p)app.fs.makeAllDirectories(app.fs.filePath(abs(p)));a:saveAs(abs(p))end
local function load(p)return Image{fromFile=abs(p)}end
local pc=app.pixelColor
local function inside(x,y,p)local hit=false;local j=#p;for i=1,#p do local a,b=p[i],p[j];if(a[2]>y)~=(b[2]>y)and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1]then hit=not hit end;j=i end;return hit end
local edits={
 [5]={pivot={163,105},degrees=-4,poly={{154,78},{180,78},{180,106},{163,110},{154,101}}},
 [6]={pivot={166,121},degrees=18,poly={{166,105},{190,105},{190,140},{166,140}}},
 [10]={pivot={162,135},degrees=-15,poly={{158,131},{178,129},{180,165},{160,165},{159,151}}}
}
local function rotate(a,p,deg)
 local b=blank(256,256);local r=deg*math.pi/180;local ca,sa=math.cos(r),math.sin(r)
 for y=0,255 do for x=0,255 do local dx,dy=x-p[1],y-p[2];local u=math.floor(p[1]+ca*dx+sa*dy+.5);local v=math.floor(p[2]-sa*dx+ca*dy+.5)
 if u>=0 and u<256 and v>=0 and v<256 then b:drawPixel(x,y,a:getPixel(u,v))end end end
 return b
end
local names={'weaponBack','body','weaponFront','handFront'};local old=read(src..'/clip.json');local processed={};local log={}
for fi,f in ipairs(old.frames)do
 local ims={};for j,n in ipairs(names)do ims[j]=load(f.layers[n].png)end
 local q=edits[fi-1]
 if q then
  local arm=blank(256,256)
  for y=0,255 do for x=0,255 do if inside(x+.5,y+.5,q.poly)then arm:drawPixel(x,y,ims[2]:getPixel(x,y));ims[2]:drawPixel(x,y,0)end end end
  ims[2]:drawImage(rotate(arm,q.pivot,q.degrees),Point(0,0))
  for _,j in ipairs({1,3,4})do ims[j]=rotate(ims[j],q.pivot,q.degrees)end
  local dx,dy=f.rightGrip[1]-q.pivot[1],f.rightGrip[2]-q.pivot[2];local r=q.degrees*math.pi/180
  q.rightGrip={q.pivot[1]+math.cos(r)*dx-math.sin(r)*dy,q.pivot[2]+math.sin(r)*dx+math.cos(r)*dy}
 end
 processed[fi]=ims;log[fi]={index=fi-1,edit=q or false}
end
local sp=Sprite(256,256,ColorMode.RGB);local ls={}
for j,n in ipairs(names)do local l=j==1 and sp.layers[1]or sp:newLayer();l.name=n;ls[j]=l end
local ns=Sprite(128,128,ColorMode.RGB);ns.layers[1].name='body'
for fi,f in ipairs(old.frames)do
 if fi>1 then sp:newEmptyFrame();ns:newEmptyFrame()end
 sp.frames[fi].duration=f.durationMs/1000;ns.frames[fi].duration=f.durationMs/1000
 for j=1,4 do sp:newCel(ls[j],fi,processed[fi][j],Point(0,0))end
 local n=blank(128,128);n:drawImage(processed[fi][2],Point(-64,-64));ns:newCel(ns.layers[1],fi,n,Point(0,0))
end
app.fs.makeAllDirectories(abs(dst..'/source'));sp:newTag(1,13).name='Attack';ns:newTag(1,13).name='Attack'
sp:saveAs(abs(dst..'/source/composite.aseprite'));ns:saveAs(abs(dst..'/source/native.aseprite'));sp:close();ns:close()
sp=app.open(abs(dst..'/source/composite.aseprite'));ns=app.open(abs(dst..'/source/native.aseprite'))
local strip=blank(256*13,256);local nstrip=blank(128*13,128);local detail=blank(256*4,256)
for fi,f in ipairs(old.frames)do
 assert(math.abs(sp.frames[fi].duration*1000-f.durationMs)<.1)
 assert(math.abs(ns.frames[fi].duration*1000-f.durationMs)<.1)
 local id=string.format('%02d',fi-1);local a=blank(256,256);a:drawSprite(sp,fi);save(a,dst..'/frames/'..id..'.png');strip:drawImage(a,Point((fi-1)*256,0))
 if fi>=5 and fi<=8 then detail:drawImage(a,Point((fi-5)*256,0))end
 for j,l in ipairs(sp.layers)do local c=l:cel(fi);local b=blank(256,256);if c then b:drawImage(c.image,c.position)end;save(b,dst..'/layers/'..l.name..'/'..id..'.png')end
 local n=blank(128,128);n:drawSprite(ns,fi);save(n,dst..'/native/'..id..'.png');nstrip:drawImage(n,Point((fi-1)*128,0))
end
save(strip,dst..'/composite-strip.png');save(nstrip,dst..'/native-strip.png');detail:resize(4096,1024);save(detail,E..'/F04-F07-4x.png')
sp:close();ns:close();local f=assert(io.open(abs(E..'/author-result.json'),'w'));f:write(json.encode({frames=log,mastersSavedReopened=true,author='Aseprite Lua local articulation',generationCalls=0}));f:close()
