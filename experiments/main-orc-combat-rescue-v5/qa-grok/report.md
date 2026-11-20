# QA independente — main-orc-combat-rescue-v5

Papel: QA independente, fallback Grok 4.7 / GitHub Copilot. A sessão GLM `76797f0a-7d99-41fc-8e1c-638dce10a345` parou sem parecer utilizável. Este arquivo não herda esse rascunho nem o parecer do diagnóstico V4.

- Manifesto: `characters/orc-v1/source/combat-rescue-v5/candidate28manifest.json`
- SHA-256 real: `00281c8608821eecb1848d187a3508eb575781cf9172f40134f1125818df4659`
- Pai: `characters/orc-v1/source/rear-reconstruction-v4/candidate28manifest.json`
- Matriz: 28 clipes / 210 quadros; 13 candidatos / 110; 15 aliases / 100
- **Veredito: `REVISIONS_REQUIRED`**
- Status artístico: **`ARTISTIC_REVISION_REQUIRED`**. Não é `READY_FOR_CREATOR_REVIEW`. Não é aprovação do criador.
- Empacotamento técnico: **PASS**. Isso não aprova a arte.
- `eligibleForIntegration`: **false**. `PENDING_CREATOR`.

## O que foi conferido

Validação própria: `node experiments/main-orc-combat-rescue-v5/validate.mjs --output experiments/main-orc-combat-rescue-v5/qa-grok/technical-validation.json` → `TECHNICAL_PASS`, 28/210/840. Inventário protegido rehasheado: 3506/3506, zero divergências. Chromium na página real, capturas em `qa-grok/browser-checks`: 21/21 funcionais. Exportação oculta do mestre nativo `back_r/Sword` bateu 8/8 PNG e as durações 90/80/90/80/100/80/100/110. Folhas e zooms em `qa-grok/evidence/`. Nenhum raster de produção foi editado.

Inspeção sequencial dos quadros nativos e dos zooms de pegada, braço, Unarmed F02/F03, Defeat e Walk. O player Chromium avançou o relógio (1× chegou ao quadro 7/8 em 1000 ms; 0,5× ao 4/8). Isso prova o player, não um olho em loop contínuo. A rejeição abaixo não usa essa ausência como motivo.

## Matriz

| Exigência | Evidência | Resultado |
|---|---|---|
| Técnica distinta de espada e machado nas 4 vistas traseiras | Nativo `back_r` Sword vs Axe difere 4373/4316/3316/4539/4724/4208/3819 px em F01–F07. `back_l` 4278–4660. Na folha, a espada varre na horizontal e o machado sobe e desce. F00 é a mesma base. | PASS só da distinção do arco do braço |
| Corpo inteiro, peso, ombro-cotovelo-punho, sem rigidez | Coluna da mão inativa idêntica a F00 nos 32 quadros (0 px). Quadril e pernas não entram no golpe. | FAIL |
| Sem truncação ou antebraço duplo | Zooms de `back_r/Sword` F03–F04, `back_l/Sword` F02–F04 e `back_l/Axe` F04: a corrente do braço de ataque continua. O deslocamento de 2–3 px do punho não abriu buraco visível. | PASS nesse defeito; não salva o peso |
| Layers-off sem arma embutida, halo ou gancho | 32 corpos traseiros vistos desarmados. 0 pixels claros >190. Sem lâmina, disco, faixa no pescoço ou gancho de ombro. Dois grãos de 4 px no alto de `back_r/Sword` F03, na coroa, não são arma. | PASS. O defeito V4 não foi reciclado |
| Retorno desarmado | F00 e F07 dos quatro ataques: 0 px de arma e de `handFront`. F07 não é cópia de F00 (3016–4691 px). | PASS desarmado; a pose não volta ao guarda |
| Dominância anatômica | Vista traseira: lado direito da tela é o braço direito do personagem. `back_r` golpeia com esse braço. `back_l` golpeia com o braço esquerdo da tela, que é a mão esquerda. O rótulo “left-handed” do DEV está anatomicamente certo. | FAIL de coerência entre vistas |
| Pegada nos 8 clipes | `grip_untinted.png`. Máscara 110–128 px, cores aço/couro/tinta, não dedos. O carimbo não liga o antebraço ao cabo. A guarda fica legível e a mão não a envolve. | FAIL |
| Corpo e tempos frontais de Sword/Axe | Body RGBA idêntico ao pai nos 13+13+12+12 quadros. Tempos e `visibleInterval` iguais. | PASS |
| Unarmed frontal F03 | F00/F01/F02/F04 idênticos ao pai. F03 difere (4219 e 4135 px) e o punho continua visível, recuado; o braço de guarda não teleporta. | PASS do defeito pedido |
| Socos traseiros próprios | Ciclos novos, não o arco da espada. A coluna da mão inativa muda (526–1116 px), não foi colada. | PASS de autoria; peso ainda curto, sem bloqueio próprio |
| Walk `back_l`, 2741 cores | F00–F03 idênticos ao pai. F04–F07 diferem 667/690/713/671 px no composto, como declarado. O recorte do braço não mostra membro da pose oposta colado. | Sem defeito de pose errada demonstrado. Flicker em loop contínuo não foi visto por olho |
| Outros Walk e Defeat frontal KEEP | Walk frontais e `back_r` são aliases. Defeat F04 está prostrado, não ajoelhado. Mãos de F02/F03 são manoplas legíveis, não borrão, no quadro parado. | KEEP sustentado na sequência parada |
| Idle, Hit, Defeat traseiro | Aliases com o mesmo caminho e o mesmo hash do pai. | PASS de proteção |
| Sem arma fora do Attack | Overlays de arma/mão com 0 px fora do intervalo e nos clipes sem ataque. | PASS estrutural. O corpo novo inspecionado também está limpo |
| Sem saque, Unity ou autoaprovação | Não há animação de sacar. Nada foi escrito no Unity. A página diz `eligibleForIntegration=false` e `PENDING_CREATOR`. | PASS |

## Achados

### QA5-01 — HIGH — pegada, 8 clipes de arma

A camada `handFront` não é uma mão. Em `front_r/Sword` F06, `front_r/Axe` F05, `front_l/Sword` F06, `back_r/Sword` F04, `back_r/Axe` F02 e F04, `back_l/Sword` F03–F04 e `back_l/Axe` F01 e F04, o carimbo de 110–128 px flutua ao lado da guarda ou do cabo. O antebraço do corpo fica noutro lugar. Não há quatro dedos, polegar na guarda nem ponte de pulso. A contagem de pixels e o toque de 1 px medido antes do zoom não provam envolvimento; o zoom desmente esse toque. A arma, quando encosta no corpo, continua sem dono.

Cores reais do carimbo, não rosa: tinta `(12,15,18)`, aço `(38,43,50)` / `(88,96,108)`, couro `(52,26,22)`. O magenta de `grip_zooms.png` é só a marcação de diagnóstico.

### QA5-02 — HIGH — rigidez do corpo traseiro armado

`clean_rear_weapon_bodies.lua` copia a coluna da mão inativa de F00: `back_r` x≤42–45, y 10–84; `back_l` x≥82–85. A medição nos PNG nativos dá 0 px de diferença nessa coluna em F01–F07 dos quatro clipes. A folha `rear_frozen_vs_f00.png` mostra esse lado parado enquanto só o braço de ataque muda. Quadril e pernas não transferem peso. Espada e machado são arcos diferentes de braço, não técnicas de corpo inteiro. Zero deslocamento não é anatomia boa.

### QA5-03 — MEDIUM — dominância

Não é confusão de lado da tela. Nas costas, a direita da imagem é a mão direita do personagem. `back_r` é destro. `back_l` é canhoto, e o texto do DEV acerta isso. As duas vistas traseiras não compartilham a mesma mão dominante. Não corrigir invertendo o rótulo de tela.

## O que não foi defeito desta versão

Não reencontrei a lâmina/disco de `back_l/Sword`, o gancho de ombro nem o antebraço duplo do passe anterior. O corpo frontal aprovado de Sword/Axe foi preservado byte a byte; o problema frontal novo é só a pegada por cima. Unarmed F03 não perde o punho. Defeat frontal permanece prostrado. Aliases protegidos não mudaram.

## Limites

Não assisti um loop contínuo a 1× como jogador. A leitura é quadro a quadro, em zoom, mais o player funcional. Isso não é o motivo da revisão. Não reexportei os 52 mestres; o validador leu cabeçalho e tempo de todos, e um mestre nativo foi reexportado e coincidiu. O estudo especialista de uma pose continua fora desta matriz.

Empacotamento técnico: PASS. Tarefa artística de resgate de combate: FAIL. `REVISIONS_REQUIRED`.

## Adendo — pegada representativa `front_r/Sword`, 2026-10-29

Escopo estreito. A matriz global não foi rejulgada e continua **`REVISIONS_REQUIRED`**. O clip rejeitado `combat/front_r/Sword/clip.json` não foi usado como arte nova. O contrato lido é `combat/qa5-repair1/front_r/Sword/clip.json`, SHA-256 `27b7574ec8dd188a4cdb6813765b9704ef3cbb889a5640aaba0f4764fe4947e0`. Hashes declarados conferem. Corpo idêntico ao frontal preservado nos 13 quadros. Tempos 730 ms iguais. Arma e mão vazias fora de F02–F10.

**Não propagar.** `representativeAcceptableForPropagation: false`.

QA5-01 permanece. Em F06 a espada atravessa o peito e o punho do corpo fica embaixo; o `handFront` (87 px) é um carimbo ciano no punho da arma, sem ponte até o antebraço e sem cabo dentro da palma. O mesmo carimbo solto aparece em F02, F04, F07, F08 e F10. A guarda continua visível, mas isso não é pegada. A alegação de quatro dedos no script não se lê na imagem. Evidência: `qa-grok/evidence/repair1_f06_wide.png`.

## Adendo — corpo representativo `back_r/Axe`, 2026-10-29

Escopo estreito: só o corpo layers-off de `combat/qa5-repair1/back_r/Axe`. A pegada provisória não foi julgada e não entra neste parecer. A matriz global não foi rejulgada e continua **`REVISIONS_REQUIRED`**.

Clip lido: `characters/orc-v1/source/combat-rescue-v5/combat/qa5-repair1/back_r/Axe/clip.json`. SHA-256 real `ae5ecf1c313e8bebfde96bf8dd687ced4f10699cf075b1e2508c1dd723cf269e`, igual ao checkpoint. Hashes de body/native/master e dos 8 PNG de `layers/body` conferem. O nativo 128 é o recorte 64,64 do corpo 256. F00 e F07 têm overlays de arma e mão com 0 px.

**Não propagar o método corporal.** `REVISIONS_REQUIRED`. `representativeBodyAcceptableForPropagation: false`.

O que o corpo acerta, e não deve ser desfeito: não há colagem da coluna de F00. O braço esquerdo da tela sai em F01–F03 e volta. O quadril e a saia mudam de apoio; F01–F03 estreitam a base e F04 reabre. A cadeia do braço direito (ombro, cotovelo, punho) continua nos 8 quadros, sem antebraço duplo, truncação ou gancho. 0 pixels claros >190. Sem machado, haste ou disco no corpo. A mão que golpeia é a direita anatômica. F05–F06–F07 voltam a um guarda de braços baixos; F07 não é cópia de F00 (5208 px), mas a pose é guarda. Identidade traseira V1 permanece: couro cabeludo verde, sem rosto, placa dorsal.

QA5-02R — HIGH — a técnica não é overhead pesado. Em `layers/body/01.png` e `02.png` o punho fica ao lado da orelha. Em F02 a borda da manopla chega a y=67 e o topo do couro cabeludo está em y=69: 2 px laterais, não uma mão acima da coroa. `03.png` estende o braço na horizontal, à altura da cabeça. `04.png` deixa o braço aberto à direita, na cintura, com o tronco ereto. Os rótulos `overhead-hoist`, `overhead-apex`, `cleave-drop` e `heavy-impact` não descrevem esses pixels. Propagar isto repetiria um corte lateral, não um machado overhead.

QA5-02R — MEDIUM — o peso do golpe não se lê. O contrapeso do braço inativo é real. O ombro de ataque não desce e o tronco não afunda no impacto. Diferença de pixels no quadril não substitui essa leitura.

Evidência própria: `qa-grok/evidence/axe_body_layers_off.png`, `axe_body_arm_zoom.png`, `axe_body_lower.png`, `axe_body_recovery.png`. Inspeção quadro a quadro, não um loop contínuo a 1×. O overhead falha no quadro parado; essa ausência de playback não é o motivo. O recibo do job `f0235167-519c-4994-86a2-1260b0e3a23e` ainda diz `processing` e 7 quadros; o clip tem 8. O saldo 1382.70 está no recibo. Isso não altera o parecer do corpo. A pegada frontal em que Sol trabalha não foi revista.

## Adendo — chave `front_r/Sword` F06, especialista Sol, 2026-10-29

Escopo: um quadro, 35 ms, origem F06. Não é ataque de um quadro e não rejulga a matriz. O veredito global continua **`REVISIONS_REQUIRED`**. Não aprova as 8 pegadas.

Contrato: `grip-specialist/F06/representative.json`, SHA-256 real `e9daacf07836ade4d66cd58a1cc97ffa25733001f535a50f9053ecbf2742ac1e`. Hashes declarados conferem. Corpo idêntico ao pai `qa5-repair1` F06, 0 px RGBA. Alfa-over das quatro camadas bate com o composto. O nativo 128 é o recorte 64,64 e não corta a lâmina.

**Anatomia, traçada no corpo sem arma, não herdada.** Há dois braços. O braço que cruza o peito sai do ombro esquerdo da tela, que é o direito do personagem, passa em aço por `(128,110)` e `(139,112)`, e termina na luva marrom. `(155,114)` é couro `(35,19,25)`. `(157,112)` também é couro: o primeiro passe já estava na luva. `(142,115)` é aço `(20,20,26)`, na braçadeira, não na palma. A mão baixa `(156,142)` é o punho do outro braço, vertical, ao lado do quadril. O parecer anterior errou ao tratar esse punho baixo como a mão do golpe. A leitura de Sol confirma-se nos pixels.

**`READY_FOR_F02_F08_AND_FULL_CLIP_EXPLORATION`.** Só este quadro, só este clipe, para explorar o mesmo método. Não é propagação.

No composto sem tinta, em 128 e no recorte 16×: a luva cobre o cabo. 69 dos 79 px de `weaponBack` ficam sob o corpo; os 10 visíveis são a borda do cabo em y=107–112, não um fragmento solto. A guarda fica fora da mão, legível. O pomo é o metal claro em `(149–152, 118–119)`, no eixo da lâmina, acima do cinto e separado do punho inativo. A lâmina sai para cima/direita, sem atravessar o peito. `handFront` tem 33 px, todos sobre a luva existente; nove são retoque interno. Não é carimbo flutuante. O fechamento é a oclusão da luva sobre o cabo, não dedos contados. Em 128 isso lê como pegada.

Limite para os quadros seguintes: traçar de novo o braço de cada pose. Não reutilizar `(155,114)` como soquete fixo. Não voltar a pegar o punho do quadril. Evidência: `qa-grok/evidence/sol_f06_native128_4x.png`, `sol_f06_hilt_16x.png`, `sol_f06_body_arms.png`.
