-- Complete front_r/Sword ONLY. Source bodies/timing untouched; validated key
-- layers F02/F06/F08 reused exactly. No writes outside this full-clip fork.
local E='experiments/main-orc-combat-rescue-v5/grip-specialist/full-front-r-sword'
local C='characters/orc-v1/source/combat-rescue-v5/grip-specialist/full-front-r-sword'
local BASE='characters/orc-v1/source/combat-rescue-v5/grip-specialist'
local function file(p)return app.fs.joinPath(app.fs.currentPath,p)end
local function blank(w,h)local i=Image(w,h,ColorMode.RGB);i:clear();return i end
local function read(p)local f=assert(io.open(file(p),'r'));local j=json.decode(f:read('*a'));f:close();return j end
local function equal(a,b)assert(a.width==b.width and a.height==b.height);for y=0,a.height-1 do for x=0,a.width-1 do local p,q=a:getPixel(x,y),b:getPixel(x,y);assert(p==q or(app.pixelColor.rgbaA(p)==0 and app.pixelColor.rgbaA(q)==0),'Source pixel drift')end end end
local function save(i,p)app.fs.makeAllDirectories(app.fs.filePath(file(p)));i:saveAs(file(p))end
local clip=read('characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword/clip.json')
local anatomy=read(E..'/anatomy.json');assert(#clip.frames==13 and clip.totalDurationMs==730)
local wd=read('characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/weapon.json')
local ws=app.open(file(wd.master));local item=blank(96,96);item:drawSprite(ws,1);ws:close();equal(item,Image{fromFile=file(wd.sprite)})
-- Traces made on each actual source glove, not masks translated from F06.
local rows={
 [3]={{116,89,93},{117,88,94},{118,88,94},{119,88,94},{120,89,93},{121,89,92}},
 [4]={{96,94,97},{97,94,97},{98,94,97},{99,94,99},{100,94,100},{101,95,101},{102,96,101},{103,96,100}},
 [5]={{86,96,100},{87,95,102},{88,95,102},{89,95,102},{90,96,102},{91,97,101}},
 [7]={{129,156,159},{130,156,160},{131,155,160},{132,155,160},{133,155,159}},
 [9]={{143,132,134},{144,132,135},{145,132,135},{146,132,135},{147,132,136},{148,132,136},{149,132,135},{150,132,134}},
 [10]={{147,109,112},{148,108,112},{149,107,112},{150,108,112},{151,108,112},{152,109,113}}
}
app.fs.makeAllDirectories(file(C..'/source'))
local sp=Sprite(256,256,ColorMode.RGB);local layerNames={'weaponBack','body','weaponFront','handFront'};local ls={}
for i,name in ipairs(layerNames)do local l=i==1 and sp.layers[1]or sp:newLayer();l.name=name;ls[name]=l end
local source=app.open(file(clip.bodyMaster));local metadata={frames={},layerOrder=layerNames,bodyOffset={64,64}}
for fi,frame in ipairs(clip.frames)do
 local idx=fi-1;local cfg=anatomy.frames[fi];assert(cfg.index==idx and frame.index==idx)
 local body=blank(256,256);body:drawSprite(source,fi);equal(body,Image{fromFile=file(frame.layers.body.png)})
 local wb,wf,hf=blank(256,256),blank(256,256),blank(256,256)
 if cfg.weaponVisible then
  if cfg.reuseRepresentative then
   local rep=read(BASE..'/'..cfg.reuseRepresentative..'/representative.json');local rf=rep.frames[1]
   assert(rf.sourceFrameIndex==idx and rf.durationMs==frame.durationMs);equal(body,Image{fromFile=file(rf.layers.body.png)})
   wb=Image{fromFile=file(rf.layers.weaponBack.png)};wf=Image{fromFile=file(rf.layers.weaponFront.png)};hf=Image{fromFile=file(rf.layers.handFront.png)}
  else
   local rad=cfg.angleDeg*math.pi/180;local c,s=math.cos(rad),math.sin(rad)
   for y=0,255 do for x=0,255 do
    local dx,dy=x-cfg.grip[1],y-cfg.grip[2];local u=math.floor(c*dx+s*dy+48+.5);local v=math.floor(-s*dx+c*dy+66+.5)
    if u>=0 and u<96 and v>=0 and v<96 then local p=item:getPixel(u,v);if app.pixelColor.rgbaA(p)>0 then local dst=(v>=60 and v<=70)and wb or wf;dst:drawPixel(x,y,p)end end
   end end
   for _,row in ipairs(rows[idx])do for x=row[2],row[3]do local p=body:getPixel(x,row[1]);assert(app.pixelColor.rgbaA(p)>0,'Trace outside source glove');hf:drawPixel(x,row[1],p)end end
  end
 end
 if fi>1 then sp:newEmptyFrame()end
 for name,im in pairs({weaponBack=wb,body=body,weaponFront=wf,handFront=hf})do sp:newCel(ls[name],fi,im,Point(0,0))end
 sp.frames[fi].duration=frame.durationMs/1000
 metadata.frames[#metadata.frames+1]={index=idx,durationMs=frame.durationMs,weaponVisible=cfg.weaponVisible,representativeReuse=cfg.reuseRepresentative}
end
source:close();sp:newTag(1,13).name='Attack';sp:saveAs(file(C..'/source/composite.aseprite'));sp:close()
-- Reopen saved composite before all layer/flat exports. Respect actual cels.
local saved=app.open(file(C..'/source/composite.aseprite'))
local bs=Sprite(256,256,ColorMode.RGB);bs.layers[1].name='body';local ns=Sprite(128,128,ColorMode.RGB);ns.layers[1].name='body'
local hs=Sprite(256,256,ColorMode.RGB);hs.layers[1].name='handFront'
local strip=blank(128*13,128);local compStrip=blank(256*13,256)
for fi,frame in ipairs(clip.frames)do
 local fn=string.format('%02d.png',fi-1);local flat=blank(256,256);flat:drawSprite(saved,fi);save(flat,C..'/'..fn);compStrip:drawImage(flat,Point((fi-1)*256,0))
 local body,hand
 for _,l in ipairs(saved.layers)do
  local im=blank(256,256);local cel=l:cel(fi);if cel then im:drawImage(cel.image,cel.position)end
  save(im,C..'/layers/'..l.name..'/'..fn);if l.name=='body'then body=im elseif l.name=='handFront'then hand=im end
 end
 local native=blank(128,128);native:drawImage(body,Point(-64,-64));save(native,C..'/native/'..fn);strip:drawImage(native,Point((fi-1)*128,0))
 if fi>1 then bs:newEmptyFrame();ns:newEmptyFrame();hs:newEmptyFrame()end
 bs:newCel(bs.layers[1],fi,body,Point(0,0));ns:newCel(ns.layers[1],fi,native,Point(0,0));hs:newCel(hs.layers[1],fi,hand,Point(0,0))
 for _,s in ipairs({bs,ns,hs})do s.frames[fi].duration=frame.durationMs/1000 end
end
saved:close()
for _,v in ipairs({{bs,'body.aseprite'},{ns,'native.aseprite'},{hs,'hand.aseprite'}})do v[1]:newTag(1,13).name='Attack';v[1]:saveAs(file(C..'/source/'..v[2]));v[1]:close()end
strip:saveAs(file(C..'/native-strip.png'));compStrip:saveAs(file(C..'/composite-strip.png'))
local f=assert(io.open(file(C..'/source-document.json'),'w'));f:write(json.encode(metadata));f:close()
print('Saved ONLY full front_r/Sword13f/730ms. Validated key layers reused exactly; pending full-motion QA.')
