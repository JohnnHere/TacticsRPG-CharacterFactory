-- The existing Aseprite masters are the source. No new character or weapon is authored.
local root=assert(app.params.root);local function file(p)return app.fs.joinPath(root,p)end
local f=assert(io.open(file('experiments/main-orc-polish-v1/plan.json'),'r'));local p=json.decode(f:read('*a'));f:close()
local pc=app.pixelColor;local function blank(w,h)local im=Image(w or 256,h or 256,ColorMode.RGB);im:clear();return im end
local function save(im,path)app.fs.makeAllDirectories(app.fs.filePath(file(path)));im:saveAs(file(path))end
local function layerImage(sprite,name,frame)
 local layer=nil;for _,l in ipairs(sprite.layers)do if l.name==name then layer=l end end;assert(layer,'Missing layer '..name);local out=blank(sprite.width,sprite.height);local cel=layer:cel(frame);if cel then out:drawImage(cel.image,cel.position)end;return out
end
local function inside(x,y,pts)local c=false;local j=#pts;for i=1,#pts do local a,b=pts[i],pts[j];if(a[2]>y)~=(b[2]>y)and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1]then c=not c end;j=i end;return c end
if app.params.mode=='prepare'then
 for category,source in pairs(p.forks)do
  local s=app.open(file(source));assert(#s.frames==#p.baseline[category].frames)
  for i=1,#s.frames do
   save(layerImage(s,'body',i),p.experiment..'/baseline/'..category..string.format('/body/%02d.png',i-1));save(layerImage(s,'handFront',i),p.experiment..'/baseline/'..category..string.format('/handFront/%02d.png',i-1))
   s.frames[i].duration=p.timingOnly[category][i]/1000
  end
  app.fs.makeAllDirectories(file(p.experiment..'/timing-only'));s:saveAs(file(p.experiment..'/timing-only/'..category:lower()..'.aseprite'))
  local body=layerImage(s,'body',6);local fg=layerImage(s,'handFront',6);local native=blank(128,128);native:drawImage(body,Point(-64,-64));save(native,p.experiment..'/inputs/'..category..'-impact.png')
  local mask=blank(128,128);mask:clear(pc.rgba(0,0,0,255));local protect=category=='Sword'and{{63,52},{88,64},{101,76},{95,90},{66,77}}or{{65,49},{83,56},{94,76},{87,91},{67,78}}
  local grip=p.baseline[category].frames[6].rightGrip;local gx,gy=grip[1]-64,grip[2]-64
  local region={{40,34},{61,33},{78,39},{88,48},{89,68},{82,91},{88,108},{43,110},{40,92},{45,72}}
  for y=33,109 do for x=39,90 do
   local protected=inside(x,y,protect)or((x-gx)^2+(y-gy)^2<=12^2)
   if not protected then for dy=-1,1 do for dx=-1,1 do local xx,yy=x+dx+64,y+dy+64;if xx>=0 and xx<256 and yy>=0 and yy<256 and pc.rgbaA(fg:getPixel(xx,yy))>0 then protected=true end end end end
   if inside(x,y,region)and not protected then mask:drawPixel(x,y,pc.rgba(255,255,255,255))end
  end end
  save(mask,p.experiment..'/inputs/'..category..'-mask.png');s:close()
 end
elseif app.params.mode=='assemble'then
 local function load(path)local s=app.open(file(path));local im=blank(s.width,s.height);im:drawSprite(s,1);s:close();return im end
 for category,seq in pairs(p.sequences)do
  local bodies,hands={},{};local out=p.output..'/'..category..'/Attack';local base=p.experiment..'/baseline/'
  for i,q in ipairs(seq)do
   local body=load(base..q.from..string.format('/body/%02d.png',q.index));local hand=blank()
   if q.visible then
    if q.onset then
     -- Trace only this Orc's own closed glove; keep wrist/forearm under the item.
     for y=81,87 do for x=30,38 do if inside(x,y,{{31,82},{34,81},{38,82},{38,85},{35,87},{31,85}})then hand:drawPixel(x+64,y+64,body:getPixel(x+64,y+64))end end end
    else hand=load(base..q.from..string.format('/handFront/%02d.png',q.index))end
   end
   if q.patch then
    local patch=load(p.experiment..'/patches/'..category..'.png');local mask=load(p.experiment..'/inputs/'..category..'-mask.png')
    for y=0,127 do for x=0,127 do if pc.rgbaR(mask:getPixel(x,y))==255 then body:drawPixel(x+64,y+64,patch:getPixel(x,y))end end end
   end
   if category=='Sword'and q.index==4 then
    -- Inherited fine diagonal blade residue in transparent space; this is not anatomy.
    -- Keep the glove/guard contour from y122 down. No true weapon pixels are on body.
    for y=99,121 do for x=160,184 do body:drawPixel(x,y,0);hand:drawPixel(x,y,0)end end
    body:drawPixel(181,93,0) -- disconnected upper tip of that same inherited residue
   end
   bodies[i]=body;hands[i]=hand;save(body,out..string.format('/layers/body/%02d.png',i-1));save(hand,out..string.format('/layers/handFront/%02d.png',i-1))
  end
  for _,part in ipairs({'body','hand-front'})do
   local images=part=='body'and bodies or hands;local s=Sprite(256,256,ColorMode.RGB);s.layers[1].name=part
   for i,im in ipairs(images)do if i>1 then s:newEmptyFrame()end;s:newCel(s.layers[1],i,im,Point(0,0));s.frames[i].duration=seq[i].ms/1000 end
   app.fs.makeAllDirectories(file(p.masters));s:saveAs(file(p.masters..'/'..category:lower()..'-'..part..'.aseprite'));s:close()
  end
 end
elseif app.params.mode=='finish'then
 for category,seq in pairs(p.sequences)do
  local out=p.output..'/'..category..'/Attack';local s=app.open(file(out..'/composition.aseprite'));s:saveAs(file(p.masters..'/'..category:lower()..'-attack.aseprite'))
  local strip=blank(256*#seq,256);for i=1,#seq do local im=blank();im:drawSprite(s,i);strip:drawImage(im,Point((i-1)*256,0))end;save(strip,out..'/native-strip.png');s:close()
 end
end
