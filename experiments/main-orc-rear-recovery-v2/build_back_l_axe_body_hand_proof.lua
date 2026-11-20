-- QA-only crops from the Aseprite-cleaned AxeL body source.
local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local out="experiments/main-orc-rear-recovery-v2/back_l-axe-hand-candidate-qa.png"
local centers={{22,8},{34,10},{40,22},{16,55},{28,79},{46,60}}
local sheet=Image(192*3,192*2,ColorMode.RGB);sheet:clear()
for i=1,6 do
 local im=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/back_l-axe-cleaned-native/"..string.format("%02d.png",i))}
 local x,y=centers[i][1],centers[i][2];local crop=Image(48,48,ColorMode.RGB);crop:clear()
 crop:drawImage(im,Point(24-x,24-y));crop:resize(192,192)
 sheet:drawImage(crop,Point(((i-1)%3)*192,math.floor((i-1)/3)*192))
end
sheet:saveAs(f(out));print("Saved six hand/forearm crops from cleaned AxeL source for measuring actual hand centers.")
