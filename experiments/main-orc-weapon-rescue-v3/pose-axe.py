"""Compact one-handed chop: whole-body authored key poses, no prop in generation."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];E=Path(__file__).resolve().parent
old=json.loads((E/'sword-posed-request.json').read_text(encoding='utf-8'));base=old['first_frame_keypoints']
def pose(neck,rs,re,rw,ls,le,lw,rh,lh,rk,lk):
 pts={a['label']:{**a} for a in base};coords={'NECK':neck,'RIGHT SHOULDER':rs,'RIGHT ELBOW':re,'RIGHT ARM':rw,'LEFT SHOULDER':ls,'LEFT ELBOW':le,'LEFT ARM':lw,'RIGHT HIP':rh,'LEFT HIP':lh,'RIGHT KNEE':rk,'LEFT KNEE':lk,'RIGHT LEG':(44,117),'LEFT LEG':(82,115)}
 dx,dy=neck[0]-66.1,neck[1]-35
 for label in ['NOSE','RIGHT EYE','LEFT EYE','RIGHT EAR','LEFT EAR']:coords[label]=(pts[label]['x']*128+dx,pts[label]['y']*128+dy)
 for label,(x,y) in coords.items():pts[label]['x']=x/128;pts[label]['y']=y/128
 return list(pts.values())
poses=[
pose((64,38),(43,40),(22,51),(28,64),(83,40),(93,59),(97,75),(55,75),(74,75),(47,100),(87,98)),
pose((63,38),(43,39),(19,53),(28,42),(81,39),(93,54),(97,70),(55,76),(73,76),(46,101),(87,99)),
pose((64,38),(44,39),(23,39),(39,38),(80,40),(92,55),(96,70),(56,76),(74,76),(47,101),(87,99)),
pose((69,39),(53,39),(67,44),(77,54),(79,41),(85,57),(91,73),(60,74),(78,74),(52,100),(86,98)),
pose((71,41),(56,42),(71,59),(82,76),(79,42),(84,61),(91,78),(62,75),(79,75),(53,101),(87,99)),
pose((70,41),(54,42),(64,65),(73,83),(81,42),(87,62),(95,79),(61,75),(78,75),(53,100),(86,98)),
pose((69,39),(51,40),(55,63),(63,78),(83,39),(89,60),(96,78),(60,74),(77,74),(51,99),(86,98)),
pose((67,36),(47,36),(40,58),(45,80),(85,36),(91,57),(98,77),(58,72),(76,72),(50,98),(85,97)),
base]
q={**old,'action':'heavy one-handed overhead downward strike','description':'The SAME bald green Orc V1 with dark spiked iron armor, brown leather gloves, oxblood hip cloth, chainmail, armored knees and boots. Both hands EMPTY. Right hand CLOSED in a natural firm gripping fist with curved fingers and thumb, NO object, NO tool, NO blade, NO stick. Left hand stays free. Exact same current angular face, green skin palette, detailed armor and rendering. Heavy grounded whole-body motion, fixed tactical camera.','keypoints':poses,'seed':10252630}
(E/'axe-posed-request.json').write_text(json.dumps(q,indent=2),encoding='utf-8');(E/'axe-authored-poses.json').write_text(json.dumps({'description':'Deep load -> elbow cock -> loaded peak -> torso-driven release -> downward impact -> follow-through -> staged recovery. Empty handed source; independent compact axe added only in Aseprite.','poses':poses},indent=2),encoding='utf-8');print('9 authored chop poses prepared')
