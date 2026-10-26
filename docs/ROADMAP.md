## Entrada natural de combate — candidato em revisão, 2026-10-25

Novo passe `main-orc-onehanded-entry-v1` parte do último **polimento v1**, preservando-o, para corrigir preparação corporal e primeira pegada. Contexto e fontes em `docs/MAIN_ORC_COMBAT_POLISH.md` (seção atual de entrada) e `experiments/main-orc-entry-v1/entry-plan.json`. Página `Biblioteca de Arte/Estudos Comparativos/Orc principal - Entrada de combate/index.html`. Não é saque/embainhamento: armas somente no ataque, sem Idle/Walk armados. Produção ativa v3 e identidade Orc V1 mantidas; antigo V4 descartado. Próximo marco é a avaliação explícita do criador da entrada refinada; não propagar ou integrar Unity automaticamente. Orquestração e QA independente via Paseo conforme pedido, sem criar QA adicional no DEV.

## Polimento de combate — candidato isolado, 2026-10-25

A correção atual de espada/machado **v3 é uma base viável e melhorada**, preservada e ainda ativa em `characters/orc-v1/source/equipment-current.json`. Novo passe incremental `main-orc-onehanded-polish-v1`, fontes/exports próprios, sem promoção automática: `characters/orc-v1/source/equipment-polish-candidate.json`. Ver `docs/MAIN_ORC_COMBAT_POLISH.md` e `Biblioteca de Arte/Estudos Comparativos/Orc principal - Polimento de combate/index.html`. Preserva armas, identidade Orc V1, Idle/Walk e política de armas somente no ataque. Próximo marco: revisão artística explícita deste candidato pelo criador; não propagar nem integrar Unity antes disso. O antigo Orc V4 permanece descartado.

## Infante de Ferro permanece atual — 2026-10-25

Por decisão explícita do criador, o Infante de Ferro original 05 fica em `Biblioteca de Arte/Orcs Atuais/05 - Infante de Ferro/`, não arquivado. É importante e deve entrar no jogo em estágio mais avançado. Orc V1 (Verde Warcraft) permanece o primeiro jogável selecionado. Ambos preservados e listados em Orcs Atuais. Esta decisão substitui a classificação de arquivo do Infante nas notas anteriores.

## Decisão vigente — Orc V1 e armas, 2026-10-25

Criador selecionou Verde Warcraft v3 como **Orc V1**, primeiro jogável para futura integração. Fonte em `characters/orc-v1/`; Infante cinza preservado na biblioteca em Arquivo de Arte/. Novos assets de uma mão: Espada do Recruta e Machado de Milícia, seguindo `docs/WEAPON_ART_STANDARD.md`. Golpe composto e Walk completo equipado em uma vista, com mestres/camadas/encaixes; esta autorização permite armas visíveis no Walk destas duas combinações e substitui a antiga restrição correspondente. Corpo base e Idle fixo permanecem independentes. Página `Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html`; documentação `docs/ORC_V1_WEAPONS.md`. São assets/prévias locais, não integração Unity ou aprovação automática dos novos golpes/armas. V4 continua descartada; não confundir seleção para integração futura com produção completa em quatro vistas.

## Infante — verde v3 amostrado de referência oficial, 2026-10-25

Nova opção mais escura, com 16 cores de pele amostradas da imagem oficial do Orc no catálogo de raças de Warcraft. Fonte/coordenadas/hash em `experiments/infante-green-skin-v3/palette.json`. Somente pele retocada no Aseprite; conceito e Idle 2,2 s na quarta opção da comparação da biblioteca. Variantes anteriores preservadas, aguardando avaliação. Relatório `reports/infante-green-skin-v3.md`.

## Infante — verde v2 mais escuro, 2026-10-25

Retoque local de pele no Aseprite, conceito + Idle 2,2 s. Nova opção à direita na comparação de pele da biblioteca; original e verde claro preservados. Fontes `source/studies/PaletteVariants/green-skin-v2/` e `source/aseprite/green-skin-v2/` no 05. Aguarda avaliação; nenhuma seleção automática.

## Infante 05 — estudo de pele verde, 2026-10-25

Variante independente `source/studies/PaletteVariants/green-skin-v1/`, conceito + Idle com padrão fixo preservado. Comparação original/verde em `Biblioteca de Arte/Estudos Comparativos/Infante de Ferro - Pele Verde/index.html`. Retoque seletivo no Aseprite, sem nova geração ou alterações nos originais. Paleta inspirada em Warcraft, aguardando avaliação; não selecionar nem propagar automaticamente. Relatório `reports/infante-green-skin-v1.md`.

## Padrão fixo obrigatório de Idle — 2026-10-25

PADRÃO FIXO OBRIGATÓRIO para criação de personagens e variantes: Idle normal segue o meio-termo aprovado, ID `idle-balanced-v1`, cinco fases com 400/450/500/450/400 ms (2200 ms), intensidade equivalente a 2 px na cabeça de humanoide 128×128. Não criar um padrão por personagem, Job, roupa ou personalidade. Ajustes de encaixe anatômico/escala preservam o mesmo ritmo e sutileza; divergências exigem autorização explícita do criador. Canon: `docs/IDLE_ART_STANDARD.md` e `config/idle-art-standard-v1.json`; biblioteca `PADRAO-DE-IDLE.md`. Baselines e notas históricas permissivas abaixo não prevalecem. Artes existentes não são migradas automaticamente e não há integração Unity neste pedido.

# Evolucao e retomada da Character Factory

## Orc principal — resgate dos ataques concluído para revisão, 2026-10-25

Fonte atual orc-v1, nunca V4. Candidatas: Sword8/775ms e Axe10/1130ms; arma visível somente em intervalos1..6 e1..7. Idle5/2200ms e Walk16/1280ms sem arma, pixels aprovados preservados. Machado47px de altura em vez de75; corpo com poses próprias por categoria, dedos da própria pose e arma independente. Preview antes/depois, pegadas e retorno ao Idle em `Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html`. Guia `docs/MAIN_ORC_ONE_HANDED_RESCUE.md`; fontes em source/aseprite/onehanded-rescue-v3/. Próximo: criador avaliar naturalidade, peso e pegada antes de qualquer propagação. Sem Unity, outras vistas ou aprovação automática.



## Histórico rejeitado — armas v2, 2026-10-25

Lote v1 rejeitado e preservado. V2 candidata com armas96×96, Idle armado5 poses/2,2s, Walk16/1,28s e golpe12/1,315s. Corpo, pegada, dedos e relógio compartilhados entre espada/machado compatíveis; não gerar novo corpo a cada item. Esclarecimento do criador: armas seguem a linguagem visual do jogo, não obrigatoriamente o design ou a paleta do Orc; servirão a várias raças/classes. Biblioteca `Personagens Jogaveis/Orc V1/index.html`; guia `docs/ORC_V1_WEAPONS_V2.md`, fontes em experiments/orc-v1-weapons-v2/. Próximo: avaliação artística do criador. Sem integração Unity.

**Terceira opção de Idle Infante 05 — 2026-10-25:** candidata `infante-idle-balanced-v3`, cinco poses completas originais (0,1,5,6,7), cabeça 2 px e ciclo 2,2 s. Comparar três opções em `Biblioteca de Arte/Estudos Comparativos/Infante de Ferro - Idle/index.html`. O sutil permanece atual até escolha do criador. Sem alteração de pixels das poses ou integração Unity.

**Infante de Ferro 05 — Idle sutil, 2026-10-25:** revisão `infante-idle-subtle-v2`, poses originais completas 0,1,6,7, sem alteração raster; oscilação de cabeça 4→1 px, ciclo 1,6→2,8 s. Biblioteca atualizada; antes/depois em `reports/orc-idle-subtle-v2/review.html`. Versões anteriores preservadas. Sem machado ou integração Unity nesta etapa. Próximo: avaliação do criador.

**Biblioteca de Arte — 2026-10-24:** abrir `Biblioteca de Arte/index.html` para navegar pelos oito Orcs atuais, conceito/Idle/Walk e mestres Aseprite. Vigia/Matriarca em `Biblioteca de Arte/Ideias Futuras/`, com a categoria NPC e/ou jogável único. Pés do Atlético limpos localmente no Aseprite (athletic-feet-v2), sem alterar corpo/poses/tempos. Fontes canônicas preservadas. [Relatório](../reports/orc-athletic-feet-v2.md). Nenhuma integração no jogo nesta sessão.

## Orc Atlético entregue — 2026-10-24

Conceito, Idle (8×200 ms) e Walk (8×100 ms) em `characters/orc-pixellab-11/`, mestres PixelLab + Aseprite. Walk usa fases reais do Ágil adaptadas ao próprio corpo em três quartos. Oito candidatos atuais/16 clipes na página `reports/orc-current-review/review.html`; Vigia/Matriarca separados em `ideas/unique-characters-or-npcs/`. V4 ativa e Reimaginado descartados; seleção de produção nula. QA: 17 quadros dos novos mestres, 144 quadros na apresentação e 567 artes anteriores preservadas. Relatório `reports/orc-athletic-v1.md`. Próximo: revisão explícita do criador, sem promover produção ou Unity automaticamente.

**Decisão vigente — 2026-10-24:** V4 ativa e V4 Reimaginado descartados pelo criador; não reutilizar como direção selecionada nem reativar pelos scripts históricos. Arquivos preservados como histórico. Nenhuma seleção de produção ativa. Novo candidato `orc-pixellab-11` (Orc Atlético): parecido com o Ágil, menos armadura, mais musculatura e verde um pouco mais claro. Revisão corrente: `reports/orc-current-review/review.html`. Vigia e Matriarca ficam separados em `ideas/unique-characters-or-npcs/` como ideias futuras de NPC e/ou jogáveis únicos. Esta decisão substitui afirmações históricas de V4 selecionada abaixo.

## Walk V8 — referência própria frontal e movimento adaptado — 2026-10-24

V7 rejeitada pelo criador por cabeça torta e marcha diagonal. Nova candidata: base frontal do próprio 07 via Pro Flash e oito poses Skeleton V3 com fases reais do Ágil adaptadas ao eixo frontal, 100 ms/quadro. Cabeça não foi transplantada. Conceito/Idle do 07 e demais personagens preservados. Comparação sincronizada Ágil × Reimaginado no topo da página canônica, seguida dos 11 conceitos e 18 clipes, inclusive Infante cabeludo. QA: 154 quadros exibidos conferidos pixel a pixel, sem erros JavaScript; isso não concede aprovação artística. A passada frontal é mais contida que a do guia. Próximo: avaliação do criador; seleção V4 e Unity inalterados. Procedência em `reports/orc-pixellab-refinement-v8.md`.

## Walk completo v7 e todos os Orcs juntos — 2026-10-24

Criador rejeitou V6 por pescoço desconexo e marcha oscilando a orientação; autorizou corrigir o ciclo completo. Nova candidata 07: 12 quadros inteiros pelo MCP Skeleton V3, usando só seu próprio conceito, com 18 pontos anotados e poses controlando cabeça/tronco/direção/faixas dos pés. Sem enxerto de cabeça. Empacotamento Aseprite, 90 ms/quadro, 1080 ms/ciclo. Conferência técnica em `reports/orc-pixellab-refinement-v7-check.json`; aprovação artística pendente.

**Revisão canônica de agora em diante:** `reports/orc-pixellab-v4-comparison/review.html`, com todos os 11 conceitos e 18 clipes existentes exibidos simultaneamente (conceito/Idle/Walk). Inclui o Infante cabeludo e Vigia/Matriarca como ideias de únicos jogáveis ou NPCs, sem inventar animações ausentes. Reconstruir com **`node tools/build-orc-all-review.mjs`**, não entregar apenas uma página isolada do reparo. Ponteiro `reports/orc-study-current-review.json`; 158 comparações de pixels na apresentação. Demais artes e aprovação do Soldado preservadas. Próximo: criador avaliar o novo Walk no conjunto; V4 selecionada e Unity continuam inalterados.

## Reimaginado — V5 rejeitada; reparo próprio v6 — 2026-10-24

Criador rejeitou V5 por cabeça alheia, cor incompatível e orientação inadequada. V5 não é referência aprovada. Candidata v6 em `reports/orc-pixellab-refinement-v6/review.html`, usando exclusivamente fontes do próprio 07, paleta original e registro pela base do pescoço/tronco. Corpo, passada, conceito/Idle e outros personagens preservados. Próximo: revisão visual do criador; sem aprovação automática, sem promover cabeça de outro personagem por ela ter sido citada como referência cinética. Procedência completa em `reports/orc-pixellab-refinement-v6.md`.

## Reimaginado — cabeça natural em revisão — 2026-10-24

Criador considerou a cabeça v4 grande e o olhar frontal artificial; pediu referência no Veterano Ágil. Revisão v5 entregue em `reports/orc-pixellab-refinement-v5/review.html`: cabeça menor e levemente inclinada de três quartos, gerada no PixelLab Pro com referências rotuladas do próprio Reimaginado e do Ágil. Composição e registro no Aseprite preservam corpo/passada/tempos; zero pixels alterados fora da máscara de cabeça/pescoço. Conceito/Idle e demais personagens preservados. Próximo: avaliação do criador da nova cabeça; não converter olhar natural em exigência de rosto perfeitamente frontal nem generalizar anatomia da referência a todos os Orcs.

## Ajustes pontuais e Infante cabeludo — 2026-10-23

Feedback do criador registrado: Ágil muito melhor, mas sombra da cabeça tremia; Infante melhor de conceito, com preferência pelos pés da passada anterior; Soldado da Vala aprovado; Reimaginado muito bom, faltando olhar para a direção da marcha. Rodada v4 concluída em `reports/orc-pixellab-refinement-v4/review.html`: sombreamento da cabeça do Ágil estabilizado no Aseprite sem refazer pernas; passada anterior de 16 quadros do Infante restaurada com cabeça sem coque; Reimaginado recebe rosto voltado à frente mantendo corpo/passada. Aprovação do Soldado registrada para conceito e estudos da vista exibida, com hashes, sem ampliar a vistas/ações ausentes ou jogo real.

Novo indivíduo `orc-pixellab-10` (Infante de Ferro — Cabeleira Negra), conceito Pro com referência autorizada de armadura/rosto do 05, proporções mais altas/esguias e cabelo preto longo; Idle 8 e Walk 16 quadros. Não substitui 05. Evidência: 15 mestres/101 quadros, 186 comparações da apresentação, 409 arquivos anteriores preservados; limites de edição de cabeça e preservação dos pés conferidos. Próximo: criador avaliar as três correções e o novo Infante, preservando o Soldado aprovado. Nenhuma integração Unity ou promoção automática de direção/receita.

## Correção visual e MCP PixelLab — retomada em 2026-10-23

Criador rejeitou Idles 04/05/06/07 por deformação e caminhadas 04/07 por execução/orientação inadequada. Refino v2 foi entrega para revisão, não aprovação; os PASS técnicos não validam arte. Rodada v3 preserva snapshot, redesenha Ágil com anatomia atlética e paleta contida, remove coque do Infante preservando rosto/armadura e refaz sete movimentos. MCP oficial configurado e autenticado; guia `docs/PIXELLAB_MCP.md`. Sete animações concluídas pelo MCP com pose inicial/final explícitas e empacotadas no Aseprite. Entrega em `reports/orc-pixellab-refinement-v3/review.html`; 12 mestres/68 quadros, 160 comparações da apresentação e 369 arquivos anteriores preservados. Aguardando avaliação artística do criador. Vigia e Matriarca foram reservados como ideias de personagens únicos jogáveis OU NPCs em `ideas/unique-characters-or-npcs/`. Próximo: avaliar resultados, corrigir defeitos restantes e entregar comparação, mantendo aprovação humana e Unity intacto.

## Refinamento PixelLab + Aseprite — 2026-10-23, pronto para revisão

Retomada concluída: Walk 04/07 refeitos com passos visíveis, 16 quadros; Idles 04/05/06/07 com respiração discreta, duas poses sustentadas em oito quadros. Infante 05 recebeu conceito Pro com armadura mais imponente/detalhada e Walk de 16 quadros compatível. Dois conceitos adicionais independentes: 08 Vigia do Passo e 09 Matriarca da Cinza. Entrega: `reports/orc-pixellab-refinement-v2/review.html`; galeria completa atualizada com dez opções incluindo V4. Relatório: `reports/orc-pixellab-refinement-v2.md`. Bridge PASS: 14 mestres/94 quadros; 241 arquivos anteriores preservados. A primeira caminhada 07 que girava para perfil foi preservada e substituída por nova tentativa com orientação mais estável.

Próximo marco: revisão artística do criador e escolha/refino da direção antes de expandir vistas e ações. Nenhuma nova aprovação inferida, nenhuma integração Unity e nenhuma alteração de direção artística no repositório principal nesta rodada. Os registros abaixo são históricos e não representam os tempos/quantidades dos clipes refinados.

**Entrega PixelLab — 2026-10-23:** três conceitos independentes e seis estudos Idle/Walk (48 quadros de movimento), com mestres Aseprite e revisão interativa em reports/pixellab-orcs-independent-v1/review.html. Exportação dos nove mestres e prévia: 51/51 comparações RGBA. Aguardando escolha artística; V4 continua selecionada e Unity não foi integrado. Próximo: escolher uma opção e refinar silhueta, materiais, mãos, apoio e fechamento dos ciclos antes de expandir vistas/classes.

**Comparação solicitada — 2026-10-23:** `reports/orc-pixellab-v4-comparison/review.html` compara a V4, os três conceitos da primeira rodada e os quatro conceitos desta rodada. Os candidatos 04–07 têm Idle/Walk de oito quadros; a página também mantém os tempos V4 reais. Revisão local interativa; conceitos e movimentos continuam pendentes de aprovação artística.

**Segunda rodada PixelLab + Aseprite — 2026-10-23, concluída para revisão:** quatro candidatos 04–07 com oito estudos Idle/Walk. O quarto foi criado no PixelLab Pro com a V4 apenas como referência de estilo; candidatos 04–06 não receberam imagens de referência. Três pedidos de conceito Pro concluíram sem problema de login. Animações V3 processadas em fila no Aseprite; mestres, PNGs brutos, prompts, hashes e tempos de estudo registrados em cada pacote. `reports/orc-pixellab-round2-status.md` contém o resumo e observações. Débito real da conta não exposto. Todos aguardam aprovação do criador; próximo: escolher/refinar direção e depois atualizar a documentação de identidade visual daqui e do projeto principal. Nenhuma escrita no projeto Unity.

## PixelLab + Aseprite e três Orcs independentes — 2026-10-23

Extensão oficial PixelLab0.4.130 instalada em %APPDATA%/Aseprite/extensions/pixellab; 652 arquivos conferidos, painel carregado no editor e permissões iniciais concluídas pelo criador. Geração textual real, importação para pacotes e mestres Aseprite comprovados na rodada inicial. Protocolo docs/PIXELLAB_ASEPRITE.md; instalação reports/pixellab-extension-install.json. O erro de Dialog em batch foi isolado pelo perfil tmp/aseprite-batch-profile. Nenhum conceito aprovado automaticamente; gate, seleção de produção e integração Unity continuam sob controle do criador.

## Laboratório Orc e identidade própria — 2026-10-23

Criador reafirmou Orc clássico medieval inspirado principalmente em World of Warcraft e também em Tolkien; delegou luz, textura e paleta ao agente e pediu cinco opções para escolher/refinar. Direção em docs/ORC_ART_LAB.md, também registrada no projeto principal. Pacote isolado characters/orc-01-art-lab-v5; revisão reports/orc-art-lab-v5/review.html. A escolha precede novo conceito refinado, base nativa, vistas e clipes. Não autoaprovar nem propagar às outras roupas antes de revisão. Seleção V4 preservada. Próximo marco: criador escolhe a direção ou os elementos que deseja combinar; refinar em Aseprite.

Cinco conceitos entregues: Ferro do Clã, Veterano da Fronteira, Bastião de Basalto, Campeão do Ocre e Ferro de Campanha. Mesmo indivíduo/pose herdados, novas armaduras e materiais criados por Lua no Aseprite; procedência V2/V4 explicitada. Cinco masters, referências ocultas e exportações exatos; bridge 5/5 RGBA; página file/HTTP e layout móvel PASS. Evidências reports/orc-art-lab-v5.json, reports/orc-art-lab-v5-source-check.json e reports/orc-art-lab-v5-preview-check.json. Miniatura comparativa reports/orc-art-lab-v5/five-options.png; conceitos não são sprites de produção. Gates do laboratório vazios; nenhuma escolha ou aprovação inferida.

## V4 aplicada aos oito Orcs — 2026-10-22

Criador autorizou: "vamos aplicar a V4 do Aseprite nas animações de todos os Orcs que criamos". Autorizacao e escopo registrados em reports/orc-production-v4-approval.json. Selecao ativa reports/orc-production-current.json; comparacao reports/orc-production-v4/review.html; guia docs/ORC_ASEPRITE_V4.md. Warrior Attack/Hit front_r usa V4 exata; outras roupas/vistas recebem ajustes compativeis sobre suas fontes, mantendo identidade/roupa/gestos. Oito Gates consistency atualizados com a autorizacao real; conceitos/bases e Gate em jogo preservados no seu escopo.

192 referencias de clipe,184 fontes animadas,856 PNGs animados;32 fontes estaticas/40 PNGs preservados. Total ativo896 PNGs/216 masters. Retornos Attack/Unarmed reutilizam suas proprias poses iniciais; Hit retorna ao inicio de Attack da propria roupa/vista. Limpeza de nove tons quase pretos mapeada ao ink existente de cada roupa; retoques locais de olho/material limitados aos clipes revisados do Warrior. Tempos Attack/Unarmed80,110,50,90,120 e Hit50,100,90ms, totais450/240; locomocao/Defeat preservam poses e tempos. Suplementos novos em actions/basic-unarmed/v4; matriz aponta fontes/hashes atuais.

Validacao:192 clipes/1792 comparacoes RGBA no navegador/zero erros JS;14/14 testes;216 masters anteriores preservados; fontes e pixels ativos conferidos pelo auditor padrao. Builds/PNGs anteriores preservados; snapshot reports/orc-production-v4-before. Exportacao completa e ZIP em reports/orc-production-v4-export.json, somente staging local. Documentacao do repositorio principal atualizada com Aseprite/reuso/V4 e limites; sem alteracoes de assets/codigo Unity. Proximas implementacoes partem dos manifests ativos via fork. Armas/projeteis/VFX, sockets/eventos, selecao por equipamento, registro Orc no runtime e tempos variaveis no jogo seguem extensoes pendentes.

## V4 — estudo original de retoque da V2 no Aseprite — 2026-10-22 (historico)

Criador rejeitou o nivel da V3 e autorizou refinar os pixels aprovados da V2 no Aseprite, preservando identidade e acabamento. A V3 nao foi usada. Nova candidata isolada characters/orc-01-aseprite-v4/: conceito na mesma resolucao1254, fontes Attack5/Hit3 front_r128 e masters em source/aseprite/retouched/. Toda nova alteracao de arte executada por Lua dentro do Aseprite; origem image_gen anterior da V2 mantida na procedencia. Sem nova geracao/reconstrucao/edicao raster externa.

Alteracoes: conceito praticamente igual (limpeza de39102 pixels com alfa<=12 e6 pixels de rebite, sem redesenhar rosto/corpo); clipes com iris aquecidas dentro da paleta existente, retoques locais de sombras/reflexos e consolidacao de nove tons quase pretos. Retornos Attack/Hit reutilizam a pose neutra inicial aprovada e ficam RGBA identicos a ela apos retoque. Mesmas contagens/tempos; apenas os dois retornos mudam silhueta por reuso. Efeito na fluidez ainda depende do criador. Repintura intermediaria de facetas do conceito rejeitada visualmente e arquivada; nao integra final.

Entrega revisavel reports/orc-aseprite-v4/review.html; documentacao reports/orc-aseprite-retouch-v4.md e .json. Verificacoes:9/9 exportacoes RGBA exatas,9 cels originais V2 preservados dentro dos masters,0 cores nativas novas/0 mudancas nao planejadas de alfa,16 comparacoes exatas de canvas/8 toggles da camada de retoque/0 errosJS,1151 arquivos protegidos e11 fontes/PNGs V2 preservados. Final reports/orc-aseprite-final-check-v4.json. V2 continua aprovada; V4 pendente. Nenhum apply, Unity ou direcao artistica nova canonizada. Proximo marco: avaliar limpeza, retoques e retorno antes de propagar outras vistas/Jobs.

## Autoria integral Aseprite e comparacao V3 — 2026-10-22

Decisao expressa vigente do criador: TODA a producao artistica deve acontecer no Aseprite. V2 anterior foi aprovada, mas era image_gen/reconstrucao e nao demonstrava autoria integral no editor. Aprovacao real V2 registrada no Gate conceito e por hashes dos estudos; nenhum apply ou Gate em jogo. Politica persistida em AGENTS/README/WORKFLOW/ASEPRITE e nos handoffs de prepare; doctor/help atualizados. Aseprite e mestre, geracao/edicao raster externa nao e padrao autorizado. Lua no runtime do editor e autoria programatica documentada, nao desenho manual nem IA nativa.

Nova candidata isolada: characters/orc-01-aseprite-v3/. Desenhados do zero dentro do Aseprite: conceito128x128, Attack5/Hit3 front_r, nove camadas regionais por quadro, paleta e tags. Zero chamadas image_gen/zero pixels raster importados para formar a arte/zero acabamento externo. Fontes em source/aseprite/authored/ e desenhos no author-orc-v3.lua. Reexecucao independente com fontes/PNGs identicos; export9/9 RGBA exatos. 1151 arquivos protegidos originais preservados. Testes13/13PASS; browser81componentes/16comparacoes nativas/3isolamentos de camada/0errosJS.

Entrega: reports/orc-aseprite-v3/review.html (V2/V3 no mesmo timing e escala, controles de camadas), reports/orc-aseprite-authorship-v3.md e .json. Avaliacao franca: V3 atual inferior a V2 em fidelidade facial/anatomia/volume/materiais; nao recomendar troca automatica. E amostra de autoria do agente por Lua, nao teto de qualidade do Aseprite. Conceitos tem resolucoes de autoria diferentes; comparacao controlada e nos clipes128. Duas tentativas preservadas em iterations/. Proximo marco: revisar/rejeitar/refinar a candidata no Aseprite antes de outras vistas/Jobs ou novos direcionamentos artisticos no projeto principal. Nenhuma escrita no Unity.

## Auditoria Orc e refinamento candidato — 2026-10-22

Pedido vigente do criador: auditar os assets Orc, melhorar conceito/animacoes e mostrar resultados; novos direcionamentos da fabrica e do repositorio principal somente depois de aprovados. Auditoria dos oito pacotes: 896 PNGs nativos, 192 referencias de clipe, 216 fontes ativas, oito Gates conceito/base/consistencia vigentes e nenhum Gate em jogo. Zero falhas tecnicas; armas independentes, eventos, sockets/oclusao e registro Unity continuam sem evidencia de runtime. Pranchas visuais de todos os Jobs em reports/orc-audit-v2/. Relatorio detalhado: reports/orc-assets-audit-v2.md; hashes: reports/orc-assets-audit-v2.json.

Produzidos tres assets artisticos reais via image_gen integrado: conceito candidato em characters/orc-01-refinement-v2/concepts/warrior-refinement-v2.png (mesmo individuo/roupa; Gate 1 pendente) e folhas novas de Attack/Hit front_r sobre o design original aprovado. Oito quadros reconstruidos 128x128, fontes .aseprite e manifesto em characters/orc-01/source/aseprite/combat-refinement-v2/; export Steam batch oculto PASS, oito comparacoes RGBA exatas. Proposta de timing conserva totais450/240ms, mas duracoes variaveis sao apenas editor/preview ate evidencia Unity. Prompts/fontes/hashes reais em characters/orc-01-refinement-v2/source/generation-record.json; modelo nao divulgado pela ferramenta. Nenhum asset/review aprovado substituido; nenhuma escrita no jogo.

Entrega revisavel: reports/orc-audit-v2/review.html, com conceito antes/depois, dois estudos animados e acervo das oito roupas/quatro vistas. Conferencia Edge headless:896 PNGs carregados,192 selecoes de clipe,8 quadros candidatos RGBA exatos em canvas,0 erros JS (reports/orc-audit-review-check-v2.json). Proximo passo: obter avaliacao artistica separada de conceito, poses Attack, poses Hit e ritmo. Nao ampliar sprites a partir do conceito novo antes de Gate1 nem promover candidatos/novas regras como aprovados. Apos evidencia do criador, atualizar documentos tematicos dos dois projetos e expandir base/vistas/clipes por lotes. Idle/Walk aprovados sao reaproveitaveis; evitar regeneracao total sem necessidade demonstrada.

## Integracao Aseprite concluida — 2026-10-22

Documentacao de ponta a ponta entregue em docs/ASEPRITE_INTEGRATION_V1.md, com arquitetura, responsabilidades, fluxos de autoria/aplicacao, contratos, evidencias, diagnostico, recuperacao e limites. docs/ASEPRITE.md permanece como guia operacional resumido. A documentacao foi conferida contra o codigo e os relatorios existentes; nenhuma nova alteracao artistica ou Unity nesta etapa.

Pedido do criador: integrar de ponta a ponta o Aseprite instalado via Steam em F:\SteamLibrary\steamapps\common\Aseprite, trabalhando sem disputar o computador. Implementados editor-config/check/template/fork/export/apply, configuracao local ignorada, processos batch ocultos, builds imutaveis com fontes/PNGs/timing/metadados/preview, backup/rollback/idempotencia e gates de personagem. Fontes genericas para environment/prop/effect/ui/weapon/enemy, tilesets e layout tilemap com indices/flags/posicoes exportados. Sem API/assinatura/dependencia nova.

Auditoria real das216 fontes ativas:888 quadros exportados RGBA/timing identicos +8 fallbacks, cobrindo896 PNGs;1112 arquivos originais e oito reviews preservados. Evidencias:reports/aseprite-production-audit-v1.json e reports/aseprite-capabilities-v1.json. Guia de retomada:docs/ASEPRITE.md. Decisao persistente: usar o bridge na autoria/exportacao futura; manter fontes aprovadas via fork e revisoes humanas existentes. O bridge nao cria arte automaticamente nem implementa runtime Unity.

Proxima entrega artistica elegivel: escolher um ajuste real ou novo asset e usar fork/template -> edicao salva -> export/preview -> revisao -> apply quando for baseline de personagem. A autoria em camadas de corpo/roupa ainda precisa de demonstracao artistica; a exportacao de dados 2D de cenario esta pronta, mas conversao para alturas/colisoes/render3D continua extensao especifica do jogo.

Fechamento verificado:13/13 testes PASS; previews Edge headless com888 quadros de producao +6 itens sinteticos RGBA exatos, HTTP/file:// e controles PASS, zero erros JS. Fluxo CLI real fork/export/apply com quatro frames retornou UNCHANGED e preservou assets.json/reviews/PNGs. Copia pronta:characters/orc-01/source/aseprite/idle-front-r-editor-v1/source/orc-01-00.aseprite. Relatorio consolidado:reports/aseprite-integration-v1.json. Nenhuma interacao com mouse/teclado ou escrita Unity.

Atualizado em 2026-10-22. Este arquivo orienta as proximas etapas entre conversas. O contexto persistente esta em AGENTS.md, docs/, referencias, receitas e pacotes de personagem. Ao abrir esta pasta como projeto, um agente com acesso a esses arquivos deve recuperar esse contexto antes de agir. Em outras ferramentas, anexar handoff/context.md, prompt.md e as imagens listadas.

## Como retomar

Pedidos suficientes: "continue a pipeline pela proxima etapa", "crie o conceito do orc-01", "ajuste a roupa do Orc Archer conforme minha revisao" ou "avance as melhorias tecnicas enquanto reviso o personagem". O agente le este arquivo, executa doctor e consulta as fichas e revisoes. Escolhe a primeira tarefa elegivel e informa o resultado a revisar. Autorizacao para desenvolvimento local permanece valida; decisao artistica explicita e exigida somente nos marcos documentados. Aprovacao de conceito nao autoriza integracao no Unity.

Ao terminar uma sessao, atualizar a tarefa executada, pendencias e proxima entrega revisavel. Nao marcar concluido por planejamento ou por teste tecnico quando a tarefa exige arte. As decisoes em reviews.json e hashes atuais sao a evidencia do personagem; esta lista e um resumo de planejamento.

## 1. Base tecnica — implementada

### Trabalho ativo: Orc nas outras sete classes basicas

Pedido vigente do criador: produzir as demais classes basicas aproveitando ao maximo o Orc Warrior para economizar tempo e tokens. Escopo confirmado pelo catalogo e pelo original Unity em leitura: Squire, Archer, Apprentice Mage, Acolyte, Rogue, Scout e Brawler. Sao variantes de roupa do MESMO individuo, nao sete novos Orcs. Warrior aprovado/exportado permanece intacto.

Ampliacao vigente apos feedback positivo do criador: auditar equipamentos nos dois repositorios, criar padrao faltante e garantir ataque basico desarmado separado das habilidades. Auditoria real de17 fontes do jogo e cinco contratos locais registrada em reports/equipment-source-audit-v1.json; jogo apenas lido. Padrao criado em docs/EQUIPMENT_AND_ACTIONS.md/config/equipment-actions-v1.json. A ausencia de arma no desenho nao torna uma puxada de arco ou conjuracao um soco.

- [x] Validar reuso das quatro vistas de ataque fisico do Warrior e Brawler (40 quadros existentes), sem copias ou alteracoes.
- [x] Produzir primeiro lote unarmed front_r nas seis outras roupas:30 PNGs novos/seis editaveis, LibreSprite RGBA/duracoes identicos, propria paleta/128RGBA8/ground126/alfa binario. Squire usa fonte/suplementov2 corrigidos; tentativas com ombreira trocada preservadas fora da selecao ativa.
- [x] Preview characters/review-orc-unarmed-front-v1.html com40 referencias de quadro nas oito roupas, incluindo reuso. Edge HTTP/file://,40/40 canvas RGBA exatos, controles verificados, zero erros JavaScript. Suite local9/9 PASS, tres testes novos da selecao offline por acao/equipamento.
- [x] Criador aprovou primeiro lote unarmed front_r: "Aprovo os ataques desarmados; continue as outras vistas." Evidencia/hash dos30 PNGs e seis fontes em orc-unarmed-front-approval-v1.json e source/unarmed-front-v1-review.json; sem autoaprovar consistencia final.
- [x] Produzir90 PNGs e18 fontes editaveis unarmed front_l/back_r/back_l nas seis roupas;32/32 clipes completos,160 referencias com120 PNGs novos/24 fontes e40 quadros reutilizados. LibreSprite90 novos RGBA/duracoes identicos, baseline e front_r aprovado intactos.
- [x] Previa conjunta review-orc-actions-complete-v1.html com oito roupas/seis acoes/quatro vistas. Edge:896 referencias carregadas HTTP/file://,896/896 canvas RGBA exatos, controles verificados, zero erros JavaScript; npm9/9 PASS.
- [x] Criador autorizou continuar condicionado ao hit/ataque desarmado: condicao verificada nas quatro vistas; sete Gates consistency registrados e suplemento aprovado. Implementada/verificada exportacao completa com suplemento; oito pacotes (incluindo Warrior referencia),896 PNGs/216 fontes editaveis, ZIP verificado. Evidencia em docs/ORC_PRODUCTION_EXPORT_V1.md. Exportador legado nao inclui actions/. Overlays, sockets, mascaras e gameplay desarmado no Unity continuam pendentes.

Matriz vigente:characters/orc-equipment-actions-v1.json; readiness:reports/orc-equipment-readiness-v1.json. Oito Orcs x quatro vistas exigem32 clipes unarmed;32 fontes nativas disponiveis,0 faltantes (0 quadros). Nenhum binding de arma provado. Original WeaponKind tem apenas Sword/Axe/Bow, default0=Sword; nao usar null/default como implementacao ficticia de desarmado. Detalhes de fontes, reuso, correcoes e proxima etapa em docs/ORC_UNARMED_DIRECTIONS_V1.md.

- [x] Criar seis fichas novas e retomar/atualizar a ficha Archer; identidade, appearance e referencia da base aprovada preservadas.
- [x] Gerar e importar sete conceitos reais image_gen, uma chamada por Job; prompts, referencias e hashes registrados. Todos em characters/orc-01-<job>/concepts/outfit-concept-v1.png. Sem armas e sem autoaprovacao.
- [x] Criar characters/review-orc-basic-classes-v1.html com o Warrior e sete variantes; verificar oito imagens, filtros e fundo no Edge local, sem erros JavaScript. Evidencias em characters/orc-basic-review-browser.json/.png.
- [x] Indexar os 97 PNGs e 20 clipes editaveis aprovados do Warrior por caminho/hash, sem duplicar fontes: characters/orc-basic-shared-source-index.json. Reuse Assessment por componente nas sete fichas.
- [x] Registrar aprovacao explicita dos conceitos: criador aprovou seis roupas e rejeitou Rogue v1 por semelhanca com Warrior. Rogue v2 com capuz e roupa carvao furtiva foi aprovado depois: "Aprovo o Rogue v2; siga com os sprites." Sete Gates concept vigentes; Rogue v1 historico rejeitado.
- [x] Produzir primeiras bases front_r: 14 PNGs (7 poses + 7 fallbacks), 128x128 RGBA8, altura100, ground126, 47–48 cores por roupa, alfa parcial zero. Sete fontes .aseprite com export LibreSprite RGBA identico. Base: 10 PASS/0 FAIL por pacote, aviso esperado fallback duplicado.
- [x] Primeiras bases aprovadas pelo criador: "Aprovo as sete bases; produza as outras vistas." Evidencia parcial front_r por SHA256 em cada source/native-base-v1/front-r-review.json. Essa decisao nao aprova outras vistas ou animacoes.
- [x] Produzir outras tres vistas por classe: 21 PNGs novos, total35 PNGs estaticos e 28 editaveis. Sete folhas image_gen + tres correcoes individuais; sem espelhamento, paleta da propria roupa e bases aprovadas intactas. Directions: 175 PASS/0 FAIL, sete avisos esperados fallback duplicado. LibreSprite: 28/28 fontes RGBA identicas apos export.
- [x] Criador aprovou as quatro vistas: "Aprovo as vistas das sete classes; continue as animações." Sete Gates base registrados com evidencia real e digest atual em reviews.json.
- [x] Primeiro lote Idle4/Walk6 front_r produzido nas sete roupas: 70 PNGs animados e 14 editaveis, paleta por roupa, alfa binario, ground126 e Idle com bob <=2px. LibreSprite: 70/70 quadros e duracoes identicos; navegador: 70/70 canvas RGBA identicos aos PNGs, controles e file:// verificados, zero erros JS.
- [x] Criador aprovou Walk front_r das sete classes; evidencia e hashes dos 42 quadros registrados em source/locomotion-front-v1/review.json.
- [x] Idle v2 aprovado: "Aprovo o Idle v2; continue as demais vistas." Evidencia/hashes em characters/orc-front-locomotion-approval-v2.json e registros parciais dos sete pacotes.
- [x] Produzir Idle/Walk nas outras tres vistas:210 quadros e42 editaveis novos;280 quadros/56 clipes no conjunto completo de locomocao. Native/paleta/proveniencia e LibreSprite RGBA+duracoes sem falhas. Front_r aprovado intacto.
- [x] Criador aprovou Idle/Walk nas tres vistas novas: "Aprovo as três vistas animadas; continue o combate." Evidencia/hashes nos sete source/locomotion-directions-v1/review.json e indice orc-locomotion-directions-approval-v1.json.
- [x] Produzir Attack5/Hit3/Defeat5 front_r por Job:91 novos PNGs e21 editaveis, com gestos de ataque distintos. LibreSprite91/91 RGBA e duracoes identicos; navegador91/91 canvas RGBA exatos, zero erros JS.
- [x] Criador aprovou primeiro combate: "Aprovo o combate front_r; continue as outras vistas." Evidencia e hashes em orc-combat-front-approval-v1.json e nos sete source/combat-front-v1/review.json.
- [x] Produzir273 quadros e63 editaveis nas outras tres vistas de combate, sem espelhamento. Inventario corporal completo:679 PNGs/168 fontes editaveis ativas. CLI full:3423 PASS/0 FAIL; sete avisos esperados de fallback. LibreSprite e navegador:644/644 quadros animados RGBA identicos; duracoes, controles e file:// verificados. Seis testes locais aprovados.
- [x] Preservar371 quadros animados e105 fontes editaveis anteriormente aprovados,35 PNGs estaticos e Warrior97 PNG/20 editaveis, com comparacao de hashes. Reutilizar referencias de poses validas somente em adaptacoes demonstradas visualmente. O Warrior possui quadros raster completos, sem corpo nu separado sob a armadura; nao existe rig de troca de roupas.
- [x] Consistencia artistica final conjunta aprovada condicionalmente; hit/desarmado presentes, aprovacao registrada em characters/orc-actions-complete-approval-v1.json e sete reviews.json. Pacotes e suplemento exportados. O criador gostou da baseline e pediu a extensao de equipamentos/ataque desarmado antes do fechamento. Os97 PNGs/24 editaveis legados por classe permanecem fingerprintados em source/complete-v1/review.json. Gate consistency e exportacao agora concluidos, conforme evidencia da resposta mais recente.
- [ ] Produzir assets independentes de armas/projeteis/VFX e extensoes runtime de overlays/casts/tiro sincronizado em tarefa propria. Os gestos do corpo por Job e os socos desarmados foram aprovados e exportados.

Baseline preservada:679 PNGs nativos e168 fontes editaveis (28 estaticas +140 animadas) nas sete variantes, mais o Warrior ja aprovado/exportado. Isso nao comprova todos os ataques por equipamento. Extensao atual:120 PNGs e24 editaveis adicionais ativos unarmed, com reuso de fontes originais Warrior/Brawler. Plano raiz aponta EXPORTED_LOCAL_BODY_AND_UNARMED. Conceitos/bases, locomocao completa e combate front_r legados aprovados; Gate consistency e exportacao das sete variantes concluidos. Proximo: armas/projeteis/VFX independentes e bindings demonstrados, com revisoes artisticas. Integracao Unity exige tarefa autorizada separada. Armas/efeitos, bindings e integracao Unity permanecem pendentes.

- [x] Repositorio local independente e comandos Node instalados.
- [x] Contexto do TacticsRPG e skill copiados com hashes; ancora e Hero documentados com papeis distintos.
- [x] Catalogos de 28 racas e 63 Jobs.
- [x] Fichas, variantes de roupa, pacotes para geracao pela LLM, importacao e previews.
- [x] Composicao de camadas 2D nativas, validacao, revisoes por hash e staging Unity.
- [x] Receitas raciais/de Job com versoes e imagens aprovadas arquivadas.
- [x] Testes de comandos, integridade, composicao, gates e exportacao com fixtures sinteticas.

## 2. Primeiro ciclo artistico — proximo trabalho

1. [x] Preencher propostas visuais e gerar conceito candidato weapon-independent de orc-01 em concepts/ (2026-10-19). Concept-07 é a versão escolhida e aprovada pelo criador; ver Gate 1 em reviews.json.
2. [x] Concept-07 careca escolhido e aprovado pelo criador em 2026-10-19; Gate 1 registrado com hash. Anteriores preservados como históricos.
3. [x] Produzir base nativa e quatro vistas candidatas: 5 PNGs 128x128 RGBA, 100px de altura, ground126, mesma paleta; validação directions sem FAIL. Revisão artística permanece no item 4.
4. [x] Base e quatro vistas aprovadas explicitamente pelo criador: "Aprovo a base e as quatro vistas; continue as animações." Gate base registrado com hash atual em reviews.json.
5. [x] Criar conceito de roupa Archer do MESMO individuo em orc-01-archer; conceito aprovado e primeira base front_r nativa produzida, em revisao junto das outras seis classes.
6. [ ] Documentar e aprovar receitas visuais de Orc/Warrior/Archer com regras e referencias reais. Apenas candidatos de regras ate a decisao do criador.
7. [ ] Criar conceito de undead-01 Archer usando a receita Archer aprovada, com anatomia racial propria. Revisao: classe reconhecivel entre racas, mesma linguagem global.

## 3. Prova de producao — conjunto aprovado e exportado

- [ ] Demonstrar fonte editavel 2D e roupa em camadas nativas compativeis numa vista, com ordem/oclusao documentadas.
- [x] Produzir Idle e Walk nas quatro vistas; revisao artistica do conjunto aprovada pelo criador.
- [x] Produzir Attack/Hit/Defeat nas quatro vistas. Tiro de arco/cast requer desenho e analise de playback proprios.
- [x] Validar os 97 PNGs: 489 PASS, 0 FAIL, 1 aviso esperado (fallback igual a front_r). Vinte clipes editaveis verificados por roundtrip RGBA e duracao no LibreSprite; seis testes locais aprovados.
- [x] Registrar revisao artistica de consistencia: "Aprovo o conjunto completo; exporte o pacote." Gate consistency vigente em reviews.json.
- [x] Exportar pacote aprovado para dist/orc-01/9b89aad88c27de68 e verificar 97 PNGs contra manifesto/hashes. Importador fornecido; compilacao Unity ainda NOT_RUN.

## 4. Melhorias tecnicas que podem acompanhar as revisoes

Os itens ainda nao marcados sao backlog; os concluidos possuem evidencia nos documentos vinculados.

- [ ] Comando status: mostrar personagem, revisoes atuais/desatualizadas, arquivos faltantes e proxima acao, derivando os JSONs existentes.
- [ ] Comparacao visual lado a lado entre versoes/roupas/racas e entre referencias de um mesmo Job.
- [x] Preview de animacao Orc com cinco estados, quatro vistas sincronizadas, velocidades, scrubbing e pausa; 92 quadros carregados sem erros de JavaScript no Edge. Generalizacao para outros pacotes continua no backlog.
- [x] Exportacao assistida Aseprite com perfis explicitos de autoria, metadados/tilemap e aplicacao baseline com gates; docs/ASEPRITE.md. Perfis que exigem runtime novo continuam bloqueados no exportador Unity.
- [ ] Preparar migration/versionamento de fichas antes de mudar schemaVersion.
- [ ] Definir pacote compartilhado de assets de armas e estender o runtime para exibi-las separadamente somente quando equipadas e invocadas por uma acao; validar encaixe, oclusao e sincronizacao. O contrato visual esta decidido, a implementacao nao.

Se o usuario pedir para continuar engenharia enquanto avalia arte, partir da primeira tarefa desta secao ainda pendente. Conservar os marcos artisticos e registrar que a implementacao tecnica nao aprovou nenhum desenho.

## 5. Integracao no jogo — tarefa futura autorizada separadamente

- [ ] Auditar o codigo atual do jogo novamente e definir registro minimo multi-personagem para UnitVisuals.
- [ ] Integrar um pacote aprovado em ../TacticsRPG/Assets/Resources/Characters/<id>/ preservando GUIDs.
- [ ] Compilar o importador, confirmar Resources.Load/importacao e executar revisao PlayMode.
- [ ] Registrar aprovacao final em jogo pelo criador.

O staging local ja esta implementado. O registro multi-personagem e a integracao real ainda estao pendentes. Camadas de equipamento no runtime e novos estados sao extensoes futuras; combinacoes completas compostas offline sao o fluxo inicial.

## Estado dos exemplos na entrega

| Pacote | Conteudo atual | Proxima entrega |
|---|---|---|
| hero-reference | 97 PNGs historicos, preview, relatorio; reference_only | Consultar como referencia; 34 divergencias de chao registradas, sem retoque automatico |
| orc-01 | Concept-07 careca e base aprovados; 97 PNGs nativos, 20 clipes animados editaveis e 4 fontes estaticas; prompts/fontes/hashes preservados | Conjunto aprovado e exportado em dist/orc-01/9b89aad88c27de68. Integracao Unity, PlayMode e armas independentes permanecem pendentes. |
| orc-01-archer | Baseline97 PNGs/24 editaveis +20 PNGs/4 editaveis unarmed; primeiro front_r desarmado aprovado | Conjunto/suplemento aprovados e exportados; proximos assets de armas e bindings |
| orc-01-squire / apprentice-mage / acolyte / rogue / scout / brawler | Baseline97 PNGs/24 editaveis por roupa; +20 PNGs/4 editaveis unarmed por roupa exceto Brawler, que reusa Attack; prefixo completo orc-01- em cada ID | Conjunto/suplemento aprovados e exportados; proximos assets de armas e bindings |
| undead-01 | Ficha Archer e handoff; conceitos ausentes | Conceito com receita Archer aprovada |

## Historico

- 2026-10-19: criador aprovou quatro vistas das sete classes e autorizou animacoes; Gates base registrados. Primeiro lote real Idle/Walk front_r:70 quadros,14 clipes editaveis. Reuso das dez poses Warrior como guia neutro de silhuetas e ferramentas existentes; novas roupas realmente desenhadas pela image_gen. Primeira fonte Squire rejeitada por herdar armadura Warrior; Scout Idle original selecionado, Walk corrigido com guia anotado apos uma edicao rejeitada por manter/duplicar manta no quadril errado. Dez chamadas reais nesta etapa; PNGs/prompts/referencias/origens/recortes/hashes preservados. Verificacao nativa e de proveniencia sem falhas; LibreSprite70/70 RGBA e duracao identicos; Edge70/70 canvas RGBA identicos em HTTP e exibicao file://, zero erros JS, servidor local encerrado. Total105 PNGs/42 editaveis; restante574 quadros. Primeiro lote aguarda revisao artistica antes das demais vistas; consistency/export/Unity pendentes.

- 2026-10-19: criador aprovou as sete primeiras bases para expandir outras vistas. Evidencia parcial com hashes preservada, sem autoaprovar Gate base completo. Produzidas 21 vistas novas via sete folhas e tres correcoes (Squire front_l, Mage back_l, faixa Brawler back_l). Todas importadas com prompts/fontes/hashes reais; paleta comum por roupa, alfa binario, altura100/ground126, frontais aprovadas intactas. 35 PNGs no total e 28 editaveis conferidos no LibreSprite RGBA identico. Validacao175 PASS/0 FAIL; preview Edge com 28 vistas/filtros/zoom/fundo e zero erros JS. Quatro vistas aguardam revisao conjunta; Gate base, animacoes das roupas, export e Unity ainda pendentes.

- 2026-10-19: criador aprovou seis roupas e pediu Rogue mais escuro/furtivo; Rogue v2 gerado/importado e depois aprovado explicitamente. Sete fontes novas de sprite image_gen, usando conceito aprovado + Warrior nativo como referencias, sem reduzir conceitos. Processamento Pixel Art Fixer forced/100px/paleta48; 14 PNGs importados pelo CLI com hashes/prompts reais. Sete fontes .aseprite exportadas no LibreSprite e verificadas RGBA identico. Preview testado no Edge: oito nativos e oito conceitos carregados, zoom1x/2x/3x, fundo e zero erros JS. Relatorios em characters/orc-native-base-*.json; fontes em cada source/native-base-v1. Primeiras bases aguardam criador antes das demais vistas. Nenhum Gate base/consistency/in-game autoaprovado; nenhuma escrita no jogo.

- 2026-10-19: pedido de producao das outras classes basicas Orc com economia por reuso. Produzidos sete conceitos distintos e preservada a arte aprovada Warrior. Reuso planejado com evidencia por componente; fontes do Warrior indexadas sem copias redundantes. Alpha original dos conceitos preservado (inclusive pixels parciais/perifericos; nao adequado a runtime sem autoria nativa). Conferencia dos sete conceitos RGBA/procedencia e preview real sem falhas; Gate 1 solicitado numa unica revisao, ainda pendente. Nenhum sprite novo de variante, receita aprovada ou integracao Unity foi declarado/executado.

- 2026-10-19: criador aprovou explicitamente todo o conjunto animado e pediu exportacao. Gate consistency registrado com evidencia real; 97 PNGs exportados localmente em dist/orc-01/9b89aad88c27de68, com manifesto de hashes, validacao e importador opcional. Nenhuma integracao Unity ou aprovacao em jogo foi registrada.

- 2026-10-19: criador aprovou base e quatro vistas e autorizou continuar animacoes. Produzidos 92 quadros (Idle 16, Walk 24, Attack 20, Hit 12, Defeat 20), completando 97 PNGs 128x128 RGBA, paleta comum de 46 cores, alpha binario e ground126. Fontes artisticas novas image_gen, grade alvo explicita, registro e acabamento RGB documentado; modelo nao exposto pela ferramenta. Walk front_r usa selecao de poses de duas geracoes (tentativa intermediaria rejeitada); Attack back_l foi redesenhado para manter ataque com braco direito; materiais das pernas Walk corrigidos sem mudar silhueta. Historicos rejeitados preservados. Vinte arquivos animados .aseprite foram exportados no LibreSprite e comparados pixel a pixel e por duracao. Verificacao completa: 489 PASS/0 FAIL/1 aviso esperado; npm test 6/6; preview real testado em HTTP e file:// com 92 PNGs e cinco estados. Manifesto em source/animations-v1/manifest.json; relatorios em characters/orc-01/reports/. Revisao artistica de consistencia solicitada e pendente; exportacao e PlayMode ainda NOT_RUN. Nenhuma escrita no projeto Unity.

- 2026-10-19: decisao do criador: conceitos e sprites base de personagens ficam sem armas; armas sao assets separados e aparecem somente quando equipadas e invocadas por uma acao. O conceito armado anterior de orc-01 foi preservado como historico e uma versao weapon-independent foi gerada; Gate 1 continua pendente. Runtime ainda exige extensao.
- 2026-10-19: feedback do criador aprovou a armadura do Orc, mas pediu feicao mais selvagem/brutal e cabelo menos humano/arrumado. Gerado `concept-03` preservando armadura e mãos vazias; Gate 1 continua pendente.
- 2026-10-19: o criador aprovou a feição do conceito 03, mas pediu reduzir muito o volume do cabelo e afastá-lo de um penteado humano. Revisar apenas o cabelo; preservar rosto, armadura e mãos vazias.
- 2026-10-19: o conceito 04 reduziu o cabelo, porém a crista ainda foi lida como humana. Próxima revisão: apenas cerdas curtas e irregulares junto ao couro cabeludo, sem crista; manter rosto e armadura.
- 2026-10-19: o criador considerou o conceito 05 melhor, mas calvo demais. Ajustar para mais cobertura e volume moderado de cabelo curto, áspero e irregular; manter rosto e armadura.
- 2026-10-19: a pedido do criador, gerada variante totalmente careca `concept-07` para comparação. `concept-06` permanece candidato principal até escolha explícita; ambas as versões preservam rosto/armadura e ficam sem arma.
- 2026-10-19: gerado/importado `orc-01-warrior-concept-01.png` como candidato Orc Warrior, Job básico inicial com afinidade Orc. Prompt e referências foram registrados no pacote; Gate 1 segue pendente da revisão do criador.
- 2026-10-18: entrega da base tecnica, documentacao, referencias e quatro pacotes de exemplo. Nenhuma arte nova ou aprovacao de personagem produzida.
- 2026-10-18: instrucoes de continuidade, destinos automaticos e backlog de evolucao explicitados para retomada com prompts curtos.

- 2026-10-19: produção completa de concept-07 solicitada. Plano de 97 PNGs em characters/orc-01/source/production-plan.json. Primeira geração image_gen ignorou o pedido 128x128 e retornou 1254x1254: arquivada em source/orc-01-base-front-r-attempt-01.png, sem redução. Validação base FAIL: sprite nativo ausente. Próximo: produzir base nativa e revisar antes de expandir vistas/animações. Export/Unity NOT_RUN; armas independentes e runtime ainda exigem extensão.

- 2026-10-19: criador reiterou produção de TODOS os assets de produção Orc Warrior. Duas novas tentativas reais image_gen (02 e 03) buscaram desenho pequeno em canvas maior, para recorte sem reescala; ambas falharam em escala nativa, com alfa parcial excessivo, e 03 introduziu halo/alteração da armadura. PNGs e prompts preservados em source; relatórios em reports/base-attempt-02.json e base-attempt-03.json. Inventário full: 97 ausentes, 0 PNGs de produção aceitos. Pedido permanece incompleto por limitação de geração nativa; não depende de nova autorização do usuário. Necessária autoria 2D nativa que preserve concept-07. Nenhuma alteração Unity, export ou aprovação artística nova.

- 2026-10-19: autorização ampliada do criador para linguagens/dependências/ferramentas gratuitas. Instalados uv, Python 3.12.15, Pixel Art Fixer MIT (ef376e5) e LibreSprite 1.3 portátil. Solução executada: novas fontes artísticas para sprites + reconstrução estrutural de grade alvo explícita (forced), paleta nativa comum e registro. Produzidos fallback + 4 vistas em sprites (5/97); 4 fontes editáveis em source/pixel-grid-v1, roundtrip RGBA idêntico, reprocessamento front_r byte idêntico. Corrigida faixa traseira inconsistente de back_r; v1 preservada rejeitada. Directions: 25 PASS, 0 FAIL, 1 aviso esperado fallback duplicado; npm test 6/6. Preview concreto: characters/orc-01/review-base-v1.html. Gate base aguarda criador; nenhuma autoaprovação. Próximo: registrar revisão real, produzir/revisar Idle front_r e Walk front_r; depois outras vistas e combate. Armas independentes, export e Unity permanecem pendentes.

- 2026-10-19: feedback real do criador: Walk esta otimo; reduzir expansao exagerada do peitoral no terceiro Idle. Walk aprovado por hashes em sete registros parciais. Sete edicoes reais image_gen preservadas em source/idle-subtle-v2/, prompt e referencias com hashes; acabamento nativo local somente no torso do quadro02, silhueta limitada pela neutra +1pixel por lado no pico. Cabeca, maos e membros inferiores preservados; 63 outros quadros e sete editaveis Walk intactos. Originais em previous-idle/. Sete fontes Idle reconstruidas, exportacao LibreSprite28/28 RGBA+duracoes identicas; contrato/paleta/proveniencia70/70 e navegador70/70 canvas identicos, sem erros JS. Preview v2 pronto; somente Idle revisado aguarda criador. Total105 PNGs/42 editaveis e574 quadros restantes.

- 2026-10-19: criador aprovou Idle v2 das sete classes e autorizou demais vistas; evidencia e hashes parciais registrados. Produzidas21 folhas10 poses image_gen, apos uma tentativa30 poses cortada rejeitada, total22 chamadas reais. Fontes/prompts/referencias/recortes/processamento/hashes preservados. Novos210 PNGs e42 editaveis Idle/Walk front_l,back_r,back_l; conjunto280 quadros/56 clipes. LibreSprite210 novos RGBA e duracoes identicos; paleta/contrato/proveniencia e preservacao dos70 quadros/14 clipes front_r aprovados verificados. Edge280/280 canvas RGBA identicos, quatro vistas/dois estados, controles e exibicao file:// testados, zero erros JS; servidor fechado. Total315 PNGs/84 fontes editaveis ativas,364 quadros de combate pendentes. Review novo enviado antes de combate conforme WORKFLOW. Warrior e Unity intactos.

- 2026-10-19: criador aprovou as tres vistas de locomocao e autorizou combate; registros parciais atualizados por hashes, sem Gate consistency incompleto. Produzidos Attack5/Hit3/Defeat5 front_r nas sete classes:91 PNGs/21 editaveis. Onze chamadas image_gen reais: sete folhas13 poses e quatro edicoes de Attack Mage/Brawler; v2 rejeitadas por manter mao incorreta, v3 selecionadas apos guias explicitos de braco direito. Hit/Defeat originais preservados. Extrator aceita alturas relativas e registro por pelve opcionais para manter escala de bracos erguidos; importador/editor existente generalizado por --batch/--report. Native/paleta/proveniencia91/91; LibreSprite91/91 RGBA+duracoes identicos, Edge91/91 canvas exatos e parada final one-shot, exibicao file:// e controles, zero erros JS; npm6/6. Locomocao280 quadros/56 editaveis e Warrior97 PNGs/20 animados intactos. Ensaio legado preservou alpha/crop/registro6/6 mas detectou cores nao reprodutiveis no OpenCV; seed42 por asset corrigido para trabalho futuro, tres reconstrucoes iguais no mesmo ambiente; lote existente nao reprocessado. Total406 PNGs/105 editaveis ativos,273 quadros restantes. Review primeiro combate enviado conforme WORKFLOW; export/Unity ainda pendentes. Detalhes em docs/ORC_COMBAT_FRONT_V1.md.

- 2026-10-19: criador aprovou unarmed front_r;90 novos quadros e18 editaveis completaram front_l/back_r/back_l das seis roupas.26 PNGs reais image_gen nesta etapa,18 fontes selecionadas/oito tentativas preservadas: Squire corrigido para remover metal herdado, seis back_l redesenhadas com soco direito distante/oclusao, Rogue front_l com capuz restaurado. Guias de poses reais Warrior/roupas proprias reutilizados sem espelhamento ou alteracao da baseline.32/32 clipes unarmed nativos,160 referencias (120 novas/40 reutilizadas),24 novas fontes; zero quadros faltantes. Paleta/RGBA/proveniencia/roundtrip LibreSprite/hashes PASS; frente aprovada e baseline intactas. Previa final conjunta oito roupas/seis estados/quatro vistas:896 referencias carregadas,896 hashes RGBA canvas exatos HTTP, exibicao file:// e controles PASS, zero erros JS; npm9/9 PASS. Uma revisao final artistica enviada conforme Gate2. Exportacao suplementar ainda exige extensao, Gate consistency/export nao autoaprovados, nenhuma escrita Unity. Evidencias:docs/ORC_UNARMED_DIRECTIONS_V1.md.

- 2026-10-19: criador autorizou continuar se incluido hit normal desarmado; condicao verificada (soco fisico e reacao Hit nas quatro vistas). Sete Gates consistency registrados com evidencia literal, suplemento aprovado por fingerprint, Warrior original intacto. Exportador complementar implementado com bloqueio de aprovacao desatualizada/hashes/canvas/overlay e fontes escolhidas; baseline CLI preservada. Oito builds completos exportados com896 PNGs e216 fontes, hashes conferidos; reexecucao idempotente preservou builds. ZIP10.52MB,1186 entradas, CRC e1184 hashes +README/MANIFEST verificados. Doctor PASS; suite11/11 PASS. Previa/plans/docs atualizados para EXPORTED_LOCAL_BODY_AND_UNARMED. Detalhes e links em docs/ORC_PRODUCTION_EXPORT_V1.md. Armas/VFX/bindings e Unity continuam pendentes, sem escrita no jogo ou Gate3.
# Refinamento PixelLab v2 em andamento — 2026-10-23

Feedback vigente: Walk 04/07 sem passada legível; Idle 04/07 precisa melhorar; Idle 06 exagerado; conceito 05 precisa de armadura mais detalhada e imponência Uruk-hai. 241 arquivos anteriores preservados por hash. Controle recuperado e Pro habilitado após atualização oficial. Walk 04 PixMiniMax16 concluído; conceito05 revisado; Idles04/05/06/07 ajustados no Aseprite com respiração0/1px e rosto/pés fixos. Walk07 gerando; Walk05 pendente. Pedido adicional: dois conceitos de padrões diferentes, IDs08 Vigia do Passo e09 Matriarca da Cinza, contextos preparados, geração posterior. Retomada exata em `reports/orc-pixellab-refinement-v2-progress.md`; prompts em `experiments/pixellab-orc-refinement-v2/brief.json`. Verificação/entrega final pendentes; sem aprovação artística ou integração Unity.
