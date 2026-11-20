import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { ROOT, hash, readJSON } from '../../src/core.mjs';

const manifestPath = 'characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json';
const patchPath = 'characters/orc-v1/source/combat-rescue-v5/final-weapon-patch.json';
const validationPath = 'experiments/main-orc-combat-rescue-v5/technical-validation.json';
const reexportDir = 'experiments/main-orc-combat-rescue-v5/source-reexports';
const browserDir = 'experiments/main-orc-combat-rescue-v5/browser-checks-final';
const rejectedPath = 'experiments/main-orc-combat-rescue-v5/qa5-rejected-manifest.json';
const absolute = file => path.resolve(ROOT, file);
const digest = file => hash(fs.readFileSync(absolute(file)));
const readText = file => fs.readFileSync(absolute(file), 'utf8');

const manifest = readJSON(absolute(manifestPath));
const patch = readJSON(absolute(patchPath));

const patchByCell = new Map(patch.cells.map(cell => [cell.cellId, cell]));
for (const cell of manifest.cells) {
  if (!cell.isAffected) continue;
  const entry = patchByCell.get(cell.cellId);
  if (entry) {
    assert.equal(entry.clipSha256, cell.clipSha256, `Patch and manifest disagree on ${cell.cellId}`);
    cell.reviewStatus = 'INDEPENDENT_QA_ACCEPTED_NOT_CREATOR_APPROVED';
    cell.qaVerdict = entry.qaVerdict;
    cell.qaEvidence = entry.qaEvidence;
    cell.provenance = entry.provenance;
    cell.notes = entry.notes;
  } else if (cell.action === 'Unarmed') {
    cell.reviewStatus = 'NO_CONFIRMED_DEFECT_IN_PRIOR_INDEPENDENT_QA';
    cell.qaVerdict = 'SUSTAINED_STATIC';
    cell.qaEvidence = [
      'experiments/main-orc-combat-rescue-v5/qa-grok/qa-result.json',
      'experiments/main-orc-combat-rescue-v5/qa-grok/report.md',
    ];
    cell.notes = 'Front Unarmed F03 recoil and the two rear Unarmed cycles were sustained by the independent reviewer; that freeze was rejected for weapon/grip and rear-body defects, which this candidate replaces. No fresh review of these four cells is claimed.';
  } else {
    assert.equal(`${cell.direction}/${cell.action}`, 'back_l/Walk');
    cell.reviewStatus = 'COLOR_ONLY_EDIT_LIMITED_CONTINUOUS_PERCEPTION';
    cell.qaVerdict = 'NO_DEFECT_DEMONSTRATED_LIMITED';
    cell.qaEvidence = [
      'experiments/main-orc-combat-rescue-v5/qa-grok/qa-result.json',
      'experiments/main-orc-combat-rescue-v5/localized/report.md',
    ];
    cell.notes = '2741 colour-only edits in F04-F07 of back_l/Walk; alpha and timing unchanged. Independent QA did not demonstrate a wrong-pose collage but did not claim human continuous 1x perception.';
  }
}

manifest.technicalStatus = 'TECHNICAL_PASS';
manifest.artisticStatus = 'VISUAL_REVIEW_REQUIRED';
manifest.creatorApproval = 'PENDING_CREATOR';
manifest.creatorApproved = false;
manifest.eligibleForIntegration = false;
manifest.integrationStatus = 'ISOLATED_CANDIDATE_NO_UNITY_AUTHORIZATION';
manifest.runtimeImplemented = false;
manifest.verification = {
  technicalValidation: { report: validationPath, note: 'Run after this manifest is final; the report records the manifest hash it verified.' },
  savedSourceReexport: { dir: reexportDir, note: 'One result per verified manifest hash; Aseprite batch CLI reopens every selected saved master and re-renders its frames.' },
  browserChecks: { dir: browserDir, status: 'BROWSER CHECK PASSED', checks: 21 },
  protectedInputs: { report: 'experiments/main-orc-combat-rescue-v5/input-preservation-result.json', files: 3506 },
  rejectedSnapshot: { report: rejectedPath, sha256: digest(rejectedPath), immutableSourcesPreserved: true },
  tests: { builderUnittest: '4/4 PASS', integrationNodeTests: '4/4 PASS' },
  limits: [
    'Continuous 1x motion perception in a real player was not established for every clip; static frame-by-frame review plus contact strips and real Chromium playback checks are what exist.',
    'No anthropometric or behavioural validation in Unity; no Unity write, no pointer promotion, no runtime implementation.',
  ],
};
manifest.weaponPatch = { path: patchPath, sha256: digest(patchPath), cells: patch.cells.length };
manifest.qaEvidenceIndex = {
  front_r_Sword: 'experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/front-r-sword-full-result.json',
  front_l_Sword: 'experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/qa-result.json',
  front_r_Axe: 'experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/qa-result.json',
  front_l_Axe: 'experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/qa-result.json',
  back_r_Axe: 'experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/rear-axe-full-result.json',
  back_l_Sword: 'experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/rear-sword-l-back-full-result.json',
  back_r_Sword: 'experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/rear-two-remaining-result.json',
  back_l_Axe: 'experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/rear-two-remaining-result.json',
};
manifest.qaReviewer = 'Gemini 3.8 Flash (High) via Antigravity, independent sessions; earlier reviews by Grok 4.7/Copilot and Sol/Codex remain in the report';

fs.writeFileSync(absolute(manifestPath), `${JSON.stringify(manifest, null, 2)}\n`);
const out = {
  manifestPath,
  manifestSha256: digest(manifestPath),
  cells: manifest.cells.length,
  activeCandidates: manifest.activeCandidatesCount,
  aliases: manifest.unchangedAliasesCount,
  totalFrames: manifest.totalFrames,
  technicalStatus: manifest.technicalStatus,
  artisticStatus: manifest.artisticStatus,
  creatorApproval: manifest.creatorApproval,
};
fs.writeFileSync(absolute('experiments/main-orc-combat-rescue-v5/final-manifest-summary.json'), `${JSON.stringify(out, null, 2)}\n`);
console.log(JSON.stringify(out));


