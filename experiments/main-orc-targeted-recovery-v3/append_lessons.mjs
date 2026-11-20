import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const filePath = path.join(ROOT, 'handoff/AGENT_CONTEXT.md');
let content = fs.readFileSync(filePath, 'utf8');

const targetStr = `17. \`surgical-same-view-donor-repair\`: Ao reparar membros cortados ou deformados pela IA (ex: punho cortado em AxeL), priorizar doadores da mesma vista e mesmo indivíduo (ex: braço/mão de \`back_l/Sword\` em Aseprite Lua), preservando perspectiva, torso e armadura, e removendo resíduos (ex: 27 px de braço antigo e restos de cabo marrom) com máscaras de coordenadas exatas.`;

const additions = `
18. \`bright-edge-artifacts-and-perimeter-outline\`: Rotação por reamostragem discreta de sprites metálicos expõe realces especulares brilhantes (\`luma >= 200\`) diretamente contra a transparência; aplicar contorno perimetral protetor (\`INK\` \`rgba(12,15,18,255)\`) em pixels expostos ao ar.
19. \`curled-glove-depth-and-grip-standard\`: Manopla de oclusão frontal (\`handFront\`) deve ter dedos visivelmente curvados sobre a haste, polegar de travamento e encaixe de profundidade, superando recortes retangulares planos de pixels.
20. \`strike-cycle-opposite-limb-preservation\`: O membro contralateral em guarda não pode desaparecer durante o impacto ou retorno do golpe (preservação contínua da massa do corpo em combate).
21. \`rear-strike-continuous-kinematics\`: Manter continuidade cinemática do punho no follow-through (desaceleração contínua sem desaparecimento) e reconstrução traseira com base autêntica (proibido misturar poses frontais antigas).
22. \`incapacitated-ground-collapse-vs-kneeling\`: A pose terminal de derrota deve rebaixar o centro de massa do torso para o nível do solo (\`height <= 58 px\`, aspecto >= 2.0), evitando postura de quatro apoios ou ajoelhamento heróico, com volume 3D total no solo sem rotação 2D global ou achatamento artificial (\`vScale\`).`;

if (content.includes(targetStr)) {
  content = content.replace(targetStr, targetStr + additions);
  fs.writeFileSync(filePath, content, 'utf8');
  console.log('Successfully appended lessons 18-22 to handoff/AGENT_CONTEXT.md');
} else {
  console.error('Target string not found in handoff/AGENT_CONTEXT.md');
}
