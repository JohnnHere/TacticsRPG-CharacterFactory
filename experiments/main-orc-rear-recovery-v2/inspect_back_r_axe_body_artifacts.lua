local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local out="characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1"
local sheet=Image(128*4,128*2,ColorMode.RGB);sheet:clear()
for i=0,7 do local im=Image{fromFile=f(out.."/native/"..string.format("%02d.png",i))};im:resize(512,512);sheet:drawImage(im,Point((i%4)*512,math.floor(i/4)*512)) end
sheet:saveAs(f("experiments/main-orc-rear-recovery-v2/back_r-axe-body-only-all-frames-4x.png"))
local body=Image{fromFile=f(out.."/layers/body/04.png")}
local crop=Image(40,40,ColorMode.RGB);crop:clear();crop:drawImage(body,Point(-144,-63));crop:resize(320,320);crop:saveAs(f("experiments/main-orc-rear-recovery-v2/back_r-axe-f04-body-fragment-10x.png"))
print("Saved whole-cycle body-only view and crop centered at reported composite (164,83).")
