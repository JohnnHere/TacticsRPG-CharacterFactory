-- Only called in an independent --batch --noinapp process. No UI interaction.
local function readJson(file)
  local f = assert(io.open(file, "r")); local text = f:read("*a"); f:close(); return json.decode(text)
end
local function saveJson(file, value)
  local f = assert(io.open(file, "w")); f:write(json.encode(value)); f:close()
end
if app.params.template then
  local spec = readJson(app.params.template)
  local s = Sprite(spec.profile.width, spec.profile.height, ColorMode.RGB)
  s.layers[1].name = spec.layers[1]
  for i = 2, #spec.layers do s:newLayer().name = spec.layers[i] end
  for i = 2, spec.profile.frames do s:newEmptyFrame() end
  for _, frame in ipairs(s.frames) do frame.duration = spec.profile.durationMs / 1000 end
  s:saveAs(app.params.output)
end
if app.params.metadata then
  local s = assert(app.sprite, "No source sprite")
  local result = { width=s.width, height=s.height, layers={}, tags={}, slices={}, tilemaps={}, tilesets={}, frames={} }
  for ti, ts in ipairs(s.tilesets) do
    local tsid="tileset-"..ti
    local entry={id=tsid,name=ts.name,baseIndex=ts.baseIndex,tileWidth=ts.grid.tileSize.width,tileHeight=ts.grid.tileSize.height,tiles={}}
    if app.params.tilesDirectory then
      local folder=app.fs.joinPath(app.params.tilesDirectory,tsid)
      app.fs.makeAllDirectories(folder)
      for i=0,#ts-1 do
        local filename=string.format("%03d.png",i)
        ts:tile(i).image:saveAs{filename=app.fs.joinPath(folder,filename),palette=s.palettes[1]}
        table.insert(entry.tiles,{index=i,file="tilesets/"..tsid.."/"..filename,paletteFrame=0})
      end
    end
    table.insert(result.tilesets,entry)
  end
  for _, frame in ipairs(s.frames) do table.insert(result.frames, {number=frame.frameNumber, durationMs=math.floor(frame.duration*1000+0.5)}) end
  for _, tag in ipairs(s.tags) do table.insert(result.tags, {name=tag.name, from=tag.fromFrame.frameNumber-1, to=tag.toFrame.frameNumber-1, direction=tostring(tag.aniDir)}) end
  for _, slice in ipairs(s.slices) do
    local b = slice.bounds
    table.insert(result.slices, {name=slice.name, bounds={x=b.x,y=b.y,width=b.width,height=b.height}})
  end
  local function layers(list, prefix)
    for _, layer in ipairs(list) do
      local name = prefix .. layer.name
      table.insert(result.layers, {name=layer.name,path=name,visible=layer.isVisible,opacity=layer.opacity,group=layer.isGroup,tilemap=layer.isTilemap})
      if layer.isGroup then layers(layer.layers, name .. "/") end
      if layer.isTilemap then
        local ts = layer.tileset
        local tilesetId=nil
        for ti, candidate in ipairs(s.tilesets) do if candidate==ts then tilesetId="tileset-"..ti;break end end
        assert(tilesetId,"Tilemap tileset not found in document")
        for _, cel in ipairs(layer.cels) do
          local image = cel.image
          local cells = {}
          for y=0,image.height-1 do
            for x=0,image.width-1 do
              local value=image:getPixel(x,y)
              table.insert(cells,{x=x,y=y,tile=app.pixelColor.tileI(value),flags=app.pixelColor.tileF(value)})
            end
          end
          local g=ts.grid
          table.insert(result.tilemaps,{layer=name,frame=cel.frameNumber-1,x=cel.position.x,y=cel.position.y,width=image.width,height=image.height,tileWidth=g.tileSize.width,tileHeight=g.tileSize.height,tileset=ts.name,tilesetId=tilesetId,baseIndex=ts.baseIndex,cells=cells})
        end
      end
    end
  end
  layers(s.layers, "")
  saveJson(app.params.metadata,result)
end
