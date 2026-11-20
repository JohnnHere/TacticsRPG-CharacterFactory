-- Bounded authored AxeR descending keypose. Same-individual/same-view donors.
-- Not a whole-character rotation, not a generic rig. Native coordinates.
local E='experiments/main-orc-rear-reconstruction-v4/dev'
local C='characters/orc-v1/source/rear-reconstruction-v4/keypose-axeR'
local function file(p)return app.fs.joinPath(app.fs.currentPath,p)end
local function blank(w,h)local i=Image(w,h,ColorMode.RGB);i:clear();return i end
local function poly(x,y,p)local yes=false;local j=#p;for i=1,#p do local a,b=p[i],p[j];if(a[2]>y)~=(b[2]>y)and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1]then yes=not yes end;j=i end;return yes end
local function mask(src,p)local o=blank(src.width,src.height);for y=0,src.height-1 do for x=0,src.width-1 do if poly(x+.5,y+.5,p)then o:drawPixel(x,y,src:getPixel(x,y))end end end;return o end
local function erase(im,p)for y=0,127 do for x=0,127 do if poly(x+.5,y+.5,p)then im:drawPixel(x,y,0)end end end end
local function turn(im,pivot,target,angle)
 local o=blank(128,128);local a=angle*math.pi/180;local c,s=math.cos(a),math.sin(a)
 for y=0,127 do for x=0,127 do local dx,dy=x-target[1],y-target[2];local u=math.floor(c*dx+s*dy+pivot[1]+.5);local v=math.floor(-s*dx+c*dy+pivot[2]+.5);if u>=0 and u<128 and v>=0 and v<128 then o:drawPixel(x,y,im:getPixel(u,v))end end end;return o
end
local src=app.open(file('characters/orc-v1/source/aseprite/rear-recovery-v2/native/axe-body-representative-v1-back_r.aseprite'))
local original=blank(128,128);original:drawSprite(src,5);src:close()
local base=Image(original)
-- Isolate the actual chainmail upper sleeve and steel/leather bracer/closed fist.
local upperPoly={{83,37},{88,37},{94,40},{100,44},{104,49},{100,55},{93,55},{85,49},{81,45}}
local forePoly={{99,47},{105,49},{112,52},{117,54},{120,57},{120,62},{117,65},{113,65},{106,61},{99,58},{96,53}}
local upper=mask(original,upperPoly);local fore=mask(original,forePoly)
erase(base,{{83,37},{93,37},{105,44},{118,51},{124,58},{122,68},{110,68},{99,61},{85,53},{81,46}})
-- Remove the old sleeve seam outside the reauthored arm (visible in attempt01).
erase(base,{{90,35},{93,35},{110,46},{108,49},{94,41}})
-- Forward scapular plate overlaps the sleeve; lower belt/feet remain unchanged.
-- Trace the existing plate mass, then reseat it 2px forward/2px down.
local platePoly={{51,25},{65,26},{71,30},{71,44},{73,52},{72,56},{51,56},{49,43}}
local plate=mask(original,platePoly)
local plateMoved=blank(128,128);plateMoved:drawImage(plate,Point(2,2))
-- Upper arm turns from shoulder toward elbow(94,55), bracer bends below it.
upper=turn(upper,{86,43},{86,44},28)
fore=turn(fore,{100,52},{94,55},43)
local seams=blank(128,128)
local ink=app.pixelColor.rgba(12,15,18,255);local steel=app.pixelColor.rgba(48,52,55,255)
local leather=app.pixelColor.rgba(60,30,29,255)
-- Individually traced elbow fold and cuff. No flood/distance glove mask.
for _,p in ipairs({{92,53},{93,53},{94,54},{95,54},{96,55},{96,56},{95,57},{94,57},{93,56}})do seams:drawPixel(p[1],p[2],ink)end
for _,p in ipairs({{93,54},{93,55},{94,55},{94,56},{95,56}})do seams:drawPixel(p[1],p[2],leather)end
for _,p in ipairs({{91,51},{92,51},{92,52},{93,52}})do seams:drawPixel(p[1],p[2],steel)end
local body=Image(base);body:drawImage(plateMoved);body:drawImage(upper);body:drawImage(fore);body:drawImage(seams)
app.fs.makeAllDirectories(file(C..'/source'))
local names={'preserved-body','forward-scapular-plate','upper-arm','bracer-and-fist','elbow-fold'}
local ims={base,plateMoved,upper,fore,seams}
local s=Sprite(128,128,ColorMode.RGB)
for i,n in ipairs(names)do local l=i==1 and s.layers[1]or s:newLayer();l.name=n;s:newCel(l,1,ims[i],Point(0,0))end
s:saveAs(file(C..'/source/descending-study.aseprite'));s:close()
local saved=app.open(file(C..'/source/descending-study.aseprite'));local out=blank(128,128);out:drawSprite(saved,1);out:saveAs(file(C..'/descending-study.png'));saved:close()
original:saveAs(file(C..'/source-F04.png'))
-- Equipment study uses the unchanged grip/category/size of the independent fork.
local item=Image{fromFile=file('characters/orc-v1/source/rear-reconstruction-v4/weapons/Axe/militia-axe.png')}
local weapon=blank(256,256);local rad=145*math.pi/180;local c,si=math.cos(rad),math.sin(rad)
for y=0,255 do for x=0,255 do
 local dx,dy=x-166,y-133;local u=math.floor(c*dx+si*dy+36+.5);local v=math.floor(-si*dx+c*dy+55+.5)
 if u>=0 and u<96 and v>=0 and v<96 then weapon:drawPixel(x,y,item:getPixel(u,v))end
end end
local body256=blank(256,256);body256:drawImage(out,Point(64,64))
local hand=blank(256,256)
local gloveMid=app.pixelColor.rgba(63,40,31,255);local gloveLight=app.pixelColor.rgba(86,61,43,255)
for _,p in ipairs({{165,131},{166,131},{167,132},{164,133},{165,134},{166,135},{167,135}})do hand:drawPixel(p[1],p[2],gloveMid)end
for _,p in ipairs({{166,132},{165,133},{166,134}})do hand:drawPixel(p[1],p[2],gloveLight)end
local comp=Sprite(256,256,ColorMode.RGB)
for i,v in ipairs({{'weaponBack',blank(256,256)},{'body',body256},{'weaponFront',weapon},{'handFront',hand}})do
 local l=i==1 and comp.layers[1]or comp:newLayer();l.name=v[1];comp:newCel(l,1,v[2],Point(0,0))
end
comp:saveAs(file(C..'/source/equipped-descending-study.aseprite'));comp:close()
local reopened=app.open(file(C..'/source/equipped-descending-study.aseprite'));local flat=blank(256,256);flat:drawSprite(reopened,1);flat:saveAs(file(C..'/equipped-descending-study.png'));reopened:close()
print('Representative body keypose saved; awaiting local visual inspection before propagation.')
