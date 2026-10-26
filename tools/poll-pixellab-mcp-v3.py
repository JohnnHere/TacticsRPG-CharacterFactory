import json,re,sys
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
root=Path(__file__).resolve().parents[1];spec=spec_from_file_location('mcp',root/'tools/pixellab-mcp.py');m=module_from_spec(spec);spec.loader.exec_module(m)
rpc,_=m.connect();folder=root/'experiments/pixellab-orc-refinement-v3/mcp'
for submission in sorted(folder.glob('*-submission.json')):
    name=submission.name.removesuffix('-submission.json');resultfile=folder/(name+'-result.json')
    text='\n'.join(c.get('text','') for c in json.loads(submission.read_text())['content']);match=re.search(r'^job_id: ([\w-]+)',text,re.M)
    if not match:print(name,'SUBMISSION_ERROR');continue
    result=rpc('tools/call',{'name':'get_image','arguments':{'job_id':match[1]}})
    resultfile.write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8')
    texts='\n'.join(c.get('text','') for c in result.get('content',[]))
    print(name,texts[:1600])
