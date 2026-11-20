# Padrão de arte — armas independentes

Decisão vigente do criador em 2026-10-25: Espada do Recruta e Machado de Milícia são assets separados de uma mão, **visíveis somente no intervalo do ataque**. Idle, Walk, repouso, inspeção, Hit/Defeat e após a ação ficam sem armas. A antiga apresentação armada v1/v2 está superada. Guia atual: [Orc principal — resgate dos ataques](MAIN_ORC_ONE_HANDED_RESCUE.md).

Armas seguem a linguagem visual do jogo: pixel art detalhada, contornos controlados, clusters deliberados, luz coerente, materiais legíveis e contraste compatível com a câmera. Não reduzir a arma a uma forma genérica nem inflar detalhes/ornamentos fora do nível do item. Não há obrigação de copiar paleta, cultura ou design Orc; os itens servirão a várias raças/classes.

## Primeiro lote e referências

### Linguagem do jogo, não uniforme do Orc — esclarecimento do criador, 2026-10-25

Armas são equipamentos do jogo, reutilizáveis entre classes e raças. Não precisam reproduzir a paleta, os adornos, a cultura ou o design da armadura do Orc. Podem ter outras cores, materiais e origens culturais. A coerência exigida é de linguagem visual: escala de pixels, tratamento dos contornos, construção de clusters, luz, contraste e nível de acabamento compatíveis com os personagens e com a câmera do jogo. A referência do Orc serve para comparar esse tratamento; não o transforma em padrão obrigatório de todos os itens. Uma arma deve parecer do mesmo jogo mesmo quando não foi feita culturalmente para aquele personagem.

Reutilização tem dois contratos independentes: identidade visual global do item; e compatibilidade física da empunhadura/movimento com a anatomia do portador. A família de movimento define corpo, tempos, sockets, orientação e oclusão da mão. Trocar por outra espada compatível reutiliza esse movimento, substituindo somente o asset e seu ponto local de pegada. Novas anatomias precisam de bindings próprios; famílias diferentes podem exigir movimentos próprios. Não gerar novamente o corpo a cada modelo de arma.

Os lotes v1 e v2 foram rejeitados pelo criador. Seus testes técnicos não comprovam qualidade artística. Os estudos Pro v2 receberam cores do equipamento atual como experimento de acabamento, não como regra de paleta universal. Armas atuais partem dessas fontes por revisão segura no Aseprite; não repetir o corpo estático com rotação360° ou a palma/dedos genéricos da v2.

- **Espada do Recruta / recruit-sword / Sword**: referência fotográfica enviada pelo criador; lâmina reta de dois gumes com canal central, guarda reta simples, empunhadura de couro castanho costurada e pomo disco. Aço funcional com desgaste contido, sem gemas/magia.
- **Machado de Milícia / militia-axe / Axe**: referência fotográfica enviada pelo criador; cabeça de ferro de um gume, fio curvo, barba curta e olhal/rebite; cabo de madeira curvo com textura e desgaste. Ferramenta/arma de milícia, não machado fantasioso de duas mãos.
- Uma mão para cada arma, direita anatômica neste lote; esquerda livre. As imagens foram observadas na conversa, não foi inventado um arquivo local de fotografia. Não concedem IDs/stats/economia ao Core: são assets visuais de categorias Sword/Axe existentes.

## Produção e fontes

**Revisão vigente:** resgate `main-orc-onehanded-v3`, sem relação com o antigo design Orc V4. O personagem é o Orc principal `orc-v1`. Fontes v1/v2 de equipamento são históricas rejeitadas. Guia e relações de mestres em `docs/MAIN_ORC_ONE_HANDED_RESCUE.md`.

Mestre .aseprite obrigatório. Armas herdam a arte PixelLab Pro v2, com correções de proporção por peças no Aseprite/Lua; não são novas gerações nem desenho manual. Poses podem usar PixelLab autorizado, com retoques, limpeza, timing, oclusão e exportação no Aseprite. PNGs são derivados. O corpo continua independente da arma; composições equipadas são derivados revisáveis.

Assets em assets/weapons/<id>/, com source/rescue-v3/, sprites/rescue-v3/ e weapon.json. Este lote: canvas96×96, PPU100, grip espada(48,66) e machado(36,55). Canvas não é tamanho visível: conteúdo espada72px e machado47px de altura, comparados ao Orc121px. Novos itens declaram dimensões e pegada próprias; não impor96×96 a todas as armas. Mudar personagem, escala ou mão exige revisar bindings por vista/corpo/ação.

## Visibilidade somente durante a ação

Política `attack-only-v1`: nenhum Idle/Walk armado, nenhuma arma carregada/embainhada ou animação de sacar. O equipamento aparece já em pegada de ataque, acompanha a mão em um intervalo contínuo e desaparece ao final; o corpo retorna ao Idle sem arma. O mestre corporal e o Idle fixo aprovado permanecem independentes. O preview deve demonstrar Idle → Attack → Idle com os PNGs reais, além de Walk sem arma.

## Encaixe e qualidade

Registrar por quadro: hash do corpo/arma/partes, mão anatômica, grip inteiro, orientação, profundidade e visibilidade. Ordem weaponBack → body → weaponFront → handFront. Dedos/polegar da própria pose envolvem o cabo, com conexão natural ao punho e antebraço; não basta coincidir âncoras. Revisar corpo inteiro e pegada ampliada, sem luva genérica girada com o item.

O corpo conduz o golpe: quadril, tronco, ombro, cotovelo e punho participam. Espada tem corte controlado e rápido; machado tem preparação/seguimento mais pesados. São perfis separados, reutilizados entre modelos compatíveis da **mesma categoria**, com ponto local de pegada por item. Não gerar animação corporal por nova espada ou forçar um movimento universal para todas as armas. Não criar IK/runtime genérico para resolver este lote.

No primeiro lote, composições 256×256 contêm o corpo 128×128 em offset (64,64), sem escala e sem recorte de arma. PPU100, referência de chão 190. Cada camada, quadro e folha usa o mesmo registro. Esse perfil é uma extensão de assets: não declarar que o pivô/loader Unity de 128 já o suporta. Não fazer trim/rescale automático.

Golpe deve ter preparação, passagem, seguimento e recuperação. A página repete o golpe para revisão, mas o clipe Attack é não repetitivo no gameplay. Marcação de contato é candidata visual, não aplicação de dano. Preservar o padrão fixo de Idle em config/idle-art-standard-v1.json; armas não autorizam outro ritmo de repouso.

## Entrega e integração

Orc principal e fontes atuais em docs/MAIN_ORC_ONE_HANDED_RESCUE.md. ORC_V1_WEAPONS.md e ORC_V1_WEAPONS_V2.md são históricos rejeitados. Escopo: front_r/south-east; não há quatro vistas aprovadas. Runtime de equipamento/eventos/pivôs/transições precisa de implementação/verificação futura. Não alterar Core, stats, saves ou Unity. Aprovação do personagem não aprova automaticamente armas ou novos golpes; só propagar após revisão explícita do criador.
