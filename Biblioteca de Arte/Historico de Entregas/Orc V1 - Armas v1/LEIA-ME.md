# Orc V1 — Espada do Recruta e Machado de Milícia

Abra index.html para conceito, Idle padrão e duas armas separadas com caminhada e golpe. Cada arma usa uma mão, a direita anatômica. As duas fotos enviadas pelo criador orientam forma e materiais; o acabamento segue a pixel art do personagem, sem equipamento mágico ou ornamental de alto nível.

Armas/<nome>/ contém PNG e mestre Aseprite independentes em 64×64. Walk/ e Attack/ contêm mestres com camadas, Quadros/, Camadas/, folha completa native-strip.png e clip.json com tempos, encaixes e procedência. Cada composição tem weaponBack, body, weaponFront e handFront. PNGs de composição: 256×256 com o corpo nativo 128×128 deslocado (64,64), PPU100, sem redimensionar a arte. A margem acomoda a arma e seu arco sem cortar pixels. O futuro importador deverá respeitar esse registro, não usar o pivô 128 antigo automaticamente.

Walk: 16 quadros de 80 ms, loop de 1280 ms. Golpe da espada: nove quadros, 1025 ms. Golpe do machado: nove quadros, 1285 ms. As animações de golpe são não repetitivas em gameplay; a página repete para revisão. Evento de contato no clip é marcação visual candidata, não aplica dano no Core.

Fonte canônica: characters/orc-v1/ e assets/weapons/. A origem e SHA256 de cada cópia ficam em catalogo.json. Corpo de ataque herdado de geração PixelLab MCP, adaptação e armas autorais Lua no Aseprite; nada é descrito como desenho manual. Uma geração de espada sem golpe claro foi descartada; o corte corporal mais legível foi reutilizado para as duas armas, com arcos e cadências próprios e limpeza de uma lâmina curta indevida gerada pelo modelo. As caminhadas reaproveitam as 16 poses do Infante e a paleta verde selecionada.

Escopo: estudos de uma vista front_r/south-east, não pacote de quatro direções pronto no runtime. Encaixes e dedos foram revisados na composição, mas a aprovação artística das novas armas/golpes é do criador. Nenhum código ou asset do jogo Unity foi alterado. O Infante original permanece em Orcs Atuais/, previsto para um estágio mais avançado, e as variantes de pele continuam em Estudos Comparativos/.

Atualizar esta página com tools/build-orc-v1-weapons-review.py. Camadas e sprites devem sempre vir dos mestres salvos/exportados no Aseprite.
