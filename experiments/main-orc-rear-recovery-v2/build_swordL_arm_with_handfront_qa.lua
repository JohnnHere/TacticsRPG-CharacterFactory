local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local base="characters/orc-v1/source/rear-recovery-v2/back_l/Sword/Attack-representative-v1/layers/"
local sheet=Image(512*2,512,ColorMode.RGB);sheet:clear()
for i=2,3 do
 local body=Image{fromFile=f(base.."body/"..string.format("%02d.png",i))}
 local hand=Image{fromFile=f(base.."handFront/"..string.format("%02d.png",i))}
 local merged=Image(256,256,ColorMode.RGB);merged:clear();merged:drawImage(body,Point(0,0));merged:drawImage(hand,Point(0,0))
 local crop=Image(80,80,ColorMode.RGB);crop:clear();crop:drawImage(merged,Point(-64,-64));crop:resize(512,512);sheet:drawImage(crop,Point((i-2)*512,0))
end
sheet:saveAs(f("experiments/main-orc-rear-recovery-v2/back_l-swordL-overhead-arm-handfront-donor-qa.png"));print("Saved body+handFront donor close-ups from accepted SwordL frames 02/03.")
