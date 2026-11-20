-- ONLY F02 and F08. Does not open/write any F06 output.
local E='experiments/main-orc-combat-rescue-v5/grip-specialist/F02-F08'
local C='characters/orc-v1/source/combat-rescue-v5/grip-specialist'
local function file(p)return app.fs.joinPath(app.fs.currentPath,p)end
local function blank(w,h)local i=Image(w,h,ColorMode.RGB);i:clear();return i end
local function read(p)local f=assert(io.open(file(p),'r'));local j=json.decode(f:read('*a'));f:close();return j end
local function save(i,p)app.fs.makeAllDirectories(app.fs.filePath(file(p)));i:saveAs(file(p))end
local function equal(a,b)assert(a.width==b.width and a.height==b.height);for y=0,a.height-1 do for x=0,a.width-1 do assert(a:getPixel(x,y)==b:getPixel(x,y),'Parent source/export differs')end end end
local parent='characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/front_r/Sword/clip.json'
local clip=read(parent);local anatomy=read(E..'/anatomy.json')
local wd=read('characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/weapon.json')
local ws=app.open(file(wd.master));local item=blank(96,96);item:drawSprite(ws,1);ws:close();equal(item,Image{fromFile=file(wd.sprite)})
local configs={
 {key='F02',index=2,rows={{128,101,103},{129,101,104},{130,101,104},{131,102,104},{132,102,105},{133,101,103}}},
 {key='F08',index=8,rows={{146,157,161},{147,157,162},{148,157,161},{149,157,160},{150,157,159}}}
}
for _,cfg in ipairs(configs)do
 local frame=clip.frames[cfg.index+1];assert(frame.index==cfg.index)
 local source=app.open(file(clip.bodyMaster));local body=blank(256,256);body:drawSprite(source,cfg.index+1);source:close();equal(body,Image{fromFile=file(frame.layers.body.png)})
 local wb,wf,hf=blank(256,256),blank(256,256),blank(256,256)
 local t=anatomy[cfg.key].transform;local r=t.angleDeg*math.pi/180;local c,s=math.cos(r),math.sin(r)
 for y=0,255 do for x=0,255 do
  local dx,dy=x-t.bodyGrip[1],y-t.bodyGrip[2];local u=math.floor(c*dx+s*dy+48+.5);local v=math.floor(-s*dx+c*dy+66+.5)
  if u>=0 and u<96 and v>=0 and v<96 then
   local p=item:getPixel(u,v);if app.pixelColor.rgbaA(p)>0 then local dst=(v>=60 and v<=70)and wb or wf;dst:drawPixel(x,y,p)end
  end
 end end
 -- Distinct per-pose rows traced from the real glove. Copy existing colors;
 -- do not stamp a fixed palm or manufacture a bridge/cuff from arm pixels.
 for _,row in ipairs(cfg.rows)do for x=row[2],row[3]do local p=body:getPixel(x,row[1]);assert(app.pixelColor.rgbaA(p)==255);hf:drawPixel(x,row[1],p)end end
 local out=C..'/'..cfg.key;app.fs.makeAllDirectories(file(out..'/source'))
 local master=out..'/source/composite.aseprite';local sp=Sprite(256,256,ColorMode.RGB)
 for i,v in ipairs({{'weaponBack',wb},{'body',body},{'weaponFront',wf},{'handFront',hf}})do local l=i==1 and sp.layers[1]or sp:newLayer();l.name=v[1];sp:newCel(l,1,v[2],Point(0,0))end
 sp.frames[1].duration=frame.durationMs/1000;sp:saveAs(file(master));sp:close()
 local saved=app.open(file(master));local flat=blank(256,256);flat:drawSprite(saved,1);save(flat,out..'/composite-256.png')
 local native=blank(128,128);native:drawImage(body,Point(-64,-64));save(native,out..'/body-128.png')
 local doc={sourceFrameIndex=cfg.index,canvas={256,256},bodyOffset={64,64},durationMs=math.floor(saved.frames[1].duration*1000+.5),layers={}}
 local outside=0
 for y=0,255 do for x=0,255 do if (x<64 or x>=192 or y<64 or y>=192)and app.pixelColor.rgbaA(flat:getPixel(x,y))>0 then outside=outside+1 end end end
 doc.opaquePixelsOutsideBody128Crop=outside;doc.nativeCompositeComplete=(outside==0)
 for _,l in ipairs(saved.layers)do
  local im=blank(256,256);local cel=l:cel(1);if cel then im:drawImage(cel.image,cel.position)end
  save(im,out..'/layers/'..l.name..'.png');if l.name=='body'then equal(im,body)end
  if outside==0 then local n=blank(128,128);n:drawImage(im,Point(-64,-64));save(n,out..'/native/layers/'..l.name..'.png')end
  doc.layers[#doc.layers+1]={name=l.name,position=cel and{cel.position.x,cel.position.y}or nil}
 end
 if outside==0 then local n=blank(128,128);n:drawImage(flat,Point(-64,-64));save(n,out..'/composite-native-128.png')end
 saved:close()
 for _,v in ipairs({{'body-256.aseprite',256,body},{'body-128.aseprite',128,native}})do
  local q=Sprite(v[2],v[2],ColorMode.RGB);q.layers[1].name='body';q:newCel(q.layers[1],1,v[3],Point(0,0));q.frames[1].duration=frame.durationMs/1000;q:saveAs(file(out..'/source/'..v[1]));q:close()
 end
 local f=assert(io.open(file(out..'/source-document.json'),'w'));f:write(json.encode(doc));f:close()
 print(cfg.key..': source body/timing preserved; native equipment crop outside pixels='..outside..'; no propagation.')
end
