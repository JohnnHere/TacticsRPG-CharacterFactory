-- Aseprite is the sole raster editor. Original PixelLab art retained; hand finishing is authored Lua.
local root=assert(app.params.root);local function file(p)return app.fs.joinPath(root,p)end
local f=assert(io.open(file('experiments/orc-v1-weapons-v2/composition-plan.json'),'r'));local p=json.decode(f:read('*a'));f:close()
local pc=app.pixelColor;local function col(r,g,b)return pc.rgba(r,g,b,255)end
local function blank(w,h)local a=Image(w or 256,h or 256,ColorMode.RGB);a:clear();return a end
local function native(path)local s=app.open(file(path));local a=blank(s.width,s.height);a:drawSprite(s,1);s:close();return a end
local function save(im,path)app.fs.makeAllDirectories(app.fs.filePath(file(path)));im:saveAs(file(path))end
local function inside(x,y,pts)local c=false;local j=#pts;for i=1,#pts do local a,b=pts[i],pts[j];if(a[2]>y)~=(b[2]>y)and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1]then c=not c end;j=i end;return c end
local function rotate(source,grip,destGrip,angle)
 local out=blank();local r=angle*math.pi/180;local c,s=math.cos(r),math.sin(r);local gx,gy=destGrip[1]+64,destGrip[2]+64
 for y=math.max(0,gy-110),math.min(255,gy+110)do for x=math.max(0,gx-110),math.min(255,gx+110)do
  local dx,dy=x-gx,y-gy;local u=math.floor(c*dx+s*dy+grip[1]+.5);local v=math.floor(-s*dx+c*dy+grip[2]+.5)
  if u>=0 and v>=0 and u<source.width and v<source.height then local pixel=source:getPixel(u,v);if pc.rgbaA(pixel)>0 then out:drawPixel(x,y,pixel)end end
 end end;return out
end
-- Glove construction around the shaft, not a square crop of the old fist.
-- Palm lies behind the weapon; separate bent fingers and thumb cross its front.
local ink=col(2,2,3);local seam=col(38,27,27);local dark=col(53,40,36);local mid=col(84,65,53);local light=col(112,92,73);local edge=col(138,122,100)
local palm=blank(17,17);local fingers=blank(17,17)
for y=-5,5 do for x=-5,5 do if (x*x/30+y*y/26)<=1 then local c=ink;if(x*x/21+y*y/18)<=1 then c=x<0 and mid or dark end;palm:drawPixel(x+8,y+8,c)end end end
-- Four distinct finger clusters wrapping the actual hilt; visible creases between them.
for _,y in ipairs({-3,-1,1,3})do
 for x=-3,3 do fingers:drawPixel(x+8,y+8,x==-3 and light or mid)end
 fingers:drawPixel(12,y+8,dark);fingers:drawPixel(11,y+9,seam);fingers:drawPixel(6,y+8,light)
end
for y=-4,0 do fingers:drawPixel(3,y+8,ink);fingers:drawPixel(4,y+8,mid);fingers:drawPixel(5,y+8,light)end
fingers:drawPixel(6,5,edge);fingers:drawPixel(7,5,mid)
local reference=native(p.reference);local weapons={}
for id,w in pairs(p.weapons)do
 local im=native(w.raw)
 -- Sword hilt material is brown leather, while steel/guard/pommel retain generated pixels.
 if id=='recruit-sword'then for y=67,81 do for x=45,50 do local q=im:getPixel(x,y);if pc.rgbaA(q)>0 and pc.rgbaR(q)>15 then im:drawPixel(x,y,((x+y)%4==0)and light or(x<48 and mid or dark))end end end end
 app.fs.makeAllDirectories(app.fs.filePath(file(w.master)));local s=Sprite(im.width,im.height,ColorMode.RGB);s.layers[1].name='PixelLab Pro + Aseprite material finish';s:newCel(s.layers[1],1,im,Point(0,0));s:saveAs(file(w.master));save(im,w.sprite);s:close();weapons[id]=im
end
local garment={{44,76},{77,74},{94,84},{93,99},{39,99},{39,87}}
local bodies={}
for state,clip in pairs(p.states)do bodies[state]={}
 for i,frame in ipairs(clip.frames)do
  local src=native(frame.input)
  if frame.stabilizeGarment then
   for y=72,127 do for x=0,127 do
    local stable=y>=99 or inside(x,y,garment)
    if stable and not inside(x,y,frame.armMask)then src:drawPixel(x,y,reference:getPixel(x,y))end
   end end
  end
  local body=blank();body:drawImage(src,Point(64,64));bodies[state][i]=body
  save(body,p.output..'/shared/'..state..string.format('/body/%02d.png',i-1))
  save(rotate(palm,{8,8},frame.grip,frame.angle),p.output..'/shared/'..state..string.format('/palmBack/%02d.png',i-1))
  save(rotate(fingers,{8,8},frame.grip,frame.angle),p.output..'/shared/'..state..string.format('/fingersFront/%02d.png',i-1))
 end
 local shared=Sprite(256,256,ColorMode.RGB);shared.layers[1].name='Weapon independent body'
 for i,frame in ipairs(clip.frames)do if i>1 then shared:newEmptyFrame()end;shared:newCel(shared.layers[1],i,bodies[state][i],Point(0,0));shared.frames[i].duration=frame.durationMs/1000 end
 shared:newTag(1,#clip.frames).name=state;app.fs.makeAllDirectories(file(p.masters));shared:saveAs(file(p.masters..'/body-'..state:lower()..'.aseprite'));shared:close()
end
for id,w in pairs(p.weapons)do for state,clip in pairs(p.states)do
 local out=p.output..'/'..id..'/'..state;local sprite=Sprite(256,256,ColorMode.RGB);local layers={}
 for i,name in ipairs(p.layers)do local l=i==1 and sprite.layers[1]or sprite:newLayer();l.name=name;layers[name]=l end
 local strip=blank(256*#clip.frames,256)
 for i,frame in ipairs(clip.frames)do
  if i>1 then sprite:newEmptyFrame()end
  local images={body=bodies[state][i],palmBack=rotate(palm,{8,8},frame.grip,frame.angle),weapon=rotate(weapons[id],w.grip,frame.grip,frame.angle),fingersFront=rotate(fingers,{8,8},frame.grip,frame.angle)}
  for _,name in ipairs(p.layers)do local im=images[name];sprite:newCel(layers[name],i,im,Point(0,0));save(im,out..'/layers/'..name..string.format('/%02d.png',i-1))end
  sprite.frames[i].duration=frame.durationMs/1000;local result=blank();result:drawSprite(sprite,i);save(result,out..string.format('/%02d.png',i-1));strip:drawImage(result,Point((i-1)*256,0))
 end
 sprite:newTag(1,#clip.frames).name=state;app.fs.makeAllDirectories(file(p.masters));sprite:saveAs(file(p.masters..'/'..id..'-'..state:lower()..'.aseprite'));save(strip,out..'/native-strip.png');sprite:close()
end end
