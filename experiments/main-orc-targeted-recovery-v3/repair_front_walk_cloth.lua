-- Repair front Walk cloth shading between legs in Aseprite
local root = app.fs.currentPath
local function file(p) return app.fs.joinPath(root, p) end

print("=== Repairing front Walk cloth shading between legs in Aseprite ===")

local CLOTH_SHADOW = app.pixelColor.rgba(48, 50, 54, 255)
local CLOTH_MID = app.pixelColor.rgba(72, 74, 78, 255)

for _, d in ipairs({ "front_r", "front_l" }) do
  local natMaster = file(string.format("characters/orc-v1/source/aseprite/complete-v1/native/walk-%s.aseprite", d))
  local compMaster = file(string.format("characters/orc-v1/source/aseprite/complete-v1/composite/%s/walk-unarmed.aseprite", d))
  local clipDir = file(string.format("characters/orc-v1/source/complete-v1/%s/Walk", d))
  
  if app.fs.isFile(compMaster) and app.fs.isFile(natMaster) then
    local compSprite = Sprite{ fromFile = compMaster }
    local natSprite = Sprite{ fromFile = natMaster }
    
    -- Frame 8 is cel index 9 in Aseprite (1-based)
    local celComp = compSprite.layers[1]:cel(9)
    local celNat = natSprite.layers[1]:cel(9)
    
    if celComp and celNat then
      -- Coordinates in 256 composite canvas:
      local coords256 = {
        {119, 133}, {120, 139}, {125, 142}, {124, 143}
      }
      for _, pt in ipairs(coords256) do
        local x, y = pt[1], pt[2]
        if d == "front_l" then
          -- mirror x around 128: 128 - (x - 128) = 256 - x
          x = 256 - x
        end
        celComp.image:drawPixel(x, y, CLOTH_MID)
        -- In 128 native canvas:
        local nx, ny = x - 64, y - 64
        if nx >= 0 and nx < 128 and ny >= 0 and ny < 128 then
          celNat.image:drawPixel(nx, ny, CLOTH_MID)
        end
      end
    end
    
    compSprite:saveAs(compMaster)
    natSprite:saveAs(natMaster)
    
    -- Re-export Frame 08 composite
    if celComp then
      celComp.image:saveAs(app.fs.joinPath(clipDir, "08.png"))
    end
    
    compSprite:close()
    natSprite:close()
    print("Repaired " .. d .. " Walk frame 08 cloth shading.")
  end
end
