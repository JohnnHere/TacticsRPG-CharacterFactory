-- QA revision 1: bounded body-only edits authored and saved in Aseprite.
local root=app.fs.currentPath
local function f(p)return app.fs.joinPath(root,p)end
local function alpha(p)return app.pixelColor.rgbaA(p)end
local function inside(x,y,poly)
 local c=false;local j=#poly
 for i=1,#poly do local xi,yi=poly[i][1],poly[i][2];local xj,yj=poly[j][1],poly[j][2]
  if ((yi>y)~=(yj>y)) and (x<(xj-xi)*(y-yi)/(yj-yi)+xi) then c=not c end;j=i
 end;return c
end
local function load(p)return Image{fromFile=f(p)}end
local function blank(w,h)local im=Image(w,h,ColorMode.RGB);im:clear();return im end
local function frames(dir,n)local a={};for i=0,n-1 do a[i+1]=load(dir.."/"..string.format("%02d.png",i)) end;return a end
local function base256(img)
 assert((img.width==128 and img.height==128) or (img.width==256 and img.height==256),"same-view donor must be 128 or 256 square")
 if img.width==256 then return img end
 local b=blank(256,256);b:drawImage(img,Point(64,64));return b
end
local function patch(dst,src,poly)
 local n=0;for y=0,255 do for x=0,255 do if inside(x,y,poly) then local p=src:getPixel(x,y);if p~=dst:getPixel(x,y) then n=n+1 end;dst:drawPixel(x,y,p) end end end;return n
end
local function saveMaster(path,fr,dur,dim)
 app.fs.makeAllDirectories(app.fs.filePath(f(path)));local s=Sprite(dim,dim,ColorMode.RGB);local l=s.layers[1];l.name="body"
 for i=1,#fr do if i>1 then s:newEmptyFrame() end;local im=fr[i];if dim==128 then local n=blank(128,128);n:drawImage(im,Point(-64,-64));im=n end;s:newCel(l,i,im,Point(0,0));s.frames[i].duration=dur[i]/1000 end
 s:newTag(1,#fr).name="Attack";s:saveAs(f(path));s:close();print("Aseprite saved "..path.." frames="..#fr)
end
local out="experiments/main-orc-rear-recovery-v2/E/qa-revision-1/body-checkpoint/source";app.fs.makeAllDirectories(f(out))
local dur={90,80,90,80,100,80,100,110}
-- QA-01 SwordL: same-view approved static pixels restore the non-striking gauntlet; F05 shoulder contour restored locally.
local sl=frames("characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/body",8)
local baseL=base256(load("characters/orc-v1/source/complete-v1/back_l/Idle/00.png"))
local hanging={{146,119},{150,115},{156,116},{162,121},{164,128},{162,135},{165,141},{161,147},{155,150},{150,146},{147,140},{145,132}}
for i=2,8 do print(string.format("QA-01 SwordL F%02d hand-mask changed=%d",i-1,patch(sl[i],baseL,hanging))) end
local shoulder={{151,82},{158,81},{164,85},{171,91},{176,97},{172,102},{166,99},{160,95},{155,90},{151,87}}
print("QA-01 SwordL F05 shoulder-mask changed="..patch(sl[6],baseL,shoulder))
saveMaster(out.."/back_l-sword-body-revision-1.aseprite",sl,dur,256);saveMaster(out.."/back_l-sword-native-body-revision-1.aseprite",sl,dur,128)
-- QA-02/03 AxeR: clear body weapon remnants, then reuse a same-view accepted connected SwordR arm only inside the distal limb mask.
local ar=frames("characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1/layers/body",8)
local baseR=base256(load("characters/orc-v1/source/complete-v1/back_r/Idle/00.png"))
local crescent={{164,77},{171,75},{178,78},{183,83},{186,91},{184,98},{180,101},{176,96},{173,91},{168,87}}
print("QA-02 AxeR F01 outer-head mask changed="..patch(ar[2],baseR,crescent))
local shaft2={{151,48},{156,45},{163,52},{169,60},{170,67},{166,72},{161,68},{157,61},{153,55}}
local shaft3={{159,42},{164,40},{170,48},{176,57},{176,65},{172,70},{167,65},{163,57}}
print("QA-02 AxeR F02 brown shaft mask changed="..patch(ar[3],baseR,shaft2))
print("QA-02 AxeR F03 brown shaft mask changed="..patch(ar[4],baseR,shaft3))
local swordR=frames("characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/layers/body",8)
local swordHand=frames("characters/orc-v1/source/rear-recovery-v2/back_r/Sword/Attack-representative-v2/layers/handFront",8)
local donorArm=blank(256,256);donorArm:drawImage(swordR[6],Point(0,0));donorArm:drawImage(swordHand[6],Point(0,0))
local armMask={{148,98},{153,94},{162,96},{169,101},{177,104},{185,108},{193,114},{194,122},{190,130},{184,136},{176,130},{169,122},{160,116},{153,110},{149,105}}
print("QA-03 AxeR F04 connected donor arm+closed-hand changed="..patch(ar[5],donorArm,armMask))
local moved=0
for y=90,137 do for x=148,194 do if inside(x,y,armMask) then ar[6]:drawPixel(x,y,app.pixelColor.rgba(0,0,0,0)) end end end
for y=90,137 do for x=148,194 do if inside(x,y,armMask) then local p=donorArm:getPixel(x+8,y-2);if alpha(p)>0 then if p~=ar[6]:getPixel(x,y) then moved=moved+1 end;ar[6]:drawPixel(x,y,p) end end end end
print("QA-03 AxeR F05 cleared old arm within connected silhouette, then reused SwordR F05 adapted -8,+2; donor pixels="..moved)
saveMaster(out.."/back_r-axe-body-revision-1.aseprite",ar,dur,256);saveMaster(out.."/back_r-axe-native-body-revision-1.aseprite",ar,dur,128)
-- QA-04 AxeL: restore only the narrow light strand above the far pauldron; preserve existing 27px cleanup and fist donor.
local al=frames("characters/orc-v1/source/rear-recovery-v2/back_l/Axe/Attack-representative-v1/layers/body",8)
local hook={{154,75},{160,73},{167,75},{174,78},{174,82},{168,84},{161,81},{156,79}}
print("QA-04 AxeL F02 hook changed="..patch(al[3],baseL,hook));print("QA-04 AxeL F03 hook changed="..patch(al[4],baseL,hook))
saveMaster(out.."/back_l-axe-body-revision-1.aseprite",al,dur,256);saveMaster(out.."/back_l-axe-native-body-revision-1.aseprite",al,dur,128)
print("Body-only checkpoint saved. No weapon layers were loaded or composed.")
