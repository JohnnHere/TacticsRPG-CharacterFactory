# Equipamentos e animacoes de acao — contrato da fabrica v1

Adendo vigente de arte Orc: [Aseprite V4 aplicada](ORC_ASEPRITE_V4.md). Os clipes ativos trazem duracoes por quadro `[80,110,50,90,120]`ms e fechamento intencional na pose inicial, ambos vinculados ao fingerprint da aprovacao. `durationMs:90` permanece somente a media/fallback legado; a lista explicita prevalece na autoria/exportacao. Duplicatas intermediarias continuam bloqueadas. Selecao em `reports/orc-production-current.json`, exportador atual `node tools/export-orc-production-v4.mjs`; V1 abaixo descreve a entrega historica. Runtime variavel/equipamento segue pendente.

Data:2026-10-19. Criado a pedido do criador apos auditoria das documentacoes e do codigo atual dos dois repositorios. Este e o padrao de producao da fabrica e de handoff para integracao. Nao descreve funcionalidade ja implementada no Unity. Fontes e SHA256: [auditoria](../reports/equipment-source-audit-v1.json).

## O que ja existia e o que faltava

AGENTS.md, VISUAL_IDENTITY.md, WORKFLOW.md, LAYERS.md, UNITY.md e as decisoes do jogo principal ja exigem personagens sem arma embutida. O jogo principal repete a decisao em Docs/GameDesign/DESIGN_DECISIONS.md e Docs/Art/CHARACTER_PIPELINE.md. Nenhum desses documentos define sockets por quadro, manifestos de arma ou selecao implementada por equipamento.

O codigo real do jogo tem WeaponKind.Sword/Axe/Bow, uma Unit.Weapon que inicia como Sword e Combat que consulta seus atributos diretamente. Weapons.Get cai em Sword para valor desconhecido: null, zero do enum ou categoria desconhecida NAO representam desarmado. UnitVisuals conhece somente WarriorPilot; UnitView desenha um sprite corporal e recebe um unico Attack. BattleFeedback distingue arco de melee, mas gera uma flecha provisoria saindo do peito. ROADMAP2.9/2.10 deixa o sistema completo de equipamentos e compatibilidades para depois. Os snapshots desta fabrica permanecem congelados; a auditoria registra divergencias em relacao ao original atual sem sobrescreve-los.

## Decisao de producao

Todo personagem capaz de executar o comando normal Atacar deve possuir um clipe de ataque basico desarmado, adequado a sua anatomia. Isso inclui Mage e Acolyte; nenhuma magia, bencao, arremesso ou puxada de arco substitui o soco normal quando nao ha arma. A inspecao dos quatro clipes originais de Warrior e Brawler demonstrou que seus golpes corporais existentes podem ser reutilizados mediante hashes e revisao vigente. Outras anatomias podem usar movimentos equivalentes, sem impor punhos humanoides a todas as racas.

Atacar e a acao basica existente. Este contrato nao cria habilidade, talento, custo, alcance ou formula de dano. Tecnicas especiais, magia e habilidades continuam dependentes das arvores de talentos conforme v2.1. Poder, acerto, alcance e balanceamento desarmados ainda exigem implementacao/decisao no Core do jogo; nao reutilizar os valores da espada por acidente.

A ausencia de arma NO DESENHO so significa corpo weapon-independent. O significado do movimento e um campo separado. A animacao deve ser escolhida pela acao real e pelo equipamento efetivamente equipado, respeitando as regras de compatibilidade de gameplay; o Job escolhe a roupa/variante corporal, nao transforma todo Atacar em magia ou tiro.

| Acao real | Movimento corporal | Arma visivel |
|---|---|---|
| Atacar sem arma | basic.unarmed | nunca |
| Atacar com espada/machado | basic.one-hand-swing ou perfil corporal compativel | somente intervalo invocado |
| Atacar com arco | basic.bow-shot | arco e flecha separados, somente intervalos invocados |
| Habilidade de conjuracao | habilidade explicita -> perfil de cast compativel | somente se a habilidade invocar arma equipada |
| Idle/Walk/Hit/Defeat | clipe correspondente do corpo | oculta por padrao |

IDs acima pertencem ao contrato visual; nao sao novos WeaponKind nem AbilityIds do Core. Dagger/staff/throw sao perfis candidatos de extensao, nao categorias implementadas ou autorizacao para usar arma incompatível. Um personagem armado com clipe ausente nao cai silenciosamente em unarmed, magia ou no Attack generico do Job: o pacote fica MISSING_ASSET. Desenvolvimento pode manter estatico com diagnostico explicito, sem publicar como pronto.

## Arquivos e compatibilidade com a baseline existente

O contrato legivel por maquina esta em config/equipment-actions-v1.json. A matriz real dos oito Orcs fica em characters/orc-equipment-actions-v1.json. O comando local `node tools/check-equipment-readiness.mjs` verifica hashes e relata faltas sem afirmar suporte Unity.

Preservar sprites/Animations/Attack e as aprovacoes existentes. Os cinco estados/97 PNGs sao a baseline legada; completar esse inventario nao comprova todos os ataques por equipamento. Novos clipes usam suplemento actions/basic-unarmed/<versao>/<vista>/, com PNGs, native-strip.png, preview e manifesto proprio; fontes em source/action-clips-vN/basic-unarmed/<vista>/. Nao adicionar estados a character.json nem forcar importacao num slot legado, pois isso invalida gates e ainda nao estende o loader. O exportador v0.1 NAO exporta esse suplemento; requer exportacao separada validada e integracao futura.

Um clipe e identificado por characterVisualId + actionProfile + direction + version. Inclui: canvas, PPU, ground, mao dominante, caminhos e SHA256 dos quadros e editavel, duracoes em ms, loop=false, origem/prompts/processamento, estado tecnico e revisao artistica independentes. Para este individuo Orc, primeiro lote unarmed:front_r,5 quadros de90ms,128x128 RGBA8,ground126,paleta da propria roupa. Revisar esse lote antes das outras vistas. Este perfil nao universaliza anatomia de outras racas.

## Armas independentes e encaixe

Compartilhar um ID de arma nao significa que a mesma camada encaixa em todo corpo, roupa, direcao ou movimento. O item de gameplay e separado do asset visual; o visual pode ter bindings por perfil anatomico e por clipe corporal. Mao dominante e assimetrias acompanham a anatomia mesmo quando o tronco gira. Nao inferir a mao somente pelo lado da tela.

Binding de producao exige quatro vistas sem espelhamento, cada quadro corporal fixado por hash e:

- Coordenadas inteiras de sockets no canvas corporal, origem superior esquerda, x para direita/y para baixo. rightGrip e leftGrip indicam maos anatomicas; bowString e projectileOrigin quando aplicaveis. Coordenadas ausentes ficam null/TBD e bloqueiam prontidao; nao inventar encaixes a partir de caixas delimitadoras.
- Camadas RGBA8 registradas, sem trim/reescala/flip, com mesmo canvas/PPU da combinacao. Padrao atual128x128/PPU100 para estes Orcs. Armas longas que precisem de outro canvas exigem perfil e suporte declarados; nunca cortar silenciosamente para caber.
- Partes weaponBack e weaponFront e, quando necessario, handFront/masks desenhadas a partir do quadro exato. Ordem por quadro:weaponBack -> corpo/roupa -> weaponFront -> handFront. Dedos que passam na frente da empunhadura precisam de pixels/mascaras proprios; sprite corporal achatado nao fornece oclusao automaticamente.
- Intervalo de visibilidade invocado pela acao e pela arma equipada. O binding nao aparece em Idle/Walk por haver item equipado. Nenhum overlay em basic.unarmed.
- Referencia ao hash do corpo, da arma, das mascaras e do preview composto. Qualquer alteracao corporal ou da arma invalida a demonstracao correspondente e exige nova verificacao.

## Eventos e sincronizacao

Corpo, arma e eventos visuais compartilham um relogio e a velocidade de animacao do jogo. O manifesto especifica frameIndex e offsetMs dentro do quadro para invoke/hide, contato ou projectile.release, conforme a acao. Nao assumir que o frame2 serve para todo ataque. O instante precisa corresponder a pose real; sem evidencia ele continua TBD. Uma flecha sai do socket de soltura, nao do peito. Seu trajeto e alcance seguem o resultado autorizado pelo Core.

Eventos de animacao sao apresentacao: nao aplicam dano novamente nem autorizam acao. Consumo, acerto, critico e dano continuam sendo resolvidos uma vez pelo Core. Erro ou tile vazio pode tocar a acao invocada sem Hit/dano ficticio. Interrupcao por Hit/Defeat, cancelamento e fim do clipe ocultam overlays e limpam eventos pendentes. Troca de vista/camera atualiza todas as camadas juntas; nao combina corpo de uma vista com arma de outra.

## Pronto para integrar significa demonstrado

Separar READY_NATIVE_BODY, READY_BINDING e VERIFIED_IN_GAME. Para READY_BINDING e obrigatorio validar hashes/canvas/paleta/registro, contato mao-empunhadura, oclusao e trajetoria em todos os quadros e quatro vistas com composicoes reais; depois obter revisao artistica do criador. Um overlay estatico de teste nao prova sincronizacao nem selecao por equipamento. VERIFIED_IN_GAME depende de integracao autorizada e Gate3 com PlayMode real.

Nenhum binding de arma dos Orcs foi produzido/validado nesta etapa. Os sockets continuam NEEDS_AUTHORING; nao ha porcentagem de compatibilidade inventada. A vantagem dos corpos sem arma embutida e evitar apagar/reconstruir arma a cada troca. Continuam necessarios encaixes, mascaras e, dependendo da familia de arma, outro movimento corporal.

## Handoff para o jogo principal

As extensoes necessarias sao:estado explicito sem arma com defaults/migracao de saves sem reinterpretar Sword=0; regras de ataque desarmado no Core; associacao unidade->characterVisualId; selecao de clipe por acao/equipamento; renderer de partes/socket/oclusao; relogio/eventos e limpeza; carregamento dos suplementos e bindings. Preservar IDs existentes, saves, direcoes, Core/Presentation e resultados de combate. O plano nao autoriza refactor ou mudanca de balanceamento no jogo.

Testar integracao futura com:mesma roupa sem arma/com espada/com arco quando permitido; Mage/Acolyte desarmados socando sem efeito; arma incompativel negada pelo Core; falta de clipe detectada; quatro vistas e giro de camera; erro/acerto/vazio; Hit/Defeat/interrupcao; velocidade; troca de equipamento; hashes alterados invalidando binding; replay/saves conforme politica vigente. O jogo principal foi apenas lido. Este documento deve acompanhar a tarefa autorizada de integracao e ser referenciado la quando houver modificacoes reais.

## Inventario corporal Orc atualizado

As oito roupas agora possuem basic.unarmed nas quatro vistas:32 clipes/160 referencias,120 PNGs novos e40 existentes reutilizados, sem quadros faltantes. Conjunto final aprovado condicionalmente pelo criador, com a condicao verificada: ataque desarmado e reacao Hit presentes nas quatro vistas. Evidencia em characters/orc-actions-complete-approval-v1.json. Auditoria tecnica:characters/orc-unarmed-complete-validation-v1.json; autoria/reuso/retomada:[ORC_UNARMED_DIRECTIONS_V1.md](ORC_UNARMED_DIRECTIONS_V1.md). Isso completa o movimento corporal desarmado, nao os bindings de armas. Zero bindings provados, runtime nao implementado, readyForUnity=false. Exportador legado continua sem actions/. A extensao local verificada `node tools/export-orc-actions-v1.mjs` cria pacotes completos com factory-actions.json, PNGs suplementares e fontes selecionadas; nenhum suporte Unity e implicado.

A reacao Hit (tres quadros/vista a80ms) e compartilhada por estado armado/desarmado: nao depende de haver arma equipada. O runtime futuro deve ocultar overlays/eventos de ataque ao receber Hit/Defeat. Isso difere do ataque basico desarmado (cinco quadros/vista a90ms), explicitamente selecionado quando nao houver arma. Os gestos de conjuracao Mage/Acolyte e de ataque por Job estao na baseline aprovada; nao constituem todas as habilidades das arvores de talentos nem provam encaixe com qualquer arma. Nenhum socket ou binding foi inventado na exportacao.
