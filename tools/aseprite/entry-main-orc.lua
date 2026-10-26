-- Attack-entry candidate assembly. Source art belongs to the orchestrator plan (entry-plan.json);
-- this script only resolves baseline layers/inputs already exported in Aseprite into body, finger,
-- composite masters and layer PNGs. It never draws or retouches character/weapon pixels.
local root=assert(app.params.root)
local function file(p)return app.fs.joinPath(root,p)end
local handle=assert(io.open(assert(app.params.plan),'r'));local plan=json.decode(handle:read('*a'));handle:close()
local function blank(w,h)local im=Image(w or 256,h or 256,ColorMode.RGB);im:clear();return im end
local function save(im,path)app.fs.makeAllDirectories(app.fs.filePath(file(path)));im:saveAs(file(path))end
local function load(path)
 local source=app.open(file(path));local im=Image(source.width,source.height,ColorMode.RGB);im:clear();im:drawSprite(source,1);source:close()
 if im.width~=256 or im.height~=256 then error('Canvas fora de 256x256 em '..tostring(path)) end
 return im
end
if app.params.mode=='assemble' then
 for category,sequence in pairs(plan.sequences) do
  local out=plan.output..'/'..category..'/Attack'
  local bodies,hands={},{}
  for i,q in ipairs(sequence) do
   local body=load(q.bodyInput or q.bodySource)
   -- Layer contract: an unarmed frame owns no handFront overlay, even when the plan supplies
   -- finger input for the same body. Fingers only override the weapon handle while armed.
   local hand
   if not q.visible then hand=blank()
   elseif q.handInput then hand=load(q.handInput)
   else hand=load(q.handSource) end
   bodies[i],hands[i]=body,hand
   save(body,out..string.format('/layers/body/%02d.png',i-1))
   save(hand,out..string.format('/layers/handFront/%02d.png',i-1))
  end
  for _,part in ipairs({'body','hand-front'}) do
   local images=part=='body'and bodies or hands
   local sprite=Sprite(256,256,ColorMode.RGB);sprite.layers[1].name=part
   for i,im in ipairs(images)do
    if i>1 then sprite:newEmptyFrame()end
    sprite:newCel(sprite.layers[1],i,im,Point(0,0))
    sprite.frames[i].duration=sequence[i].durationMs/1000
   end
   app.fs.makeAllDirectories(file(plan.masters))
   sprite:saveAs(file(plan.masters..'/'..category:lower()..'-'..part..'.aseprite'))
   sprite:close()
  end
 end
elseif app.params.mode=='finish' then
 for category,sequence in pairs(plan.sequences) do
  local out=plan.output..'/'..category..'/Attack'
  local sprite=app.open(file(out..'/composition.aseprite'))
  sprite:saveAs(file(plan.masters..'/'..category:lower()..'-attack.aseprite'))
  local strip=Image(256*#sequence,256,ColorMode.RGB);strip:clear()
  for i=1,#sequence do
   local frameImage=blank();frameImage:drawSprite(sprite,i)
   strip:drawImage(frameImage,Point((i-1)*256,0))
  end
  save(strip,out..'/native-strip.png')
  sprite:close()
 end
else error('entry-main-orc.lua: modo invalido: '..tostring(app.params.mode)) end
