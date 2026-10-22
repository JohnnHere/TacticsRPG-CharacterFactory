import fs from 'node:fs';import path from 'node:path';
import {inside,hash,DIRECTIONS,slash} from './core.mjs';import {decode,measure} from './images.mjs';import {checkFrameHashes} from './action-contract.mjs';
export const actionFingerprint=clips=>hash(Buffer.from(JSON.stringify(clips.map(r=>({direction:r.direction,frames:r.frames,editableSha256:r.editableSha256})))));
// Produces a validated copy plan. Never discovers clips by glob or infers weapon compatibility.
export function planUnarmedExport(root,id,review,clips){
 if(review.status!=='APPROVED_BY_CREATOR'||!review.approvalEvidence?.reviewer||!review.approvalEvidence?.quote)throw Error('Explicit supplement approval absent');
 if(clips.length!==4||new Set(clips.map(c=>c.direction)).size!==4||DIRECTIONS.some(d=>!clips.some(c=>c.direction===d)))throw Error('Four actual directions required');
 if(actionFingerprint(review.clips)!==review.candidateFingerprint||actionFingerprint(clips)!==review.candidateFingerprint)throw Error('Supplement approval stale');
 const copies=[],directions={};
 for(const c of clips){
  if(c.durationMs!==90||c.loop!==false||c.weaponOverlay!==false)throw Error('Unarmed timing/overlay mismatch');
  if(!c.artisticReview?.startsWith('APPROVED'))throw Error('Clip not approved');
  checkFrameHashes(root,c.frames);
  const own=f=>{const absolute=inside(root,f);inside(path.join(root,'characters',id),path.relative(path.join(root,'characters',id),absolute));return absolute;};
  if(hash(fs.readFileSync(own(c.editable)))!==c.editableSha256)throw Error('Editable SHA256 changed');
  const frames=c.frames.map((f,i)=>{const source=own(f.file),decoded=decode(source),m=measure(decoded.image);if(decoded.colorType!==6||decoded.image.depth!==8||m.width!==128||m.height!==128||m.partial||m.bottom!==126)throw Error('Native contract mismatch');
   const relative=slash(path.relative(path.join(root,'characters',id,'sprites'),source));const reuse=!!c.reuse;
   if(reuse&&(!relative.startsWith('Animations/Attack/')||relative.startsWith('..')))throw Error('Reused punch must be existing own Attack');
   const output=reuse?relative:`Actions/basic-unarmed/v1/${c.direction}/attack_${c.direction}_${String(i).padStart(2,'0')}.png`;
   if(!reuse)copies.push({source:f.file,path:output,sha256:f.sha256});return {path:output,sha256:f.sha256};
  });
  directions[c.direction]={frames,durationMs:90,loop:false,weaponOverlay:false,bodySourceReuse:!!c.reuse,sourceEditable:c.editable,sourceEditableSha256:c.editableSha256};
 }
 return {copies,manifest:{schemaVersion:1,actionProfile:'basic.unarmed',selection:{actionKind:'basic-attack',equippedWeaponKind:null},profile:{width:128,height:128,groundY:126,ppu:100},candidateFingerprint:review.candidateFingerprint,approvalEvidence:review.approvalEvidence,directions,runtimeImplemented:false,weaponBindingsProven:0}};
}
