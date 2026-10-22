# Entrega inicial — 2026-10-18

Repositorio independente em TacticsRPG-CharacterFactory, ao lado do jogo. Git inicializado localmente, sem remoto, publicacao ou commit automatico. Os arquivos do TacticsRPG foram somente lidos e copiados. O projeto de origem ja tinha alteracoes em andamento; sourceWasDirty=true esta no manifesto.

## Material reunido

240 arquivos no snapshot de referencias: documentacao relevante de arte/design, skill character-art-design com referencias, 97 PNGs do piloto e seus metas, codigo/testes de direcao e animacao como evidencia. Catalogos extraidos: 28 racas, 63 Jobs. Painel visual references/index.html e preview do Hero em characters/hero-reference/preview.html. A ancora e referencia de linguagem global aprovada conforme ART_DIRECTION; o Hero tem status reference_only e mantem suas pendencias historicas.

Quatro fichas de demonstracao: hero-reference, orc-01 (Warrior), orc-01-archer (mesmo identityId do Orc) e undead-01 (Archer). Orc/Undead ainda sem imagens de conceito ou sprites produzidos. Nenhuma receita de raca/Job foi promovida a approved. Nenhuma aprovacao humana ficticia foi registrada nesses exemplos.

## Verificacao automatizada

Node v24.20.0 nesta maquina. npm install --ignore-scripts instalou pngjs 7.0.0 e gerou lockfile; npm reportou zero vulnerabilidades naquela execucao. Doctor verificou os hashes das 240 referencias sem divergencia.

`npm test`: seis testes locais, incluindo fluxo de integracao por CLI com arquivos sinteticos temporarios. Cobre confinamento de caminhos e symlinks, alpha/source-over e ordem de camadas, canvas/chao, PNG invalido, catalogos, criacao de ficha/roupa com identidade compartilhada, gates, exportacao de 97 slots, rejeicao mais recente, revisao invalidada por alteracao de pixels, composicao com proveniencia e arquivo de receitas/imagens imutaveis. As aprovacoes em testes se referem apenas a fixtures sinteticas excluidas ao terminar; nao aprovam arte real.

Preview PNG do Hero inspecionado visualmente durante a entrega. A folha de contato e derivada para revisao; nao e novo sprite nem modifica originais. O HTML local inclui todos os PNGs e rotulos de arquivo; nao foi feito teste automatizado em navegador.

## Resultado tecnico do piloto existente

`validate --id hero-reference --stage full`: 455 PASS, 34 FAIL, 48 WARNING, 1 NOT_RUN e 1 REQUIRES_HUMAN_REVIEW. Os 34 FAIL sao linha do chao diferente do y=126 especificado, incluindo pixels parcialmente transparentes no calculo de bounds. Inspecionar por arquivo em characters/hero-reference/reports/validation.json; essa medicao nao identifica qual pixel e o pe anatomico. Os PNGs copiados foram mantidos sem retoque. Isso nao e falha dos testes da ferramenta: e um resultado honesto sobre os assets historicos.

Importador C# exportado, compilacao Unity e PlayMode: NOT_RUN. O jogo nao foi aberto ou alterado. Novo personagem requer registro em UnitVisuals e revisao de compatibilidade. Gate 3 continua pendente.

## Proximo uso real

Abrir AGENTS.md no contexto do agente e pedir o conceito do orc-01, usando handoff/prompt.md e imagens listadas. Depois da aprovacao real, produzir a base nativa, revisar quatro vistas e seguir animacoes por lotes. Documentar a primeira receita de Archer aprovada para que um Undead Archer futuro preserve a linguagem do Job.
