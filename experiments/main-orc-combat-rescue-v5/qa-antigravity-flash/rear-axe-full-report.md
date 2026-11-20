# Parecer de QA Independente — Ciclo Completo de 12 Quadros (`back_r/Axe`)

**Documento:** `experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/rear-axe-full-report.md`  
**JSON Estruturado:** `experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/rear-axe-full-result.json`  
**Revisor:** Gemini 3.8 Flash (QA Independente via Antigravity)  
**Data:** 29 de Outubro de 2026  
**Checkpoint Avaliado:** `REAR_AXE_FULL_READY`  
**Autor do Pacote:** `7db0e7b6-ab88-49e9-9362-a19121c8ebf5` (DEV ESPECIALISTA PEGADA)  
**Status Técnico:** `TECHNICALLY_COMPLETE`  
**Veredito do Revisor:** **`READY_FOR_MATRIX_REVIEW`**  
**Status Artístico Global:** `ARTISTIC_REVISION_REQUIRED` (*inalterado*)  
**Aprovação do Criador:** `PENDING_CREATOR`  

---

## 1. Escopo Delimitado e Contexto Operacional

Este parecer de QA independente avalia com rigor técnico e inspeção multimodal direta a propagação para os **12 quadros completos** da animação de ataque traseiro com machado (`back_r/Axe`), entregue pelo especialista de pegada após a validação prévia dos representantes `F04` e `F07`:
- **Direção e Categoria:** `back_r` / `Axe` (Machado de Milícia)
- **Extensão:** 12 quadros (`F00`..`F11`), 1100 ms no total (`[70, 80, 90, 100, 110, 50, 60, 110, 100, 100, 100, 130] ms`)
- **Intervalo Ativo de Ataque:** `visibleInterval: [2, 8]` (7 quadros armados: `F02`..`F08`)
- **Quadro Base:** Corpo base aceito `body-specialist/full-back-r-axe/` (12 quadros, status `READY_FOR_REAR_GRIPS`)

### Fronteiras Rígidas de Não-Propagação
- **Escopo Estrito:** Apenas o clipe `back_r/Axe` foi avaliado.
- **Outros Corpos Traseiros Não Incluídos:** Os três outros corpos (`back_r/Sword`, `back_l/Sword`, `back_l/Axe`) estão em reparo corporal com outro produtor e não fazem parte desta avaliação.
- **Não Promoção:** Este laudo não concede aprovação artística final, não atualiza o manifest canônico de 28 células e não autoriza escritas em `../TacticsRPG`.

---

## 2. Auditoria dos Seis Contratos Técnicos Declarados

| Contrato | Exigência | Resultado da Auditoria Independente | Status |
|---|---|---|---|
| **Contrato 1** | `bodyRgbaDelta == 0` nos 12 quadros contra `body-specialist` | Verificado byte a byte nos 12 quadros de 256×256 (`bodyMaster`) e pixel a pixel no canvas nativo de 128×128. **0 delta RGBA absoluto**. | **PASS** |
| **Contrato 2** | `F04` e `F07` byte-idênticos aos representantes aceitos | `F04` e `F07` possuem hashes SHA-256 byte-idênticos para `composite-256`, `composite-native-128`, `body-128` e para as 4 camadas (`weaponBack`, `body`, `weaponFront`, `handFront`). | **PASS** |
| **Contrato 3** | Política `attack-only-v1` e `visibleInterval: [2, 8]` | Quadros `F00`, `F01`, `F09`, `F10`, `F11` têm camadas de equipamento 100% transparentes (alfa = 0). O composto final é byte-idêntico ao corpo desarmado. | **PASS** |
| **Contrato 4** | Trajetória angular e plano de solo `groundY = 190` | Ângulos verificados: `[null, null, 305°, 318°, 330°, 15°, 75°, 120°, 105°, null, null, null]`. Em `F07`, o gume cortante atinge exatamente `y = 190` (nativo 126) em `x = 177`, coincidindo com os pés cravados em `y = 190`. Em `F08`, o machado assenta em `y = 188`, sem penetração subterrânea. | **PASS** |
| **Contrato 5** | Mestres Aseprite salvos e re-exportados | Quatro mestres canônicos salvos no executável Aseprite (batch mode) e verificados com duração e hashes exatos: `composite.aseprite` (`3ca86a16...`), `body256.aseprite` (`e4aa361c...`), `native128.aseprite` (`f789d6b9...`), `hand256.aseprite` (`a38a90db...`). | **PASS** |
| **Contrato 6** | Integridade da fonte canônica 256×256 vs Recorte 128 | O recorte no topo da lâmina em `composite-native-128.png` no quadro `F04` decorre do deslocamento `[-64, -64]` da janela de prévia nativa 128. A fonte canônica de combate 256×256 preserva a cabeça do machado 100% íntegra. | **PASS** |

---

## 3. Avaliação Artística Detalhada (Inspeção Multimodal de Pixels)

### 3.1 Anatomia da Pegada e Aplicação do Método Sol (`F02`..`F08`)
- **Envelope da Luva Genuína:** Em cada um dos 7 quadros armados, a frente da luva foi extraída dos pixels opacos reais da mão do corpo base, preservando a textura de couro e cota de malha.
- **Roteamento Tridimensional do Cabo:** A seção de empunhadura do machado (`v = 50..57` do sprite) foi roteada para `weaponBack`, enquanto o gume e a cabeça estão em `weaponFront` e o fechamento dos dedos em `handFront`. O cabo passa visualmente por dentro do punho fechado em toda a trajetória.
- **Continuidade Articular:** Não há carimbos flutuantes, descontinuidade com o antebraço ou membros cortados. A cadeia ombro-cotovelo-punho conecta-se naturalmente em todas as fases.
- **Isolamento do Braço Esquerdo:** O braço esquerdo atua estritamente como contrapeso dinâmico baixo junto ao quadril (`x ≈ 86..87, y ≈ 140..148`), com silhueta limpa e zero contato com o machado.

### 3.2 Continuidade e Dinâmica do Arco Pesado
1. **F02 — Preparação (`90 ms`, `305°`, Grip `[158, 71]`):** O cotovelo direito ergue-se lateralmente; o punho eleva o machado apontando a lâmina para trás e para cima, preparando o carregamento.
2. **F03 — Subida do Carregamento (`100 ms`, `318°`, Grip `[147, 72]`):** O braço eleva a empunhadura em rotação suave de 13°, aproximando o machado do plano vertical.
3. **F04 — Ápice Overhead (`110 ms`, `330°`, Grip `[139, 72]`):** Ponto máximo de elevação, com a cabeça do machado suspensa no espaço negativo livre sobre a nuca (`y = 24..68`), sem colisão com o crânio.
4. **F05 — Início do Desabamento (`50 ms`, `15°`, Grip `[147, 81]`):** Transição de 45° com timing curto (50 ms), imprimindo aceleração cinética explosiva logo após o ápice.
5. **F06 — Golpe Descendente / Cleave (`60 ms`, `75°`, Grip `[172, 130]`):** O cotovelo lidera a queda e o machado corta o espaço diagonal com forte sensação de massa e inércia.
6. **F07 — Impacto no Solo (`110 ms`, `120°`, Grip `[157, 146]`):** O corpo dobra-se para a frente (*body hinge*), o ombro afunda e a lâmina morde o chão na linha de contato dos pés (`y = 190`).
7. **F08 — Assentamento e Rebote (`100 ms`, `105°`, Grip `[160, 150]`):** A lâmina assenta sobre o solo (`y = 188`), sustentando o peso do golpe sem afundar na terra.

### 3.3 Retorno Neutro e Ausência de Resíduos (`F09`..`F11`)
- Nos quadros `F09` (100 ms), `F10` (100 ms) e `F11` (130 ms), a arma desaparece integralmente conforme a política `attack-only-v1`.
- A descompressão do tronco e o retorno dos braços à postura de guarda ocorrem de forma fluida, sem nenhum pixel residual, rastro de corte (*swoosh*) fantasma ou artefato de arma colado ao corpo.

### 3.4 Legibilidade em Escala Tática (64×64 e 128×128)
- A inspeção do painel `before-after-tactical.png` confirma que a silhueta em escala tática reduzida (64 px) mantém leitura imediata do ataque pesado, com diferenciação clara entre o corpo couraçado, a projeção da lâmina e o impacto no solo.

---

## 4. Tabela de Hashes SHA-256 Verificados em Disco

- **Manifesto do Clipe (`clip.json`):** `66f4b0e1e6ec60dafc493620e9beb68e5fbb42791ccd53be671a52f9e73f8c9e`
- **Tira Composta 256 (`composite-strip.png`):** `836a6f2db1038d47ce4af57c98760a4801b6f11e5bf870e6396686cdd806086a`
- **Tira Nativa 128 (`native-strip.png`):** `c18602344a993ad4cbb50a0c8853ac80d06943f3ca7d17ef2b34b8f5e9207abe`
- **Tira Nativa Composta 128 (`native-composite-strip.png`):** `d1058d5be7b4513a695b1bc5abf1ed6ca57b90515a656f335e9e531495ba7fca`

| Quadro | Fase | Duração | Ângulo | Grip `[x, y]` | SHA-256 Composto 256 | SHA-256 Nativo 128 |
|---|---|---|---|---|---|---|
| **F00** | guard | 70 ms | - | - | `245ce5ce71cebb37d30b738a941b212270a3386939e0c646642d31c62e2836d2` | `251998d6cebce682a21d8fafde620200e820ef46301c6743348e331bb47e5d8c` |
| **F01** | load-begin | 80 ms | - | - | `f18a4c458721af83e2db637c5ef08ebae42f1b2f16b27eedc2be12fdf693cc94` | `54742efc1dbebfe86541cc37c4b0699ebea2cb862b12089dd5ac8d3803a3e13e` |
| **F02** | elbow-hoist | 90 ms | 305° | `[158, 71]` | `8750320163c9c5ba440803bfce1dca5967c31c7dd7c834f2d0180e294c14867b` | `fdb8b8e332269a37f46bb970db6dd0ef3c6fc18c49fee24d160cfcb06739be36` |
| **F03** | validated-hoist | 100 ms | 318° | `[147, 72]` | `4b6a0efe08c9e0b6f932cb7776d50080c633b21ab656c0efd2d89ae57ace6dbb` | `d6fff9076b7f88ef07e382ae3daa6e97f5ec235f18fb255d6f51f1da43a580b1` |
| **F04** | validated-apex | 110 ms | 330° | `[139, 72]` | `27cab6a671d6edd68113eee1e0b9f70872e2e563466df66ad5bed7367c065a95` | `e10e4e7beda70ef734af9787f90be4cfb6321a93f551a33652fd9e7cbbc5fae3` |
| **F05** | drop-initiation | 50 ms | 15° | `[147, 81]` | `69bff313ab55c3665cfa49c7dbc270126ee4498f5d01484e82c072053548f921` | `7496de7012afc107e4194988e75663c77160f902170c85faf74e504e2f885a08` |
| **F06** | forward-down-cleave | 60 ms | 75° | `[172, 130]` | `2d9f6e9b0e8d09f3dec448ce1525b83810b002b54baea764e46c5dbef5267d42` | `471027e2ecb28804f51f0660fed8ca297ed9333bb6e33e912b7dc23361c1ee3b` |
| **F07** | validated-impact | 110 ms | 120° | `[157, 146]` | `b9b17570db0d8759edf863ca7e48b14f289bc9ae0460bdf6e2235e4ee3d34b9f` | `7b68137872bb4e08a648ba34aa155cf061d93eb301c89df52f197c98e7e176cb` |
| **F08** | recover-low | 100 ms | 105° | `[160, 150]` | `1bd82560358fbaee36dd2beba0f773da4a80a00efd0ce2aaa5c7ac24b1fbfa3e` | `c1badeef27cf492fe9071669e1c4f3315646a53988a4d621a615a2f85e16bc41` |
| **F09** | recover-pelvis | 100 ms | - | - | `fbbe93e33fd174f015d48aaa662fb93b7f9ce3d02d0a816c57dd1dba85ea5039` | `edeaaa5cd175f5fe5b07bf5620f1dff3d9c0372f15592c20614f2ffbca1c244b` |
| **F10** | recover-guard | 100 ms | - | - | `cb92432ed305d238775d5e027746c86b5c446b7b1457fa8a50cc0569bb8245db` | `b0231c677cf7c736e4923391c4d962d5e81eb6f0cd189e2e424b745105cd1077` |
| **F11** | guard-return | 130 ms | - | - | `245ce5ce71cebb37d30b738a941b212270a3386939e0c646642d31c62e2836d2` | `251998d6cebce682a21d8fafde620200e820ef46301c6743348e331bb47e5d8c` |

---

## 5. Limitações Críticas da Avaliação

1. **Distinção entre Inspeção Estática e Percepção 1× ao Vivo:**
   - Este exame baseia-se na inspeção minuciosa quadro a quadro de todas as camadas, na verificação de tiras contínuas e na análise das durações e rotações. A cadência temporal foi projetada com base nos parâmetros do player HTML (`index.html`), mas a percepção fluida a 60 fps em tempo real no motor de jogo final permanece como critério a ser apreciado no freeze de matriz completa.
2. **Escopo Delimitado:**
   - O veredito refere-se **exclusivamente** ao ciclo `back_r/Axe`. Não valida os demais três corpos traseiros que continuam sob reparo, nem antecipa a aprovação das outras armas traseiras.
3. **Aprovação do Criador Pendente:**
   - O status artístico geral da recuperação do Orc permanece estritamente `ARTISTIC_REVISION_REQUIRED`, aguardando a consolidação das demais correções e a avaliação explícita do criador.

---

## 6. Veredito Final e Próximos Passos

- **Veredito:** **`READY_FOR_MATRIX_REVIEW`**
- **Recomendação ao Root / Orquestrador:**
  - O clipe `back_r/Axe` cumpre todos os requisitos de arte, oclusão, anatomia e preservação do corpo base. Está aprovado tecnicamente e artisticamente para ser integrado na revisão conjunta de matriz quando os reparos dos outros corpos e pegadas forem concluídos.
- **Contabilidade de Recursos:**
  - Chamadas PixelLab de produção nesta revisão: **0**
  - Custo de inferência LLM: **Não informado**
  - Modificações em arte / Unity / Git: **Nenhuma**.