local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local centers={{40,14},{40,14},{22,54},{22,69},{19,83},{29,68}}
local sheet=Image(384*3,384*2,ColorMode.RGB);sheet:clear()
for i=1,6 do
 local frame=string.format("%02d.png",i)
 local before=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/back_l-axe-cleaned-native/"..frame)}
 local after=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native/"..frame)}
 for side,img in ipairs({before,after}) do
  local crop=Image(32,32,ColorMode.RGB);crop:clear();crop:drawImage(img,Point(16-centers[i][1],16-centers[i][2]));crop:resize(192,192)
  sheet:drawImage(crop,Point(((i-1)%3)*384+(side-1)*192,math.floor((i-1)/3)*384))
 end
end
sheet:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-axe-arm-before-after-grip-crops-qa.png"));print("Saved actual 1x before/after source regions around each AxeL hand/gauntlet anchor.")
