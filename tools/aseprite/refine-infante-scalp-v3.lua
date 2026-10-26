-- Specific hand-authored pixel retouch: remove topknot and redraw bald crown.
-- No torso/face/armor deformation. Output is a new candidate, not an approval.
local s=app.open(assert(app.params.input));local im=s.cels[1].image
local colors={['#']=app.pixelColor.rgba(2,2,3,255),o=app.pixelColor.rgba(49,50,54,255),x=app.pixelColor.rgba(83,85,88,255),['+']=app.pixelColor.rgba(134,134,135,255),['@']=app.pixelColor.rgba(141,142,143,255)}
for y=0,11 do for x=52,79 do im:drawPixel(x,y,0) end end
local rows={
 {6,64,'#xxxx#'},
 {7,62,'#x+++++xx#'},
 {8,61,'#x++@@@+++xx#'},
 {9,61,'#x+@@@@++++xx#'},
 {10,61,'#x++x++++++x+x#'},
 {11,61,'#x++xx++++@++++x#'},
}
for _,r in ipairs(rows) do for i=1,#r[3] do im:drawPixel(r[2]+i-1,r[1],colors[r[3]:sub(i,i)]) end end
s.layers[1].name='PixelLab Infante + Aseprite bald crown retouch v3'
s:saveAs(assert(app.params.master));app.command.SaveFileAs{filename=assert(app.params.png)};s:close()
