-- Darken only the previously authored green skin pixels in Aseprite.
local root=assert(app.params.root);local function file(p)return app.fs.joinPath(root,p)end
local f=assert(io.open(file('experiments/infante-green-skin-v1/retouch.json'),'r'));local log=json.decode(f:read('*a'));f:close()
local pc=app.pixelColor;local base='characters/orc-pixellab-05/source/aseprite/green-skin-v2/source/'
local out='characters/orc-pixellab-05/source/studies/PaletteVariants/green-skin-v2/'
for j,job in ipairs(log.jobs)do
 local state=job.state;local stem=state=='Concept'and 'concept'or'idle'
 local s=app.open(file(base..'green-'..stem..'.aseprite'))
 s.layers[1].name='Green skin palette v2 - darker, same approved body and Idle'
 app.fs.makeAllDirectories(file(out..state))
 for i,frame in ipairs(job.frames)do
  local im=Image(128,128,ColorMode.RGB);im:clear();im:drawSprite(s,i)
  for _,p in ipairs(frame.changed)do
   local c=im:getPixel(p.x,p.y)
   assert(pc.rgbaR(c)==p.to[1]and pc.rgbaG(c)==p.to[2]and pc.rgbaB(c)==p.to[3],'Skin source changed')
   im:drawPixel(p.x,p.y,pc.rgba(math.floor(p.to[1]*.80+.5),math.floor(p.to[2]*.82+.5),math.floor(p.to[3]*.80+.5),pc.rgbaA(c)))
  end
  s:newCel(s.layers[1],i,im,Point(0,0))
  im:saveAs(file(out..state..(state=='Concept'and '/concept.png'or string.format('/%02d.png',i-1))))
 end
 s:saveAs(file(base..'dark-green-'..stem..'.aseprite'));s:close()
end
