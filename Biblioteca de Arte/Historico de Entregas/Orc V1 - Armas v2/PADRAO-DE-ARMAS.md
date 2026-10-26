# Padrão de arte — armas independentes

Decisão do criador em 2026-10-25: iniciar Espada do Recruta e Machado de Milícia, ambas de uma mão, com assets separados, golpe composto e caminhada completa com a arma na mão. Armas seguem a mesma identidade visual dos personagens: pixel art detalhada, contornos controlados, clusters deliberados, luz coerente, materiais legíveis e contraste compatível com a câmera. Não reduzir a arma a uma forma genérica nem inflar detalhes/ornamentos fora do nível do item.

## Primeiro lote e referências

### Linguagem do jogo, não uniforme do Orc — esclarecimento do criador, 2026-10-25

Armas são equipamentos do jogo, reutilizáveis entre classes e raças. Não precisam reproduzir a paleta, os adornos, a cultura ou o design da armadura do Orc. Podem ter outras cores, materiais e origens culturais. A coerência exigida é de linguagem visual: escala de pixels, tratamento dos contornos, construção de clusters, luz, contraste e nível de acabamento compatíveis com os personagens e com a câmera do jogo. A referência do Orc serve para comparar esse tratamento; não o transforma em padrão obrigatório de todos os itens. Uma arma deve parecer do mesmo jogo mesmo quando não foi feita culturalmente para aquele personagem.

Reutilização tem dois contratos independentes: identidade visual global do item; e compatibilidade física da empunhadura/movimento com a anatomia do portador. A família de movimento define corpo, tempos, sockets, orientação e oclusão da mão. Trocar por outra espada compatível reutiliza esse movimento, substituindo somente o asset e seu ponto local de pegada. Novas anatomias precisam de bindings próprios; famílias diferentes podem exigir movimentos próprios. Não gerar novamente o corpo a cada modelo de arma.

O lote v1 foi rejeitado pelo criador: falta de unidade visual, espada pequena, mãos sem pegada convincente, ataques inconsistentes e ruído de sombra na roupa. Seus testes técnicos não comprovam qualidade artística. O lote v2 está em estudo; não há aprovação automática. Os primeiros estudos Pro v2 receberam cores do equipamento atual como experimento de acabamento, não como regra de paleta universal; avaliar os candidatos à luz deste esclarecimento antes de selecioná-los.

- **Espada do Recruta / recruit-sword / Sword**: referência fotográfica enviada pelo criador; lâmina reta de dois gumes com canal central, guarda reta simples, empunhadura de couro castanho costurada e pomo disco. Aço funcional com desgaste contido, sem gemas/magia.
- **Machado de Milícia / militia-axe / Axe**: referência fotográfica enviada pelo criador; cabeça de ferro de um gume, fio curvo, barba curta e olhal/rebite; cabo de madeira curvo com textura e desgaste. Ferramenta/arma de milícia, não machado fantasioso de duas mãos.
- Uma mão para cada arma, direita anatômica neste lote; esquerda livre. As imagens foram observadas na conversa, não foi inventado um arquivo local de fotografia. Não concedem IDs/stats/economia ao Core: são assets visuais de categorias Sword/Axe existentes.

## Produção e fontes

**Revisão vigente:** v1 abaixo é procedência histórica rejeitada. A candidata atual usa PixelLab Pro para a arte das armas, com importação/acabamento e composição em Aseprite, canvas96×96 e família corporal compartilhada. Guia e limites em `docs/ORC_V1_WEAPONS_V2.md`. Não reproduzir automaticamente o desenho Lua simplificado v1 nem seus bindings/tempos por item.

Mestre .aseprite obrigatório. Produção nova das duas armas é Lua autoral no Aseprite, não desenho manual ou geração PixelLab. PNGs são derivados. Reutilizar material/movimento compatível e registrar adaptação. O corpo continua independente da arma; as composições equipadas são derivados revisáveis. Não embutir permanentemente uma espada/machado no conceito ou corpo mestre.

Assets em assets/weapons/<id>/: source/<id>.aseprite, sprites/<id>.png e weapon.json. Canvas nativo 64×64, PPU100, grip da espada (32,50) e do machado (32,49). Mudar personagem, escala ou mão não comprova encaixe: criar/revisar bindings próprios por vista, corpo e ação.

## Caminhada armada autorizada

Este pedido substitui a restrição histórica de arma oculta no Walk **para o Orc V1 equipado com estas duas armas**: elas são mostradas durante o ciclo completo solicitado. O corpo sem equipamento e o Idle padrão continuam preservados. Não generalizar visibilidade para armas/estados não especificados sem design explícito; futuramente o renderer deve selecionar pelo equipamento e ação reais.

## Encaixe e qualidade

Registrar por quadro: hash do corpo, arma e partes, mão anatômica, grip inteiro, ângulo e profundidade. Ordem weaponBack → body → weaponFront → handFront. Dedos/gauntlet passam à frente do cabo na região de pegada; não basta posicionar a arma perto da caixa do personagem. Revisar corpo inteiro, empunhadura ampliada, arma visível em todos os quadros de Walk e fechamento do loop.

No primeiro lote, composições 256×256 contêm o corpo 128×128 em offset (64,64), sem escala e sem recorte de arma. PPU100, referência de chão 190. Cada camada, quadro e folha usa o mesmo registro. Esse perfil é uma extensão de assets: não declarar que o pivô/loader Unity de 128 já o suporta. Não fazer trim/rescale automático.

Golpe deve ter preparação, passagem, seguimento e recuperação. A página repete o golpe para revisão, mas o clipe Attack é não repetitivo no gameplay. Marcação de contato é candidata visual, não aplicação de dano. Preservar o padrão fixo de Idle em config/idle-art-standard-v1.json; armas não autorizam outro ritmo de repouso.

## Entrega e integração

Orc V1 e suas armas em docs/ORC_V1_WEAPONS.md. Vista atual única front_r/south-east: não são quatro vistas aprovadas. Runtime de equipamento, eventos, pivôs e transições ainda precisam de implementação/verificação no pedido futuro de integração. Não alterar Core, stats, saves ou o jogo nesta produção local. A seleção do personagem verde não aprova automaticamente as armas e os novos golpes.
