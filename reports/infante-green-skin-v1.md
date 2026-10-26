# Infante de Ferro — estudo de pele verde

2026-10-25. Pedido do criador: preservar tudo que existe e mostrar o mesmo Infante com pele mais esverdeada, aproximadamente na paleta dos Orcs de Warcraft. Variante local do mesmo indivíduo 05; não novo personagem, sem seleção automática.

## Autoria e preservação

Fork via editor-fork de conceito e Idle aprovados. Mestres novos em `characters/orc-pixellab-05/source/aseprite/green-skin-v1/source/green-concept.aseprite` e `green-idle.aseprite`. Lua `tools/aseprite/infante-green-skin-v1.lua` aplica no Aseprite uma rampa verde-folha/oliva com sombras verde-escuras e luzes quentes, somente nas linhas de pele selecionadas manualmente na cabeça. Presas, pontos claros dos olhos, cicatrizes quentes, contorno, armadura e transparência preservados conforme a máscara registrada. Original PixelLab herdado e retoques prévios mantêm sua procedência; não é geração nova nem desenho manual. Zero chamadas/cobranças novas de PixelLab.

A paleta é uma interpretação inspirada nos verdes clássicos de Warcraft, não amostragem de uma imagem oficial específica. A comparação mantém a armadura idêntica e não copia identidade de personagem da franquia.

O Idle verde tem as mesmas cinco poses, 400/450/500/450/400 ms e ciclo 2200 ms do padrão fixo aprovado. Não houve alteração de forma, movimento, detalhes ou duração; só troca seletiva de cores. A aprovação herdada cobre o movimento, não esta nova paleta. Walk, seleção atual e toda a arte original ficaram intactos.

## Entrega e revisão

PNG e clip variante em `source/studies/PaletteVariants/green-skin-v1/`, com variant.json. Comparação portátil com conceito e Idle original/verde em `Biblioteca de Arte/Estudos Comparativos/Infante de Ferro - Pele Verde/index.html`, link no índice principal. Cada versão inclui conceito, Idle e mestres separados. Atualizar com `tools/build-infante-green-review.py` e depois `tools/build-art-library.py`.

Exportação Aseprite PASS: seis quadros comparados, build `dist/editor/infante-green-skin-v1/20eca81a9328001d3cae/`. Registro por pixel em `experiments/infante-green-skin-v1/retouch.json`; `reports/infante-green-skin-v1/check.json` comprova apenas alterações de cor listadas e preservação de alpha/silhueta/originais. Viewer PASS: dez quadros, 16 hashes de cópias, mesmo ciclo nas duas versões, abertura local, mobile e zero erros JavaScript; `viewer-check.json`. Biblioteca principal também passou com os oito Orcs atuais.

Variante aguarda avaliação do criador. Não substitui original ou muda padrão global de pele dos Orcs; nenhuma integração Unity, arma ou migração dos demais personagens.
