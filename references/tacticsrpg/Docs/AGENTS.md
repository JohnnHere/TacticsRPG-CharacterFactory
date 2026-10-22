# Instruções do repositório — TacticsRPG

Este arquivo deve ficar na **raiz do projeto Unity** (`TacticsRPG/AGENTS.md`), não apenas em `Docs/`.

## Leitura obrigatória antes de propor ou escrever código
1. Ler `Docs/GameDesign/DOCUMENT_INDEX.md` e `Docs/GameDesign/DESIGN_DECISIONS.md`.
2. Ler os documentos temáticos relevantes à tarefa, especialmente `JOB_CATALOG.md`, `SUMMONING_SYSTEM.md` e `DAMAGE_OVER_TIME_AND_ELEMENTAL_MAGIC.md` quando envolver Jobs, invocações ou DoT.
3. Ler `Docs/GAMEPLAY.md`, `Docs/ROADMAP.md`, `Docs/ART_DIRECTION.md` conforme o impacto e verificar o código Unity real.
4. Informar quais documentos foram lidos e quaisquer conflitos antes de mudanças significativas.

## Regras inegociáveis de design
- **REGRA CANÔNICA v2.1 — desbloqueio de habilidades:** TODAS as habilidades (Jobs, raciais, magias, invocações, transformações, técnicas, reações, suporte e movimento) são aprendidas EXCLUSIVAMENTE por árvores de talentos (árvore de Job e/ou árvore racial) com pontos de progressão, níveis de Job e pré-requisitos internos da árvore. Nenhuma habilidade ou Job pode exigir exploração, captura de criaturas, contratos, pactos, rituais, missões, itens encontrados, NPCs ou eventos narrativos para ser aprendido. Distinguir sempre: requisito de aprendizado × custo de execução (MP/cooldown) × condição tática (ex.: cadáver válido para Reanimar Cadáver). Recrutamento de personagens para o grupo permanece narrativo.
- 28 raças-alvo; recrutamento desigual por narrativa/facções, não alinhamento racial obrigatório.
- 63 Jobs na baseline: 61 originais + Venomancer + Affliction Master independente.
- Affliction Master é mestre de DoT e **não** especialização de Warlock.
- Shaman: bonecos controláveis, totens, venenos, raízes, suporte e controle, sem superar especialistas.
- Summoner: múltiplas criaturas controláveis; Hunter: um companheiro; Necromancer: cadáveres elegíveis; Warlock: um demônio principal robusto.
- Elfos: respeitar as origens detalhadas em `Docs/GameDesign/DESIGN_DECISIONS.md`; High Elf é posição aristocrática, não superioridade biológica.
- **Arte nova de personagens é weapon-independent:** conceitos e sprites base não mostram armas empunhadas, carregadas ou embainhadas. Armas são assets separados e só aparecem quando equipadas e invocadas por uma ação; a espada do Human Warrior Pilot é exceção histórica do protótipo. O runtime ainda não implementa esse overlay.
- Não criar Pyromancer/Cryomancer/Arcanist/Plague Doctor como Jobs adicionais sem autorização.

## Engenharia e segurança de alterações
- A documentação é design, não prova de implementação. Inspecionar cenas, prefabs, assemblies, scripts e testes antes de alterar.
- Trabalhar em etapas pequenas, com diff e testes; preservar arte aprovada e pipeline visual.
- Não reescrever `GAMEPLAY.md`, `ROADMAP.md`, `ART_DIRECTION.md`, cenas ou assets sem solicitação explícita.
- Ao codificar: definir IDs estáveis, migração quando necessário, testes determinísticos de DoT e limite de ações de invocações.
- Ao mudar design: atualizar documentos correlatos e registrar a decisão; não inventar cânone.
