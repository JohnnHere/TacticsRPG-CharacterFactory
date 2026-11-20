from pathlib import Path
import json,re,hashlib
O=Path(__file__).resolve().relative_to(Path.cwd().resolve()).parent
jobs=[]
for label in ['sword','axe','sword-reference2','axe-reference2']:
 p=O/f'{label}-submit.json';r=json.loads(p.read_text(encoding='utf-8'))
 text='\n'.join(x.get('text','') for x in r['content'])
 req=json.loads((O/f'{label}-request.json').read_text(encoding='utf-8'))
 jobs.append({'label':label,'jobId':re.search(r'job_id: ([\w-]+)',text)[1],'costGenerationsFromReceipt':int(re.search(r'cost: (\d+) generations',text)[1]),'seed':req['seed'],'tool':'animate_with_skeleton_v3','frames':12,'receipt':p.as_posix(),'request':(O/f'{label}-request.json').as_posix(),'requestSha256':hashlib.sha256((O/f'{label}-request.json').read_bytes()).hexdigest(),'use':'unused raw foundation; local-arm attempt rejected by DEV' if 'reference2' not in label else 'selected body foundation, with documented local Aseprite finishing'})
snapshots=[]
for label in ['balance-before','balance-after','balance-reference2-before','balance-final']:
 p=O/f'{label}.json'
 if p.exists():
  r=json.loads(p.read_text(encoding='utf-8'));t='\n'.join(x.get('text','') for x in r['content'])
  snapshots.append({'receipt':p.as_posix(),'generationsRemaining':float(re.search(r'generations_remaining: ([\d.]+)',t)[1]),'creditBalanceUSD':float(re.search(r'credits: \$([\d.]+)',t)[1])})
own=sum(j['costGenerationsFromReceipt'] for j in jobs)
delta=round(snapshots[0]['generationsRemaining']-snapshots[-1]['generationsRemaining'],2)
(O/'pixellab-ledger.json').write_text(json.dumps({'jobs':jobs,'jobCount':4,'outputFrames':48,'ownGenerationsFromJobReceipts':own,'snapshots':snapshots,'observedAccountDelta':delta,'accountDeltaBeyondOwnReceipts':round(delta-own,2),'attributionNote':'Account is shared with other activity. Only these four job receipts are attributed to rear DEV; the additional observed account delta is not attributed without corresponding receipts. No token or dollar usage estimate.','purchases':False},indent=2,ensure_ascii=False),encoding='utf-8')
