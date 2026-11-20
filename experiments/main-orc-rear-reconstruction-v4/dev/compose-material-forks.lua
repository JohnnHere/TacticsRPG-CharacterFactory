-- Weapon materials and exact known scalp-outline coordinates in Aseprite.
-- All other body pixels, handFront, depth masks, alpha and timing unchanged.
-- Prior rear dark contour overrides are retained exactly and recorded.
local E='experiments/main-orc-rear-reconstruction-v4/dev'
local C='characters/orc-v1/source/rear-reconstruction-v4'
local function file(p)return app.fs.joinPath(app.fs.currentPath,p)end
local function read(p)local f=assert(io.open(file(p),'r'));local v=json.decode(f:read('*a'));f:close();return v end
local function write(p,v)local f=assert(io.open(file(p),'w'));f:write(json.encode(v));f:close()end
local function blank(w,h)local i=Image(w,h,ColorMode.RGB);i:clear();return i end
local function layerRender(s,l,i)local im=blank(s.width,s.height);local cel=l:cel(i);if cel then im:drawImage(cel.image,cel.position)end;return im end
local function save(im,p)app.fs.makeAllDirectories(app.fs.filePath(file(p)));im:saveAs(file(p))end
local clips=read(E..'/input-clips.json');local registration=read(E..'/weapon-registration.json');local reg={}
local scalp=read(E..'/scalp-outline-points.json');local scalpFrames={}
for _,r in ipairs(scalp.frames)do scalpFrames[r.frame]=r.points end
for _,r in ipairs(registration)do reg[r.cellId..'/'..string.format('%d',r.frame)]=r end
local summaries={}
for _,dir in ipairs({'front_r','front_l','back_r','back_l'})do for _,cat in ipairs({'Sword','Axe'})do
 local key=dir..'/'..cat;local clip=clips[key];local itemId=cat=='Sword'and'recruit-sword'or'militia-axe'
 local def=read('assets/weapons/'..itemId..'/weapon.json')
 local oldItem=Image{fromFile=file(def.sprite)}
 local newItem=Image{fromFile=file(C..'/weapons/'..cat..'/'..itemId..'.png')}
 local s=app.open(file(clip.master));assert(s.width==256 and #s.frames==#clip.frames)
 local out=C..'/'..key;app.fs.makeAllDirectories(file(out..'/source'))
 local evidence={cellId=key,frames={}}
 for fi,frame in ipairs(clip.frames)do
  local r=reg[key..'/'..(fi-1)];local overrides,changed,matched=0,0,0
  if frame.weaponVisible then
   assert(r and r.alphaIoU==1)
   local rad=r.angle*math.pi/180;local c,si=math.cos(rad),math.sin(rad)
   for _,l in ipairs(s.layers)do if l.name=='weaponFront'or l.name=='weaponBack'then
    local im=layerRender(s,l,fi)
    for y=0,255 do for x=0,255 do
     local q=im:getPixel(x,y)
     if app.pixelColor.rgbaA(q)>0 then
      local dx,dy=x-r.grip[1],y-r.grip[2];local rx=c*dx+si*dy;local ry=-si*dx+c*dy
      if r.flip then rx=-rx end
      local u=math.floor(rx+def.grip[1]+.5);local v=math.floor(ry+def.grip[2]+.5)
      assert(u>=0 and u<96 and v>=0 and v<96)
      local old=oldItem:getPixel(u,v);local new=newItem:getPixel(u,v)
      assert(app.pixelColor.rgbaA(old)>0 and app.pixelColor.rgbaA(new)==app.pixelColor.rgbaA(old))
      if q==old then
       matched=matched+1;if q~=new then im:drawPixel(x,y,new);changed=changed+1 end
      else
       -- The old rear composer substituted this exact dark contour. Keeping
       -- it avoids broad luminance recoloring and preserves its occupied mask.
       assert(q==app.pixelColor.rgba(30,33,36,255),'Unexpected source/layer disagreement')
       overrides=overrides+1
      end
     end
    end end
    local cel=l:cel(fi);if cel then cel.image=im;cel.position=Point(0,0)else s:newCel(l,fi,im,Point(0,0))end
   end end
  end
  local scalpChanged=0
  if dir=='back_r'and fi>1 then
   for _,l in ipairs(s.layers)do if l.name=='body'then
    local im=layerRender(s,l,fi)
    for _,p in ipairs(scalpFrames[fi-1])do
     local x,y=p.native[1]+64,p.native[2]+64;local b=p.before
     assert(im:getPixel(x,y)==app.pixelColor.rgba(b[1],b[2],b[3],b[4]),'Scalp input changed')
     im:drawPixel(x,y,app.pixelColor.rgba(12,15,18,255));scalpChanged=scalpChanged+1
    end
    local cel=l:cel(fi);cel.image=im;cel.position=Point(0,0)
   end end
  end
  evidence.frames[#evidence.frames+1]={index=fi-1,materialPixelsChanged=changed,scalpOutlinePixelsChanged=scalpChanged,priorContourPixelsRetained=overrides,rawSourceColorMatches=matched}
 end
 s:saveAs(file(out..'/source/composite.aseprite'));s:close()
 -- Fresh reopen/render of the saved composite and each actual positioned cel.
 local saved=app.open(file(out..'/source/composite.aseprite'))
 local native=Sprite(128,128,ColorMode.RGB);native.layers[1].name='body'
 local body=Sprite(256,256,ColorMode.RGB);body.layers[1].name='body'
 local strip=blank(128*#saved.frames,128);local cs=blank(256*#saved.frames,256)
 for fi,frame in ipairs(clip.frames)do
  if fi>1 then native:newEmptyFrame();body:newEmptyFrame()end
  local flat=blank(256,256);flat:drawSprite(saved,fi)
  save(flat,out..string.format('/%02d.png',fi-1));cs:drawImage(flat,Point((fi-1)*256,0))
  local bodyIm
  for _,l in ipairs(saved.layers)do
   local im=layerRender(saved,l,fi);save(im,out..'/layers/'..l.name..string.format('/%02d.png',fi-1));if l.name=='body'then bodyIm=im end
  end
  assert(bodyIm)
  local nat=blank(128,128);nat:drawImage(bodyIm,Point(-64,-64))
  save(nat,out..string.format('/native/%02d.png',fi-1));strip:drawImage(nat,Point((fi-1)*128,0))
  native:newCel(native.layers[1],fi,nat,Point(0,0));body:newCel(body.layers[1],fi,bodyIm,Point(0,0))
  native.frames[fi].duration=frame.durationMs/1000;body.frames[fi].duration=frame.durationMs/1000
  assert(math.floor(saved.frames[fi].duration*1000+.5)==frame.durationMs)
 end
 native:saveAs(file(out..'/source/native.aseprite'));native:close()
 body:saveAs(file(out..'/source/body.aseprite'));body:close()
 strip:saveAs(file(out..'/native-strip.png'));cs:saveAs(file(out..'/composite-strip.png'));saved:close()
 -- Reopen the two new body sources too: source position/timing proof is fresh.
 for _,part in ipairs({'native','body'})do
  local b=app.open(file(out..'/source/'..part..'.aseprite'))
  for fi=1,#b.frames do local im=blank(b.width,b.height);im:drawSprite(b,fi);save(im,E..'/fresh-proof/'..key..'/'..part..string.format('/%02d.png',fi-1))end
  b:close()
 end
 summaries[#summaries+1]=evidence;print('Saved weapon material-only fork '..key)
end end
write(E..'/material-composition-evidence.json',summaries)
