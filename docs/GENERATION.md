# Geracao de arte com o agente

A primeira opcao e a ferramenta de imagem disponivel na conversa, se houver. O agente le AGENTS.md, prepara o pacote, abre a ancora e imagens de referencia, gera candidatos e importa arquivos reais. O processo nao precisa de assinatura de gerador especializado de pixel art. A disponibilidade/limites da ferramenta de conversa dependem da sessao/plano existente; a fabrica local continua utilizavel para briefs, composicao e exportacao sem ela.

Todo conceito de personagem e o conjunto base de sprites mostram o personagem sem armas empunhadas, carregadas ou embainhadas. Mesmo Jobs armados comunicam sua identidade pela roupa, corpo, postura e silhueta. A arma e desenhada como asset independente e aparece somente quando equipada e invocada por uma acao. Nao inventar nem embutir uma arma apenas para preencher a mao; a espada do Human Warrior Pilot e excecao historica. O runtime ainda requer extensao para esse overlay dinamico.

## Pedido completo para retomar daqui a meses

> Abra este repositorio. Leia AGENTS.md, docs/VISUAL_IDENTITY.md e docs/WORKFLOW.md. Execute doctor. Quero criar um Orc Warrior original. Crie uma ficha com ID orc-novo; leia as fontes copiadas, abra a ancora e o Hero como referencia opcional. Prepare handoff e gere candidatos de conceito 2D sem armas empunhadas, carregadas ou embainhadas; trate qualquer arma como asset separado a ser invocado por uma acao quando equipada. Marque anatomia/roupa novas como candidate. Salve os PNGs reais e mostre o preview antes de sprites finais.

> Para o mesmo individuo orc-novo ja aprovado, crie a variante orc-novo-archer com Job Archer. Use outfit e mantenha rosto, corpo, paleta racial e assimetrias aprovadas. Aplique a receita de Archer aprovada se existir; proponha o figurino se ainda nao existir. Preserve o estilo global da ancora.

## Pacote transferivel

handoff/prompt.md tem instrucao de etapa e ficha resolvida. handoff/context.md contem os documentos canônicos relevantes completos. handoff/handoff.json lista imagens com papeis, documentos com hashes e a etapa. Caminhos sao relativos a raiz desta fabrica. Para ferramenta sem acesso ao disco, anexe os PNGs indicados e cole o prompt/contexto; use a ficha como referencia escrita. Nao espere que o nome de um arquivo faca a ferramenta enxerga-lo.

Concept: uma identidade candidata. Base: uma vista nativa 128x128 RGBA. Directions: quatro vistas desenhadas de fato. Animation: um estado/lote revisavel. Os pacotes evitam solicitar os 97 PNGs de uma vez. Disponibilidade de ferramenta visual nao comprova pixel art nativa, transparência correta ou identidade entre quadros.

## Arte final

Conceito grande fica em concepts/. Para producao, redesenhar/refinar pixels em canvas nativo. Reducao, paletizacao e nearest-neighbor nao conferem qualidade artistica por si. O importador recusa dimensoes/canal incompativeis para sprites, e a validacao checa inventario e alinhamento. Aprovar clusters, mao dominante, rosto e animacao exige revisao.

Use LibreSprite opcionalmente para editar camadas e timeline: https://github.com/LibreSprite/LibreSprite. Uma fonte editavel deve acompanhar arte final; source/ pode guardar arquivos do editor, camadas por PNG e notas sobre como exporta-las. O programa nao converte PNG chapado automaticamente em camadas de roupa.

## Google existente, quando fizer sentido

NotebookLM pode consultar documentos; arquivos originais e snapshots continuam fonte de verdade. Ferramentas de imagem do Gemini/AI Studio podem receber o pacote manualmente. Flow pode ajudar como referencia de movimento, mas video nao entrega automaticamente frames pixel art coerentes ou transparência. Flow Music e audio. Google Cloud pode hospedar ferramentas futuramente; nenhuma conta Cloud e necessaria aqui.

Assinatura de aplicativos e quota de API possuem regras distintas. A entrega nao configura APIs, login, scraping da interface, credenciais nem cobranca. Registro de fornecedor/modelo desconhecido permanece unknown. Rotas de consulta: [AI Studio](https://ai.google.dev/aistudio), [API Gemini](https://ai.google.dev/gemini-api/docs/billing), [Flow](https://support.google.com/flow/answer/16526234?hl=pt-br).

## Capacidade honesta

Faltou ferramenta de imagem: entregar pacote e NOT_RUN. Gerou conceito: registrar conceito, sem alegar animacoes prontas. Rodou validate: registrar resultado tecnico, sem marcar aprovacao artistica. Gerou PNGs compostos: registrar quais camadas existiam. A fabrica organiza geracao assistida e composicao; a avaliacao visual sustenta a identidade ao longo do tempo.
