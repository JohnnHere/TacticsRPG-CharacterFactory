# Experimento 01 — Skeleton-first, Sword `back_l`

Status: **protótipo de motion design entregue, com uma geração paga de validação.**
Aprovação artística: `PENDING_CREATOR`. Nada foi promovido, nada foi commitado.

Página de revisão: `experiments/main-orc-skeleton-first-01/index.html`

---

## 1. Fontes vigentes confirmadas

| Item | Fonte lida |
|---|---|
| Identidade atual | `reports/orc-production-current.json`, `characters/orc-v1/character.json` — Orc V1 / Verde Warcraft |
| Corpo da vista `back_l` | `characters/orc-v1/source/complete-v1/back_l/Idle/*.png` (128×128, `groundY` 126) |
| Quadro de referência do ataque | `characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/frames/02.png` (256×256, `establish-grip`) |
| Arma | `characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/recruit-sword.png` + `weapon.json` (96×96, grip em `48,66`, `hands: 1`, `hand: right`) |
| Timing vigente | `combat-recovery-v8/rear-arc/back_l-sword/clip.json` — 14 f / 730 ms, contato em F08 / 325 ms |
| Tentativas reprovadas | `combat-recovery-v7/rear-alt/back_l-sword`, `combat-recovery-v8/rear/back_l-sword`, `combat-recovery-v8/rear-inbetween/back_l-sword` |

Medição própria do quadro de referência, usada para ancorar tudo: corpo de `y 72` a `y 190`,
silhueta em `x 90..182`, mão que empunha em `(175, 120)`, arma subindo de `y 134` até `y 66`.

## 2. Técnica pretendida

Corte diagonal de cima para baixo, a mesma das vistas frontais aceitas: a arma sobe acima e atrás
da cabeça, desce num arco contínuo, contata, segue adiante e recolhe. O que se transplantou foi a
*ordem das articulações* — ombro inicia, cotovelo segue, quadril gira depois, peso vai para a perna
da frente — e não coordenadas.

Confirmação empírica de lateralidade, resolvida pela própria arte: a espada é da mão direita por
contrato, e em `back_l` ela aparece à direita da imagem com a mão em `x 0,680`. Portanto nesta vista
o lado direito do personagem **coincide** com a direita do observador, e o aviso contrário que eu
havia dado ao DEV estava errado.

## 3. As cinco poses

`poses-fixed.json`, espaço 256×256, chão em `0,7422`.

| Pose | Punho direito | Ombro | Quadril | Tornozelo |
|---|---|---|---|---|
| `ready` | (0,680; 0,477) | (0,586; 0,398) | (0,570; 0,586) | (0,574; 0,719) |
| `raise` | (0,570; 0,281) | (0,598; 0,402) | (0,578; 0,590) | (0,574; 0,719) |
| `strike` | (0,578; 0,508) | (0,551; 0,395) | (0,551; 0,590) | (0,586; 0,703) |
| `follow` | (0,578; 0,539) | (0,543; 0,398) | (0,547; 0,594) | (0,590; 0,699) |
| `recover` | (0,625; 0,551) | (0,586; 0,406) | (0,570; 0,586) | (0,574; 0,719) |

Estabilidade de membros entre as cinco poses, medida: úmero direito 3,9%, antebraço direito 3,6%,
úmero esquerdo 8,2%, antebraço esquerdo 0,4%, coxa direita 3,6%, canela direita 4,8%, coxa esquerda
4,2%, canela esquerda 0,5%. Todos abaixo do limite de 12%.

## 4. O preview

Três artefatos, todos sem edição de pixel:

- `viewer/index.html` — visualizador interativo: esqueleto com os 18 rótulos sobreposto ao corpo,
  trilha da lâmina, linha do chão medida, play 1× e 0,5×, passo a passo, cinco poses clicáveis e
  distância da ponta por quadro. Verificado em Chromium headless.
- `generated-animation.gif` — as 14 imagens devolvidas pelo PixelLab, com as durações reais.
- `v8-reference-animation.gif` — o clipe atual, para comparar lado a lado.

## 5. PixelLab: o que existe de fato

`animate_with_skeleton_v3` existe, é beta, e o contrato completo está em
`pixellab-skeleton-findings.md`. Resumo do que importa:

- Esqueleto **COCO-18**, um por quadro, de **3 a 15 quadros**; `ARM` é o punho, `LEG` é o tornozelo.
- Exige `first_frame_keypoints` coincidentes com a imagem de referência; divergência "custa
  transparência e precisão de cor silenciosamente".
- `first_frame_url` é preferível a base64; teto de 256×256.
- Custo: 3 quadros = 2 generations; 4–14 = 3; 15 = 4. Tempo de 3 a 6 minutos.
- Saldo antes: 1259,70 generations. **Depois da chamada: 3 generations consumidos.**
- A ferramenta não expõe junta de mão, de dedo, de pé nem de arma.

## 6. Limitações observadas — o resultado do teste

A geração única foi feita com as 14 poses, direção `north-west`, referência armada, seed fixa.

**O corpo funcionou.** A progressão de postura foi respeitada, o tronco acompanhou, o quadril
participou, os pés ficaram no chão, e a identidade do orc sobreviveu à conversão.

**A arma não funcionou**, e isso é medível: pixels de metal claro por quadro foram
68, 71, 50, **15, 1, 3, 3, 5, 6, 5, 5, 5, 3**, 44. A lâmina existe como aço até F02, colapsa em
F03–F04 e passa o resto do golpe como massa cinzenta sem aresta, voltando só no último quadro.

A causa é mecânica, não de ajuste: **a arma não é uma junta do esqueleto**. O modelo redesenha cada
quadro a partir de uma única referência, e ao girar o braço ele precisa reinventar a espada — e não
consegue manter aço, aresta e proporção.

## 7. Recomendação para a próxima etapa

Não animar a arma dentro da geração generativa. O esqueleto serve para o corpo, e isso está
demonstrado. A arma deve continuar sendo o asset independente que a fábrica já tem, posicionada por
transformação rígida a partir do punho, exatamente como a política de armas da fábrica determina.
A próxima etapa deveria testar: corpo gerado por esqueleto, arma composta por cima a partir da pose
do punho, e só então avaliar se o conjunto convence.

## 8. Resumo do diff

- 64 arquivos criados, todos dentro de `experiments/main-orc-skeleton-first-01/`.
- `git status` para esse caminho: 1 entrada, a pasta nova não rastreada.
- **Nenhum arquivo em `characters/` foi criado ou modificado** durante o experimento (verificado por
  data de modificação desde o início da sessão).
- **Nenhum arquivo em `../TacticsRPG` foi tocado** (0 alterações).
- Nenhum commit.

## 9. Confirmação exigida

Não houve alteração em mestres de produção, manifestos, `assets/`, `reports/` ou arquivos do Unity.
O único efeito fora do diretório do experimento foi o consumo de **3 generations** do PixelLab,
autorizado pelo criador.

---

# Relatório de orquestração

## A. Inventário de agentes

| Papel | Provider / Modelo | Agent ID | Responsabilidade | Por que foi escolhido | Resultado |
|---|---|---|---|---|---|
| DEV — motion design | `cline-glm-api/glm-5.3` | `46139122-4e9b-4267-a1a4-bcabaa8122f6` | Cinco poses COCO-18 e sequência de 14 quadros | Regra do contrato: subtarefa complexa vai para GLM 5.3 | Entregou `poses.json`, `sequence.json` e um `measure-out.json` com as juntas reais extraídas dos clipes. Não entregou o relatório; encerrado por mim após ~2h. |
| DEV — visualizador v1 | `opencode-free/opencode/deepseek-v4.1-flash-free` | `4ff71340-4632-4dc3-af37-db4aab3326f6` | Página de revisão | Regra: subtarefa intermediária começa em modelo free | **Falhou antes de ler qualquer arquivo**: `Free usage limit reached` |
| DEV — visualizador v1b | `opencode-free/openrouter/google/gemma-4-31b-it:free` | `00ce5cd0-2b07-4c75-b7c7-cf634e1070e7` | idem | Cota separada do OpenRouter | **Falhou**: `Rate limit exceeded: free-models-per-day` |
| DEV — visualizador v2 | `cline-glm-api/glm-5.3-flash` | `2f6181e0-aa04-4844-96cf-f02c7e501261` | idem | Fallback previsto para intermediária | **Morreu** com `A foreground turn is already active`, causado por mensagem minha enviada com o turno em execução |
| DEV — visualizador v3 | `cline-glm-api/glm-5.3-flash` | `4b28108b-c92d-4d23-b0ad-48d677b281a8` | idem | Recriação limpa | Entregou `viewer/index.html`, `app.js` e ferramentas. Corrigi dois defeitos dele: diretório do experimento resolvido um nível acima e nome do campo da lâmina. Encerrado por mim. |
| Orquestrador | GitHub Copilot (esta sessão) | — | Contratos, investigação PixelLab, auditoria, correção da lâmina, chamada única, integração | — | Ver abaixo |

Totais: **5 sessões DEV**, **0 sessões QA** (a task desta etapa não previa QA independente), **5 agentes distintos**.

### Trabalho do Orquestrador, declarado

- **Investigação PixelLab direta**: `tools/list` e `get_balance` são ferramentas restritas ao
  orquestrador, não herdadas por subagentes. Nenhuma geração foi feita nesse acesso.
- **Chamada paga**: `animate_with_skeleton_v3`, uma única vez, 3 generations. Feita por mim porque
  o payload depende do contrato que eu mesmo auditei e porque o MCP não é herdado.
- **Scripts escritos por mim**: validador de payload (`build-pixellab-payload.mjs`), correção de
  lâmina (`apply-blade-fix.mjs`), montagem da requisição, download dos quadros, artefatos de
  revisão. Justificativa: são auditoria e integração, não produção artística.
- **Correção de lâmina**: apliquei a correção numérica sobre uma cópia, preservando os originais do
  DEV como evidência em `poses.json` / `sequence.json`.

## B. Resultados por frente

| Frente | DEV | Arquivos | Validação | Status |
|---|---|---|---|---|
| Motion design | GLM 5.3 | `poses.json`, `sequence.json`, `dev/measure-out.json` | comprimentos de membro ≤ 8,2%, juntas dentro da silhueta | aceito com correção |
| Correção da lâmina | Orquestrador | `poses-fixed.json`, `sequence-fixed.json`, `blade-table.md` | 14/14 pontas dentro do canvas, descida monotônica F05→F08 | aprovado |
| Visualizador | GLM 5.3 Flash | `viewer/` | Chromium headless, 5 poses clicáveis, 0 erros de página | aprovado |
| Geração de validação | PixelLab | `pixellab-frames/` (14), `pixellab-sheet.png` | metal claro medido por quadro | concluído, com falha de arma |

## C. Evidência de qualidade

Três defeitos meus, encontrados e corrigidos durante a execução:

1. **Caminho errado da referência** nas três especificações (`back_l-sword/02.png` em vez de
   `.../frames/02.png`).
2. **Tabela de grade somando 700 ms** em vez de 730, que fazia o DEV recursar a entregar.
3. **Mensagem enviada com turno ativo**, que matou um agente.

Defeitos do motion design encontrados por auditoria e corrigidos: ponta da lâmina fora do canvas no
ápice (`y = −0,019`), lâmina atravessando o chão em F09–F13 (até `y = 0,844` contra chão `0,742`) e
lâmina terminando apontando para o chão. Causa raiz medida: comprimento de lâmina 0,30 usado contra
0,2305 real, medido do cabo à ponta na arma.

## D. Custos

- PixelLab: **3 generations** (14 quadros). Saldo anterior 1259,70; nenhuma outra chamada paga.
- Nenhum custo em dólar reportado pelo provedor (`credits: $0.00`).
- Nenhuma regeneração, nenhum retry pago.

## E. Demonstração

`experiments/main-orc-skeleton-first-01/index.html` — verificado em Chromium headless, 3 imagens,
0 quebradas, 0 erros de página. Abre por `file://`.

## F. Status final

- Implementação do protótipo de motion design: **concluída**.
- Testes técnicos: **aprovados** (payload válido, paginação de limites, visualizador headless).
- QA independente: **não executado**, fora do escopo desta etapa pelo contrato da task.
- Defeitos artísticos remanescentes: **a arma não sobrevive à geração**, demonstrado com medição.
- Aprovação do criador: **pendente**.
- Integração Unity: **não aplicável**, nada foi produzido para produção.
