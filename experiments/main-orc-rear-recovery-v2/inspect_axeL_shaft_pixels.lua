local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local function alpha(p)return app.pixelColor.rgbaA(p)end
local function classify(p)
 if alpha(p)==0 then return "." end
 local r,g,b=app.pixelColor.rgbaR(p),app.pixelColor.rgbaG(p),app.pixelColor.rgbaB(p)
 if g>r*1.18 and g>b*1.12 then return "G" end
 if r>g*1.04 and g>b*1.04 and r>45 then return "B" end
 return "#"
end
local raw="experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l_axe/"
local donorBody=Image{fromFile=f("characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/body/02.png")}
local donorHand=Image{fromFile=f("characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/handFront/02.png")}
local donor=Image(128,128,ColorMode.RGB);donor:clear();donor:drawImage(donorBody,Point(-64,-64));donor:drawImage(donorHand,Point(-64,-64))
for _,spec in ipairs({{"RAW AxeL 01",raw.."01.png"},{"RAW AxeL 02",raw.."02.png"},{"REPAIRED AxeL 01","experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native/01.png"},{"REPAIRED AxeL 02","experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native/02.png"}}) do
 local im=Image{fromFile=f(spec[2])};print(spec[1].." ROI native x30..85 y0..23; B=brown/red, G=green head, #=other opaque")
 for y=0,23 do local s=string.format("%02d ",y);for x=30,85 do s=s..classify(im:getPixel(x,y)) end;print(s) end
end
print("SwordL accepted F02 body+handFront donor pre-offset ROI native x30..85 y0..23")
for y=0,23 do local s=string.format("%02d ",y);for x=30,85 do s=s..classify(donor:getPixel(x,y)) end;print(s) end
