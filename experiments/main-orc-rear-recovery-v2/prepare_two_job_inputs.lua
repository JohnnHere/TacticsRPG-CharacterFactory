-- Aseprite-only native body inputs; crop each direction's own approved base.
local root=app.fs.currentPath
local function file(p) return app.fs.joinPath(root,p) end
local targets={
 {"back_l-sword","back_l"},
 {"back_r-axe","back_r"}
}
app.fs.makeAllDirectories(file("experiments/main-orc-rear-recovery-v2/inputs"))
for _,t in ipairs(targets) do
 local direction=t[2]
 local p="characters/orc-v1/source/complete-v1/"..direction.."/Directions/base.png"
 local source=Image{fromFile=file(p)}
 assert(source.width==256 and source.height==256,"approved directional base must be composite 256")
 local native=Image(128,128,ColorMode.RGB);native:clear();native:drawImage(source,Point(-64,-64))
 local out="experiments/main-orc-rear-recovery-v2/inputs/"..t[1].."-native128.png"
 native:saveAs(file(out))
 local spr=Sprite(128,128,ColorMode.RGB);spr.layers[1].name="body_"..direction
 spr:newCel(spr.layers[1],1,native,Point(0,0));spr.frames[1].duration=0.1;spr:saveAs(file("characters/orc-v1/source/aseprite/rear-recovery-v2/native/"..t[1].."-base.aseprite"));spr:close()
end
print("Prepared two own-direction native128 Aseprite body-only generation references.")
