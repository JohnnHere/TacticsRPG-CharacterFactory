# Character Production Pipeline v1.0 — Produção reutilizável de personagens

> **Documento central e autoritativo** para produzir e integrar novos personagens no
> TacticsRPG. Um agente (ou pessoa) deve conseguir produzir e integrar outro personagem
> seguindo este documento + `Characters/CHARACTER_TEMPLATE.md`, sem contexto histórico de
> conversas. Derivado e validado pelo piloto **Human Warrior Pilot**
> (`Characters/HUMAN_WARRIOR_PILOT.md` — implementação de referência; **não** é template
> visual obrigatório).
>
> **Modelo de propriedade da documentação:** `ART_DIRECTION.md` = linguagem visual geral ·
> este arquivo = processo de produção reutilizável · `CHARACTER_TEMPLATE.md` = especificação
> de novo personagem · `HUMAN_WARRIOR_PILOT.md` = registro do piloto ·
> `HUMAN_WARRIOR_ANIMATIONS.md` = detalhes de implementação das animações do piloto ·
> `ROADMAP.md` = marcos · `GAMEPLAY.md` = comportamento verificado (nunca planejamentos).
> Links entre documentos em vez de duplicação.

**Versão:** 1.0 (2026-10-11) — consolidado após o piloto (MVP 1–4, visualmente aprovado
como protótipo reutilizável). Extensões futuras: incrementar a versão e registrar a mudança
na seção 14.

---

## 1. Propósito e escopo

- **Escopo:** processo completo de produção de um personagem 2D (direções, animações,
  import, integração na Presentation, testes, aprovação) para **humanoides de 1 tile** no
  padrão validado pelo piloto.
- **Fora do escopo (pontos de extensão futuros, não implementados):** criaturas não
  humanoides, proporções incomuns, voadores, criaturas de múltiplos tiles, invocações,
  transformações, animação dependente de equipamento, casts de magia distintos, ataques à
  distância com projéteis, dual wield (ver §12).
- Este documento **não** cria features: descreve o que está implementado e o que exige
  trabalho novo.

## 2. Baseline implementada (verificada no repositório, 2026-10-11)

| Estado visual | Asset | Direções | Quadros | Trigger | Loop? |
|---|---|---|---|---|---|
| Estático por direção | `Directions/warrior_pilot_dir_<vista>.png` | 4 | 1 cada | Quando não há clipe para a vista | — |
| Idle | `Animations/Idle/idle_<vista>_<NN>.png` | 4 | 4/vista | Parado | Sim (0,96 s @1×) |
| Walk | `Animations/Walk/walk_<vista>_<NN>.png` | 4 | 6/vista | Durante `MoveAlong` real | Ciclo = 2 passos |
| Attack | `Animations/Attack/attack_<vista>_<NN>.png` | 4 | 5/vista | Qualquer ataque (um shot) | Não |
| Hit | `Animations/Hit/hit_<vista>_<NN>.png` | 4 | 3/vista | Golpe que ACERTA o piloto (um shot) | Não |
| Defeat | `Animations/Defeat/defeat_<vista>_<NN>.png` | 4 | 5/vista | Morte do piloto | Trava até a view sumir |

Total do piloto: **92 quadros de animação** + 4 estáticos direcionais + 1 estático MVP 1
(fallback). Escala visual ×1,15. Cubo branco de facing **desligado** em unidades com sprite.
**92/92 metas de animação validadas como Sprite/Single** (52 delas corrigidas de import
default em 2026-10-11 — ver §8.2).

## 3. Distinção fundamental: concept art ≠ sprite de produção

- **Concept/reference art** define estilo, proporção, silhueta e paleta. Pode ser pintada,
  suave e em alta resolução.
- **Sprite de produção (game-ready)** é pixel art em resolução nativa, com transparência,
  clusters de pixel limpos, canvas e pivot definidos.
- **Ampliar ou reduzir uma concept art NÃO produz sprite válido** — reescala borrado,
  quebra clusters e destrói a leitura de pixel. Todo sprite de produção nasce da referência,
  mas é **redesenhado à mão na resolução nativa**.

## 4. Padrões visuais (validados pelo piloto)

- Canvas **128×128 px**, RGBA com alfa limpo (sem halo).
- **Linha do chão em y=126** (coordenada de topo da imagem) em TODOS os frames — pés nunca
  afundam nem flutuam (o runtime realinha cada quadro por `sprite.bounds`, mas a consistência
  é responsabilidade da arte — gate 2).
- Altura de conteúdo ~**100 px** (topo entre y=25–28) — proporções compactas táticas;
  **não** introduzir proporções novas para um personagem já aprovado.
- Idle: bob vertical ≤ **2 px**. Walk: passada visível sem deslizar os pés no chão.
- **Identidade consistente** entre todas as vistas e clipes: paleta, corte de cabelo,
  equipamento, traços (gate 2). Referência de estilo: `ART_DIRECTION.md` §2.
- **Proibido espelhar** (`flipX`): assimetrias de corpo, mão dominante e roupa são parte da identidade.
- Silhueta legível em zoom-out (a câmera chega a 19 unidades).
- Personagens novos são weapon-independent: conceitos e sprites de corpo ficam sem armas
  empunhadas, carregadas ou embainhadas. Ver §11; a arma é um asset separado.

## 5. Sistema de direções (4 vistas de tela)

- Vistas: `front_l`, `front_r`, `back_l`, `back_r` — rótulos **de tela** (o que o jogador vê:
  `front_*` mostra o rosto; `back_*` mostra a capa/costas; `_l/_r` = lado da tela).
- **Mapeamento implementado e testado** (`UnitView.DirectionIndex`, tabela congelada em
  `DirectionMappingTests`): `d = Repeat(yawUnidade − yawCâmera, 360)`; índice =
  `RoundToInt((d+45)/90) & 3` → `[back_l, back_r, front_r, front_l]`. O yaw da unidade vem do
  **Facing do Core** (4 ortogonais — nunca alterado); o yaw da câmera é o real (sobrevive a
  câmera livre). Especificação completa: `Characters/HUMAN_WARRIOR_DIRECTIONS.md` §2.
- Com a câmera quantizada (45°+90k), **as 4 diagonais cobrem 100% dos estados visíveis**.
  Cardinais puras (`front`, `back`, `profile_*`) só fariam sentido com câmera livre — não
  produzir agora.
- **Anatomia consistente:** o personagem é desenhado de verdade em cada vista (nunca
  espelhado); a mão dominante não muda entre vistas. O sprite do corpo permanece sem arma.
  Quando uma ação invocar a arma equipada, o asset separado deve respeitar a mão e o encaixe.

## 6. Requisitos de animação

### 6.1 Contrato do piloto (referência, não limite de engine)

| Clipe | Quadros/vista | Ciclo @1× | Avanço | Loop |
|---|---|---|---|---|
| Idle | 4 | 0,96 s (0,24 s/quadro) | Relógio (`Time.deltaTime × GameSettings.AnimationSpeed`) | Sim |
| Walk | 6 (3/passo) | 2 passos = 0,44 s | `t` da interpolação do passo (`MoveAlong`, `StepTime` = 0,22 s/tile) | Durante o movimento |
| Attack | 5 (0,09 s) | ~0,45 s | Relógio, um shot | Não |
| Hit | 3 (0,08 s) | ~0,24 s | Relógio, um shot (só em golpe que acerta) | Não |
| Defeat | 5 (0,12 s) | ~0,60 s | Relógio, trava até a view sumir | Não |

- **Contagens do piloto são a referência validada, não limite de engine:** o carregador sonda
  `00..15` por vista e aceita 1–16 quadros; clipes novos/estados novos exigem trabalho de
  integração (§10).
- Fase do Walk é **contínua pelo passo cumulativo** (frame 00 não reinicia a cada tile);
  ciclo par fecha a cada 2 tiles.
- Transições (precedência **Defeat > Hit > Attack > Walk > Idle**): Idle→Walk no início do
  `MoveAlong`; Walk→Idle no fim (seguro contra interrupção via `finally`); Attack dispara no
  início do feedback de ataque; Hit só em golpe que acerta; Defeat na morte e trava até a view
  ser destruída. Undo/save/load não deixam estado residual (views são recriadas; save é
  bloqueado durante animação).
- Giro de câmera durante qualquer animação: só troca a vista (o clock não reinicia).

## 7. Padrão de import no Unity (procedure de validação)

Por frame/sprite, o `.meta` deve ter exatamente:

1. `textureType: 8` (Sprite 2D and UI) — **o defeito mais comum**: metas geradas como
   `textureType: 0` (textura default) tornam `Resources.Load<Sprite>` nulo (ocorreu 2× no
   projeto). Verificação rápida: Inspector mostra aba **Sprite** e preview do recorte.
2. `spriteMode: 1` (Single) · `spritePixelsToUnits: 100` · `filterMode: 0` (Point) ·
   `enableMipMap: 0` · `alphaIsTransparency: 1`.
3. Compressão **None** na plataforma Default (`textureCompression: 0` no bloco
   `DefaultTexturePlatform`; Standalone/WebGL podem ficar em 1 como no aprovado).
4. GUID único (nunca clonar GUID entre assets); mover/renomear sempre **com o `.meta`**.
5. Canvas 128×128 e linha do chão y=126 (conferir por medição de pixels opacos).

**Procedure:** após copiar PNGs, (a) conferir se o Unity gerou metas; (b) se geradas com o
padrão default do projeto (textura), aplicar o template aprovado (clonar um `.meta` aprovado
preservando o GUID existente do arquivo e trocando nome/spriteID/internalID); (c) validar com
a checklist da seção 14.1.

## 8. Estrutura de pastas e naming

```
Assets/Resources/Characters/<CharacterId>/
  <character>_mvp1_static_128.png            (estático de fallback)
  Directions/<character>_dir_<vista>.png     (4 estáticos direcionais)
  Animations/Idle/<state>_<vista>_<NN>.png   (idle_<vista>_00..)
  Animations/Walk/walk_<vista>_<NN>.png
  Animations/Attack/attack_<vista>_<NN>.png
  Animations/Hit/hit_<vista>_<NN>.png
  Animations/Defeat/defeat_<vista>_<NN>.png
```

- `<vista>` ∈ {`front_l`, `front_r`, `back_l`, `back_r`} · `<NN>` = `00, 01, …` sem pular
  índice (máximo sonda: 15) · tudo minúsculo, prefixo = id do personagem.
- **Nunca** colocar assets de personagem fora de `Resources/` (a carga é por
  `Resources.Load`).
- Detalhe do naming do piloto: o fallback MVP 1 e os direcionais usam prefixo
  `warrior_pilot_` completo; os clipes usam só o nome do estado — manter o padrão por
  personagem exatamente como no piloto para o carregador funcionar sem ajustes.

## 9. Integração com a Presentation (o que é reutilizável × o que é do piloto)

Arquitetura atual (toda na Presentation; **Core não conhece visuais**):

| Peça | Reutilizável hoje? | Detalhe |
|---|---|---|
| `UnitView` (billboard, pés por `bounds`, escala, sombra, Walk sincronizado ao `t` do passo, transições Idle/Walk, one-shots de combate, Defeat travado, fallback em cascata) | **Sim — agnóstica de personagem** | Seleciona quadros por índice de direção; sem branch por personagem |
| `UnitVisuals.LoadClipByDirection` (sonda `00..15`, cache + re-sonda enquanto houver direção sem clipe) | **Sim** | Genérica por `(pasta, prefixo)` |
| `UnitView.DirectionIndex` + `DirectionNames` | **Sim** | Testado (`DirectionMappingTests`) |
| Caminhos `Characters/WarriorPilot/…` e predicado `IsWarriorPilot(unit)` (time 0 + `IsKey` + nome `"Hero"`) | **Não — específico do piloto** | Todo `*FramesFor(unit)`/`SpriteFor`/`ScaleFor`/`DirectionsFor` passa por esse gate |

**Consequência importante: copiar a pasta de PNGs de um novo personagem NÃO o torna
jogável.** A integração mínima de um segundo humanoide exige (Presentation-only, ~30–60 min
de código):

1. Generalizar `UnitVisuals`: trocar o predicado `IsWarriorPilot` + constantes de caminho por
   uma pequena tabela `characterId → { pasta, escala, estático de fallback }` (sem framework).
2. Em `BattleSandbox`/dado da unidade, definir qual `characterId` cada unidade usa
   (hoje: o `Hero` do `MapData`).
3. Nada mais — `UnitView` não precisa de mudança para um humanoide no mesmo padrão.

Fallback em cascata (por estado/vista): clipe → estático MVP 1 → cápsula procedural. Sem
`flipX` em hipótese alguma. Indicador branco de facing fica **desligado** em unidades com
sprite (renderer off; GameObject e Facing do Core intactos).

## 10. Como integrar (passo a passo, Presentation)

1. Colocar os PNGs em `Assets/Resources/Characters/<Id>/…` (§8) e validar import (§7).
2. Confirmar contagens: 4 estáticos direcionais + Idle/Walk/Attack/Hit/Defeat por vista.
3. Registrar o personagem em `UnitVisuals` (gate/caminhos — ver §9) e na unidade de destino
   (`BattleSandbox.CreateViews` chama os `*FramesFor` — nada a mudar ali para o piloto).
4. Compilar (0 erros) e rodar a checklist §14.
5. Aprovação do criador (§15).

## 11. Política weapon-independent (DECISÃO VISUAL — 2026-10-19)

Personagens novos são produzidos sem arma empunhada, carregada ou embainhada em conceitos e
sprites do corpo, incluindo estáticos, Idle, Walk, Hit e Defeat. A roupa, postura e silhueta
devem identificar raça e Job sem depender da arma.

Cada arma é um asset separado. Ela só aparece quando a unidade a tem equipada e a ação/estado
atual a invoca. A Presentation precisará encaixar o asset na mão correta e sincronizar
posição, oclusão e tempo com a ação. A implementação atual usa um sprite composto por unidade
e **não suporta** esse overlay dinâmico; esta decisão define arte e direção futura, não declara
runtime pronto. A composição offline atual também não simula troca por equipamento/ação.

A espada do Human Warrior Pilot permanece desenhada nos seus sprites como exceção histórica do
protótipo. Preservar esses assets e suas pendências; não usá-los como template para personagens
novos nem alterar o piloto por esta decisão.

## 12. Reuso e pontos de extensão

**Reutilizável hoje (humanoide 1 tile, padrão do piloto):** jogáveis do time 0, inimigos
humanoides e NPCs — desde que registrados no gate de `UnitVisuals` e com a pasta de assets
completa (§10).

**Exige validação/trabalho novo (não suportado pelo piloto):** criaturas não humanoides ·
proporções fora do padrão 128×128/100 px · voadores (sem linha de chão) · múltiplos tiles ·
invocações/transformações (novos estados visuais) · animação dependente de equipamento ·
overlays de armas independentes, encaixe/oclusão e invocação por ação · cast de magia com
clipe próprio · sincronização de projéteis com frames · dual wield ·
tamanhos de canvas diferentes (o runtime tolera, mas a consistência visual e a escala ×1,15
foram calibradas para 128×128).

## 13. How to Produce the Next Character (workflow ordenado)

1. **Ler** `AGENTS.md`, este arquivo, `CHARACTER_TEMPLATE.md`, `ART_DIRECTION.md`,
   `Characters/HUMAN_WARRIOR_DIRECTIONS.md` (mapeamento) e `GAMEPLAY.md` (o que existe).
2. **Especificar** o personagem preenchendo `CHARACTER_TEMPLATE.md` (identidade, arquétipo,
   paleta, silhueta, status protótipo/produção).
3. **Referência visual aprovada** (gate 1) registrada em `Docs/Art/References/`; conceito de personagem sem arma. Armas são propostas/desenhadas como assets separados.
4. **Produzir os 4 estáticos direcionais weapon-independent** (§5/§8) + estático de fallback; validar import (§7).
5. **Validar identidade e proporções** em jogo com o estático (gate 2 parcial): silhueta,
   escala ×1,15, linha do chão, handedness.
6. **Produzir animações** na ordem do piloto: `idle_front_r` → `walk_front_r` → demais vistas
   de idle → demais vistas de walk → Attack/Hit/Defeat de `front_r` → demais vistas (§6).
   Aprovação por lote de vista, não por frame.
7. **Importar** seguindo §7 (metas com configuração aprovada; GUIDs únicos).
8. **Integrar** conforme §10 (gate de `UnitVisuals` + unidade de destino).
9. **Testar** com a checklist §14 (automação + PlayMode manual).
10. **Registrar** aprovação, defeitos artísticos e pendências no documento do personagem.

Aprovações do criador: gate 1 (referência), gate 2 (consistência entre vistas/clipes), gate 3
(aprovação final em jogo). Evitar aprovação frame a frame.

## 14. Testes

### 14.1 Verificação técnica (automatizada quando possível)

1. Compilação 0 erros (Core+Presentation+Tests com o SDK do Unity).
2. Testes EditMode existentes (`DirectionMappingTests`, `IdleFrameTests`, `WalkFrameTests`,
   suíte de Core ~140 testes) — rodar no Test Runner quando o editor estiver livre.
3. Metas: 92/92+ como Sprite/Single (scan de `textureType/spriteMode`).
4. Mediação de pixels: linha do chão y=126 e altura de conteúdo por frame.

### 14.2 PlayMode manual (obrigatório antes de aprovar)

1. Import sem erros · 2. 4 estáticos direcionais · 3. Idle nas 4 vistas · 4. Walk nas 4
vistas · 5. Movimento multi-tile com fase contínua · 6. Q/E durante e após animações ·
7. Attack toca uma vez · 8. Hit só em acerto · 9. Defeat toca uma vez e some limpo ·
10. Transições Idle↔Walk↔combate corretas · 11. Escala ×1,15 e pés no chão · 12. Sem
sprites duplicados/ausentes · 13. Sem textura rosa/ausente · 14. Sem indicador branco ·
15. Gameplay e outras unidades inalterados · 16. Undo/save/load sem estado residual.

### 14.3 Aprovação artística

Silhueta, paleta, handedness, legibilidade em zoom-out, qualidade do loop — **só o criador
aprova**. Compilar ≠ aprovado.

## 15. Critérios de aceite

- [ ] Checklist 14.1 sem falhas.
- [ ] 14.2 executada e registrada (ou pendências explícitas).
- [ ] Gate 3 do criador concedido.
- [ ] Documento do personagem atualizado (template preenchido, testes, pendências).
- [ ] Nenhum toque em Core/regras.

## 16. Limitações conhecidas (v1.0)

- Gate de personagem hardcoded no piloto (`UnitVisuals`) — generalização é o primeiro passo
  do segundo personagem (§9).
- Sem sombra direcional dedicada; sprite unlit sobre terreno lit; sorting entre múltiplas
  unidades com sprite ainda não exercitado (uma unidade com sprite hoje).
- Sem clipes de esquiva; Hit/Attack/Defeat são one-shots sem blend.
- Sem suporte a canvas/escala por personagem além do multiplicador ×1,15.
- Consistência de mão da espada entre vistas do piloto: pendente de decisão de arte.
- Assets/overlays de arma equipável não têm pacote, encaixe nem render por ação no runtime; personagens novos continuam sem armas nos seus sprites de corpo.

## 17. Versionamento e extensão

- v1.0 (2026-10-11): consolidação inicial pós-piloto (Idle/Walk/Attack/Hit/Defeat × 4
  direções + estáticos).
- 2026-10-19: diretriz do criador torna weapon-independent obrigatório para personagens novos;
  a espada do piloto permanece exceção histórica. Overlay de arma em runtime segue pendente.
- Próximas versões previstas: v1.1 multi-personagem (gate em tabela), v1.2 arma como camada
  (§11), v2.0 estados/criaturas fora do padrão humanoide. Alterar este arquivo somente com
  verificação no repositório (a implementação é a fonte da verdade).
