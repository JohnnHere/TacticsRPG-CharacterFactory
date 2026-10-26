## Política vigente — Orc principal e armas somente no ataque, 2026-10-25

O Orc principal atual é **orc-v1 / Verde Warcraft**, em characters/orc-v1/. O antigo Orc V4 está descartado e nunca é fonte de restauração ou direção atual. A identidade atual é a referência; poses de ataque defeituosas podem ser substituídas.

Espada/machado ficam **ocultos no Idle, Walk, repouso, inspeção, Hit/Defeat e após a ação**. Aparecem somente no intervalo declarado do Attack. Os pedidos anteriores de Idle/Walk armados e o corte único compartilhado entre Sword/Axe estão **SUPERADOS**. São dois perfis: corte de espada e golpe de machado, reutilizáveis entre itens compatíveis da própria categoria. Sem sacar/embainhar, rig universal ou animação corporal por item.

Guia atual: docs/MAIN_ORC_ONE_HANDED_RESCUE.md; autoridade de identidade: reports/orc-production-current.json. Armas seguem a linguagem visual do jogo, sem obrigação de copiar a paleta/cultura Orc. Aseprite continua mestre; PixelLab autorizado auxilia poses; toda edição/exportação artística é no Aseprite. Esta tarefa não modifica Unity nem concede aprovação artística. **Nos registros anteriores abaixo, toda afirmação conflitante de V4 ativa, nenhuma seleção, arma em Idle/Walk ou movimento universal é histórica e superada.**

# PixelLab via Aseprite — integração e avaliação independente

**Histórico superado — 2026-10-24:** V4 ativa e V4 Reimaginado descartados pelo criador; não reutilizar como direção selecionada nem reativar pelos scripts históricos. Arquivos preservados como histórico. Nenhuma seleção de produção ativa. Novo candidato `orc-pixellab-11` (Orc Atlético): parecido com o Ágil, menos armadura, mais musculatura e verde um pouco mais claro. Revisão corrente: `reports/orc-current-review/review.html`. Vigia e Matriarca ficam separados em `ideas/unique-characters-or-npcs/` como ideias futuras de NPC e/ou jogáveis únicos. Esta decisão substitui afirmações históricas de V4 selecionada abaixo.

**Candidata atual de Walk — V8, 2026-10-24:** V7 rejeitada por orientação da cabeça e marcha. Base própria frontal gerada com `edit_image_pro_flash`, animação inteira `animate_with_skeleton_v3`, oito quadros/100 ms. Guia Ágil usado somente para extração e adaptação de fases; nenhum enxerto de rosto/paleta. Alternativa `animate_image` descartada por maior deriva. Relatório: `reports/orc-pixellab-refinement-v8.md`; página conjunta: `reports/orc-pixellab-v4-comparison/review.html`. PixelLab Pro ativo; nomes dos modelos registrados separadamente do plano. Aprovação artística pendente.

**Pedido vigente de 2026-10-24 — Walk completo e revisão conjunta:** o criador rejeitou também a passada do Reimaginado, não apenas sua cabeça. Nesse caso, a regra anterior de preservar aquela passada foi superada: refazer corpo/pescoço/direção juntos, com poses controladas, usando só o conceito próprio. Candidata Skeleton V3 v7 e limites em `reports/orc-pixellab-refinement-v7.md`. Mostrar sempre todos os conceitos/Idles/Walks existentes juntos na página canônica, incluindo Infante cabeludo e ideias reservadas; comando `node tools/build-orc-all-review.mjs`. Não continuar substituindo cabeças sobre um ciclo corporal rejeitado.

**Regra extraída da revisão v4:** se o defeito é localizado (sombras da cabeça, direção do olhar, cabelo), preservar a passada aprovada e retocar/reutilizar uma peça registrada no Aseprite. Gerar/reparar apenas a região necessária pelo MCP quando houver mudança artística. Não regenerar todo o Walk para corrigir só a cabeça. Este caso não autoriza compressão de faixas no torso nem um rig universal. Evidência e limitações: `reports/orc-pixellab-refinement-v4.md`.

**Interface adicional autorizada em 2026-10-23:** [MCP oficial PixelLab](PIXELLAB_MCP.md), configurado e autenticado. Pedidos podem rodar sem UI; importação, retoque e mestres continuam no Aseprite. Correção do criador: Vigia e Matriarca são ideias de **personagens únicos jogáveis OU NPCs**, reservadas em `ideas/unique-characters-or-npcs/`; a classificação apenas como NPC abaixo é histórica e foi substituída.

## Correção vigente — avaliação do criador em 2026-10-23

**Licença ativa: PixelLab Pro**, confirmada explicitamente pelo criador. Selecionar e registrar o modelo real na interface. O nome histórico “Create S-XL image (pro)” corresponde a pedidos cujo seletor estava em Pro; não confundir nome do comando, modelo e plano da conta.

O criador rejeitou os quatro Idles locais do refino v2 por aspecto quebrado e a caminhada 07 por orientação torta; o Walk 04 também não resolveu sua expectativa. Os PASS técnicos anteriores não constituem aceitação visual. **Não reutilizar compressão/translação de faixas do tronco como solução automática de Idle.** Examinar articulação contínua, direção fixa, apoio e fechamento em reprodução, além da folha de poses. A observação do criador sobre respiração não é a causa da implementação inadequada.

Vigia do Passo e Matriarca foram reservados em `ideas/npcs/` como ideias futuras de NPC, sem direção racial/genérica. Veterano Ágil deve receber rebranding completo: Orc atlético, sem aspecto gordo/inchado, paleta contida e armadura imponente articulada que permita agilidade sem parecer pesada. Infante mantém rosto e imponência da armadura como elementos apreciados; cabelo deve ser revisto. Rodada corretiva em `experiments/pixellab-orc-refinement-v3/`; nenhuma aprovação global inferida.

Decisão expressa do criador em 2026-10-23: incorporar **PixelLab pela extensão oficial para Aseprite** ao fluxo de produção de arte. Essa autorização atualiza a restrição anterior a geradores externos/serviços especializados especificamente para PixelLab via Aseprite. Aseprite continua sendo o editor e o arquivo `.aseprite` salvo continua sendo o mestre de trabalho. Registrar corretamente a geração PixelLab e os retoques posteriores; não descrever geração em nuvem como desenho manual ou geração local do Aseprite.

## Estado e instalação

Atualização de 2026-10-23: refino concluído com três caminhadas PixMiniMax de 16 quadros, quatro Idles locais e três novas chamadas de conceito Pro (Infante e dois indivíduos adicionais). Evidência atual: `reports/orc-pixellab-refinement-v2.md`; 14 mestres/94 quadros conferidos e 306 comparações de pixels visíveis na apresentação. A descrição abaixo registra a instalação e a primeira rodada, não o total acumulado.

Extensão oficial **PixelLab 0.4.130 instalada** a partir de `PixelLab.aseprite-extension`, baixado pelo criador em Documentos. Pacote SHA256 `c6471eb7634a2f842159b47f72b726ca6a4dc85776eaf8faad650f7ed08e3a22`; 652 arquivos extraídos e conferidos em `%APPDATA%/Aseprite/extensions/pixellab`. Painel PixelLab e Create image Pro abertos no editor; permissões iniciais concluídas pessoalmente pelo criador. Funcionamento comprovado por uma geração Pro (quatro saídas, três selecionadas) e seis animações reais de oito quadros. Há nove mestres de revisão e 51 quadros exportados/comparados pelo bridge; a prévia também passou em 51 comparações RGBA. Consultar `reports/pixellab-extension-install.json`, `reports/pixellab-integration-status.json` e `node tools/pixellab-status.mjs` para evidência local. O status automático detecta arquivos, sem ler credenciais, e não prova autenticação.

Verificação posterior, em 2026-10-23: o criador assinou PixelLab Pro e três chamadas adicionais de geração Pro concluíram pela extensão oficial sem bloqueio de login. O mesmo lote produziu oito pedidos de animação V3 para quatro candidatos. Não guardar dados da conta; o débito efetivo continua `NOT_EXPOSED`. Evidência e resultados: `experiments/pixellab-independent-orc-round2-v1/provider-status.json` e `reports/orc-pixellab-round2-status.md`.

Instalador repetível: `tmp/pixel-venv/Scripts/python.exe tools/install-pixellab-extension.py CAMINHO_DO_PACOTE`. Valida identidade, caminhos/links, tamanho e conflitos antes de escrever; versões diferentes existentes não são sobrescritas. Não copiar o pacote ou `package.json` da extensão para o Git: o pacote obtido na conta pode conter informação de autenticação. Somente versão/hashes e metadados públicos vão aos relatórios.

Compatibilidade batch: PixelLab 0.4.130 tenta construir `Dialog` na inicialização, causando erros quando não há GUI. O bridge agora define `ASEPRITE_USER_FOLDER=tmp/aseprite-batch-profile` somente nos subprocessos batch. A instalação e o perfil do usuário continuam na GUI normal. Assim exportações/testes não inicializam PixelLab nem fazem chamadas de geração. Dois testes reais de descoberta/bridge passaram após a correção. Essa separação usa a [variável oficial de pasta de preferências](https://www.aseprite.org/docs/preferences-folder/).

1. Criador entra na conta pelo site oficial. Senha, tokens e códigos são preenchidos pelo próprio criador e não entram no chat, no Git ou nos relatórios.
2. Obter a extensão pelo botão de download da conta. Registrar versão, origem pública e SHA256 do pacote; guardar o instalador somente em diretório local ignorado, sem URLs assinadas ou credenciais nos relatórios.
3. Instalar pelo gerenciador de extensões do Aseprite (`Edit > Preferences > Extensions > Add Extension`) ou por extração no diretório de extensões conforme o formato oficial. Preservar qualquer versão anterior.
4. Abrir/reiniciar o editor com os documentos do criador salvos. Permissões de arquivos/conexão e eventual autenticação da extensão são etapas verificadas na instalação; o criador conclui diretamente os diálogos sensíveis que exigirem sua intervenção.
5. Conferir `Edit > PixelLab > Open plugin`, disponibilidade da conta e ferramenta de criação. Somente após isso registrar instalação operacional. Uma geração real salva é evidência separada de funcionamento.

O serviço executa modelos em nuvem e utiliza a conta/plano/créditos do criador. Não comprar assinatura, upgrade ou créditos automaticamente. Confirmar a disponibilidade real da conta antes de gerar; não afirmar custo zero ou economia de tokens sem medição. O bridge batch de exportação continua local e não passa a ter uma API PixelLab por instalar a extensão.

## Experimento independente solicitado

O objetivo é descobrir se PixelLab + Aseprite oferece uma direção artística melhor que a atual. **Começar sem qualquer inspiração visual ou material herdado dos nossos assets.** Não carregar Orc V4, estudos V5, Human Warrior Pilot, âncora global, folhas, receitas, paletas, poses, sketches, máscaras ou referências de estilo anteriores como condicionamento. Não copiar seus pixels para formar o candidato. Não usar o `prepare` padrão como prompt direto desta experiência, pois ele inclui referências legadas.

Pedido subsequente do criador, no mesmo dia: **três opções de Orcs com inspirações Tolkien + World of Warcraft**, sem sequer consultar a V4/conceitos V4, de preferência já com animações básicas para avaliar o potencial em jogo. Essa instrução atualiza o briefing inicial sem franquias: os nomes Tolkien/Warcraft são agora usados como referências textuais de arquétipo e atmosfera, com designs originais. Não usar personagens/símbolos comerciais específicos como assets.

Usar canvas novo e vazio, geração por texto, init image desativada e nenhuma referência de estilo/paleta. Descrever Orc Warrior adulto medieval, corpo inteiro, leitura tática, mãos vazias e sem armas carregadas/embainhadas, sem cenário/texto. Deixar espaço para o PixelLab propor rosto, cabelo, corpo, paleta, roupa, luz e acabamento. Não abrir artes antigas nem copiá-las para esta experiência. A comparação com o acervo só pode ocorrer em etapa posterior autorizada; as três opções atuais devem ser comparadas entre si.

Protocolo preparado em `experiments/pixellab-independent-orc-v1/brief.md` e `experiment.json`. Nenhuma imagem de entrada. Registrar parâmetros realmente disponíveis, ferramenta/modelo/versão mostrados, prompt exato, seed quando exposta, resolução, conta autenticada sem identificadores sensíveis, duração e consumo exibido. Se algum dado não existir, registrar `NOT_EXPOSED` em vez de inventar. A primeira geração deve ser preservada intacta; acabamento no Aseprite fica em camada/cópia identificada para comparação honesta.

Pacotes entregues sem consulta a arte legada na primeira rodada: **orc-pixellab-01 — Veterano da Vanguarda**, **orc-pixellab-02 — Quebra-Linhas**, **orc-pixellab-03 — Campeão de Bronze**. São três indivíduos candidatos, não roupas do Orc atual. Os rótulos iniciais do planejamento foram substituídos pelos nomes das saídas reais em selected-candidates.json. Os quatro resultados brutos foram preservados. Cada handoff contém apenas seu próprio conceito novo. Uma única requisição Create image Pro gerou quatro propostas 128×128; seis requisições Animate with Text (v3) geraram Idle e Walk, oito quadros por clipe. Os modelos/seed/prompts reais estão em source/generation-record.json e source/studies/<estado>/clip.json. Custos anunciados: Pro 10–25 gerações por requisição e animação 1–8; débito efetivo NOT_EXPOSED. Naquela etapa, o criador ainda não havia comprado o plano.

## Segunda rodada — quatro direções Orc

Depois da primeira rodada, o criador autorizou uma comparação com o acervo e pediu quatro novas direções, reservando a referência visual V4 explicitamente para o quarto pedido. Após a assinatura do criador, foram produzidos quatro conceitos adicionais para comparação, IDs `orc-pixellab-04` a `orc-pixellab-07`. O bloqueio do plano gratuito foi histórico; três conceitos Pro (05–07) concluíram pela extensão sem problema de autenticação. O conceito 04 veio de Pixen S-XL, em texto, antes da assinatura.

- **04 Veterano Ágil:** texto, sem referência de imagem. A geração ficou mais robusta do que o prompt atlético sugeria.
- **05 Infante de Ferro:** PixelLab Pro, texto sem imagem de referência; infantaria pesada de ferro escuro.
- **06 Soldado da Vala:** PixelLab Pro, texto sem imagem de referência; silhueta magra, curvada e de equipamento gasto.
- **07 Veterano V4 Reimaginado:** PixelLab Pro com a V4 enviada pelo Aseprite **Set style**. Esta é a única opção desta rodada que usou imagem V4 como referência; a V4 não foi usada como init image nem houve cópia de pixels. A amostra `v4-style-128.png`, fonte original, hashes e registro da chamada ficam no pacote 07.

Cada candidato tem um Idle e um Walk de oito quadros produzidos pelo Animate with Text (v3) e arquivados como `.aseprite` editável e PNGs de revisão. A galeria `reports/orc-pixellab-v4-comparison/review.html` compara a V4, os três candidatos da primeira rodada e os quatro da segunda. Todos continuam candidatos sem aprovação. As animações variam do início ao último quadro e precisam de avaliação de fechamento de loop antes de produção. Os prompts reais e bloqueios antigos estão preservados em cada pacote e no relatório da rodada.

## Operação em segundo plano e entrega

### Sincronização do plano e cuidado com a entrada

Se o plano foi assinado depois do download da extensão, a versão 0.4.130 pode continuar exibindo ferramentas de animação Pro desabilitadas porque o pacote instalado contém o nível anterior. A atualização pelo menu oficial **Edit > PixelLab > Update plugin**, seguida de uma instância que carregue os arquivos novos, sincronizou esse estado nesta sessão. A versão continuou 0.4.130. Preservar os documentos abertos; o criador opera as permissões de conexão/arquivos. A comprovação operacional vem da ferramenta habilitada e da geração concluída, não apenas do arquivo atualizado. Não editar manualmente nível de plano ou dados da conta.

No **Animate with text (PixMiniMax)**, **Set reference image redefine câmera/direção para Auto**. Conferir a miniatura do indivíduo e só depois definir câmera e direção explícitas. A rodada de refino usou 128×128, 16 quadros e, em 05/07, south-east + low top-down (ca 20 degrees). Repetir o nome de uma direção no prompt não substitui conferir esses controles.

Uma sequência com quadros diferentes ainda pode ter pés imóveis, giro do corpo ou variação de detalhes. A revisão de Walk deve observar apoio alternado, levantamento/passagem das botas, orientação, recorte e fechamento. Para Idle discreto, o conceito próprio pode ser reutilizado e retocado dentro do Aseprite: o estudo v2 usa duas poses sustentadas, movimento de um pixel no tronco e rosto/região inferior fixos, sem novas chamadas de geração para esses Idles. Os limites regionais são específicos dos quatro corpos; não são um rig universal. Procedência, prompts, tentativas e resultados em `reports/orc-pixellab-refinement-v2.md`.

1. Abrir a extensão oficial no Aseprite. Uma nova geração ainda exige sua interface; esta integração não expõe uma API headless autenticada.
2. Ativar Edit > PixelLab > Generation queue > Queue new generations in the background. Usar Continue in background na requisição em andamento; as seguintes entram na fila. Não fechar o Aseprite durante o processamento.
3. Para cada personagem, abrir seu conceito e definir explicitamente Set start frame. O painel reutiliza a última entrada e precisa ser atualizado ao trocar de indivíduo. Não selecionar um quadro vazio ou arte antiga. Para Idle/Walk do mesmo conceito, manter essa entrada e substituir apenas a ação.
4. O complemento grava o resultado local em generation_history. O `jobs.json` da primeira rodada relaciona número da fila, personagem, ação e histórico real; a segunda rodada está registrada em `experiments/pixellab-independent-orc-round2-v1/provider-status.json`. `node tools/poll-pixellab-jobs.mjs` recolhe os resultados da primeira rodada sem ocupar mouse/teclado. Somente PNGs de saída e campos permitidos de procedência são importados; configurações e credenciais não são copiadas.
5. O importador confere que `0.png` pertence ao conceito daquele personagem: dimensões, alfa e RGB dos pixels visíveis precisam corresponder. RGB sob alfa zero pode ser normalizado pelo provedor; essa diferença é contada e registrada, enquanto o PNG bruto permanece preservado. Lua dentro do Aseprite monta o mestre bruto (entrada + oito saídas), o mestre de estudo (oito saídas) e exporta PNGs. O tempo de revisão, 100 ms por quadro, foi definido na fábrica: o arquivo PNG do provedor não expõe timing.
6. node tools/build-pixellab-orc-review.mjs monta reports/pixellab-orcs-independent-v1/review.html. Permite comparar conceitos, Idle/Walk, escala nativa/ampliada, fundos, pausa e quadro a quadro. node tools/export-pixellab-review.mjs exporta os nove mestres via bridge para dist/editor; manifesto em experiments/pixellab-independent-orc-v1/editor.json. Não escreve slots de produção.
7. Verificação da apresentação: tmp/pixel-venv/Scripts/python.exe tools/check-pixellab-review.py. Folhas de inspeção: tools/pixellab-motion-contact.py. Esses comandos montam apresentação e conferem pixels; não geram arte.

Locais por candidato: concepts/concept-selected.png, source/aseprite/concept-selected.aseprite, source/aseprite/idle-study.aseprite, source/aseprite/walk-study.aseprite, source/studies/Idle e Walk (00–07.png e clip.json). Originais da extensão em source/pixellab-results; versões brutas preservadas. Evidências: reports/pixellab-jobs-status.json, pixellab-master-roundtrip.json, pixellab-orcs-review-check.json e pixellab-orcs-independent-v1.json.

Leitura artística inicial: as três opções têm anatomia robusta, rostos expressivos e armaduras legíveis. A exploração varia sobretudo paleta, cabelo e armadura; ainda não demonstra três linguagens artísticas radicalmente diferentes. Os movimentos têm poses reais, mas há oscilação de detalhes de mãos/armadura e ajustes de apoio/fechamento do ciclo a revisar. São estudos brutos, não clipes finais. A extensão acelera propostas e movimentos; o Aseprite continua necessário para curadoria, registro, acabamento e consistência. Economia de tokens e custo monetário não foram medidos; não prometer economia com base apenas nesta demonstração.


## Retorno à fábrica e aprovação

Salvar resultados em pacote candidato próprio: conceitos em `characters/<id>/concepts/`, mestres em `source/aseprite/`, parâmetros e procedência em `source/`, contexto sem referências antigas em `handoff/`, revisão em `reports/`. Não reutilizar o identityId do Orc atual se o resultado representar outro indivíduo. Importar PNGs sem reescala e exportar os mestres pelo bridge existente. Não transformar um conceito reduzido automaticamente em sprite de produção.

O Orc V4 continua selecionado em `reports/orc-production-current.json`; estudos V5 continuam candidatos históricos. A experiência independente é exceção autorizada à reutilização automática e à obrigação de seguir a âncora durante a geração. Não rejeitar o experimento só por divergir da arte atual: é essa divergência que está sendo avaliada. Contratos de armas independentes, revisão humana, transparência e requisitos técnicos continuam aplicáveis.

Comparar presença e expressão, coerência de formas, clareza em escala de jogo, materiais, identidade própria e potencial de manter o estilo nas próximas vistas/animações. O criador autorizou explicitamente **estudos candidatos de animações básicas antes da escolha do conceito** para essa avaliação; preservar e identificar como estudo, nunca autoaprovar gates para conseguir importar/exportar. Preferir Idle e Walk de uma vista inicial, expandindo somente se houver evidência útil. Usar apenas o próprio conceito PixelLab novo como entrada das suas animações. Novas poses devem vir do PixelLab/Aseprite; não simular animação de locomoção por deslocar a imagem inteira.

O criador escolhe se alguma proposta merece refinamento. Para produção definitiva, Gate 1 antes da base, base/vistas antes de expandir clipes, Gate 2 antes de exportação de produção e Gate 3 após jogo real. Os estudos podem ser apresentados fora dos slots ativos por manifestos genéricos de revisão, sem contornar esses gates. Três estudos não aprovam três personagens. Instalação não prova consistência de animações, ganho de qualidade ou uma nova direção canônica.

## Referências oficiais verificadas

- [Instalação PixelLab no Aseprite](https://www.pixellab.ai/docs/installation)
- [Formas oficiais de usar PixelLab](https://www.pixellab.ai/docs/ways-to-use-pixellab)
- [FAQ — execução em nuvem e uso da conta](https://www.pixellab.ai/docs/faq)
- [Init image é opcional; criação e edição](https://www.pixellab.ai/docs/getting-started)
- [Formato e instalação de extensões Aseprite](https://www.aseprite.org/docs/extensions/)
