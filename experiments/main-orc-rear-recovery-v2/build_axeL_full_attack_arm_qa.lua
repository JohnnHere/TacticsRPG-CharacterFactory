local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local sheet=Image(256*3,384*2,ColorMode.RGB);sheet:clear()
for i=1,6 do
 local im=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native/"..string.format("%02d.png",i))}
 local crop=Image(64,96,ColorMode.RGB);crop:clear();crop:drawImage(im,Point(0,0));crop:resize(256,384)
 sheet:drawImage(crop,Point(((i-1)%3)*256,math.floor((i-1)/3)*384))
end
sheet:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-axe-complete-left-arm-crops-qa.png"));print("Saved full left-side arm crops from all six AxeL attack poses.")
