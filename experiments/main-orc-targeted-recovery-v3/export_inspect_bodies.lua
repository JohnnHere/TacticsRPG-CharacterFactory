local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

local outDir = file("experiments/main-orc-targeted-recovery-v3/inspect_bodies")
app.fs.makeAllDirectories(outDir)

local sets = {
  { key = "AxeR", src = "experiments/main-orc-rear-recovery-v2/qa-revision-1-repair/checkpoint/source/AxeR-body-256.aseprite" },
  { key = "SwordL", src = "experiments/main-orc-rear-recovery-v2/qa-revision-1-repair/checkpoint/source/SwordL-body-256.aseprite" },
  { key = "AxeL", src = "experiments/main-orc-rear-recovery-v2/qa-revision-1-repair/checkpoint/source/AxeL-body-256.aseprite" }
}

for _, s in ipairs(sets) do
  local spr = app.open(file(s.src))
  for i = 1, #spr.frames do
    local img = Image(256, 256, ColorMode.RGB)
    img:clear()
    img:drawSprite(spr, i)
    img:saveAs(app.fs.joinPath(outDir, string.format("%s_%02d.png", s.key, i - 1)))
  end
  spr:close()
  print("Exported inspection frames for " .. s.key)
end
