local root=assert(app.params.root);local function file(p)return app.fs.joinPath(root,p)end
local f=assert(io.open(assert(app.params.plan),'r'));local p=json.decode(f:read('*a'));f:close()
local function blank()local im=Image(256,256,ColorMode.RGB);im:clear();return im end
local function native(path)local s=app.open(file(path));local im=Image(s.width,s.height,ColorMode.RGB);im:clear();im:drawSprite(s,1);s:close();return im end
local function save(im,path)app.fs.makeAllDirectories(app.fs.filePath(file(path)));im:saveAs(file(path))end
local item=native(p.item.sprite);local profile=p.bodyProfile;local s=Sprite(256,256,ColorMode.RGB);local names={'weaponBack','body','weaponFront','handFront'};local layers={}
for i,name in ipairs(names)do local l=i==1 and s.layers[1]or s:newLayer();l.name=name;layers[name]=l end
for i,frame in ipairs(profile.frames)do
 local body=native(frame.body.png);local hand=native(frame.handFront.png);local back,front=blank(),blank()
 if frame.weaponVisible then local r=frame.angle*math.pi/180;local c,si=math.cos(r),math.sin(r);local gx,gy=frame.grip[1],frame.grip[2]
  for y=0,255 do for x=0,255 do local dx,dy=x-gx,y-gy;local u=math.floor(c*dx+si*dy+p.item.grip[1]+.5);local v=math.floor(-si*dx+c*dy+p.item.grip[2]+.5)
   if u>=0 and u<item.width and v>=0 and v<item.height then local q=item:getPixel(u,v);if app.pixelColor.rgbaA(q)>0 then local layer=frame.weaponBehindBody and v<p.item.grip[2]-9 and back or front;layer:drawPixel(x,y,q)end end
  end end
 end
 if i>1 then s:newEmptyFrame()end;local images={body=body,handFront=hand,weaponBack=back,weaponFront=front}
 for _,name in ipairs(names)do s:newCel(layers[name],i,images[name],Point(0,0));save(images[name],p.output..'/layers/'..name..string.format('/%02d.png',i-1))end
 s.frames[i].duration=frame.durationMs/1000;local flat=blank();flat:drawSprite(s,i);save(flat,p.output..string.format('/%02d.png',i-1))
end
s:saveAs(file(p.output..'/composition.aseprite'));s:close()
