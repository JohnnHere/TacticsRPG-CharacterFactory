-- Read-only check of the hidden approved references embedded in each V4 source.
local root=assert(app.params.root);local base=app.fs.joinPath(root,'characters/orc-01-aseprite-v4/source/aseprite/retouched')
local count=0
for _,id in ipairs({'attack','hit','concept'})do
 local s=app.open(app.fs.joinPath(base,id..'.aseprite'))
 for i,l in ipairs(s.layers)do l.isVisible=i==1 end
 for f=1,#s.frames do
  local originalPath=id=='concept' and 'characters/orc-01-refinement-v2/concepts/warrior-refinement-v2.png' or string.format('characters/orc-01/source/aseprite/combat-refinement-v2/%s/%s_front_r_%02d.png',id=='attack' and 'Attack' or 'Hit',id,f-1)
  local expected=Image{fromFile=app.fs.joinPath(root,originalPath)}
  local actual=Image(s.width,s.height,ColorMode.RGB);actual:clear();actual:drawSprite(s,f)
  for y=0,s.height-1 do for x=0,s.width-1 do assert(actual:getPixel(x,y)==expected:getPixel(x,y),'Preserved V2 cel differs: '..id..'/'..f)end end
  count=count+1
 end
 s:close() -- Changes only in this independent process; never save.
end
print('PASS: '..count..' hidden V2 reference cels pixel-identical; masters not modified')
