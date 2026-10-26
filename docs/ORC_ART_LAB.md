# Laboratório visual Orc — direção do criador

**Decisão vigente — 2026-10-24:** V4 ativa e V4 Reimaginado descartados pelo criador; não reutilizar como direção selecionada nem reativar pelos scripts históricos. Arquivos preservados como histórico. Nenhuma seleção de produção ativa. Novo candidato `orc-pixellab-11` (Orc Atlético): parecido com o Ágil, menos armadura, mais musculatura e verde um pouco mais claro. Revisão corrente: `reports/orc-current-review/review.html`. Vigia e Matriarca ficam separados em `ideas/unique-characters-or-npcs/` como ideias futuras de NPC e/ou jogáveis únicos. Esta decisão substitui afirmações históricas de V4 selecionada abaixo.

**Atualização posterior do mesmo dia:** o criador pediu [PixelLab + Aseprite](PIXELLAB_ASEPRITE.md), com três Orcs novos Tolkien/Warcraft e estudos de animação, sem consultar ou usar a V4 e suas artes como referência. O estudo V5 abaixo é histórico da exploração anterior; não deve ser entrada ou condicionamento do novo lote. A escolha entre suas cinco opções deixou de ser o próximo passo imediato.

Decisão expressa em 2026-10-23. O alvo é um **Orc clássico de fantasia medieval, inspirado principalmente em World of Warcraft e também em Tolkien**, dentro da leitura tática e da pixel art refinada do TacticsRPG. Essa hipótese já existia nas referências; o criador a reafirmou. Warcraft orienta presença, anatomia robusta, armaduras e força das formas; Tolkien orienta atmosfera e credibilidade medieval. Designs, símbolos e cultura desenvolvidos para o jogo são próprios.

O criador quer um jogo com alma e deseja fugir de uma aparência genérica de IA. Cabe ao agente assumir a direção de paleta, textura, materiais e luz, apresentar escolhas visuais concretas e explicar suas diferenças. Não exigir que o criador escolha esses parâmetros técnicos antes de ver propostas. Ferramenta ou procedência, por si só, não comprovam identidade ou qualidade artística.

## Como explorar e aprovar

Usar o Orc Warrior como laboratório: entregar **cinco propostas visuais comparáveis**, o criador escolhe uma base e então agente e criador a refinam. As opções devem trazer diferenças de construção de armadura, massas, motivos e acabamento, além de cor. Nomes de estudo não criam clãs, facções, habilidades ou lore canônico. Preservar a identidade reconhecível do Orc aprovado ao explorar sua apresentação.

Toda autoria e todo retoque acontecem no Aseprite; `.aseprite` é mestre. Reutilizar a arte aprovada quando compatível, documentando a procedência herdada e as intervenções novas. Lua no Aseprite é autoria programática e deve ser identificada. Abrir ou retocar arte legada não muda sua origem. Previews externos apenas apresentam os PNGs exportados, sem produzir arte.

Critérios de revisão: presença de Orc clássico; leitura de Warrior sem armas; rosto expressivo e anatomia robusta; hierarquia clara de formas e valores; materiais distinguíveis com brilho controlado; detalhes com propósito; coerência com a âncora global. Não impor uma contagem de cores ou nível de simplificação como solução universal. Comparar conceito em tamanho integral e reduzido; conceito reduzido continua sendo conceito, nunca sprite de produção.

Após a escolha explícita, refinar o conceito escolhido e registrar Gate 1 antes de produzir a nova base nativa. Revisar base e vistas, depois os primeiros clipes, antes de escalar. Consolidar regras aprovadas em receita e documentação; adaptar as demais roupas Orc por compatibilidade. As cinco alternativas são candidatas, não cinco aprovações. A V4 ativa permanece referência de produção até decisão explícita de substituição. A exploração não concede Gate em jogo nem autoriza integração Unity.

## Entrega para escolha

| Opção | Direção visual candidata |
|---|---|
| 01 — Ferro do Clã | Ombreira assimétrica com cristas, ferro frio, vermelho queimado e marca bifurcada. |
| 02 — Veterano da Fronteira | Lâminas baixas, malha localizada, reparos e tecido musgo; atmosfera medieval mais sóbria. |
| 03 — Bastião de Basalto | Placas largas angulares, aço frio, tecido ardósia e inserto verde sem emissão. |
| 04 — Campeão do Ocre | Bronze, pequenas lâminas no peito, tecido cru e pintura facial clara. |
| 05 — Ferro de Campanha | Ferro oxidado, placas de reparo, rebites e tecido azul apagado. |

São cinco direções sobre o mesmo rosto, corpo e pose aprovados, com novas construções de armadura e tratamento de materiais. A anatomia/desenho herdados mantêm sua procedência V2/V4; a intervenção nova é autoria programática Lua dentro do Aseprite. As placas novas ainda são estudos e seu acabamento conjunto com o corpo será refinado após escolha. Nenhuma opção constitui uma nova raça, classe ou personagem canônico.

Os caminhos abaixo são relativos à raiz da Character Factory, repositório irmão do jogo.

Pacote de estudo: `characters/orc-01-art-lab-v5/`. Comparação: `reports/orc-art-lab-v5/review.html`. Procedência e verificações: `reports/orc-art-lab-v5.json`. A opção vencedora está **PENDENTE DO CRIADOR**. A prioridade imediata é escolher/refinar essa direção; a integração Unity permanece uma etapa posterior, autorizada separadamente.

Verificação desta entrega: cinco PNGs integrais 1254×1254 importados sem reescala; cinco mestres com quatro camadas cada, cinco referências ocultas V4 exatas e cinco exportações salvas exatas; build do bridge com comparação RGBA de cinco quadros. A página comparativa funciona por arquivo e HTTP local, com cinco seleções, fundos/zoom e layout móvel conferidos. Os hashes de 10.039 arquivos de produção/referências protegidos permaneceram iguais durante o empacotamento. Evidências complementares: `reports/orc-art-lab-v5-source-check.json` e `reports/orc-art-lab-v5-preview-check.json`. Essas verificações são técnicas; a decisão artística continua com o criador.
