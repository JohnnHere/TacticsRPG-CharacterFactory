local base='experiments/main-orc-rear-reconstruction-v4/specialist'
local function file(p)return app.fs.joinPath(app.fs.currentPath,p)end
assert(app.params.params==base..'/recovery/params-frozen.lua')
local paramsChunk=assert(loadfile(file(app.params.params)))
local p=paramsChunk()
assert(p.name=='impact-recovered')
assert(p.outDir=='characters/orc-v1/source/rear-reconstruction-v4-specialist/impact-recovered')
assert(p.armFrom=='F05' and p.armK==-.45 and p.headDrop==3 and p.pauldronDrop==2)
assert(p.grip[1]==108 and p.grip[2]==66 and p.axeDeg==135)
assert(app.fs.isFile(file('characters/orc-v1/source/aseprite/rear-recovery-v2/native/axe-body-representative-v1-back_r.aseprite')))
assert(app.fs.isFile(file('assets/weapons/militia-axe/sprites/rescue-v3/militia-axe.png')))
local authorChunk=assert(loadfile(file(base..'/author-impact.lua')))
print('Prepared Lua syntax and bounded input/output checks passed; '..tostring(app.version))
authorChunk()
