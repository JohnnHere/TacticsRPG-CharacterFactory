-- Aseprite-only REUSE_ADAPTED: same-view accepted SwordL F02 forearm/closed
-- gauntlet adapted to AxeL frames 01/02. The AxeL torso and all other pixels
-- remain from the generated+cleaned AxeL body; raw files stay immutable.
local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local function alpha(p)return app.pixelColor.rgbaA(p)end
local function inside(x,y,poly)
 local c=false;local j=#poly
 for i=1,#poly do local xi,yi=poly[i][1],poly[i][2];local xj,yj=poly[j][1],poly[j][2]
  if ((yi>y)~=(yj>y)) and (x<(xj-xi)*(y-yi)/(yj-yi)+xi) then c=not c end;j=i
 end
 return c
end
local bodyPath="characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/body/02.png"
local handPath="characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/handFront/02.png"
local body256=Image{fromFile=f(bodyPath)};local hand256=Image{fromFile=f(handPath)}
local donor=Image(128,128,ColorMode.RGB);donor:clear();donor:drawImage(body256,Point(-64,-64));donor:drawImage(hand256,Point(-64,-64))
-- Silhouette polygon follows the raised arm and closed gauntlet, ending at
-- the arm/shoulder seam. It excludes the head, torso, and neighboring armor.
local donorMask={{28,28},{29,23},{33,19},{34,14},{31,9},{31,4},{34,0},{42,0},{46,5},{47,10},{45,15},{43,19},{43,24},{41,29},{39,34},{34,35},{30,33}}
-- Remove only the clipped AxeL arm silhouette, restoring its underlying
-- same-view base pixels so the donor arm can attach cleanly.
local targetMask={{10,0},{43,0},{48,7},{47,14},{44,21},{42,28},{39,34},{33,37},{27,34},{23,29},{19,23},{15,18},{11,12}}
local base=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/inputs/back_l-sword-native128.png")}
local out="experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native"
app.fs.makeAllDirectories(f(out))
for idx=0,6 do
 local im=Image{fromFile=f("experiments/main-orc-rear-recovery-v2/back_l-axe-cleaned-native/"..string.format("%02d.png",idx))}
 local cleared,placed=0,0
 if idx==1 or idx==2 then
  for y=0,39 do for x=8,50 do if inside(x,y,targetMask) then
   im:drawPixel(x,y,base:getPixel(x,y));cleared=cleared+1
  end end end
  -- Restore the head/back-of-skull area to the NW base before adding the
  -- attacking arm, removing any generated shaft pixels passing behind it.
  local headShaft=0
  for y=0,23 do for x=47,85 do
   if im:getPixel(x,y)~=base:getPixel(x,y) then headShaft=headShaft+1 end
   im:drawPixel(x,y,base:getPixel(x,y))
  end end
  -- Lower the borrowed arm by 8 native pixels so the complete fist clears
  -- the canvas edge. Copy only pixels within the closed arm silhouette.
  -- Exclude brown, disconnected-looking line pixels from the source's upper
  -- edge; preserve the steel gauntlet and forearm clusters.
  for y=0,35 do for x=25,49 do if inside(x,y,donorMask) then
   local p=donor:getPixel(x,y);local r,g,b=app.pixelColor.rgbaR(p),app.pixelColor.rgbaG(p),app.pixelColor.rgbaB(p)
   local brownLine=x>=35 and y<=8 and r>g*1.04 and g>b*1.04 and r>45
   if alpha(p)>0 and not brownLine and y+8<128 then im:drawPixel(x,y+8,p);placed=placed+1 end
  end end end
  -- Root identified an unconnected generated-axe wood shaft over/behind the
  -- head in raw frames 01/02. Remove only brown shaft-colored pixels in its
  -- bounded diagonal region, replacing each with the corresponding approved
  -- NW base pixel. Green head, black outline, pauldron and new raised arm stay.
  local shaft=0
  for y=0,23 do for x=35,85 do
   local p=im:getPixel(x,y);local r,g,b=app.pixelColor.rgbaR(p),app.pixelColor.rgbaG(p),app.pixelColor.rgbaB(p)
   if alpha(p)>0 and r>g*1.12 and g>b*1.08 and r>65 then im:drawPixel(x,y,base:getPixel(x,y));shaft=shaft+1 end
  end end
  print(string.format("AxeL frame %02d shaft cleanup: restored %d head/shaft source pixels; removed %d residual brown shaft-colored pixels in ROI x35..85 y0..23",idx,headShaft,shaft))
  if idx==2 then
   -- Root-confirmed old clipped-arm remnant: this exact detached 8-connected
   -- component was absent from the approved base at all 27 coordinates.
   -- Remove only this confirmed residue; do not apply a size filter.
   local pts={{18,22},{18,23},{18,24},{19,24},{19,25},{20,25},{19,26},{20,26},{20,27},{21,27},{20,28},{21,28},{22,28},{21,29},{22,29},{21,30},{22,30},{23,30},{22,31},{23,31},{24,31},{24,32},{25,32},{25,33},{26,33},{26,34},{28,35}}
   local removed=0
   for _,p in ipairs(pts)do assert(alpha(base:getPixel(p[1],p[2]))==0,"reported residue overlaps approved NW base");if alpha(im:getPixel(p[1],p[2]))>0 then im:drawPixel(p[1],p[2],app.pixelColor.rgba(0,0,0,0));removed=removed+1 end end
   print(string.format("AxeL frame 02 removed Root-confirmed detached old-arm residue at exact bbox x18..26 y22..34 plus (28,35): %d pixels; all 27 locations transparent in approved base",removed))
  end
 end
 local state=(idx==1 or idx==2) and "repaired" or "unchanged"
 print(string.format("AxeL frame %02d arm repair: restored %d base-mask pixels; reused %d donor pixels at +8y from SwordL Attack v1 F02 (%s)",idx,cleared,placed,state))
 im:saveAs(f(out.."/"..string.format("%02d.png",idx)))
end
local strip=Image(128*4,128*2,ColorMode.RGB);strip:clear()
for idx=0,6 do local im=Image{fromFile=f(out.."/"..string.format("%02d.png",idx))};strip:drawImage(im,Point((idx%4)*128,math.floor(idx/4)*128)) end
strip:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-axe-repaired-native-sheet-qa.png"))
print("Saved local AxeL arm repair and complete seven-pose native body sheet; verify the joint and closed-fist silhouette visually.")
