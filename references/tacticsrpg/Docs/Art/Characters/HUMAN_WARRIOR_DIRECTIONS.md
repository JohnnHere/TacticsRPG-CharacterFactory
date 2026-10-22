# Human Warrior Pilot — Especificação de Direções (MVP 2)

> Fonte canônica do MVP 2. Complementa `HUMAN_WARRIOR_PILOT.md` (identidade e status) e
> `CHARACTER_PIPELINE.md` (processo). **Integração implementada em 2026-10-11** (Presentation
> apenas; ver §5) com 4 sprites candidatos de teste — **aprovação visual pendente**; nada aqui
> marca a arte como final.

## A/B/C — três classes de arte (não confundir)

| Classe | O que é | Estado |
|---|---|---|
| **A — Direção de arte** | `character_style_anchor_v1.png` — estilo, proporção, paleta | ✅ aprovada |
| **B — Sprites de produção direcionais** | Vistas estáticas por direção, 128×128, alfa | ⬜ a produzir (este MVP) |
| **C — Frames de animação futuros** | Idle/Walk/Attack por direção | ⬜ MVP 3+ |

## 1. Como a direção funciona hoje (auditoria do código)

- **Core:** `Unit.Facing` é um `GridPos` ortogonal — 4 valores: `(0,1)`, `(1,0)`, `(0,-1)`, `(-1,0)`. **Não será alterado.**
- **`UnitView.SetFacing`:** rotação de mundo `LookRotation((X,0,Y))` → yaw mundial θu: `(0,1)`→0°, `(1,0)`→90°, `(0,-1)`→180°, `(-1,0)`→270°.
- **Câmera (`TacticsCamera`):** yaw θc inicia em **45°** e só muda em passos de **±90°** (Q/E) → θc ∈ {45, 135, 225, 315}. Pitch/zoom não afetam o azimuth.
- **Billboard (`UnitView.LateUpdate`):** o holder do sprite copia o forward horizontal da câmera (rotação cilíndrica). O sprite **não espelha** e o indicador "Front" (chão) continua mostrando o facing tático.
- **Consequência chave:** como θc é sempre `45° + n·90°` e θu é `0/90/180/270`, o ângulo relativo `d = (θu − θc) mod 360` é **sempre um múltiplo ímpar de 45°** — a unidade aparece em tela sempre em **diagonal**, nunca de frente/costas/perfil puros.

**Mundo ≠ tela:** o facing do Core (mundo) e a direção que o sprite aparenta na tela são coisas distintas; a tabela abaixo é a ponte entre elas.

## 2. Tabela de mapeamento mundo → tela

`d = (θu − θc) mod 360`. Componentes em tela: `sen(d)` > 0 → personagem olha para a **direita da tela**; `−cos(d)` > 0 → olha **para a câmera** (frente).

| Facing de mundo (θu) | Yaw da câmera (θc) | d | Direção na tela | Sprite requerido |
|---|---|---|---|---|
| `(0,1)` 0° | 45° | 315 | costas-diagonal à esquerda da tela | `back_l` |
| `(1,0)` 90° | 45° | 45 | costas-diagonal à direita da tela | `back_r` |
| `(0,-1)` 180° | 45° | 135 | frente-diagonal à direita da tela | `front_r` |
| `(-1,0)` 270° | 45° | 225 | frente-diagonal à esquerda da tela | `front_l` |

> **Correção (2026-10-11):** as linhas `(0,1)` e `(-1,0)` originais deste tabela diziam
> `front_l`/`back_l` trocados — contrariavam a própria fórmula da seção (`−cos(d) > 0` → frente:
> para d=315, `−cos(315°) = −0,71 < 0` → costas). Re-verificado vetorialmente contra o código
> (`SetFacing` = `LookRotation((X,0,Y))`; right da câmera = `(cos θc, 0, −sen θc)`): a tabela
> acima está correta. Os sprites candidatos seguem a semântica de tela da fórmula (conferido
> nos PNGs: `front_*` mostra o rosto, `back_*` mostra a capa). Confirmação final em jogo pelo
> rótulo de depuração (§5).

Os outros giros de câmera (135/225/315°) permutam os mesmos quatro pares (facing × câmera) — **com a câmera quantizada, apenas estas 4 vistas diagonais aparecem no jogo atual**. Rótulos `*_l/_r` são **da tela** (o que o jogador vê), não do personagem; confirmar o sinal visualmente com o primeiro sprite produzido (risco baixo, correção trivial de tabela se invertido).

### 4 ou 8 direções?

- **Agora (MVP 2): 4 diagonais** — `front_l`, `front_r`, `back_l`, `back_r`. Cobrem **100% dos estados visíveis** do jogo atual (prova acima). Zero desperdício de produção.
- **Futuro: 8 direções** — as 4 cardinais (`front`, `back`, `profile_l`, `profile_r`) só aparecem se o yaw da câmera deixar de ser quantizado em 45+90n (câmera livre) ou para reuso de diagonais→cardinais em animação. **Decisão: produzir 4 agora; reservar a nomenclatura para 8**; adicionar as cardinais apenas se/houve câmera livre.
- 4 direções cardinais puras **não** seriam suficientes: com a câmera a 45°, sempre cairiam "tortas" na tela.

## 3. Especificação do asset (classe B)

| Parâmetro | Valor | Origem |
|---|---|---|
| Naming | `warrior_pilot_dir_<direção>.png` com direção ∈ {`front_l`,`front_r`,`back_l`,`back_r`} (futuras: `front`,`back`,`profile_l`,`profile_r`) | novo, alinhado a MVP 1 |
| Diretório | `Assets/Resources/Characters/WarriorPilot/Directions/` | padrão `Resources` do MVP 1 |
| Canvas | **128×128** (mesmo do MVP 1) | MVP 1 aprovado |
| PPU | **100** (idêntico ao MVP 1) | MVP 1 aprovado |
| Filtro | **Point (no filter)**, sem mipmap, compressão off | MVP 1 aprovado |
| Pivot | **bottom-center** nos pés (o posicionamento no chão já é resolvido por `UseSprite` via `bounds.min.y`) | MVP 1 |
| Fundo | alfa transparente, sem halo | pipeline |
| Altura do personagem | **mesma contagem de pixels da arte útil do MVP 1 aprovado** — medir do PNG aprovado antes de desenhar (TBD: valor exato em px) | a medir |
| Consistência | mesma paleta, luz e escala entre as 4 vistas; silhueta idêntica; linha do chão no mesmo y | pipeline gate 2 |
| Iluminação | consistente entre vistas (direção da luz fixa; TBD: reproduzir exatamente a do MVP 1) | a definir na primeira vista |
| Equipamento assimétrico | **cada vista é desenhada de verdade — proibido espelhar** (a espada e a capa têm lado fixo no mundo; espelhar trocaria a mão da espada). A capa aparece nas vistas de costas por trás do corpo | decisão v2 |
| Clusters de pixel | validar em 100% de zoom na resolução nativa; sem reescala da referência | pipeline |

**Ordem de produção sugerida:** `front_r` primeiro (valida o mapeamento d e o lado da espada contra o MVP 1 em jogo) → `front_l` → `back_l` → `back_r` (capa).

## 4. Identidade preservada (todas as vistas)

Os mesmos traços aprovados: cabelo castanho descoberto, expressão madura, placas prateadas,
dourado contido, capa azul-marinho, couro marrom, espada longa única de aço, proporções
compactas, pixel nítido. A espada permanece na **mesma mão do personagem** em todas as
vistas (o lado que aparece na tela muda com a vista — isso é correto). Capa visível nas
vistas `back_*`; nas `front_*` aparece apenas a borda nos ombros.

## 5. Plano mínimo de integração (Presentation, pós-aprovação dos assets)

> **Status: implementado em 2026-10-11** conforme o plano abaixo; aprovação visual pendente.

1. **`UnitVisuals`** (único ponto de ligação unidade→visual, já existente): carrega as 4 direções uma única vez (novo método retornando um pequeno conjunto imutável `Sprite[4]` indexado por direção; entradas nulas permitidas). Escala 1.15 e o alvo "Hero" permanecem como estão.
2. **`UnitView`**: nova sobrecarga `UseSprite(Sprite[] directional, float scale)` ao lado da atual (que continua como fallback de personagem de sprite único). No `LateUpdate` (billboard já existente), calcula o índice de direção a partir de `Facing` (θu) e do yaw da câmera (`Camera.main.transform.eulerAngles.y` quantizado) **só quando o índice muda** — sem carga de asset, sem alocação por frame (`_sprite.sprite = conjunto[i]`, referência pré-carregada).
3. **Fallback em cascata:** direção exata → sprite estático do MVP 1 → cápsula. Nenhuma exceção por personagem espalhada em outras classes.
4. **Sem espelhamento automático** (`flipX` proibido): direção ausente cai no fallback, nunca num flip da espada/capa.
5. **Intocados:** Core/Facing, flanco, seleção, movimento, ataques, save/load, câmera, paleta de daltonismo (tint no `SpriteRenderer.color` como hoje).

Estimativa de diff: ~1 método + 1 sobrecarga + ~10 linhas em `UnitView.LateUpdate`. Nada de Animator, nem prefabs, nem cenas.

### Como ficou implementado (2026-10-11)

- `UnitVisuals.DirectionsFor(unit)`: conjunto `Sprite[4]` **cacheado estaticamente** (carrega 1×);
  índices `BackLeft=0, BackRight=1, FrontRight=2, FrontLeft=3` (constantes públicas). Retorna o
  conjunto se ≥1 vista carregou; `null` caso contrário (cápsula) ou para não-pilotos.
- `UnitView.UseDirectionalSprites(Sprite[])`: guarda o conjunto e força re-seleção. No
  `LateUpdate`: `d = Repeat(yawRaiz − yawCâmera, 360)`; índice = `RoundToInt((d+45)/90) & 3`
  (constantes `UnitVisuals.BackLeft..FrontLeft`) — **vista diagonal mais próxima** da direção
  aparente em tela: nos estados de repouso (câmera quantizada) d é exatamente diagonal e o
  resultado é inteiro exato; durante o giro da câmera (ou futura câmera livre) escolhe o vizinho
  mais próximo em vez de saltar 90°. *Correção (2026-10-11): a versão anterior usava piso em
  `(d+45)/90`, com limites de setor NAS diagonais — correta em repouso, mas podia exibir a vista
  ~90° errada por alguns quadros durante a transição da câmera; achada por verificação executada
  (25 checagens, 0 falhas após a correção).* `SpriteRenderer.sprite` só é tocado quando o índice
  muda; pés reposicionados por vista via `bounds.min.y`; vista nula → sprite estático (nunca
  `flipX`).
- **Testes determinísticos:** `Assets/Tests/EditMode/DirectionMappingTests.cs` congela a tabela
  das 16 combinações (facing × giro de câmera), diagonais exatas, yaw contínuo e wrap de ângulos
  — função pura `UnitView.DirectionIndex`, sem rendering Unity.
- **Depuração in-game:** com o overlay F3 (`GameSettings.ShowStats`), o rótulo da unidade ganha
  `[<vista> d=<ângulo>°]` (ex.: `[front_r d=135°]`) — `UnitView.DirectionLabel` — para conferir
  rótulo × orientação real em cada facing×giro de câmera.
- Fallback em cascata preservado: direção → estático MVP 1 → cápsula (se `SpriteFor` falhar,
  `Create` nem chama `UseSprite`). Escala ×1,15, sombra de contato e indicador "Front" no chão
  permanecem do MVP 1.

## 6. Riscos e questões em aberto

- **Sinal esquerda/direita da tabela:** derivado analiticamente; confirmar com o primeiro sprite em jogo (se invertido, corrige-se a tabela, não a arte). **Atualização (2026-10-11): a tabela original tinha 2 linhas trocadas (ver correção na §2); agora confere com a fórmula e com os PNGs — falta a conferência visual em jogo (§5, rótulo F3).**
- **Suposição de câmera quantizada:** o código de integração deve derivar o índice do yaw real (não presumir 45+90n), para sobreviver a uma futura câmera livre com fallback correto.
- **Luz/sombra:** sprite unlit sobre terreno URP lit (aceito no MVP 1); sombra continua sendo disco de contato sem direção.
- **Altura em pixels do MVP 1:** medir e congelar antes de desenhar (evita 4 vistas com alturas discrepantes).
- **Animator futuro (MVP 3):** troca por código hoje; migração para `Animator` no filho "Sprite" decidida só na fase de animação.

## 7. Próxima ação recomendada

Produzir **`warrior_pilot_dir_front_r.png`** (128×128, PPU 100, pivot nos pés, sem espelhar
o MVP 1) a partir do sprite aprovado, e validá-lo em jogo contra o mapeamento da seção 2
antes de desenhar as outras três.
## 8. Auditoria de ataque/direções (2026-10-11)

Diagnóstico do relato "ataca de lado" (vídeo: golpe de 27 = costas, regra correta):

- **Sequência de ataque — sem defeito:** `Combat.Execute` define `attacker.Facing` para o alvo
  ANTES do feedback; `PerformAttack` chama `SetFacing` antes de `PlayAttack`; a vista troca no
  `LateUpdate` do mesmo quadro (antes do primeiro quadro visível do avanço). O impulso do golpe
  (direção cardinal de mundo) projeta em tela na MESMA diagonal que a vista exibe — movimento e
  postura são coerentes. Tabela das 16 combinações verificada e congelada em testes.
- **Causa raiz da leitura "de lado": artística.** Com apenas 4 vistas estáticas diagonais não
  há pose de ataque: o personagem mantém a postura de repouso enquanto desliza ~0,35 u na
  diagonal do alvo; nas vistas de costas o rosto e a espada ficam ocultos — nada comunica
  "golpeando o alvo à frente". Animações de Attack são o MVP 4 (fora do escopo aqui); é a
  dependência para vender a direção, como no FFT.
- **Defeitos de arte encontrados (decisão do criador, sem correção em código):**
  1. `front_l` e `front_r` parecem **poses espelhadas**: a espada aparece à esquerda da tela em
     `front_l` e à direita em `front_r` — para um canhoto/destro consistente, ela deveria ficar
     no MESMO lado da tela nas duas vistas de frente. Viola "espada na mesma mão em todas as
     vistas" (§4/decisão v2).
  2. `back_r` não mostra a espada no lado próximo (esperado para a mão fixa; `back_l` escondê-la
     está correto) — possivelmente coberta pela capa; confirmar visualmente.
  3. O item 1 pode agravar a leitura "de lado" em ataques (espada do lado oposto ao alvo numa
     das vistas de frente).
- **Medições (consistência de escala):** altura do conteúdo 100 px idêntica nas 4 vistas
  (estático: 99 px), linha do chão em y=126 em todas — sem salto perceptível na troca de vista;
  larguras 89–97 px (esperado pelas poses). Escala aprovada mantida.
- **Oclusão por terreno:** comportamento de profundidade esperado (sprite transparente testa
  profundidade contra tiles opacos, igual à cápsula) — não é regressão; transparência de
  terreno/silhueta fica como task futura.

> **Fechamento (2026-10-11):** a revisão visual PlayMode inicial do criador aceitou as 4 vistas
> e a seleção direcional — **MVP 2 fechado** com as ressalvas registradas acima (suíte completa
> do Test Runner e regressão ampla não executadas; mão da espada pendente de inspeção de
> arte). Continuação animada (Idle/Walk) especificada em `HUMAN_WARRIOR_ANIMATIONS.md`.