# Relatório QA Independente — Piloto B2 (`back_r` / Sword, Arquitetura C)

Experiência: `main-orc-hybrid-weapon-04b2`
Data da revisão: **2026-11-03**
Freeze auditado: **`3736c9dc79e5372a155dfa6a480bd085ef93b0b5e518432c5213f8b09cc49964`**

## VEREDITO: `PASS`

Statuses finais (imutáveis salvo revisão do criador):

- **Técnico:** `TECHNICALLY_COMPLETE`
- **Visual:** `VISUAL_REVIEW_REQUIRED` (decisão do criador sobre a lâmina B e o golpe)
- **Aprovação artística:** `PENDING_CREATOR`
- Apto para revisão do criador: **sim** · Runtime: **não implementado** · Promoção: **nenhuma**

Este veredito é válido **unicamente para o freeze identificado acima**. Qualquer alteração
sob `experiments/main-orc-hybrid-weapon-04b2/` invalida este resultado e exige nova revisão.

---

## 1. Método

Dois procedimentos independentes, ambos executados por este QA:

1. **Recomputação determinística** (`qa/qa-independent-verify.mjs`, resultados registrados em
   `qa/qa-independent-results.json`): leitura direta de pixels RGBA (pngjs) e hashes SHA-256
   de todos os artefatos relevantes; nenhuma lógica de `run.mjs`/`author.lua` foi reutilizada
   para produzir resultados — todas as afirmações do piloto foram rederivadas a partir das
   fontes (`characters/orc-v1/source/combat-recovery-v8/rear-arc/back_r-sword/`) e das
   variantes locais.
2. **Inspeção visual direta por este QA:** `representative-review-2x.png` (original / A / B /
   corpo isolado / arma isolada em F02, F05, F08, F11), zoom de pegada 10× em
   `grip-10x-both.png`, e o quadro de máxima complexidade de profundidade **F06** nas duas
   variantes (`full/{a,b}/composite/F06.png`), que não está no conjunto representativo.

## 2. Evidências recomputadas — 30/30 verificações verdadeiras

### 2.1 Procedência e reutilização de assets (hashes)

| Verificação | Resultado |
|---|---|
| Master Aseprite da variante A byte-idêntico ao master de fonte (`composite.aseprite`) | **sim** (`b1109f1a…`) |
| Faixa composta de A byte-idêntica à de fonte | **sim** (`49050df0…`) |
| Espada A `.png` + `.aseprite` idênticas ao Exp 04 e ao Piloto front_r | **sim** |
| Espada B `.png` + `.aseprite` idênticas ao Exp 04 e ao Piloto front_r | **sim** |
| `provenance.json` de A e B declara hashes que batem com os arquivos locais | **sim** |
| `provenance.scriptSha256` de A e B = SHA-256 do `author.lua` do Exp 04 | **sim** |

Reuso real comprovado: as duas espadas não foram regeneradas nem retocadas nesta rodada —
são os mesmos assets carregados dos experimentos anteriores, byte a byte.

### 2.2 Integridade do corpo e da mão (contrato central do piloto)

| Verificação | Resultado |
|---|---|
| `body` e `handFront` idênticos à fonte, 14 quadros × 2 variantes | **28/28 camadas, 0 px de delta** |
| Corpo isolado idêntico entre A e B (14 quadros) | **sim** |
| Composto A idêntico à fonte (14 quadros) | **0 px** |
| Camadas de arma de A idênticas à fonte (14 × 2 camadas) | **sim** |

Isto fecha a questão de contaminação: **nenhum pixel do corpo, da mão de pegada ou da
coreografia foi introduzido pela composição**. `COMPOSITION_REGRESSION = 0`.

### 2.3 Mapeamento da lâmina B

| Verificação | Resultado |
|---|---|
| Silhueta da arma alterada por B (`silhouetteDeltaAB`) | **0 px em 14/14 quadros** |
| Composto fora da lâmina diferente entre A e B (`nonWeaponCompositeDiffAB`) | **0 px em 14/14** |
| Cor de lâmina da espada A sobrevivente em B (`leftoverSwordABladeInB`) | **0 px** |
| Pixels semi-transparentes de arma em B | **0 px** (nenhum halo de matte) |
| Contagem de pixels da arma idêntica A vs B por quadro | **sim** (ex.: F02 = 706) |
| Repinturas de lâmina (somatório F02..F11) | **4735 px** = valor reportado |
| Guarda/cabo preservados (hereditários, somatório) | **2315 px** = valor reportado |

### 2.4 Timing e contrato de clip

| Verificação | Resultado |
|---|---|
| 14 quadros, 730 ms, mesma grade de durações em fonte / A / B | **sim** (30, 65, 35, 50, 45, 35, 30, 35, 35, 100, 55, 80, 45, 90) |
| Contato do golpe (`F08`) se completa em `325 ms` | **sim** |
| Quadros desarmados (`F00`, `F01`, `F12`, `F13`) sem nenhum pixel de arma | **sim** (0 px) |
| `clip.json` de A e B declara `730 ms` | **sim** |
| Estrutura Aseprite: 14 frames, camadas em ordem `weaponBack → body → weaponFront → handFront`, 4 cels por camada | **sim** (inspeção registrada em `qa/aseprite-master-inspect.json`) |

### 2.5 Validação dos pivôs declarados (`grip-pivot-fit.json`)

Nos 10 quadros armados, este QA conferiu quadro a quadro que cada `rightGrip` declarado é o
ótimo inteiro da busca contra a estimativa por centroide de transformação rígida, com desvio
máximo de **0,58 px**. Nenhum pivô precisou de ajuste — o trabalho do piloto foi validar
pivôs já declarados pela recuperação, não inventá-los.

**Observação não-bloqueante:** nos quadros de rotação alta (`F05 −14°`, `F07 83°`,
`F11 80°`), a contagem `declaredValidWeaponPixels` (680/666/685 contra 700–707) e o SAD de
cor (43k–65k) refletem arredondamento da renderização da rotação (costura de 1–2 px, ex.:
2 px em `v = 55` no `F07`, declarado no `brief-art.md`). Esse comportamento é **idêntico em A
e B** (consequência direta de `silhouetteDeltaAB = 0`) e herdado da recuperação — não é um
defeito introduzido pelo mapeamento da lâmina.

## 3. Revisão visual independente — observações

### 3.1 Satisfatórios

- **F06 (o caso mais exigente):** cabo na frente do corpo (51 px de sobreposição declarada) e
  pega de couro atrás, nas duas variantes, sem vazamento além das camadas declaradas; mão de
  pegada por cima, legível em ambas.
- **Zoom de pegada 10× (`F08`):** a marca de ancoragem coincide visualmente com o encaixe do
  punho nas duas variantes; nenhum resíduo metálico fora do lugar.
- **Conjunto representativo 2×:** a silhueta de B sobreplanta pixel a pixel a de A nos
  4 quadros; contorno escuro contínuo de 1 px, sem espessamento de contorno preto e sem halo
  claro de matte ao redor da lâmina clara de B.
- **Diferenciação de material:** a lâmina B (aço facetado claro, 4 tons frios) é claramente
  distinta da lâmina A (cinza), e ainda assim o contrato "silhueta 100% preservada" se
  mantém visualmente em todas as imagens inspecionadas.
- **Nenhuma arma ou elemento de arma aparece nos quadros desarmados** — política
  attack-only-v1 respeitada nesta direção.

### 3.2 Questões para a revisão do criador (não bloqueantes para este QA)

1. **Legibilidade da lâmina clara:** a B é intencionalmente mais clara que A, e o contraste
   com o corpo traseiro escuro (luma ~34 em F02..F11) ficou forte. Isso é decisão estética,
   não defeito técnico.
2. **Características herdadas do corpo base V8** permanecem intocadas por contrato e
   documentadas no §7 do `report.md` (luma do corpo traseiro, salto de entrada `F02 → F03`,
   escorço do antebraço direito em `F07..F09`). Este QA reitera que **nenhuma delas é
   introduzida ou agravada pela composição** (corpo e mão são byte-idênticos à fonte), mas a
   decisão artística sobre elas segue aberta ao criador.

### 3.3 Equivalente comprovado de "layers-off"

Nos quadros desarmados F00/F01/F12/F13, o corpo sem arma é medido diretamente: zero pixels
de arma nas duas variantes. Como o composto A é byte-idêntico à fonte e o delta A→B fica
100% dentro da lâmina, não existe arma pintada no corpo escondida sob camada de equipamento.

## 4. Escopo e limitações deste QA

- **Artístico:** este resultado confirma a completude técnica e a ausência de regresso
  introduzido pela composição. **Não aprova arte**: a escolha entre Espada A e Espada B no
  `back_r` e a classificação final dos defeitos herdados do corpo V8 pertencem ao criador.
- **Produção:** nada neste veredito promove `equipment-current.json`, a matriz canônica ou
  aliases. Unity não tocado. PixelLab pago nesta rodada: **zero**.
- **Guardas físicas:** os hashes confirmam os assets chave intactos. O working tree do
  repositório contém mudanças prévias de séries anteriores, fora do escopo desta revisão; o
  escopo deste QA é o diretório `experiments/main-orc-hybrid-weapon-04b2/` e a fonte que ele
  consome. O sinal `protectedFilesChanged: 0` do piloto é consistente com todos os hashes
  verificados aqui.
- **Nao avaliado aqui:** Axe Attack, `back_l` e vistas frontais (cobertos pelo Exp 04 e pelo
  Piloto front_r), comportamento no runtime e numeração de dano.
- A validação de pivôs usa o método do próprio piloto (`fit-back-r-grip.mjs`); os números em
  `grip-pivot-fit.json` foram conferidos por este QA e os 10 grips selecionados batem com os
  declarados.

## 5. Consolidação

| Pergunta do Piloto B2 | Veredito |
|---|---|
| A Arquitetura C se aplica à `back_r`? | **sim** |
| Substituição de lâmina sem tocar corpo/mão? | **sim** (0 px em ambos) |
| Pivôs declarados estão corretos? | **sim** (ótimo da busca, desvio ≤ 0,58 px) |
| Espadas reutilizadas sem regeneração? | **sim** (hashes idênticos entre 04 / 04b / 04b2) |
| Alguma regressão comprometadora? | **não** (`COMPOSITION_REGRESSION = 0`) |

Resultado final: **`PASS` (para o exato freeze `3736c9dc…`)** — o pacote fica liberado para
**revisão visual do criador** (`VISUAL_REVIEW_REQUIRED`, `PENDING_CREATOR`), sem promoção
automática.

## 6. Arquivos de evidência desta revisão

| Arquivo | Conteúdo |
|---|---|
| `qa/qa-independent-results.json` | Resultados das 30 recomputações (hashes, pixels, durações) |
| `qa/qa-independent-verify.mjs` | Script de recomputação independente (somente leitura) |
| `qa/aseprite-master-inspect.json` | Estrutura dos 3 masters (fonte, A, B) |
| `qa/qa-inspect-master.lua` | Inspeção Lua dos masters no Aseprite |
| `qa/qa-report.md` | Este relatório |
| `qa/qa-result.json` | Veredito máquina-legível |

— QA Independente do Piloto B2, 2026-11-03
