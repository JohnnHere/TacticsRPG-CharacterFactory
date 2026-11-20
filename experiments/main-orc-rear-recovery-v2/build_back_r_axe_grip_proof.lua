local root=app.fs.currentPath;local function f(p)return app.fs.joinPath(root,p)end
local out="characters/orc-v1/source/rear-recovery-v2/back_r/Axe/Attack-representative-v1"
local grips={{167,98},{167,73},{167,78},{173,116},{159,121},{156,139}}
local all=Image(192*3,192*2,ColorMode.RGB);all:clear()
local bodyOnly=Image(192*3,192*2,ColorMode.RGB);bodyOnly:clear()
for i=1,6 do
 local ix=i+1;local comp=Image{fromFile=f(out.."/"..string.format("%02d.png",ix-1))}
 local body=Image{fromFile=f(out.."/layers/body/"..string.format("%02d.png",ix-1))}
 local rect=Rectangle(grips[i][1]-24,grips[i][2]-24,48,48)
 local c=Image(48,48,ColorMode.RGB);c:clear();c:drawImage(comp,Point(-rect.x,-rect.y));c:resize(192,192);all:drawImage(c,Point(((i-1)%3)*192,math.floor((i-1)/3)*192))
 local b=Image(48,48,ColorMode.RGB);b:clear();b:drawImage(body,Point(-rect.x,-rect.y));b:resize(192,192);bodyOnly:drawImage(b,Point(((i-1)%3)*192,math.floor((i-1)/3)*192))
end
all:saveAs(f("experiments/main-orc-rear-recovery-v2/back_r-axe-grip-closeups-qa.png"));bodyOnly:saveAs(f("experiments/main-orc-rear-recovery-v2/back_r-axe-grip-body-only-qa.png"))
print("Saved actual AxeR composite grip closeups and corresponding weapon-layers-off body crops.")
