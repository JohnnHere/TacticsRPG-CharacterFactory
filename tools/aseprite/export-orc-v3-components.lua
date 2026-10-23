-- Preview derivatives only, rendered by Aseprite from its own native sources.
local source=assert(app.params.source);local output=assert(app.params.output)
for _,id in ipairs({"concept","attack","hit"})do
 local s=app.open(app.fs.joinPath(source,id..".aseprite"))
 local directory=app.fs.joinPath(output,id);app.fs.makeAllDirectories(directory)
 local states={};for i,l in ipairs(s.layers)do states[i]=l.isVisible;l.isVisible=false end
 for i,l in ipairs(s.layers)do
  l.isVisible=true
  for f=1,#s.frames do
   local render=Image(128,128,ColorMode.RGB);render:clear();render:drawSprite(s,f)
   render:saveAs(app.fs.joinPath(directory,string.format("layer-%02d-frame-%02d.png",i,f-1)))
  end
  l.isVisible=false
 end
 for i,l in ipairs(s.layers)do l.isVisible=states[i]end
 s:close()
end
print("81 regional layer previews rendered from Aseprite sources; source files not modified")
