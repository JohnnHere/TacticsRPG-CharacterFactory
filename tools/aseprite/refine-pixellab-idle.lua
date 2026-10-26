-- Authored in Aseprite: compress the torso by one authored pixel on inhale.
-- Face and ground contacts are copied unchanged from the PixelLab concept.
local root=assert(app.params.root)
local f=assert(io.open(app.params.plan,'r'));local plan=json.decode(f:read('*a'));f:close()
local function file(p)return app.fs.joinPath(root,p)end
for _,p in ipairs(plan.items)do
 local source=app.open(file(p.input));local base=Image(source.width,source.height,ColorMode.RGB);base:clear();base:drawSprite(source,1);source:close()
 local inhale=Image(base)
 for y=p.headLockY+1,p.waistCutY-1 do
  for x=0,base.width-1 do inhale:drawPixel(x,y,base:getPixel(x,y+1))end
 end
 local s=Sprite(base.width,base.height,ColorMode.RGB)
 local art=s.layers[1];art.name='Idle breathing - one pixel torso edit'
 local ref=s:newLayer();ref.name='Original PixelLab concept - preserved reference';ref.isVisible=false
 app.fs.makeAllDirectories(file(p.output))
 for i,pose in ipairs(plan.poses)do
  if i>1 then s:newEmptyFrame()end
  local image=pose==1 and inhale or base
  s:newCel(art,i,image,Point(0,0));s:newCel(ref,i,base,Point(0,0));s.frames[i].duration=plan.durationsMs[i]/1000
  image:saveAs(file(p.output..string.format('/%02d.png',i-1)))
 end
 local tag=s:newTag(1,#plan.poses);tag.name='Idle'
 s:saveAs(file(p.master));s:close()
 print('Refined '..p.id..' Idle in Aseprite; face and feet fixed; torso 0/1 pixel.')
end
