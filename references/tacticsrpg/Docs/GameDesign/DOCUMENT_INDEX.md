# Índice e autoridade documental — v2.1

## Regra canônica de desbloqueio (v2.1, obrigatória)
- TODAS as habilidades — de Jobs, raciais, magias, invocações, companheiros, transformações e técnicas — são aprendidas EXCLUSIVAMENTE por árvores de talentos (Job e/ou racial), com pontos de progressão, níveis de Job e pré-requisitos internos da árvore.
- Nenhuma habilidade ou Job é desbloqueado por exploração, captura de criaturas, contratos, pactos, rituais, missões, itens encontrados, NPCs ou eventos narrativos. Propostas anteriores nesse sentido estão **substituídas**.
- Três categorias distintas, nunca confundir: **requisito de aprendizado** (talentos/progressão), **custo de execução** (MP, cooldown, recursos) e **condição tática de execução** (cadáver válido, alcance, terreno, linha de visão).
- Recrutamento de personagens para o grupo permanece narrativo (`FACTIONS_AND_RECRUITMENT.md`); não confundir com aprendizado de invocações.

## Ordem de leitura para agentes
1. `../GAMEPLAY.md` — mecânicas atuais do projeto, quando presentes.
2. `DESIGN_DECISIONS.md` — decisões expressas e limites da baseline.
3. `RACES.md` e `RACIAL_ABILITIES.md` — 28 raças, canon élfico e passivas.
4. `JOB_SYSTEM.md`, `JOB_CATALOG.md`, `JOB_ACCESS_RULES.md` — 63 Jobs e acesso.
5. `SUMMONING_SYSTEM.md`, `DAMAGE_OVER_TIME_AND_ELEMENTAL_MAGIC.md` — regras de invocação e DoT.
6. `FACTIONS_AND_RECRUITMENT.md` — narrativa, recrutamento e cultura.
7. `UNITY_ARCHITECTURE.md`, `PROGRESSION_AND_BALANCE.md` — recomendações técnicas e testes.
8. `../ART_DIRECTION.md` e `../Art/` — identidade visual; não modificar sem solicitação.

## Autoridade e conflito
- Pedido explícito mais recente do criador > decisões expressas em `DESIGN_DECISIONS.md` > especificação temática mais recente > propostas antigas.
- Documentos em `Docs/` não substituem código real; o agente deve inspecionar implementação existente e reportar incompatibilidades.
- Se `GAMEPLAY.md`/`ROADMAP.md` conflitarem, reportar antes de editar; **não** sobrescrever automaticamente.
- Conteúdo rotulado 'proposta' não equivale a requisito implementado.

## Checklist de revisão
- [ ] Nenhuma habilidade/Job depende de exploração, missão, contrato, pacto, ritual ou captura para ser aprendido.
- [ ] Contagem de 28 raças e 63 Jobs conferida.
- [ ] Affliction Master é independente de Warlock.
- [ ] Summoner mantém primazia de múltiplas invocações controláveis.
- [ ] Shaman mantém versatilidade com venenos e bonecos.
- [ ] Requisitos e afinidades não geram bloqueio racial indevido.
- [ ] Não foram criados Jobs elementais extras não solicitados.
- [ ] Alterações técnicas têm testes e plano de rollback.
