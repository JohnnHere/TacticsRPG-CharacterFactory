local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local specs={
 {"AxeL repaired F02","experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native/02.png"},
 {"AxeL cleaned raw F02","experiments/main-orc-rear-recovery-v2/back_l-axe-cleaned-native/02.png"},
 {"NW base","experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png"}
}
local sheet=Image(384*3,384,ColorMode.RGB);sheet:clear()
for i,s in ipairs(specs)do local im=Image{fromFile=f(s[2])};local c=Image(48,48,ColorMode.RGB);c:clear();c:drawImage(im,Point(-2,-2));c:resize(384,384);sheet:drawImage(c,Point((i-1)*384,0))end
sheet:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-axe-detached-old-arm-qa.png"));print("Saved exact reported AxeL component region x2..50,y2..50 at 8x for repaired/raw/base comparison.")
