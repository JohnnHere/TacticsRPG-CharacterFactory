import fs from 'node:fs';import {inside,hash} from './core.mjs';
// Offline production contract only. This does not change Unity's WeaponKind enum.
export function resolveActionProfile({actionKind,equippedWeaponKind,abilityVisualProfile}){
 if(actionKind==='basic-attack'){
  if(equippedWeaponKind===null)return 'basic.unarmed';
  if(['Sword','Axe'].includes(equippedWeaponKind))return 'basic.one-hand-swing';
  if(equippedWeaponKind==='Bow')return 'basic.bow-shot';
  throw Error('Unknown equipment; no silent Sword/unarmed/cast fallback');
 }
 if(actionKind==='ability'&&typeof abilityVisualProfile==='string'&&abilityVisualProfile.startsWith('ability.'))return abilityVisualProfile;
 throw Error('Action/ability requires an explicit visual profile');
}
export function checkFrameHashes(root,frames){
 if(!Array.isArray(frames)||frames.length!==5)throw Error('Unarmed Orc clip requires five actual frames');
 const hashes=new Set();
 for(const f of frames){const file=inside(root,f.file);if(!fs.existsSync(file)||hash(fs.readFileSync(file))!==f.sha256)throw Error('Frame absent or SHA256 changed');hashes.add(f.sha256);}
 if(hashes.size!==5)throw Error('Duplicate unarmed poses');
 return true;
}
