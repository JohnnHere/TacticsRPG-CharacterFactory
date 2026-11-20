local root=app.fs.currentPath
for _,n in ipairs({"03","04","05","06"}) do local p=app.fs.joinPath(root,"experiments/main-orc-rear-recovery-v2/axe-r-cleaned-native/"..n..".png");local im=Image{fromFile=p};im:resize(768,768);im:saveAs(app.fs.joinPath(root,"experiments/main-orc-rear-recovery-v2/back_r-axe-cleaned-frame"..n.."-4x.png")) end
print("Saved cleaned raw frames 03..06 at 4x.")
