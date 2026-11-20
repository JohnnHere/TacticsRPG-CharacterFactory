import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";

const ROOT = process.cwd();
const ASEPRITE = "F:/SteamLibrary/steamapps/common/Aseprite/Aseprite.exe";
const userFolder = path.join(ROOT, "tmp", "aseprite-batch-profile");
fs.mkdirSync(userFolder, { recursive: true });

const env = { ...process.env, ASEPRITE_USER_FOLDER: userFolder };

console.log("[1/3] Running Aseprite step1_weapons_and_swords.lua...");
execFileSync(ASEPRITE, ["--batch", "--noinapp", "--script", "experiments/main-orc-final-v10/scripts/step1_weapons_and_swords.lua"], {
  cwd: ROOT,
  env,
  stdio: "inherit",
});

console.log("[2/4] Running Aseprite step2_axes_and_remaining.lua...");
execFileSync(ASEPRITE, ["--batch", "--noinapp", "--script", "experiments/main-orc-final-v10/scripts/step2_axes_and_remaining.lua"], {
  cwd: ROOT,
  env,
  stdio: "inherit",
});

console.log("[3/4] Running Aseprite step3_polish_all_other_clips.lua...");
execFileSync(ASEPRITE, ["--batch", "--noinapp", "--script", "experiments/main-orc-final-v10/scripts/step3_polish_all_other_clips.lua"], {
  cwd: ROOT,
  env,
  stdio: "inherit",
});

console.log("[4/4] Running build_manifests_and_verify.mjs...");
execFileSync(process.execPath, ["experiments/main-orc-final-v10/build_manifests_and_verify.mjs"], {
  cwd: ROOT,
  stdio: "inherit",
});
