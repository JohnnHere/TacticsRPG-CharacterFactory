-- Review-only actual playback exports from the saved Aseprite master.
local root=app.fs.currentPath
local function file(p) return app.fs.joinPath(root,p) end
local src="characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/sword-attack-representative-v2.aseprite"
local out="experiments/main-orc-rear-recovery-v2"
local scales={
 {"1x",{90,80,90,80,100,80,100,110}},
 -- GIF stores centiseconds; nearest 10 ms values approximate the 0.75x target.
 {"075x",{120,110,120,110,130,110,130,150}},
 {"05x",{180,160,180,160,200,160,200,220}}
}
for _,v in ipairs(scales) do
 local s=Sprite{fromFile=file(src)}
 for i,f in ipairs(s.frames) do f.duration=v[2][i]/1000 end
 local path=out.."/back_r-sword-representative-"..v[1]..".gif"
 assert(s:saveAs(file(path)),"GIF export failed: "..path)
 s:close()
end
print("Saved 1x, 0.75x and 0.5x review GIFs from saved representative Aseprite master.")
