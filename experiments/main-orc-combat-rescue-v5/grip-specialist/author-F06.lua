-- ONLY representative front_r/Sword F06. Actual body/palm traced from source.
-- No inferred socket stamp, cuff bridge, body choreography or timing change.
local E='experiments/main-orc-combat-rescue-v5/grip-specialist'
local C='characters/orc-v1/source/combat-rescue-v5/grip-specialist/F06'
local function file(p)return app.fs.joinPath(app.fs.currentPath,p)end
local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function read(p)local f=assert(io.open(file(p),'r'));local d=json.decode(f:read('*a'));f:close();return d end
local function equal(a,b)assert(a.width==b.width and a.height==b.height);for y=0,a.height-1 do for x=0,a.width-1 do assert(a:getPixel(x,y)==b:getPixel(x,y),'Source/export mismatch')end end end
local function save(im,p)app.fs.makeAllDirectories(app.fs.filePath(file(p)));im:saveAs(file(p))end
local parent='characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword/clip.json'
local clip=read(parent);local frame=clip.frames[7];assert(frame.index==6 and frame.durationMs==35)
local bs=app.open(file(clip.bodyMaster));assert(bs.width==256 and #bs.frames==13)
local body=blank(256,256);body:drawSprite(bs,7);bs:close()
equal(body,Image{fromFile=file(frame.layers.body.png)})
local definition=read('characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/weapon.json')
local itemSource=app.open(file(definition.master));local item=blank(96,96);item:drawSprite(itemSource,1);itemSource:close()
equal(item,Image{fromFile=file(definition.sprite)})
local wb,wf,hf=blank(256,256),blank(256,256),blank(256,256)
local gx,gy,angle=155,114,32
local r=angle*math.pi/180;local c,s=math.cos(r),math.sin(r)
for y=0,255 do for x=0,255 do
 local dx,dy=x-gx,y-gy;local u=math.floor(c*dx+s*dy+48+.5);local v=math.floor(-s*dx+c*dy+66+.5)
 if u>=0 and u<96 and v>=0 and v<96 then
  local p=item:getPixel(u,v)
  if app.pixelColor.rgbaA(p)>0 then
   -- Semantic item split: leather grip inside the real opaque glove goes
   -- behind body. Guard/blade/disk pommel remain independently in front.
   local layer=(v>=60 and v<=70)and wb or wf
   layer:drawPixel(x,y,p)
  end
 end
end end
-- These are rows of the EXISTING brown closed glove, visually traced in the
-- actual source grid. No distance field, ellipse, generic fingers or new cuff.
local rows={{110,154,157},{111,153,157},{112,153,157},{113,154,157},{114,153,156},{115,153,156},{116,152,155},{117,152,154}}
for _,row in ipairs(rows)do for x=row[2],row[3]do
 local p=body:getPixel(x,row[1]);assert(app.pixelColor.rgbaA(p)==255)
 hf:drawPixel(x,row[1],p)
end end
-- Tiny local glove finish, INSIDE the observed source hand. Upper thumb turns
-- over the shaft; one lower crease suggests the curled fingers. No extension
-- toward the forearm, no generic cuff or enlarged hand silhouette.
local highlight=body:getPixel(157,119) -- original glove's warm highlight
local mid=app.pixelColor.rgba(58,35,28,255)
local crease=app.pixelColor.rgba(21,16,19,255)
local retouch={{156,111,highlight},{157,111,highlight},{157,112,highlight},{156,113,mid},{155,113,crease},{156,114,crease},{154,115,mid},{155,115,mid},{154,116,crease}}
for _,v in ipairs(retouch)do assert(app.pixelColor.rgbaA(body:getPixel(v[1],v[2]))==255);hf:drawPixel(v[1],v[2],v[3])end
app.fs.makeAllDirectories(file(C..'/source'))
local master=C..'/source/composite.aseprite';local spr=Sprite(256,256,ColorMode.RGB)
for i,v in ipairs({{'weaponBack',wb},{'body',body},{'weaponFront',wf},{'handFront',hf}})do
 local l=i==1 and spr.layers[1]or spr:newLayer();l.name=v[1];spr:newCel(l,1,v[2],Point(0,0))
end
spr.frames[1].duration=frame.durationMs/1000;spr:saveAs(file(master));spr:close()
-- All production PNG exports below derive from reopening the saved master.
local saved=app.open(file(master));local composite=blank(256,256);composite:drawSprite(saved,1)
save(composite,C..'/composite-256.png')
local nativeBody,nativeComposite=blank(128,128),blank(128,128)
local metadata={canvas={256,256},durationMs=math.floor(saved.frames[1].duration*1000+.5),layers={}}
for _,l in ipairs(saved.layers)do
 local im=blank(256,256);local cel=l:cel(1);if cel then im:drawImage(cel.image,cel.position)end
 save(im,C..'/layers/'..l.name..'.png')
 local ni=blank(128,128);ni:drawImage(im,Point(-64,-64));save(ni,C..'/native/layers/'..l.name..'.png')
 if l.name=='body'then nativeBody:drawImage(ni);equal(im,body)end
 metadata.layers[#metadata.layers+1]={name=l.name,position=cel and{cel.position.x,cel.position.y}or nil}
end
nativeComposite:drawImage(composite,Point(-64,-64));save(nativeBody,C..'/body-128.png');save(nativeComposite,C..'/composite-native-128.png')
saved:close()
-- Independent body sources, exact preserved pixels, authored/saved in Aseprite.
for _,spec in ipairs({{'body-256.aseprite',256,body},{'body-128.aseprite',128,nativeBody}})do
 local q=Sprite(spec[2],spec[2],ColorMode.RGB);q.layers[1].name='body';q:newCel(q.layers[1],1,spec[3],Point(0,0));q.frames[1].duration=.035;q:saveAs(file(C..'/source/'..spec[1]));q:close()
end
local f=assert(io.open(file(C..'/source-document.json'),'w'));f:write(json.encode(metadata));f:close()
print('Saved ONLY F06 actual-palm representative;35ms preserved. Awaiting local visual inspection and Root QA.')
