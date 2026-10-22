# Raças jogáveis — Catálogo e arquitetura (proposta v0.1, regra de aprendizado v2.1)

**Status:** 28 raças são elenco-alvo e jogáveis em alguma medida. Nem todas são recrutáveis no começo, igualmente comuns ou pertencentes às facções do protagonista. **Não implementar sem validação posterior.**

## Decisões consolidadas
- **Aprendizado racial v2.1 (canônico):** características anatômicas e propriedades inatas da raça existem desde a criação do personagem, sem desbloqueio; habilidades raciais evolutivas, transformações, técnicas e poderes são aprendidos **exclusivamente pela árvore de talentos racial**, com pontos de progressão e pré-requisitos (`DESIGN_DECISIONS.md` §Regra canônica v2.1). Exemplos: o Lobisomem aprende e aprimora suas formas de combate na árvore racial; o Dragonborn aprende técnicas dracônicas; o Vampiro aprende poderes vampíricos; os Elfos aprendem suas habilidades específicas pela progressão racial. Nenhuma habilidade racial depende de exploração, missões, rituais, pactos ou eventos narrativos.
- Manter as 22 raças originais e adicionar Lizardfolk, Harpia/Aviário, Merfolk/Aquático, Felino/Catfolk, Constructo/Golem e Sátiro/Fauno.
- Raça ≠ cultura ≠ facção ≠ Job. Não atribuir alinhamento moral por biologia.
- Disponibilidade narrativa, chance de recrutamento e acesso a Jobs são eixos independentes.
- Todas devem ser jogáveis em alguma medida; algumas por eventos, alianças, deserções, personagens especiais ou recrutamento avançado.
- Lobisomens parecem humanos normalmente e desbloqueiam transformações de combate.
- Elfos possuem seis designações élficas e Half Elf como ascendência híbrida; as sete opções permanecem no catálogo de 28.

## Catálogo

| Raça | Fantasia mecânica | Traço inato (proposta) | Ativa (proposta) | Cultura possível (não exclusiva) | Disponibilidade ilustrativa | Perfil visual |
|---|---|---|---|---|---|---|
| Humano | Adaptação | Adaptabilidade | Improvisação | Reinos plurais, ordens e mercadores | Comum | Humanoide |
| Orc | Fúria | Fúria crescente | Frenesi | Clãs e confederações, aliados e inimigos | Contextual | Robusto |
| Troll | Regeneração | Regeneração interrompível | Recuperação primitiva | Tradições xamânicas, povos diversos | Contextual | Robusto |
| Ogro | Massa | Resistência a empurrão | Esmagamento | Fortalezas e comunidades gigantes | Raro | Grande |
| Dragonborn | Linhagem | Resistência elemental da linhagem | Sopro dracônico | Clãs e dinastias dracônicas | Contextual | Humanoide |
| Anão | Resiliência | Constituição anã | Postura de ferro | Reinos de forja e guildas | Comum/contextual | Robusto |
| Gnomo | Engenharia | Engenhosidade | Dispositivo arcano | Cidades tecnomágicas | Contextual | Pequeno |
| Goblin | Oportunismo | Bônus contra vulneráveis | Truque sujo | Mercadores, oficinas e bandos | Contextual | Pequeno |
| Undead | Pós-vida | Imunidades biológicas específicas | Persistência profana | Necrópoles e ordens independentes | Raro | Variável |
| Demon | Corrupção | Essência infernal | Marca da corrupção | Domínios, castas e dissidentes | Raro | Variável |
| Half-Demon | Dualidade | Sangue dual | Manifestação parcial | Diásporas e linhagens mistas | Raro/contextual | Humanoide |
| Vampiro | Sangue | Sede de sangue | Predação | Casas noturnas e linhagens | Raro | Humanoide |
| Lobisomem | Metamorfose | Instinto predatório | Metamorfose | Clãs humanos e tradições lunares | Raro/contextual | Metamorfo |
| Minotauro | Investida | Ímpeto após deslocamento | Carga | Cidades-fortaleza e ordens marciais | Contextual | Robusto |
| Centauro | Mobilidade | Passada equina | Galope | Confederações das planícies | Contextual | Quadrúpede |
| Elf | Harmonia | Sintonia natural | Afinidade temporária | Civilizações élficas plurais | Contextual | Humanoide |
| Dark Elf | Sombras | Visão sombria | Véu sombrio | Casas e cidades subterrâneas | Contextual | Humanoide |
| Moon Elf | Ciclos | Ciclo lunar | Bênção lunar | Templos e observatórios | Contextual | Humanoide |
| Mystical Elf | Arcano | Ressonância arcana | Sobrecarga arcana | Ordens de pesquisa | Raro/contextual | Humanoide |
| Half Elf | Herança | Dupla herança | Convergência | Comunidades multiculturais | Comum/contextual | Humanoide |
| Wood Elf | Terreno | Guardião silvestre | Raízes vivas | Clãs florestais | Contextual | Humanoide |
| High Elf | Disciplina | Maestria de escola | Conjuração refinada | Academias e reinos antigos | Contextual | Humanoide |
| Lizardfolk | Adaptação ambiental | Escamas adaptativas | Ataque venenoso | Pântanos e cidades ribeirinhas | Contextual | Reptiliano |
| Harpia / Aviário | Altitude | Natureza alada | Mergulho predatório | Cidades altas e clãs aéreos | Raro/contextual | Alado |
| Merfolk / Aquático | Água | Locomoção anfíbia | Maré ascendente | Reinos costeiros e submersos | Contextual | Anfíbio |
| Felino / Catfolk | Agilidade posicional | Reflexos felinos | Salto predatório | Povos caçadores e cidades mercantis | Contextual | Felino |
| Constructo / Golem | Corpo artificial | Imunidades biológicas | Reconfiguração modular | Seres conscientes e guardiões | Raro | Artificial |
| Sátiro / Fauno | Encantamento | Espírito feérico | Melodia encantadora | Bosques e tradições musicais | Contextual | Caprino |

## Regras de arquitetura
- `RaceDefinition` contém identidade, anatomia, tags, habilidades e compatibilidade, **não** facção fixa.
- `RaceAbilityDefinition` representa habilidades passivas/ativas e seus gatilhos; **cada habilidade racial evolutiva corresponde a um nó da árvore de talentos racial (v2.1)**; reutilizar componentes (dano, cura, deslocamento, status, transformação) em vez de subclasses para cada raça.
- `RacialProgression` representa a árvore de talentos racial e seus desbloqueios por pontos/pré-requisitos, independente da árvore de Jobs.
- `CharacterVisualProfile` resolve sprites, direção, forma, animações e equipamentos visuais.
- `FactionMembership`, `RecruitmentRule` e `JobAccessRule` devem ser dados separados, referenciados por IDs estáveis.
- Preferir composição e ScriptableObjects ou dados equivalentes validados, sem alterar a arquitetura Unity atual antes de uma auditoria.
- Primeira versão: unidade ocupa uma célula; voo, água e grandes corpos devem ser testados sem assumir grid multi-célula.

## Regras de balanceamento
- Evitar bônus genéricos como identidade única. Cada raça deve alterar pelo menos uma decisão tática.
- Habilidades raciais não devem substituir Job principal ou subjob.
- Biomas concedem vantagem, não tornam personagens inviáveis fora deles.
- Vulnerabilidades de Troll, Undead, Golem etc. precisam de contrajogo e documentação explícita.
- Raças com transformações e recursos exclusivos são casos avançados; não criar 28 barras de recursos.

## Questões em aberto
- Quem pode ser recrutado em cada ato, e por qual facção?
- Quais raças possuem linhagens/subespécies selecionáveis e quais são culturas?
- Como cura, ressurreição e status interagem com Undead, Demon e Golem?
- Quais formas do Lobisomem substituem equipamento/ações?
- Como voo e locomoção aquática funcionam em mapas sem água ou altitude?
- Como equipamentos e sprites se adaptam a anatomias distintas?

## Cânone élfico — decisão explícita v1.0 (prevalece sobre interpretações anteriores)
- **Elf**: linhagem élfica original e ancestral, origem das demais.
- **Dark Elf**: linhagem élfica transformada/corrompida por magia das trevas. Corrupção de origem não implica alinhamento moral individual.
- **Moon Elf**: descendentes élficos especializados em magia lunar, com características próprias desenvolvidas ao longo de gerações.
- **Mystical Elf**: linhagem dedicada à magia arcana; especialização prolongada moldou práticas e características.
- **Wood Elf**: linhagem vinculada às magias e aos mistérios das florestas.
- **High Elf**: **estrato aristocrático, político e econômico**, de grande influência; NÃO é automaticamente uma espécie biologicamente superior ou uma linhagem de magia mais forte. O acesso ao poder é social e institucional, não bônus genético automático.
- **Half Elf**: descendência mista de humano e Elf; podem existir heranças de diferentes linhagens élficas, a definir.
- Facção, linhagem, condição social e raça são campos separados. High Elf deve ser modelado como identidade social/cultural elegível e opção de personagem, preservando as 28 entradas do catálogo, sem impor um gene de nobreza.
- A descrição anterior de High Elf como 'maestria arcana inata' fica **substituída**: acesso privilegiado a tutores, academias, recursos, redes e Jobs culturais; qualquer habilidade arcana é aprendida.
