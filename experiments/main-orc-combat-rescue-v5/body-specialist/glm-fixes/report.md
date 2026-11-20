# Relatório GLM Body Fixes — 2 quadros confirmados (Repair 2, dev especialista)

**Status de paragem:** `GLM_BODY_FIXES_READY`
**Empacotamento técnico:** `TECHNICALLY_COMPLETE` · **Artístico local:** `VISUAL_REVIEW_REQUIRED`
**Global (inalterado):** `ARTISTIC_REVISION_REQUIRED` · **Criador:** `PENDING_CREATOR`
**Papel:** DEV especialista de correção — sem QA, sem orquestração, **sem autoaprovação**.

## Limite visual declarado
Este DEV (GLM 5.3/Cline, contexto limpo) **não possui visão de imagem**. Nenhum PNG foi
aberto por ferramenta visual do chat; nenhuma imagem/base64 entrou no chat. Toda análise de
arte foi **textual** (Pillow lendo pixels como RGBA/hex; somente leitura da produção).
Autoria/edição/execução de arte: Aseprite 1.3.18.6 batch via Lua (perfil exclusivo
`tmp/aseprite-glm-body-fixes-profile`) e uma chamada real PixelLab MCP para re-autoria
anatômica. A inspeção visual final é exclusiva do QA independente Gemini 3.8 Flash
Antigravity (`863ae631-5582-4955-a0ef-020d51692fbb`), acionado apenas pelo Root.

## Entradas (lidas textualmente)
- QA: `qa-antigravity-flash/rear-bodies-repair1-result.json` + `rear-bodies-repair1-report.md`
  (veredito `REVISIONS_REQUIRED`; REAR-01-RESIDUAL-A/B em back_r-Sword F06; REAR-02-PERSISTENT
  2ª reprovação em back_l-Axe F02; back_l-Sword `READY_FOR_REAR_GRIPS` — **intocado**).
- Produtor anterior: `body-specialist/final-cycles/repair1/{report.md,patch-manifest.json,author-repair1.lua}`
  (o reparo rejeitado pintara um retângulo x83..92/y15..20 como "luva" e deixara a trave).

## FIX A — back_r-Sword-full F06 (REAR-01-RESIDUAL-A/B) · 100% Aseprite Lua
- 5 pixels flutuantes `(112,64)=94979c`, `(110,69),(109,70),(108,71),(107,72)=86878c` → alfa 0.
- Região QA `y88..94/x45..55`: **30 px** da família couro-vinho (`592d2b/34181e/30171c/27181d/…`)
  recoloridos para malha de aço com **doadores F07/F05 da mesma vista nas mesmas coordenadas**
  (prescrição literal do QA); faixa tasset x40..44 preservada (legítima em F05); sem filtro global.
- Resultado: diff total **35 px, 0 fora do permitido**; 0 px vinho restantes; veredito `PASS`
  (`verify-fix-a.json`): 11 frames byte-idênticos, grounds 126/190, composto = nativo@(64,64).

## FIX B — back_l-Axe-full F02 (REAR-02-PERSISTENT) · PixelLab + Aseprite
- Diagnóstico textual pré-edição: trave horizontal marrom-escuro y19 x76..90 + y20 x73..87;
  bloco x82..92/y15..20; pino x70..72/y16..18 (+ px claro `abadad`); braço real interrompido.
- **1 job real** `inpaint_image_pro_flash` (job `540302e4-2690-4282-8de5-c609f15b1142`, seed
  20261029, máscara retangular x68..100/y8..33), prompt somente anatômico (sem vocabulário de
  armas, nem negativo): braço direito em elevação, punho fechado vazio, pescoço/trapézio limpos.
- Composição no Aseprite (Lua): F02 final = original **fora** da máscara + resultado **dentro**.
- Validação textual (`validate-fix-b.json`, `verify-fix-b.json` → `PASS`): delta **510 px, 0 fora
  da máscara**; **0 runs de trave** ≥8px; componente do braço **673 px (x62..101/y10..37)
  conectando ombro→zona do punho**; punho/luva marrom **15 px em x83..91/y16..20** (altura de
  face, entre F01 mão-no-quadril e F03 punho-erguido); pino 9/15 e bloco 57/60 px alterados;
  y≥40 idêntico ao original; 5 cores novas, todas da família escura/pele; 11 frames
  byte-idênticos; grounds 126/190; composto exato. **Proveniência: imagem editada por IA
  condicionada e retocada/composta no Aseprite — não é desenho manual do zero.**

## Preservação e imutabilidade
- Chaves F03/F04/F07 nos 2 ciclos: SHA-256 **idênticos** aos aceitos pelo QA (assert executado
  contra `repair1/clip.json` em runtime — elimina erro de digitação; ver `make_clips.py`).
- Todos os 11 frames não-reparados por ciclo: **byte-idênticos** aos de repair1 (file-copy;
  recodificação Aseprite causaria divergência de bytes nas chaves, identificado e corrigido).
- `back_l-Sword-full` (aprovado `READY_FOR_REAR_GRIPS`): **intocado**, fora de escopo.
- Mestres reabertos e verificados (12f, camada `body`, durações ms exatas, cels (0,0)/(64,64)):
  `aseprite-verify-masters-result.json` — 4/4 OK.

## Entregáveis
- Ciclos (mestres 128/256 + frames + strips + clip.json + representative.json + review.html):
  `characters/orc-v1/source/combat-rescue-v5/body-specialist/glm-fixes/{back_r-Sword-full,back_l-Axe-full}/`
  (espelho em `experiments/main-orc-combat-rescue-v5/body-specialist/glm-fixes/…`).
- `patch-manifest.json` (clipSha256 Sword `aba36d66…`, Axe `d87cd833…`) · `hashes-summary.json`
  · `review.html` principal + comparações `glm-*-before-after.png` (layout Pillow).
- Evidências: `analysis/frames-analysis.txt`, `verify-fix-a.json`, `validate-fix-b.json`,
  `verify-fix-b.json`, recibos PixelLab (`pixellab-*-f02-*.json`, `pixellab-balance-*.json`).

## Contabilidade PixelLab (custo LLM não informado)
- Antes: **1342.70** (recibo) → job inpaint **6.0** → depois: **1336.70** (recibo conferido).
- 1 job, 1 imagem 128×128. Zero compras/assinaturas/instalações. Sem novas gerações autorizadas.

## Escopo e paragem
Escritas SOMENTE em `glm-fixes/` (characters+experiments) e `tmp/aseprite-glm-body-fixes-profile/`.
Sem Unity, sem commits, sem promoção, sem outros agentes, sem refatorar tools/compor armas.
**PAREI após os 2 reparos (A e B), conforme limite.** Nenhum bloqueio de quota/ferramenta.
