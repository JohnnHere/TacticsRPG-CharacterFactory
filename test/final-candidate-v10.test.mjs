import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const ROOT = process.cwd();

function sha256(rel) {
  return crypto.createHash("sha256").update(fs.readFileSync(path.join(ROOT, rel))).digest("hex");
}

test("final-candidate-v10: 28-cell manifest, Architecture C 4-view reuse, and staged package hashes", () => {
  const mPath = "characters/orc-v1/source/final-candidate-v10/candidate28manifest.json";
  const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, mPath), "utf8"));

  assert.equal(manifest.totalClips, 28);
  assert.equal(manifest.cells.length, 28);
  assert.equal(manifest.technicalStatus, "TECHNICALLY_COMPLETE");
  assert.equal(manifest.artisticStatus, "VISUAL_REVIEW_REQUIRED");
  assert.equal(manifest.creatorApproval, "PENDING_CREATOR");
  assert.equal(manifest.runtimeImplemented, false);

  for (const cell of manifest.cells) {
    assert.equal(sha256(cell.clipJson), cell.clipSha256, `clipSha256 mismatch on ${cell.cellId}`);
    const clip = JSON.parse(fs.readFileSync(path.join(ROOT, cell.clipJson), "utf8"));
    for (const f of clip.frames) {
      assert.equal(sha256(f.png), f.sha256, `frame sha256 mismatch on ${cell.cellId} F${f.index}`);
    }
  }

  const arch = JSON.parse(fs.readFileSync(path.join(ROOT, manifest.architectureC.verification), "utf8"));
  assert.equal(arch.status, "PASS");
  assert.equal(arch.bodyFramesModifiedForVariantB, 0);
  assert.equal(arch.handFramesModifiedForVariantB, 0);
  assert.equal(arch.unarmedWeaponPixelsTotal, 0);
  assert.equal(arch.partialAlphaPixelsTotal, 0);
  assert.equal(arch.weaponPixelsBelowGroundYTotal, 0);

  for (const dir of ["front_r", "front_l", "back_r", "back_l"]) {
    assert.equal(arch.views[dir].bodyIdenticalFrames, 14);
    assert.equal(arch.views[dir].handIdenticalFrames, 14);
    assert.ok(arch.views[dir].totalSilhouetteDeltaABPx >= 990, `Expected real silhouette delta in ${dir}`);
  }

  const distHashes = JSON.parse(fs.readFileSync(path.join(ROOT, "dist/orc-v1/final-candidate-v10/hashes.json"), "utf8"));
  assert.equal(distHashes.totalFiles, 292);
});
