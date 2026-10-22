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
