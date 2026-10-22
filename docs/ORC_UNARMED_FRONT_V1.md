# Orc — primeiro lote de ataque basico desarmado

Em2026-10-19, apos feedback positivo sobre o conjunto anterior, o criador pediu verificar documentacao de equipamentos nos dois repositorios, criar padrao ausente e considerar o ataque normal sem arma em todos os personagens. O feedback nao foi registrado como Gate consistency final; houve ampliacao do inventario de acoes a verificar.

Auditoria executada em17 arquivos atuais do jogo e cinco contratos locais, com SHA256 em reports/equipment-source-audit-v1.json. GAMEPLAY.md/ROADMAP.md atuais divergem dos snapshots; as decisoes visuais de arma separada, UnitVisuals e UnitView conferidos continuam compativeis com a regra descrita. Snapshots congelados preservados. O jogo foi apenas lido, nenhuma escrita Unity.

O contrato faltante foi criado em [EQUIPMENT_AND_ACTIONS.md](EQUIPMENT_AND_ACTIONS.md) e config/equipment-actions-v1.json: Atacar depende da arma real; desarmado usa golpe fisico, habilidades de magia/suporte nao substituem esse comando. A ausencia de arma no desenho nao prova tipo de acao. Sockets anatomicos, partes/mascaras, ordem de oclusao por quadro, SHA do corpo/arma e eventos visuais sao exigidos para provar encaixe. Nao ha sockets inventados nem binding pronto. src/action-contract.mjs valida a selecao OFFLINE, sem alterar Core/Presentation do jogo; tres testes novos previnem fallback por Job, arma desconhecida e magia indevida no ataque basico. npm test:9/9 PASS.

Reuso demonstrado: o Attack original do Warrior foi inspecionado nas quatro vistas, incluindo a fonte corrected-v2 de back_l, e ja representa golpe fisico de punho. Ele e o Brawler reutilizam seus20 quadros cada por caminho/hash, sem copias ou alteracoes. As seis outras roupas precisam de unarmed separado; Archer nao pode puxar arco sem arma, Mage/Acolyte nao podem conjurar no lugar do soco.

Primeiro lote:30 PNGs novos e seis .aseprite, cinco poses front_r por roupa. Guarda, preparacao, soco, continuacao e retorno;90ms/quadro, acao unica. Pixel Art Fixer recupera a grade dos cinco desenhos reais, paleta da propria roupa, canvas128 RGBA8,ground126,alpha binario; nao ha deformacao de base estatica. As fontes raster nao fingem corpo/roupa em camadas.

Nove chamadas reais image_gen retornaram PNGs:sete primeiras folhas e duas correcoes de assimetria Warrior/Squire. A comparacao com a arte original mostrou que o Warrior deve reutilizar os clipes ja aprovados; suas duas novas tentativas nao foram selecionadas. A primeira Squire tambem nao foi selecionada por troca de ombreira. Squire ativo usa source/action-clips-v2 e actions/basic-unarmed/v2; as outras cinco roupas novas usam v1. Todas as tentativas, prompts exatos, referencias e hashes permanecem nas fontes, com modelo nao exposto pela ferramenta. A selecao ativa e somente characters/orc-equipment-actions-v1.json.

Validacao independente: tools/verify-orc-unarmed-front-v1.mjs verifica origens/prompts/referencias/processamento, paleta, RGBA, hashes e roundtrip real LibreSprite. Trinta novos quadros e duracoes do editor identicos; os PNGs/editaveis do conjunto anterior e do Warrior permanecem intactos. Preview com40 referencias de quadro (30 novos+10 reutilizados) em [review-orc-unarmed-front-v1.html](../characters/review-orc-unarmed-front-v1.html). Edge/Playwright:40/40 hashes RGBA de canvas exatos, HTTP e file:// carregados, oito filtros, zoom/velocidade/scrub/repeticao/ultimo quadro verificados, zero erros JavaScript; servidor local encerrado. Evidencias em characters/orc-unarmed-front-browser-v1.json e captura correspondente.

Matriz atual:32 clipes direcionais unarmed necessarios para os oito Orcs,14 com fonte nativa existente (Warrior4+Brawler4+seis front_r),18 faltantes =90 quadros. Prontidao artistica separada: seis novos front_r aguardam criador; reuso de fontes antigas nao autoaprova as novas. Readiness nao equivale a export ou suporte em jogo.

Proximo marco: revisar este primeiro lote front_r antes de produzir front_l/back_r/back_l nas seis roupas, conforme AGENTS.md e WORKFLOW.md. Pergunta enviada com a previa concreta. Depois revisar consistencia do suplemento e conjunto completo antes de exportar os pacotes. Exportador legado nao inclui actions/; extensao de exportacao validada permanece pendente. Armas/efeitos e gameplay desarmado ainda requerem implementacao propria; parametros Core de dano/alcance/acerto nao foram inventados.

Comandos de retomada:

```powershell
node tools/check-equipment-readiness.mjs
node tools/verify-orc-unarmed-front-v1.mjs
node tools/build-orc-unarmed-front-review.mjs
& 'tmp/pixel-venv/Scripts/python.exe' tools/check-orc-unarmed-front-preview.py
```

Nao reexecutar preparadores/seletores historicos: eles descrevem tentativas anteriores e podem substituir a selecao ativa. Os97 PNGs legados por personagem continuam no lugar;30 PNGs suplementares ativos sao inventario adicional, nao novos slots do loader atual.

## Atualizacao apos aprovacao do primeiro lote

O criador aprovou: "Aprovo os ataques desarmados; continue as outras vistas." O estado de30 quadros/90 faltantes acima e historico. As tres vistas foram produzidas;32/32 clipes unarmed estao completos, com120 PNGs novos e40 reutilizados,24 editaveis novos. Previa final conjunta em characters/review-orc-actions-complete-v1.html. Detalhes e retomada vigentes em [ORC_UNARMED_DIRECTIONS_V1.md](ORC_UNARMED_DIRECTIONS_V1.md); consistencia final/exportacao ainda pendentes.
