-- All rotation, masking, clean-up, layer composition and raster exports happen in Aseprite.
local root=assert(app.params.root);local function file(p)return app.fs.joinPath(root,p)end
local f=assert(io.open(file('experiments/orc-v1-weapons-v1/composition-plan.json'),'r'));local plan=json.decode(f:read('*a'));f:close()
local function blank()local im=Image(256,256,ColorMode.RGB);im:clear();return im end
local function native(p)local s=app.open(file(p));local im=Image(s.width,s.height,ColorMode.RGB);im:clear();im:drawSprite(s,1);s:close();return im end
local weapons={};for id,w in pairs(plan.weapons)do weapons[id]=native(w.source)end
for _,job in ipairs(plan.jobs)do
 local sprite=Sprite(256,256,ColorMode.RGB);local layers={}
 for i,name in ipairs({'weaponBack','body','weaponFront','handFront'})do local l=i==1 and sprite.layers[1]or sprite:newLayer();l.name=name;layers[name]=l end
 app.fs.makeAllDirectories(file(job.output));app.fs.makeAllDirectories(app.fs.filePath(file(job.master)))
 for i,frame in ipairs(job.frames)do
  local source=native(frame.input)
  for _,r in ipairs(frame.cleanup)do for y=r[2],r[4]-1 do for x=r[1],r[3]-1 do source:drawPixel(x,y,0)end end end
  local body=blank();body:drawImage(source,Point(64,64))
  local weapon=blank();local config=plan.weapons[job.weapon];local original=weapons[job.weapon]
  local gx,gy=frame.rightGrip[1]+64,frame.rightGrip[2]+64
  local rad=frame.rotationDeg*math.pi/180;local c,s=math.cos(rad),math.sin(rad)
  -- Inverse nearest-neighbour rotation. No antialiasing, scaling or raster editing outside editor.
  for y=math.max(0,gy-85),math.min(255,gy+85)do for x=math.max(0,gx-85),math.min(255,gx+85)do
   local dx,dy=x-gx,y-gy;local u=math.floor(c*dx+s*dy+config.grip[1]+.5);local v=math.floor(-s*dx+c*dy+config.grip[2]+.5)
   if u>=0 and u<original.width and v>=0 and v<original.height then local pixel=original:getPixel(u,v);if app.pixelColor.rgbaA(pixel)>0 then weapon:drawPixel(x,y,pixel)end end
  end end
  local hand=blank()
  for dy=-2,2 do for dx=-2,2 do local x,y=frame.rightGrip[1]+dx,frame.rightGrip[2]+dy
   if x>=0 and x<128 and y>=0 and y<128 then local color=source:getPixel(x,y);if app.pixelColor.rgbaA(color)>0 then hand:drawPixel(x+64,y+64,color)end end
  end end
  local images={body=body,weaponBack=frame.depth=='back'and weapon or blank(),weaponFront=frame.depth=='front'and weapon or blank(),handFront=hand}
  if i>1 then sprite:newEmptyFrame()end
  for name,im in pairs(images)do sprite:newCel(layers[name],i,im,Point(0,0));local folder=job.output..'/layers/'..name;app.fs.makeAllDirectories(file(folder));im:saveAs(file(folder..string.format('/%02d.png',i-1)))end
  sprite.frames[i].duration=frame.durationMs/1000
  local flattened=blank();flattened:drawSprite(sprite,i);flattened:saveAs(file(job.output..string.format('/%02d.png',i-1)))
 end
 sprite:newTag(1,#job.frames).name=job.state;sprite:saveAs(file(job.master));sprite:close()
end
