local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local spec={
 {"AxeL frame 01","experiments/main-orc-rear-recovery-v2/back_l-axe-cleaned-native/01.png"},
 {"AxeL frame 02","experiments/main-orc-rear-recovery-v2/back_l-axe-cleaned-native/02.png"},
 {"SwordL accepted F02","characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/native/02.png"},
 {"SwordL accepted F03","characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/native/03.png"}
}
local sheet=Image(512*2,512*2,ColorMode.RGB);sheet:clear()
for i,v in ipairs(spec) do local src=Image{fromFile=f(v[2])};local crop=Image(64,64,ColorMode.RGB);crop:clear();crop:drawImage(src,Point(-8,-0));crop:resize(512,512);sheet:drawImage(crop,Point(((i-1)%2)*512,math.floor((i-1)/2)*512)) end
sheet:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-axe-swordL-arm-donor-comparison-qa.png"));print("Saved actual AxeL and same-view accepted SwordL attack-arm comparison crops from Aseprite sources.")
