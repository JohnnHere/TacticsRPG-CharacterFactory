# Auditoria Orc e candidatos de refinamento v2

Data: 2026-10-22. Estado: **auditoria técnica concluída; candidatos artísticos aguardam o criador**.

## Resultados para revisar

- [Comparador interativo](orc-audit-v2/review.html): conceito antes/depois, Attack e Hit candidatos, acervo dos oito Jobs nas quatro vistas.
- [Evidência técnica e hashes](orc-assets-audit-v2.json).
- [Manifesto dos candidatos](orc-refinement-candidates-v2.json).
- [Prompts, referências, hashes e procedência](../characters/orc-01-refinement-v2/source/generation-record.json).

## Escopo e situação real

Warrior, Squire, Archer, Apprentice Mage, Acolyte, Rogue, Scout e Brawler representam variantes de roupa/Job do **mesmo indivíduo Orc**. Não são oito anatomias raciais, nem um catálogo de inimigos integrado ao jogo.

| Item | Evidência encontrada |
|---|---|
| Baseline legado | 8 × 97 = 776 PNGs; quatro vistas, Idle, Walk, Attack, Hit e Defeat |
| Acervo nativo único | 896 PNGs, incluindo suplementos físicos desarmados; referências reutilizadas não são contadas como novos desenhos |
| Clipes inspecionados | 192 referências de clipe: seis estados × quatro vistas × oito Jobs |
| Fontes editáveis ativas | 216 fontes selecionadas pelos manifestos dos pacotes exportados |
| Suplemento desarmado | 32/32 direções disponíveis, 160 referências de quadro, sem ausências técnicas |
| Gates existentes | Conceito, base e consistência aprovados pelo criador nos oito pacotes |
| Gate em jogo | 0/8; PlayMode não executado nesta auditoria |
| Equipamento/runtime | 0 bindings de armas demonstrados; registro multi-personagem e overlays ainda pendentes |
| Resultado técnico | 0 falhas nos controles executados; avisos e revisões humanas exigidas pelo validador não equivalem a falhas técnicas |

Foi verificada a integridade de PNGs, dimensões, transparência, limites, conteúdo, componentes conexos, diferenças entre quadros, fontes ASE e hashes dos pacotes imutáveis. Foram inspecionadas visualmente as 16 pranchas de locomoção/combate, a âncora, o piloto pertinente, o conceito 07 aprovado e a base nativa Warrior. As métricas de fechamento de loops não sinalizaram salto acima do limiar exploratório usado; isso não certifica fluidez. Nenhum componente minúsculo desconectado foi encontrado nos clipes, mas esse controle não detecta erros de desenho conectados ao corpo.

Os snapshots de ART_DIRECTION, CHARACTER_PIPELINE, DESIGN_DECISIONS, UnitVisuals e UnitView correspondiam por SHA256 aos arquivos do projeto principal no momento da auditoria. UnitVisuals continua com a seleção WarriorPilot; exportação local não significa personagem registrado no jogo.

## Avaliação artística e prioridades

As observações abaixo são propostas de revisão e preservam as aprovações anteriores. Inspeção de contato não substitui reprodução dentro do jogo com cenário, câmera e velocidade reais.

| Job | Preservar | Próximo foco |
|---|---|---|
| Warrior | Individualidade careca/bestial, vermelho/ferro/couro, assimetria do ombro, Walk aprovado | Peso do soco; antecipação, contato e retorno; ferragens e rosto mais estáveis entre quadros |
| Squire | Roupa clara e proteção leve, leitura distinta do Warrior | Distinguir movimento legado de golpe e suplemento desarmado; validar a ação junto ao equipamento real |
| Archer | Corpo sem arco embutido, leitura de couro | Rotação grande durante a puxada deve ser revista junto ao arco, mão de apoio, corda, alvo e instante do disparo; não classificar a torção isolada como erro sem esse contexto |
| Apprentice Mage | Azul, bordas claras, identidade do indivíduo | Punhos e acabamento das bordas; selecionar conjuração e ataque físico por ação, sem converter Atacar em magia automaticamente |
| Acolyte | Manto verde curto e roupa clara | Separação de mãos/torso e recuperação do impacto; gesto e evento da ação precisam de evidência conjunta |
| Rogue | Capuz, paleta escura/furtiva já aprovada | Braços e torso podem perder separação sobre cenários escuros; avaliar no cenário antes de clarear roupa aprovada |
| Scout | Camadas de couro e verde | Continuidade de pequenos detalhes do cinto; distinguir alcance/retorno do gesto legado e soco |
| Brawler | Bandagens, peito livre e peso muscular | Linguagem do golpe back_l tem trajetória diferente do soco das outras vistas; conferir intenção e leitura, além da continuidade muscular no Hit |

Prioridade funcional: provar seleção por ação/equipamento, eventos, sockets, oclusão e arma independente. Prioridade artística: validar um piloto de combate antes de replicar alterações. Idle e Walk têm base aprovada aproveitável; não há evidência que justifique regenerar todo o acervo.

## O que foi produzido

### Conceito candidato separado

Pacote `characters/orc-01-refinement-v2/`, mesmo identityId do original, criado como estudo do mesmo equipamento. PNG real importado pelo CLI em `concepts/warrior-refinement-v2.png`. A ficha registra o objetivo, o reaproveitamento e o risco de variação de rosto/proporções pelo gerador.

Objetivo visual: clusters mais deliberados, separação de ferro/couro/tecido, rosto e mãos mais legíveis. O gerador também reinterpretou alguns volumes e ferragens: o resultado é uma **proposta**, não uma melhoria comprovada nem substituição aprovada. O conceito original 07 permanece a referência selecionada. Gate 1 do pacote novo continua pendente; não foram produzidos sprites de produção a partir desse novo conceito.

### Dois estudos de animação sobre o design original aprovado

Fontes: `characters/orc-01/source/aseprite/combat-refinement-v2/`.

- Attack front_r: cinco poses distintas, buscando leitura de antecipação → extensão do punho direito → desaceleração → retorno.
- Hit front_r: três poses distintas, buscando recuo → absorção → recuperação.
- Canvas 128×128 RGBA, chão 126, alfa binário, paleta de referência da base vigente.
- Duração total conservada: Attack 450 ms e Hit 240 ms. Distribuição candidata: Attack 80/110/50/90/120 ms; Hit 50/100/90 ms.
- Fontes `.aseprite`, PNGs nativos, APNGs, contatos e manifesto `editor.json`.
- Exportação Aseprite Steam em lote oculto: **2 clipes / 8 quadros / 8 comparações RGBA idênticas, PASS**. Build `dist/editor/orc-combat-refinement-v2/f734582a7ff6c1a68481/`.

Foram usadas três chamadas reais da ferramenta integrada `image_gen`, sem chave/API externa: um conceito e duas folhas de poses. O modelo não foi exposto pela ferramenta. As folhas são novos desenhos de poses; não são deformações do Hero nem redução do conceito para sprite. O processamento existente `extract-animation-sheet.py` separa corpos conectados, reconstrói a grade alvo explicitamente, aplica a paleta compartilhada e registra por translação inteira. Essa reconstrução tem perdas e não equivale a acabamento manual. O Attack tem caixas X sobrepostas entre duas figuras, mas os corpos estão separados; a extração por componentes foi liberada após inspeção visual e essa condição está registrada no clip.json.

Conferir especialmente: proporção da cabeça/tronco em relação à base, ferragens, botas plantadas e transições com Idle. Os estudos têm intenção de melhorar a leitura, porém não foram aprovados como substitutos. Só existem candidatos front_r; nenhuma outra vista ou roupa foi reescrita. A duração variável funciona no editor e no comparador; nenhum suporte correspondente no Unity foi implementado ou declarado.

## Como reproduzir a auditoria e visualizar

Na raiz da fábrica:

```powershell
node tools/audit-orc-assets-v2.mjs
tmp/pixel-venv/Scripts/python.exe tools/build-orc-audit-boards-v2.py
node tools/build-orc-audit-review-v2.mjs
node src/cli.mjs editor-export --manifest characters/orc-01/source/aseprite/combat-refinement-v2/editor.json
```

Abrir `reports/orc-audit-v2/review.html` no navegador. O comparador oferece pausa, quadro manual, meia velocidade e todos os Jobs/vistas vigentes. A reprodução de combate se repete para facilitar avaliação e não define o loop da ação no jogo.

`tools/package-orc-refinement-v2.py` reempacota somente os candidatos a partir dos PNGs já reconstruídos. Não gera nova arte, não aplica builds e não altera PNGs/reviews aprovados. Não executar scripts históricos de aprovação para reproduzir esta auditoria.

## Decisão e documentação após aprovação

Revisar separadamente: (1) fidelidade/qualidade do conceito; (2) poses Attack; (3) poses Hit; (4) ritmo proposto. Uma aprovação não deve ser inferida da aprovação de outra entrega.

Se o conceito for aprovado: registrar evidência no Gate 1 do novo pacote, criar/revisar primeira base nativa, depois quatro vistas e primeiro clipe. Se os movimentos forem aprovados sobre o design vigente: registrar evidência específica dos estudos, revisar as demais vistas e Jobs em lotes, sem promover timings incompatíveis ao runtime. Conservar fontes/hashes e versões antigas para reversão.

Só depois atualizar os direcionamentos canônicos da fábrica e do projeto principal. Os documentos temáticos correspondentes são `docs/VISUAL_IDENTITY.md`, `docs/WORKFLOW.md`, `docs/EQUIPMENT_AND_ACTIONS.md` e, no principal, `Docs/ART_DIRECTION.md`, `Docs/Art/CHARACTER_PIPELINE.md` e decisões de design pertinentes. Registrar apenas decisões efetivamente aprovadas e separar aprimoramento artístico de extensão funcional. Não generalizar este indivíduo como anatomia/paleta universal dos Orcs.

Nenhum novo direcionamento foi promovido a cânone nesta sessão. O projeto principal não foi alterado; não houve aplicação dos candidatos, autoaprovação ou integração Unity.

## Conferência de entrega

`orc-audit-review-check-v2.json`: Edge headless carregou os 896 PNGs, percorreu as 192 seleções de clipe e comparou os oito quadros candidatos do canvas com os PNGs nativos byte a byte em RGBA; zero erros JavaScript. Visualização local file:// e leitura exata via HTTP de loopback foram conferidas. O navegador restringe leitura de pixels de canvas no modo file://, mas exibe as imagens normalmente.

`orc-refinement-final-check-v2.json`: 1.151 arquivos protegidos conferidos sem alteração, build imutável dos candidatos íntegro, nenhum apply ou novo Gate aprovado. A prancha `orc-audit-v2/concepts-current.png` reúne os oito conceitos vigentes, também inspecionados. A conferência técnica não substitui a decisão artística do criador.
