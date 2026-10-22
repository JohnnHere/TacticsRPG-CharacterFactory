# Human Warrior Pilot

> **Decisão preservada desde o início: Human Warrior Pilot ≠ protagonista definitivo.**
> Este personagem **não** é automaticamente o herói narrativo do jogo. Ele é o primeiro
> piloto visual do projeto, usado inicialmente como representação visual do `Hero` no sandbox.
> **Status na pipeline v1.0 (`../CHARACTER_PIPELINE.md`):** implementação de REFERÊNCIA do
> processo — protótipo reutilizável aprovado (Idle/Walk/Attack/Hit/Defeat × 4 direções);
> refinamentos artísticos em aberto (incl. mão da espada entre vistas) e regressão ampla
> ainda não executada. Pela diretriz do criador de 2026-10-19, novos personagens são
> weapon-independent; a espada embutida deste piloto é uma **exceção histórica** e permanece
> preservada sem migração. Novos personagens seguem `../CHARACTER_PIPELINE.md` +
> `CHARACTER_TEMPLATE.md`.

## Fatos aprovados

- **Identidade de trabalho:** Human Warrior Pilot.
- **Raça:** Humano.
- **Arquétipo:** guerreiro medieval corpo a corpo / espadachim.
- **Propósito:** primeiro MVP de produção visual e técnica de personagem — valida o pipeline
de arte, o fluxo de importação/integração de sprites e a leitura tática em campo
(silhueta, direção, escala).
- **Uso em protótipo:** pode representar temporariamente a unidade `Hero` existente
(unidade-chave do time 0 no mapa `Assets/Resources/Maps/Proving.asset`).
- **Status narrativo:** NÃO é automaticamente o protagonista final da história.
- **A imagem aprovada é referência de direção de arte**
(`Docs/Art/References/character_style_anchor_v1.png`), **não necessariamente um sprite
pronto para produção.** Ampliar ou reduzir arte conceitual não produz automaticamente
pixel art válida em resolução nativa.
- **Nenhuma nova raça, Job, habilidade ou cânone de protagonista é autorizado por este piloto.**
- Ocupante temporário do slot `Hero` em cenas de protótipo/sandbox.

## O que este piloto NÃO é

- **Não é o protagonista definitivo.** Protagonista será decidido em Estágio 8 (design) e
  Estágio 10 (arte final), com conceito próprio.
- **Não é um Job implementado.** O gameplay atual **ainda não implementou classes/Jobs**
  (ver `Docs/GAMEPLAY.md`). `Warrior` e `Knight` existem apenas no catálogo de design
  (`Docs/GameDesign/JOB_CATALOG.md`): `Warrior` é Job básico de dano físico; `Knight` é Job
  intermediário tanque (requisito proposto: Warrior 3 + Squire 2). Este piloto representa a
  *fantasia* do guerreiro corpo a corpo, sem acoplá-la prematuramente ao sistema de Jobs.

## Divisão de responsabilidades da documentação

| Documento | Responsabilidade |
|---|---|
| `Docs/ART_DIRECTION.md` | Identidade visual universal do jogo e imagem de referência aprovada |
| `Docs/Art/Characters/HUMAN_WARRIOR_PILOT.md` (este arquivo) | Identidade, assets, animações, limitações e status do guerreiro humano |
| `Docs/Art/CHARACTER_PIPELINE.md` | Processo de produção reutilizável para qualquer raça ou classe |
| `Docs/ROADMAP.md` | Tasks, progresso e próximos marcos de integração (Estágio 10) |
| `Docs/GAMEPLAY.md` | Apenas comportamentos efetivamente implementados e testados |

## Estados planejados de assets (registrados separadamente)

| Estado | Descrição | Status |
|---|---|---|
| Concept/reference | Imagem de direção de arte aprovada (`character_style_anchor_v1.png`) — define estilo, não template | ✅ aprovado como referência |
| Game sprite (estático) | Sprite em resolução nativa, fundo transparente, pivot e escala corretos | ✅ `warrior_pilot_mvp1_static_128.png` (128×128, alfa, PPU 100) integrado e **visualmente aprovado pelo criador** (tamanho e apresentação in-game) |
| Direções (directions) | Visualizações por direção para o billboard (4 diagonais agora + 4 cardinais futuros) | ✅ 4 vistas diagonais integradas e **aceitas na revisão PlayMode inicial** (2026-10-11); regressão completa não executada; mão da espada requer validação de arte; não são arte final |
| Idle | Animação de espera alinhada ao loop do jogo | ✅ **4 direções visualmente aprovadas (MVP 3C, 2026-10-11)**: 16 quadros (4 por vista, 0,24 s/ciclo de 0,96 s @1×), mesmo bob ≤2 px e linha do chão y=126; regressão ampla permanece não executada |
| Walk | Ciclo de caminhada alinhado ao passo tático (`StepTime` ≈ 0,22 s) | ✅ **4 direções integradas (MVP 3D, 2026-10-11)**: 24 quadros (6 por vista, 3/passo, ciclo = 2 passos = 0,44 s @1×), fase contínua pelo passo cumulativo + `t` da interpolação real; `front_r` validado no PlayMode (3B), demais vistas aguardando aprovação |
| Attack | Golpe de espada alinhado à rotina de ataque melee atual | 🔶 **integrado (MVP 4, 2026-10-11)**: 20 quadros (5×4 vistas, um shot ~0,45 s disparado em qualquer ataque, inclusive em tile vazio); aguardando aprovação visual |
| Reactions | Dano/esquiva/derrota (hoje: flash de cor e encolher até sumir) | 🔶 **Hit/Defeat integrados (MVP 4, 2026-10-11)**: Hit 12 quadros (3×4 vistas, ~0,24 s, só em golpe que ACERTA); Defeat 20 quadros (5×4 vistas, ~0,60 s, trava o visual até a view sumir); esquiva segue sem clipe (só o desvio procedural); aguardando aprovação visual |
| Integração Unity | Import, representação visual, posição no chão, sorting, sombra | 🔶 MVP 1 implementado (2026-10-10) + polimento (2026-10-11: escala ×1,15, sombra de contato, indicador no chão); revalidação PlayMode pendente |
| Validação | Leitura tática em campo (zoom-out, giros de câmera), regressão de save/load e IA | ⬜ pendente |

## Assets atuais no projeto

- `Docs/Art/References/character_style_anchor_v1.png` — âncora de estilo aprovada
  (definida em `Docs/ART_DIRECTION.md`).
- `Assets/Resources/Characters/WarriorPilot/warrior_pilot_mvp1_static_128.png` — sprite de
  teste do MVP 1 (PNG 128×128 com alfa; Sprite (2D e UI), Single, PPU 100, Point filter,
  sem compressão, sem mipmap). Movido de `Assets/Characters/WarriorPilot/` para dentro de
  `Resources` **junto com o `.meta` (GUID preservado)** para permitir carga em runtime por
  `Resources.Load<Sprite>()`, no mesmo padrão dos mapas (`Resources/Maps`).
- ~~`Assets/Characters/WarriorPilot/Animations/`~~ — verificado em 2026-10-10: a pasta **não
  existe mais** no projeto (o rascunho de Animator Controller citado anteriormente foi removido
  em trabalho anterior). Idle e direções voltam a ser produzidos nos marcos MVP 2+.

## MVP 1 — integração do sprite estático (implementado; aguardando validação PlayMode)

Implementado em 2026-10-10 (Estágio 10.2b). Visual apenas — nenhum toque no Core, nas regras,
no mapa `Proving` nem na cena.

- **Alvo seguro:** `UnitVisuals.SpriteFor` aplica o sprite apenas à unidade com `Team == 0`
  (time do jogador), `IsKey` e `Name == "Hero"` — a identidade vem do `MapData` (ex.: spawn
  `Hero` do `Proving`). Nenhuma outra unidade é afetada.
- **Carga do asset:** `Resources.Load<Sprite>("Characters/WarriorPilot/warrior_pilot_mvp1_static_128")`.
- **`UnitView`:** a raiz do boneco passou a ter escala uniforme 1 (a cápsula virou filha "Body"
  e o visual fica idêntico ao anterior); `UseSprite(sprite)` cria um filho "Sprite" com
  `SpriteRenderer`, esconde a cápsula (`Renderer.enabled = false`) e mantém o cubo "Front"
  como indicador de facing tático.
- **Câmera/orientação:** billboard cilíndrico em `LateUpdate` (só giro em Y, seguindo a câmera
  tática) — o sprite permanece visível nos 4 giros de 90° (Q/E) **sem espelhar** a arte
  (equipamento assimétrico preservado). O facing de combate (`Unit.Facing`/`SetFacing`) não é
  alterado; leitura tática continua pelo "Front".
- **Chão e escala:** a base da arte pousa no topo do tile via `sprite.bounds.min.y`
  (independente do pivot do sprite); 128 px @ PPU 100 ≈ 1,28 u nativos, aplicado o
  multiplicador de perfil visual **×1,15** (`UnitVisuals.ScaleFor`, 2026-10-11) ≈ **1,47 u**
  de canvas (~1,2 u de arte útil — leitura de herói ao lado das cápsulas de ~1 u).
  Proporções originais preservadas; os pés continuam no chão para qualquer escala.
- **Feedback existente:** flash de dano aplicado também ao sprite via `SpriteRenderer.color`
  (cor de repouso branca para não repintar a arte; paleta de time/daltonismo continua na
  cápsula escondida e nos rótulos); avanço de ataque, empurrão, desvio e o encolhimento de
  derrota (`Vanish`) funcionam na raiz e arrastam o sprite junto. Undo/knockback usam
  `Place`/`SetFacing` na raiz; o carregador interno de snapshots recria as views pelo mesmo caminho de criação (F5/F9 removidos do gameplay normal no MVP 5A.4).
- **Limitações conhecidas (aceitas no MVP 1):**
  - Um único sprite estático (sem frentes/lados/costas) — direções são o MVP 2; o billboard não
    indica facing, papel do marcador "Front".
  - Sprite unlit (padrão `SpriteRenderer`) sobre terreno URP lit; oclusão por tiles altos à
    frente é o comportamento de profundidade esperado.
  - Sombra é um disco de contato simples (transparente, sem direção de luz), não uma sombra
    projetada real.

### Polimento MVP 1 (2026-10-11)

Após a primeira passagem PlayMode do criador (integração funcional e promissora), três ajustes
de apresentação — todos apenas na Presentation, compilação validada, **revalidação PlayMode
pendente**:

- **Escala +15%:** multiplicador configurável por personagem em `UnitVisuals.ScaleFor`
  (`WarriorPilotScale = 1.15f`), aplicado com `UseSprite(sprite, scale)` mantendo os pés no
  chão. Reutilizável para perfis visuais futuros sem nova arquitetura.
- **Indicador de facing no chão:** o cubo branco "Front" (o "tile/indicador branco" visto
  perto do Hero) descia do meio do corpo para o **chão, à frente dos pés** (unidades sem
  sprite ficam exatamente como antes) — legível nos 4 giros, sem cobrir a arte.
- **Sombra de contato:** disco transparente (cacho `Sprites/Default`, α 0,35) represado no
  topo do tile mais próximo a cada quadro — fica no chão durante hop/desníveis/empurrões e
  encolhe junto no `Vanish`. Ancora a leitura do sprite no grid como as sombras reais das
  cápsulas.
- **Caminho para o MVP 2 (somente especificação, nada implementado):** estender
  `UnitVisuals` para conjuntos de sprites por direção, selecionados em `UnitView` pelo
  ângulo entre facing mundial e yaw da câmera — mapeamento, nomenclatura e plano em
  **`Docs/Art/Characters/HUMAN_WARRIOR_DIRECTIONS.md`** (fonte canônica do MVP 2).
- **Validação (estado real):** a aprovação do criador cobre **escala e apresentação visual**
  do sprite. A regressão PlayMode completa — seleção/movimento/ataque (incl. ataque em tile
  vazio), undo, save/load sem duplicação, derrota, giros Q/E nos três zooms e sombra em
  desníveis — **não foi executada/verificada** e permanece como pendência registrada.

## Identidade visual aprovada (preservar em todas as direções)

Humano masculino adulto/jovem-adulto; cabelo castanho descoberto; expressão madura e séria;
armadura de placas prateada; ornamentos dourados contidos; capa azul-marinho; couro marrom;
espada longa única de aço; proporções compactas de RPG tático; pixel art refinada e nítida.
Referência primária: `character_style_anchor_v1.png`. FFT, RPGs táticos clássicos, Warcraft e
fantasia tolkieniana são inspirações amplas de linguagem — **não** designs a copiar. Nenhuma
nova arte é gerada nem a aprovada alterada nesta fase.

## MVP 2 — direções (fechado na revisão PlayMode inicial de 2026-10-11)

Implementado em 2026-10-11 (Estágio 10.2b) com 4 sprites **candidatos de teste** — mapeamento
 canônico em `HUMAN_WARRIOR_DIRECTIONS.md` (tabela §2 corrigida na mesma data).
Visual apenas; MVP 1 preservado como fallback em cascata (direção → estático → cápsula).

- **Assets:** `Assets/Resources/Characters/WarriorPilot/Directions/warrior_pilot_dir_{front_l,front_r,back_l,back_r}.png`
  (128×128, alfa; `.meta` clonado do MVP 1: Sprite/Single/PPU 100/Point/sem compressão/sem mipmap).
- **Seleção:** `UnitView.LateUpdate` escolhe a vista pelo ângulo relativo `d = yawUnidade − yawCâmera`
  (`idx = RoundToInt((d+45)/90) & 3` — vista mais próxima; idêntica em repouso) , sempre pelo
  yaw real, trocando `SpriteRenderer.sprite` só na mudança, com pés reposicionados por vista.
  Sem espelhamento (`flipX` proibido); vista ausente cai no estático do MVP 1. Conjunto
  carregado 1× e cacheado em `UnitVisuals.DirectionsFor`.
- **Depuração:** overlay F3 mostra `[vista d=ângulo°]` sobre o Hero para conferir mapeamento.
- **Auditoria "ataca de lado" (2026-10-11, detalhes em `HUMAN_WARRIOR_DIRECTIONS.md` §8):**
  sem defeito de orientação — Facing do Core é definido antes do feedback e a vista correta já
  está no primeiro quadro do golpe; tabela das 16 combinações verificada e congelada em
  `DirectionMappingTests`. Causa da leitura "de lado": **arte estática sem pose de ataque**
  (desliza na diagonal do alvo; vistas de costas ocultam rosto/espada) — Attack animado é o
  MVP 4. Correção técnica derivada da auditoria: seleção por vista mais próxima
  (`RoundToInt((d+45)/90)`) — idêntica em repouso, correta durante o giro da câmera.
- **Achados de arte para decisão do criador:** `front_l`/`front_r` parecem poses espelhadas
  (espada troca de lado da tela → mão inconsistente) e `back_r` não mostra a espada próxima;
  escala/linha do chão medidas e consistentes (100 px / y=126 nas 4 vistas).
- **Fechamento (2026-10-11):** revisão visual PlayMode inicial do criador **aceitou as 4 vistas
  diagonais** e a seleção direcional. Permanecem **expressamente não verificadas**: a suíte
  completa no Unity Test Runner (incl. `DirectionMappingTests`) e a regressão PlayMode ampla
  (save/load, undo, derrota, zooms) — nenhuma marcada como aprovada. **Aberto em arte:**
  consistência anatômica da mão da espada (possíveis `front_l`/`front_r` espelhadas e `back_r`
  sem espada visível) exige inspeção mais próxima e decisão de regeneração antes dos frames
  do MVP 3 (ver `HUMAN_WARRIOR_ANIMATIONS.md` §7).

## Animações

- **MVP 4 (2026-10-11): Attack/Hit/Defeat integrados** — 52 quadros em
  `Animations/{Attack,Hit,Defeat}/` (5/3/5 por vista; 4 vistas), carregados pelo mesmo esquema
  de cache/sondagem dos demais e tocados como estado transitório de combate em `UnitView`
  (precedência Defeat > Hit > Attack > Walk > Idle):
  Attack dispara em qualquer ataque (inclusive em tile vazio) no momento do `SetFacing`, um
  shot de ~0,45 s; Hit dispara só quando o golpe ACERTA (~0,24 s); Defeat dispara na morte,
  trava o visual no clipe até a view ser destruída (o encolher do `Vanish` continua sobre ele;
  o resultado de gameplay não muda). Falta de quadros em uma vista → fallback imediato. Erro
  de import detectado e corrigido: os 52 metas vieram como textura default (textureType 0) —
  convertidos para Sprite/Single/PPU 100/Point com os GUIDs originais preservados.
  **Aguardando aprovação visual PlayMode do criador**.

- **MVP 3D (2026-10-11): Walk completo nas 4 direções + cubo branco removido** — 18 novos
  quadros (`walk_front_l/back_r/back_l_00..05`) descobertos automaticamente pelo carregador
  existente (**zero alterações na lógica de carga/animação**; import clonado do aprovado com
  compressão Default 0; medição: 128×128, linha do chão y=126 em todos, tops 26–30 = passo).
  O cubo branco "Front" foi **desligado nas unidades com sprite** (renderer off; GameObject,
  Facing do Core e debug F3 intactos — cápsulas mantêm o indicador como antes), a pedido do
  criador. **Aguardando aprovação visual PlayMode do criador**. Correção pós-playtest 1.14
  (2026-10-11): o disco de contato sob o Hero renderizava **magenta** (material com
  error-shader — `Shader.Find("Sprites/Default")` não resolveu neste projeto/URP); a sombra
  agora deriva o shader do próprio sprite (que renderiza corretamente) — disco preto
  translúcido, mesmo tamanho/posição.
- **MVP 3C (2026-10-11): Idle completo nas 4 direções — APROVADO** — 12 novos quadros
  (`idle_front_l/back_r/back_l_00..03`) validados e integrados **sem nenhuma alteração de
  código** (o carregador do MVP 3A já sondava as 4 vistas). Import clonado do aprovado
  (Sprite/Single/PPU 100/Point/sem compressão/sem mipmap); medição: 128×128, linha do chão
  y=126 constante, bob 25–27 (≤2 px) idêntico ao `front_r` aprovado; identidade e convenções
  de vista conferidas por amostragem (rosto nas `front_*`, capa nas `back_*`). O clock de Idle
  não reinicia ao trocar de vista (giro de câmera/facing). **Aprovado visualmente pelo criador
  após reteste PlayMode (2026-10-11)** — o incidente "respiração só em front_r" foi resolvido
  com reimport/atualização dos assets (consistente com import desatualizado/cache estático;
  causa não reproduzida em código — ver `HUMAN_WARRIOR_ANIMATIONS.md` §8/§8.1). Diagnósticos
  temporários removidos; cache de clipes endurecido (re-sonda enquanto houver direção sem
  clipe — cobre Enter Play Mode com Reload Domain desabilitado).
- **MVP 3B (2026-10-11): Walk front_r integrado** — `Animations/Walk/walk_front_r_00..05.png`
  tocam durante o `MoveAlong` real: 3 quadros/passo, ciclo = 2 passos (fase contínua pelo passo
  cumulativo, sem reiniciar no início de cada tile), avançando pelo MESMO `t` da interpolação
  (velocidade 1×/2×/4×/50× já embutida — sem multiplicação dupla). Vista sem clipe de Walk →
  estático do MVP 2. Estado do movimento é resetado em `finally` (seguro contra interrupção).
  Registro medido: linha do chão y=126 nos 6 quadros. `WalkFrameIndex` puro e testado (146
  checagens executadas, 0 falhas). Compilado sem erros; **validação PlayMode pendente**.
- **MVP 3A (2026-10-11): Idle front_r integrado** — `Animations/Idle/idle_front_r_00..03.png`
  tocam em loop (0,24 s/quadro, honrando a velocidade de animação das opções) quando o Hero
  está parado e a vista selecionada é `front_r`; qualquer outra vista usa o estático do MVP 2.
  Carga/sondagem e cache em `UnitVisuals.IdleFramesFor`; avanço e seleção em `UnitView.LateUpdate`
  (`IdleFrameIndex` puro, testado); `_moving` pausa o Idle durante `MoveAlong` (finally garante
  retomada mesmo se interrompido). Registros medidos: linha do chão y=126 nos 4 quadros, bob
  25–27 (≤2 px).
- **MVP 3 (Idle + Walk) em andamento** — especificação canônica em
  **`Docs/Art/Characters/HUMAN_WARRIOR_ANIMATIONS.md`**; Idle (3C) e Walk (3D) completos nas
  4 direções, aguardando aprovação visual do criador; Attack aguarda frames (MVP 4; feedback
  procedural atual segue operativo).

## Limitações conhecidas

- Representa **humano, 1 tile, melee** — não serve de referência para anatomias não humanas
  (ver Estágio 3.9 do roadmap: sprites por anatomia com fallback validado).
- Direção ortogonal (frente/lado/costas usados pelo combate de flanco) deve permanecer
  legível em zoom-out e nos 4 giros de câmera de 90°.
- A imagem de referência é conceitual: a conversão para sprite exige produção dedicada
  (resolução nativa, clusters de pixel, transparência — ver `Docs/Art/CHARACTER_PIPELINE.md`).
- Nenhum vínculo com o sistema de Jobs (inexistente em código até o momento).

## Status geral

| Marco | Status |
|---|---|
| Referência de estilo aprovada | ✅ |
| Documentação do piloto + pipeline (`CHARACTER_PIPELINE.md`) | ✅ |
| MVP 1 — sprite estático do guerreiro como `Hero` em `Proving` | ✅ **visualmente aceito** (escala ×1,15 e apresentação aprovadas); regressão completa permanece não verificada |
| MVP 2 — direções | ✅ **fechado** (revisão PlayMode inicial aceita, 2026-10-11; seleção testada 25/25) — ressalvas: Test Runner completo e regressão ampla não executados; mão da espada pendente de validação → `HUMAN_WARRIOR_DIRECTIONS.md` |
| Walk | ✅ **4 direções integradas (MVP 3D, 2026-10-11)**: 24 quadros (6/vista); `front_r` validado no PlayMode (3B), demais vistas aguardando aprovação |
| Attack | 🔶 **integrado (MVP 4, 2026-10-11)**: 20 quadros (5×4 vistas), um shot ~0,45 s em qualquer ataque; aguardando aprovação visual |
| Asset visual reutilizável registrado na biblioteca | ⬜ |
