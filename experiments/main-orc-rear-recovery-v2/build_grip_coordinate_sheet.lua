local root=app.fs.currentPath
local function f(p) return app.fs.joinPath(root,p) end
for _,d in ipairs({"back_l","back_r_axe"}) do
  local out=Image(128*7,128,ColorMode.RGB);out:clear()
  for i=0,6 do
    local im=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/"..d.."/"..string.format("%02d.png",i))}
    for q=0,8 do
      local c=q%2==0 and app.pixelColor.rgba(245,70,210,180) or app.pixelColor.rgba(70,225,255,170)
      local x=q*16; for y=0,127 do im:drawPixel(x,y,c) end
      local y=q*16; for x=0,127 do im:drawPixel(x,y,c) end
    end
    out:drawImage(im,Point(i*128,0))
  end
  out:resize(128*7*4,128*4)
  out:saveAs(f("experiments/main-orc-rear-recovery-v2/"..d.."-grip-coordinate-qa.png"))
  if d=="back_r_axe" then
    for i=0,6 do
      local im=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/"..d.."/"..string.format("%02d.png",i))}
      for q=0,8 do local c=q%2==0 and app.pixelColor.rgba(245,70,210,180) or app.pixelColor.rgba(70,225,255,170); for y=0,127 do im:drawPixel(q*16,y,c) end; for x=0,127 do im:drawPixel(x,q*16,c) end end
      im:resize(768,768);im:saveAs(f("experiments/main-orc-rear-recovery-v2/back_r_axe-frame-"..string.format("%02d",i).."-coordinate-qa.png"))
    end
  end
  if d=="back_l" then
    for i=0,6 do local im=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/"..d.."/"..string.format("%02d.png",i))};for q=0,8 do local c=q%2==0 and app.pixelColor.rgba(245,70,210,180) or app.pixelColor.rgba(70,225,255,170);for y=0,127 do im:drawPixel(q*16,y,c) end;for x=0,127 do im:drawPixel(x,q*16,c) end end;im:resize(768,768);im:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-frame-"..string.format("%02d",i).."-4x.png")) end
  end
end
print("Created QA-only Aseprite coordinate overlays.")
