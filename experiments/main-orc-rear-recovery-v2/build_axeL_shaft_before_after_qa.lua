local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local paths={
 "experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l_axe/01.png",
 "experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native/01.png",
 "experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l_axe/02.png",
 "experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native/02.png"
}
local sheet=Image(448*2,208*2,ColorMode.RGB);sheet:clear()
for i,p in ipairs(paths) do local im=Image{fromFile=f(p)};local c=Image(56,26,ColorMode.RGB);c:clear();c:drawImage(im,Point(-30,0));c:resize(448,208);sheet:drawImage(c,Point(((i-1)%2)*448,math.floor((i-1)/2)*208)) end
sheet:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-axe-shaft-before-after-qa.png"));print("Saved upper-head shaft crops, raw vs repaired, in source-frame order.")
