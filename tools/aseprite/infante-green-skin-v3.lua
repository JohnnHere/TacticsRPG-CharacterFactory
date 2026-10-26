-- Aseprite-only palette retouch; colors sampled from official Warcraft Orc skin.
local root=assert(app.params.root);local function file(p)return app.fs.joinPath(root,p)end
local function read(p)local f=assert(io.open(file(p),'r'));local v=json.decode(f:read('*a'));f:close();return v end
local log=read('experiments/infante-green-skin-v1/retouch.json')
local palette=read('experiments/infante-green-skin-v3/palette.json');local mapping={}
for _,v in ipairs(palette.ramp)do mapping[table.concat(v.fromGreenV1,',')]=v.to end
local base='characters/orc-pixellab-05/source/aseprite/green-skin-v3/source/'
local out='characters/orc-pixellab-05/source/studies/PaletteVariants/green-skin-v3/'
for _,job in ipairs(log.jobs)do
 local state=job.state;local stem=state=='Concept'and'concept'or'idle'
 local s=app.open(file(base..'green-'..stem..'.aseprite'))
 s.layers[1].name='Warcraft sampled darker green skin - Aseprite palette study v3'
 app.fs.makeAllDirectories(file(out..state))
 for i,frame in ipairs(job.frames)do
  local im=Image(128,128,ColorMode.RGB);im:clear();im:drawSprite(s,i)
  for _,p in ipairs(frame.changed)do
   local rgb=assert(mapping[table.concat(p.to,',')]);im:drawPixel(p.x,p.y,app.pixelColor.rgba(rgb[1],rgb[2],rgb[3],255))
  end
  s:newCel(s.layers[1],i,im,Point(0,0))
  im:saveAs(file(out..state..(state=='Concept'and'/concept.png'or string.format('/%02d.png',i-1))))
 end
 s:saveAs(file(base..'warcraft-green-'..stem..'.aseprite'));s:close()
end
