import json,re,urllib.request
from pathlib import Path
root=Path(__file__).resolve().parents[1];folder=root/'experiments/pixellab-orc-refinement-v3/mcp'
for resultfile in sorted(folder.glob('*-result.json')):
    name=resultfile.name.removesuffix('-result.json');r=json.loads(resultfile.read_text());text='\n'.join(c.get('text','') for c in r.get('content',[]))
    if 'status: completed' not in text:continue
    job=re.search(r'^job_id: ([\w-]+)',text,re.M).group(1);count=int(re.search(r'^frames: (\d+)',text,re.M).group(1))
    if not re.search(r'https://api\.pixellab\.ai/mcp/images/'+re.escape(job)+'/download',text):raise ValueError('Missing official download URL')
    target=folder/name/'raw';target.mkdir(parents=True,exist_ok=True)
    for i in range(count):
        dest=target/f'{i}.png'
        if dest.exists():continue
        with urllib.request.urlopen(f'https://api.pixellab.ai/mcp/images/{job}/download?index={i}',timeout=60) as response:data=response.read()
        if not data.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Not a PNG')
        dest.write_bytes(data)
    print(name,count,'downloaded')
