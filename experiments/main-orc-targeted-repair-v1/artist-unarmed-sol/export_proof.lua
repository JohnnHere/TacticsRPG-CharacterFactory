-- Independent fresh Aseprite renders of copied source and candidate forks.
local E="experiments/main-orc-targeted-repair-v1/artist-unarmed-sol"
local S="characters/orc-v1/source/targeted-repair-unarmed-sol-v1"
local function f(p)return app.fs.joinPath(app.fs.currentPath,p)end
local records={}
for _,sp in ipairs({
 {"before-native",E.."/before/unarmed-back_l.aseprite"},
 {"before-composite",E.."/before/unarmed-attack.aseprite"},
 {"candidate-native",S.."/source/unarmed-back_l-f03-retraction-native.aseprite"},
 {"candidate-composite",S.."/source/unarmed-back_l-f03-retraction-composite.aseprite"}
})do
 local s=app.open(f(sp[2]));app.fs.makeAllDirectories(f(E.."/source-proof/"..sp[1]))
 local r={key=sp[1],source=sp[2],width=s.width,height=s.height,layers={},frames={}}
 for _,l in ipairs(s.layers)do table.insert(r.layers,l.name)end
 for i=1,5 do
  local im=Image(s.width,s.height,ColorMode.RGB);im:clear();im:drawSprite(s,i)
  im:saveAs(f(E.."/source-proof/"..sp[1].."/"..string.format("%02d.png",i-1)))
  local c=s.layers[1]:cel(i)
  table.insert(r.frames,{index=i-1,durationMs=math.floor(s.frames[i].duration*1000+0.5),celPosition={c.position.x,c.position.y},celImageSize={c.image.width,c.image.height}})
 end;table.insert(records,r);s:close()
end
local file=io.open(f(E.."/source-proof/document.json"),"w");file:write(json.encode(records));file:close()
print("Fresh20 frame renders from4 saved sources; frame/cel position metadata recorded.")
