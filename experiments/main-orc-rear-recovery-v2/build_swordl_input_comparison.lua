local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local s=Image(768*4,768*2,ColorMode.RGB);s:clear()
local paths={"experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png"}
for i=0,6 do paths[#paths+1]="experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l/"..string.format("%02d.png",i) end
for i,p in ipairs(paths) do local im=Image{fromFile=f(p)};im:resize(768,768);s:drawImage(im,Point(((i-1)%4)*768,math.floor((i-1)/4)*768)) end
s:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-input-vs-returned-4x.png"));print("Saved native input plus all returned SwordL frames at 4x.")
