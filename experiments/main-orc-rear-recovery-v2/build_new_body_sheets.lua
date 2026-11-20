local root=app.fs.currentPath
local function f(p) return app.fs.joinPath(root,p) end
for _,dir in ipairs({"back_l","back_r_axe","back_l_axe"}) do
  local sheet=Image(128*4,128*2,ColorMode.RGB);sheet:clear()
  for i=0,6 do
    local p="experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/"..dir.."/"..string.format("%02d.png",i)
    local im=Image{fromFile=f(p)};assert(im.width==128 and im.height==128)
    sheet:drawImage(im,Point((i%4)*128,math.floor(i/4)*128))
  end
  local out="experiments/main-orc-rear-recovery-v2/"..dir.."-generated-body-sheet.png"
  sheet:saveAs(f(out))
  local zoom=Image(128*4*4,128*4*2,ColorMode.RGB);zoom:clear()
  for i=0,6 do
    local im=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/"..dir.."/"..string.format("%02d.png",i))}
    im:resize(512,512)
    zoom:drawImage(im,Point((i%4)*512,math.floor(i/4)*512))
  end
  zoom:saveAs(f("experiments/main-orc-rear-recovery-v2/"..dir.."-generated-body-sheet-4x.png"))
end
print("Built Aseprite QA sheets from the exact seven returned PNGs.")
