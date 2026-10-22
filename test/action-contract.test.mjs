import test from 'node:test';import assert from 'node:assert/strict';import {resolveActionProfile} from '../src/action-contract.mjs';
test('basic unarmed never uses a Job cast or bow gesture',()=>{
 for(const job of ['Warrior','Squire','Archer','Apprentice Mage','Acolyte','Rogue','Scout','Brawler'])assert.equal(resolveActionProfile({actionKind:'basic-attack',equippedWeaponKind:null,job,abilityVisualProfile:'ability.offensive-cast'}),'basic.unarmed');
});
test('equipped basic action follows actual weapon; unknown or omitted equipment fails',()=>{
 for(const [weapon,expected] of [['Sword','basic.one-hand-swing'],['Axe','basic.one-hand-swing'],['Bow','basic.bow-shot']])assert.equal(resolveActionProfile({actionKind:'basic-attack',equippedWeaponKind:weapon,job:'Acolyte'}),expected);
 for(const kind of [undefined,0,'None','Unknown'])assert.throws(()=>resolveActionProfile({actionKind:'basic-attack',equippedWeaponKind:kind}));
});
test('ability requires its explicit visual profile and cannot reuse basic attack implicitly',()=>{
 assert.equal(resolveActionProfile({actionKind:'ability',equippedWeaponKind:null,abilityVisualProfile:'ability.support-cast'}),'ability.support-cast');
 assert.throws(()=>resolveActionProfile({actionKind:'ability',equippedWeaponKind:'Sword'}));assert.throws(()=>resolveActionProfile({actionKind:'ability',abilityVisualProfile:'basic.unarmed'}));
});
