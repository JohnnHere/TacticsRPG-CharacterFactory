local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local specs={
 {"back_l-sword","characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/sword-attack-representative-v1.aseprite"},
 {"back_r-axe","characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_r/axe-attack-representative-v1.aseprite"},
 {"back_l-axe","characters/orc-v1/source/aseprite/rear-recovery-v2/composite/back_l/axe-attack-representative-v1.aseprite"}
}
local scales={{"1x",{90,80,90,80,100,80,100,110}},{"075x",{120,110,120,110,130,110,130,150}},{"05x",{180,160,180,160,200,160,200,220}}}
local axeLOnly=os.getenv("ASEPRITE_AXE_L_ONLY")=="1"
for _,sp in ipairs(specs) do if not axeLOnly or sp[1]=="back_l-axe" then for _,scale in ipairs(scales) do
 local s=app.open(f(sp[2]));for i,fr in ipairs(s.frames)do fr.duration=scale[2][i]/1000 end
 local p="experiments/main-orc-rear-recovery-v2/"..sp[1].."-representative-"..scale[1]..".gif";assert(s:saveAs(f(p)),"GIF export failed: "..p);s:close()
end end end
print("Exported six 8-frame playback GIFs from the saved Aseprite representative masters.")
