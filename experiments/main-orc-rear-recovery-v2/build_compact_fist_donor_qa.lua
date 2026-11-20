local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
for _,v in ipairs({
 {"back_l", "back_l-sword-native128.png",31,82},
 {"back_r", "back_r-axe-native128.png",96,82}
}) do
 local im=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/inputs/"..v[2])}
 local crop=Image(13,13,ColorMode.RGB);crop:clear()
 for y=0,12 do for x=0,12 do local p=im:getPixel(v[3]-6+x,v[4]-6+y);crop:drawPixel(x,y,p) end end
 crop:resize(208,208);crop:saveAs(f("experiments/main-orc-rear-recovery-v2/"..v[1].."-compact-fist-donor-13x13-qa.png"))
end
print("Saved exact 13x13 donor crops centered on the Root-indicated same-view fist landmarks.")
