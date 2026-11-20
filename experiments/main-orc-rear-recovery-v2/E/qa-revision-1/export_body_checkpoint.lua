-- Re-export actual saved checkpoint masters through Aseprite for visual review.
local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local specs={
 {key="back_l-sword",master="experiments/main-orc-rear-recovery-v2/E/qa-revision-1/body-checkpoint/source/back_l-sword-body-revision-1.aseprite"},
 {key="back_r-axe",master="experiments/main-orc-rear-recovery-v2/E/qa-revision-1/body-checkpoint/source/back_r-axe-body-revision-1.aseprite"},
 {key="back_l-axe",master="experiments/main-orc-rear-recovery-v2/E/qa-revision-1/body-checkpoint/source/back_l-axe-body-revision-1.aseprite"}
}
local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
for _,sp in ipairs(specs) do
 local s=app.open(f(sp.master));assert(#s.frames==8 and #s.layers==1 and s.layers[1].name=="body")
 local dir="experiments/main-orc-rear-recovery-v2/E/qa-revision-1/body-checkpoint/exports/"..sp.key
 app.fs.makeAllDirectories(f(dir.."/body"));app.fs.makeAllDirectories(f(dir.."/native"))
 local sheet=Image(256*4,256*2,ColorMode.RGB);sheet:clear();local nativeStrip=Image(128*8,128,ColorMode.RGB);nativeStrip:clear()
 for i=1,8 do
  local body=blank(256,256);body:drawSprite(s,i);body:saveAs(f(dir.."/body/"..string.format("%02d.png",i-1)))
  local native=Image(128,128,ColorMode.RGB);native:clear();native:drawImage(body,Point(-64,-64));native:saveAs(f(dir.."/native/"..string.format("%02d.png",i-1)))
  sheet:drawImage(body,Point(((i-1)%4)*256,math.floor((i-1)/4)*256));nativeStrip:drawImage(native,Point((i-1)*128,0))
 end
 sheet:saveAs(f(dir.."/body-only-sheet-qa.png"));nativeStrip:saveAs(f(dir.."/native-strip-qa.png"));s:close()
 print("Re-exported saved body-only master "..sp.master)
end
