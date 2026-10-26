-- All authored pixels, cleanup, registered pieces, masks and composites are edited/exported in Aseprite.
local root=assert(app.params.root);local function file(p)return app.fs.joinPath(root,p)end
local f=assert(io.open(file('experiments/main-orc-weapon-rescue-v3/composition-plan.json'),'r'));local p=json.decode(f:read('*a'));f:close()
local pc=app.pixelColor;local function blank(w,h)local im=Image(w or 256,h or 256,ColorMode.RGB);im:clear();return im end
local function native(path)local s=app.open(file(path));local im=blank(s.width,s.height);im:drawSprite(s,1);s:close();return im end
local function save(im,path)app.fs.makeAllDirectories(app.fs.filePath(file(path)));im:saveAs(file(path))end
local function inside(x,y,pts)local c=false;local j=#pts;for i=1,#pts do local a,b=pts[i],pts[j];if(a[2]>y)~=(b[2]>y)and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1]then c=not c end;j=i end;return c end
local function affected(x,y,regions)for _,poly in ipairs(regions)do if inside(x,y,poly)then return true end end;return false end
local function rotate(im,grip,target,angle,behind)
 local back,front=blank(),blank();local r=angle*math.pi/180;local c,s=math.cos(r),math.sin(r);local gx,gy=target[1]+64,target[2]+64
 for y=0,255 do for x=0,255 do local dx,dy=x-gx,y-gy;local u=math.floor(c*dx+s*dy+grip[1]+.5);local v=math.floor(-s*dx+c*dy+grip[2]+.5)
  if u>=0 and u<im.width and v>=0 and v<im.height then local q=im:getPixel(u,v);if pc.rgbaA(q)>0 then local layer=behind and v<grip[2]-9 and back or front;layer:drawPixel(x,y,q)end end
 end end;return back,front
end
local function makeSprite(names)local s=Sprite(256,256,ColorMode.RGB);local layers={};for i,name in ipairs(names)do local l=i==1 and s.layers[1]or s:newLayer();l.name=name;layers[name]=l end;return s,layers end
local reference=native(p.reference)
-- These are exact padded copies of the approved unarmed Idle/Walk, never armed states.
for state,clip in pairs(p.base)do
 local s,l=makeSprite({'Unarmed body'});local strip=blank(256*#clip.frames,256)
 for i,frame in ipairs(clip.frames)do local im=blank();im:drawImage(native(frame.input),Point(64,64));if i>1 then s:newEmptyFrame()end;s:newCel(l['Unarmed body'],i,im,Point(0,0));s.frames[i].duration=frame.durationMs/1000;save(im,p.output..'/'..state..string.format('/%02d.png',i-1));strip:drawImage(im,Point((i-1)*256,0))end
 app.fs.makeAllDirectories(file(p.masters));s:newTag(1,#clip.frames).name=state;s:saveAs(file(p.masters..'/'..state:lower()..'-unarmed.aseprite'));save(strip,p.output..'/'..state..'/native-strip.png');s:close()
end
for category,clip in pairs(p.profiles)do
 local item=native(clip.weapon.sprite);local out=p.output..'/'..category..'/Attack';local s,l=makeSprite(p.layerOrder);local bodyMaster,bl=makeSprite({'Weapon independent posed body'});local handMaster,hl=makeSprite({'Pose-specific original glove/fingers'});local strip=blank(256*#clip.frames,256)
 for i,frame in ipairs(clip.frames)do
  local src=native(frame.input)
  for y=0,src.height-1 do for x=0,src.width-1 do if affected(x,y,frame.cleanup)then src:drawPixel(x,y,0)end end end
  if frame.cloneSelf then local a=frame.cloneSelf.source;local b=frame.cloneSelf.target;local patch=Image(a[3],a[4],ColorMode.RGB);patch:clear();for y=0,a[4]-1 do for x=0,a[3]-1 do patch:drawPixel(x,y,src:getPixel(a[1]+x,a[2]+y))end end;src:drawImage(patch,Point(b[1],b[2]))end
  local body=blank();body:drawImage(src,Point(64,64))
  -- Restore the clipped near-boot sole from this SAME Orc's approved boot; no torso/leg freezing.
  if frame.footShift~=nil then
   for y=118,129 do for x=34,61 do body:drawPixel(x+64,y+64,0)end end
   for y=118,126 do for x=30,54 do body:drawPixel(x+64+frame.footShift,y+64,reference:getPixel(x,y))end end
  end
  local hand=blank();local back,front=blank(),blank()
  if frame.visible then
   back,front=rotate(item,clip.weapon.grip,frame.grip,frame.angle,frame.behind)
   for y=0,127 do for x=0,127 do if affected(x,y,frame.hand)then local q=body:getPixel(x+64,y+64);if pc.rgbaA(q)>0 then hand:drawPixel(x+64,y+64,q)end end end end
  end
  if i>1 then s:newEmptyFrame();bodyMaster:newEmptyFrame();handMaster:newEmptyFrame()end
  local images={body=body,weaponBack=back,weaponFront=front,handFront=hand}
  for _,name in ipairs(p.layerOrder)do s:newCel(l[name],i,images[name],Point(0,0));save(images[name],out..'/layers/'..name..string.format('/%02d.png',i-1))end
  bodyMaster:newCel(bl['Weapon independent posed body'],i,body,Point(0,0));handMaster:newCel(hl['Pose-specific original glove/fingers'],i,hand,Point(0,0));bodyMaster.frames[i].duration=frame.durationMs/1000;handMaster.frames[i].duration=frame.durationMs/1000;s.frames[i].duration=frame.durationMs/1000
  local result=blank();result:drawSprite(s,i);save(result,out..string.format('/%02d.png',i-1));strip:drawImage(result,Point((i-1)*256,0))
 end
 local stem=p.masters..'/'..category:lower();s:newTag(1,#clip.frames).name=clip.id;s:saveAs(file(stem..'-attack.aseprite'));bodyMaster:saveAs(file(stem..'-body.aseprite'));handMaster:saveAs(file(stem..'-hand-front.aseprite'));save(strip,out..'/native-strip.png');s:close();bodyMaster:close();handMaster:close()
end
