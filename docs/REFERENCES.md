# Fontes locais e sincronizacao

`references/tacticsrpg/` preserva os caminhos do projeto original. Links relativos entre ART_DIRECTION, Art e GameDesign continuam funcionais. O manifesto references/manifest.json lista SHA256 por arquivo, papel, tamanho, data UTC, commit de origem e indicador sourceWasDirty. Copias incluem PNGs/metas do piloto e a skill de personagens com suas referencias. Nenhum arquivo do TacticsRPG e alterado pelo sync.

Prioridade: pedido explicito vigente do criador > DESIGN_DECISIONS > especificacao tematica recente > propostas historicas. O snapshot e contexto do jogo; docs/ nesta fabrica explica as ferramentas e nao cria novo canone. Considere a data e a finalidade de cada fonte.

## Mapa de leitura

| Necessidade | Fonte copiada |
|---|---|
| Autoridade | Docs/AGENTS.md, GameDesign/DOCUMENT_INDEX.md, DESIGN_DECISIONS.md |
| Identidade visual | Docs/ART_DIRECTION.md + Art/References/character_style_anchor_v1.png |
| Processo | Docs/Art/CHARACTER_PIPELINE.md, Characters/CHARACTER_TEMPLATE.md |
| Hero/piloto | Characters/HUMAN_WARRIOR_PILOT.md, DIRECTIONS e ANIMATIONS |
| Racas/Jobs/culturas | RACES.md, RACIAL_ABILITIES.md, JOB_SYSTEM.md, JOB_CATALOG.md, JOB_ACCESS_RULES.md, FACTIONS_AND_RECRUITMENT.md |
| Estado real | GAMEPLAY.md, ROADMAP.md e snapshots UnitVisuals.cs/UnitView.cs |
| Skill existente | .agents/skills/character-art-design/SKILL.md e referencias |

Os catalogos de 28 racas e 63 Jobs sao extraidos das tabelas. IDs slug sao locais da fabrica. O jogo ainda nao tem RaceId/JobId implementados no snapshot inspecionado. Campos de Job sao papel mecanico, nao figurino aprovado. A fabrica nao cria restricoes raciais a partir de afinidades.

## Atualizar e revisar

`node src/cli.mjs sync --source ../TacticsRPG --accept-update` atualiza o snapshot e extrai catalogos. `doctor` confere hashes dos arquivos copiados. Se voce editar o snapshot manualmente, doctor acusa divergencia; edite a fonte sob autorizacao e sincronize. Atualizacoes afetam os hashes das revisoes; prepare regenere os pacotes dos personagens. O sync nao remove automaticamente referencias antigas que deixaram de existir no projeto; somente os arquivos do novo manifesto sao a versao corrente. Arquive/migre referencias conscientemente quando mudar o inventario.

Nao altere a ancora manualmente. Nova direcao visual precisa de nova referencia/versionamento e decisao do criador. Git desta fabrica preserva snapshots depois de commits; a entrega nao faz commit automaticamente.

## Divergencias observadas

- O pipeline abre com descricao de prototipo aprovado; o registro detalhado do Hero especifica aprovacoes parciais e pendencias. Registramos reference_only.
- UnitVisuals continua fixa em WarriorPilot e identifica Hero por time/IsKey/nome. Nova pasta nao registra personagem no runtime.
- UnitView usa um unico SpriteRenderer. Equipamento/roupas em camadas e tiro sincronizado nao estao implementados.
- Perfil humanoide 128x128/chao126 nao define todas as anatomias de 28 racas. Undead e variavel; Orc e robusto. Maos, culturas e paletas precisam de decisao visual.
- Historial da skill menciona AGENTS raiz ausente na auditoria de outubro; na entrega atual AGENTS.md raiz existe. Nao repetir essa observacao antiga como fato atual.
- Defeat e prioridades de override possuem ressalvas na auditoria da skill: estado persistente nao comprova congelamento do ultimo frame ou arbitragem global de prioridade. Confirmar em PlayMode antes de afirmar comportamento.
- O projeto de origem possui modificacoes em andamento. Snapshot SHA256 inclui o conteudo local exato; nao inferir versao apenas de Git HEAD.

Estas divergencias ficam documentadas; nao foram corrigidas no jogo durante a criacao da fabrica.
