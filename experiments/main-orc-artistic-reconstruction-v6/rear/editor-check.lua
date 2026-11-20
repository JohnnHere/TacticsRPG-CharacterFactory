local f=assert(io.open('experiments/main-orc-artistic-reconstruction-v6/rear/editor-check.json','w'));f:write(json.encode({version=app.version,apiVersion=app.apiVersion}));f:close()
