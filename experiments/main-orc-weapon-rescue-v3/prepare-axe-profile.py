from pathlib import Path
import json
E=Path(__file__).resolve().parent;prefix='experiments/main-orc-weapon-rescue-v3';weapons=json.loads((E/'weapon-revisions.json').read_text(encoding='utf-8'));rest='characters/orc-v1/source/studies/Idle/00.png'
def f(i,phase,time,grip,angle,hand,behind=False):return {'input':rest if i is None else f'{prefix}/axe-posed/raw/{i:02d}.png','phase':phase,'durationMs':time,'grip':grip,'angle':angle,'visible':grip is not None,'hand':hand,'cleanup':[],'footShift':None,'behind':behind}
frames=[
 f(None,'rest',80,None,0,[]),
 f(0,'load',120,[29,70],300,[[[24,66],[29,65],[32,68],[32,72],[28,74],[24,71]],[[29,67],[34,68],[34,72],[30,74]]]),
 f(1,'raise',110,[24,54],325,[[[20,50],[24,49],[28,51],[28,55],[24,58],[20,56]],[[25,52],[29,52],[29,56],[25,58]]]),
 f(2,'cocked-shoulder',170,[34,36],350,[[[30,32],[34,31],[38,33],[38,37],[34,39],[30,37]],[[35,33],[39,34],[39,38],[35,40]]],True),
 f(3,'release',70,[82,55],35,[[[77,51],[81,49],[85,51],[86,55],[82,58],[78,57]],[[83,52],[87,53],[87,57],[83,59]]]),
 f(4,'impact',70,[84,79],85,[[[79,75],[83,74],[87,76],[87,80],[83,83],[79,81]],[[84,76],[88,77],[88,81],[84,83]]]),
 f(5,'follow-through',120,[74,84],90,[[[69,80],[73,78],[77,80],[78,84],[74,87],[70,86]],[[75,81],[79,82],[79,86],[75,88]]]),
 f(6,'recovery',150,[65,84],80,[[[60,80],[64,78],[68,80],[69,84],[65,87],[61,86]],[[66,81],[70,82],[70,86],[66,88]]]),
 f(7,'after-attack-settle',100,None,0,[]),
 f(None,'return-unarmed',140,None,0,[])]
(E/'axe-profile-authored.json').write_text(json.dumps({'id':'basic.axe-chop','weapon':weapons['axe'],'frames':frames},indent=2),encoding='utf-8');print('Axe: ten-frame attack/return, 1130ms, visible interval1..7')
