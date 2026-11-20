import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const filePath = path.join(ROOT, 'handoff/AGENT_CONTEXT.md');
let content = fs.readFileSync(filePath, 'utf8');

const targetStateBlockStart = '**Estado real de recuperação Wave 2';
const targetStateBlockEnd = 'As 12 lições semânticas obrigatórias';

const newStateBlock = `**Estado de recuperação direcionada Wave 3 (Passe main-orc-targeted-recovery-v3, 2026-10-27):**
- **Papéis ativos:** Sole DEV atual é o agente Antigravity (execução integral do brief de recuperação direcionada no workspace local). Histórico: Sole Art Producer \`b8ca8bb5\` encerrou reparos iniciais; Preview Owner GLM (\`8591\`); QA Independente histórico GPT Sol6.1 Copilot. DEV é proprietário exclusivo da engenharia de recuperação, diagnósticos, scripts Aseprite Lua, manifests, reviews e documentação;
- **Veredito e Status Atual:** O pacote atinge **\`TECHNICALLY_COMPLETE\`** e avança para **\`VISUAL_REVIEW_REQUIRED\`** (\`PENDING_CREATOR\`), aguardando avaliação artística direta do criador no estúdio comparativo. Testes automatizados: 50/50 PASS; Chromium headless checks: 20/20 PASS;
- **Resolução cirúrgica dos 10 apontamentos do Criador:**
  1. \`back_r\`/\`back_l\` Sword: arcos de corte contínuos e progressivos (0° -> 325° -> 350° -> 15° -> 60° -> 100° -> 135° -> 0°), grip autêntico de luva dobrada contornado em INK, eliminação total de halos/bordas claras (0 pixels com luma >= 200 expostos);
  2. \`back_r\`/\`back_l\` Axe: arcos overhead contínuos e pesados (0° -> 315° -> 345° -> 15° -> 65° -> 110° -> 140° -> 0°), grip reforçado com luva fechada em profundidade e zero artefatos perimetrais;
  3. \`back_l\` Unarmed: reconstruído integralmente a partir da base NO autêntica, eliminando frames frontais repintados obsoletos de \`complete-v1\` (delta suave de 0,89%);
  4. \`back_r\` Unarmed: restauração do punho em desaceleração no F03 (x=182 descendo de x=186 no impacto), eliminando o desaparecimento transitório do punho;
  5. \`front_r\`/\`front_l\` Unarmed: restauração do braço contralateral de guarda nos quadros 02 e 03 a partir do quadro 01 de preparação (recuperação de mais de 1000 pixels da silhueta em cada direção);
  6. \`back_r\`/\`back_l\` Walk: estabilização do contorno do braço esquerdo no Aseprite, eliminando cintilação/ruído temporal;
  7. \`front_r\`/\`front_l\` Defeat: rebaixamento do torso superior no colapso terminal (altura 55px, y=136, aspecto 2,18, groundY=190 ancorado), eliminando a leitura de ajoelhamento e mantendo volume 3D total no solo sem rotação 2D global ou vScale;
  8. \`front_l\` Sword: remoção de pixel isolado e resíduos de recorte na axila do braço de ataque (F01-F03);
  9. \`front\` Walk: sombreamento atenuado na virilha/tecido no quadro 8;
  10. Padrão de empunhadura e contorno perimetral: conformidade com \`curled-glove-grip-standard\` e \`weapon-perimeter-outline-no-bright-edges\`;
- **Contabilidade rigorosa preservada (17 jobs, 78 gerações consumidas):** Exatamente 0 chamadas de IA pagas consumidas neste passe. Total histórico inalterado em 17 jobs / 78 gerações consumidas. Todo o reparo foi 100% autoral local via Aseprite Lua;
- **Preservação comprovada:** 16 aliases baseline byte-idênticos preservados integralmente: todos os 4 clipes de \`Idle\`, todos os 4 clipes de \`Hit\`, \`front_r/Sword\`, \`front_r/Axe\`, \`front_l/Axe\` e \`Defeat\` traseiro (\`back_r\`/\`back_l\`);
- **Matriz canônica e cobertura local:** 28 clipes no manifesto canônico \`candidate28manifest.json\` com 12 candidatos ativos (\`ACTIVE_CANDIDATE\`) e 16 pseudônimos protegidos (\`UNCHANGED_ALIAS\`). Cobertura local de 210 quadros compostos no total: 78 quadros nos 12 clipes alvo e 132 quadros nos 16 pseudônimos da baseline protegida. 28 mestres ativos declarados e verificados;
- **Visualizador / Preview:** Atualizado em \`Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/index.html\` cobrindo todos os 28 clipes com seções antes/depois completas;
- **Status geral:** \`TECHNICALLY_COMPLETE\` para o pacote local; \`VISUAL_REVIEW_REQUIRED\`; \`PENDING_CREATOR\`. \`runtimeImplemented: false\`; nenhuma escrita em \`../TacticsRPG\`. Orc V4 permanece descartado.

`;

const startIdx = content.indexOf(targetStateBlockStart);
const endIdx = content.indexOf(targetStateBlockEnd);

if (startIdx !== -1 && endIdx !== -1) {
  content = content.slice(0, startIdx) + newStateBlock + content.slice(endIdx);
  fs.writeFileSync(filePath, content, 'utf8');
  console.log('Successfully updated handoff/AGENT_CONTEXT.md state block');
} else {
  console.error('Could not find markers in handoff/AGENT_CONTEXT.md', { startIdx, endIdx });
}
