"""Use the official PixelLab MCP over HTTP; credentials stay in user Codex config.

This is an MCP client, not a substitute REST generation API. Saves full results
locally; stdout contains only a small status summary, never credentials/images.
"""
import argparse, json, os, tomllib, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def connect():
    config=Path(os.environ.get('CODEX_HOME',Path.home()/'.codex'))/'config.toml'
    settings=tomllib.loads(config.read_text(encoding='utf-8'))['mcp_servers']['pixellab']
    if settings.get('url')!='https://api.pixellab.ai/mcp':
        raise ValueError('Expected official PixelLab MCP endpoint')
    headers=dict(settings.get('http_headers',{}))
    if settings.get('bearer_token_env_var'):
        headers['Authorization']='Bearer '+os.environ[settings['bearer_token_env_var']]
    headers.update({'Content-Type':'application/json','Accept':'application/json, text/event-stream'})
    session=None
    def rpc(method,params=None,request_id=1):
        nonlocal session
        payload={'jsonrpc':'2.0','method':method}
        if params is not None:payload['params']=params
        if request_id is not None:payload['id']=request_id
        h=dict(headers)
        if session:h['Mcp-Session-Id']=session
        req=urllib.request.Request(settings['url'],data=json.dumps(payload).encode(),headers=h,method='POST')
        with urllib.request.urlopen(req,timeout=180) as response:
            session=response.headers.get('Mcp-Session-Id',session)
            body=response.read().decode('utf-8')
        if not body.strip():return {}
        messages=[json.loads(line[6:]) for line in body.splitlines() if line.startswith('data: ')] if body.lstrip().startswith(('event:','data:')) else [json.loads(body)]
        message=next((m for m in messages if m.get('id')==request_id),messages[-1])
        if 'error' in message:raise RuntimeError(json.dumps(message['error']))
        return message.get('result',{})
    initialized=rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'TacticsRPG-CharacterFactory','version':'0.1'}})
    rpc('notifications/initialized',request_id=None)
    return rpc,initialized

def main():
    p=argparse.ArgumentParser();p.add_argument('--list',action='store_true');p.add_argument('--call');p.add_argument('--input',type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    rpc,initialized=connect()
    if a.list:
        result=rpc('tools/list');summary={'server':initialized.get('serverInfo'),'tools':[t['name'] for t in result.get('tools',[])]}
    elif a.call:
        args=json.loads(a.input.read_text(encoding='utf-8-sig')) if a.input else {}
        result=rpc('tools/call',{'name':a.call,'arguments':args});summary={'tool':a.call,'isError':result.get('isError',False),'saved':str(a.output)}
    else:p.error('Choose --list or --call')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
