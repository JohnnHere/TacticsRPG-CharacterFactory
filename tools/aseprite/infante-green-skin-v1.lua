-- Aseprite palette study on own approved pixels; no new generation or body changes.
local root=assert(app.params.root);local function file(p)return app.fs.joinPath(root,p)end
local base='characters/orc-pixellab-05/source/aseprite/green-skin-v1/source/'
local out='characters/orc-pixellab-05/source/studies/PaletteVariants/green-skin-v1/'
local pc=app.pixelColor
local ramp={
 {{11,12,17},{10,18,8}},{{20,20,26},{15,27,13}},{{26,26,32},{20,35,16}},
 {{33,34,40},{25,44,19}},{{41,42,47},{32,55,24}},{{49,51,55},{40,68,28}},
 {{58,60,64},{46,79,32}},{{66,68,72},{54,91,36}},{{74,76,80},{62,103,39}},
 {{83,85,88},{70,115,43}},{{90,92,96},{79,125,47}},{{101,102,105},{90,137,52}},
 {{117,118,120},{106,151,60}},{{134,134,135},{121,164,68}},
 {{141,142,143},{133,173,77}},{{153,154,155},{148,185,91}},
 {{49,50,54},{40,68,28}},{{83,85,88},{70,115,43}}
}
local palette={};for _,v in ipairs(ramp)do palette[table.concat(v[1],',')]=pc.rgba(v[2][1],v[2][2],v[2][3],255)end
-- Hand-selected skin rows, excluding collar/armor and bright ivory tusks.
local rows={
 [6]={64,70},[7]={62,71},[8]={61,72},[9]={61,73},[10]={61,73},[11]={61,74},
 [12]={61,77},[13]={60,77},[14]={60,77},[15]={60,77},[16]={59,77},[17]={59,77},
 [18]={60,77},[19]={60,77},[20]={62,77},[21]={62,77},[22]={63,77},
 [23]={63,77},[24]={64,77},[25]={65,76},[26]={66,75}
}
local report={tool='Aseprite Lua',palette=ramp,reference='Original Infante 05 only; green Warcraft-inspired palette study',jobs={}}
for _,job in ipairs({{id='Concept',input='infante-concept.aseprite',output='green-concept.aseprite',offsets={0}},{id='Idle',input='infante-idle.aseprite',output='green-idle.aseprite',offsets={0,1,2,1,0}}})do
 local source=app.open(file(base..job.input));local sprite=Sprite(128,128,ColorMode.RGB)
 sprite.layers[1].name='Original Infante + selected green skin palette study'
 local jr={state=job.id,frames={}}
 app.fs.makeAllDirectories(file(out..job.id))
 for frame=1,#source.frames do
  local im=Image(128,128,ColorMode.RGB);im:clear();im:drawSprite(source,frame)
  local dy=job.offsets[frame];local changed={}
  for y,span in pairs(rows)do for x=span[1],span[2]do
   -- Preserve teeth and their shaded bases, as well as eye whites/highest highlights.
   local tooth=(y==23 or y==24)and((x>=68 and x<=72)or x==77)
   if not tooth then
    local color=im:getPixel(x,y+dy);local rgb={pc.rgbaR(color),pc.rgbaG(color),pc.rgbaB(color)}
    local target=palette[table.concat(rgb,',')]
    if pc.rgbaA(color)>0 and target then im:drawPixel(x,y+dy,target);changed[#changed+1]={x=x,y=y+dy,from=rgb,to={pc.rgbaR(target),pc.rgbaG(target),pc.rgbaB(target)}}end
   end
  end end
  if frame>1 then sprite:newEmptyFrame()end
  sprite:newCel(sprite.layers[1],frame,im,Point(0,0));sprite.frames[frame].duration=source.frames[frame].duration
  im:saveAs(file(out..job.id..(job.id=='Concept' and '/concept.png' or string.format('/%02d.png',frame-1))))
  jr.frames[#jr.frames+1]={frame=frame-1,offsetY=dy,changed=changed,count=#changed}
 end
 sprite:saveAs(file(base..job.output));sprite:close();source:close();report.jobs[#report.jobs+1]=jr
end
local f=assert(io.open(file('experiments/infante-green-skin-v1/retouch.json'),'w'));f:write(json.encode(report));f:close()
