"""Retarget cached Agile joint angles to Athletic anatomy; metadata only."""
from pathlib import Path
import json,math,statistics
root=Path(__file__).resolve().parents[1];out=root/'experiments/pixellab-orc-athletic-v1'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
own=read(out/'concept-skeleton.json')['keypoints'];P={p['label']:(p['x']*128,p['y']*128) for p in own}
G=[{p['label']:(p['x']*128,p['y']*128) for p in read(out/f'guide/agile-{i:02d}-skeleton.json')['keypoints']} for i in range(8)]
mean=statistics.mean
hipYs=[mean([g['RIGHT HIP'][1],g['LEFT HIP'][1]]) for g in G]
poses=[];plans=[]
for i,g in enumerate(G):
    bob=max(-1.2,min(1.2,(hipYs[i]-mean(hipYs))*.8))
    Q={k:[v[0],v[1]+bob] for k,v in P.items()}
    # Head/neck stay registered to their own reference, not another character's face.
    for side in ['RIGHT','LEFT']:
        for chain in [[f'{side} SHOULDER',f'{side} ELBOW',f'{side} ARM'],[f'{side} HIP',f'{side} KNEE',f'{side} LEG']]:
            for a,b in zip(chain,chain[1:]):
                length=math.dist(P[a],P[b]);dx=g[b][0]-g[a][0];dy=g[b][1]-g[a][1];norm=max(1,math.hypot(dx,dy));Q[b]=[Q[a][0]+length*dx/norm,Q[a][1]+length*dy/norm]
    poses.append([{**p,'x':round(Q[p['label']][0]/128,6),'y':round(Q[p['label']][1]/128,6)} for p in own]);plans.append({'frame':i,'bob':bob,'points':Q})
request={'action':'walk','description':'Bald muscular athletic adult orc, slightly lighter muted sage green skin, angular mature face, small ivory tusks, narrow waist, bare defined pectorals and abdomen, narrow brown leather cross harness, one compact charcoal iron shoulder guard, dark bracers, short leather hip protection, compact kneepads and brown practical boots, empty hands. Refined detailed medieval fantasy pixel art. Same face, proportions, palette and armor as own reference; connected neck and naturally aligned three-quarter head.','direction':'south-east','first_frame_url':'https://api.pixellab.ai/mcp/images/1e0cbd5c-6cab-4536-9330-de259a00a366/download','first_frame_keypoints':own,'keypoints':poses,'view':'low top-down','template_id':'mannequin','no_background':True,'seed':8241703}
(out/'Walk-request.json').write_text(json.dumps(request),encoding='utf-8')
(out/'walk-motion-plan.json').write_text(json.dumps({'method':'Measured actual Agile Walk joint angles; both arms/legs retargeted to own bone lengths, own stationary head/neck registration plus pelvis bob. Same south-east orientation as guide.','guide':'characters/orc-pixellab-04/source/studies/Walk/clip.json','cachedEstimates':'experiments/pixellab-orc-athletic-v1/guide/agile-00..07-skeleton.json','guidePixelsUsedByAnimationRenderer':False,'frames':plans},indent=2),encoding='utf-8')
print('Eight actual Agile pose phases adapted to Athletic limb lengths; own head retained.')
