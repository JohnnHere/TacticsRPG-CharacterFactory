> **HISTÓRICO REJEITADO / SUPERADO.** Ataques artisticamente rejeitados pelo criador. Idle/Walk armados e movimento comum Sword/Axe não são política atual. Consulte [resgate do Orc principal](MAIN_ORC_ONE_HANDED_RESCUE.md). Preservado como procedência e comparação, nunca como receita de produção.

# Orc V1 — revisão candidata de equipamento v2

2026-10-25. O lote v1 foi rejeitado pelo criador: ataques inconsistentes, arma sem pegada convincente, ruído de sombra na roupa, espada pequena e acabamento que parecia de outro jogo. A aprovação do corpo não se estende a esse lote. A v2 é uma revisão para avaliação, sem Gate artístico ou integração Unity.

## Direção visual

As armas pertencem à linguagem visual do jogo e serão compartilháveis entre raças e classes. Não precisam copiar a paleta, a ornamentação ou a cultura do Orc. A unidade vem de pixels/clusters, contorno, materiais, luz, contraste, escala e acabamento coerentes na câmera. O Orc foi uma referência de tratamento nesta experiência, não um uniforme obrigatório para equipamentos futuros. Regra permanente: `docs/WEAPON_ART_STANDARD.md`.

Os estudos Pro receberam uma amostra de cores do aço/couro atual para testar acabamento. Isso é um condicionamento deste experimento, não uma restrição universal. Foram escolhidos espada candidata0 e machado candidato1 entre quatro opções de cada. A espada tem lâmina mais longa e proporção total maior que a v1; o cabo recebeu acabamento de couro no Aseprite. Aço, guarda e pomo preservam o estudo Pro. A forma segue as fotografias fornecidas anteriormente: espada reta funcional e machado de um gume de milícia.

## Arquivos e revisão

Abra `Biblioteca de Arte/Personagens Jogaveis/Orc V1/index.html`. Cada arma inclui PNG separado, mestre Aseprite e **Idle armado / Walk / Attack**. A pasta `Biblioteca de Arte/Orcs Atuais/` continua contendo todos os conceitos e animações corporais atuais; o Infante original05 permanece ali para uma etapa mais avançada. Vigia e Matriarca continuam em Ideias Futuras como NPC e/ou jogável único.

| Clipe por arma | Quadros | Tempos |
|---|---:|---|
| Idle armado | 5 | 400/450/500/450/400 ms; 2200 ms, padrão fixo |
| Walk armado | 16 | 80 ms; ciclo1280 ms |
| Attack | 12 | 160/100/100/120/140/60/55/70/90/120/120/180 ms; 1315 ms |

As duas armas usam o mesmo corpo, ângulos, posições e tempos em cada estado. Attack não é um loop de gameplay; o preview o repete para revisão. Contato frame6 é candidato visual e não aplica dano.

- Armas: `assets/weapons/<id>/source/v2/` e `sprites/v2/`, 96×96. `weapon.json` aponta a candidata v2.
- Compósitos: `characters/orc-v1/source/equipment-v2/<id>/<Idle|Walk|Attack>/` com PNGs, camadas, folha e clip.json.
- Mestres: `characters/orc-v1/source/aseprite/equipment-v2/`.
- Corpo/pegada independentes: `source/equipment-v2/shared/` e mestres `body-idle`, `body-walk`, `body-attack`.
- Ponteiro candidato: `characters/orc-v1/source/equipment-current.json`; não é aprovação.
- Rig reutilizável: `experiments/orc-v1-weapons-v2/binding-rig.json`.
- Planejamento, pedidos e brutos: `experiments/orc-v1-weapons-v2/`.

## Como funciona a reutilização

O rig da família `onehanded-cut-v2` contém corpo independente da arma, grip da mão direita por quadro, orientação, relógio e oclusão. Cada item guarda apenas seu PNG/mestre, ponto de pegada local e contrato de compatibilidade. Para outra espada compatível: importar o asset no Aseprite, marcar seu grip no cabo e recompor usando esse rig; não gerar outro corpo ou outro golpe. A v2 demonstra a substituição com espada e machado compartilhando os mesmos dados de movimento.

Esta família é um corte genérico de uma mão deste corpo/vista. Não é promessa de animação universal para lanças, arcos, armas de duas mãos, outras anatomias ou todas as técnicas de espada/machado. Novos itens compatíveis reutilizam; outra família, anatomia ou vista pode exigir adaptação e validação próprias. Comprimento, espessura do cabo, guarda e cabeça precisam caber no contrato físico e no canvas, além de passar pela revisão visual.

Ordem real: **body → palmBack → weapon → fingersFront**. A palma fica atrás do cabo; quatro grupos de dedos e o polegar ficam à frente, com vincos e materiais da luva. As peças da mão são retoques autorais Lua executados no Aseprite; não são um recorte quadrado opaco da mão anterior. A orientação e a posição vêm do mesmo rig da arma, sem bindings separados por item. Os mestres mantêm tudo em camadas editáveis.

O novo ataque tem poses corporais controladas por esqueleto, com inspeção e correção dos grips após a geração, pois o modelo não obedece aos pontos de modo exato. O contorno da roupa inferior e as pernas são estabilizados com pixels aprovados no Aseprite, preservando a oclusão do braço. Idle e Walk reutilizam os corpos existentes. Não comprimir o tronco nem regenerar locomação para trocar equipamentos.

Composições256×256, corpo128×128 em(64,64), PPU100, chão190. Não houve redimensionamento do corpo ou trim dos PNGs. A espada separada está maior em pixels que a v1; não foi apenas ampliada no navegador. Novos itens maiores exigem revisão de margens.

## Procedência e custo real

PixelLab Pro confirmado pelo criador. Duas chamadas `create_image_pro`, quatro candidatos por arma,10 gerações cada; uma `animate_with_skeleton_v3`,12 poses,3 gerações. Estimativa auxiliar de esqueleto:0,1 geração. Total registrado deste experimento:23,1 gerações. A assinatura Pro não implica que todo método exponha um seletor Pro: o golpe usa Skeleton V3. Pedidos/seeds/recibos foram mantidos, sem credenciais versionadas. Não confundir isso com desenho manual ou IA interna do Aseprite.

Importação, acabamento do couro, estabilização da roupa, construção da pegada, composição, rotação por vizinho próximo e exportações aconteceram no Aseprite. Python/Node apenas organizam arquivos, validam pixels/metadados e apresentam a revisão. O custo de novas armas compatíveis não inclui regenerar o corpo; novas chamadas para desenhar o item continuam podendo consumir créditos.

## Preservação, reconstrução e limites

As fontes corporais aprovadas e o Infante original não foram substituídos. v1 preservada nos caminhos originais e em `experiments/orc-v1-weapons-v2/preserved-v1/`, incluindo uma cópia portátil da página anterior. Os caminhos v2 são novos; a biblioteca apresenta a revisão candidata.

1. `node tools/rebuild-orc-v1-weapons-v2.mjs` usa os resultados locais já baixados; não chama PixelLab. Autoria em `tools/aseprite/compose-orc-v1-weapons-v2.lua`.
2. `node src/cli.mjs editor-export --manifest experiments/orc-v1-weapons-v2/editor.json` compara os PNGs com seis mestres, timings e transparência.
3. `tmp/pixel-venv/Scripts/python.exe tools/build-orc-v1-weapons-v2-review.py` atualiza a página portátil.
4. `tmp/pixel-venv/Scripts/python.exe tools/check-orc-v1-weapons-v2.py` valida camadas, compartilhamento do rig, preservação e preview.

É uma vista front_r/south-east. Runtime de overlays, equipamento, pivôs, eventos de dano, transições e outras vistas ainda precisa de implementação e teste no pedido futuro de integração. Nenhum arquivo Unity foi alterado. Exportação e testes técnicos não concedem aprovação artística: pegada, material, peso e naturalidade continuam sujeitos à avaliação do criador.
