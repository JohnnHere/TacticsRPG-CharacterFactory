local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local paths={"experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native/02.png","experiments/main-orc-rear-recovery-v2/back_l-axe-cleaned-native/02.png","experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png"}
local sheet=Image(192*3,256,ColorMode.RGB);sheet:clear()
for i,p in ipairs(paths)do local im=Image{fromFile=f(p)};local c=Image(12,16,ColorMode.RGB);c:clear();c:drawImage(im,Point(-18,-20));c:resize(192,256);sheet:drawImage(c,Point((i-1)*192,0))end
sheet:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-axe-component-micro-qa.png"));print("Saved 16x actual source pixels at reported bbox around x18..28,y22..35: repaired, cleaned, base.")
