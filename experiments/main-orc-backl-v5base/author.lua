-- Authorship: programmatic assembly and local integer translation in Aseprite.
-- Original v5 body/hand pixels are never retouched or synthesized.
local E='experiments/main-orc-backl-v5base'
local function read(p)local f=assert(io.open(p,'r'));local v=json.decode(f:read('*a'));f:close();return v end
local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function save(im,p)app.fs.makeAllDirectories(app.fs.filePath(p));im:saveAs(p)end
local function load(p)return Image{fromFile=p}end
local function shifted(im,dx,dy)local r=blank(256,256);r:drawImage(im,Point(dx,dy));return r end
local names={'weaponBack','body','weaponFront','handFront'}
for _,c in ipairs(read(E..'/author-config.json'))do
 local out=E..'/'..c.name;app.fs.makeAllDirectories(out..'/source')
 local spr=Sprite(256,256,ColorMode.RGB);local ls={}
 for j,n in ipairs(names)do local l=j==1 and spr.layers[1] or spr:newLayer();l.name=n;ls[n]=l end
 local def=read(c.weaponDefinition);local item=load(def.sprite)
 for fi,f in ipairs(c.frames)do
  if fi>1 then spr:newEmptyFrame()end
  spr.frames[fi].duration=f.durationMs/1000
  local ims={body=shifted(load(f.sourceBody),f.dx,f.dy),weaponBack=blank(256,256),weaponFront=blank(256,256),handFront=blank(256,256)}
  if f.weaponVisible then
   if c.name=='axe' then
    for _,n in ipairs({'weaponBack','weaponFront','handFront'})do ims[n]=shifted(load(f.sourceLayers[n].png),f.dx,f.dy)end
   else
    local r=f.angleDeg*math.pi/180;local co,si=math.cos(r),math.sin(r)
    for y=0,255 do for x=0,255 do
     local dx,dy=x-f.grip[1],y-f.grip[2]
     local u=math.floor(co*dx+si*dy+def.grip[1]+0.5);local v=math.floor(-si*dx+co*dy+def.grip[2]+0.5)
     if u>=0 and u<item.width and v>=0 and v<item.height then
      local p=item:getPixel(u,v)
      if app.pixelColor.rgbaA(p)>0 then
       local dest=(v>=60 and v<=70)and ims.weaponBack or ims.weaponFront
       dest:drawPixel(x,y,p)
      end
     end
    end end
    -- Copy existing observed glove and its wrist border verbatim. No repaint.
    local box=f.handBox
    for y=box[2],box[4]do for x=box[1],box[3]do
     local p=ims.body:getPixel(x+f.dx,y+f.dy)
     if app.pixelColor.rgbaA(p)>0 then ims.handFront:drawPixel(x+f.dx,y+f.dy,p)end
    end end
   end
  end
  for _,n in ipairs(names)do spr:newCel(ls[n],fi,ims[n],Point(0,0))end
 end
 spr:newTag(1,#c.frames).name='Attack';spr:saveAs(out..'/source/composite.aseprite');spr:close()
 -- Exports are rendered only from the saved, reopened master.
 local saved=app.open(out..'/source/composite.aseprite')
 local ns=Sprite(128,128,ColorMode.RGB);local nl={}
 for j,n in ipairs(names)do local l=j==1 and ns.layers[1]or ns:newLayer();l.name=n;nl[n]=l end
 local bs=Sprite(256,256,ColorMode.RGB);bs.layers[1].name='body'
 local strip=blank(256*#c.frames,256);local nativeStrip=blank(128*#c.frames,128)
 for fi,f in ipairs(c.frames)do
  assert(math.abs(saved.frames[fi].duration*1000-f.durationMs)<0.1)
  if fi>1 then ns:newEmptyFrame();bs:newEmptyFrame()end
  ns.frames[fi].duration=f.durationMs/1000;bs.frames[fi].duration=f.durationMs/1000
  local fn=string.format('%02d.png',fi-1);local comp=blank(256,256);comp:drawSprite(saved,fi)
  save(comp,out..'/frames/'..fn);strip:drawImage(comp,Point((fi-1)*256,0))
  local native=blank(128,128);native:drawImage(comp,Point(-64,-64));save(native,out..'/native/'..fn);nativeStrip:drawImage(native,Point((fi-1)*128,0))
  for _,l in ipairs(saved.layers)do
   local im=blank(256,256);local cel=l:cel(fi);if cel then im:drawImage(cel.image,cel.position)end
   save(im,out..'/layers/'..l.name..'/'..fn)
   local ni=blank(128,128);ni:drawImage(im,Point(-64,-64));save(ni,out..'/native/layers/'..l.name..'/'..fn);ns:newCel(nl[l.name],fi,ni,Point(0,0))
   if l.name=='body'then bs:newCel(bs.layers[1],fi,im,Point(0,0))end
  end
 end
 ns:newTag(1,#c.frames).name='Attack';ns:saveAs(out..'/source/native.aseprite');ns:close()
 bs:saveAs(out..'/source/body.aseprite');bs:close();saved:close()
 save(strip,out..'/composite-strip.png');save(nativeStrip,out..'/native-strip.png')
 print('EXPORTED '..c.name..' '..#c.frames)
end
