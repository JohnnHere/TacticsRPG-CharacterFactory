import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const ROOT = process.cwd();
const EXP_DIR = path.join(ROOT, "experiments/main-orc-hybrid-weapon-04b2");

function sha256File(filePath) {
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function buildExportPipelineManifest() {
  const gripProfile = JSON.parse(fs.readFileSync(path.join(EXP_DIR, "grip-profile-back-r.json"), "utf8"));
  const clipA = JSON.parse(fs.readFileSync(path.join(EXP_DIR, "full/a/clip.json"), "utf8"));
  const clipB = JSON.parse(fs.readFileSync(path.join(EXP_DIR, "full/b/clip.json"), "utf8"));

  const pipeline = {
    schemaVersion: "1.0.0",
    experimentId: "main-orc-hybrid-weapon-04b2",
    pilot: "B2",
    architecture: "Architecture C (Hybrid Weapon Architecture)",
    direction: "back_r",
    action: "Sword",
    authoritativeSource: {
      clip: gripProfile.sourceClip,
      clipSha256: gripProfile.sourceClipSha256,
      master: gripProfile.sourceMaster,
      masterSha256: gripProfile.sourceMasterSha256,
    },
    layerOrder: ["weaponBack", "body", "weaponFront", "handFront"],
    variants: {
      A: {
        id: clipA.weapon.id,
        name: clipA.weapon.name,
        master: clipA.master,
        masterSha256: clipA.masterSha256,
        strip: clipA.strip,
        stripSha256: clipA.stripSha256,
        clipManifest: "experiments/main-orc-hybrid-weapon-04b2/full/a/clip.json",
        clipManifestSha256: sha256File(path.join(EXP_DIR, "full/a/clip.json")),
      },
      B: {
        id: clipB.weapon.id,
        name: clipB.weapon.name,
        master: clipB.master,
        masterSha256: clipB.masterSha256,
        strip: clipB.strip,
        stripSha256: clipB.stripSha256,
        clipManifest: "experiments/main-orc-hybrid-weapon-04b2/full/b/clip.json",
        clipManifestSha256: sha256File(path.join(EXP_DIR, "full/b/clip.json")),
      },
    },
    reusableStages: [
      "representative (F02, F05, F08, F11)",
      "full (F00..F13, 730 ms)",
    ],
  };

  fs.writeFileSync(path.join(EXP_DIR, "export-pipeline.json"), JSON.stringify(pipeline, null, 2) + "\n");
  console.log("Wrote export-pipeline.json");
}

buildExportPipelineManifest();

