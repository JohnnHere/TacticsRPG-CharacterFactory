local root=assert(app.params.root);local function file(p)return app.fs.joinPath(root,p)end
local f=assert(io.open(file('experiments/orc-v1-weapons-v1/composition-plan.json'),'r'));local p=json.decode(f:read('*a'));f:close()
for _,job in ipairs(p.jobs)do
 local s=app.open(file(job.master));local strip=Image(256*#s.frames,256,ColorMode.RGB);strip:clear()
 for i=1,#s.frames do strip:drawSprite(s,i,Point((i-1)*256,0))end
 strip:saveAs(file(job.output..'/native-strip.png'));s:close()
end
