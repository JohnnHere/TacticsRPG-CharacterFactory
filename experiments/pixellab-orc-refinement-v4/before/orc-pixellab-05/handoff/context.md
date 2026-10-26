# Estado vigente — correção v3

PixelLab MCP instalado e usado. Ver docs/PIXELLAB_MCP.md e reports/orc-pixellab-refinement-v3.md. Rejeição do Idle regional v2 é autoritativa; não reutilizar compressão de faixas. Fonte visual atual: próprio concepts/concept-selected.png. Aprovação pendente. Textos abaixo são históricos quando conflitarem com a ficha/manifesto atual.

# Refinamento PixelLab v2 — contexto vigente

Este é um experimento visual independente. Para refinar animações, a única entrada de imagem é o conceito do próprio indivíduo. As referências globais descritas no contexto de fábrica abaixo são documentação de processo e não condicionamento visual desta experiência. Ver docs/PIXELLAB_ASEPRITE.md e reports/orc-pixellab-refinement-v2.md.

---

# Instrucoes da fabrica

# Character Factory — instrucoes para agentes

## PixelLab + Aseprite — pedido vigente de 2026-10-23

Criador autorizou instalar e usar a extensão oficial PixelLab no Aseprite. Essa autorização atualiza a restrição anterior a serviços/geração externa especificamente para PixelLab via Aseprite. Leia docs/PIXELLAB_ASEPRITE.md. Experimento atual: **três Orcs novos**, inspirados em Tolkien e principalmente World of Warcraft, sem consultar nem condicionar com V4, seus conceitos, a âncora, Hero, V5, paletas ou receitas legadas. Canvas vazio, texto e nenhuma imagem de entrada. Pode criar estudos candidatos de animações básicas antes da escolha, por autorização expressa deste pedido; isso não concede Gate1/Gate2 nem seleção de produção. A V4 permanece selecionada. Nesta experiência, não usar o handoff/prepare padrão que injeta referências antigas. Credenciais ficam só na instalação local; não versionar o pacote da extensão, configurações de conta ou tokens. Geração PixelLab é em nuvem, mestre salvo/edição/exportação no Aseprite; não confundir com desenho manual. Exportação batch usa perfil separado em tmp/aseprite-batch-profile para não executar plugins de interface.

## Direção Orc reafirmada — 2026-10-23

Orc clássico de fantasia medieval, principalmente WORLD OF WARCRAFT e também TOLKIEN. O criador delegou paleta, luz e textura ao agente e pediu cinco opções visuais concretas para escolher uma base e refiná-la. Usar o Orc Warrior como laboratório para uma identidade própria e um jogo com alma; evitar aparência genérica de IA com decisões de forma, material e acabamento. Leia docs/ORC_ART_LAB.md. Não pedir ao criador uma nova hipótese nem parâmetros técnicos que ele delegou. Candidatos não alteram a V4 selecionada e só escalam após revisão explícita. Toda autoria continua no Aseprite.

## Aseprite integrado

Decisao expressa do criador em 2026-10-22: **TODA a producao artistica deve acontecer no Aseprite**, incluindo conceitos, sprites, poses, animacoes e acabamento. `.aseprite` salvo e a fonte mestre; PNGs/folhas sao derivados. Autoria Lua executada no proprio Aseprite e permitida, com codigo/procedencia registrados e identificada como autoria programatica do agente. Nao confundir script com desenho manual ou com uma IA generativa do editor. Nao usar image_gen, reconstrucao de grade, recoloracao ou edicao raster externa para arte nova sem nova instrucao explicita do criador. Ferramentas externas podem organizar metadados, validar hashes/pixels e construir previews sem alterar a arte. Legados aprovados mantem sua procedencia original. Esta decisao substitui as instrucoes antigas que indicavam imagegen como fluxo padrao.

Para autoria/revisao/exportacao 2D, leia docs/ASEPRITE.md. Execute editor-check; o caminho desta maquina fica em config/aseprite.local.json ignorado pelo Git (ou ASEPRITE_PATH). Use editor-fork para preservar a fonte aprovada antes de editar, editor-template para fontes vazias novas, editor-export para builds/preview/metadados e editor-apply para slots baseline com gates/backup. Processos batch --noinapp ocultos permitem trabalhar sem disputar a GUI com o usuario. Exporte apenas arquivos salvos; nao controle a janela aberta quando o usuario estiver usando a maquina. Assets genericos de cenarios/props/efeitos/UI/armas/inimigos usam perfis explicitos; tilemap exportado nao implementa terreno 3D ou overlays no Unity. Auditoria de fontes ativas: node tools/audit-aseprite-production.mjs; exemplos sinteticos: node tools/verify-aseprite-capabilities.mjs. Preserve os gates e os exportadores de acoes existentes.

Para melhorias de arte aprovada, partir da fonte/pixels aprovados por fork e retocar no Aseprite, preservando rosto, anatomia, roupa e acabamento. Nao substituir por um redesenho generico de coordenadas como a V3 rejeitada pelo criador. V4 e estudo de retoque sobre V2: reports/orc-aseprite-v4/review.html. Diferenciar procedencia herdada de novas alteracoes; nao chamar uma imagem importada/retocada de autoria integral do zero. Alteracoes numericas, camadas e exportacao correta nao comprovam melhoria artistica.

Objetivo: criar personagens e variantes em sprites 2D de pixel art refinada para TacticsRPG. Leia README.md, docs/VISUAL_IDENTITY.md, docs/WORKFLOW.md, docs/ROADMAP.md e references/manifest.json. Execute doctor. O usuario descartou ComfyUI, personagens modelados em 3D e assinatura de servico especializado em sprites. Use os comandos locais e, quando disponivel, a ferramenta de imagem da conversa. Nenhuma chave de API e necessaria para os comandos desta fabrica.

## Continuidade e destinos padrao

Esta pasta e a fabrica do projeto irmao ../TacticsRPG. Um pedido curto como "crie um Orc Warrior" ja se refere a esse jogo, a identidade visual e as fontes locais. Nao exigir que o usuario repita o nome do projeto, o estilo, a ancora, a funcao do Hero ou os destinos em cada prompt. Esta instrucao so acompanha agentes com acesso a este repositorio; em ferramenta externa, carregar o pacote handoff com suas imagens/contexto.

Inferir a etapa pelo pedido e pelo estado real de character.json, reviews.json, assets.json e arquivos presentes. Retomar o personagem indicado; se nao houver ID, escolher ID livre e informar. Pedidos de roupa preservam o individuo existente. Distinguir novo individuo de nova variante. Persistir as decisoes do usuario no pacote e os proximos passos em docs/ROADMAP.md ao concluir a sessao. Reviews e hashes prevalecem sobre resumos textuais de progresso.

Destinos: conceitos em characters/<id>/concepts/; arquivos editaveis do editor e pecas em characters/<id>/source/; PNGs nativos em characters/<id>/sprites/; instrucoes/contexto em handoff/; validacoes em reports/; receitas aprovadas em recipes/<races|jobs>/<id>/vN/; exportacao de revisao em dist/<id>/<build>/Assets/Resources/Characters/<id>/. Sempre importar/copiar resultados da ferramenta de imagem para o pacote, mesmo que a ferramenta inicialmente salve em pasta temporaria. Criar previews e informar os caminhos reais.

## Regra de armas independentes

Conceitos e sprites base do personagem ficam sem armas empunhadas, carregadas ou embainhadas. Armas sao assets separados, equipados e exibidos somente quando uma acao/animacao os invocar; a identidade do Job deve continuar legivel sem a arma. A espada embutida do Human Warrior Pilot e excecao historica do prototipo, nao modelo para personagens novos. A fabrica ainda nao possui pacote/comando proprio para assets compartilhados de armas e o runtime atual nao possui overlay dinamico por arma; registrar essa extensao como pendente e nao simular suporte no jogo.

O destino final de uma integracao autorizada e ../TacticsRPG/Assets/Resources/Characters/<id>/. Exportar e preparar pacotes fazem parte da fabrica; copiar/registrar dentro do jogo depende da tarefa de integracao autorizada, pois UnitVisuals ainda precisa de extensao. Manter revisoes artisticas nos marcos previstos, sem solicitar reconfirmacoes para trabalho local ja autorizado.

Padrao complementar de equipamento/acao: leia docs/EQUIPMENT_AND_ACTIONS.md e config/equipment-actions-v1.json. Corpo desenhado com maos vazias nao significa ataque desarmado. O comando Atacar deve ter movimento fisico sem arma para cada personagem/anatomia; selecionar clipes pela acao/equipamento real, sem converter automaticamente o ataque basico em magia pelo Job. Suplementos de acao, sockets, oclusao e eventos precisam de evidencia propria; nao os declarar prontos por completar os97 PNGs legados. Consulte a matriz characters/orc-equipment-actions-v1.json e reports/orc-equipment-readiness-v1.json.

## Fontes e hierarquia

Pedido explicito vigente > decisoes expressas de design > documento tematico mais recente > propostas antigas. Leia references/tacticsrpg/Docs/GameDesign/DOCUMENT_INDEX.md e DESIGN_DECISIONS.md. ART_DIRECTION.md e a ancora definem estilo; CHARACTER_PIPELINE.md define processo. Os snapshots preservam exatamente o estado local na sincronizacao; podem incluir alteracoes nao commitadas. Manifesto SHA256 e evidencia da versao copiada. Consulte o projeto original somente para verificar atualizacoes; altere-o apenas quando houver autorizacao de integracao.

Inspecione visualmente references/tacticsrpg/Docs/Art/References/character_style_anchor_v1.png e os PNGs do Hero pertinentes antes de gerar. Ancora e linguagem global; o Human Warrior Pilot e referencia de implementacao/leitura e prototipo. Nao o tornar protagonista final, uniforme, anatomia ou paleta universal. Seus clipes possuem pendencias e nao equivalem a aprovacao completa.

A skill copiada descreve caminhos/comandos no projeto Unity original. Nesta fabrica, as leituras correspondem a references/tacticsrpg/<caminho>; os comandos operacionais sao os desta fabrica. Nao executar comandos historicos contra o jogo como efeito colateral.

## Executar um pedido de personagem

1. `node src/cli.mjs new --id ... --race ... --job ...` ou `outfit --from ... --id ... --job ...`. IDs de catalogo desta fabrica nao sao IDs runtime do Unity. Use catalog em caso de duvida.
2. Preencher character.json com o pedido; respeitar racas/Jobs existentes e separar cultura/faccao/individuo/forma/equipamento. Propor lacunas como TBD e candidate. Afinidade nao concede exclusividade racial. High Elf e aristocracia. Aprendizado de qualquer habilidade so por arvores de talentos (v2.1); recrutamento narrativo e independente.
   Receitas aprovadas de raca/Job em recipes/ sao reutilizadas automaticamente por novas fichas. Leia docs/RECIPES.md. recipe-save prepara candidata; recipe-review so registra aprovacao explicita do criador. Regras de Archer nao universalizam anatomia/pele da referencia Orc.
3. Execute prepare e leia handoff/prompt.md + context.md + handoff.json. Autorar imagem nova/edicao artistica no Aseprite com as referencias e invariantes corretas. Fontes Lua podem desenhar clusters/poses explicitamente no editor; preservar codigo e registrar autoria programatica. Nao substituir o individuo por um boneco generico, recoloracao ou redimensionamento do Hero. Sem Aseprite, informar NOT_RUN e o bloqueio; nao trocar por imagegen sem instrucao explicita.
4. Salvar PNG real em concepts/, via import, exibir preview e registrar ferramenta/modelo/prompt reais. Modelos nao garantem reproducao bit a bit nem consistencia entre frames. Nao inventar que uma imagem foi gerada.
5. Gate 1 exige aprovacao explicita do conceito pelo criador antes de sprites. O comando review registra a evidencia; agente nunca se autoaprova. Conceitos e sprites base do corpo ficam sem armas; criar assets de arma separadamente e planejar sua exibicao apenas nas acoes que a invocam. `prepare --purpose base` organiza a primeira vista nativa; depois direcoes, Idle front_r, Walk front_r, outras vistas, combate por lotes. Nao gerar o lote todo antes de revisar a base.
6. Sprites nativos RGBA, quatro vistas sem espelhamento, mao dominante coerente, clusters limpos, transparencia real. Conceito reduzido nao vira sprite de producao. Em fonte 2D por camadas, todas as pecas compartilham canvas e registro por quadro. Compativel significa demonstrado visualmente.
7. Validacao tecnica nao concede aprovacao artistica. Gate 2 requer revisao das vistas/clipes. Gate 3 depende de jogo real e evidencia do criador. Export e staging local; integracao Unity e tarefa separada e precisa de autorizacao do usuario.

## Reutilizacao e limites

Selecao vigente dos oito Orcs: reports/orc-production-current.json (Aseprite V4 aplicada por autorizacao do criador). Antes de reutilizar, consultar esse ponteiro e os editor.json de source/aseprite/orc-production-v4/. Fontes/exportacoes V1 permanecem historicas; nao executar aprovadores/verificadores antigos para sobrescrever a selecao atual. Auditoria padrao detecta a revisao ativa. Documentacao e recuperacao: docs/ORC_ASEPRITE_V4.md. Conceitos/bases preservados; V4 de animacao nao universaliza anatomia/roupa nem concede Gate em jogo.

Preencher Reuse Assessment: REUSE_DIRECT, REUSE_ADAPTED, REQUIRES_EXTENSION ou CREATE_NEW com evidencia, adaptacao, risco, dependencias e validacao. Nao marcar todas as racas como humanoides padrao. Canvas piloto 128x128/ground126 e baseline, nao anatomia universal. Perfis especiais podem ser especificados/validados, mas exportador v0.1 bloqueia perfis que exigem runtime novo.

O loader atual no snapshot so conhece WarriorPilot. Camadas de roupas e overlays de armas independentes no runtime, casts, tiro sincronizado, transformacoes e novos estados exigem extensoes. Composicao offline nao implementa equipar/invocar armas durante uma acao. Nao trocar Core/Animator/rig por necessidade visual. Respeitar arte aprovada e GUIDs Unity.

Nao conectar servicos, instalar ComfyUI, criar planos pagos ou usar APIs cobradas como efeito colateral. A ferramenta de imagem disponivel na conversa pode ser usada dentro do pedido de geracao ja autorizado, sem solicitar chave. Para trabalho de pipeline, executar testes locais pertinentes; nao escrever no projeto Unity durante esses testes.


# Contrato visual derivado

{
  "id": "tactics-core-v1",
  "status": "derived-from-source-approved-direction",
  "anchor": "references/tacticsrpg/Docs/Art/References/character_style_anchor_v1.png",
  "anchorRole": "Linguagem visual global; nao copiar identidade, roupa ou paleta do Hero para outras racas.",
  "pilotRole": "Human Warrior Pilot representa Hero no sandbox; referencia de implementacao e leitura, nao protagonista definitivo nem padrao universal.",
  "medium": "sprites 2D em pixel art refinada, em mapa tatico 3D (apresentacao 2.5D/HD-2D inspirada)",
  "principles": [
    "Proporcoes compactas taticas, maturidade, silhueta legivel no zoom do jogo.",
    "Clusters intencionais, materiais distintos, luz coerente com a ancora observada, detalhe controlado.",
    "Raca, individuo, Job, cultura, faccao, equipamento e forma sao eixos independentes.",
    "Sem espelhamento entre vistas; preservar mao dominante e assimetrias.",
    "Conceitos e sprites base do personagem ficam sem armas; armas sao assets separados, exibidos somente quando equipados e invocados por uma acao.",
    "Conceito e sprite nativo sao entregas diferentes. Reduzir conceito nao cria sprite pronto.",
    "Camadas 2D precisam de canvas, registro e timeline identicos; sobrepor imagens arbitrarias nao produz roupa compativel.",
    "Cores de pele, presas, cultura e ornamentacao racial ausentes nas fontes permanecem TBD/proposta.",
    "Gera-se conceito, depois base nativa, depois vistas, depois animacoes por lotes revisados."
  ],
  "inspirations": [
    {
      "name": "Final Fantasy Tactics",
      "use": "Leitura tatica, silhueta de Job, personagens pixel art 2D em arenas 3D."
    },
    {
      "name": "World of Warcraft",
      "use": "Linguagem de armadura e arquetipos claros, fantasia rica com exagero controlado."
    },
    {
      "name": "Tolkien",
      "use": "Tom medieval-fantastico serio, heroico e culturas verossimeis."
    },
    {
      "name": "Triangle Strategy / HD-2D",
      "use": "Apresentacao 2D com profundidade de cenario; nao implica modelar personagens 3D."
    }
  ],
  "baselineProfile": {
    "width": 128,
    "height": 128,
    "groundY": 126,
    "ppu": 100,
    "counts": {
      "Idle": 4,
      "Walk": 6,
      "Attack": 5,
      "Hit": 3,
      "Defeat": 5
    },
    "note": "Baseline do piloto humanoide 1 tile; anatomias diferentes exigem perfil e revisao. Walk atual usa 3 quadros/tile."
  }
}

---

# references/tacticsrpg/Docs/ART_DIRECTION.md

# ART DIRECTION — TacticsRPG

## 1. Purpose

This document defines the official character art direction for the project.

Its role is to:
- establish a consistent visual identity for the project
- define the approved reference style for all future characters
- guide the creation of classes, races, named units, enemies, and important NPCs
- ensure visual coherence across the full roster

---

## 2. Official Style Anchor

Official visual reference:

![Character Style Anchor](Art/References/character_style_anchor_v1.png)

Reference file:
`Docs/Art/References/character_style_anchor_v1.png`

This image is the current approved visual anchor for the project’s character style.

It defines the baseline for:
- character proportions
- sprite readability
- armor rendering
- cloth rendering
- face maturity
- silhouette clarity
- detail density
- shading quality
- overall visual tone

Important:
This anchor defines the STYLE, not the exact character template.
Future characters do not need to share the same hair, armor, weapon, colors, or role.
They must preserve the same visual language.

---

## 3. Core Visual Inspirations

The project’s visual identity should be guided by the following inspirations:

### 3.1 Final Fantasy Tactics and classic tactical RPGs
Used as inspiration for:
- compact tactical character proportions
- battlefield readability
- class-based identity
- iconic silhouette clarity
- strong unit recognizability

### 3.2 World of Warcraft
Used as inspiration for:
- fantasy armor language
- visual boldness
- faction-readable shapes
- class identity through equipment and silhouette
- strong fantasy archetypes

Important:
Use World of Warcraft as inspiration for visual richness and fantasy clarity,
not for cartoon exaggeration or oversized proportions.

### 3.3 Tolkien-inspired fantasy
Used as inspiration for:
- grounded medieval-fantasy atmosphere
- noble heroic tone
- believable races and cultural flavor
- mythic but serious mood
- elegant, immersive fantasy worldbuilding

Important:
Use Tolkien as inspiration for tone, world flavor, and fantasy sensibility,
not as a requirement to mimic any specific copyrighted design.

---

## 4. Style Summary

Target style:
- tactical RPG character art
- refined pixel-art presentation
- compact readable proportions
- mature and grounded fantasy tone
- elegant armor and costume rendering
- visually rich but controlled detail
- game-ready character readability

The art should feel like a blend of:
- classic tactical RPG readability
- strong fantasy identity
- polished HD-2D-inspired sprite presentation

---

## 5. Character Rendering Rules

### 5.1 Proportions
- compact tactical proportions
- not chibi
- not super-deformed
- not realistic full-human proportions
- slightly heroic but readable at small scale

### 5.2 Face Design
- faces should look expressive and readable
- avoid excessively childish or baby-faced characters unless intentional
- default style should lean slightly mature or young-adult
- facial features should remain simple and readable in sprite scale

### 5.3 Silhouette
- each class must remain identifiable by the character's body, clothing, armor, and stance
- weapons are separate assets; when an action invokes an equipped weapon, its silhouette reinforces the role without being baked into the character sprite
- readability at gameplay scale is mandatory

### 5.4 Pixel Rendering
- handcrafted-looking pixel art
- clean clusters
- controlled detail density
- readable shading
- avoid muddy or noisy rendering
- avoid overly painterly softness
- avoid excessive blur

### 5.5 Materials
Armor:
- polished steel / silver base
- controlled highlights
- readable forms

Cloth:
- rich but controlled folds
- readable cape and tunic shapes
- strong color blocking

Leather:
- warm brown range
- straps, belts, boots should help define equipment hierarchy

Gold accents:
- restrained and elegant
- ornamental, not excessive

### 5.6 Weapon-independent character art
- New character concepts and character-base sprites show the character without a weapon in hand, carried, or sheathed.
- Weapon designs are authored as independent assets. They appear only when the unit has that weapon equipped and the current action invokes it.
- Character identity and Job readability must hold in weaponless states such as Idle and Walk.
- The Human Warrior Pilot's embedded sword is a historical prototype exception, not a template for new assets.
- This is an approved visual direction; dynamic weapon rendering, hand anchors, occlusion, and action synchronization still require implementation.

---

## 6. Tone and Mood

The project should feel:
- heroic
- noble
- serious
- medieval-fantasy
- grounded but imaginative
- visually rich without losing tactical clarity

Avoid:
- overly comedic stylization
- excessively childish art direction
- exaggerated cartoon stretch
- visual overload
- overdesigned noise

---

## 7. Character Diversity Rules

As the project grows into many classes, races, and named units,
future character creation must become more detailed and specific.

Each new character brief should define:
- class
- race
- role in gameplay
- faction / kingdom / origin
- age impression
- body type
- personality tone
- primary colors
- secondary colors
- armor / clothing type
- weapon type as a separate equipment asset, plus the actions that invoke it
- notable accessories
- silhouette goals
- special fantasy motifs if any

The more important the character, the more detailed the brief must be.

---

## 8. Style Boundaries

Do not drift into:
- generic mobile-game fantasy
- overly realistic painterly art
- soft illustration that loses sprite clarity
- oversized anime heads
- childlike proportions by default
- excessively noisy pixel rendering
- overly giant weapons unless intentionally class-specific
- direct imitation of copyrighted characters

---

## 9. Approval Criteria

A character should only be approved if it:
- matches the approved style anchor
- is readable as a tactical RPG unit
- has a strong and clear silhouette
- visually communicates class and role
- feels coherent with the project’s fantasy world
- respects the mature heroic tone
- preserves the project’s rendering language

---

## 10. Production Workflow

Recommended creation workflow:

1. Define character brief
2. Define class and race identity
3. Define silhouette goals
4. Generate candidate visuals
5. Compare against style anchor
6. Approve or refine
7. Save approved art reference
8. Add character to visual roster documentation

For the full technical process (directional views, animation frame contract, Unity import
standards, Presentation integration, testing and approval gates), follow
**`Docs/Art/CHARACTER_PIPELINE.md` v1.0** (spec template:
`Docs/Art/Characters/CHARACTER_TEMPLATE.md`). Principles that carry over from this document:
compact readable proportions, silhouette-first design, and **weapon-independent character
art as the production rule** — permanent weapons drawn into sprites (as in the Human Warrior
Pilot) are a historical prototype exception, not a production standard.

---

## 11. AI / Agent Usage Rule

Any AI agent or tool used for character creation must:
- read this document first
- inspect `Docs/Art/References/character_style_anchor_v1.png`
- preserve the approved visual language
- ask for clarification if it cannot interpret the image reference

If image interpretation is unavailable, the agent must rely on the written style rules in this document.

---

## 12. Versioning

Current approved anchor:
- `character_style_anchor_v1.png`

Future revisions may add:
- additional approved anchors for other archetypes
- race-specific style anchors
- enemy-specific anchors
- monster anchors
- environment anchors


---

# references/tacticsrpg/Docs/GameDesign/DESIGN_DECISIONS.md

# Registro de decisões — v2.1

## Regra canônica v2.1 — desbloqueio EXCLUSIVO por árvores de talentos (obrigatória)
- **Decisão do criador:** todas as habilidades de Jobs, habilidades raciais, magias, invocações, habilidades de companheiros, transformações e técnicas de combate são aprendidas **exclusivamente** pelas árvores de talentos (árvore de Job e/ou árvore racial), gastando pontos de progressão e respeitando níveis de Job, pré-requisitos de talentos anteriores e requisitos internos da própria árvore.
- **Substitui explicitamente** toda proposta anterior de desbloqueio por exploração, captura de criaturas, contratos com criaturas, pactos, rituais, missões especiais, itens encontrados, NPCs ou descoberta de criaturas. Onde os documentos antigos citam esses gatilhos, leia-se: **talento correspondente na árvore**.
- Três categorias distintas: **requisito de aprendizado** (progressão/talentos), **custo de execução** (MP, cooldown, capacidade de invocação, limite de unidades) e **condição tática de execução** (posição, alcance, terreno, linha de visão, cadáver válido para Reanimar Cadáver etc.). Condições de execução permanecem.
- Características anatômicas/propriedades inatas da raça existem desde a criação, sem desbloqueio; habilidades raciais evolutivas, transformações e poderes são talentos da árvore racial.
- Jobs avançados e secretos são desbloqueados por progressão (níveis de Jobs, combinações, pontos, pré-requisitos); o caráter "secreto" está em requisitos complexos ou ocultos na interface, nunca em missões/exploração/itens/NPCs.
- Jobs únicos podem conservar exclusividade narrativa de personagem, mas suas habilidades também vêm da árvore de talentos do Job.
- Recrutamento de personagens para o grupo **não** é afetado.

## Decisões expressas pelo criador (cânone de design)
- 28 raças-alvo, todas jogáveis em alguma medida; recrutamento depende de história, facções, relações e raridade.
- Elf é a linhagem original. Dark Elf: linhagem corrompida por magia das trevas. Moon Elf: tradição lunar com características próprias adquiridas ao longo do tempo. Mystical Elf: especialização arcana. Wood Elf: magia e mistérios florestais. High Elf: aristocracia de alto poder político/financeiro, **não** superioridade biológica inata. Half Elf: descendência humano + Elf.
- Lobisomens parecem humanos fora de combate e aprendem formas de transformação em batalha.
- Summoner invoca múltiplas criaturas controláveis (não apenas efeitos mágicos). Shaman usa bonecos/espíritos controláveis e totens. Hunter tem companheiro animal. Necromancer reanima corpos de oponentes. Warlock invoca um demônio robusto. **As invocações são habilidades individuais aprendidas nas árvores de talentos de cada Job (v2.1)** — sem captura, contratos ou descoberta de criaturas.
- **Venomancer** deve ser criado como Job independente.
- **Shaman** deve aprofundar venenos e desgaste, preservando versatilidade de invocação, suporte e controle.
- **Affliction Master** deve ser **Job independente** e **maior especialista em DoT**, não uma especialização de Warlock.
- Não adicionar novas classes elementais independentes nesta revisão. Magia clássica de fogo, gelo e raio deve estar disponível por Jobs existentes.
- Inspirações de mecânica e atmosfera: Tolkien, World of Warcraft, Triangle Strategy, Dofus, Final Fantasy Tactics; criar nomes, assets e lore próprios.

## Propostas automáticas para validação (não cânone fechado)
- 63 Jobs: 61 da baseline v1.0 + Venomancer + Affliction Master.
- Estrutura das árvores de talentos (nós, custos em pontos, pré-requisitos, ramificações), valores de JobLevel e balanceamento de progressão.
- Estruturas técnicas Unity e fases de implementação.
- Facções, NPCs, itens e missões ainda não definidos.

## Fora de escopo / não fazer agora
- Não implementar 28 raças/63 Jobs em lote.
- Não modificar cenas, prefabs, sprites, pipeline artístico ou scripts existentes sem auditoria e autorização específica.
- Não assumir que documentação em Docs é automaticamente lida por todo agente: usar AGENTS.md + prompt explícito.
- Não reintroduzir Pyromancer, Cryomancer, Arcanist, Plague Doctor ou Affliction Warlock como Jobs separados na baseline consolidada.

## Critérios para mudar a baseline
Qualquer alteração deve atualizar `JOB_CATALOG.md`, `JOB_ACCESS_RULES.md`, `DESIGN_DECISIONS.md` e documentos temáticos afetados; conferir total de Jobs, IDs e requisitos. Registre motivo e impacto.

## Política canônica de save em combate — MVP 5A.4 (2026-10-12)

Save/load manual irrestrito em combate não é permitido. Batalhas específicas poderão permitir checkpoints em batalha, habilitados somente quando condições de cenário definidas pelo criador forem satisfeitas. Condições e batalhas elegíveis serão definidas depois. Esta decisão substitui acesso livre por F5/F9, menus e Continuar save; não proíbe permanentemente salvar durante batalhas. Objetivo: evitar save scumming irrestrito preservando checkpoints adequados ao design.

A implementação atual remove entradas normais e preserva snapshots v2 e saves legados sem apagá-los. Checkpoints não estão implementados. As decisões abertas pertencem ao ROADMAP 5.7; não inventar condições, regras de RNG/tentativas, reuso ou suspensão de batalhas longas.

## Diretriz visual canônica — personagem sem arma embutida (2026-10-19)

- Conceitos e sprites-base de personagens são produzidos sem armas empunhadas, carregadas ou embainhadas. A leitura do personagem e do Job vem do corpo, roupa, armadura, postura e silhueta.
- Cada arma é um asset independente. Ela só aparece quando está equipada pela unidade e a ação/animacao atual a invoca; estados como Idle e Walk permanecem sem arma visível.
- A Presentation deverá compor/renderizar o asset separado com ponto de encaixe, oclusão e sincronização com a ação. Esse suporte não está implementado no runtime atual e não pode ser presumido a partir dos sprites compostos existentes.
- A espada embutida no Human Warrior Pilot permanece como exceção histórica de protótipo e não será alterada por esta decisão.
- Esta decisão define arte nova e direção de arquitetura; não autoriza integração ou mudança de runtime nesta tarefa.


---

# references/tacticsrpg/Docs/GameDesign/RACES.md

# Raças jogáveis — Catálogo e arquitetura (proposta v0.1, regra de aprendizado v2.1)

**Status:** 28 raças são elenco-alvo e jogáveis em alguma medida. Nem todas são recrutáveis no começo, igualmente comuns ou pertencentes às facções do protagonista. **Não implementar sem validação posterior.**

## Decisões consolidadas
- **Aprendizado racial v2.1 (canônico):** características anatômicas e propriedades inatas da raça existem desde a criação do personagem, sem desbloqueio; habilidades raciais evolutivas, transformações, técnicas e poderes são aprendidos **exclusivamente pela árvore de talentos racial**, com pontos de progressão e pré-requisitos (`DESIGN_DECISIONS.md` §Regra canônica v2.1). Exemplos: o Lobisomem aprende e aprimora suas formas de combate na árvore racial; o Dragonborn aprende técnicas dracônicas; o Vampiro aprende poderes vampíricos; os Elfos aprendem suas habilidades específicas pela progressão racial. Nenhuma habilidade racial depende de exploração, missões, rituais, pactos ou eventos narrativos.
- Manter as 22 raças originais e adicionar Lizardfolk, Harpia/Aviário, Merfolk/Aquático, Felino/Catfolk, Constructo/Golem e Sátiro/Fauno.
- Raça ≠ cultura ≠ facção ≠ Job. Não atribuir alinhamento moral por biologia.
- Disponibilidade narrativa, chance de recrutamento e acesso a Jobs são eixos independentes.
- Todas devem ser jogáveis em alguma medida; algumas por eventos, alianças, deserções, personagens especiais ou recrutamento avançado.
- Lobisomens parecem humanos normalmente e desbloqueiam transformações de combate.
- Elfos possuem seis designações élficas e Half Elf como ascendência híbrida; as sete opções permanecem no catálogo de 28.

## Catálogo

| Raça | Fantasia mecânica | Traço inato (proposta) | Ativa (proposta) | Cultura possível (não exclusiva) | Disponibilidade ilustrativa | Perfil visual |
|---|---|---|---|---|---|---|
| Humano | Adaptação | Adaptabilidade | Improvisação | Reinos plurais, ordens e mercadores | Comum | Humanoide |
| Orc | Fúria | Fúria crescente | Frenesi | Clãs e confederações, aliados e inimigos | Contextual | Robusto |
| Troll | Regeneração | Regeneração interrompível | Recuperação primitiva | Tradições xamânicas, povos diversos | Contextual | Robusto |
| Ogro | Massa | Resistência a empurrão | Esmagamento | Fortalezas e comunidades gigantes | Raro | Grande |
| Dragonborn | Linhagem | Resistência elemental da linhagem | Sopro dracônico | Clãs e dinastias dracônicas | Contextual | Humanoide |
| Anão | Resiliência | Constituição anã | Postura de ferro | Reinos de forja e guildas | Comum/contextual | Robusto |
| Gnomo | Engenharia | Engenhosidade | Dispositivo arcano | Cidades tecnomágicas | Contextual | Pequeno |
| Goblin | Oportunismo | Bônus contra vulneráveis | Truque sujo | Mercadores, oficinas e bandos | Contextual | Pequeno |
| Undead | Pós-vida | Imunidades biológicas específicas | Persistência profana | Necrópoles e ordens independentes | Raro | Variável |
| Demon | Corrupção | Essência infernal | Marca da corrupção | Domínios, castas e dissidentes | Raro | Variável |
| Half-Demon | Dualidade | Sangue dual | Manifestação parcial | Diásporas e linhagens mistas | Raro/contextual | Humanoide |
| Vampiro | Sangue | Sede de sangue | Predação | Casas noturnas e linhagens | Raro | Humanoide |
| Lobisomem | Metamorfose | Instinto predatório | Metamorfose | Clãs humanos e tradições lunares | Raro/contextual | Metamorfo |
| Minotauro | Investida | Ímpeto após deslocamento | Carga | Cidades-fortaleza e ordens marciais | Contextual | Robusto |
| Centauro | Mobilidade | Passada equina | Galope | Confederações das planícies | Contextual | Quadrúpede |
| Elf | Harmonia | Sintonia natural | Afinidade temporária | Civilizações élficas plurais | Contextual | Humanoide |
| Dark Elf | Sombras | Visão sombria | Véu sombrio | Casas e cidades subterrâneas | Contextual | Humanoide |
| Moon Elf | Ciclos | Ciclo lunar | Bênção lunar | Templos e observatórios | Contextual | Humanoide |
| Mystical Elf | Arcano | Ressonância arcana | Sobrecarga arcana | Ordens de pesquisa | Raro/contextual | Humanoide |
| Half Elf | Herança | Dupla herança | Convergência | Comunidades multiculturais | Comum/contextual | Humanoide |
| Wood Elf | Terreno | Guardião silvestre | Raízes vivas | Clãs florestais | Contextual | Humanoide |
| High Elf | Disciplina | Maestria de escola | Conjuração refinada | Academias e reinos antigos | Contextual | Humanoide |
| Lizardfolk | Adaptação ambiental | Escamas adaptativas | Ataque venenoso | Pântanos e cidades ribeirinhas | Contextual | Reptiliano |
| Harpia / Aviário | Altitude | Natureza alada | Mergulho predatório | Cidades altas e clãs aéreos | Raro/contextual | Alado |
| Merfolk / Aquático | Água | Locomoção anfíbia | Maré ascendente | Reinos costeiros e submersos | Contextual | Anfíbio |
| Felino / Catfolk | Agilidade posicional | Reflexos felinos | Salto predatório | Povos caçadores e cidades mercantis | Contextual | Felino |
| Constructo / Golem | Corpo artificial | Imunidades biológicas | Reconfiguração modular | Seres conscientes e guardiões | Raro | Artificial |
| Sátiro / Fauno | Encantamento | Espírito feérico | Melodia encantadora | Bosques e tradições musicais | Contextual | Caprino |

## Regras de arquitetura
- `RaceDefinition` contém identidade, anatomia, tags, habilidades e compatibilidade, **não** facção fixa.
- `RaceAbilityDefinition` representa habilidades passivas/ativas e seus gatilhos; **cada habilidade racial evolutiva corresponde a um nó da árvore de talentos racial (v2.1)**; reutilizar componentes (dano, cura, deslocamento, status, transformação) em vez de subclasses para cada raça.
- `RacialProgression` representa a árvore de talentos racial e seus desbloqueios por pontos/pré-requisitos, independente da árvore de Jobs.
- `CharacterVisualProfile` resolve sprites, direção, forma, animações e equipamentos visuais.
- `FactionMembership`, `RecruitmentRule` e `JobAccessRule` devem ser dados separados, referenciados por IDs estáveis.
- Preferir composição e ScriptableObjects ou dados equivalentes validados, sem alterar a arquitetura Unity atual antes de uma auditoria.
- Primeira versão: unidade ocupa uma célula; voo, água e grandes corpos devem ser testados sem assumir grid multi-célula.

## Regras de balanceamento
- Evitar bônus genéricos como identidade única. Cada raça deve alterar pelo menos uma decisão tática.
- Habilidades raciais não devem substituir Job principal ou subjob.
- Biomas concedem vantagem, não tornam personagens inviáveis fora deles.
- Vulnerabilidades de Troll, Undead, Golem etc. precisam de contrajogo e documentação explícita.
- Raças com transformações e recursos exclusivos são casos avançados; não criar 28 barras de recursos.

## Questões em aberto
- Quem pode ser recrutado em cada ato, e por qual facção?
- Quais raças possuem linhagens/subespécies selecionáveis e quais são culturas?
- Como cura, ressurreição e status interagem com Undead, Demon e Golem?
- Quais formas do Lobisomem substituem equipamento/ações?
- Como voo e locomoção aquática funcionam em mapas sem água ou altitude?
- Como equipamentos e sprites se adaptam a anatomias distintas?

## Cânone élfico — decisão explícita v1.0 (prevalece sobre interpretações anteriores)
- **Elf**: linhagem élfica original e ancestral, origem das demais.
- **Dark Elf**: linhagem élfica transformada/corrompida por magia das trevas. Corrupção de origem não implica alinhamento moral individual.
- **Moon Elf**: descendentes élficos especializados em magia lunar, com características próprias desenvolvidas ao longo de gerações.
- **Mystical Elf**: linhagem dedicada à magia arcana; especialização prolongada moldou práticas e características.
- **Wood Elf**: linhagem vinculada às magias e aos mistérios das florestas.
- **High Elf**: **estrato aristocrático, político e econômico**, de grande influência; NÃO é automaticamente uma espécie biologicamente superior ou uma linhagem de magia mais forte. O acesso ao poder é social e institucional, não bônus genético automático.
- **Half Elf**: descendência mista de humano e Elf; podem existir heranças de diferentes linhagens élficas, a definir.
- Facção, linhagem, condição social e raça são campos separados. High Elf deve ser modelado como identidade social/cultural elegível e opção de personagem, preservando as 28 entradas do catálogo, sem impor um gene de nobreza.
- A descrição anterior de High Elf como 'maestria arcana inata' fica **substituída**: acesso privilegiado a tutores, academias, recursos, redes e Jobs culturais; qualquer habilidade arcana é aprendida.


---

# references/tacticsrpg/Docs/GameDesign/JOB_CATALOG.md

# Catálogo de Jobs v2.0 — baseline consolidada

**Status:** catálogo autoral inicial, autorizado para documentação, **não implementado**. Níveis e requisitos são hipóteses de design, sujeitos a testes. Referências são inspirações de mecânica, sem copiar personagens, nomes próprios ou artes protegidas.

- 8 básicas, 18 intermediárias, 26 avançadas, 8 secretas e 3 únicas — **63 Jobs** (61 originais + Venomancer + Affliction Master).
- Cada Job possui papel, três habilidades exemplares, requisito inicial e afinidades que aceleram acesso, não concedem exclusividade automática.
- `JobLevel` representa proficiência da classe, não nível geral da unidade. Requisitos cumulativos são avaliados por IDs estáveis.
- **Regra v2.1 (canônica):** desbloqueio de Jobs e aprendizado de habilidades são EXCLUSIVAMENTE por progressão e árvores de talentos. Onde a tabela menciona "talento de conclusão" ou requisitos equivalentes, trata-se de um nó da própria árvore do Job (pontos investidos + pré-requisitos). Nenhum Job ou habilidade depende de missões, exploração, itens, NPCs, rituais, pactos, contratos ou captura de criaturas.

| Categoria | Job | Papel | Desbloqueio proposto | Kit de habilidades (conceitual) | Afinidades culturais/raciais (não bloqueio) |
|---|---|---|---|---|---|
| Básica | Squire | Versátil | Inicial | Golpe preciso; Primeiros socorros; Foco | Humano,Half Elf |
| Básica | Warrior | Dano físico | Inicial | Corte pesado; Guarda quebrada; Grito de guerra | Orc,Minotauro,Ogro |
| Básica | Archer | Distância | Inicial | Tiro mirado; Disparo alto; Chuva curta | Wood Elf,Felino / Catfolk |
| Básica | Apprentice Mage | Magia | Inicial | Faísca; Gelo menor; Concentração | Elf,Mystical Elf |
| Básica | Acolyte | Suporte | Inicial | Cura; Purificar; Proteção | Humano,Elf |
| Básica | Rogue | Mobilidade | Inicial | Golpe furtivo; Desarmar; Fuga | Goblin,Felino / Catfolk |
| Básica | Scout | Reconhecimento | Inicial | Marcar alvo; Reconhecer; Armadilha simples | Wood Elf,Centauro |
| Básica | Brawler | Combate desarmado | Inicial | Soco rápido; Agarrar; Contra-golpe | Orc,Troll |
| Intermediária | Knight | Tanque | Warrior 3 + Squire 2 | Provocar; Escudo aliado; Quebra-armadura | Anão,Humano |
| Intermediária | Monk | Dano/suporte | Brawler 3 + Acolyte 2 | Golpe de chakra; Palma curativa; Contra-ataque | Humano,Orc |
| Intermediária | Thief | Utilidade | Rogue 3 + Scout 2 | Roubar item; Roubar posição; Passo sombrio | Goblin,Felino / Catfolk |
| Intermediária | Ranger | Distância/terreno | Archer 3 + Scout 3 | Tiro perfurante; Camuflagem; Laço | Wood Elf,Centauro |
| Intermediária | Hunter | Companheiro animal | Ranger 3 + talento de vínculo na própria árvore | Domar; Ordem de ataque; Proteger mestre | Wood Elf,Felino / Catfolk |
| Intermediária | Black Mage | Dano mágico | Apprentice Mage 3 | Bola de fogo; Relâmpago; Tempestade gelada | Mystical Elf,Dark Elf |
| Intermediária | White Mage | Cura/proteção | Acolyte 3 | Cura em área; Dissipar; Ressuscitar | Elf,Humano |
| Intermediária | Elementalist | Controle elemental | Apprentice Mage 3 + Scout 2 | Parede de gelo; Solo ígneo; Corrente elétrica | Dragonborn,Lizardfolk |
| Intermediária | Alchemist | Itens/apoio | Acolyte 2 + Apprentice Mage 2 | Catalisar poção; Bomba; Antídoto | Gnomo,Goblin |
| Intermediária | Venomancer | Venenos e desgaste | Alchemist 3 + Rogue 2 + talento de toxicologia | Dose progressiva; Nuvem tóxica; Catalisar toxina | Lizardfolk,Goblin,Dark Elf |
| Intermediária | Engineer | Dispositivos | Scout 3 + Alchemist 2 | Torre mecânica; Mina; Reparar | Gnomo,Constructo / Golem |
| Intermediária | Bard | Buffs | Acolyte 2 + Rogue 2 | Canção de coragem; Dissipar medo; Marcha | Sátiro / Fauno,Humano |
| Intermediária | Shaman | Natureza/controle | Acolyte 2 + Elementalist 2 + talento de rito natural | Boneco de espinhos; Totem de raízes; Ordem espiritual | Troll,Sátiro / Fauno,Wood Elf |
| Intermediária | Spearman | Alcance físico | Warrior 3 + Scout 2 | Estocada longa; Muralha de lanças; Impalar | Centauro,Lizardfolk |
| Intermediária | Berserker | Risco/dano | Warrior 4 + Brawler 2 | Fúria insaciável; Golpe selvagem; Rugido | Orc,Minotauro |
| Intermediária | Geomancer | Terreno | Elementalist 3 + Scout 3 | Terreno vivo; Fissura; Proteção geológica | Wood Elf,Anão |
| Intermediária | Oracle | Debuffs | Apprentice Mage 3 + Acolyte 2 | Maldição; Silêncio; Presságio | Moon Elf,Dark Elf |
| Intermediária | Mystic Knight | Híbrido | Knight 3 + Black Mage 2 | Lâmina elemental; Guarda rúnica; Ruptura | Dragonborn,Elf |
| Avançada | Samurai | Técnica física | Knight 3 + Monk 3 + talento de postura | Iai; Postura; Contra-corte | Humano,High Elf |
| Avançada | Ninja | Mobilidade/assassinato | Thief 4 + Monk 3 | Passo duplo; Shuriken; Sombra | Felino / Catfolk,Dark Elf |
| Avançada | Dragoon | Lança/salto | Spearman 4 + Knight 2 | Salto; Investida aérea; Caça-dragões | Dragonborn,Harpia / Aviário |
| Avançada | Paladin | Defesa sagrada | Knight 4 + White Mage 3 + talento de juramento | Aura protetora; Julgamento; Interceptar | Humano,Anão |
| Avançada | Dark Knight | Sacrifício/trevas | Knight 4 + Black Mage 3 + talento de sacrifício | Lâmina sombria; Sacrifício; Drenar | Dark Elf,Half-Demon |
| Avançada | Red Mage | Híbrido magia | Black Mage 3 + White Mage 3 | Dupla escola; Magia rápida; Selo | Half Elf,Elf |
| Avançada | Time Mage | Controle temporal | Black Mage 3 + Oracle 3 | Acelerar; Lentidão; Retardar ação | Moon Elf,Mystical Elf |
| Avançada | Summoner | Múltiplas invocações | Black Mage 3 + Shaman 2 + talento de convocação | Convocar familiar; Ordem coletiva; Troca de formação | Mystical Elf,Elf,Half Elf |
| Avançada | Warlock | Demônio principal | Black Mage 4 + Oracle 2 + talento de pacto | Invocar guardião infernal; Pacto de dor; Ordem demoníaca | Demon,Half-Demon |
| Avançada | Affliction Master | **Mestre de DoT**: múltiplas aflições, propagação e controle | Oracle 4 + Venomancer 3 + Black Mage 3 + talento de aflição | Agonia persistente; Contágio calculado; Tormento prolongado | Dark Elf,Undead,Vampiro,Half-Demon |
| Avançada | Necromancer | Cadáveres | Black Mage 4 + Oracle 3 + talento de reanimação | Reanimar cadáver; Ordem dos mortos; Colheita de essência | Undead,Dark Elf |
| Avançada | Beastmaster | Controle feras | Hunter 4 + Shaman 2 | Comando de matilha; Vínculo primal; Adestrar elite | Felino / Catfolk,Wood Elf |
| Avançada | Druid | Metamorfose natural | Shaman 4 + Geomancer 3 | Forma animal; Bosque vivo; Renovação | Wood Elf,Sátiro / Fauno |
| Avançada | Runesmith | Encantamento/equipamento | Engineer 3 + Mystic Knight 3 | Runa de guarda; Arma rúnica; Campo de selo | Anão,Gnomo |
| Avançada | Templar | Antimagia | Paladin 2 + Oracle 3 | Selo antimágico; Prisão sagrada; Expurgar | Humano,High Elf |
| Avançada | Assassin | Eliminação | Ninja 3 + Oracle 2 | Execução; Marca mortal; Ocultação | Dark Elf,Goblin |
| Avançada | Sniper | Alcance extremo | Ranger 4 + Archer 4 | Disparo longo; Mira concentrada; Tiro de supressão | Wood Elf,Centauro |
| Avançada | Spellblade | Híbrido ofensivo | Mystic Knight 3 + Red Mage 2 | Corte mágico; Combo rúnico; Explosão curta | Elf,Dragonborn |
| Avançada | Battle Cleric | Suporte de linha | Monk 3 + White Mage 3 | Círculo de cura; Golpe sagrado; Vigília | Anão,Humano |
| Avançada | Warden | Defesa de terreno | Knight 3 + Geomancer 3 | Barreira; Zona guardada; Âncora | Anão,Constructo / Golem |
| Avançada | Illusionist | Engano | Oracle 3 + Rogue 3 | Imagem falsa; Confundir; Passagem velada | Moon Elf,Sátiro / Fauno |
| Avançada | Blood Mage | Magia de sacrifício | Black Mage 4 + Alchemist 2 + talento de sangue | Conversão vital; Selo sanguíneo; Explosão carmesim | Vampiro,Half-Demon |
| Avançada | Stormcaller | Clima/eletricidade | Elementalist 4 + Time Mage 2 | Tempestade; Campo condutor; Vento cortante | Harpia / Aviário,Merfolk / Aquático |
| Avançada | Tidecaller | Água/controle | Elementalist 3 + Geomancer 3 + talento de maré | Maré alta; Correnteza; Névoa | Merfolk / Aquático,Lizardfolk |
| Avançada | Artificer | Autômatos/engenharia | Engineer 4 + Runesmith 2 | Drone de suporte; Núcleo auxiliar; Sobrecarga | Gnomo,Constructo / Golem |
| Avançada | Duelist | Esgrima | Thief 3 + Knight 3 | Desafio; Aparar; Ripostar | Humano,High Elf |
| Secreta | Chronomancer | Tempo avançado | Time Mage 5 + talento de conclusão da árvore | Eco temporal; Repetição parcial; Suspender | Moon Elf,Mystical Elf |
| Secreta | Grand Summoner | Mestre das invocações | Summoner 5 + talento de convergência | Convergência; Reforço de vínculo; Chamado supremo | Mystical Elf,Elf |
| Secreta | Lich | Morte avançada | Necromancer 5 + talento de filactério | Âncora de alma; Legião espectral limitada; Frio eterno | Undead |
| Secreta | Demonologist | Pacto supremo | Warlock 5 + talento supremo de pacto | Demônio exaltado; Fusão pactuada; Ordem suprema | Demon,Half-Demon |
| Secreta | Dragon Sage | Ascendência dracônica | Mystic Knight 4 + Elementalist 4 + talento dracônico | Ressonância ancestral; Sopro amplificado; Escamas | Dragonborn |
| Secreta | Spirit Warden | Espíritos e proteção | Shaman 5 + Warden 3 + talento espiritual | Guardião ancestral; Totem de vigília; Véu espiritual | Troll,Wood Elf |
| Secreta | Void Weaver | Espaço/controle | Illusionist 4 + Time Mage 4 + talento do vazio | Dobra espacial; Campo vazio; Ancoragem | Mystical Elf,Dark Elf |
| Secreta | Royal Strategist | Comando político | Bard 3 + Templar 3 + talento de comando | Ordem tática; Reserva; Coordenação | High Elf,Humano |
| Única | Sword Saint | Espadachim lendário | Personagem nomeado; condição de história | Técnica lendária; Corte final; Postura perfeita | Variável |
| Única | Herald of Ash | Avatar de cinzas | Personagem nomeado; condição de história | Chamas ancestrais; Cinzas vivas; Decreto | Variável |
| Única | Moon Oracle | Oráculo lunar | Personagem nomeado; condição de história | Profecia lunar; Selo da noite; Vigília | Variável |

## Distinções obrigatórias de design (v2.0)
- **Affliction Master** é Job **independente**, não uma especialização ou subclasse de Warlock. **Não requer Warlock** e não recebe automaticamente demônio pactuado. É o maior especialista em dano periódico (DoT), cumulativo, propagação e desgaste.
- **Venomancer** é Job independente intermediário de toxinas e envenenamento; o seu foco é veneno, antídotos, zonas tóxicas e redução de eficiência do inimigo. **Não** domina todos os tipos de DoT.
- **Shaman** é versátil: bonecos controláveis, totens, raízes, suporte, venenos e desgaste. Não deve superar Affliction Master em DoT puro, Venomancer em especialização tóxica, nem Summoner em quantidade de invocações.
- **Warlock** permanece demonologista de um demônio principal robusto; não confundir com Affliction Master.
- **Black Mage** inclui magias clássicas de fogo, gelo e raio; **Elementalist** manipula interações elementais e terreno; **Stormcaller**, **Tidecaller**, **Geomancer** e **Mystic Knight** aprofundam outras fantasias. Não adicionar Pyromancer, Cryomancer, Arcanist ou Plague Doctor como Jobs independentes nesta versão. Fogo/gelo/arcano podem ser árvores/escolas internas, sem ampliar catálogo.
- Os nomes de Jobs e kits são provisórios e devem ser refinados antes de produção. Requisitos de progressão são hipóteses, não balanceamento aprovado.

## Definição de kits
As três habilidades por Job são **sementes de design**, não kits finais. Cada Job deverá futuramente receber ações, passiva, reaction/support/movement quando pertinentes, custos, alcance, altura, área, duração, efeitos, contrajogo, animações e testes.

## Jobs únicos
Os três Jobs únicos são **placeholders narrativos**, não personagens aprovados. Podem ser alterados sem afetar o núcleo. Seu acesso depende do personagem, nunca de uma raça inteira.


---

# references/tacticsrpg/Docs/GameDesign/JOB_ACCESS_RULES.md

# Regras de acesso a Jobs v2.1

## Regra canônica v2.1 (substitui propostas anteriores)
- Desbloqueio de Jobs e aprendizado de habilidades são **progressão pura**: níveis de Jobs, combinações de classes, pontos de progressão e pré-requisitos de talentos (`DESIGN_DECISIONS.md` §Regra canônica v2.1).
- **Nenhum** Job ou habilidade é desbloqueado por missões, exploração, itens encontrados, NPCs, tutores obrigatórios, rituais, provas, contratos, pactos ou eventos narrativos. Facção/cultura podem explicar o *tema* do acesso, mas a fórmula de desbloqueio é progressão.
- O caráter "secreto" de um Job está em requisitos complexos ou ocultos na interface — nunca em conteúdo narrativo.
- Recrutamento de personagens para o grupo permanece narrativo e independente desta regra.

## Camadas independentes
1. `RaceId`: traços biológicos e forma; não define moralidade ou facção.
2. `CultureId`/`LineageId`: tradição e conhecimentos; High Elf é condição aristocrática/institucional.
3. `FactionId` e reputação: narrativa, recrutamento e conflitos; **não** participam da fórmula de desbloqueio de habilidades/Jobs (v2.1).
4. `RecruitmentRule`: quando e como uma unidade entra no grupo (narrativo, preservado).
5. `JobUnlockRule`: pré-requisitos de progressão (níveis de Jobs e talentos).
6. `JobAffinityRule`: caminhos facilitados, sem bloquear alternativas.
7. `JobCompatibilityRule`: apenas restrições físicas/sobrenaturais justificadas, com variantes de animação e equipamentos quando necessário.
8. `UniqueJobOwnerId`: Jobs de personagem, não de raça.

## Política inicial
- Todas as 28 raças são jogáveis em alguma medida; nem todas são recrutáveis cedo, comuns ou amigáveis ao protagonista.
- **Todas as raças podem alcançar Jobs universais e a maior parte dos intermediários/avançados**, por treinamento e acesso narrativo.
- Afinidade reduz esforço ou oferece mentor alternativo, não muda a potência final por origem.
- Bloqueios absolutos são raros e justificados por anatomia/essência (ex.: metamorfose lupina racial, sopro biológico de Dragonborn), **não por preconceito do mundo**.
- Jobs secretos exigem progressão complexa e/ou requisitos ocultos na interface; Jobs únicos dependem de personagem definido, com habilidades aprendidas pela árvore do Job.
- Um High Elf não ganha magia inata superior: sua aristocracia pode facilitar acesso a academia, tutores e patrocínio, enquanto outros podem conquistar acesso por mérito, missão ou rebelião.
- Raças hostis por facção podem se tornar aliadas por deserção, pacto, missão ou diplomacia.

## Modelo de dificuldade de acesso (por unidade, não por espécie inteira)
- **A — Natural:** requisitos usuais de progressão atendidos.
- **B — Aprendível:** requisitos usuais com custo de pontos adicional leve.
- **C — Raro:** cadeia de pré-requisitos longa (múltiplos Jobs/talentos).
- **D — Secreto:** requisitos complexos ou ocultos na interface até quase atendidos.
- **E — Exclusivo:** só personagem definido ou poder racial intrínseco (sem aprendizado; identidade do personagem).
- Nenhum Job universal recebe E por raça; E para Jobs únicos não significa raça proibida.

## Afinidades exemplares, sem travas
- Orc: Warrior/Berserker A, White Mage B/C (cadeia de progressão mais longa).
- Gnomo: Engineer/Artificer A, Berserker B/C conforme pontos investidos.
- Moon Elf: Time Mage/Chronomancer facilitado por talentos da tradição lunar, não inato.
- High Elf: Samurai/Royal Strategist via talentos culturais; origem não garante talento.
- Merfolk: Tidecaller A, Dragoon B com pré-requisitos adaptados.
- Constructo: Artificer/Runesmith A; White Mage possível, mas cura sobre corpo artificial exige interação explícita (condição de execução).
- Demon: Warlock A, Paladin C mediante cadeia de progressão mais longa (não proibição moral).
- Undead: Necromancer A, White Mage B/C com cura/resurreição adaptadas (condição de execução).

## Algoritmo de desbloqueio
`Unlocked = JobPrerequisitesMet && TalentPointsSpent && CompatibleBodyPlan && !UniqueOwnerMismatch`
Afinidade altera custo de pontos/rota de talentos, não `Unlocked` diretamente. Mostrar na UI requisito faltante e rota alternativa.

## Adições v2.0 (revisadas v2.1: gatilhos narrativos substituídos por talentos)
- **Venomancer**: Alchemist 3 + Rogue 2 + talento de toxicologia; afinidades Lizardfolk, Goblin e Dark Elf. Não exclusivo.
- **Affliction Master**: Oracle 4 + Venomancer 3 + Black Mage 3 + talento de aflição; afinidades Dark Elf, Undead, Vampiro e Half-Demon. **Não exige Warlock nem pacto demoníaco**.
- **Shaman**: continua Acolyte 2 + Elementalist 2 + talento de rito natural; acesso a venenos/raízes/bonecos sem ser o melhor DoT.
- Nenhum requisito numérico é definitivo; `RaceId`, `FactionId`, `CultureId` e `JobId` não devem ser inferidos do nome de exibição.


---

# references/tacticsrpg/Docs/Art/CHARACTER_PIPELINE.md

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


---

# references/tacticsrpg/Docs/Art/Characters/CHARACTER_TEMPLATE.md

# CHARACTER_TEMPLATE — Especificação de novo personagem

> Preencher este template ao criar um novo personagem. Processo completo e padrões técnicos:
> `../CHARACTER_PIPELINE.md` (v1.0). Linguagem visual: `../../ART_DIRECTION.md`. Exemplo
> preenchido (referência de implementação): `HUMAN_WARRIOR_PILOT.md`.
> **Não implementar nada antes do gate 1 (referência visual aprovada).**

## 1. Identidade

- **CharacterId** (pasta/prefixo de assets, minúsculo): `______`
- **Nome de trabalho:** ______
- **Raça / ancestralidade visual:** ______
- **Classe / arquétipo:** ______
- **Papel:** jogável (time 0) · inimigo · NPC — ______
- **Status:** protótipo técnico · produção final — ______
- **Observação de canônica:** (o piloto NÃO é template visual obrigatório; protagonista é
  decisão separada — Estágio 8)

## 2. Silhueta e proporções

- Silhueta distinguishing em zoom-out (1 frase): ______
- Proporções: compactas táticas padrão (128×128, ~100 px de altura útil) ·
  variação: ______
- A identidade do personagem e do Job sem arma: roupa, corpo, armadura e postura: ______
- Assets de arma separados e ações que os invocam quando equipados: ______

## 3. Paleta e traços

- Paleta principal (3–5 cores): ______
- Cabelo/couro/metal/capa: ______
- Traços distinguíveis: ______
- Referência visual aprovada (gate 1): `Docs/Art/References/…` — ______

## 4. Vistas direcionais (4 — rótulos de TELA)

| Vista | Arquivo | Status (a fazer / feito / aprovado) |
|---|---|---|
| `front_r` | `<id>/Directions/<prefixo>_dir_front_r.png` | ______ |
| `front_l` | `…front_l.png` | ______ |
| `back_r`  | `…back_r.png` | ______ |
| `back_l`  | `…back_l.png` | ______ |

Regras: rosto nas `front_*`, costas/capa nas `back_*`, `_l/_r` = lado da TELA, **nunca
espelhar**. O corpo não contém arma; ativos de arma separados seguem a mão/encaixe quando uma
ação os invoca. Mapeamento: `HUMAN_WARRIOR_DIRECTIONS.md` §2.

## 5. Inventário de animações (padrão do piloto — ver `../CHARACTER_PIPELINE.md` §6)

| Clipe | Quadros/vista | Timing/quadro | Pasta | Status |
|---|---|---|---|---|
| Idle | 4 | 0,24 s (ciclo 0,96 s) | `Animations/Idle/` | ______ |
| Walk | 6 (3/passo, ciclo = 2 passos) | derivado do passo 0,22 s | `Animations/Walk/` | ______ |
| Attack | 5 | 0,09 s (~0,45 s) | `Animations/Attack/` | ______ |
| Hit | 3 | 0,08 s (~0,24 s) | `Animations/Hit/` | ______ |
| Defeat | 5 | 0,12 s (~0,60 s) | `Animations/Defeat/` | ______ |

Naming: `<state>_<vista>_<NN>.png` (`NN` = 00.., sem pular) · linha do chão y=126 ·
bob de idle ≤2 px · sem espelhamento. Contagens diferentes exigem acordo prévio
(o carregador aceita 1–15 por vista; consistência entre vistas é gate 2).

## 6. Local dos assets

- `Assets/Resources/Characters/<CharacterId>/…` (§8 do pipeline) — ______
- Metas com configuração aprovada (Sprite/Single/PPU 100/Point/sem compressão/sem mipmap)? —
  ______

## 7. Tratamento de equipamento

- Arma como asset independente (ID/referência): ______
- Ações em que a arma equipada é invocada e aparece: ______
- Estado de suporte no runtime (atual: overlay dinâmico não implementado): ______
- Encaixe na mão, oclusão e sincronização de animação: ______

## 8. Integração técnica (Presentation)

- Registrado em `UnitVisuals` (gate + caminhos)? — ______
- Unidade de destino no mapa (`BattleSandbox.CreateViews`)? — ______
- Fallback verificado (clipe → estático → cápsula)? — ______
- Escala visual aplicada (padrão ×1,15)? — ______

## 9. Testes

- Técnica (compilação, Test Runner, metas 92/92+ Sprite/Single, medição y=126): ______
- PlayMode (`../CHARACTER_PIPELINE.md` §14.2 — 16 itens): ______
- Data da última validação e por quem: ______

## 10. Aprovação

- Gate 1 (referência): ______ · Gate 2 (consistência): ______ · Gate 3 (final em jogo): ______

## 11. Limitações e pendências conhecidas

- ______

## 12. Histórico

- 2026-__-__ — criação da especificação · ______


---

# references/tacticsrpg/.agents/skills/character-art-design/SKILL.md

---
name: character-art-design
description: Criar, adaptar, animar e validar personagens 2D em pixel art do TacticsRPG, com análise de reutilização e preparação de integração Unity. Use para arte de personagens e auditoria do pipeline; não para implementar gameplay.
---

# Character Art Design

Trabalhe a partir da raiz do TacticsRPG; caminhos `Docs/` e `Assets/` são relativos à raiz, recursos abaixo são relativos a esta skill. Não dependa de conversas anteriores. Versão 1.0.

## Entrada e contexto

Identifique o modo: **DESIGN**, **GENERATE**, **ADAPT**, **ANIMATE**, **VALIDATE**, **PREPARE_INTEGRATION**, **INTEGRATE** ou **AUDIT**. Combine modos apenas dentro do pedido autorizado.

Leia `AGENTS.md` quando existir (na auditoria inicial só havia `Docs/AGENTS.md`), `Docs/ART_DIRECTION.md`, `Docs/Art/CHARACTER_PIPELINE.md` e `Docs/Art/Characters/CHARACTER_TEMPLATE.md`. Inspecione `Docs/Art/References/character_style_anchor_v1.png` se houver visão; senão declare a limitação e use as regras escritas. Consulte [project-contract.md](references/project-contract.md) para localizar fontes e divergências. Reuse auditorias recentes, confirmando arquivos alterados e o código pertinente; não releia todo o projeto em tarefas pequenas.

Raça, Job, cultura, facção, indivíduo, equipamento e forma são eixos separados. Consulte fontes temáticas somente conforme o personagem. Não invente cânone ausente: marque propostas e `TBD`. O anchor define linguagem visual; o piloto não define protagonista, anatomia universal, roupa ou paleta obrigatória. Preserve pixel art refinada, proporções táticas compactas sem chibi obrigatório, maturidade, clusters limpos, silhueta legível, materiais e iluminação coerentes. Não promova conceitos A/B a cânone.

## Recursos por modo

- DESIGN / ADAPT: [design-and-reuse.md](references/design-and-reuse.md) e [character-package.md](templates/character-package.md).
- GENERATE: [image-generation-capabilities.md](references/image-generation-capabilities.md) e [generation-prompt.md](templates/generation-prompt.md). Verifique ferramentas reais nesta sessão antes de prometer arquivos.
- ANIMATE / PREPARE_INTEGRATION / INTEGRATE: [production.md](references/production.md).
- VALIDATE / AUDIT: [validation.md](references/validation.md), [validate_character_assets.ps1](scripts/validate_character_assets.ps1) e [review-and-report.md](templates/review-and-report.md).
- [delivery-audit.md](references/delivery-audit.md) registra a auditoria inicial, testes conceituais e limitações de descoberta; é evidência datada, não contrato canônico.

## Fluxo e gates

1. **Brief:** preencha o pacote com identidade, papel (jogável/inimigo/NPC/invocação), anatomia, silhueta, equipamento, paleta e relação com assets. Use o template canônico; pergunte só por lacunas que bloqueiam a etapa atual.
2. **Reuse Assessment:** classifique cada componente em `REUSE_DIRECT`, `REUSE_ADAPTED`, `REQUIRES_EXTENSION` ou `CREATE_NEW`, com fonte, evidência, adaptações, riscos, dependências, validação e impacto de produção. Dimensões iguais não comprovam compatibilidade.
3. **Conceito:** gere candidatos apenas com capacidade e autorização reais; sem geração, entregue o pacote transferível. Exiba arquivos existentes. **Gate 1: aprovação explícita do conceito pelo criador antes de produção de sprites.** Autorização de gerar não equivale a aprovação artística.
4. **Base:** produza/solicite a primeira vista estática em resolução nativa; valide alfa, clusters, proporções, luz, chão e escala antes de expandir. Não trate redução de conceito como sprite pronto.
5. **Direções:** quatro diagonais desenhadas individualmente, sem espelhamento; preserve mão dominante e assimetrias. Perfil excepcional exige parâmetros próprios e validação, não conformidade automática.
6. **Animações:** siga a ordem do pipeline, com revisão por lote. **Gate 2: aprovação explícita da consistência entre vistas e clipes.** Não produza todos os frames antes de validar a base.
7. **Integração:** PREPARE_INTEGRATION entrega inventário e plano sem alterar Unity. INTEGRATE exige autorização explícita para assets/import/registro e, quando necessária, para a extensão arquitetural cujo escopo deve ser apresentado primeiro. Autorizações já dadas persistem; não solicite novamente. Não altere Core por necessidade visual, nem substitua a arquitetura por Animator/rig/Spine.
8. **Final:** verificações técnicas e PlayMode manual. **Gate 3: aprovação final em jogo pelo criador.** Registre aprovação, defeitos, `NOT_RUN` e pendências; testes não concedem aprovação artística.

## Limites e conclusão

Não instalar dependências, conectar serviços ou usar APIs pagas sem autorização; não solicitar/expor credenciais. Não substituir anchors nem modificar documentos canônicos como efeito colateral. Referências recebem versão e status `approved`, `candidate`, `deprecated` ou `experimental`; somente o criador aprova/substitui.

Entregue somente o modo solicitado: pacote de design, arquivos realmente existentes ou relatório, Reuse Assessment, capacidades verificadas, testes e próximo gate. Diferencie `PASS`, `FAIL`, `WARNING`, `NOT_RUN` e `REQUIRES_HUMAN_REVIEW`. Conclusão de design não significa suporte de runtime ou produção aprovada. Registre recomendações de extensões para etapa futura.


---

# references/tacticsrpg/.agents/skills/character-art-design/references/design-and-reuse.md

# Design, anatomia e reutilização

Rendering universal: clusters intencionais, detalhe controlado, materiais distintos, sombras e luz consistentes com anchor, leitura no zoom do jogo. Prata/azul/couro do piloto são exemplos, não paleta de todas as raças. Declare direção de luz no brief a partir da referência observada; não invente um ângulo canônico numérico.

| Perfil organizacional | Aplicação possível | Validação adicional |
|---|---|---|
| Humanoide padrão | Humano Knight | Baseline do piloto; novo registro ainda necessário |
| Humanoide robusto | Orc/Troll/Anão, conforme brief | Massa, passada, altura, equipamento e clipping |
| Humanoide pequeno | Goblin/Gnomo | Escala própria, legibilidade e chão |
| Humanoide grande | Ogro | Canvas, oclusão, footprint e escala |
| Humanoide alado | Harpia | Asas, chão/voo, estados e oclusão |
| Quadrúpede | Fera | Contatos, gait e amplitude |
| Corpo híbrido | Centauro | Torso humano + corpo equino, múltiplos contatos |
| Não humanoide | Criatura distinta | Direção, locomoção e estados próprios |
| Forma transformada | Lobisomem | Pacote por forma, vínculo de identidade e transição |
| Entidade/invocação especial | Espírito/constructo convocado | Material, ancoragem, ciclo de vida e estados |

Perfis são classificação artística inicial, não novas classes C# nem suporte implementado. Não force canvas/altura do humano a todas as anatomias. Humano de referência é validado; cada combinação raça/Job continua exigindo análise. Formas do Lobisomem além de humano/combate são propostas até aprovação.

## Matriz de decisão

| Categoria | Critério com evidência | Exemplos e fronteiras |
|---|---|---|
| A `REUSE_DIRECT` | Sem mudança funcional; confirmar contrato atual | Regras de rendering, templates, fórmula direcional, procedimentos de import, controlador genérico `UnitView` no perfil compatível |
| B `REUSE_ADAPTED` | Compatibilidade demonstrada após adaptação | Pose, gait humanoide, paleta/material, base anatômica e partes de equipamento; justificar anatomia/identidade |
| C `REQUIRES_EXTENSION` | Runtime/processo não atende requisito | Registro multi-personagem, camadas de armas, sockets, transformação, novas ações, tiro sincronizado, voo, montaria, footprint multi-tile |
| D `CREATE_NEW` | Não existe elemento artístico compatível | Rosto, silhueta, anatomia racial distintiva, ornamento cultural original, pose/ciclo não coberto |

Classifique separadamente arte e integração: desenho novo de quadrúpede é D; suporte técnico a seus contatos/estados pode ser C. Não classifique toda anatomia incomum automaticamente como runtime impossível; marque candidato a validação e enumere os requisitos ainda não demonstrados.

No Reuse Assessment, inclua para cada linha: componente, fonte e trecho/asset, categoria, justificativa, adaptações, risco artístico, risco técnico, dependências, status de validação e impacto no trabalho (redução estimada/novo trabalho/migração, sem prometer prazo sem evidência).

Orc Berserker requer corpo/rosto/silhueta próprios; recolorir o piloto não basta. Pele, presas, ornamentos, cultura e cores não definidos são propostas a aprovar, não características raciais definitivas. Não confunda afinidade a Job com exclusividade racial.


---

# references/tacticsrpg/.agents/skills/character-art-design/references/production.md

# Produção e integração

Leia o pipeline canônico para detalhes; confirme `UnitVisuals`/`UnitView` antes da integração. Baseline humanoide: PNG RGBA 128×128, altura útil ~100 px, chão y=126 com origem no topo, PPU100, Point, sem mipmaps/halo/compressão prejudicial, escala piloto 1,15. Canvas/altura/escala são referência validada do piloto, não limite universal.

Direções de tela: `front_r`, `front_l`, `back_r`, `back_l`; ordem das tabelas runtime `[back_l, back_r, front_r, front_l]`. Índice `RoundToInt((Repeat(unitYaw-cameraYaw,360)+45)/90)&3`. Preserve Facing ortogonal do Core e yaw real da câmera. Desenhe cada vista; não espelhe automaticamente.

Pasta final autorizada: `Assets/Resources/Characters/<CharacterId>/`. Fallback `<prefix>_mvp1_static_128.png`; direções `Directions/<prefix>_dir_<direction>.png`; animações `Animations/<State>/<state>_<direction>_<NN>.png`. Clipes usam apenas estado como prefixo. O runtime atual conhece somente WarriorPilot; caminhos novos são plano, não registro implementado.

| Estado | Frames/vista piloto | Avanço |
|---|---:|---|
| Idle | 4 | 0,24 s/frame, loop |
| Walk | 6 | 3/tile, `stepT`, ciclo de 2 tiles |
| Attack | 5 | 0,09 s/frame, override expira |
| Hit | 3 | 0,08 s/frame, golpe que acerta |
| Defeat | 5 | 0,12 s/frame, override não expira; ressalva de módulo no código |

Total 92 animados + 4 direcionais + fallback. Carregador aceita sequências 1–16 por direção, iniciadas em 00 sem lacunas. Variações precisam documentar contagem e timing; Walk permanece 3 frames/tile no código, portanto alterar contagem altera o ciclo, não parametriza automaticamente gait. Novos estados exigem integração.

Ordem: validar base estática -> quatro vistas/fallback -> Idle front_r -> Walk front_r -> outras vistas Idle -> outras vistas Walk -> Attack/Hit/Defeat front_r -> outras vistas combate. Antes de expansão, revisar base; aprovar lotes, não cada frame. Inspeção em jogo de estáticos segue autorização explícita de integração mesmo quando recomendada antes de animações.

Equipamento: registre `embedded` ou `separate`. Corpo sem arma permanente é meta de produção; layers/rig/sockets não existem. Embutir arma é exceção consciente com custo de redesenho de clipes + separar assets + registro/encaixes futuros. Não implemente arquitetura antecipadamente.

Import: `textureType:8`, `spriteMode:1`, `spritePixelsToUnits:100`, `filterMode:0`, `enableMipMap:0`, `alphaIsTransparency:1`. Compressão None no bloco **DefaultTexturePlatform**; não confundir com Standalone/WebGL históricos. Preserve GUID ao corrigir meta existente; não clone GUID. Mudanças de assets/metas exigem autorização para integração.

Plano PREPARE_INTEGRATION deve listar arquivos, perfil, naming, validação, seleção da unidade e extensão mínima do registro, riscos e rollback. Mostre escopo antes de pedir autorização de extensão. Sem Core novo, sem Animator. INTEGRATE executa somente o autorizado, compila/testa e prepara revisão manual.

PlayMode: quatro vistas e giros Q/E, Idle/Walk, trajetória multi-tile sem reinício por tile, zoom-out, chão/desníveis, ataque inclusive vazio, Hit em acerto, derrota, transições, fallback, sombra sem magenta, marcador branco desligado, demais unidades preservadas e undo/snapshots internos conforme política atual. Não restabeleça save livre. Gate 3 permanece humano.
