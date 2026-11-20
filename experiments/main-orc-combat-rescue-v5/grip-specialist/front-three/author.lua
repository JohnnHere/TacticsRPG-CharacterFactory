local E='experiments/main-orc-combat-rescue-v5/grip-specialist/front-three'
local C='characters/orc-v1/source/combat-rescue-v5/grip-specialist/front-three'
local function file(p)return app.fs.joinPath(app.fs.currentPath,p)end
local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function read(p)local f=assert(io.open(file(p),'r'));local j=json.decode(f:read('*a'));f:close();return j end
local function save(im,p)app.fs.makeAllDirectories(app.fs.filePath(file(p)));im:saveAs(file(p))end
local function equal(a,b)for y=0,a.height-1 do for x=0,a.width-1 do local p,q=a:getPixel(x,y),b:getPixel(x,y);assert(p==q or(app.pixelColor.rgbaA(p)==0 and app.pixelColor.rgbaA(q)==0),'Source differs')end end end
local snap=read(E..'/input-snapshot.json');local plan=read(E..'/anatomy-plan.json');local names={'weaponBack','body','weaponFront','handFront'}
for _,cfg in ipairs(plan.clips)do
 local parent=read(snap.clips[cfg.cellId]);assert(#parent.frames==cfg.frameCount)
 local wd=read('characters/orc-v1/source/combat-rescue-v5/combat/weapons/'..cfg.action..'/weapon.json')
 local is=app.open(file(wd.master));local item=blank(96,96);item:drawSprite(is,1);is:close();equal(item,Image{fromFile=file(wd.sprite)})
 local byFrame={};for _,f in ipairs(cfg.frames)do byFrame[f.index]=f end
 local out=C..'/'..cfg.cellId;app.fs.makeAllDirectories(file(out..'/source'))
 local s=Sprite(256,256,ColorMode.RGB);local layers={};for i,n in ipairs(names)do local l=i==1 and s.layers[1]or s:newLayer();l.name=n;layers[n]=l end
 local src=app.open(file(parent.bodyMaster))
 for fi,pf in ipairs(parent.frames)do
  local idx=fi-1;local body=blank(256,256);body:drawSprite(src,fi);equal(body,Image{fromFile=file(pf.layers.body.png)})
  local wb,wf,hf=blank(256,256),blank(256,256),blank(256,256);local f=byFrame[idx]
  if f then
   local rad=f.angleDeg*math.pi/180;local c,si=math.cos(rad),math.sin(rad)
   for y=0,255 do for x=0,255 do
    local dx,dy=x-f.grip[1],y-f.grip[2];local rx=c*dx+si*dy;local ry=-si*dx+c*dy;if cfg.itemFlipX then rx=-rx end
    local u=math.floor(rx+wd.grip[1]+.5);local v=math.floor(ry+wd.grip[2]+.5)
    if u>=0 and u<96 and v>=0 and v<96 then local p=item:getPixel(u,v);if app.pixelColor.rgbaA(p)>0 then local dst=(v>=cfg.gripSectionV[1]and v<=cfg.gripSectionV[2])and wb or wf;dst:drawPixel(x,y,p)end end
   end end
   for _,row in ipairs(f.gloveRows)do for x=row[2],row[3]do local p=body:getPixel(x,row[1]);assert(app.pixelColor.rgbaA(p)>0,cfg.cellId..' F'..idx..' glove trace misses source at '..x..','..row[1]);hf:drawPixel(x,row[1],p)end end
  else assert(idx<cfg.visibleInterval[1]or idx>cfg.visibleInterval[2])end
  if fi>1 then s:newEmptyFrame()end
  for n,im in pairs({weaponBack=wb,body=body,weaponFront=wf,handFront=hf})do s:newCel(layers[n],fi,im,Point(0,0))end
  s.frames[fi].duration=pf.durationMs/1000
 end
 src:close();s:newTag(1,#parent.frames).name='Attack';s:saveAs(file(out..'/source/composite.aseprite'));s:close()
 -- Fresh saved-source rendering; each positioned cel exported separately.
 local saved=app.open(file(out..'/source/composite.aseprite'))
 local bs=Sprite(256,256,ColorMode.RGB);bs.layers[1].name='body';local ns=Sprite(128,128,ColorMode.RGB);ns.layers[1].name='body';local hs=Sprite(256,256,ColorMode.RGB);hs.layers[1].name='handFront'
 local strip=blank(128*#parent.frames,128);local compStrip=blank(256*#parent.frames,256);local doc={frames={},layers=names,bodyOffset={64,64}}
 for fi,pf in ipairs(parent.frames)do
  local fn=string.format('%02d.png',fi-1);local flat=blank(256,256);flat:drawSprite(saved,fi);save(flat,out..'/'..fn);compStrip:drawImage(flat,Point((fi-1)*256,0))
  local body,hand
  for _,l in ipairs(saved.layers)do local im=blank(256,256);local cel=l:cel(fi);if cel then im:drawImage(cel.image,cel.position)end;save(im,out..'/layers/'..l.name..'/'..fn);if l.name=='body'then body=im elseif l.name=='handFront'then hand=im end end
  local native=blank(128,128);native:drawImage(body,Point(-64,-64));save(native,out..'/native/'..fn);strip:drawImage(native,Point((fi-1)*128,0))
  if fi>1 then bs:newEmptyFrame();ns:newEmptyFrame();hs:newEmptyFrame()end
  bs:newCel(bs.layers[1],fi,body,Point(0,0));ns:newCel(ns.layers[1],fi,native,Point(0,0));hs:newCel(hs.layers[1],fi,hand,Point(0,0));for _,q in ipairs({bs,ns,hs})do q.frames[fi].duration=pf.durationMs/1000 end
  doc.frames[#doc.frames+1]={index=fi-1,durationMs=pf.durationMs,weaponVisible=(byFrame[fi-1]~=nil)}
 end
 saved:close();for _,v in ipairs({{bs,'body.aseprite'},{ns,'native.aseprite'},{hs,'hand.aseprite'}})do v[1]:newTag(1,#parent.frames).name='Attack';v[1]:saveAs(file(out..'/source/'..v[2]));v[1]:close()end
 strip:saveAs(file(out..'/native-strip.png'));compStrip:saveAs(file(out..'/composite-strip.png'))
 local f=assert(io.open(file(out..'/source-document.json'),'w'));f:write(json.encode(doc));f:close();print('Saved '..cfg.cellId..' '..#parent.frames..'f; body/item/timing unchanged.')
end
