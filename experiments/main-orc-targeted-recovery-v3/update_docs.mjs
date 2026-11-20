import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();

// 1. Update docs/MAIN_ORC_COMBAT_POLISH.md
{
  const filePath = path.join(ROOT, 'docs/MAIN_ORC_COMBAT_POLISH.md');
  let content = fs.readFileSync(filePath, 'utf8');
  
  const marker = '## Candidato atual — 2026-10-26';
  const idx = content.indexOf(marker);
  if (idx !== -1) {
    const headerPrefix = `> Atualização de integração — 27/10/2026: Passe de recuperação direcionada \`main-orc-targeted-recovery-v3\` executado pelo Sole DEV. Matriz atual: 12 candidatos ativos e 16 aliases inalterados. Todos os 10 apontamentos visuais do Criador foram corrigidos localmente em Aseprite (0 gerações de IA consumidas; saldo de contabilidade inalterado em 17 jobs / 78 gerações consumidas historicamente). Suíte completa de testes: 50/50 PASS, 20/20 Chromium headless browser checks PASS. O pacote permanece em status estrito de \`VISUAL_REVIEW_REQUIRED\` (\`PENDING_CREATOR\`) aguardando avaliação artística visual do criador no estúdio de revisão local. Nenhuma escrita no Unity (\`../TacticsRPG\`).

# Biblioteca de animações do Orc principal — revisão atual e histórico

## Candidato atual — 2026-10-27 (\`main-orc-targeted-recovery-v3\`)

\`main-orc-targeted-recovery-v3\` é o candidato atual de recuperação direcionada do **Orc V1 / Verde Warcraft**, resolvendo cirurgicamente todas as 10 constatações levantadas pelo criador:
1. **Espada traseira (\`back_r\`/\`back_l\` Sword):** arco de corte contínuo e natural (0° -> 325° -> 350° -> 15° -> 60° -> 100° -> 135° -> 0°), eliminando reversões erráticas e saltos de 220°; empunhadura autêntica de luva dobrada envolvendo a haste com contorno escuro em INK; eliminação total de halos e bordas claras via contorno perimetral protetor (0 pixels com luma >= 200 expostos à transparência).
2. **Machado traseiro (\`back_r\`/\`back_l\` Axe):** arco overhead pesado contínuo (0° -> 315° -> 345° -> 15° -> 65° -> 110° -> 140° -> 0°), pegada reforçada e firme com luva fechada em profundidade e 0 artefatos de borda clara.
3. **Desarmado traseiro esquerdo (\`back_l\` Unarmed):** reconstruído integralmente a partir do corpo autêntico NO, eliminando todos os resíduos de quadros obsoletos de repintura frontal de \`complete-v1\`, atingindo delta suave de 0,89%.
4. **Desarmado traseiro direito (\`back_r\` Unarmed):** punho de ataque restaurado no quadro 03 em desaceleração natural (x=182, após impacto em x=186), eliminando o desaparecimento temporário do punho no follow-through.
5. **Desarmado frontal (\`front_r\`/\`front_l\` Unarmed):** braço contralateral em guarda restaurado nos quadros 02 e 03 a partir do quadro 01 de preparação, eliminando a amputação acidental de mais de 1000 pixels da silhueta durante o clímax do golpe.
6. **Caminhada traseira (\`back_r\`/\`back_l\` Walk):** contorno do braço esquerdo estabilizado no Aseprite, eliminando cintilação e ruído temporal de borda.
7. **Derrota frontal (\`front_r\`/\`front_l\` Defeat):** torso rebaixado progressivamente até y=136 com altura terminal rebaixada de 66 px para 55 px (proporção 2,18, groundY=190 ancorado), eliminando a impressão de apoio sobre joelhos/quatro apoios e comunicando colapso e incapacitação reais com volume 3D total preservado no chão (sem rotação 2D global ou vScale).
8. **Espada frontal esquerda (\`front_l\` Sword):** remoção de pixel isolado e resíduos de recorte na axila do braço de ataque (F01-F03).
9. **Caminhada frontal (\`front\` Walk):** sombreamento excessivo na virilha/tecido atenuado no quadro 8 para tons médios/sombra.
10. **Padrão de empunhadura e contorno:** conformidade rigorosa com \`curled-glove-grip-standard\` e \`weapon-perimeter-outline-no-bright-edges\`.

[Abrir a revisão completa](../Biblioteca%20de%20Arte/Estudos%20Comparativos/Orc%20principal%20-%20Recuperacao%20traseira/index.html) · [manifesto canônico](../characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json) · [experimento de recuperação v3](../experiments/main-orc-targeted-recovery-v3/).

Clipes protegidos preservados byte a byte: todas as 4 direções de \`Idle\`, todas as 4 direções de \`Hit\`, \`front_r/Sword\`, \`front_r/Axe\`, \`front_l/Axe\`, e \`Defeat\` traseiro (\`back_r\`/\`back_l\`).
Contabilidade final: 17 jobs / 78 gerações de IA consumidas (0 novas gerações consumidas neste passe; todo o reparo foi 100% autoral local via Aseprite Lua). Status: \`VISUAL_REVIEW_REQUIRED\`, \`PENDING_CREATOR\`.

## Candidato anterior — 2026-10-26 (\`main-orc-rear-recovery-v2\`)`;
    content = headerPrefix + '\n\n' + content.slice(idx + marker.length).trimStart();
    fs.writeFileSync(filePath, content, 'utf8');
    console.log('Updated docs/MAIN_ORC_COMBAT_POLISH.md');
  }
}

// 2. Update handoff/AGENT_CONTEXT.md
{
  const filePath = path.join(ROOT, 'handoff/AGENT_CONTEXT.md');
  let content = fs.readFileSync(filePath, 'utf8');
  
  const topNotice = `> Atualização de integração — 27/10/2026: Passe de recuperação direcionada \`main-orc-targeted-recovery-v3\` executado pelo Sole DEV. Matriz atual: 12 candidatos ativos e 16 aliases inalterados. Todos os 10 apontamentos visuais do Criador foram corrigidos localmente em Aseprite (0 gerações de IA consumidas; saldo de contabilidade inalterado em 17 jobs / 78 gerações consumidas historicamente). Suíte completa de testes: 50/50 PASS, 20/20 Chromium headless browser checks PASS. O pacote permanece em status estrito de \`VISUAL_REVIEW_REQUIRED\` (\`PENDING_CREATOR\`) aguardando avaliação artística visual do criador no estúdio de revisão local. Nenhuma escrita no Unity (\`../TacticsRPG\`).`;

  // Replace top notice up to first ##
  const firstHash = content.indexOf('## Portões artísticos');
  if (firstHash !== -1) {
    content = topNotice + '\n\n' + content.slice(firstHash);
    fs.writeFileSync(filePath, content, 'utf8');
    console.log('Updated handoff/AGENT_CONTEXT.md');
  }
}
