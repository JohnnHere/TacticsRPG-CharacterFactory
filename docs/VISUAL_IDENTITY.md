# Identidade visual

O alvo e personagem 2D em pixel art refinada, legivel em batalha tatica. A apresentacao pode combinar sprites com o mapa 3D do Unity (2.5D e inspiracao HD-2D). HD-2D descreve uma apresentacao visual; nao transforma personagem em modelo 3D. Esta fabrica trabalha com PNGs e fontes artisticas 2D.

## Autoridade

Consulte [ART_DIRECTION.md](../references/tacticsrpg/Docs/ART_DIRECTION.md) e a [ancora aprovada](../references/tacticsrpg/Docs/Art/References/character_style_anchor_v1.png). A ancora define proporcao, materiais, qualidade de sombreamento, maturidade facial, densidade de detalhe e leitura. O usuario aprova cada nova referencia racial/de Job; configs locais derivadas permanecem propostas quando acrescentam conteudo ausente nas fontes.

![Ancora de estilo aprovada na documentacao original](../references/tacticsrpg/Docs/Art/References/character_style_anchor_v1.png)

## Hero como ponto de partida

![Sprite do piloto](../references/tacticsrpg/Assets/Resources/Characters/WarriorPilot/warrior_pilot_mvp1_static_128.png)

O Human Warrior Pilot ocupa o Hero no sandbox; nao e o protagonista definitivo. Foi usado para validar escala, direcoes, billboard, Idle/Walk e clipes. E um humano com armadura prata, ornamentos dourados contidos, capa azul e espada embutida. Esses detalhes pertencem ao piloto. Uma Orc arqueira pode ter anatomia, paleta e roupa proprias e continuar na mesma linguagem visual.

O Hero possui revisoes parciais em datas diferentes. [HUMAN_WARRIOR_PILOT.md](../references/tacticsrpg/Docs/Art/Characters/HUMAN_WARRIOR_PILOT.md) e mais detalhado que o resumo geral do pipeline. Caminhada/combate e handedness ainda possuem pendencias historicas; nao promover os 97 PNGs a arte final aprovada. A ficha hero-reference nesta fabrica fica reference_only e nao e exportavel como producao.

## Personagem base e armas separadas

Conceitos e sprites do personagem representam o corpo e a roupa sem arma empunhada, carregada ou embainhada. Armas sao assets independentes e so aparecem quando estao equipadas e uma acao/animacao as invoca; nao entram por padrao em Idle, Walk ou na arte base. Corpo, roupa, postura e silhueta do Job devem continuar reconheciveis sem a arma. O Human Warrior Pilot, com espada desenhada nos sprites, e uma excecao historica do prototipo.

O contrato visual esta definido; o runtime ainda nao tem o overlay/equipamento dinamico necessario. A fabrica nao deve apresentar uma composicao offline como se ela demonstrasse esse comportamento em jogo.

## Inspiracoes aplicadas

| Inspiracao | O que orientar | Limite |
|---|---|---|
| Final Fantasy Tactics | Leitura de unidade, identidade de Job, proporcoes taticas compactas, quatro vistas | Designs originais do projeto |
| World of Warcraft | Materiais, armaduras marcantes, arquetipo reconhecivel | Detalhe controlado e proporcoes sem exagero cartunesco |
| Tolkien | Fantasia medieval seria, maturidade, culturas e atmosfera heroica | Nenhum design protegido reproduzido |
| Triangle Strategy / HD-2D | Pixel art com profundidade e efeitos de cenario | Acabamento de cena nao substitui pixel art do personagem |

As tres primeiras bases constam em ART_DIRECTION; Triangle Strategy tambem consta nas decisoes de design. Links oficiais para consulta futura: [FFT](https://final-fantasy-tactics-the-ivalice-chronicles.square-enix-games.com/en-us), [Triangle Strategy/HD-2D](https://www.square-enix-games.com/it_IT/news/triangle-strategy-meta-quest-launch-interview). A pipeline nao baixa sprites comerciais nem depende desses sites para funcionar.

## Constancia por meses

Conservar a mesma versao da ancora e receitas aprovadas. Cada ficha recebe styleId; cada importacao registra hash, fornecedor/modelo quando conhecidos e prompt relacionado. Evoluir uma ancora exige nova versao e decisao do criador. Geracao estocastica nao promete imagem identica com o mesmo texto.

Uma receita visual de Archer aprovada deve descrever silhueta, materiais, proporcao do arco/aljava e limites de variacao. Ela ainda nao existe no catalogo: os 63 Jobs possuem papel mecanico e afinidades, nao 63 uniformes prontos. Desenvolver o primeiro Archer e uma decisao visual candidata. Reutiliza-se a linguagem de classe em outras racas, com adaptacoes anatomicas e culturais justificadas.

## Campos para aprovar antes de escalar

Rosto e corpo individual; anatomia racial; idade visual; mao dominante; assimetrias; silhueta do Job; materiais/paleta; direcao de luz observada; equipamento; perfil de canvas/escala. Acordo tecnico e qualidade artistica sao revisoes diferentes.
