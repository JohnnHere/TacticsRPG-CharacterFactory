# Preparar integracao Unity

Export e uma entrega de staging para revisao. O comando nao altera cenas, sprites, metas ou codigo no TacticsRPG. Requisitos tecnicos so cobrem o perfil piloto compativel: 128x128, PPU100, Walk6 e os estados Idle/Walk/Attack/Hit/Defeat. Outros perfis podem ser especificados/validados; export bloqueia os que exigem extensao arquitetural.

O pacote dist/<id>/<build>/ contem Assets/Resources/Characters/<id>/ com os PNGs e factory-manifest.json, mais Assets/Editor/CharacterFactoryImporter.cs. O importador opcional ajusta PNGs de pastas que possuem esse manifesto: Sprite/Single, PPU100, Point, alfa, sem mipmaps e compressao Uncompressed. Unity gera metas/GUIDs novos em arquivos novos e preserva metas existentes. O pacote nunca copia metas do Hero para evitar GUIDs duplicados.

O importador nao foi compilado/executado no Editor nesta entrega. Verificar API/compilacao, configuracoes de plataforma e import real na versao do jogo quando houver integracao autorizada. Guardar o .meta junto de cada asset depois da primeira importacao. Nao apagar metas existentes nem permitir GUIDs duplicados. Sobrescrever arte aprovada exige tarefa explicita de migracao/rollback.

## Registro runtime pendente

UnitVisuals no snapshot usa Characters/WarriorPilot e predicado Hero/time0/IsKey. Precisa de um registro characterVisualId -> pasta/escala/fallback e associacao da unidade ao perfil visual. A fabrica nao implementa esse registro no jogo. UnitView ja suporta billboard, quatro vistas e animacoes do piloto, com ressalvas historicas documentadas. Um unico SpriteRenderer recebe cada PNG composto.

Troca dinamica de roupa pode usar pacotes completos por variante registrados separadamente. Roupas/armas como SpriteRenderers independentes exigem outra extensao de rendering, oclusao e sincronizacao. Novo Job no catalogo de design nao implementa gameplay nem animacao nova.

Diretriz visual aprovada para novos personagens: os sprites de corpo sao weaponless; assets de arma ficam separados e so aparecem quando a unidade tem a arma equipada e uma acao a invoca. A excecao historica e o Human Warrior Pilot. O `UnitView` atual desenha um unico sprite composto e nao suporta esse comportamento; serao necessarios overlay, ponto de encaixe, ordem de oclusao e sincronizacao com a animacao/acao. A documentacao nao declara essa extensao implementada.

## Revisao em jogo

O contrato complementar de integracao e [EQUIPMENT_AND_ACTIONS.md](EQUIPMENT_AND_ACTIONS.md). A auditoria de2026-10-19 verificou tambem Core/Unit.cs, Combat.cs, BattleSave.cs e BattleFeedback.cs reais do jogo: WeaponKind so tem Sword/Axe/Bow e nenhum estado desarmado; o valor0/default representa Sword. Implementacao futura precisa de representacao explicita sem arma, regras Core e migracao preservando IDs/saves, selecao visual por acao/equipamento, renderer de partes e relogio/eventos. O modulo local src/action-contract.mjs e validacao offline da fabrica, nao uma alteracao de runtime. Suplementos actions/ nao entram no export legado. Nenhuma integracao Unity foi realizada.

Depois de integracao autorizada: compilar; verificar Resources.Load, quatro vistas e Q/E, zooms, chao/desniveis, Idle/Walk multi-tile e contatos, Attack/Hit/Defeat, falhas de vista, cores/sombra, undo e snapshots conforme politica atual (sem save livre F5/F9). Registrar NOT_RUN para o que nao foi exercitado. Gate 3 e decisao visual explicita do criador com evidencia. Nenhum teste de arquivos substitui PlayMode.
