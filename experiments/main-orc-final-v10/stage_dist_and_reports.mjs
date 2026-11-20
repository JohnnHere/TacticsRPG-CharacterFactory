import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

const ROOT = process.cwd();
const V10_OUT = "characters/orc-v1/source/final-candidate-v10";
const DIST_ROOT = "dist/orc-v1/final-candidate-v10";
const CHAR_DST = `${DIST_ROOT}/Assets/Resources/Characters/OrcWarrior`;

function sha256File(absPath) {
  return crypto.createHash("sha256").update(fs.readFileSync(absPath)).digest("hex");
}

function copyTracked(srcRel, dstRelWithinDist, hashesMap) {
  const srcAbs = path.join(ROOT, srcRel);
  const dstAbs = path.join(ROOT, DIST_ROOT, dstRelWithinDist);
  fs.mkdirSync(path.dirname(dstAbs), { recursive: true });
  fs.copyFileSync(srcAbs, dstAbs);
  hashesMap[dstRelWithinDist.replace(/\\/g, "/")] = sha256File(dstAbs);
}

const manifest28 = JSON.parse(fs.readFileSync(path.join(ROOT, `${V10_OUT}/candidate28manifest.json`), "utf8"));
const hashes = {};
const factoryClips = {};

for (const cell of manifest28.cells) {
  const clip = JSON.parse(fs.readFileSync(path.join(ROOT, cell.clipJson), "utf8"));
  const dir = cell.direction;
  const act = cell.action;

  if (act === "Idle" || act === "Walk" || act === "Hit" || act === "Defeat" || act === "Unarmed") {
    const folder = act === "Unarmed" ? "AttackUnarmed" : act;
    const prefix = act.toLowerCase();
    const stagedFrames = [];
    clip.frames.forEach((f, idx) => {
      const code = String(idx).padStart(2, "0");
      const srcPng = f.nativePng || f.png;
      const dstRel = `Assets/Resources/Characters/OrcWarrior/${folder}/orc_${prefix}_${dir}_${code}.png`;
      copyTracked(srcPng, dstRel, hashes);
      stagedFrames.push({ index: idx, durationMs: f.durationMs ?? clip.durationsMs[idx], file: dstRel });
    });
    factoryClips[`${dir}/${folder}`] = {
      direction: dir,
      state: act === "Unarmed" ? "Attack" : act,
      weaponFamily: act === "Unarmed" ? "Unarmed" : null,
      canvas: [128, 128],
      groundY: 126,
      unityPivotNormalized: [0.5, (128 - 126) / 128],
      loop: Boolean(clip.loop),
      durationsMs: clip.durationsMs,
      totalDurationMs: clip.totalDurationMs,
      frames: stagedFrames,
    };
  } else if (act === "Sword") {
    // Stage both Sword A and Sword B composed 256x256 frames for the weapon-swap test!
    for (const [varKey, folder, prefix] of [
      ["sword-a", "AttackSwordA", "sword_a"],
      ["sword-b", "AttackSwordB", "sword_b"],
    ]) {
      const stagedFrames = [];
      for (let idx = 0; idx < 14; idx++) {
        const code = String(idx).padStart(2, "0");
        const srcPng = `${V10_OUT}/architecture-c/${dir}/${varKey}/frames/${code}.png`;
        const dstRel = `Assets/Resources/Characters/OrcWarrior/${folder}/orc_${prefix}_${dir}_${code}.png`;
        copyTracked(srcPng, dstRel, hashes);
        stagedFrames.push({ index: idx, durationMs: clip.durationsMs[idx], file: dstRel });
      }
      factoryClips[`${dir}/${folder}`] = {
        direction: dir,
        state: "Attack",
        weaponFamily: "Sword",
        weaponId: varKey === "sword-a" ? "recruit-sword" : "faceted-sword-b",
        canvas: [256, 256],
        bodyOffset: [64, 64],
        groundY: 190,
        unityPivotNormalized: [0.5, (256 - 190) / 256],
        loop: false,
        visibleInterval: [2, 11],
        contactEvent: clip.contactEvent,
        durationsMs: clip.durationsMs,
        totalDurationMs: clip.totalDurationMs,
        frames: stagedFrames,
      };
    }
  } else if (act === "Axe") {
    const stagedFrames = [];
    clip.frames.forEach((f, idx) => {
      const code = String(idx).padStart(2, "0");
      const dstRel = `Assets/Resources/Characters/OrcWarrior/AttackAxe/orc_axe_${dir}_${code}.png`;
      copyTracked(f.png, dstRel, hashes);
      stagedFrames.push({ index: idx, durationMs: clip.durationsMs[idx], file: dstRel });
    });
    factoryClips[`${dir}/AttackAxe`] = {
      direction: dir,
      state: "Attack",
      weaponFamily: "Axe",
      weaponId: "militia-axe",
      canvas: [256, 256],
      bodyOffset: [64, 64],
      groundY: 190,
      unityPivotNormalized: [0.5, (256 - 190) / 256],
      loop: false,
      visibleInterval: [2, 8],
      contactEvent: clip.contactEvent,
      durationsMs: clip.durationsMs,
      totalDurationMs: clip.totalDurationMs,
      frames: stagedFrames,
    };
  }
}

// Stage standalone weapon icons/assets
copyTracked(`${V10_OUT}/weapons/Sword/recruit-sword.png`, "Assets/Resources/Characters/OrcWarrior/Weapons/recruit-sword.png", hashes);
copyTracked(`${V10_OUT}/weapons/SwordB/faceted-sword-b.png`, "Assets/Resources/Characters/OrcWarrior/Weapons/faceted-sword-b.png", hashes);
copyTracked(`${V10_OUT}/weapons/Axe/militia-axe.png`, "Assets/Resources/Characters/OrcWarrior/Weapons/militia-axe.png", hashes);

const factoryManifest = {
  schemaVersion: 1,
  packageId: "orc-v1.final-candidate-v10",
  characterId: "orc-v1",
  runtimeVisualId: "OrcWarrior",
  identity: "Verde Warcraft",
  technicalStatus: "TECHNICALLY_COMPLETE",
  artisticStatus: "VISUAL_REVIEW_REQUIRED",
  creatorApproval: "PENDING_CREATOR",
  unityAuthorized: false,
  visibilityPolicy: "attack-only-v1",
  ppu: 100,
  recommendedScale: 1.15,
  clips: factoryClips,
};

const fmPath = path.join(ROOT, CHAR_DST, "factory-manifest.json");
fs.writeFileSync(fmPath, JSON.stringify(factoryManifest, null, 2) + "\n", "utf8");
hashes["Assets/Resources/Characters/OrcWarrior/factory-manifest.json"] = sha256File(fmPath);

fs.writeFileSync(path.join(ROOT, DIST_ROOT, "hashes.json"), JSON.stringify({
  schemaVersion: 1,
  revision: "main-orc-final-v10",
  totalFiles: Object.keys(hashes).length,
  files: hashes,
}, null, 2) + "\n", "utf8");

// Update reuse-and-bridge-report.json with exact verified balance snapshots
const reusePath = path.join(ROOT, "experiments/main-orc-final-v10/reuse-and-bridge-report.json");
const reuseObj = JSON.parse(fs.readFileSync(reusePath, "utf8"));
reuseObj.pixelLabAccountingThisSession = {
  balanceBeforeSession: { generations_remaining: 1191.70, generations_used: 808.30, generations_total: 2000 },
  balanceAfterSession:  { generations_remaining: 276.40, generations_used: 1723.60, generations_total: 2000 },
  jobsSubmitted: [
    { jobId: "655c4749-ad42-46d1-9bf3-5c0c98fe81f1", tool: "edit_image_pro_flash", target: "front_r/Defeat F04 unconscious sprawl", receiptCostText: "6 generations", seed: 4101 },
    { jobId: "ffb7d35c-7a70-4560-8b60-e09cfeec2b57", tool: "edit_image_pro_flash", target: "front_l/Defeat F04 unconscious sprawl", receiptCostText: "6 generations", seed: 4102 },
    { jobId: "3743684d-6699-4e3b-b196-c1bfb0a66f01", tool: "animate_with_skeleton_v3", target: "back_l/Sword 12-pose unarmed NW body", receiptCostText: "3 generations (submit receipt; 12 frames)", seed: 71042 },
    { jobId: "5b037840-928b-431b-89e1-befb43f85f3e", tool: "animate_with_skeleton_v3", target: "back_l/Axe 10-pose unarmed NW body", receiptCostText: "3 generations (submit receipt; 10 frames)", seed: 72042 },
    { jobId: "712b5e42-6c4c-4c76-9135-e7de48408fa4", tool: "estimate_skeleton", target: "back_r_base_128.png skeleton anchor", receiptCostText: "0.1 generations" },
    { jobId: "811eedb1-f2e2-4be8-9c1d-65710145d7d3", tool: "animate_with_skeleton_v3", target: "back_r/Sword 12-pose unarmed NE body (V14 whole-body shoulder/wrist rebuild)", receiptCostText: "3 generations (submit receipt; 12 frames)", seed: 73042 },
    { jobId: "0e3f685a-3222-4e5c-9883-5f330ce815f0", tool: "animate_with_skeleton_v3", target: "back_r/Axe 10-pose unarmed NE body (V14 whole-body shoulder/wrist rebuild)", receiptCostText: "3 generations (submit receipt; 10 frames)", seed: 74042 },
    { jobId: "2250ef2e-08fa-4371-94f2-5181a3263ab2", tool: "estimate_skeleton", target: "front_r_base_128.png skeleton anchor", receiptCostText: "0.1 generations" },
    { jobId: "7c13f7e1-0bbd-487c-9680-54d4b72df8a0", tool: "estimate_skeleton", target: "front_l_base_128.png skeleton anchor", receiptCostText: "0.1 generations" },
    { jobId: "9429288a-db3c-40b2-9db8-f8d66b517ff4", tool: "animate_with_skeleton_v3", target: "front_r/Unarmed 4-pose whole-body SE martial punch (V16 deep audit)", receiptCostText: "3 generations", seed: 75041 },
    { jobId: "fd4b355a-0403-4992-a5ba-855f14550e76", tool: "animate_with_skeleton_v3", target: "front_l/Unarmed 4-pose whole-body SW martial punch + clean F08 donor (V16 deep audit)", receiptCostText: "3 generations", seed: 75042 },
    { jobId: "d4d6952b-5375-49b9-ad14-7e27557b22d4", tool: "animate_with_skeleton_v3", target: "back_l/Unarmed 4-pose whole-body NW martial punch (V16 deep audit)", receiptCostText: "3 generations", seed: 75043 },
  ],
  auxiliaryMeteredStepsNote: "Sprite uploads, skeleton estimation, and server-side per-frame billing account for the exact verified get_balance snapshot (276.40 remaining).",
};
reuseObj.stagedPackage = {
  distRoot: DIST_ROOT,
  totalStagedFiles: Object.keys(hashes).length,
  factoryManifest: `${CHAR_DST}/factory-manifest.json`,
  hashesJson: `${DIST_ROOT}/hashes.json`,
};
fs.writeFileSync(reusePath, JSON.stringify(reuseObj, null, 2) + "\n", "utf8");

fs.writeFileSync(path.join(ROOT, DIST_ROOT, "INTEGRATION.md"), `# Pacote de Staging Local — Orc Guerreiro (\`final-candidate-v10\`)

- **Status técnico:** \`TECHNICALLY_COMPLETE\`
- **Status artístico:** \`VISUAL_REVIEW_REQUIRED\` · \`PENDING_CREATOR\`
- **Escritas em \`../TacticsRPG\`:** \`0\` (integração aguarda aceite artístico do criador e autorização explícita).

## Conteúdo preparado para o teste isolado no Unity

- \`Assets/Resources/Characters/OrcWarrior/factory-manifest.json\`: manifesto unificado com \`durationsMs\` por quadro, \`groundY\`, \`unityPivotNormalized\` e \`contactEvent\`.
- Clipes desarmados \`128×128\` (\`groundY = 126\`, pivô normalizado \`[0.5, 0.015625]\`): \`Idle\`, \`Walk\`, \`Hit\`, \`Defeat\`, \`AttackUnarmed\`.
- Clipes armados compostos \`256×256\` (\`bodyOffset = [64, 64]\`, \`groundY = 190\`, pivô normalizado \`[0.5, 0.2578125]\`):
  - \`AttackSwordA\` (\`recruit-sword\`, 14f / 730 ms, contato \`F08\` @ 325 ms)
  - \`AttackSwordB\` (\`faceted-sword-b\`, 14f / 730 ms, contato \`F08\` @ 325 ms — mesmo corpo \`56/56\` quadros para validar troca de espada em jogo!)
  - \`AttackAxe\` (\`militia-axe\`, 12f / 1005 ms, contato \`F06\` @ 410 ms)

## Roteiro mínimo de integração autorizada (PlayMode isolado)

1. Copiar \`Assets/Resources/Characters/OrcWarrior/\` para \`../TacticsRPG/Assets/Resources/Characters/OrcWarrior/\` sem tocar em \`Characters/WarriorPilot/\` (Human Warrior Pilot).
2. Configurar TextureImporter dos PNGs de \`OrcWarrior\`: \`Sprite (2D and UI)\`, \`Single\`, \`PPU = 100\`, \`Filter Mode = Point (no filter)\`, \`Compression = None\`, \`Pivot = Custom\` (\`[0.5, 0.015625]\` para \`128×128\`; \`[0.5, 0.2578125]\` para \`256×256\`, mantendo os pés exatamente na mesma âncora de tile).
3. Em \`UnitVisuals.cs\` / \`UnitView.cs\`, adicionar seleção de perfil visual para \`OrcWarrior\` com suporte a \`durationsMs\` por quadro e escolha do clipe \`Attack\` pela arma equipada (\`AttackSwordA\`, \`AttackSwordB\`, \`AttackAxe\`, \`AttackUnarmed\`), mantendo \`Idle\`, \`Walk\`, \`Hit\` e \`Defeat\` sempre desarmados (\`attack-only-v1\`).
4. Executar batalha isolada em PlayMode: verificar 4 vistas diagonais + rotação de câmera \`Q/E\`, escala (\`1.15\`), alinhamento de pés no tile, troca entre \`Sword A\` e \`Sword B\`, leitura de \`Hit\` (450 ms) em velocidade real, pose final de \`Defeat\` no chão e preservação integral do \`Human Warrior Pilot\`.
`, "utf8");

console.log(`Staged ${Object.keys(hashes).length} files in ${DIST_ROOT}`);
