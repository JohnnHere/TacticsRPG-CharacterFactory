-- Assemble four rear clips ONLY after validating the frontal-derived phase map.
local root=app.fs.currentPath;local E='experiments/main-orc-combat-recovery-v8/rear'
local function abs(p)return app.fs.joinPath(root,p)end
local function read(p)local f=assert(io.open(abs(p),'r'));local a=json.decode(f:read('*a'));f:close();return a end
local function blank(w,h)local a=Image(w,h,ColorMode.RGB);a:clear();return a end
local function load(p)return Image{fromFile=abs(p)}end
local function save(a,p)app.fs.makeAllDirectories(app.fs.filePath(abs(p)));a:saveAs(abs(p))end
local function crop(a)local n=blank(128,128);n:drawImage(a,Point(-64,-64));return n end
local function eq(a,b)for y=0,a.height-1 do for x=0,a.width-1 do local u,v=a:getPixel(x,y),b:getPixel(x,y);assert(u==v or(app.pixelColor.rgbaA(u)==0 and app.pixelColor.rgbaA(v)==0),'RGBA mismatch')end end end
assert(read(E..'/phase-map-validation.json').status=='PASS_BEFORE_AUTHORING');assert(read(E..'/pre-propagation-validation.json').status=='STRUCTURAL_AND_LOCAL_VISUAL_CHECK_COMPLETE')
local spec=read(E..'/temporal-spec.json');local plan=read(E..'/phase-plan.json');local names={'weaponBack','body','weaponFront','handFront'};local out={}
for _,direction in ipairs({'back_l','back_r'})do for _,kind in ipairs({'Sword','Axe'})do
 local key=direction..'/'..kind;local cfg=plan[key];local old=read(cfg.sourceClip);local timing=spec[kind];local processed={};local frameInfo={}
 for fi,f in ipairs(cfg.frames)do
  local src=old.frames[f.sourceFrame+1];local ims={}
  for j,n in ipairs(names)do
   if f.mode=='MANUAL_DESCENT'then ims[j]=load(E..'/transitions/'..kind:lower()..'/layers/'..n..'.png')
   elseif not f.weaponVisible and n~='body'then ims[j]=blank(256,256)
   else ims[j]=load(src.layers[n].png)end
  end
  processed[fi]=ims;frameInfo[fi]={index=fi-1,sourceFrame=f.sourceFrame,mode=f.mode,phase=f.phase,startMs=f.startMs,durationMs=f.durationMs}
 end
 local dst=cfg.dest;app.fs.makeAllDirectories(abs(dst..'/source'));local sp=Sprite(256,256,ColorMode.RGB);local ls={}
 for j,n in ipairs(names)do local l=j==1 and sp.layers[1]or sp:newLayer();l.name=n;ls[j]=l end
 for fi,f in ipairs(cfg.frames)do if fi>1 then sp:newEmptyFrame()end;sp.frames[fi].duration=f.durationMs/1000;for j=1,4 do sp:newCel(ls[j],fi,processed[fi][j],Point(0,0))end end
 sp:newTag(1,#cfg.frames).name='Attack';sp:saveAs(abs(dst..'/source/composite.aseprite'));sp:close()
 local ns=Sprite(128,128,ColorMode.RGB);ns.layers[1].name='body'
 for fi,f in ipairs(cfg.frames)do if fi>1 then ns:newEmptyFrame()end;ns.frames[fi].duration=f.durationMs/1000;ns:newCel(ns.layers[1],fi,crop(processed[fi][2]),Point(0,0))end
 ns:newTag(1,#cfg.frames).name='Attack';ns:saveAs(abs(dst..'/source/native.aseprite'));ns:close()
 sp=app.open(abs(dst..'/source/composite.aseprite'));ns=app.open(abs(dst..'/source/native.aseprite'));local strip=blank(256*#cfg.frames,256);local nstrip=blank(128*#cfg.frames,128);local contact=blank(128*5,128*math.ceil(#cfg.frames/5))
 for fi,f in ipairs(cfg.frames)do
  assert(math.abs(sp.frames[fi].duration*1000-f.durationMs)<.1);assert(math.abs(ns.frames[fi].duration*1000-f.durationMs)<.1)
  local id=string.format('%02d',fi-1);local comp=blank(256,256);comp:drawSprite(sp,fi);save(comp,dst..'/frames/'..id..'.png');strip:drawImage(comp,Point((fi-1)*256,0));local metadata={}
  for j,l in ipairs(sp.layers)do local c=l:cel(fi);local a=blank(256,256);if c then a:drawImage(c.image,c.position)end;eq(a,processed[fi][j]);save(a,dst..'/layers/'..l.name..'/'..id..'.png');metadata[#metadata+1]={layer=l.name,celPosition=c and{c.position.x,c.position.y}or false}end
  local n=blank(128,128);n:drawSprite(ns,fi);eq(n,crop(processed[fi][2]));save(n,dst..'/native/'..id..'.png');nstrip:drawImage(n,Point((fi-1)*128,0));contact:drawImage(n,Point(((fi-1)%5)*128,math.floor((fi-1)/5)*128));frameInfo[fi].savedLayers=metadata
 end
 save(strip,dst..'/composite-strip.png');save(nstrip,dst..'/native-strip.png');contact:resize(1280,256*math.ceil(#cfg.frames/5));save(contact,E..'/'..direction..'-'..kind:lower()..'-body-contact.png');sp:close();ns:close()
 out[key]={frames=frameInfo,mastersSavedReopened=true,rgbaAndTimingVerified=true}
end end
local f=assert(io.open(abs(E..'/author-result.json'),'w'));f:write(json.encode(out));f:close()
