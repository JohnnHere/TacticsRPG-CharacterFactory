# Human Warrior Pilot — Animações (Idle/Walk/Attack/Hit/Defeat)

> **Registro verificado das animações do piloto** (estados, triggers, timing e incidentes) —
> complementa `HUMAN_WARRIOR_PILOT.md` (identidade/status),
> `HUMAN_WARRIOR_DIRECTIONS.md` (mapeamento direcional, aprovado) e
> `../CHARACTER_PIPELINE.md` v1.0 (**contrato de produção reutilizável — fonte autoritativa
> para NOVOS personagens**). Originalmente escrito como especificação do MVP 3; as seções
> abaixo foram atualizadas com o implementado (MVP 3A/3B/3C/3D e MVP 4 — todos integrados;
> 3C/3D aprovados pelo criador; MVP 4 aguardando aprovação visual).

## 1. Como o movimento/visual funciona hoje (auditoria do código)

- **Passo tático:** `UnitView.MoveAlong` interpola cada tile em `StepTime = 0,22 s`
  (`GameSettings.Duration` escala 1×/2×/4×/50× "Instantâneo"), com *hop* senoidal vertical e
  rotação da raiz para o último passo. O avanço já é paramétrico (`t` de 0→1 por passo).
- **Direção:** `UnitView.LateUpdate` seleciona a vista por `DirectionIndex(yawUnidade, yawCâmera)`
  (testado — `DirectionMappingTests`); troca só quando o índice muda; billboard + sombra de
  contato + pés realocados por frame via `bounds.min.y` (registro por frame já tolerante).
- **Estados visuais:** não existem — o sprite é estático desde o MVP 2. Sem Animator, sem
  prefabs: tudo é criado em runtime pela Presentation (`UnitView.Create` → `UseSprite` →
  `UseDirectionalSprites`), com cache em `UnitVisuals`.
- **Undo/save/load:** undo usa `Place`/`SetFacing` (view segue); save só fora de animação
  (`CanSave` exige `!_busy`); load destrói e recria as views pelo mesmo caminho.
- **Ataque:** feedback procedural (`BattleFeedback`) — avanço/recuo; **não faz parte do MVP 3**.

## 2. Mecanismo recomendado (auditoria de arquitetura)

**Controlador de frames leve, orientado a dados — não Unity Animator.**

| Critério | Animator Controller | Frame controller leve (escolhido) |
|---|---|---|
| Direção dinâmica (muda com facing E giro de câmera, a cada quadro) | Máquina de estados por GameObject: 2 estados × 4 direções + transições instantâneas em cada troca | Tabela `frames[clipe][direção]` + índice já existente (`DirectionIndex`) |
| Sincronização com o passo (0,22 s escalável até 50×) | `Animator.speed` por unidade/quadro, frágil com corotinas | Avanço do frame **derivado do próprio `t` do passo** em `MoveAlong` — sincronia por construção, clampa naturalmente no 50× |
| Assets | `.controller` + `AnimationClip` por vista (16+ assets) | Zero assets novos: `Sprite[]` em `Resources` como hoje |
| Padrão do projeto | Nenhum uso atual de Animator | Tudo procedural em runtime (`UnitView`/`UnitVisuals`/`BattleFeedback`) |
| Migração futura | — | Clips podem migrar para Animator por estado depois, sem tocar a seleção |

Previsível, sem branch por personagem (personagem novo = pasta nova + predicado em
`UnitVisuals`), diff estimado de ~60–80 linhas em 2 arquivos quando a integração for autorizada.

## 3. Padrão dos assets (classe B — frames)

| Parâmetro | Valor |
|---|---|
| Diretório | `Assets/Resources/Characters/WarriorPilot/Animations/<State>/` com `<State>` ∈ {`Idle`, `Walk`} |
| Naming | `<state>_<vista>_<NN>.png` — ex.: `Animations/Walk/walk_front_r_03.png`; `vista` ∈ {`front_l`,`front_r`,`back_l`,`back_r`}` (mesma semântica de tela do MVP 2); `NN` = `00, 01, 02…` (2 dígitos, sem pular índice) |
| Canvas | **128×128** idêntico ao aprovado |
| Linha do chão | **y = 126 px** em TODOS os frames (medida aprovada: conteúdo entre y=27 e y=126, altura 100 px) — pés sempre na linha; sem deslocamento horizontal do corpo além de ±2 px |
| Proporção/escala | Mesma contagem de pixels de altura do MVP 1/MVP 2 (100 px) — **não introduzir proporções novas**; escala in-game ×1,15 permanece |
| Import | Clonar o `.meta` das `Directions/`: Sprite (2D e UI), Single, PPU 100, Point, sem compressão, sem mipmap, alfa |
| Espelhamento | **Proibido** (`flipX` nunca; vistas desenhadas de verdade) |
| Identidade | Cabelo castanho descoberto, aparência madura jovem-adulta, placas prateadas, dourado contido, capa azul-marinho (visível nas `back_*`), couro marrom, espada longa na **mesma mão em todos os frames e vistas** |

## 4. Contagem de frames e timing

| Clipe | Mínimo | Baseline recomendado | Máximo útil | Ciclo / loop |
|---|---|---|---|---|
| **Idle** | 2 (respiração) | **4 frames** | 8 | Ciclo completo 0,8–1,2 s @1× (baseline: 4 × 0,24 s = 0,96 s); loop contínuo, sem deslocar a raiz; bob vertical ≤ 2 px |
| **Walk** | 4 | **6 frames** | 8 | **Ciclo = 2 passos = 0,44 s @1×** (3 frames/passo ≈ 13,6 fps). Deve completar ciclos inteiros a cada 2 tiles para não "escorregar" em distâncias variáveis |

- O tempo por frame NÃO é fixo no código: o walk avança pelo parâmetro `t` do passo
  (`frame = floor((passo + t) × framesPorPasso) mod N`) — honra automaticamente 1×/2×/4×/50×.
- No 50× ("Instantâneo") o passo dura ~4 ms: o walk simplesmente não é visível (frame 0) —
  comportamento aceitável e já previsto.

## 5. Regras de estado (contrato de integração futura)

- **Idle** (padrão na criação): toca em loop quando a unidade está parada; direção = facing
  relativo atual (reage a giros de câmera e mudanças de facing sem reiniciar o clock além da troca de vista).
- **Walk:** entra no início de `MoveAlong`, sai no fim (inclusive em interrupção/`ClearScene`);
  loop só enquanto move; direção pelo facing relativo **durante** o passo (a raiz já gira para o
  passo atual); pés acompanham hop/desnível pela interpolação existente.
- **Undo:** view volta por `Place`/`SetFacing` — permanece Idle, sem estado residual.
- **Save/load:** save nunca ocorre com animação em andamento (`!_busy`); load recria views → Idle.
- **Ataque/Hit/Defeat (MVP 4, integrados 2026-10-11):** estados transitórios de combate em
  `UnitView` (`PlayOneShot`/`PlayDefeat`) com precedência Defeat > Hit > Attack > Walk > Idle.
  Attack dispara em `PerformAttack`/`AttackEmptyRoutine` logo após o `SetFacing` (um shot
  ~0,45 s); Hit só quando o golpe ACERTA (~0,24 s); Defeat na morte (~0,60 s) e trava o visual
  até a view ser destruída (o `Vanish` existente continua sobre ele; gameplay inalterado).
  A vista do quadro segue o `DirectionIndex` (giro de câmera ok); vista sem quadro → estático.
- **Fallback em cascata por vista/estado:** walk → idle → estático MVP 1 → cápsula; frame ausente
  no meio do clipe → clipe encurta para os frames carregados; **nunca espelha, nunca quebra**.

## 6. Plano mínimo de integração (quando autorizado — NÃO implementar agora)

1. `UnitVisuals`: `FramesFor(unit)` → tabela `frames[estado][índice de direção]`, carregada 1×
   (sondagem de `00..15` por vista até falhar; ≥1 frame valida o clipe), cache estático.
2. `UnitView`: estado atual (Idle/Walk) + índice de frame; idle avança por `Time.deltaTime ×
   GameSettings.AnimationSpeed` no `LateUpdate`; walk avança dentro do loop de `MoveAlong`
   pelo `t`; `ApplySprite` existente já realoca os pés por frame.
3. `BattleSandbox`: **sem mudança** (todo o ciclo de vida já passa por `UnitView`).
4. Testes: `DirectionIndex` já coberto; adicionar teste puro do avanço de frame
   (`FrameIndex(passo, t, framesPorPasso)`), incluindo 50× e fim de ciclo.

## 7. Riscos e compatibilidade

- **Mão da espada:** se a inconsistência `front_l`/`front_r` do MVP 2 for confirmada, corrigir a
  arte ANTES de produzir os frames (senão ~48 frames herdam o erro).
- **Registro de frames:** pés fora da linha 126 causam "pulinhos" por frame — o código tolera
  (realoca por `bounds`), mas o gate 2 exige linha de chão consistente.
- **Contagens diferentes entre vistas:** o loader tolera (encurta o clipe), mas a consistência
  (gate 2) pede a mesma contagem nas 4 vistas.
- **Sorting entre múltiplas unidades com sprite:** continua adiado (uma unidade com sprite hoje).
- **Compatibilidade:** nenhum toque em Core, corotinas existentes, câmera, saves ou regras; o
  estático do MVP 1 e as `Directions/` permanecem como fallback.

## 8. Primeiro asset a produzir e validar

1. **`Animations/Idle/idle_front_r_00..03.png` (4 frames)** — valida registro/linha do chão,
   suavidade do loop, identidade e mão da espada na pose de repouso (estado dominante em tela),
   sem risco de contrato de timing. **Status (2026-10-11): produzido e integrado no MVP 3A**
   (loop 0,24 s/quadro; registro medido y=126 constante, bob 25–27 = ≤2 px; metas com
   compressão Default corrigida para 0). Validação PlayMode pelo criador pendente.
   **MVP 3C (mesma data): as demais 3 vistas de Idle foram produzidas e integradas** — 12
   quadros (`idle_front_l/back_r/back_l_00..03`) com import clonado do aprovado, medição
   idêntica (y=126, bob 25–27) e **zero alterações de runtime** (o carregador já sondava as
   4 vistas). **Investigação pós-teste (2026-10-11): respiração visível apenas em `front_r`.**
   Descartado por evidência: (F) quadros idênticos — diferenças de 1.346–1.869 px entre
   quadros consecutivos nas 4 vistas, magnitude igual à do `front_r` aprovado; (B) meta
   estrutural — dif normalizada contra o meta funcional de `front_r`: idêntica. **RESOLUÇÃO
   (2026-10-11): após reteste do criador com os assets reimportados, as 4 direções respiram —
   MVP 3C visualmente APROVADO.** Causa consistente com import desatualizado/cache estático
   sondado antes do import (não reproduzida em código). Endurecimento aplicado: o cache de
   clipes re-sonda enquanto houver direção sem clipe (cobre Enter Play Mode com Reload Domain
   desabilitado). Diagnósticos temporários (`[UnitVisuals]`/`[AnimDbg]`) removidos após a
   aprovação; queda de referência em §8.1 (histórico).
2. Em seguida, **`Animations/Walk/walk_front_r_00..05.png` (6 frames)** — valida o contrato de
   sincronia com o passo (0,22 s/tile) e a leitura de deslocamento diagonal, antes de expandir
   para as outras três vistas de cada clipe. **Status (2026-10-11): produzido e integrado no
   MVP 3B** (3 quadros/passo, ciclo = 2 passos, fase contínua pelo passo cumulativo; registro
   medido y=126 nos 6 quadros; metas com compressão Default 0). **MVP 3D (mesma data): as
   demais 3 vistas de Walk foram produzidas e integradas** — 18 quadros
   (`walk_front_l/back_r/back_l_00..05`) descobertos automaticamente pelo carregador existente
   (**zero alterações de runtime**; import clonado do aprovado; medição: 128×128, y=126 em
   todos, tops 26–30). Validação PlayMode pelo criador pendente (3D); `front_r` validado (3B).
   Próximo marco de arte: Attack/reações (MVP 4).

3. **`Animations/{Attack,Hit,Defeat}/` (MVP 4)** — 52 quadros (Attack 5×4, Hit 3×4, Defeat
   5×4 vistas). **Status (2026-10-11): produzidos e integrados.** Atenção de import: os metas
   vieram como textura default (textureType 0) e foram convertidos para Sprite/Single/PPU
   100/Point **preservando os GUIDs originais**; timing por quadro: Attack 0,09 s (≈0,45 s),
   Hit 0,08 s (≈0,24 s), Defeat 0,12 s (≈0,60 s), escalados pela velocidade de animação.
   Validação PlayMode pelo criador pendente.

## 8.1 Diagnóstico do incidente "respiração só em front_r" (MVP 3C — histórico)

> Diagnósticos removidos do código após a aprovação (2026-10-11). Registro para referência.

- `[UnitVisuals] Quadros de Idle por vista: back_l=N | back_r=N | front_r=N | front_l=N` —
  logava 1× na carga (início da batalha). Esperado: `=4` nas quatro vistas.
- `[AnimDbg] facing=(x,y) camYaw=… idx=N(vista) moving=… idle=N walk=N frame=F sprite=nome` —
  1×/s na unidade do piloto. Esperado, parado: `moving=False`, `frame` alternando 0→1→2→3 a
  cada ~0,24 s e `sprite=idle_<vista>_0F` mudando junto, em TODAS as vistas.
- Interpretação: `idle=0` em alguma vista → asset não importado como Sprite (reimportar) ou
  cache sondado antes do import (reiniciar o Play resolve — o cache é por domínio); `idle=4` e
  `sprite=` alternando mas visualmente parado → arte (reportar ao criador).
- **Endurecimento permanente resultante:** `LoadClipByDirection` re-sonda a tabela enquanto
  houver direção sem clipe (uma vez por construção de batalha), cobrindo o caso de assets
  importados após a primeira carga com Enter Play Mode em Reload Domain desabilitado.
