# ROADMAP — RPG Tático de Turnos (título provisório)

> Documento vivo. Serve como espinha dorsal e contexto para a execução das tasks.
> Sem prazos: apenas estágios, tasks e critérios de conclusão.
> Pode e deve ser alterado ao longo do desenvolvimento (a história, por exemplo, será construída em paralelo).

---

## 0. Como usar este documento

- Cada **Estágio** agrupa um tema. Cada estágio contém **Tasks** pequenas, entregáveis por si só.
- Estágios **não são estritamente sequenciais**: os marcados como *contínuos* (Lore, Arte, Áudio) andam em paralelo com os demais.
- Marcação de status: `[ ]` pendente · `[~]` em andamento · `[x]` concluída · `[!]` bloqueada/revisar.
- Toda mudança de rumo relevante vai para o **Registro de Decisões** (seção 9).
- Ideias que não cabem agora vão para o **Backlog de Ideias** (seção 10), não são descartadas.
- Ao iniciar uma task, copie o **Template de Task** (seção 11) para uma nota/issue e trabalhe nela isoladamente.

---

## 1. Visão

**Sucessor espiritual de Final Fantasy Tactics**: um RPG tático de turnos, em grid com altura, focado em montar um exército, criar builds próprias e viver histórias dentro de uma guerra política complexa. Com identidade e originalidade próprias (como Triangle Strategy fez).

**Ambientação:** fantasia medieval clássica (humanos, anões, elfos, orcs, trolls etc.), fortemente influenciada pela mitologia de Tolkien, com lore profunda e rica ao nível de World of Warcraft — porém com mundo, nomes, povos e história originais.

### Pilares

| Pilar | Objetivo |
|---|---|
| Combate tático profundo | Grid com verticalidade, posicionamento, terreno, decisões com trade-offs reais |
| Classes e raças | Builds muito variadas; raça muda a forma de montar o exército, não só números |
| Guerra em escala | Batalhas pequenas *e* massivas; comandantes, moral, cercos |
| Personagens | Recrutas com identidade, traços, relações e motivações |
| Mundo vivo | Facções, territórios que mudam, segredos, exploração entre batalhas |
| Narrativa | Dois níveis: pessoal (protagonista e companheiros) e geopolítico (reinos, religião, rivalidades) |
| Refúgio | Cenários bonitos e acolhedores; o jogo como lugar confortável de se estar (inspiração: Digimon World 2003) |

### Influências e o que cada uma traz

| Referência | Contribuição |
|---|---|
| Final Fantasy Tactics | Base do gênero, sistema de jobs, tom político-dramático |
| Triangle Strategy | Escolhas com consequência, facções, originalidade dentro do gênero |
| Dofus | Profundidade estratégica, sinergia de builds, posicionamento |
| World of Warcraft | Densidade de lore, raças e facções marcantes |
| Digimon World (2003) | Afeto, beleza dos cenários, ambiente acolhedor |
| Tolkien / medieval | Mitologia, tom, cultura, linguagem, história longa e profunda |

---

## 2. Decisões de design já tomadas

- **Batalhas longas são desejáveis.** O prazer de "perder tempo" é um valor do projeto. Não simplificar batalhas grandes só por velocidade.
- **Checkpoints condicionais durante batalhas específicas**, somente mediante condições futuras definidas pelo criador. Save/load manual livre em combate não é permitido (MVP 5A.4).
- **Estética de raças/classes mais clássica** (orcs, trolls, humanos, anões etc.), sem copiar nomes, poderes e limitações das sugestões do chat.
- **Sistemas conversam entre si** (raça ↔ classe ↔ facção ↔ território ↔ batalha ↔ narrativa). Evitar sistemas isolados.
- **Trabalho por etapas e tasks pequenas**, cada uma entregável.
- **História é escrita em paralelo** ao desenvolvimento; a lore evolui em camadas (ver Estágio 6).
- **Originalidade legal:** inspiração em Tolkien/WoW/FFT não deve virar cópia de nomes, personagens ou elementos protegidos.
- **Tecnologia:** Unity + C#. Lógica de regras (turnos, dano, moral, IA) em C# puro, separada da apresentação, para permitir testes, saves em batalha e desfazer ações.
- **Baseline de conteúdo v2.0 (canônica, ver `Docs/GameDesign/`):** 28 raças jogáveis em alguma medida (recrutamento desigual por narrativa/facção; cânone élfico com High Elf como posição aristocrática, não superioridade biológica) e 63 Jobs (61 originais + Venomancer + Affliction Master, ambos independentes). Summoner é o principal especialista em múltiplas invocações controláveis; Shaman é versátil (bonecos, totens, venenos, desgaste); Warlock tem 1 demônio robusto; Hunter 1 companheiro; Necromancer reanima cadáveres. Sem Jobs elementais novos (nada de Pyromancer, Cryomancer, Arcanist ou Plague Doctor) — fogo/gelo/raio vivem em escolas internas dos Jobs existentes.
- **Documentação é design, não implementação:** conteúdo de `Docs/GameDesign/` descreve a baseline; nada disso existe ainda em código. Inspecionar a implementação real antes de presumir sistemas prontos.
- **Plataformas:** PC/Steam primeiro. Android somente após lançamento estável no PC. Console é possibilidade futura, sem descartar.
- **Estilo visual:** HD-2D / 2.5D (mapas 3D com altura + sprites 2D), com estrutura inicial próxima de FFT The Ivalice Chronicles e Triangle Strategy.

---

## 3. Gaps de FFT a resolver (mapa de diferenciais)

Cada item aponta para o estágio onde é tratado.

| Gap | Estágio |
|---|---|
| Pouca variedade/combinação de classes; builds convergem para "meta skills" | 2 |
| Raças pouco relevantes | 3 |
| Montarias como mero equipamento; pouca presença no campo | 4 |
| Batalhas pequenas demais para uma guerra | 5 |
| Rivalidade entre reinos/facções pouco sentida | 6, 7 |
| Poucos extras e segredos | 15 |
| Pouca agência entre batalhas (mapa → cidade → loja → batalha) | 7 |
| Recrutas genéricos e intercambiáveis | 8 |
| IA sem identidade | 9 |
| Objetivos de batalha pouco variados | 7 |
| Derrotas/vitórias sem consequência real | 7 |
| Morte/perda de unidades pouco estratégica | 8 |
| Equipamentos pouco significativos | 2 |
| Longevidade (NG+, desafios) | 15 |

---

## 4. Visão geral dos estágios

```
FUNDAÇÃO (0)
   │
   ├─► NÚCLEO TÁTICO (1) ─► CLASSES (2) ─► RAÇAS (3) ─► MONTARIAS (4) ─► GRANDE ESCALA (5)
   │                                                                          │
   ├─► LORE E MUNDO (6, contínuo) ─► CAMPANHA E MUNDO VIVO (7) ─► EXÉRCITO E PERSONAGENS (8)
   │                                                                          │
   ├─► IA (9) ── ARTE (10, contínuo) ── ÁUDIO (11, contínuo) ── UI/UX (12)
   │
   └─► VERTICAL SLICE (13) ─► PRODUÇÃO DE CONTEÚDO (14) ─► EXTRAS (15) ─► POLIMENTO E LANÇAMENTO (16)
```

**Marcos principais:**
1. *Protótipo cinza jogável* (fim do Estágio 1)
2. *Sistema de builds funcional* (fim do Estágio 3)
3. *Batalha em grande escala funcional* (fim do Estágio 5)
4. *Vertical Slice* (Estágio 13): capítulo completo, representativo do jogo final

---

## 5. Estágios e Tasks

### Estágio 0 — Fundação

**Objetivo:** alinhar o projeto antes de construir.

- [ ] 0.1 Definir nome provisório e *one-page pitch* (1 parágrafo + pilares + diferenciais)
- [ ] 0.2 Definir escopo alvo (tamanho da campanha, nº de classes, raças, capítulos) — pode ser revisto
- [x] 0.3 Escolher plataforma(s) alvo e engine e justificar → **Unity + C#**; lançamento inicial em PC/Steam; Android após lançamento estável no PC; console em avaliação futura (ver seção 9)
- [x] 0.4 Definir estilo visual base → **2.5D / HD-2D**: mapas 3D em grid com altura + sprites 2D, iluminação e profundidade de campo; referência estrutural: FFT The Ivalice Chronicles e Triangle Strategy (impacta Estágio 10)
- [ ] 0.5 Definir organização de pastas, versionamento (Git) e convenção de nomes
- [~] 0.6 Criar pasta `/docs` com: este roadmap, bíblia de lore, documento de design (GDD), registro de decisões → `TacticsRPG/docs/` criada com `ROADMAP.md` e `GAMEPLAY.md` (regras de gameplay como implementadas); `Docs/GameDesign/` criada com documentação consolidada v2.0 (índice e autoridade em `DOCUMENT_INDEX.md`, decisões em `DESIGN_DECISIONS.md`, 28 raças e 63 Jobs catalogados); faltam lore (Estágio 6) e consolidação final da bíblia de design
- [ ] 0.7 Montar *moodboard* (cenários, paleta, tom, referências musicais)
- [ ] 0.8 Escolher ferramenta de tasks (quadro Kanban, issues, Notion etc.)

**Entregável:** pitch de 1 página + repositório organizado + stack definida.

---

### Estágio 1 — Núcleo Tático (protótipo cinza)

**Objetivo:** provar que o combate é divertido com arte placeholder.

- [x] 1.1 Definir regras centrais no papel: grid, altura, ordem de turno (CT/iniciativa), ações por turno → seção 0 de `GAMEPLAY.md` (versão inicial, valores provisórios; pontos em aberto listados lá)
- [x] 1.2 Implementar grid com altura (tiles com elevação) e câmera/rotação → grid com altura e câmera no padrão Triangle Strategy (giro de 90°, 3 níveis de zoom, foco automático na unidade da vez); transparência de tiles que tapam a visão adiada para quando houver arte de mapa
- [~] 1.3 Movimento com custo, alcance, pathfinding e regras de salto/queda → feito: Move/Jump, custo por terreno (lama), atravessar aliados, inimigos bloqueiam, knockback com colisão e dano de queda (regra pronta, sem HP ainda); falta: direção/facing, custos por outros terrenos, queda voluntária, integração com turnos
- [x] 1.4 Ordem de turnos e fila visível → CT por Velocidade, 1 movimento + 1 ação por turno, direção final, fila de 8 turnos na tela
- [x] 1.5 Ataque básico: alcance, linha de visão, direção (frente/lado/costas), altura → corpo a corpo e arco, desnível máximo por arma (padrão 1; categorias futuras personalizam), linha de visão de projétil estilo FFT, ângulo com dano e acerto
- [~] 1.6 Fórmulas de dano, precisão, evasão, crítico (documentar em planilha) → feito: crítico base por ângulo (frente 0%, lado 10%, costas 20%, ×1,5) com ganchos de bônus por arma e unidade; falta: planilha de balanceamento e crítico por classe/raça/habilidade
- [ ] 1.7 Habilidades ativas com tempo de conjuração, alvo, área
- [ ] 1.8 Terreno e efeitos (água, lama, gelo, fogo, cobertura)
- [ ] 1.9 Estados/condições (veneno, sono, medo etc.)
- [~] 1.10 Objetivos de vitória/derrota configuráveis (base para Estágio 7) → feito: derrotar todos/unidades-chave inimigas, derrota por todas ou pela unidade-chave, configurável por mapa; falta: objetivos com turno limite, escolta, captura etc.
- [~] 1.11 Editor/formato de mapa simples (dados em JSON/ScriptableObject/recurso) → feito: `MapData` (ScriptableObject) e editor visual compacto (Tactics > Map Editor) com janelas sob demanda para tamanho, unidades e objetivos; falta: layout final do editor (a definir), preenchimento/seleção em área, teste de mapa direto do editor
- [x] 1.12 IA mínima (mover e atacar o mais próximo) para teste → ataca a melhor opção (dano esperado, flanco, abate) ou avança até o inimigo mais próximo
- [x] 1.13 Save/load de estado de batalha (base para saves durante a luta) → infraestrutura interna de snapshot JSON no meio do turno; MVP5C v3 preserva status/fonte/duração e lê v2 legado; acesso irrestrito F5/F9/UI removido no MVP 5A.4; checkpoints condicionais futuros em 5.7
- [x] 1.14 Sessão de playtest interno e notas → **mapa de playtest "A Passagem" criado** (`Assets/Resources/Maps/Playtest_Passagem.asset`, 14×14, 3 rotas: passagem central entre paredões h3, rota oeste em lama com lagoa, alta rota leste com planalto h2 e posto inimigo; 4×4 unidades, vitória = Commander (chave), derrota = Hero (chave)); validação técnica automatizada contra o Core real: 40/40 checagens (imports/spawns/movimento/alcance do comandante/lama 2-tile/água/LOS do arqueiro/objetivos). **Playtest exploratório realizado pelo criador (2026-10-11): batalha divertida e viável** — posicionamento exigiu escolhas reais (flanquear × avanço melee × caça aos arqueiros); elevação influenciou movimento e combate à distância; CT gerou escolhas reais entre mover/agir/esperar; **lama foi mecanicamente válida mas de baixo impacto neste cenário**; **qualidade do posicionamento/decisões da IA precisa melhorar**; **defeito visual corrigido na sequência**: disco magenta sob o Hero (sombra de contato com error-shader — corrigido na Presentation, ver `UnitView.CreateShadowMaterial`). Checklist e observações: `Docs/PLAYTEST_A_PASSAGEM.md`. **Ressalvas**: cobertura automatizada/manual ampla continua separada e pendente; passes de balance (spawns/speeds/terreno) são trabalho futuro e não invalidam o playtest realizado

**Critério de conclusão:** uma batalha 4×4 em mapa com altura é jogável do início ao fim e "é divertida" mesmo com cubos cinzas.

---

### Estágio 2 — Classes (Jobs), Builds e Equipamentos

**Objetivo:** sistema de builds profundo, sem "habilidade objetivamente melhor".

> **Fonte canônica do catálogo:** `Docs/GameDesign/JOB_CATALOG.md` (63 Jobs: 8 básicas, 18 intermediárias, 26 avançadas, 8 secretas, 3 únicas), regras de acesso em `JOB_ACCESS_RULES.md`, slots e economia em `PROGRESSION_AND_BALANCE.md`. Implementação por fatias, nunca o catálogo inteiro de uma vez.

- [~] 2.1 **Fundação de dados:** `JobDefinition` e `AbilityDefinition` (efeitos compostos: dano, cura, status, deslocamento, área, criar entidade) com IDs estáveis e validação de referências — sem classe C# por Job
- [~] 2.1A **MVP 5A incremental — primeira habilidade ativa:** Corte Pesado (`warrior.heavy_slash`), definição imutável + validação/execução no Core via Combat existente, fixture apenas do Hero, escolha F/H, prévia real, animações reaproveitadas e snapshots v2 preservados. Parâmetros 135% / −10 pontos percentuais são provisórios. Testes Core e compilação realizados; demonstração manual PlayMode pendente (`Docs/MVP_5A_HEAVY_SLASH.md`). Não conclui Jobs, catálogo de efeitos, talentos ou progressão.
- [~] **MVP 5A.2 — direção final por ordem de ações:** implementado no TurnManager/Presentation com `FacingLocked` existente, sem novo campo/save v2; confirmação manual protegida por turno. Ataque básico, Corte Pesado, erro e vazio seguem a ordem. Compilação e testes Core externos executados; PlayMode pendente (checklist em `GAMEPLAY.md`, seção 3.2).
- [~] **MVP 5A.5 (2026-10-13) — correções de Corte Pesado:** mira/Core aceitam tiles vazios válidos, sem resultado fictício ou gasto duplicado; destaques/execução usam mesma validação. Menu mostra apenas IDs pertencentes à unidade; posse separada da disponibilidade de turno/arma e H/Core mantêm autorização. Fixture somente Hero/time 0, sem Jobs/talentos. 205 casos Core externos passaram e Core/Presentation compilados; animação/menu/H reais pendentes de PlayMode. Mantém 5A.2–5A.4 e snapshot v2.
- [~] **MVP 5B — Multi-Ability Batch 01 (2026-10-13):** Cura (`acolyte.heal`, Ally/C, 30 HP, alcance 0–3, suporte sem trava); Faísca (`mage.spark`, Soldier/G, 20 dano direto, alcance 1–3, desnível ≤3 e LoS existente); Tiro Mirado (`archer.aimed_shot`, Archer/T, arco, +15 pp acerto e 90% dano bruto). Parâmetros provisórios. Hero/H mantém Corte Pesado. Catálogo/menu/validação compartilhados, grants unitários temporários e feedback sem nova arte. Checkpoints A/B/C/D: 209/212/216/230 casos Core passaram; Core/Presentation compilados externamente. Presentation pura: 12 passaram, 1 divergência preexistente no empate direcional em câmera livre (UnitView/teste inalterados). PlayMode novo pendente, checklist GAMEPLAY 3.1B. Não implementa Jobs, talentos, Subjob, MP, resistências, status, IA de habilidades ou equipamento avançado; checkpoints condicionais permanecem futuros em 5.7.
  - **Targeting UX + Ability Design Skill v1.0 (2026-10-14):** skill instalada em `.agents/skills/ability-design/SKILL.md`, descoberta nesta sessão, oito arquivos e sete referências relativas validados; `AGENTS.md` raiz encaminha tarefas de habilidades. Geometria independente de presença de alvo/ação; overlays distinguem área e tiles executáveis. Cura consultável sem feridos. Faísca mantém alcance próprio 1–3/desnível ≤3/LoS e 20 dano, agora aceita aliado vivo exceto si (fogo amigo) e vazio (uma ação, sem dano); permissões específicas, não regra global. Core/Presentation compilados; **258 casos Core passaram**, snapshot v2 round-trip passou; Presentation pura 12 PASS/1 FAIL preexistente. PlayMode e legibilidade pendentes: `Docs/MVP_5B_TARGETING_UX.md`. Nenhuma habilidade nova, mudança de talentos/CT/saves/sprites ou alteração de character-art-design.
- [ ] 2.1A follow-up: integração definitiva de cura/magia e fórmulas/recursos/custos quando introduzidos, integração com árvores de talentos e persistência de IDs aprendidos, seleção de habilidades pela IA e playtest de balanceamento.
- [~] **MVP 5C — Ability Batch 02 (2026-10-14):** Chuva Curta (`archer.short_volley`, Archer/V) valida centro com arco e resolve cruz raio1 enemy-only via Combat×65%, uma ação inclusive sem vítimas. Proteção (`acolyte.protection`, Ally/P) +3 Defesa efetiva; Gelo Menor (`mage.minor_ice`, Soldier/I) 12 dano mágico e Move−1/mínimo1. Dois status finitos com source/target/refresh sem acúmulo, expiração no fim de duas ativações futuras, ignorando turno de aplicação no alvo ativo. Área/previews, movimento real/highlights/IA e painel de status integrados; correções Cura/Faísca preservadas. Snapshot v3 com leitura v2, sem save livre/checkpoints novos. A/B/C/D: **269/279/291/308 Core PASS**, Core/Presentation/Tests compilados; Presentation pura 12 PASS/1 FAIL preexistente. PlayMode/legibilidade/balanceamento pendentes em `Docs/MVP_5C_ABILITY_BATCH_02.md`. Não conclui Jobs/talentos/IA de habilidades nem sistema avançado de status.
- [~] **MVP 5C.1 — tile apontado, menu hierárquico e direção final (2026-10-18):** quadro fino do tile sob o cursor (verde = alvo válido, laranja = no alcance sem alvo elegível, branco = neutro) classificado no Core (`TargetingPreview`) e desenhado na peça de hover existente (`MapView.ShowHover`, 4 barras finas que não cobrem terreno/unidade); corrige a causa do destaque que sumia (a limpeza de overlays mantinha o tile em cache e impedia redesenhar o MESMO tile — `BattleSandbox.ClearOverlays` agora zera `_hovered` e usa `TargetingOverlays.HoverChanged`). Menu de comandos hierárquico (Principal: Mover/Ações >/Esperar; Ações: Atacar/Habilidades >; Habilidades: possuídas) montado do acesso/turno reais por `ActionMenu`, com itens desabilitados visíveis e motivo, **Voltar** subindo um nível e **Desfazer movimento [Backspace]** separado da navegação; atalhos seguem como acesso rápido pela mesma validação do Core. **Correção de direção final que supersede explicitamente a regra "Attack Only"** do MVP 5A.2: `FacingLocked = ação ofensiva E já se moveu`, então Mover → Atacar trava no alvo, mas Atacar → Mover, **Atacar → Esperar sem movimento**, Só mover e Só esperar abrem escolha manual (confirmação gratuita, uma vez, sem alterar CT); Cura/Proteção seguem suporte sem trava; IA encerra sem prompt. Unity Test Runner EditMode em cópia isolada do projeto: **362 testes, 361 PASS, 1 FAIL preexistente** (`DirectionMappingTests.Index_DerivesFromRealYaw_SurvivesFreeCamera`, empate 135/45 já registrado nos lotes 5B/5C, `UnitView`/teste intactos); novos testes em `Assets/Tests/EditMode/Mvp51HoverMenuFacingTests.cs`. Sem habilidade/Job/talento/arma/mapa/snapshot novos; aparência do quadro, raycast e navegação real seguem pendentes de PlayMode, e a **legibilidade do menu/HUD em batalhas grandes permanece em aberto** (Estágio 12 / 12.11).
  - **Revisão técnica 5C.1 (2026-10-18):** corrigidos Voltar na Presentation, troca de página durante mira, hover em inspeção/comandos, preview básico após uso da ação e limpeza da área ao encerrar batalha. Unity EditMode revisado: **370 casos, 369 PASS, 1 FAIL direcional preexistente** (308 Core e 49 testes MVP5C.1 passaram); substitui a contagem anterior para o estado revisado. Matriz dos 28 requisitos e limites em [MVP_5C_1_TECHNICAL_REVIEW.md](MVP_5C_1_TECHNICAL_REVIEW.md). PlayMode e HUD de grande escala permanecem pendentes.
- [~] **MVP 5C.2 — retorno automático ao menu principal e desfazer só pelo Backspace (2026-10-18):** depois de uma ação ou movimento **executados e confirmados pelo Core**, a Presentation volta à página **Principal** da árvore de comandos enquanto o turno do jogador continua. Causa raiz: `BattleSandbox.AfterAction` reabria os comandos sem resetar `_menuPage`, então o submenu de origem (Ações/Habilidades) ficava aberto e o jogador tinha de subir um nível à mão. Erro (miss) e conjuração válida em tile vazio contam como execução; cancelamento da mira volta ao submenu que a lançou; tile inválido, habilidade não autorizada, prévia e recusa do Core não navegam (aviso "Execução recusada: nenhuma ação foi gasta."). Direção final continua com prioridade (Atacar→Mover e Atacar→Esperar abrem escolha manual; Move→Atacar trava e encerra) e nada reabre durante animação, no turno da IA, em callback atrasado de outra unidade ou com a batalha decidida. O item **Desfazer movimento [Backspace]** saiu do MENU PRINCIPAL e **não** foi recriado em nenhum submenu: desfazer voltou a ser **só o atalho** Backspace, com a mesma autorização do Core (`TurnManager.CanUndoMove`/`UndoMove`), distinto de Voltar/Esc e com dica passiva na aba Sistema. Sem habilidade/Job/talento/arma/mapa/snapshot novos; `MapView` ganhou descarte de overlay seguro em EditMode (apoio aos testes, sem mudança visual). Unity Test Runner EditMode em cópia isolada do projeto: **398 casos, 397 PASS, 1 FAIL direcional preexistente** (o mesmo `DirectionMappingTests.Index_DerivesFromRealYaw_SurvivesFreeCamera` de 5C.1; baseline revisado 370/369), com os **28 casos novos** de `Assets/Tests/EditMode/Mvp52AutoMenuReturnTests.cs` passando **28/28** e zero erros de compilação. PlayMode pendente: clique real do mouse, ausência física do botão e tecla Backspace; HUD de grande escala (12.11) segue aberto.
- [~] 2.2 **Fundação de status:** MVP5C implementa somente `StatusDefinition`/`StatusInstance`, dois modificadores efetivos com refresh, ciclo no fim da ativação e persistência. **Pendentes:** tick de DoT no início do turno, stacks com teto, dispel, resistências, imunidades/auras/propagação — base futura para venenos, queimaduras e maldições (`DAMAGE_OVER_TIME_AND_ELEMENTAL_MAGIC.md`); não aplicar sem nova autorização.
- [ ] 2.3 Reescrever o ataque básico atual como a primeira `AbilityDefinition` (refactor transparente; testes existentes como rede de segurança)
- [ ] 2.4 Definir estrutura de personalização (slots): Job principal, Subjob (comando secundário, sem passivas), 1 Reaction, 1 Support, 1 Movement, traço racial inato + habilidade racial ativa (`PROGRESSION_AND_BALANCE.md`)
- [ ] 2.5 Definir sistema de progressão e **árvores de talentos** (`TalentTreeDefinition`/`TalentNode` de Job e racial; pontos de progressão, pré-requisitos entre nós, habilidades ativas/passivas, invocações e transformações como nós; persistência dos talentos aprendidos no save — regra canônica v2.1 em `Docs/GameDesign/DESIGN_DECISIONS.md`); JobLevel 1–5, desbloqueio por IDs estáveis (`JobUnlockRule` apenas progressão), afinidades que reduzem custo de pontos sem alterar potência nem bloquear
- [ ] 2.6 Regra de design: **todo bônus forte precisa de custo** (trade-offs) — documentar "princípios de balanceamento"
- [ ] 2.7 Prototipar os 8 Jobs básicos (Squire, Warrior, Archer, Apprentice Mage, Acolyte, Rogue, Scout, Brawler) + 1 intermediário completo com progressão
- [ ] 2.8 Criar Jobs avançados, secretos e únicos por fatias verticais (a serem expandidos em 14); validação das distinções: Affliction Master independente de Warlock e maior especialista em DoT; Venomancer especialista em veneno; Shaman versátil sem superar especialistas; Summoner com primazia de invocações
- [ ] 2.9 Sistema de equipamentos: poucas peças, mais significativas (armas com propriedades, peso, alcance; runas/modificadores); compatibilidade com anatomia (raças)
- [ ] 2.10 Sistema de habilidades de arma e compatibilidade Job ↔ equipamento
- [ ] 2.11 Ferramenta/planilha de balanceamento (dano esperado, custo-benefício) e matriz de especialização (burst/DoT/controle/invocações; horizontes de 1, 3, 5 e 8 turnos)
- [ ] 2.12 Playtest de builds: procurar combinações quebradas ou "obrigatórias"
- [ ] 2.13 **Motor de invocações controláveis** (`SUMMONING_SYSTEM.md`): entidades com `EntityId`/`OwnerId`/cap/duração no mesmo motor de turnos, orçamento de 2 ordens completas por rodada, prevenção de recursão (invocações não invocam), `CorpseToken` para o Necromancer e `CapacityPoints` para o Summoner; provar com 1 criatura antes dos 5 Jobs de invocação

**Critério de conclusão:** ao menos 3 builds distintas e viáveis por Job, sem uma dominar as demais.

---

### Estágio 3 — Raças

**Objetivo:** raça como sistema estratégico, não só "+10% de atributo".

> **Fonte canônica:** `Docs/GameDesign/RACES.md` (catálogo de 28 raças com traços inatos e ativas propostos), `RACIAL_ABILITIES.md` (contrato de habilidades e mecânicas avançadas) e o cânone élfico em `DESIGN_DECISIONS.md`. Lista de raças **já definida** — implementar por fatias, não em lote.

- [ ] 3.1 **Fundação de dados:** `RaceDefinition`, `RaceAbilityDefinition` e `RacialProgression` (composição, IDs estáveis, sem subclasse por raça)
- [ ] 3.2 Implementar as 2 primeiras raças com passiva + ativa e testes (provar a arquitetura antes de escalar)
- [ ] 3.3 Para cada raça: papel estratégico, forças, fraquezas, contrajogo documentado (vulnerabilidades de Troll, Undead, Golem etc.)
- [ ] 3.4 Habilidades raciais (passivas condicionais) e mecânicas exclusivas (ex.: tamanho de unidade, movimento, resistências, visão)
- [ ] 3.5 Casos avançados, um por vez, com tabela de cura/status explícita antes de cada um: Lobisomem (humano fora de batalha + formas de combate), Dragonborn (sopro), Vampiro (predação/recurso Sangue), Undead e Constructo (imunidades biológicas, cura diferenciada), Harpia (voo limitado), Merfolk (locomoção anfíbia), Centauro (galope/anatomia)
- [ ] 3.6 Acesso a Jobs: `JobCompatibilityRule` (bloqueios raros e justificados por anatomia/essência), afinidades culturais/raciais sem travas; High Elf como identidade social (Rede de Influência), sem bônus biológico de magia
- [ ] 3.7 Cultura e sociedade de cada raça (base para Lore — Estágio 6)
- [ ] 3.8 Como raça se conecta a facções e a território (ex.: recrutar uma raça exige confiança de seu povo) — ver `FACTIONS_AND_RECRUITMENT.md`
- [ ] 3.9 Regras de equipamento e sprites por anatomia (visual por forma/direção com fallback validado)
- [ ] 3.10 Balanceamento raça × Job e playtest

**Critério de conclusão:** montar um exército com raças diferentes muda a estratégia de forma perceptível.

---

### Estágio 4 — Montarias e Ocupação do Campo

**Objetivo:** montarias com presença tática real.

- [ ] 4.1 Definir tipos de montaria (cavalaria leve/pesada, feras, criaturas voadoras, máquinas)
- [ ] 4.2 Unidades multi-tile (ex.: 1×2, 2×2): regras de ocupação, giro, colisão, terreno estreito
- [ ] 4.3 Movimento e alcance de montarias (investida, arrancada, carga)
- [ ] 4.4 Regras de montar/desmontar; o que acontece se montaria ou cavaleiro cai
- [ ] 4.5 Voo e verticalidade (alcance, vulnerabilidades)
- [ ] 4.6 Montarias exclusivas de região/raça/facção (conexão com Estágio 7)
- [ ] 4.7 Ajustes de pathfinding, câmera e UI para unidades grandes
- [ ] 4.8 Playtest e balanceamento

**Critério de conclusão:** mapas com corredores/pontes/portões fazem a escolha de montar ou não ser uma decisão relevante.

---

### Estágio 5 — Batalhas em Grande Escala

**Objetivo:** permitir desde duelos até cercos massivos, com foco em imersão (batalhas longas são bem-vindas).

- [ ] 5.1 Definir escalas de batalha: pequena (emboscada/duelo), média (padrão), grande (exército), cerco
- [~] 5.2 Testar limites técnicos (nº de unidades em campo, desempenho, legibilidade visual) → feito: pathfinding com fila binária, IA limitada aos inimigos mais próximos, tiles do mapa em batching estático, mapas até 64×64 no editor, mapa de estresse (Tactics > Criar mapa de estresse: 40×40 com 60 unidades) e overlay de FPS (F3); falta: medir no Unity e decidir o teto de unidades e o orçamento para Android
- [ ] 5.3 Decidir e prototipar o modelo de unidades em massa: unidades individuais e/ou esquadrões (personagem + grupo)
- [ ] 5.4 Sistema de comandantes: auras, ordens, reorganização, habilidades de exército
- [ ] 5.5 Sistema de moral (confiança → abalado → fuga) e impacto de eliminar generais
- [ ] 5.6 Máquinas de guerra, portões, torres, muralhas e regras de cerco
- [~] 5.7 **Checkpoints condicionais em batalhas específicas:** infraestrutura BattleSave/BattleSnapshot v2 preservada; MVP 5A.4 removeu acesso irrestrito F5/F9, comandos Salvar/Carregar/Continuar save. **Futuro, não implementado:** sistema de checkpoints condicionado ao design de cada cenário. Definir pelo criador: batalhas elegíveis; eventos/condições de desbloqueio; ativação automática ou por confirmação; quantidade; sobrescrita; load/retomada; reuso ou consumo; RNG e tentativas; suspensão segura de batalhas muito longas. Não há condições aprovadas nem valores hardcoded.
- [~] 5.8 Ferramentas de conforto para batalhas longas: histórico de turnos, avanço de animações, resumo do estado, alerta de objetivos → feito: histórico (L), velocidade de animação 1x/2x/4x/instantâneo, inspeção de qualquer unidade; falta: resumo do estado da batalha e alerta de objetivos
- [~] 5.9 Fluxo de turno otimizado (sem cortar profundidade): fila clara, foco de câmera, atalhos → feito: fila de turnos, câmera segue a unidade da vez, atalhos de teclado, desfazer movimento; falta: ajustes após playtest de batalha grande
- [ ] 5.10 Playtest de batalha grande e ajustes de ritmo

**Critério de conclusão:** uma batalha de 15×20 (ou equivalente) é jogável, legível e pode ser pausada e retomada sem perda.

---

### Estágio 6 — Lore e Mundo (contínuo)

**Objetivo:** construir uma bíblia de lore rica em camadas, sem precisar da história pronta.

**Abordagem em camadas (do macro ao micro):**

- [ ] 6.1 **Camada 1 — Mito e origem:** cosmogonia, deuses/forças, criação das raças, eras (inspiração Tolkien: mito de criação, queda, eras longas)
- [ ] 6.2 **Camada 2 — Mapa e geografia:** continentes, regiões, clima, rotas, locais marcantes
- [ ] 6.3 **Camada 3 — Linha do tempo histórica:** grandes eventos, guerras antigas, origem das rivalidades
- [ ] 6.4 **Camada 4 — Povos e culturas:** cada raça com sociedade, religião, costumes, idioma/nomes, conflitos internos
- [ ] 6.5 **Camada 5 — Reinos e facções:** reinos, casas nobres, igreja/ordens, mercenários, rebeldes, povos independentes
- [ ] 6.6 **Camada 6 — Matriz de relações:** quadro reino × reino × facção (aliança, rivalidade, dívida, ódio, comércio) com **motivo concreto** para cada tensão
- [ ] 6.7 **Camada 7 — Situação atual:** o "agora" do jogo, o estopim da guerra, quem quer o quê
- [ ] 6.8 Definir tom e regras de escrita (nomes, convenções de idioma, glossário)
- [ ] 6.9 Criar glossário vivo e índice de lore
- [ ] 6.10 Esqueleto da história principal: premissa, protagonista, ato I/II/III, ganchos (detalhar por capítulo em 14)
- [ ] 6.11 Ganchos de lore escondida (livros, rumores, ruínas) para o sistema de segredos (Estágio 15)
- [ ] 6.12 Checagem de originalidade: garantir que nomes/conceitos não copiem obras existentes

**Critério de conclusão (mínimo para avançar):** matriz de relações + situação atual + premissa da história definidas. O restante evolui em paralelo.

---

### Estágio 7 — Campanha, Mundo Vivo e Consequências

**Objetivo:** guerra que continua existindo fora das batalhas do jogador.

- [ ] 7.1 Estrutura da campanha: capítulos, ramificações, pontos de decisão
- [ ] 7.2 Mapa do mundo explorável (nós/locais, descoberta, viagem, eventos) sem virar mundo aberto completo
- [ ] 7.3 Sistema de territórios: controle por facção, mudança de dono, efeito em lojas, preços, missões, NPCs, recrutamento
- [ ] 7.4 Simulação leve de guerra: eventos que ocorrem sem o jogador (cidades caem, fortalezas tomadas, rumores)
- [ ] 7.5 Catálogo de objetivos de batalha: capturar, sobreviver, escoltar, evacuar, sabotar, assassinar, impedir fuga, manter território, resgatar…
- [ ] 7.6 Resultados graduais: vitória, vitória com perdas, vitória parcial, derrota com continuação
- [ ] 7.7 Escolhas significativas (estilo "defender cidade / perseguir comandante / salvar civis") com consequência mensurável
- [ ] 7.8 Sistema de reputação por facção/raça e efeitos (acesso, aliados, montarias, classes)
- [ ] 7.9 Missões secundárias e descobertas por diálogo/exploração (sem marcador óbvio quando fizer sentido)
- [ ] 7.10 Ferramenta para escrever/testar eventos e ramificações (dados + flags)
- [ ] 7.11 Testar coerência: uma decisão do capítulo 2 aparece de fato no capítulo 5?

**Critério de conclusão:** duas decisões diferentes levam a estados de mundo diferentes e jogáveis.

---

### Estágio 8 — Exército, Personagens e Relações

**Objetivo:** cada unidade importa; gestão de exército sem virar 4X.

- [ ] 8.1 Design do protagonista: conceito, personalidade, arco, visual (conecta com 6.10 e 10)
- [ ] 8.2 Elenco principal: companheiros, rivais, antagonistas (fichas curtas)
- [ ] 8.3 Recrutas genéricos: geração com origem, raça, profissão, personalidade, ambição, medo
- [ ] 8.4 Sistema de traços (Veterano, Temerário, Leal, etc.) com bônus **e** custos
- [ ] 8.5 Relações entre unidades (amizade, rivalidade, parentesco, admiração, ódio) e efeitos em combate/eventos
- [ ] 8.6 Eventos de personagem (diálogos, missões pessoais)
- [ ] 8.7 Sistema de ferimentos: ferido → incapacitado por N batalhas → recuperação → morte (opções de dificuldade)
- [ ] 8.8 Gestão de exército (recursos leves: dinheiro, suprimentos, tropas, montarias)
- [ ] 8.9 Moral do exército na campanha e sua ligação com o moral em batalha
- [ ] 8.10 Base/acampamento como refúgio (conecta com pilar "conforto" e Estágio 10)

**Critério de conclusão:** o jogador sente falta de uma unidade específica quando ela está ferida.

---

### Estágio 9 — Inteligência Artificial

**Objetivo:** inimigos com doutrina militar, não apenas números maiores.

- [~] 9.1 Arquitetura de IA (behavior tree, utility AI ou similar) e ferramentas de debug → feito: interface `IAiBehavior` (ponto de extensão para doutrinas), plano com motivo, opções avaliadas e tempo de cálculo no overlay (F3); falta: escolher a arquitetura definitiva quando as doutrinas estiverem definidas
- [ ] 9.2 Doutrinas: cavalaria, magos, assassinos, defensivos, guerrilha, cerco
- [ ] 9.3 IA por objetivo (defender ponto, escoltar, fugir, invadir)
- [ ] 9.4 IA de comandante e resposta à moral (recuo, reorganização)
- [ ] 9.5 IA em grande escala (formações, flancos, coordenação de esquadrões)
- [ ] 9.6 Níveis de dificuldade por comportamento (não só HP/dano)
- [ ] 9.7 Playtest cego para checar previsibilidade e frustração

**Critério de conclusão:** dois exércitos diferentes exigem táticas diferentes do jogador.

---

### Estágio 10 — Direção de Arte e Ambientação (contínuo)

**Objetivo:** visual coerente e acolhedor.

- [ ] 10.1 Guia de estilo (paleta, iluminação, silhuetas, proporções, texturas)
- [ ] 10.2 Definir pipeline de arte (conceito → modelo/sprite → animação → integração)
- [x] 10.2a Documentar o processo reutilizável de personagens em `Docs/Art/CHARACTER_PIPELINE.md` (produção para qualquer raça ou classe) → criado com 9 etapas, 3 quality gates e distinção explícita concept art ≠ sprite de produção
- [~] 10.2b **Human Warrior Pilot** — primeiro MVP de integração de personagem (`Docs/Art/Characters/HUMAN_WARRIOR_PILOT.md`) → documentação e auditoria de integração feitas; piloto autorizado apenas como asset de teste visual/técnico que pode representar temporariamente o `Hero` em `Proving`; **não é o protagonista definitivo** e não cria dependência do sistema de Jobs (`Warrior`/`Knight` só existem no catálogo). Marcos planejados, nenhum concluído sem implementação e validação:
  - [~] MVP 1 — sprite estático do guerreiro como visual do `Hero` na batalha `Proving` → **implementado em 2026-10-10** (menor mudança na Presentation: novo `UnitVisuals` + filho billboard opcional no `UnitView`; sprite movido para `Resources` com GUID preservado; Core, regras, mapa e cena intactos; compilação validada). **Polimento 2026-10-11** após 1ª passagem PlayMode do criador: escala visual ×1,15 configurável por personagem (`UnitVisuals.ScaleFor`), indicador de facing "Front" movido para o chão (não cobre a arte) e sombra de contato presa ao tile. **Aprovação visual do criador (2026-10-11): escala ×1,15 e apresentação do sprite aprovadas.** Itens de regressão PlayMode não executados (seleção/undo/save-load/derrota/zooms/sombra) permanecem **explicitamente não verificados**
  - [x] MVP 2 — direções para o billboard (4 diagonais cobrendo 100% dos estados visíveis; +4 cardinais futuros) → **implementado, auditado e fechado (2026-10-11)**: revisão PlayMode inicial do criador aceitou as 4 vistas e a seleção direcional (mapping 16 combinações congelado em `DirectionMappingTests`, 25 checagens executadas — 0 falhas; seleção corrigida para vista mais próxima `RoundToInt((d+45)/90)`); leitura "ataca de lado" diagnosticada como limitação da arte estática sem pose de ataque (depende do MVP 4). **Ressalvas de fechamento**: suíte completa do Unity Test Runner e regressão PlayMode ampla (save/load, undo, derrota, zooms) **não executadas**; consistência da mão da espada (possíveis `front_l`/`front_r` espelhadas; `back_r` sem espada visível) pendente de decisão de arte — `HUMAN_WARRIOR_DIRECTIONS.md` §8
  - [~] MVP 3 — Idle + Walk (Idle migrou do MVP 2) → **MVP 3A/3B/3C implementados (3C visualmente APROVADO após reteste PlayMode) e MVP 3D integrado (2026-10-11)**: Idle nas **4 direções** (16 quadros: `front_r` 3A; `front_l`/`back_r`/`back_l` 3C integrados **sem alteração de runtime** — o carregador já sondava as 4 vistas) e Walk nas **4 direções** (24 quadros: `front_r` 3B validado; `front_l`/`back_r`/`back_l` 3D descobertos automaticamente — **zero alterações de runtime**) via frame controller leve — `UnitVisuals` cacheia/sonda os clipes por vista (`IdleFramesFor`/`WalkFramesFor`), `UnitView` centraliza a seleção no `LateUpdate` (`IdleFrameIndex`/`WalkFrameIndex` puros e testados — 154 checagens executadas, 0 falhas); Walk avança pelo MESMO `t` da interpolação do `MoveAlong` (sem relógio extra, sem multiplicar velocidade; fase contínua por passo cumulativo; estado resetado em `finally`); incidente "respiração só em front_r" resolvido com reimport dos assets (causa consistente com import desatualizado/cache estático — não reproduzida em código; F e meta estrutural descartados por evidência) e **cache de clipes endurecido** (re-sonda enquanto houver direção sem clipe — cobre Reload Domain desabilitado); diagnósticos temporários removidos após aprovação; **cubo branco "Front" desligado nas unidades com sprite** (renderer off; Facing do Core e F3 intactos — pedido do criador). **3D aguarda aprovação visual PlayMode**; **ressalva permanente: regressão PlayMode ampla (undo/save/load/derrota/zooms) não executada como suíte.** Attack = MVP 4 — `Docs/Art/Characters/HUMAN_WARRIOR_ANIMATIONS.md`
  - [~] MVP 4 — Attack (golpe alinhado à rotina melee atual) e reações de dano/derrota → **integrado como MVP 4 (2026-10-11)**: 52 quadros em `Animations/{Attack,Hit,Defeat}/` (5/3/5 por vista × 4 direções) tocados como estado transitório de combate em `UnitView` (`PlayOneShot`/`PlayDefeat`, precedência Defeat > Hit > Attack > Walk > Idle) — Attack dispara em qualquer ataque (incl. tile vazio) junto do `SetFacing`; Hit só quando o golpe ACERTA; Defeat trava o visual até a view sumir (o `Vanish` existente continua; gameplay inalterado). **Defeito de import corrigido**: os 52 metas vieram como textura default (textureType 0) e foram convertidos para Sprite/Single/PPU 100/Point preservando os GUIDs. **Aguardando aprovação visual PlayMode**; esquivas continuam com o desvio procedural (sem clipe)
  - [ ] MVP 5 — registrar como asset visual reutilizável na biblioteca de personagens
- [x] 10.2c **Character Production Pipeline v1.0** consolidada (`Docs/Art/CHARACTER_PIPELINE.md`) → **estabelecida em 2026-10-11** a partir do piloto validado (MVP 1–4): processo completo para humanoides de 1 tile (4 vistas de tela, contratos de Idle/Walk/Attack/Hit/Defeat com contagens e timing verificados no código, padrão de import com procedure de validação, integração Presentation passo a passo, checklist de 16 itens de PlayMode, gates do criador e critérios de aceite) + template reutilizável (`Docs/Art/Characters/CHARACTER_TEMPLATE.md`) + auditoria de reuso (carregador genérico é reutilizável; gate `IsWarriorPilot`/caminhos é específico do piloto — generalizar é o 1º passo do 2º personagem) + política **weapon-independent** então documentada como requisito futuro; a decisão visual de 2026-10-19 tornou-a obrigatória para personagens novos (espada do piloto = exceção histórica; equipamento swappable NÃO implementado). **Distinção explícita: protótipo aprovado ≠ pronto para produção** — regressão ampla continua pendente. Próximo uso real: produzir e integrar o 2º humanoide seguindo o pipeline
- [ ] 10.3 Cenário-piloto (ex.: uma vila/refúgio + um campo de batalha) como referência de qualidade
- [ ] 10.4 Design do protagonista (arte final, expressões, variações) — decisão independente do Human Warrior Pilot (10.2b), que é apenas piloto visual e não o herói narrativo
- [ ] 10.5 Design visual de raças (silhuetas distinguíveis mesmo em zoom-out)
- [ ] 10.6 Designs de classes (leitura rápida em campo: arma, silhueta, cor)
- [ ] 10.7 Design de montarias e criaturas
- [ ] 10.8 Biblioteca de tiles/tilesets por bioma (floresta, montanha, castelo, cidade, pântano…)
- [ ] 10.9 Ciclo dia/noite, clima e efeitos que reforcem o sentimento de refúgio
- [~] 10.10 Efeitos visuais de habilidades (VFX) e feedback de combate → feito (provisório, sem arte): avanço de espada e machado, flecha em arco, desvio em golpe errado, brilho e empurrão no alvo, tremor de câmera, números de dano flutuantes; falta: VFX reais e animações por classe
- [ ] 10.11 Retratos e cutscenes/ilustrações-chave
- [ ] 10.12 Mapa do mundo ilustrado

**Critério de conclusão:** o cenário-piloto transmite o "clima" desejado e serve de régua para o resto.

---

### Estágio 11 — Áudio e Trilha Sonora (contínuo)

- [ ] 11.1 Definir identidade musical (instrumentação, temas, referências)
- [ ] 11.2 Tema principal do jogo
- [ ] 11.3 Temas por região/facção/raça (leitmotifs)
- [ ] 11.4 Músicas de batalha por escala (pequena, grande, cerco, chefe)
- [ ] 11.5 Música de refúgio/acampamento e de exploração
- [~] 11.6 Efeitos sonoros (combate, UI, ambiente, montarias) → feito: serviço de áudio com sons de teste sintetizados (golpes, flecha, acerto, crítico, erro, passos, UI, vitória/derrota) e `SoundBank` para trocar por sons reais sem mexer em código; falta: os sons reais, ambiente e montarias
- [ ] 11.7 Sistema de música adaptativa (moral, fase da batalha)
- [ ] 11.8 Dublagem/vozes (decidir: nenhuma, parcial, total)
- [ ] 11.9 Mixagem e implementação

---

### Estágio 12 — Interface e Experiência (UI/UX)

- [ ] 12.1 Princípios de UI (leitura clara em batalhas grandes, estilo coerente com a arte)
- [~] 12.2 Wireframes: menu principal, mapa-múndi, acampamento, batalha, edição de classes/build → feito (provisório): menu principal com lista de mapas, menu de pausa e opções, batalha; falta: mapa-múndi, acampamento e edição de builds
- [~] 12.3 HUD de batalha (fila de turnos, previsão de dano, altura, alcance, moral) → feito: fila de turnos, menu de comandos em abas, previsão de ataque (ângulo, altura, acerto, dano, crítico), alcance de movimento e ataque, painel de status de qualquer unidade, histórico; falta: moral e visual final
- [ ] 12.4 Câmera e controles (mouse/teclado, controle, possivelmente toque)
- [ ] 12.5 Tutorial integrado e onboarding progressivo
- [ ] 12.6 Interface de diplomacia/territórios/relações
- [~] 12.7 Acessibilidade (daltonismo, legendas, tamanho de fonte, velocidades) → feito: paleta para daltonismo, tamanho da interface (100% a 200%), velocidade de animação; falta: legendas (quando houver diálogos) e revisão de contraste
- [x] 12.8 Opções de qualidade de vida: velocidade de animação, desfazer movimento, salvar/retomar → opções salvas em PlayerPrefs (animação, volumes, interface, daltonismo, FPS); desfazer movimento; snapshots internos preservados, save/load livre removido no MVP 5A.4
- [~] 12.9 **Menu de comandos contextual/recolhível** (meta aprovada pelo criador; candidato a entrar no início da integração do sistema de habilidades, se de baixo risco): recolher/reabrir à vontade durante o turno da unidade atual; fechar NÃO consome ação/movimento/turno; permitir inspecionar o mapa e usar câmera com o menu oculto; acesso por teclado/mouse sem conflitar com atalhos existentes; comportamento compatível com Escape/pausa e com o modo de mira de ações
  - **MVP 5A.1 (2026-10-12) implementado:** controles Recolher/Abrir, seleção preservada e confirmação de cliques bloqueada com painel oculto; abertura a cada turno/load e comandos táticos bloqueados para IA. Core/Presentation compilados; 175 casos Core passaram em runner externo, incluindo restore repetido após dano/kill de Corte Pesado. F5/F9 posteriormente removidos no MVP 5A.4; interação IMGUI e Console em PlayMode **pendentes do criador**; checklist em `Docs/MVP_5A_HEAVY_SLASH.md`. Não conclui o Estágio 12 nem configuração/escala/expansão da fila.
  - **MVP 5A.3 implementado (2026-10-12):** modos Comandos/Mira/Inspeção separados, Voltar contextual e destaques limpos na inspeção; direção final 5A.2 preservada. Substitui a simples ocultação da mira do 5A.1. Compilação externa e regressões Core realizadas; entrada real PlayMode pendente.
- [~] 12.10 **Fila de turnos configurável** (meta aprovada pelo criador): modos compacto/expandido/oculto; identificação clara aliado × inimigo; unidade atual, próximas ativações e CT quando relevante; previsão baseada no `TurnManager` real (sem garantir ordem futura quando CT/velocidade mudam); legível em batalhas com muitas unidades
  - **MVP 5A.3 implementado:** recolhido/compacto 6/expandido 18 com scroll, texto aliado/inimigo, CT atual/velocidade, previsão pelo TurnManager e preferência em GameSettings/PlayerPrefs. 196 casos Core externos passaram; reinício real da aplicação e legibilidade em batalha grande aguardam validação. Configuração ampla e redução de sobreposição permanecem no Estágio 12.
- [ ] 12.11 **HUD de batalha escalável e sem poluição** (meta aprovada pelo criador): visibilidade e tamanho dos painéis configuráveis e persistentes entre sessões; rótulos/HP contextuais; reduzir sobreposição de rótulos em unidades agrupadas; não obstruir tiles importantes do mapa; **critério de aceite explícito: legibilidade em batalhas de grande escala**. O MVP 5C.1 reduziu a poluição do cursor (quadro fino em vez de bloco) e encurtou a árvore de comandos, mas **não fecha este item**: a legibilidade do menu/hover em batalhas grandes continua pendente de PlayMode.
- [ ] 12.12 Nota de timing de UX: a 12.9 (menu recolhível) é a melhoria pequena recomendada para o INÍCIO da integração do sistema de habilidades (baixo risco, alivia poluição já percebida no playtest de A Passagem); 12.10/12.11 e revisão maior de HUD pertencem ao Estágio 12 e à validação de batalhas em grande escala

---

### Estágio 13 — Vertical Slice

**Objetivo:** provar o jogo inteiro em miniatura.

- [ ] 13.1 Escolher escopo: 1 capítulo com introdução, 3–5 batalhas (incluindo 1 grande), 1 hub, 1 decisão com consequência
- [ ] 13.2 Integrar: classes, raças, montaria, moral, save em batalha, território mudando
- [ ] 13.3 Arte, áudio e UI em qualidade próxima ao final
- [ ] 13.4 Playtest externo (amigos/comunidade) com formulário estruturado
- [ ] 13.5 Revisar pilares e escopo com base no feedback (atualizar este roadmap)

**Critério de conclusão:** alguém de fora joga por algumas horas e entende a proposta do jogo.

---

### Estágio 14 — Produção de Conteúdo

**Objetivo:** produzir o jogo completo, capítulo a capítulo (ciclo repetível).

Ciclo por capítulo:

- [ ] 14.x.1 Roteiro do capítulo (cenas, diálogos, decisões)
- [ ] 14.x.2 Mapas de batalha e objetivos
- [ ] 14.x.3 Novos inimigos/doutrinas
- [ ] 14.x.4 Novos personagens/recrutas
- [ ] 14.x.5 Arte, música e eventos exclusivos
- [ ] 14.x.6 Integração + playtest + balanceamento
- [ ] 14.x.7 Atualização da lore e do estado de mundo

Tasks transversais:

- [ ] 14.a Expansão das classes (completar a árvore)
- [ ] 14.b Expansão de equipamentos e itens
- [ ] 14.c Expansão de localizações do mundo
- [ ] 14.d Localização/tradução (planejar cedo)

---

### Estágio 15 — Extras, Segredos e Rejogabilidade

- [ ] 15.1 Classes, raças e personagens secretos (com pistas na lore)
- [ ] 15.2 Armas lendárias e mapas secretos
- [ ] 15.3 Dungeons sequenciais (recursos limitados, eventos, escolhas, recompensas)
- [ ] 15.4 Bosses opcionais e superbosses
- [ ] 15.5 Finais alternativos e eventos raros
- [ ] 15.6 Segredos descobertos por investigação (sem marcador de missão)
- [ ] 15.7 New Game+ (inimigos remixados, novas quests, manter personagens)
- [ ] 15.8 Modos de desafio (permadeath, limite de nível, classes restritas, randomizer)
- [ ] 15.9 Enciclopédia/bestiário/registro de descobertas

---

### Estágio 16 — Polimento, Testes e Lançamento

- [ ] 16.1 Balanceamento geral e passe final de dificuldade
- [ ] 16.2 Otimização e estabilidade (batalhas grandes, save/load)
- [ ] 16.3 QA sistemático (bugs de save, progressão, ramificações)
- [ ] 16.4 Consistência final de lore, textos e localização
- [ ] 16.5 Página de loja, trailer, materiais de divulgação
- [ ] 16.6 Estratégia de lançamento (demo, acesso antecipado ou lançamento direto)
- [ ] 16.7 Pós-lançamento: correções, feedback, conteúdo adicional

---

## 6. Princípios de design (para guiar decisões futuras)

1. **Escolha > número:** preferir decisões interessantes a estatísticas maiores.
2. **Todo poder tem preço:** trade-offs em habilidades, traços e equipamentos.
3. **Sistemas conversam:** toda nova mecânica deve dizer com quais outras interage.
4. **A guerra é maior que o herói:** o mundo reage e continua fora da tela.
5. **Tempo é bem-vindo:** profundidade e imersão antes de ritmo acelerado; conforto para pausar (saves).
6. **Legibilidade primeiro:** mesmo com muitas unidades, o jogador precisa entender o que acontece.
7. **Refúgio:** locais de descanso e beleza são parte da experiência, não decoração.
8. **Originalidade:** absorver a essência das inspirações, não seus elementos.

---

## 7. Perguntas em aberto

- ~~Engine e estilo visual~~ → resolvido: Unity + C#, HD-2D / 2.5D (ver seção 9)
- Estrutura inicial de referência (FFT Ivalice Chronicles / Triangle Strategy): quais elementos exatos seguir (câmera, fluxo de capítulo, tela de batalha, sistema de escolhas)?
- Orçamento técnico de desempenho para futura versão Android (nº de unidades, efeitos) — definir antes do Estágio 5
- Batalhas grandes: unidades individuais, esquadrões ou modelo híbrido?
- Sistema de progressão: JP/pontos de classe estilo FFT ou algo novo?
- Nível de morte permanente (opcional, obrigatório, por dificuldade)?
- Jogo single-player apenas ou modos extras (arena, PvP assíncrono)?
- Quantas raças jogáveis e quantas não jogáveis no lançamento?
- Nível de dublagem?
- Protagonista fixo ou personalizável?
- Escala de campanha (nº de capítulos e de horas)?

---

## 8. Ordem sugerida das primeiras tasks

1. 0.1 Pitch + 0.3 Engine
2. 1.1 Regras centrais no papel
3. 6.1–6.3 Mito, geografia, linha do tempo (rascunho curto)
4. 1.2–1.5 Protótipo de grid, movimento e ataque
5. 10.7/0.7 Moodboard e cenário-piloto conceitual
6. 2.1–2.3 Estrutura de builds e princípios de balanceamento
7. 6.5–6.7 Reinos, facções e matriz de relações
8. 1.13 + 5.7 Base para save/load durante batalha
9. Voltar ao Estágio 3 (Raças) com a lore mais sólida

---

## 9. Registro de decisões

| Data | Decisão | Motivo | Impacto |
|---|---|---|---|
| 2026-10-12 | Manual unrestricted save/load during combat is not allowed. Some specific battles may support in-battle checkpoints, enabled only when creator-defined scenario conditions are satisfied. Conditions and eligible battles will be defined later. | Evitar save scumming irrestrito, preservando checkpoints adequados ao cenário; substitui F5/F9/UI/Continuar save anteriores. MVP 5A.4 implementado e compilado; 196 casos Core passaram em runner externo; PlayMode pendente | 1.13, 5.7, 12.8; snapshots v2 preservados |
| 2026-09-30 | **Acesso irrestrito substituído pelo MVP 5A.4**; salvar em batalha permanece planejado via checkpoints condicionais | Valor do projeto: prazer em "perder tempo" | Estágios 1, 5, 12 |
| 2026-09-30 | Raças e classes com estética clássica (orcs, trolls, anões etc.) e nomenclatura própria | Preferência do autor | Estágios 2, 3, 6 |
| 2026-09-30 | História escrita em paralelo ao desenvolvimento | Lore ainda em construção | Estágios 6, 7, 14 |
| 2026-09-30 | Engine: Unity + C# | Suporte oficial a console no futuro, pipeline maduro de Android, `ScriptableObject` para dados de classes/raças/habilidades | Todos os estágios; 0.3 |
| 2026-09-30 | Plataformas: PC/Steam primeiro; Android após lançamento estável; console possível no futuro | Foco em entregar um lançamento estável antes de expandir | 5.2, 12.4, 16 |
| 2026-09-30 | Estilo visual: HD-2D / 2.5D (mapas 3D + sprites 2D), próximo de FFT Ivalice Chronicles e Triangle Strategy | Combina com grid com altura e com o pilar de refúgio/cenários bonitos | Estágios 1, 10, 12; 0.4 |
| 2026-09-30 | Lógica de regras separada da apresentação (C# puro) | Viabiliza save em batalha, desfazer, histórico de turnos e testes automatizados | 1.13, 5.7, 5.8, 12.8 |
| 2026-10-10 | Human Warrior Pilot é o primeiro MVP de integração de personagem: apenas asset visual/técnico, pode representar temporariamente o `Hero`; não é protagonista canônico e não autoriza nova raça/Job/habilidade (`Docs/Art/Characters/HUMAN_WARRIOR_PILOT.md`, `Docs/Art/CHARACTER_PIPELINE.md`) | Validar pipeline de arte e leitura tática antes de produzir elenco; evitar acoplamento prematuro com o sistema de Jobs ainda não implementado | Estágio 10 (10.2a/10.2b); nenhum impacto em Core, Jobs ou narrativa |
| 2026-10-10 | MVP 1 do piloto implementado: sprite estático carregado por `Resources.Load<Sprite>` e aplicado apenas ao `Hero` (time 0, unidade-chave, nome "Hero" do `MapData`) via novo `UnitVisuals.SpriteFor` + filho billboard opcional no `UnitView` (raiz com escala uniforme 1; cápsula escondida; facing tático preservado pelo cubo "Front") | Menor seam reutilizável na Presentation, sem tocar o Core; compatível com os giros de 90° da câmera sem espelhar a arte assimétrica | Estágio 10 (10.2b); detalhes e limitações em `Docs/Art/Characters/HUMAN_WARRIOR_PILOT.md`; conclusão pendente de validação PlayMode |
| 2026-10-10 | **Regra canônica v2.1:** todas as habilidades (Jobs, raciais, magias, invocações, transformações, técnicas) e o desbloqueio de Jobs avançados/secretos são exclusivamente por árvores de talentos e progressão; sem exploração, captura, contratos, pactos, rituais, missões, itens ou NPCs como gatilho. Recrutamento de personagens para o grupo permanece narrativo | Uniformizar a progressão e eliminar dependências de conteúdo narrativo no desbloqueio | Estágio 2 (2.5, 2.8); `Docs/GameDesign/*` revisados; futura implementação precisa de `TalentTreeDefinition`/`TalentNode` + persistência |
| 2026-09-30 | Regras de gameplay documentadas em `docs/GAMEPLAY.md`; roadmap e docs ficam em `TacticsRPG/docs/` (fora de `Assets`) | Separar "o que fazer" (roadmap) de "como o jogo funciona hoje" | 0.6 |
| 2026-09-30 | Movimento estilo FFT: Move/Jump, custo por terreno, aliados atravessáveis, inimigos bloqueiam | Base do núcleo tático; valores provisórios | 1.3 |
| 2026-09-30 | Ataque por ângulo: costas ×1,5 de dano e sem esquiva, lado ×1,15 e meia esquiva, frente dano normal e esquiva total | Recompensa posicionamento e flanco; valores provisórios | 1.5, 1.6 |
| 2026-09-30 | Turnos por CT (estilo FFT): 1 movimento + 1 ação em qualquer ordem, CT de volta menor para quem faz menos, direção escolhida ao fim do turno | Faz o flanco ter contrapartida defensiva e recompensa esperar; valores provisórios | 1.1, 1.4 |
| 2026-10-12 | Final facing follows FFT-style action order: Move → Attack locks facing toward the target; Attack → Move permits manual final-facing selection; Attack Only preserves attack-facing; Move Only/Wait permit manual facing selection. Substitui a regra anterior de trava após qualquer ataque e a proposta de seleção manual após todo ataque | Decisão aprovada pelo criador; distinguir ordem sem alterar orçamento ou CT | MVP 5A.2; 1.4, 1.5, 2.1A; snapshot v2 preservado |
| 2026-10-18 | **Substitui a cláusula "Attack Only preserves attack-facing" do MVP 5A.2:** a direção final só é travada quando a unidade **já se moveu** E a última coisa feita foi uma ação ofensiva (`FacingLocked = ofensivo ∧ HasMoved`); Atacar → Esperar sem movimento, Atacar → Mover, Só atacar, Só mover e Só esperar abrem escolha manual. Correção pedida pelo criador (o caso Atacar → Esperar encerrava sem permitir escolher a direção) | O custo de posicionamento deve existir só quando a unidade de fato se posicionou; suporte (Cura/Proteção) nunca trava; confirmar direção não gasta ação nem CT | MVP 5C.1; 1.4, 1.5, 2.1A; snapshot v2/v3 preservados (`facingLocked` continua serializado e restaurado) |
| 2026-10-18 | **Navegação após execução e desfazer por atalho (MVP 5C.2):** ação/movimento **executados** devolvem o menu à página Principal enquanto o turno do jogador continua; cancelar a mira volta ao submenu que a lançou, e tile inválido/habilidade não autorizada/prévia/recusa do Core mantêm a mira sem navegar; o item "Desfazer movimento" sai do menu e desfazer volta a existir **só** no atalho Backspace, distinto de Voltar/Esc | Fricção de navegação apontada pelo criador em PlayMode (o submenu de origem ficava aberto depois de atacar/curar); desfazer continua sendo recuperação do movimento antes de agir, mas não precisa de botão permanente | MVP 5C.2; §3.1D/§3.1E de `GAMEPLAY.md`; 1.1, 1.4; nenhuma mudança de CT, orçamento de movimento, direção final ou snapshot |
| 2026-09-30 | **Substituída pelo MVP 5A.2 (2026-10-12):** regra anterior de que todo ataque impede escolha final, inclusive após mover posteriormente | Igual ao FFT: atacar tem custo de posicionamento | 1.1, 1.5, 1.7 |
| 2026-09-30 | Alcance vertical depende da arma (padrão 1 para todas; categorias futuras definem o seu); arco usa linha de visão em vez de limite de altura | Altura importa sem engessar armas futuras | 1.5, 2.9 |
| 2026-09-30 | Crítico base fixo só para golpes de lado (10%) e costas (20%); arma e unidade somam bônus (classe, raça, habilidades entram depois) | O usuário quer crítico dependente de arma/classe/raça/habilidade, com uma base para flanco | 1.6, 2.x, 3.x |
| 2026-09-30 | Infraestrutura sem depender de conteúdo criativo feita em paralelo: feedback de combate provisório, serviço de áudio com `SoundBank`, opções e acessibilidade, menus, histórico, ferramentas de depuração da IA e de desempenho | Adiantar o que não depende de raças, classes, história, arte e sons finais | 5.x, 9.1, 10.10, 11.6, 12.x |
| 2026-09-30 | Qualquer unidade (aliada ou inimiga) pode ser inspecionada a qualquer momento: mouse em cima mostra o status e o botão direito fixa | Planejar a jogada exige conhecer os atributos dos inimigos, como no FFT | 12 |
| 2026-09-30 | Altura altera o dano em 4% por nível, limitada a ±20% | O usuário pediu altura no dano sem exagerar no scaling | 1.1, 1.6 |
| 2026-09-30 | O movimento pode ser desfeito até a unidade agir (volta ao tile e à direção do início do turno) | Permitir repensar a jogada, como em FFT; atacar confirma | 1.3 |
| 2026-09-30 | Menu de comandos compacto em abas (Ação, Info, Sistema) e barra de avisos fina | O menu anterior cobria muito da tela | 12 |
| 2026-09-30 | Arco com alcance base 2 a 6, +1 por 2 níveis de vantagem de altura (teto +3); desvantagem não reduz | Recompensa ocupar terreno alto; valores provisórios | 1.5 |
| 2026-09-30 | Câmera no padrão de Triangle Strategy: diagonal fixa, giro de 90°, 3 níveis de zoom, foco automático na unidade da vez | Referência pedida pelo autor | 1.2, 12 |
| 2026-09-30 | Editor de mapas compacto: uma barra e janelas pequenas sob demanda (tamanho, unidades, objetivos), sem formato novo de dados | Menos poluição visual; layout final ainda será decidido | 1.11 |
| 2026-09-30 | Save em batalha guarda todas as unidades (inclusive derrotadas) e o turno em andamento, em JSON; terreno vem do mapa | Objetivos dependem das unidades derrotadas; saves pequenos | 1.13, 5.7 |
| 2026-09-30 | Testes automatizados do `Core` em `Assets/Tests/EditMode` (NUnit, Test Runner do Unity): movimento, combate, knockback, turnos, objetivos, IA. Toda regra nova no `Core` entra com testes | Protege as regras enquanto a IA, as habilidades e o save/load passam a depender delas | 1.x, 2.x |
| 2026-10-11 | **Character Production Pipeline v1.0** estabelecida: `CHARACTER_PIPELINE.md` como documento central de produção de personagens (baseline verificada do piloto — 92 quadros de animação × 4 direções + estáticos; contratos Idle 4/Walk 6/Attack 5/Hit 3/Defeat 5 com timing real do código; import com procedure de validação; integração Presentation e testes), `CHARACTER_TEMPLATE.md` como especificação de novo personagem e auditoria de reuso (carregador genérico reutilizável; gate `IsWarriorPilot`/caminhos específicos do piloto). A espada embutida do piloto já era documentada como exceção ao objetivo weapon-independent | Evitar redesenhar o processo a cada personagem; um novo agente deve conseguir produzir/integrar outro humanoide só com os documentos; separar protótipo aprovado de pronto para produção | Estágio 10 (10.2c); nenhuma mudança de runtime nesta consolidação |
| 2026-10-19 | **Diretriz visual weapon-independent:** novos conceitos e sprites de personagem ficam sem arma; cada arma é asset separado e só aparece quando equipada e invocada por uma ação. A espada do Human Warrior Pilot permanece exceção histórica | Fazer do corpo/roupa do personagem o asset reutilizável e evitar armas visíveis sem contexto de equipamento/ação | Estágio 10; atualiza `ART_DIRECTION.md`, `CHARACTER_PIPELINE.md` e `CHARACTER_TEMPLATE.md`; overlay, encaixe, oclusão e sincronização em runtime continuam pendentes |

---

## 10. Backlog de ideias

- Dois níveis narrativos que se cruzam (pessoal ↔ geopolítico)
- Unidades individuais com motivações que geram eventos
- Rivalidade entre personagens que afeta combate (ex.: lutam melhor separados)
- Descoberta de segredos por rumores/livros, sem marcador de missão
- Verticalidade avançada (habilidades de altura, telhados, navios, muralhas)
- Facções internas dentro de cada raça (apoio a reinos diferentes)
- Dungeon com condição secreta (ex.: completar sem perder ninguém desbloqueia classe)
- Doutrina militar de cada facção refletida em unidades e IA

---

## 11. Template de task

```
Task: [nº e título]
Estágio: [nº]
Objetivo: [uma frase]
Contexto/dependências: [tasks, documentos de lore, decisões]
Entregável: [arquivo, protótipo, documento, asset]
Critério de pronto: [como saber que acabou]
Notas / decisões tomadas: [...]
Impacto em outros estágios: [...]
```

---

## 12. Histórico do documento

- 2026-09-30 — Versão inicial criada a partir da conversa de planejamento (inspirações, gaps de FFT, decisões de design).
- 2026-09-30 — Definidos engine (Unity + C#), plataformas (PC/Steam → Android → console futuro) e estilo visual (HD-2D / 2.5D). Tasks 0.3 e 0.4 concluídas.

## Character Art Direction Pipeline

### Current status
- Official character style anchor has been approved
- Reference file saved at:
  `Docs/Art/References/character_style_anchor_v1.png`
- Art direction documentation is being formalized in `Docs/ART_DIRECTION.md`
- New character concepts/sprites are weapon-independent; the Human Warrior Pilot's embedded sword is a historical prototype exception
- Runtime weapon assets/overlays are not implemented; action timing, hand anchors, and occlusion are future work

### Visual direction goals
- preserve tactical RPG readability
- maintain compact class-readable silhouettes
- blend classic tactical RPG identity with richer fantasy presentation
- use Final Fantasy Tactics, classic tactical RPGs, World of Warcraft, and Tolkien-inspired fantasy as style inspirations

### Next deliverables
1. Formalize `ART_DIRECTION.md`
2. Build initial core roster concepts
3. Approve first visual class lineup
4. Expand into races and named units
5. Begin converting approved concepts into production-ready assets
6. Define a standalone weapon-asset package and action-triggered runtime rendering contract

### First production roster
- Generic Knight / Swordsman
- Archer
- Mage
- Cleric
- Rogue / Thief
- Spearman
- Generic Enemy Soldier
- Generic Enemy Archer
- Generic Enemy Mage

### Future expansion
- race-specific variants
- kingdom / faction visual differentiation
- elite units
- named characters
- monster roster
