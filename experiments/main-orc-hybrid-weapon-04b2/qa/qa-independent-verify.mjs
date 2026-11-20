// INDEPENDENT QA — Pilot B2 (back_r / Sword) re-verification.
// Read-only. Recomputes every claim from raw pixels/hashes; does not reuse run.mjs logic.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { PNG } from "pngjs";

const ROOT = process.cwd();
const SRC = path.join(ROOT, "characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword");
const EXP = path.join(ROOT, "experiments/main-orc-hybrid-weapon-04b2");
const E04 = path.join(ROOT, "experiments/main-orc-hybrid-weapon-04");
const E04B = path.join(ROOT, "experiments/main-orc-hybrid-weapon-04b");
const OUT = path.join(EXP, "qa", "qa-independent-results.json");

const sha256File = (p) => crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
const loadPng = (p) => PNG.sync.read(fs.readFileSync(p));
const nn = (i) => String(i).padStart(2, "0");
const identical = (a, b) => a.width === b.width && a.height === b.height && Buffer.compare(a.data, b.data) === 0;
const must = (p) => { if (!fs.existsSync(p)) throw new Error("MISSING: " + p); return p; };
const expF = (variant, sub, i) => must(path.join(EXP, "full", variant, sub, `F${nn(i)}.png`));
const srcP = (...parts) => must(path.join(SRC, ...parts));

// ---------- 1. Hashes ----------
const hashes = {
  srcCompositeMaster: sha256File(srcP("source", "composite.aseprite")),
  fullACompositeMaster: sha256File(must(path.join(EXP, "full/a/composite.aseprite"))),
  fullBCompositeMaster: sha256File(must(path.join(EXP, "full/b/composite.aseprite"))),
  srcCompositeStrip: sha256File(srcP("composite-strip.png")),
  fullAStrip: sha256File(must(path.join(EXP, "full/a/strip.png"))),
};
for (const [tag, base] of [["e04", E04], ["e04b", E04B], ["e04b2", EXP]]) {
  hashes[`swordA_png_${tag}`] = sha256File(must(path.join(base, "variants/sword-a/sword.png")));
  hashes[`swordA_master_${tag}`] = sha256File(must(path.join(base, "variants/sword-a/sword.aseprite")));
  hashes[`swordB_png_${tag}`] = sha256File(must(path.join(base, "variants/sword-b/sword.png")));
  hashes[`swordB_master_${tag}`] = sha256File(must(path.join(base, "variants/sword-b/sword.aseprite")));
}
const provA = JSON.parse(fs.readFileSync(must(path.join(EXP, "variants/sword-a/provenance.json")), "utf8"));
const provB = JSON.parse(fs.readFileSync(must(path.join(EXP, "variants/sword-b/provenance.json")), "utf8"));
hashes.e04AuthorLua = sha256File(must(path.join(E04, "author.lua")));

const hashChecks = {
  fullA_master_byte_identical_to_source_master: hashes.fullACompositeMaster === hashes.srcCompositeMaster,
  fullA_strip_byte_identical_to_source_strip: hashes.fullAStrip === hashes.srcCompositeStrip,
  swordA_png_identical_across_04_04b_04b2:
    hashes.swordA_png_e04 === hashes.swordA_png_e04b && hashes.swordA_png_e04b === hashes.swordA_png_e04b2,
  swordA_master_identical_across_04_04b_04b2:
    hashes.swordA_master_e04 === hashes.swordA_master_e04b && hashes.swordA_master_e04b === hashes.swordA_master_e04b2,
  swordB_png_identical_across_04_04b_04b2:
    hashes.swordB_png_e04 === hashes.swordB_png_e04b && hashes.swordB_png_e04b === hashes.swordB_png_e04b2,
  swordB_master_identical_across_04_04b_04b2:
    hashes.swordB_master_e04 === hashes.swordB_master_e04b && hashes.swordB_master_e04b === hashes.swordB_master_e04b2,
  provenance_scriptSha256_matches_e04_authorLua:
    provA.scriptSha256 === hashes.e04AuthorLua && provB.scriptSha256 === hashes.e04AuthorLua,
  swordA_variant_files_match_own_provenance_hashes:
    hashes.swordA_png_e04b2 === provA.pngSha256 && hashes.swordA_master_e04b2 === provA.masterSha256,
  swordB_variant_files_match_own_provenance_hashes:
    hashes.swordB_png_e04b2 === provB.pngSha256 && hashes.swordB_master_e04b2 === provB.masterSha256,
};

// ---------- 2. Blade palettes (for leftover-A-blade detection) ----------
const swordA = loadPng(must(path.join(EXP, "variants/sword-a/sword.png")));
const swordB = loadPng(must(path.join(EXP, "variants/sword-b/sword.png")));
const ckey = (r, g, b, a) => `${r},${g},${b},${a}`;
const aBlade = new Set(), aHilt = new Set(), bAll = new Set();
for (let y = 0; y < swordA.height; y++)
  for (let x = 0; x < swordA.width; x++) {
    const i = (swordA.width * y + x) * 4;
    if (!swordA.data[i + 3]) continue;
    (y <= 54 ? aBlade : aHilt).add(ckey(swordA.data[i], swordA.data[i + 1], swordA.data[i + 2], swordA.data[i + 3]));
  }
for (let i = 0; i < swordB.data.length; i += 4)
  if (swordB.data[i + 3]) bAll.add(ckey(swordB.data[i], swordB.data[i + 1], swordB.data[i + 2], swordB.data[i + 3]));
const aBladeOnly = new Set([...aBlade].filter((c) => !aHilt.has(c) && !bAll.has(c)));
// ---------- 3. Per-frame pixel recomputation ----------
const perFrame = [];
let totals = {
  bodyDiffVsSource: 0, handDiffVsSource: 0, bodyOnlyDiffAB: 0,
  compositeADiffVsSource: 0, weaponLayerADiffVsSource: 0,
  nonWeaponCompositeDiffAB: 0, silhouetteDeltaAB: 0,
  leftoverSwordABladeInB: 0, semiTransparentWeaponB: 0, unarmedWeaponPixels: 0,
};
for (let i = 0; i <= 13; i++) {
  const bodyA = loadPng(expF("a", "layers/body", i));
  const bodyB = loadPng(expF("b", "layers/body", i));
  const bodyS = loadPng(srcP("layers", "body", `${nn(i)}.png`));
  const hfA = loadPng(expF("a", "layers/handFront", i));
  const hfB = loadPng(expF("b", "layers/handFront", i));
  const hfS = loadPng(srcP("layers", "handFront", `${nn(i)}.png`));
  const wbA = loadPng(expF("a", "layers/weaponBack", i));
  const wbS = loadPng(srcP("layers", "weaponBack", `${nn(i)}.png`));
  const wfA = loadPng(expF("a", "layers/weaponFront", i));
  const wfS = loadPng(srcP("layers", "weaponFront", `${nn(i)}.png`));
  const bodyOnlyA = loadPng(expF("a", "body-only", i));
  const bodyOnlyB = loadPng(expF("b", "body-only", i));
  const wOnlyA = loadPng(expF("a", "weapon-only", i));
  const wOnlyB = loadPng(expF("b", "weapon-only", i));
  const compA = loadPng(expF("a", "composite", i));
  const compB = loadPng(expF("b", "composite", i));
  const compS = loadPng(srcP("frames", `${nn(i)}.png`));

  const bodyDiffVsSource = identical(bodyA, bodyS) && identical(bodyB, bodyS) ? 0 : 1;
  const handDiffVsSource = identical(hfA, hfS) && identical(hfB, hfS) ? 0 : 1;
  const bodyOnlyDiffAB = identical(bodyOnlyA, bodyOnlyB) ? 0 : 1;
  const compADiffVsSource = identical(compA, compS) ? 0 : 1;
  const weaponADiffVsSource = identical(wbA, wbS) && identical(wfA, wfS) ? 0 : 1;

  let weaponPixelsA = 0, weaponPixelsB = 0, silhouetteDeltaAB = 0,
    weaponDiffPixelsAB = 0, leftoverBladeInB = 0, semiTransparentB = 0;
  for (let p = 0; p < wOnlyA.data.length; p += 4) {
    const aA = wOnlyA.data[p + 3], aB = wOnlyB.data[p + 3];
    if (aA) weaponPixelsA++;
    if (aB) weaponPixelsB++;
    if ((aA > 0) !== (aB > 0)) silhouetteDeltaAB++;
    if (aB > 0 && aB < 255) semiTransparentB++;
    if (aB > 0 && aBladeOnly.has(ckey(wOnlyB.data[p], wOnlyB.data[p + 1], wOnlyB.data[p + 2], aB))) leftoverBladeInB++;
    if (aA > 0 || aB > 0) {
      const same = wOnlyA.data[p] === wOnlyB.data[p] && wOnlyA.data[p + 1] === wOnlyB.data[p + 1] &&
        wOnlyA.data[p + 2] === wOnlyB.data[p + 2] && aA === aB;
      if (!same) weaponDiffPixelsAB++;
    }
  }

  let compositeDiffPixelsAB = 0, nonWeaponCompositeDiffAB = 0;
  for (let p = 0; p < compA.data.length; p += 4) {
    const same = compA.data[p] === compB.data[p] && compA.data[p + 1] === compB.data[p + 1] &&
      compA.data[p + 2] === compB.data[p + 2] && compA.data[p + 3] === compB.data[p + 3];
    if (same) continue;
    compositeDiffPixelsAB++;
    const inWeaponMask = wOnlyA.data[p + 3] > 0 || wOnlyB.data[p + 3] > 0;
    if (!inWeaponMask) nonWeaponCompositeDiffAB++;
  }

  const unarmed = [0, 1, 12, 13].includes(i);
  if (unarmed && (weaponPixelsA > 0 || weaponPixelsB > 0)) totals.unarmedWeaponPixels += weaponPixelsA + weaponPixelsB;

  totals.bodyDiffVsSource += bodyDiffVsSource;
  totals.handDiffVsSource += handDiffVsSource;
  totals.bodyOnlyDiffAB += bodyOnlyDiffAB;
  totals.compositeADiffVsSource += compADiffVsSource;
  totals.weaponLayerADiffVsSource += weaponADiffVsSource;
  totals.nonWeaponCompositeDiffAB += nonWeaponCompositeDiffAB;
  totals.silhouetteDeltaAB += silhouetteDeltaAB;
  totals.leftoverSwordABladeInB += leftoverBladeInB;
  totals.semiTransparentWeaponB += semiTransparentB;

  perFrame.push({
    frame: i, code: `F${nn(i)}`, unarmed,
    bodyHandIdenticalToSource: bodyDiffVsSource === 0 && handDiffVsSource === 0,
    weaponLayersAIdenticalToSource: weaponADiffVsSource === 0,
    compositeAIdenticalToSource: compADiffVsSource === 0,
    weaponPixelsA, weaponPixelsB, silhouetteDeltaAB, weaponDiffPixelsAB,
    compositeDiffPixelsAB, nonWeaponCompositeDiffAB,
    leftoverSwordABladeInB: leftoverBladeInB, semiTransparentWeaponB: semiTransparentB,
  });
}

// ---------- 4. Durations & metadata ----------
const srcClip = JSON.parse(fs.readFileSync(srcP("clip.json"), "utf8"));
const clipFrames = srcClip.frames ?? srcClip.clips ?? srcClip.keyframes;
const srcDurations = clipFrames.map((f) => f.durationMs);
const readDurations = (v) =>
  JSON.parse(fs.readFileSync(must(path.join(EXP, "full", v, "frame-durations.json")), "utf8")).map((f) => f.durationMs);
const durA = readDurations("a"), durB = readDurations("b");
const contactStart = srcDurations.slice(0, 8).reduce((s, d) => s + d, 0);
const clipA = JSON.parse(fs.readFileSync(must(path.join(EXP, "full/a/clip.json")), "utf8"));
const clipB = JSON.parse(fs.readFileSync(must(path.join(EXP, "full/b/clip.json")), "utf8"));

const durationChecks = {
  source_total_730ms: srcDurations.reduce((s, d) => s + d, 0) === 730 && srcClip.totalDurationMs === 730,
  variantA_durations_match_source: JSON.stringify(durA) === JSON.stringify(srcDurations),
  variantB_durations_match_source: JSON.stringify(durB) === JSON.stringify(srcDurations),
  contact_F08_starts_at_325ms: contactStart === 325,
  variantAClip_declares_730ms: clipA.totalDurationMs === 730,
  variantBClip_declares_730ms: clipB.totalDurationMs === 730,
};

// ---------- 5. Representative == Full, review assets exist ----------
let repMatch = true;
for (const i of [2, 5, 8, 11])
  for (const v of ["a", "b"]) {
    const rep = loadPng(must(path.join(EXP, "representative", v, "composite", `F${nn(i)}.png`)));
    const full = loadPng(expF(v, "composite", i));
    if (!identical(rep, full)) repMatch = false;
  }
const reviewAssetsExist = [
  "review/index.html", "grip-10x-both.png", "representative-review-2x.png",
  "review/hands/a", "review/hands/b", "variants/sword-a/sword.png", "variants/sword-b/sword.png",
].every((rel) => fs.existsSync(path.join(EXP, rel)));
const handsComplete = ["a", "b"].every((v) =>
  Array.from({ length: 14 }, (_, i) => fs.existsSync(path.join(EXP, "review/hands", v, `${nn(i)}.png`))).every(Boolean));

// ---------- 6. Blade repaint stats totals ----------
const repaintStats = JSON.parse(fs.readFileSync(must(path.join(EXP, "blade-repaint-stats.json")), "utf8"));
const repaintTotals = Object.values(repaintStats).reduce(
  (acc, s) => ({ blade: acc.blade + s.bladePixelsRepainted, hilt: acc.hilt + s.hiltPixelsPreserved }),
  { blade: 0, hilt: 0 });

// ---------- Final ----------
const checks = {
  ...hashChecks,
  ...durationChecks,
  all14_body_and_handFront_identical_to_source: totals.bodyDiffVsSource === 0 && totals.handDiffVsSource === 0,
  all14_body_only_identical_between_A_and_B: totals.bodyOnlyDiffAB === 0,
  all14_composite_A_identical_to_source: totals.compositeADiffVsSource === 0,
  all14_weapon_layers_A_identical_to_source: totals.weaponLayerADiffVsSource === 0,
  unarmed_frames_zero_weapon_pixels: totals.unarmedWeaponPixels === 0,
  zero_weapon_silhouette_delta_A_vs_B: totals.silhouetteDeltaAB === 0,
  zero_non_weapon_composite_diff_A_vs_B: totals.nonWeaponCompositeDiffAB === 0,
  zero_leftover_swordA_blade_colors_in_B: totals.leftoverSwordABladeInB === 0,
  zero_semi_transparent_weapon_pixels_in_B: totals.semiTransparentWeaponB === 0,
  weapon_pixel_counts_identical_A_vs_B_every_frame: perFrame.every((f) => f.weaponPixelsA === f.weaponPixelsB),
  representative_matches_full: repMatch,
  review_assets_present: reviewAssetsExist && handsComplete,
  blade_repaint_totals_match_report: repaintTotals.blade === 4735 && repaintTotals.hilt === 2315,
};

const result = {
  qa: "independent-reverification",
  experiment: "main-orc-hybrid-weapon-04b2",
  reviewedAt: new Date().toISOString(),
  method: "Independent recomputation from raw PNG pixels (pngjs) and file hashes; pilot scripts not reused.",
  checks, totals, repaintTotals,
  durations: { source: srcDurations, variantA: durA, variantB: durB, contactF08StartMs: contactStart },
  perFrame, hashes,
};
fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify(result, null, 2) + "\n");

const failed = Object.entries(checks).filter(([, ok]) => !ok);
console.log(`Independent QA re-verification: ${Object.keys(checks).length - failed.length}/${Object.keys(checks).length} checks PASSED`);
if (failed.length) { console.error("FAILED:", failed.map(([k]) => k).join(", ")); process.exit(1); }
console.log("Written:", path.relative(ROOT, OUT));


