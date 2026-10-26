"""Pose metadata only. Never edits sprite pixels."""
from pathlib import Path
import json,base64,math,statistics
root=Path(__file__).resolve().parents[1]
out=root/'experiments/pixellab-orc-refinement-v8'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
own=read(out/'frontal-reference-skeleton.json')['keypoints']
P={p['label']:(p['x']*128,p['y']*128) for p in own}
guides=[{p['label']:(p['x']*128,p['y']*128) for p in read(out/f'agile-{i:02d}-skeleton.json')['keypoints']} for i in range(8)]
mean=lambda a:statistics.mean(a)
cx=mean([P['RIGHT HIP'][0],P['LEFT HIP'][0]])
hipY=mean([P['RIGHT HIP'][1],P['LEFT HIP'][1]])
guideHip=[mean([g['RIGHT HIP'][1],g['LEFT HIP'][1]]) for g in guides]
shoulderHalf=abs(P['LEFT SHOULDER'][0]-P['RIGHT SHOULDER'][0])/2
shoulderY=mean([P['LEFT SHOULDER'][1],P['RIGHT SHOULDER'][1]])
hipHalf=abs(P['LEFT HIP'][0]-P['RIGHT HIP'][0])/2
poses=[];plans=[]
for i,g in enumerate(guides):
    bob=max(-1,min(1,(guideHip[i]-mean(guideHip))*.65))
    Q={k:[v[0],v[1]+bob] for k,v in P.items()}
    Q['NECK']=[cx,P['NECK'][1]+bob]
    # Level original head, preserving its width and height. Nose shares torso axis.
    Q['NOSE']=[cx,P['NOSE'][1]+bob]
    for pair in [('RIGHT EYE','LEFT EYE'),('RIGHT EAR','LEFT EAR')]:
        half=abs(P[pair[0]][0]-P[pair[1]][0])/2
        y=mean([P[pair[0]][1],P[pair[1]][1]])+bob
        Q[pair[0]]=[cx-half,y];Q[pair[1]]=[cx+half,y]
    phase={}
    for side,sgn in [('RIGHT',-1),('LEFT',1)]:
        a=f'{side} LEG';k=f'{side} KNEE';h=f'{side} HIP';s=f'{side} SHOULDER';e=f'{side} ELBOW';w=f'{side} ARM'
        xs=[q[a][0] for q in guides];ys=[q[a][1] for q in guides]
        # Convert guide stride phase to depth instead of lateral screen travel.
        phaseX=(g[a][0]-mean(xs))/max(1,(max(xs)-min(xs))/2)
        ground=statistics.median([q[a][1]-.07*(q[a][0]-mean(xs)) for q in guides])
        lift=max(0,ground+.07*(g[a][0]-mean(xs))-g[a][1])
        Q[h]=[cx+sgn*hipHalf,hipY+bob]
        lane=cx+sgn*(hipHalf+2)
        ankleBase=P[a][1]
        ankleY=ankleBase+phaseX*4.5-min(4,lift*.35)
        kneeY=P[k][1]+phaseX*1.8-min(1.5,lift*.13)+bob*.25
        ankleY=max(kneeY+16,ankleY)
        Q[a]=[lane,ankleY];Q[k]=[(Q[h][0]+lane)/2,kneeY]
        Q[s]=[cx+sgn*shoulderHalf,shoulderY+bob]
        # Opposed arm swing expressed in depth; keep arms beside the same body.
        wristY=P[w][1]-phaseX*3+bob
        Q[w]=[P[w][0],wristY]
        Q[e]=[P[e][0],P[e][1]-phaseX*1.5+bob]
        phase[side]={'sourceStridePhase':phaseX,'sourceLift':lift,'fixedLaneX':lane,'ankleY':ankleY}
    poses.append([{**p,'x':round(Q[p['label']][0]/128,6),'y':round(Q[p['label']][1]/128,6)} for p in own])
    plans.append({'frame':i,'bob':bob,'phase':phase,'points':Q})
request=read(out/'07-Forward-request.json')
request.update(first_frame_base64=base64.b64encode((out/'frontal-reference.png').read_bytes()).decode(),first_frame_keypoints=own,keypoints=poses,seed=8241603,direction='south')
request.pop('first_frame_url',None)
(out/'07-FrontalWalk-request.json').write_text(json.dumps(request),encoding='utf-8')
(out/'07-frontal-motion-plan.json').write_text(json.dumps({'sourceGuide':'characters/orc-pixellab-04/source/studies/Walk/clip.json','reference':'frontal-reference.png','sourceGuidePixelsUsedForRendering':False,'method':'Measured Agile stride/support/lift/bob phases projected onto frontal depth; adapted to own frontal anatomy, reduced foot lift, fixed lanes and level head.','frames':plans},indent=2),encoding='utf-8')
print('Prepared 8 frontal whole-body poses; sprite pixels unchanged.')
