# Sistema de Jobs — índice v2.1

O documento v0.1 era apenas uma preparação; esta versão substitui sua indicação de 'sem catálogo aprovado'. O usuário autorizou a criação automática de um sistema conceitual completo, com polimento posterior.

- [Catálogo de Jobs](JOB_CATALOG.md)
- [Regras de acesso](JOB_ACCESS_RULES.md)
- [Invocações controláveis](SUMMONING_SYSTEM.md)
- [Progressão e balanceamento](PROGRESSION_AND_BALANCE.md)
- [Arquitetura Unity](UNITY_ARCHITECTURE.md)
- [Decisões e status](DESIGN_DECISIONS.md)
- [Raças e cânone élfico](RACES.md)
- [Habilidades raciais](RACIAL_ABILITIES.md)
- [Facções e recrutamento](FACTIONS_AND_RECRUITMENT.md)

## Consolidação v2.0
- Catálogo canônico atual: **63 Jobs** (61 originais + Venomancer + Affliction Master).
- Affliction Master não é Warlock, não exige pacto demoníaco e lidera DoT.
- Shaman é versátil em invocações naturais, suporte, veneno e controle.
- Magias de fogo/gelo/raio permanecem em Black Mage e escolas elementais existentes; não criar novos Jobs elementais nesta versão.
- Requisitos, números e habilidades são propostas para refinamento; IDs persistentes devem ser criados antes de persistir saves.

## Regra de aprendizado v2.1 (canônica)
- Todas as habilidades (ativas, passivas, magias, invocações, reações, suporte, movimento) são aprendidas **exclusivamente por árvores de talentos** com pontos de progressão, níveis de Job e pré-requisitos internos.
- Desbloqueio de Jobs avançados/secretos é progressão pura; nenhum requisito narrativo, de exploração ou de itens/NPCs. O caráter secreto vive em requisitos complexos ou ocultos na interface.
- As invocações (Summoner, Shaman, Warlock, Necromancer, Hunter) são habilidades individuais das respectivas árvores; as distinções mecânicas entre os cinco Jobs permanecem (`SUMMONING_SYSTEM.md`).
- Requisito de aprendizado ≠ custo de execução ≠ condição tática; ver `DESIGN_DECISIONS.md` §Regra canônica v2.1.
- Habilidades aprendidas devem ser persistidas no save (`UNITY_ARCHITECTURE.md`).
