-- Mechanical transplant of validated normalized bookends. No artistic edits.
local root=app.fs.currentPath;local E='experiments/main-orc-combat-recovery-v7/rear-r-flashfixed';local C='characters/orc-v1/source/combat-recovery-v7/rear-r-flashfixed'
local function abs(p)return app.fs.joinPath(root,p)end
local function read(p)local f=assert(io.open(abs(p),'r'));local v=json.decode(f:read('*a'));f:close();return v end
local function blank(w,h)local a=Image(w,h,ColorMode.RGB);a:clear();return a end
local function load(p)return Image{fromFile=abs(p)}end
local function save(a,p)app.fs.makeAllDirectories(app.fs.filePath(abs(p)));a:saveAs(abs(p))end
local function eq(a,b)assert(a.width==b.width and a.height==b.height);for y=0,a.height-1 do for x=0,a.width-1 do local u,v=a:getPixel(x,y),b:getPixel(x,y);assert(u==v or(app.pixelColor.rgbaA(u)==0 and app.pixelColor.rgbaA(v)==0),'RGBA mismatch')end end end
local function crop(a)local b=blank(128,128);b:drawImage(a,Point(-64,-64));return b end
local normalized={load('characters/orc-v1/source/combat-recovery-v7/bookends/back_r-sword/layers/body/00.png'),load('characters/orc-v1/source/combat-recovery-v7/bookends/back_r-sword/layers/body/11.png')}
local result={}
for _,kind in ipairs({'sword','axe'})do
 local dst=C..'/back_r-'..kind;local old=read(dst..'/clip.json');assert(old.frameCount==12)
 local sp=app.open(abs(dst..'/source/composite.aseprite'));local ns=app.open(abs(dst..'/source/native.aseprite'));local bl=nil
 for _,l in ipairs(sp.layers)do if l.name=='body'then bl=l end end;assert(bl)
 for j,fi in ipairs({1,12})do
  local c=bl:cel(fi);if c then sp:deleteCel(c)end;sp:newCel(bl,fi,normalized[j],Point(0,0))
  local n=ns.layers[1]:cel(fi);if n then ns:deleteCel(n)end;ns:newCel(ns.layers[1],fi,crop(normalized[j]),Point(0,0))
 end
 sp:saveAs(abs(dst..'/source/composite.aseprite'));ns:saveAs(abs(dst..'/source/native.aseprite'));sp:close();ns:close()
 -- Separate body256 master is explicit, rather than mislabelling native128.
 sp=app.open(abs(dst..'/source/composite.aseprite'));local bs=Sprite(256,256,ColorMode.RGB);bs.layers[1].name='body'
 local layer=nil;for _,l in ipairs(sp.layers)do if l.name=='body'then layer=l end end
 for fi=1,12 do if fi>1 then bs:newEmptyFrame()end;bs.frames[fi].duration=sp.frames[fi].duration;local c=layer:cel(fi);local a=blank(256,256);if c then a:drawImage(c.image,c.position)end;bs:newCel(bs.layers[1],fi,a,Point(0,0))end
 bs:newTag(1,12).name='Attack';bs:saveAs(abs(dst..'/source/body.aseprite'));bs:close();sp:close()
 sp=app.open(abs(dst..'/source/composite.aseprite'));ns=app.open(abs(dst..'/source/native.aseprite'));bs=app.open(abs(dst..'/source/body.aseprite'))
 local strip=blank(256*12,256);local nstrip=blank(128*12,128);local frames={}
 for fi=1,12 do
  local index=fi-1;local id=string.format('%02d',index);local f=old.frames[fi];assert(math.abs(sp.frames[fi].duration*1000-f.durationMs)<.1);assert(math.abs(ns.frames[fi].duration*1000-f.durationMs)<.1);assert(math.abs(bs.frames[fi].duration*1000-f.durationMs)<.1)
  local isBook=fi==1 or fi==12;local expectedBody=isBook and normalized[fi==1 and 1 or 2]or load(f.layers.body.png)
  local layerMeta={}
  for _,l in ipairs(sp.layers)do
   local a=blank(256,256);local c=l:cel(fi);if c then a:drawImage(c.image,c.position)end
   local expected=l.name=='body'and expectedBody or load(f.layers[l.name].png);eq(a,expected)
   save(a,E..'/master-reexport/'..kind..'/layers/'..l.name..'/'..id..'.png')
   if isBook and l.name=='body'then save(a,dst..'/layers/body/'..id..'.png')end
   layerMeta[#layerMeta+1]={name=l.name,celPosition=c and{c.position.x,c.position.y}or false}
  end
  local a=blank(256,256);a:drawSprite(sp,fi);local n=blank(128,128);n:drawSprite(ns,fi);local b=blank(256,256);b:drawSprite(bs,fi);eq(b,expectedBody);eq(n,crop(expectedBody))
  if isBook then eq(a,expectedBody);save(a,dst..'/frames/'..id..'.png');save(n,dst..'/native/'..id..'.png')else eq(a,load(f.png));eq(n,load(f.nativePng))end
  save(a,E..'/master-reexport/'..kind..'/frames/'..id..'.png');save(n,E..'/master-reexport/'..kind..'/native/'..id..'.png');save(b,E..'/master-reexport/'..kind..'/body/'..id..'.png')
  strip:drawImage(a,Point(index*256,0));nstrip:drawImage(n,Point(index*128,0));frames[#frames+1]={index=index,durationMs=sp.frames[fi].duration*1000,layers=layerMeta}
 end
 save(strip,dst..'/composite-strip.png');save(nstrip,dst..'/native-strip.png');sp:close();ns:close();bs:close()
 result[kind]={mastersReopenedReexported=3,rgbaAndTimingVerified=true,frames=frames}
end
local f=assert(io.open(abs(E..'/master-verification.json'),'w'));f:write(json.encode(result));f:close()
