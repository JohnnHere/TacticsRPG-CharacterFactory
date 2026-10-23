# Character Factory — instrucoes para agentes

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
