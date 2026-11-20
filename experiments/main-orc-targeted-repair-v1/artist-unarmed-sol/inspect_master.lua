local E="experiments/main-orc-targeted-repair-v1/artist-unarmed-sol"
local function f(p)return app.fs.joinPath(app.fs.currentPath,p)end
local function inspect(path,name)
 local s=app.open(f(path));print(name.." canvas="..s.width.."x"..s.height.." layers="..#s.layers.." frames="..#s.frames)
 app.fs.makeAllDirectories(f(E.."/fresh-before/"..name))
 for li,l in ipairs(s.layers)do
  print("layer="..li.." name="..l.name)
  for i=1,#s.frames do local cel=l:cel(i);if cel then print(string.format("F%02d cel.position=(%d,%d) image=%dx%d duration=%d",i-1,cel.position.x,cel.position.y,cel.image.width,cel.image.height,math.floor(s.frames[i].duration*1000+0.5))) end end
 end
 for i=1,#s.frames do local im=Image(s.width,s.height,ColorMode.RGB);im:clear();im:drawSprite(s,i);im:saveAs(f(E.."/fresh-before/"..name.."/"..string.format("%02d.png",i-1))) end
 s:close()
end
inspect(E.."/before/unarmed-attack.aseprite","composite")
inspect(E.."/before/unarmed-back_l.aseprite","native")
