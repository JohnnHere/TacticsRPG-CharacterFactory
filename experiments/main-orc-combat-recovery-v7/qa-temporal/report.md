# Relatório de QA Temporal — Candidato V7 (Orc V1 / Verde Warcraft)

**Documento:** `experiments/main-orc-combat-recovery-v7/qa-temporal/report.md`  
**Manifesto Avaliado:** `characters/orc-v1/source/combat-recovery-v7/candidate28manifest.json`  
**SHA-256 do Manifesto:** `fde1fe23f2d637589b6abef6b9b946b6c4370cc8ae5f3927525fb038397b2579`  
**Página de Revisão Real:** `Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao de combate V7/index.html`  
**Navegador e Ambiente:** Chromium Headless Shell 156.0.8078.4 (Win64) via Playwright / Node.js v24.20.0  
**Data:** 30 de Outubro de 2026  
**Revisor:** Antigravity Temporal QA (Gemini 3.8 Flash High)  

---

## Sumário Executivo e Veredito

| Item | Status |
|---|---|
| **Veredito do Criador** | **`REJECTED_BY_CREATOR`** |
| **Veredito de QA Temporal** | **`ARTISTIC_ISSUES_FOUND`** (Não emitir `TEMPORAL_PASS`) |
| **Status Técnico** | `TECHNICALLY_COMPLETE` |
| **Status Artístico** | **`ARTISTIC_REVISION_REQUIRED`** |
| **Elegibilidade de Integração** | `false` (Bloqueado para runtime e `../TacticsRPG`) |

> [!CAUTION]
> **MUDANÇA DE MISSÃO E REJEIÇÃO FORMAL:**  
> O Criador inspecionou diretamente a página V7 e **REJEITOU o candidato** com três apontamentos determinantes:
> 1. **"O flash da espada FRONTAL continua"** — o criador percebe claramente clarões no golpe de espada nas vistas frontais;
> 2. **"Problemas de frame pioraram"** — sensação de instabilidade, flutter e cadência picada;
> 3. **"O ataque de costas está MENOS uniforme"** — quebra perceptiva entre `back_r` e `back_l`.
>
> Este relatório atende à prioridade TOTAL solicitada: **localizar com precisão matemática, espacial e temporal onde e por que o flash ocorre em movimento na espada frontal**, expor a assimetria crítica do ataque traseiro e diagnosticar os problemas de frame agravados no candidato V7.

---

## 1. Sessão de Reprodução e Loops Assistidos

Todos os 8 ataques foram reproduzidos em navegador real (Chromium), monitorando as transições de estado através do loop de renderização do canvas em escala nativa (1×), câmera lenta (0,5×), escala tática reduzida (64 px) e sincronização simultânea das 4 vistas:

| Clipe | Quadros | Duração | Loops em 1× | Tempo 1× | Loops em 0,5× | Tempo 0,5× | Percepção em 1× |
|---|---|---|---|---|---|---|---|
| `front_r/Sword` | 13 | 730 ms | 4 completos | 2932 ms | 3 completos | 4387 ms | Flash agudo na pegada (F01→F02), estrobo de lâmina no golpe (F05→F07) e piscar no fim (F11→F12) |
| `front_l/Sword` | 13 | 730 ms | 4 completos | 2951 ms | 3 completos | 4391 ms | Mesmos 3 flashes de luminância; recorte da axila em F03-F04 lê como degrau duro no movimento |
| `back_r/Sword` | 12 | 950 ms | 4 completos | 3825 ms | 3 completos | 5716 ms | Flash dos bookends atenuado (Δ = 0 a -1), mas golpe mais lento e pesado que `back_l` |
| `back_l/Sword` | 15 | 860 ms | 4 completos | 3511 ms | 3 completos | 5164 ms | Cadência picada/tremida (6 quadros < 50ms); impacto ocorre antes de `back_r` (dessincronia) |
| `front_r/Axe` | 12 | 1005 ms | 4 completos | 4038 ms | 3 completos | 6042 ms | Leitura sólida de cleave; sem o estrobo agudo da espada (cabeça do machado tem massa contínua) |
| `front_l/Axe` | 12 | 1005 ms | 4 completos | 4048 ms | 3 completos | 6050 ms | Boa coerência com `front_r/Axe`; sem artefatos severos de luminância |
| `back_r/Axe` | 12 | 1320 ms | 4 completos | 5288 ms | 3 completos | 7940 ms | Postura cravada estável (groundY 190); luva fecha sobre o cabo em F03/F04/F07; cadência lenta |
| `back_l/Axe` | 15 | 1230 ms | 4 completos | 4942 ms | 3 completos | 7396 ms | 15 quadros; movimento mais agitado que `back_r`; impacto dessincronizado na visualização 4-dir |

---

## 2. Prioridade TOTAL: Localização Forense do Flash da Espada Frontal em Movimento

### 2.1 Por que o DEV Econômico não encontrou o Flash na Tarefa T3
Na entrega V7, o DEV econômico realizou um censo estático de pixels claros (`L >= 145`) isoladamente em cada quadro e comparou com a baseline V5, concluindo: *"0 pixels confirmados alterados; veredicto: nenhum artefato"*.  
Essa abordagem falhou fundamentalmente porque **flash em animação é um fenômeno temporal e cinético, não uma contagem estática de paleta**. Uma espada com pixels perfeitamente dentro da paleta legítima (`rgb(176,178,180)`) gera um flash ofuscante se 117 desses pixels surgirem em 35 ms e sumirem 35 ms depois, ou se saltarem 60 pixels de distância sem interpolação.

---

### 2.2 Os Três Focos de Flash no Golpe da Espada Frontal

Nossa perícia temporal pixel-a-pixel revelou com exatidão onde o flash se manifesta na reprodução contínua da espada frontal (`front_r` e `front_l`):

```
ESTRUTURA TEMPORAL DE LUMINÂNCIA (front_r/Sword):
F00 (30ms) : 161 px claros (repouso)
F01 (65ms) : 144 px claros (preparação desarmada)
F02 (35ms) : 255 px claros  <=== [FOCO 1: FLASH DA PEGADA (+111 px em 35 ms)]
F03 (50ms) : 168 px claros  <=== (Queda abrupta de -87 px: peito vira para sombra)
F04 (45ms) : 163 px claros
F05 (65ms) : 164 px claros (ápice atrás da cabeça, lâmina em x:85..110)
F06 (35ms) : 144 px claros  <=== [FOCO 2: FLASH DO GOLPE (Lâmina teletransporta 60 px em 35 ms)]
F07 (35ms) : 139 px claros  <=== [FOCO 2: Lâmina teletransporta mais 30 px até solo em 35 ms]
F08 (100ms): 151 px claros
F09 (55ms) : 162 px claros
F10 (80ms) : 181 px claros (espada ainda visível)
F11 (45ms) :  68 px claros  <=== [FOCO 3: ENTALHE ESCURO (-113 px: espada some do nada)]
F12 (90ms) : 161 px claros  <=== [FOCO 3: REACENDIMENTO (+93 px: couraça frontal reaparece)]
F00 (30ms) : 161 px claros
```

---

### 2.3 Detalhamento Foco a Foco

#### FOCO 1 — O Flash da Pegada (F01 → F02 → F03)
* **Localização no canvas:** Quadrante superior esquerdo/central (peito e mão da espada), `x: 65..112`, `y: 85..141` em `front_r` (`x: 143..191` em `front_l`).
* **Mecânica do defeito:** 
  1. Em F01 (65 ms), o corpo está desarmado e exibe sua iluminação frontal de guarda (144 px com `L >= 140`).
  2. Em F02 (duração de apenas **35 ms**, correspondendo a 1 único frame em ~28 FPS), a espada entra em cena pela primeira vez via contrato `visibleInterval`. A lâmina injeta **117 pixels de aço reflexivo** (`L >= 140`, até `L = 177.7`).
  3. Crucialmente: o corpo em F02 **ainda não iniciou a rotação de ataque** e mantém integralmente os 144 px de luz no peito!
  4. O total de pixels claros no quadro atinge uma explosão de **255 px** em `front_r` e **275 px** em `front_l` (+45.716 de luminância acumulada).
  5. No quadro imediatamente seguinte, F03 (50 ms), o torso rotaciona para preparar o golpe, ocultando 83 px (em `front_r`) / 113 px (em `front_l`) de metal do peito.
* **Leitura perceptiva:** Um pico isolado de hiperluminância com duração efêmera de 35 ms que surge violentamente e desaparece em 50 ms. O olho humano lê isso como um clarão/flash branco brilhante disparado no momento em que a espada é sacada.

---

#### FOCO 2 — O Flash de Estrobo no Golpe (F05 → F06 → F07)
* **Localização no canvas:** Diagonal superior até o quadrante inferior direito, `x: 111..215`, `y: 64..181` em `front_r` (`x: 39..134` em `front_l`).
* **Mecânica do defeito:**
  1. Em F05 (`apex-hold`, 65 ms), a espada está retida atrás da cabeça (`x: 85..110`, `y: 30..101`).
  2. Em F06 (`slash-release`, duração de **35 ms**!), a lâmina teletransporta subitamente **61 pixels de distância horizontal** para `x: 146..186`, `y: 64..125`. São 110 pixels de aço reflexivo (`rgb(176,178,180)`) acendendo subitamente em uma região do canvas anteriormente escura.
  3. Em F07 (`contact`, novamente **35 ms**!), a lâmina salta outros 30 pixels para baixo até `x: 146..216`, `y: 117..142`.
  4. Não existe nenhum *smear frame*, traço de desfoque de movimento (*motion trail*) ou curva de interpolação visual entre F05 e F06.
* **Leitura perceptiva:** Em velocidade normal (1×), um objeto de altíssimo contraste (aço claro L=177.7 contra a armadura escura e pele verde L=20..40) que salta 60 a 100 pixels em 35 ms **não produz a ilusão de movimento contínuo** (Princípio de Gestalt da Continuidade). O cérebro interpreta esses dois clarões isolados de 35 ms como um **flash estroboscópico de luz branca no ar** durante a descida da espada.

---

#### FOCO 3 — O Entalhe de Apagão e o Salto de Guarda (F10 → F11 → F12)
* **Localização no canvas:** Centro do peitoral e ombro direito, `x: 94..159`, `y: 87..174`.
* **Mecânica do defeito:**
  1. Em F10 (`settle-grip`, 80 ms), a espada ainda está sendo segurada (113 px de arma + 68 px de corpo = 181 px claros).
  2. Em F11 (`release-grip`, duração de **45 ms**), a arma desaparece abruptamente da tela (0 px de arma) porque o intervalo de visibilidade encerra no frame 10. A luminância total despenca para **68 px** (entalhe escuro).
  3. Em F12 (`return-to-guard`, 90 ms), a espada continua invisível, mas o corpo estala de volta para a pose estática frontal. Os reflexos metálicos da couraça frontal reaparecem instantaneamente: **salto de +93 px** em `front_r` e **+94 px** em `front_l` (subindo de 68 px para 161/173 px).
* **Leitura perceptiva:** A transição cria uma queda abrupta para o escuro por 45 ms seguida de um reascendimento explosivo de +94 pixels claros em 90 ms. Quando o clipe entra em loop contínuo (F12→F00→F01→F02), essa variação rápida de luminância atua como uma piscada de luz no final de cada golpe.

---

#### FOCO 4 — A Descontinuidade do Pixel Especular do Peitoral
* **Coordenadas exatas:** `(132, 104)` em `front_r`; `(123, 104)` em `front_l`.
* **Comportamento:**
  * F00, F01, F02: `rgb(215, 214, 213)` / `rgb(221, 220, 219)` (`L = 214.1` a `220.1`, quase branco puro).
  * F03 até F11: `rgb(20, 20, 26)` / `rgb(2, 2, 3)` (`L = 2.1` a `20.4`, sombra profunda).
  * F12: `rgb(215, 214, 213)` (`L = 214.1`).
* **Impacto:** Uma variação de **194 unidades de luminância** exatamente no centro anatômico do peitoral. Em reprodução rápida, esse ponto acende e apaga violentamente, gerando um efeito de centelha/piscar no tronco.

---

## 3. Análise da Rejeição: "O Ataque de Costas está MENOS Uniforme"

O Criador observou que a uniformidade direcional traseira foi severamente comprometida. A perícia temporal confirmou a causa técnica: **as duas câmeras traseiras foram produzidas por frentes distintas e com contratos cinéticos incompatíveis**.

| Critério | `back_r / Sword` (Refinamento V7) | `back_l / Sword` (Reconstrução Manual V7) | Consequência Perceptiva |
|---|---|---|---|
| **Contagem de Quadros** | **12 quadros** | **15 quadros** | Dessincronização completa de fases no visualizador 4-vistas |
| **Duração Total** | **950 ms** | **860 ms** | `back_l` completa o ciclo 90 ms antes de `back_r`, saindo de fase a cada repetição |
| **Padrão de Cadência** | Durações longas: `[90, 80, 80, 110, 50, 40, 40, 80, 100, 90, 90, 100]` ms | Durações curtas/flutter: `[40, 55, 35, 45, 55, 45, 70, 40, 40, 55, 90, 65, 80, 60, 85]` ms | `back_r` lê como pesado e firme; `back_l` lê como rápido, picado e nervoso |
| **Quadro e Momento de Impacto** | **Quadro F07** no tempo acumulado de **490 ms** | **Quadro F09** no tempo acumulado de **425 ms** | No player simultâneo, o golpe de `back_l` atinge o alvo 65 ms antes de `back_r`, quebrando a técnica |
| **Intervalo da Arma** | F01 a F09 (9 quadros visíveis) | F02 a F12 (11 quadros visíveis) | `back_r` já começa engatilhado em F01; `back_l` começa desarmado |
| **Metodologia de Autoria** | Ajuste local de grip e bookends sobre V6 | Reconstrução manual cel-a-cel no Aseprite (zero PixelLab) | As duas vistas parecem pertencer a dois personagens com pesos diferentes |

No machado (`back_r/Axe` vs `back_l/Axe`), a discrepância se repete: `back_r/Axe` tem 12 quadros e dura 1320 ms, enquanto `back_l/Axe` tem 15 quadros e dura 1230 ms.  
**Veredito de uniformidade:** A rejeição do criador é plenamente fundamentada. Um visualizador em 4 direções exige que as ações sejam homólogas em tempo e impacto.

---

## 4. Análise da Rejeição: "Problemas de Frame Pioraram"

1. **Flutter e Perda de Peso em `back_l`:**  
   Ao tentar resolver a elevação da arma manualmente com 15 quadros, foram introduzidos seis quadros de duração ultra-curta (`35ms`, `40ms`, `40ms`, `40ms`, `45ms`, `45ms`). Sem interpolação ou smear, essas poses estáticas rápidas causam um tremor contínuo no braço e na arma, fazendo a espada parecer leve e sem inércia.
2. **Degrau Medial na Axila de `front_l/Sword`:**  
   O reparo de 19 pixels do DEV econômico em F03 e F04 eliminou os tons de nanquim e o pixel órfão, mas preservou um corte vertical reto na coluna `x=147` ao longo de 9 linhas. Em movimento, a abertura da axila salta bruscamente de F02 para F03, chamando a atenção do olho exatamente onde o criador esperava suavidade anatômica.

---

## 5. Diretrizes e Recomendações Técnicas para o Próximo Passe (V8)

Para solucionar de forma definitiva as queixas do criador sem novos ciclos de rejeição, as seguintes correções são mandatórias:

1. **Atenuação da Entrada da Arma (F01→F02):**
   * Em F02, a espada não deve surgir em 100% de reflexo com a couraça frontal totalmente acesa.
   * A rotação corporal deve se antecipar para F02 (reduzindo os 144 px do peito para ~80 px antes do pico), ou a lâmina em F02 deve iniciar com specularidade atenuada (tom de aço médio em vez de branco L=177), eliminando o salto de +112 pixels.
2. **Smear Frame / Rastro de Lâmina no Ataque (F05→F06→F07):**
   * O salto de 61 pixels entre F05 e F06 em 35 ms precisa de um arco de movimento (*slash smear* semitransparente ou desenho de lâmina estendida conectando a ponta de F05 à lâmina de F06).
   * Aumentar ligeiramente o tempo de corte (ex.: 50 ms / 50 ms) ou conectar a trajetória geométrica para que a vista leia um corte veloz, não um teletransporte de metal.
3. **Suavização da Desaparição e Retorno à Guarda (F10→F12):**
   * Em F11, o desarmamento não pode cortar bruscamente a luz da cena para 68 px enquanto F12 salta para 161 px.
   * A pose de recuperação em F11 deve começar a transicionar o corpo de volta para a guarda, criando uma rampa de luminância suave (`181 px → 130 px → 161 px`) em vez de um entalhe de 45 ms.
4. **Equalização Estrutural das Vistas Traseiras:**
   * Unificar a contagem de quadros de `back_r` e `back_l` (definir padrão de 12 ou 13 quadros para ambos).
   * Alinhar rigidamente os tempos de impacto das 4 câmeras (ex.: impacto de espada cravado em ~450 ms em todas as direções).
   * Eliminar durações abaixo de 50 ms nas poses estáticas de `back_l`, devolvendo a sensação de massa orc.

---

## 6. Arquivos Gerados Nesta Perícia

* `experiments/main-orc-combat-recovery-v7/qa-temporal/result.json` — Veredito JSON completo com dados brutos, findings e rejeição formal.
* `experiments/main-orc-combat-recovery-v7/qa-temporal/report.md` — Este relatório técnico circunstanciado.
* `experiments/main-orc-combat-recovery-v7/qa-temporal/flash-forensics-data.json` — Censo completo de luminância quadro a quadro e matrizes de transição.
* `experiments/main-orc-combat-recovery-v7/qa-temporal/flash-forensics/` — Tiras de diagnóstico visual e mapas de diferença:
  * `front_r_sword_flash_entry_F01_F02_F03.png` e `diff_front_r_F01_to_F02_entry_spike.png`
  * `front_r_sword_flash_strike_F05_F06_F07.png` e `diff_front_r_F05_to_F06_strike_teleport.png`
  * `front_r_sword_flash_recovery_F10_F11_F12.png` e `diff_front_r_F11_to_F12_guard_snap.png`
  * Mapas homólogos gerados para `front_l`.
