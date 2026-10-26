"""Hand-authored whole-body key poses, not an IK/runtime framework. No raster editing."""
from pathlib import Path
import json,base64,hashlib
R=Path(__file__).resolve().parents[2];E=Path(__file__).resolve().parent
source=R/'characters/orc-v1/concepts/concept-selected.png'
old=json.loads((R/'experiments/orc-v1-weapons-v2/attack-skeleton-request.json').read_text(encoding='utf-8'))
assert hashlib.sha256(base64.b64decode(old['first_frame_base64'])).digest()==hashlib.sha256(source.read_bytes()).digest()
base=old['first_frame_keypoints']
def pose(neck,rs,re,rw,ls,le,lw,rh,lh,rk,lk,ra=(44,117),la=(82,115)):
 pts={a['label']:{**a} for a in base}; coords={'NECK':neck,'RIGHT SHOULDER':rs,'RIGHT ELBOW':re,'RIGHT ARM':rw,'LEFT SHOULDER':ls,'LEFT ELBOW':le,'LEFT ARM':lw,'RIGHT HIP':rh,'LEFT HIP':lh,'RIGHT KNEE':rk,'LEFT KNEE':lk,'RIGHT LEG':ra,'LEFT LEG':la}
 dx,dy=neck[0]-66.1,neck[1]-35
 for label in ['NOSE','RIGHT EYE','LEFT EYE','RIGHT EAR','LEFT EAR']:
  coords[label]=(pts[label]['x']*128+dx,pts[label]['y']*128+dy)
 for label,(x,y) in coords.items():pts[label]['x']=x/128;pts[label]['y']=y/128
 return list(pts.values())
poses=[
 pose((64,37),(43,37),(24,49),(28,62),(83,39),(94,60),(98,76),(55,74),(74,74),(47,99),(86,98)),
 pose((63,36),(43,38),(21,48),(33,29),(80,39),(93,54),(96,69),(55,74),(73,74),(46,99),(86,98)),
 pose((66,36),(47,36),(31,19),(52,31),(80,39),(89,55),(93,70),(58,74),(76,74),(50,100),(86,98),(46,118)),
 pose((70,38),(55,39),(69,45),(85,51),(79,40),(85,56),(90,73),(61,73),(78,73),(53,100),(86,98),(48,119)),
 pose((71,40),(57,40),(72,54),(87,67),(79,41),(84,60),(91,77),(62,74),(79,74),(54,101),(86,99),(48,119)),
 pose((70,40),(54,41),(66,63),(77,79),(82,41),(87,61),(95,79),(61,74),(78,74),(53,100),(86,98),(48,119)),
 pose((68,37),(49,39),(47,61),(48,78),(85,37),(90,58),(97,77),(59,73),(77,73),(51,99),(85,97),(46,118)),
 base]
q={'action':'one-handed diagonal sword slash','description':'The SAME bald green Orc V1, same angular face and dark spiked iron armor, brown leather gloves, oxblood hip cloth and chainmail, armored knees and boots. Closed RIGHT fist naturally grips a SHORT 7-pixel wood handle ONLY, with curved fingers and thumb; NO blade, NO long stick, NO weapon head. Left hand empty. Exact current green skin, face, armor, materials, same rendering detail and body proportions.','direction':'south-east','view':'low top-down','template_id':'mannequin','first_frame_base64':base64.b64encode(source.read_bytes()).decode(),'first_frame_keypoints':base,'keypoints':poses,'no_background':True,'seed':10252620}
(E/'sword-posed-request.json').write_text(json.dumps(q,indent=2),encoding='utf-8')
(E/'sword-authored-poses.json').write_text(json.dumps({'description':'Whole-body load -> high guard -> hip/shoulder drive -> extension -> strike -> follow-through -> recovery. Original current character, no historical artwork. Hand-annotated joints; no IK solver.','poses':poses},indent=2),encoding='utf-8');print('8 whole-body sword poses prepared')
