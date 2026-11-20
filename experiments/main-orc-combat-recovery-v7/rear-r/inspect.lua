local root=app.fs.currentPath
local function abs(p)return app.fs.joinPath(root,p)end
for _,k in ipairs({'axe','sword'}) do
 for _,i in ipairs({2,3,4,6,7,8}) do
 local im=Image{fromFile=abs('characters/orc-v1/source/artistic-reconstruction-v6/rear/back_r-'..k..'/frames/'..string.format('%02d',i)..'.png')}
 im:resize(1024,1024)
 im:saveAs(abs('experiments/main-orc-combat-recovery-v7/rear-r/before-'..k..'-'..i..'.png'))
 end
end
