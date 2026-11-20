-- Aseprite-only local cleanup of the contaminated PixelLab AxeR outputs.
-- Original 7 raw frames remain immutable under raw/pixellab-skeleton-v3.
local root=app.fs.currentPath
local function f(p) return app.fs.joinPath(root,p) end
local function alpha(p) return app.pixelColor.rgbaA(p) end
local input="experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_r_axe/"
local out="experiments/main-orc-rear-recovery-v2/axe-r-cleaned-native"
app.fs.makeAllDirectories(f(out))
local mask={
 [2]={{105,0},{127,0},{127,45},{120,44},{111,31},{107,23}},
 [3]={{100,0},{127,0},{127,48},{120,48},{113,41},{105,38}},
 [4]={{110,43},{127,42},{127,89},{111,87},{108,75},{111,67}},
 [5]={{109,54},{127,54},{127,96},{110,96},{106,82},{109,74}},
 [6]={{106,59},{127,58},{127,99},{110,98},{105,85},{105,76}}
}
local shaftMask={
 [4]={{101,47},{112,47},{118,68},{109,73},{101,62}},
 [5]={{99,53},{109,49},{117,68},{108,75},{98,67}},
 [6]={{96,57},{105,54},{115,74},{106,81},{95,73}}
}
local rects={
 [2]={{108,0,127,46}},
 [3]={{101,0,127,50}},
 [4]={{110,42,127,95},{104,48,116,70}},
 [5]={{109,44,127,99},{102,51,116,76}},
 [6]={{107,49,127,101},{100,55,115,81}}
}
local records={}
local function inside(x,y,poly)
 local c=false;local j=#poly
 for i=1,#poly do local xi,yi=poly[i][1],poly[i][2];local xj,yj=poly[j][1],poly[j][2]
  if ((yi>y)~=(yj>y)) and (x<(xj-xi)*(y-yi)/(yj-yi)+xi) then c=not c end;j=i
 end
 return c
end
local function erasePolygon(im,poly)
 local minX,minY,maxX,maxY=127,127,0,0
 for _,p in ipairs(poly) do minX=math.min(minX,p[1]);maxX=math.max(maxX,p[1]);minY=math.min(minY,p[2]);maxY=math.max(maxY,p[2]) end
 local n=0
 for y=minY,maxY do for x=minX,maxX do if inside(x,y,poly) and alpha(im:getPixel(x,y))>0 then im:drawPixel(x,y,app.pixelColor.rgba(0,0,0,0));n=n+1 end end end
 return n
end
local function eraseRect(im,r)
 local n=0;for y=r[2],r[4] do for x=r[1],r[3] do if alpha(im:getPixel(x,y))>0 then im:drawPixel(x,y,app.pixelColor.rgba(0,0,0,0));n=n+1 end end end;return n
end
for i=0,6 do
 local im=Image{fromFile=f(input..string.format("%02d.png",i))};assert(im.width==128 and im.height==128)
 local erased=0;if mask[i] then erased=erasePolygon(im,mask[i]) end
 if shaftMask[i] then erased=erased+erasePolygon(im,shaftMask[i]) end
 for _,r in ipairs(rects[i] or {}) do erased=erased+eraseRect(im,r) end
 -- Root identified a detached 2px generated axe-shaft fragment in composite
 -- F04 at (164,83). In this raw native frame it is x=99..100,y=18..30.
 local rootResidual=0
 if i==3 then for y=18,30 do for x=99,100 do if alpha(im:getPixel(x,y))>0 then im:drawPixel(x,y,app.pixelColor.rgba(0,0,0,0));rootResidual=rootResidual+1 end end end end
 if rootResidual>0 then print(string.format("raw 03 root residual cleanup x99..100 y18..30 removed %d pixels",rootResidual)) end
 if mask[i] then print(string.format("raw %02d head/shaft masks erased %d pixels",i,erased)) end
 im:saveAs(f(out.."/"..string.format("%02d.png",i)))
 records[#records+1]={rawFrame=i,polygons=mask[i] or {},alphaPixelsErased=erased,cleaned=out.."/"..string.format("%02d.png",i)}
end
local strip=Image(128*4,128*2,ColorMode.RGB);strip:clear()
for i=0,6 do local im=Image{fromFile=f(out.."/"..string.format("%02d.png",i))};strip:drawImage(im,Point((i%4)*128,math.floor(i/4)*128)) end
strip:saveAs(f("experiments/main-orc-rear-recovery-v2/back_r-axe-weapon-layers-off-cleanup-preview.png"))
local bodyMaster="characters/orc-v1/source/aseprite/rear-recovery-v2/native/axe-body-only-back_r-representative.aseprite"
app.fs.makeAllDirectories(app.fs.filePath(f(bodyMaster)))
local s=Sprite(128,128,ColorMode.RGB);s.layers[1].name="AxeR_empty_hand_body"
local durations={0.09,0.08,0.09,0.08,0.10,0.08,0.10}
for i=0,6 do if i>0 then s:newEmptyFrame() end;s:newCel(s.layers[1],i+1,Image{fromFile=f(out.."/"..string.format("%02d.png",i))},Point(0,0));s.frames[i+1].duration=durations[i+1] end
s:newTag(1,7).name="AxeR_body_source";s:saveAs(f(bodyMaster));s:close()
-- SwordL also carried a generated object beside the nondominant hip/hand in
-- raw 01..06. Restore only the matching own-direction relaxed gauntlet patch
-- from the exact native input; the attacking arm on viewer-left is untouched.
local swordDir="experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l/"
local donor=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png")}
local swordOut="experiments/main-orc-rear-recovery-v2/back_l-sword-cleaned-native"
app.fs.makeAllDirectories(f(swordOut))
local swordFrames={}
for i=0,6 do
 local im=Image{fromFile=f(swordDir..string.format("%02d.png",i))}
 if i>=1 then
  for y=46,84 do for x=96,112 do im:drawPixel(x,y,app.pixelColor.rgba(0,0,0,0));local p=donor:getPixel(x,y);if alpha(p)>0 then im:drawPixel(x,y,p) end end end
 end
 im:saveAs(f(swordOut.."/"..string.format("%02d.png",i)));swordFrames[#swordFrames+1]=im
end
local swordSheet=Image(128*4,128*2,ColorMode.RGB);swordSheet:clear()
for i=0,6 do swordSheet:drawImage(swordFrames[i+1],Point((i%4)*128,math.floor(i/4)*128)) end
swordSheet:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-sword-weapon-layers-off-cleanup-preview.png"))
local swordMaster="characters/orc-v1/source/aseprite/rear-recovery-v2/native/sword-body-only-back_l-representative.aseprite"
local sl=Sprite(128,128,ColorMode.RGB);sl.layers[1].name="SwordL_empty_hand_body"
for i=0,6 do if i>0 then sl:newEmptyFrame() end;sl:newCel(sl.layers[1],i+1,swordFrames[i+1],Point(0,0));sl.frames[i+1].duration=durations[i+1] end
sl:newTag(1,7).name="SwordL_body_source";sl:saveAs(f(swordMaster));sl:close()

-- AxeL raw 01..03 contains an extra generated axe beside the non-dominant
-- viewer-right pauldron. Restore only that stationary own-direction region
-- from the approved NW empty-hand input. The raised/clenched attacking arm
-- is viewer-left and remains untouched. This patch is authored in Aseprite.
local axeLDir="experiments/main-orc-rear-recovery-v2/raw/pixellab-skeleton-v3/back_l_axe/"
local axeLBase=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png")}
local axeLOut="experiments/main-orc-rear-recovery-v2/back_l-axe-cleaned-native"
app.fs.makeAllDirectories(f(axeLOut))
local axeLFrames={}
for i=0,6 do
 local im=Image{fromFile=f(axeLDir..string.format("%02d.png",i))}
 local restored=0
 if i>=1 and i<=3 then
  for y=20,58 do for x=96,127 do
   local p=axeLBase:getPixel(x,y);local q=im:getPixel(x,y)
   if q~=p then restored=restored+1 end
   im:drawPixel(x,y,p)
  end end
 end
 if restored>0 then print(string.format("AxeL raw %02d restore non-dominant shoulder/weapon contamination x96..127 y20..58: %d source pixels replaced",i,restored)) end
 im:saveAs(f(axeLOut.."/"..string.format("%02d.png",i)));axeLFrames[#axeLFrames+1]=im
end
local axeLSheet=Image(128*4,128*2,ColorMode.RGB);axeLSheet:clear()
for i=0,6 do axeLSheet:drawImage(axeLFrames[i+1],Point((i%4)*128,math.floor(i/4)*128)) end
axeLSheet:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-axe-weapon-layers-off-cleanup-preview.png"))
local axeLMaster="characters/orc-v1/source/aseprite/rear-recovery-v2/native/axe-body-only-back_l-representative.aseprite"
local al=Sprite(128,128,ColorMode.RGB);al.layers[1].name="AxeL_empty_hand_body"
for i=0,6 do if i>0 then al:newEmptyFrame() end;al:newCel(al.layers[1],i+1,axeLFrames[i+1],Point(0,0));al.frames[i+1].duration=durations[i+1] end
al:newTag(1,7).name="AxeL_body_source";al:saveAs(f(axeLMaster));al:close()
print("Aseprite-only contamination mask and weapon-layers-off body preview saved.")
