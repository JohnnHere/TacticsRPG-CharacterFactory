import json,re,urllib.request,importlib.util,argparse
from pathlib import Path
root=Path(__file__).resolve().parents[1];exp=root/'experiments/pixellab-orc-refinement-v5';sp=importlib.util.spec_from_file_location('m',root/'tools/pixellab-mcp.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
p=argparse.ArgumentParser();p.add_argument('--download',action='store_true');a=p.parse_args();rpc,_=m.connect()
for submission in sorted(exp.glob('*-submission.json')):
 name=submission.name.removesuffix('-submission.json');text='\n'.join(c.get('text','') for c in json.loads(submission.read_text(encoding='utf-8')).get('content',[]));match=re.search(r'^job_id: ([\w-]+)',text,re.M)
 if not match:print(name,text[:400]);continue
 r=rpc('tools/call',{'name':'get_image','arguments':{'job_id':match[1]}});(exp/f'{name}-result.json').write_text(json.dumps(r),encoding='utf-8');text='\n'.join(c.get('text','') for c in r.get('content',[]));print(name,text[:750],flush=True)
 if a.download and 'status: completed' in text:
  count=int(re.search(r'^frames: (\d+)',text,re.M).group(1));d=exp/name/'raw';d.mkdir(parents=True,exist_ok=True)
  for i in range(count):
   dest=d/f'{i}.png'
   if dest.exists():continue
   with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{match[1]}/download?index={i}',timeout=60) as response:raw=response.read()
   if not raw.startswith(b'\x89PNG'):raise ValueError('Not PNG')
   dest.write_bytes(raw)
