-- Programmatic local Aseprite authorship. No generation, no body/hand editing.
local E='experiments/main-orc-hybrid-weapon-04'
local function read(p)local f=assert(io.open(p,'r'));local v=json.decode(f:read('*a'));f:close();return v end
local clip=read('characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_l-sword/clip.json')
local function blank(w,h)local i=Image(w,h,ColorMode.RGB);i:clear();return i end
local function save(i,p)app.fs.makeAllDirectories(app.fs.filePath(p));i:saveAs(p)end
local function raster(s,n,f)local im=blank(s.width,s.height);for _,l in ipairs(s.layers)do if l.name==n then local c=l:cel(f);if c then im:drawImage(c.image,c.position)end;return im end end;error(n)end
local function render(s,f)local im=blank(s.width,s.height);im:drawSprite(s,f);return im end
local function rgba(r,g,b)return app.pixelColor.rgba(r,g,b,255)end
local stage=app.params.stage or 'representative'
if stage=='representative' then
 local src=app.open(clip.weapon.master)
 app.fs.makeAllDirectories(E..'/variants/sword-a');src:saveAs(E..'/variants/sword-a/sword.aseprite');save(render(src,1),E..'/variants/sword-a/sword.png');src:close()
 src=app.open(E..'/variants/sword-a/sword.aseprite')
 local inherited=render(src,1);local b=Image(inherited)
 -- Only blade y7..54 is replaced. Hilt, guard, pommel, grip all inherited exactly.
 for y=0,54 do for x=0,95 do b:drawPixel(x,y,0)end end
 for y=7,54 do
  local half= y<15 and math.floor((y-7)/2) or (y<45 and 4 or 3)
  for x=48-half,48+half do
   local c
   if x==48-half or x==48+half or y==7 then c=rgba(12,15,18)
   elseif x<48 then c=rgba(174,191,201)
   elseif x==48 then c=rgba(112,136,154)
   else c=rgba(66,84,103)end
   if x==49-half and y>=16 and y<=43 then c=rgba(205,218,223)end
   b:drawPixel(x,y,c)
  end
 end
 -- The inherited layers stay hidden as editable provenance; replacement is the visible master.
 for _,l in ipairs(src.layers)do l.isVisible=false end
 local l=src:newLayer();l.name='facet-steel-blade-inherited-hilt';src:newCel(l,1,b,Point(0,0))
 app.fs.makeAllDirectories(E..'/variants/sword-b');src:saveAs(E..'/variants/sword-b/sword.aseprite');src:close()
 src=app.open(E..'/variants/sword-b/sword.aseprite');save(render(src,1),E..'/variants/sword-b/sword.png');src:close()
end
local item=Image{fromFile=E..'/variants/sword-b/sword.png'}
local original=app.open(clip.master)
local selected=stage=='full' and {0,1,2,3,4,5,6,7,8,9,10,11,12,13} or {2,8,11}
for _,variant in ipairs({'a','b'})do
 local s=Sprite(256,256);local names={'weaponBack','body','weaponFront','handFront'};local layers={}
 for i,n in ipairs(names)do local l=i==1 and s.layers[1]or s:newLayer();l.name=n;layers[n]=l end
 for fi,idx in ipairs(selected)do
  if fi>1 then s:newEmptyFrame()end
  local pf=clip.frames[idx+1];local ims={}
  for _,n in ipairs(names)do ims[n]=raster(original,n,idx+1)end
  if variant=='b' and pf.weaponVisible then
   -- Preserve original handle/guard placement and masks. Replace only the blade footprint.
   -- F06 was authored as a second integer rotation of F05: replay that exact lookup.
   for y=0,255 do for x=0,255 do
    local xx,yy=x,y;local cfg=pf
    if idx==6 then
     local a=math.rad(-16);local dx,dy=x-128,y-101
     xx=math.floor(157+dx*math.cos(a)+dy*math.sin(a)+.5)
     yy=math.floor(89-dx*math.sin(a)+dy*math.cos(a)+.5)
     cfg=clip.frames[6]
    end
    local a=math.rad(cfg.rotationDeg);local dx,dy=xx-cfg.grip[1],yy-cfg.grip[2]
    local u=math.floor(48+dx*math.cos(a)+dy*math.sin(a)+.5)
    local v=math.floor(66-dx*math.sin(a)+dy*math.cos(a)+.5)
    if u>=0 and u<96 and v>=0 and v<=54 then
     ims.weaponBack:drawPixel(x,y,0);ims.weaponFront:drawPixel(x,y,item:getPixel(u,v))
    end
   end end
  end
  for _,n in ipairs(names)do s:newCel(layers[n],fi,ims[n],Point(0,0))end
  s.frames[fi].duration=pf.durationMs/1000
 end
 local out=E..'/'..stage..'/'..variant;app.fs.makeAllDirectories(out)
 s:saveAs(out..'/composite.aseprite');s:close()
 -- Export only reopened saved sources, as in the existing Aseprite offline pipeline.
 s=app.open(out..'/composite.aseprite')
 local sheet=blank(256*#selected,256)
 for fi,idx in ipairs(selected)do
  local fn=string.format('F%02d.png',idx)
  local wb=raster(s,'weaponBack',fi);wb:drawImage(raster(s,'weaponFront',fi))
  save(wb,out..'/weapon-only/'..fn);save(raster(s,'body',fi),out..'/body-only/'..fn)
  for _,n in ipairs(names)do save(raster(s,n,fi),out..'/layers/'..n..'/'..fn)end
  local c=render(s,fi);save(c,out..'/composite/'..fn);sheet:drawImage(c,Point((fi-1)*256,0))
 end
 save(sheet,out..'/strip.png');s:close()
end
original:close()
print('Saved and reopened '..stage..' A/B; bodies and hands untouched.')
