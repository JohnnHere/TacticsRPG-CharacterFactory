local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
for i=1,6 do
 local im=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native/"..string.format("%02d.png",i))}
 local crop=Image(64,96,ColorMode.RGB);crop:clear();crop:drawImage(im,Point(0,0))
 for x=0,64,8 do for y=0,95 do crop:drawPixel(x,y,app.pixelColor.rgba(54,54,70,255)) end end
 for y=0,96,8 do for x=0,63 do crop:drawPixel(x,y,app.pixelColor.rgba(54,54,70,255)) end end
 crop:resize(512,768);crop:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-axe-arm-grid-"..string.format("%02d",i)..".png"))
end
print("Saved 8px coordinate grid overlays for repaired AxeL attacking-arm regions (QA only).")
