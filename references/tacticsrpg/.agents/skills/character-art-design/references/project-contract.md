# Fontes e auditoria técnica

Snapshot: 2026-10-13. Confirme novamente código/contratos quando mudarem. Todas as fontes abaixo existem no projeto na auditoria inicial; não copie seu conteúdo como novo cânone.

| Necessidade | Fontes na raiz do projeto |
|---|---|
| Autoridade | `Docs/AGENTS.md`, `Docs/GameDesign/DOCUMENT_INDEX.md`, `Docs/GameDesign/DESIGN_DECISIONS.md` |
| Estilo/processo | `Docs/ART_DIRECTION.md`, `Docs/Art/CHARACTER_PIPELINE.md`, `Docs/Art/Characters/CHARACTER_TEMPLATE.md` |
| Piloto/histórico | `Docs/Art/Characters/HUMAN_WARRIOR_PILOT.md`, `Docs/Art/Characters/HUMAN_WARRIOR_DIRECTIONS.md`, `Docs/Art/Characters/HUMAN_WARRIOR_ANIMATIONS.md` |
| Identidade | `Docs/GameDesign/RACES.md`, `Docs/GameDesign/RACIAL_ABILITIES.md`, `Docs/GameDesign/JOB_SYSTEM.md`, `Docs/GameDesign/JOB_CATALOG.md`, `Docs/GameDesign/JOB_ACCESS_RULES.md` |
| Cultura/recrutamento | `Docs/GameDesign/FACTIONS_AND_RECRUITMENT.md`; localize documentos adicionais de lore apenas se relevantes |
| Sistemas futuros | `Docs/GameDesign/UNITY_ARCHITECTURE.md`, `Docs/GameDesign/SUMMONING_SYSTEM.md` |
| Estado/marcos | `Docs/GAMEPLAY.md`, `Docs/ROADMAP.md` |
| Código efetivo | `Assets/Scripts/Presentation/UnitView.cs`, `Assets/Scripts/Presentation/UnitVisuals.cs`, `Assets/Scripts/Presentation/BattleSandbox.cs` |
| Testes existentes | `Assets/Tests/EditMode/DirectionMappingTests.cs`, `IdleFrameTests.cs`, `WalkFrameTests.cs` na mesma pasta |
| Imagens | `Docs/Art/References/character_style_anchor_v1.png`, `Assets/Resources/Characters/WarriorPilot/` (PNGs e metas) |

Autoridade: pedido explícito vigente > decisões expressas > especificações temáticas recentes > propostas históricas. Código prova implementação, não aprovação de design. Jobs e raças documentados não implicam sistemas implementados. Transformações evolutivas são talentos raciais; recrutamento narrativo é independente. High Elf representa aristocracia, não superioridade biológica.

## Estado efetivamente inspecionado

`UnitVisuals` usa caminho fixo `Characters/WarriorPilot/` e `IsWarriorPilot`: time do jogador + `IsKey` + nome `Hero`. Novo personagem requer registro ainda inexistente. A função privada `LoadClipByDirection` parametriza pasta/estado, mas ainda concatena a base fixa do piloto: algoritmo reutilizável, registro/caminho requer extensão.

Clipes são sondados de `00` até `15`, interrompendo no primeiro sprite nulo. Quadros após uma lacuna não carregam. Cache completo não é re-sondado; incompleto é re-sondado na construção de views. Direções estáticas têm cache próprio.

`UnitView` oferece billboard, escala, sombra e alinhamento por `sprite.bounds.min.y` (não medição dos pixels opacos). Walk usa `stepIndex` cumulativo dentro da ação + `stepT`, três frames por tile, passo de 0,22 s; fase reinicia por ação. Idle usa 0,24 s/frame. Attack/Hit/Defeat usam 0,09/0,08/0,12 s/frame. `BattleSandbox.CreateViews` liga estáticos, Idle e Walk; feedback dispara os clipes de combate.

## Divergências e ressalvas (registrar, não corrigir)

- Comentários de `UnitVisuals` ainda dizem Idle/Walk só `front_r`; carregador e arquivos cobrem quatro direções.
- Pipeline chama Defeat de travado/toca uma vez, mas `LateUpdate` usa `IdleFrameIndex` com módulo inclusive no Defeat; `_overrideEnds=false` mantém o estado, não congela o último frame. Verificar visualmente o ciclo até destruição.
- Precedência documentada Defeat > Hit > Attack não é arbitrada por enum/prioridade dentro de `UnitView`; há um único override substituível. O chamador dispara Hit antes de Defeat quando há morte. Não prometer prioridade global independente da ordem das chamadas.
- Vista nula de override limpa o override inteiro; fallback subsequente pode retomar Walk/Idle. Pipeline descreve fallback imediato estático; confirmar casos por estado.
- §9 do pipeline abrevia fallback omitindo estático direcional; código usa clipe -> direcional -> fallback MVP1, mantendo cápsula se sprite inicial não carrega.
- Template/histórico do piloto contêm marcos antigos, incluindo indicador branco e animações pendentes. Código atual desliga o indicador no sprite. Aprovações parciais não autorizam afirmar aprovação final de todos os clipes.
- Checklist histórica de save/load não deve reintroduzir F5/F9: decisão MVP5A.4 remove save livre; snapshots internos continuam existentes.
- Anatomia de Centauro é rotulada quadrúpede no catálogo; perfil artístico híbrido descreve melhor torso + corpo equino, sem mudar o catálogo.
- `Docs/AGENTS.md` declara que deveria estar na raiz; `AGENTS.md` raiz não foi encontrado. Não mover nem alterar nesta tarefa.

Não há suporte demonstrado a transformação, equipamentos em camadas, vôo ou footprint multi-tile. Arco existe no gameplay; isso não prova clipe de tiro/projétil sincronizado. Testes encontrados são EditMode; nenhuma pasta PlayMode foi localizada.
