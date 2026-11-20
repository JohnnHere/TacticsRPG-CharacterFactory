local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local s=Image(128*4,128*2,ColorMode.RGB);s:clear()
for i=0,6 do local im=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/axe-r-cleaned-native/"..string.format("%02d.png",i))};im:resize(512,512);s:drawImage(im,Point((i%4)*512,math.floor(i/4)*512)) end
s:saveAs(f("experiments/main-orc-rear-recovery-v2/back_r-axe-cleaned-body-4x.png"));print("Saved 4x cleanup QA.")
