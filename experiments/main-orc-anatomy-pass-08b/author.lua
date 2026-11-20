local E='experiments/main-orc-anatomy-pass-08b/'
local src=Image{fromFile='experiments/main-orc-skeleton-02/stage-bcde/body-only/08.png'}
local sp=Sprite(256,256,ColorMode.RGB)
local im=Image(src)
local pc=app.pixelColor
-- All colors selected from the source palette, never synthesized.
local function col(r,g,b)
 local best,dist=nil,1e9
 for y=0,255 do for x=0,255 do local p=src:getPixel(x,y)
 if pc.rgbaA(p)==255 then local d=(pc.rgbaR(p)-r)^2+(pc.rgbaG(p)-g)^2+(pc.rgbaB(p)-b)^2
 if d<dist then best,dist=p,d end end end end
 return best
end
local ink=col(2,2,3);local dark=col(20,20,26);local metal=col(33,34,40)
local grey=col(49,51,55);local light=col(86,88,92);local mid=col(58,60,64)
local red=col(51,19,28);local rshadow=col(36,14,23);local rlight=col(72,33,38);local leather=col(38,27,27)
local function poly(v,c)
 for y=111,153 do for x=147,190 do
 local inside=false;local j=#v
 for i=1,#v do local a,b=v[i],v[j]
 if ((a[2]>y)~=(b[2]>y)) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then inside=not inside end;j=i end
 if inside then im:drawPixel(x,y,c) end end end
end
-- Erase only the old free limb below the preserved shoulder plate.
for y=111,138 do for x=147,188 do im:drawPixel(x,y,0) end end
-- Newly drawn continuous silhouette: sleeve, bent elbow, tapered vambrace and fist.
poly({{147,111},{155,111},{160,115},{164,119},{167,123},{171,127},{174,132},{177,136},{180,139},{181,145},{178,150},{173,152},{168,150},{165,146},{164,140},{160,136},{157,132},{153,128},{150,122},{147,119}},ink)
poly({{148,112},{154,112},{158,116},{162,119},{165,124},{164,130},{160,133},{156,129},{153,124},{150,120}},rshadow)
poly({{150,113},{154,114},{160,120},{163,124},{161,128},{158,126},{154,120}},red)
poly({{150,113},{153,114},{155,117},{153,118},{150,116}},rlight)
-- Chain sleeve: discrete clustered links with shared shadow mass, no transformed donor.
poly({{155,118},{160,120},{164,125},{163,130},{160,132},{156,127},{153,122}},metal)
for _,p in ipairs({{155,119},{158,121},{161,123},{156,123},{159,125},{162,127},{157,126},{160,129}}) do
 im:drawPixel(p[1],p[2],mid);im:drawPixel(p[1]+1,p[2]+1,grey)
end
-- Broad overlapping elbow plate, flowing into the forearm rather than a thin connector.
poly({{162,124},{166,125},{171,130},{174,136},{172,141},{167,142},{162,136},{159,131}},dark)
poly({{163,125},{166,127},{171,132},{173,136},{170,139},{166,137},{162,132}},metal)
poly({{163,126},{165,128},{167,133},{170,136},{169,138},{166,136},{163,132}},grey)
poly({{163,126},{164,127},{165,130},{164,131},{162,128}},light)
-- Vambrace: lit outer ridge, shaded underside and uninterrupted cuff.
poly({{169,132},{172,134},{176,139},{176,144},{172,146},{167,143},{165,138}},leather)
poly({{170,132},{173,135},{177,139},{178,143},{175,146},{171,144},{168,140}},metal)
poly({{170,134},{172,135},{174,139},{175,143},{173,143},{171,140}},mid)
poly({{170,134},{171,135},{172,138},{171,139},{169,136}},light)
poly({{167,141},{170,143},{175,145},{178,143},{178,146},{175,148},{170,146},{167,145}},grey)
-- Closed fist: grouped knuckles, curled fingers and thumb with a dark palm crease.
poly({{168,146},{171,147},{176,148},{179,145},{178,149},{174,151},{170,149}},rshadow)
poly({{168,145},{170,145},{172,148},{171,150},{169,149}},leather)
poly({{173,148},{176,148},{177,147},{177,149},{174,150}},red)
im:drawPixel(171,147,rlight);im:drawPixel(172,148,ink);im:drawPixel(175,149,leather)
sp:newCel(sp.layers[1],1,im,Point(0,0));sp.layers[1].name='body - redrawn right arm clusters'
sp:saveAs(E..'master-08b.aseprite');im:saveAs(E..'candidate-08b.png');sp:close()
local reopened=app.open(E..'master-08b.aseprite')
reopened.cels[1].image:saveAs(E..'master-roundtrip.png');reopened:close()
