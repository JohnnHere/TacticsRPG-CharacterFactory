local root=app.fs.currentPath
for _,k in ipairs({'sword','axe'})do for _,i in ipairs({2,3,4,7})do
local im=Image{fromFile=app.fs.joinPath(root,'characters/orc-v1/source/artistic-reconstruction-v6/rear/back_l-'..k..'/layers/body/'..string.format('%02d',i)..'.png')};local crop=Image(128,128,ColorMode.RGB);crop:clear();crop:drawImage(im,Point(-64,-64));crop:resize(768,768);crop:saveAs(app.fs.joinPath(root,'experiments/main-orc-combat-recovery-v7/rear-alt/inspect-'..k..'-'..i..'.png'))
end end
