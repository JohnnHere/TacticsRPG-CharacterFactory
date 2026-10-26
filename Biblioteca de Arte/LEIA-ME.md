# Biblioteca de Arte

Abra **index.html** para comparar os Orcs atuais, com conceito, Idle e Walk juntos. Os links no topo levam diretamente a cada personagem.

## Padrão de Idle aprovado — 2026-10-25

PADRÃO FIXO OBRIGATÓRIO na criação de personagens: mesmo Idle normal do meio-termo aprovado, cinco fases 400/450/500/450/400 ms, ciclo 2,2 s e amplitude equivalente a 2 px na cabeça de humanoide 128×128. Não variar o padrão por personagem, Job, roupa ou personalidade. Ajustar somente o encaixe à anatomia/escala, mantendo a mesma cadência e sutileza. Qualquer exceção exige autorização explícita do criador. Diretriz completa em **PADRAO-DE-IDLE.md**. O Infante já exibe a versão aprovada; demais personagens não foram alterados automaticamente.

## Pendência artística — 2026-10-25

Precisamos trabalhar melhor a armadura do **Orc Ágil (Veterano Ágil, 04)** antes de fechar sua versão de produção. A pendência também aparece na ficha visual e em PENDENCIAS.md do personagem. Notas persistentes em docs/ART_LIBRARY_NOTES.json, preservadas ao reconstruir a biblioteca.

## Pastas

- **Orcs Atuais/**: inclui o **Orc V1**, pele Verde Warcraft selecionada para futura integração, e os demais candidatos.
- **Infante de Ferro original**: permanece em **Orcs Atuais/**, com conceito, Idle, Walk e mestres, destinado a uma etapa mais avançada do jogo. **Orc V1** continua como primeiro jogável selecionado.
- **Arquivo de Arte/**: reservado a históricos; não é a categoria atual do Infante de Ferro.
- **Personagens Jogaveis/Orc V1/**: armas separadas e estudos equipados de golpe e caminhada; prévias locais, sem integração Unity.
- **Conceito/**: PNG do conceito.
- **Idle/Quadros/** e **Walk/Quadros/**: PNGs nativos em ordem. O clip.json da ação registra os tempos reais.
- **Mestres Aseprite/**: arquivos editáveis de Conceito, Idle e Walk.
- **Estudos Comparativos/**: versões alternativas lado a lado; inclui os três Idles do Infante de Ferro e **Infante de Ferro - Pele Verde/** (original × pele verde, conceito e Idle), com mestres e quadros por versão. Candidatos não substituem a seleção atual automaticamente.
- **Ideias Futuras/**: Vigia do Passo e Matriarca, separados como ideias de NPC e/ou jogáveis exclusivos/únicos. Somente conceito nesta etapa.
- **Historico de Entregas/**: criada nas atualizações quando uma cópia anterior precisa ser preservada.

Cada personagem tem seu próprio **index.html** e **ORIGEM.json**. Esta é uma cópia de consulta/entrega, autossuficiente para abrir os PNGs, mestres e páginas sem Internet. Fontes canônicas da pipeline continuam em characters/ e ideas/unique-characters-or-npcs/, identificadas em ORIGEM.json e catalogo.json. Para continuar a produção, editar a fonte canônica por fork e reconstruir a biblioteca.

Atualizar após exportar/salvar no Aseprite:

`tmp/pixel-venv/Scripts/python.exe tools/build-art-library.py`

O construtor confere hashes, preserva versões anteriores e interrompe se detectar uma cópia de arte editada diretamente nesta biblioteca, para não sobrescrever seu trabalho. Não há integração ou alteração no jogo. V4 e Reimaginado descartados não são opções atuais. A limpeza dos pés do Atlético foi feita localmente no Aseprite, preservando as oito poses e os tempos.
