-- Programmatic local rearticulation in Aseprite; no generation, donor or external raster authoring.
local E='experiments/main-orc-anatomy-pass-08/'
local input='experiments/main-orc-skeleton-02/stage-bcde/body-only/08.png'
local src=Image{fromFile=input}
local sp=Sprite(256,256,ColorMode.RGB)
sp:newCel(sp.layers[1],1,src,Point(0,0))
local out=Image(src)
local pc=app.pixelColor
local function arm(x,y) return x>=147 and x<=188 and y>=111 and y<=138 end
for y=111,138 do for x=147,188 do out:drawPixel(x,y,0) end end
-- Two separate local joint rotations, nearest integer samples, no scaling.
-- Upper arm retains original length; forearm is rigidly articulated at elbow.
local function part(ox,oy,nx,ny,angle,kind)
 local c,s=math.cos(angle),math.sin(angle)
 for y=109,149 do for x=145,190 do
  local dx,dy=x-nx,y-ny
  local u=math.floor(ox+c*dx+s*dy+.5)
  local v=math.floor(oy-s*dx+c*dy+.5)
  local valid=arm(u,v) and ((kind==1 and u<=168) or (kind==2 and u>=167))
  if valid then local p=src:getPixel(u,v);if pc.rgbaA(p)>0 then out:drawPixel(x,y,p) end end
 end end
end
part(147,112,147,112,math.atan(12,19)-math.atan(8,21),1)
part(168,120,166,124,math.atan(12,7)-math.atan(5,13),2)
-- Only indispensable underside junction: restore its original palette/contour pixels.
-- The shoulder plate above y111 and torso left of x147 remain untouched.
for y=0,255 do for x=0,255 do if x<147 or y<111 then out:drawPixel(x,y,src:getPixel(x,y)) end end end
sp.cels[1].image=out
sp.layers[1].name='body - local right arm articulation'
sp:saveAs(E..'master-08.aseprite')
out:saveAs(E..'candidate-08.png')
sp:close()



