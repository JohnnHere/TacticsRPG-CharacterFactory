# Catálogo de Jobs v2.0 — baseline consolidada

**Status:** catálogo autoral inicial, autorizado para documentação, **não implementado**. Níveis e requisitos são hipóteses de design, sujeitos a testes. Referências são inspirações de mecânica, sem copiar personagens, nomes próprios ou artes protegidas.

- 8 básicas, 18 intermediárias, 26 avançadas, 8 secretas e 3 únicas — **63 Jobs** (61 originais + Venomancer + Affliction Master).
- Cada Job possui papel, três habilidades exemplares, requisito inicial e afinidades que aceleram acesso, não concedem exclusividade automática.
- `JobLevel` representa proficiência da classe, não nível geral da unidade. Requisitos cumulativos são avaliados por IDs estáveis.
- **Regra v2.1 (canônica):** desbloqueio de Jobs e aprendizado de habilidades são EXCLUSIVAMENTE por progressão e árvores de talentos. Onde a tabela menciona "talento de conclusão" ou requisitos equivalentes, trata-se de um nó da própria árvore do Job (pontos investidos + pré-requisitos). Nenhum Job ou habilidade depende de missões, exploração, itens, NPCs, rituais, pactos, contratos ou captura de criaturas.

| Categoria | Job | Papel | Desbloqueio proposto | Kit de habilidades (conceitual) | Afinidades culturais/raciais (não bloqueio) |
|---|---|---|---|---|---|
| Básica | Squire | Versátil | Inicial | Golpe preciso; Primeiros socorros; Foco | Humano,Half Elf |
| Básica | Warrior | Dano físico | Inicial | Corte pesado; Guarda quebrada; Grito de guerra | Orc,Minotauro,Ogro |
| Básica | Archer | Distância | Inicial | Tiro mirado; Disparo alto; Chuva curta | Wood Elf,Felino / Catfolk |
| Básica | Apprentice Mage | Magia | Inicial | Faísca; Gelo menor; Concentração | Elf,Mystical Elf |
| Básica | Acolyte | Suporte | Inicial | Cura; Purificar; Proteção | Humano,Elf |
| Básica | Rogue | Mobilidade | Inicial | Golpe furtivo; Desarmar; Fuga | Goblin,Felino / Catfolk |
| Básica | Scout | Reconhecimento | Inicial | Marcar alvo; Reconhecer; Armadilha simples | Wood Elf,Centauro |
| Básica | Brawler | Combate desarmado | Inicial | Soco rápido; Agarrar; Contra-golpe | Orc,Troll |
| Intermediária | Knight | Tanque | Warrior 3 + Squire 2 | Provocar; Escudo aliado; Quebra-armadura | Anão,Humano |
| Intermediária | Monk | Dano/suporte | Brawler 3 + Acolyte 2 | Golpe de chakra; Palma curativa; Contra-ataque | Humano,Orc |
| Intermediária | Thief | Utilidade | Rogue 3 + Scout 2 | Roubar item; Roubar posição; Passo sombrio | Goblin,Felino / Catfolk |
| Intermediária | Ranger | Distância/terreno | Archer 3 + Scout 3 | Tiro perfurante; Camuflagem; Laço | Wood Elf,Centauro |
| Intermediária | Hunter | Companheiro animal | Ranger 3 + talento de vínculo na própria árvore | Domar; Ordem de ataque; Proteger mestre | Wood Elf,Felino / Catfolk |
| Intermediária | Black Mage | Dano mágico | Apprentice Mage 3 | Bola de fogo; Relâmpago; Tempestade gelada | Mystical Elf,Dark Elf |
| Intermediária | White Mage | Cura/proteção | Acolyte 3 | Cura em área; Dissipar; Ressuscitar | Elf,Humano |
| Intermediária | Elementalist | Controle elemental | Apprentice Mage 3 + Scout 2 | Parede de gelo; Solo ígneo; Corrente elétrica | Dragonborn,Lizardfolk |
| Intermediária | Alchemist | Itens/apoio | Acolyte 2 + Apprentice Mage 2 | Catalisar poção; Bomba; Antídoto | Gnomo,Goblin |
| Intermediária | Venomancer | Venenos e desgaste | Alchemist 3 + Rogue 2 + talento de toxicologia | Dose progressiva; Nuvem tóxica; Catalisar toxina | Lizardfolk,Goblin,Dark Elf |
| Intermediária | Engineer | Dispositivos | Scout 3 + Alchemist 2 | Torre mecânica; Mina; Reparar | Gnomo,Constructo / Golem |
| Intermediária | Bard | Buffs | Acolyte 2 + Rogue 2 | Canção de coragem; Dissipar medo; Marcha | Sátiro / Fauno,Humano |
| Intermediária | Shaman | Natureza/controle | Acolyte 2 + Elementalist 2 + talento de rito natural | Boneco de espinhos; Totem de raízes; Ordem espiritual | Troll,Sátiro / Fauno,Wood Elf |
| Intermediária | Spearman | Alcance físico | Warrior 3 + Scout 2 | Estocada longa; Muralha de lanças; Impalar | Centauro,Lizardfolk |
| Intermediária | Berserker | Risco/dano | Warrior 4 + Brawler 2 | Fúria insaciável; Golpe selvagem; Rugido | Orc,Minotauro |
| Intermediária | Geomancer | Terreno | Elementalist 3 + Scout 3 | Terreno vivo; Fissura; Proteção geológica | Wood Elf,Anão |
| Intermediária | Oracle | Debuffs | Apprentice Mage 3 + Acolyte 2 | Maldição; Silêncio; Presságio | Moon Elf,Dark Elf |
| Intermediária | Mystic Knight | Híbrido | Knight 3 + Black Mage 2 | Lâmina elemental; Guarda rúnica; Ruptura | Dragonborn,Elf |
| Avançada | Samurai | Técnica física | Knight 3 + Monk 3 + talento de postura | Iai; Postura; Contra-corte | Humano,High Elf |
| Avançada | Ninja | Mobilidade/assassinato | Thief 4 + Monk 3 | Passo duplo; Shuriken; Sombra | Felino / Catfolk,Dark Elf |
| Avançada | Dragoon | Lança/salto | Spearman 4 + Knight 2 | Salto; Investida aérea; Caça-dragões | Dragonborn,Harpia / Aviário |
| Avançada | Paladin | Defesa sagrada | Knight 4 + White Mage 3 + talento de juramento | Aura protetora; Julgamento; Interceptar | Humano,Anão |
| Avançada | Dark Knight | Sacrifício/trevas | Knight 4 + Black Mage 3 + talento de sacrifício | Lâmina sombria; Sacrifício; Drenar | Dark Elf,Half-Demon |
| Avançada | Red Mage | Híbrido magia | Black Mage 3 + White Mage 3 | Dupla escola; Magia rápida; Selo | Half Elf,Elf |
| Avançada | Time Mage | Controle temporal | Black Mage 3 + Oracle 3 | Acelerar; Lentidão; Retardar ação | Moon Elf,Mystical Elf |
| Avançada | Summoner | Múltiplas invocações | Black Mage 3 + Shaman 2 + talento de convocação | Convocar familiar; Ordem coletiva; Troca de formação | Mystical Elf,Elf,Half Elf |
| Avançada | Warlock | Demônio principal | Black Mage 4 + Oracle 2 + talento de pacto | Invocar guardião infernal; Pacto de dor; Ordem demoníaca | Demon,Half-Demon |
| Avançada | Affliction Master | **Mestre de DoT**: múltiplas aflições, propagação e controle | Oracle 4 + Venomancer 3 + Black Mage 3 + talento de aflição | Agonia persistente; Contágio calculado; Tormento prolongado | Dark Elf,Undead,Vampiro,Half-Demon |
| Avançada | Necromancer | Cadáveres | Black Mage 4 + Oracle 3 + talento de reanimação | Reanimar cadáver; Ordem dos mortos; Colheita de essência | Undead,Dark Elf |
| Avançada | Beastmaster | Controle feras | Hunter 4 + Shaman 2 | Comando de matilha; Vínculo primal; Adestrar elite | Felino / Catfolk,Wood Elf |
| Avançada | Druid | Metamorfose natural | Shaman 4 + Geomancer 3 | Forma animal; Bosque vivo; Renovação | Wood Elf,Sátiro / Fauno |
| Avançada | Runesmith | Encantamento/equipamento | Engineer 3 + Mystic Knight 3 | Runa de guarda; Arma rúnica; Campo de selo | Anão,Gnomo |
| Avançada | Templar | Antimagia | Paladin 2 + Oracle 3 | Selo antimágico; Prisão sagrada; Expurgar | Humano,High Elf |
| Avançada | Assassin | Eliminação | Ninja 3 + Oracle 2 | Execução; Marca mortal; Ocultação | Dark Elf,Goblin |
| Avançada | Sniper | Alcance extremo | Ranger 4 + Archer 4 | Disparo longo; Mira concentrada; Tiro de supressão | Wood Elf,Centauro |
| Avançada | Spellblade | Híbrido ofensivo | Mystic Knight 3 + Red Mage 2 | Corte mágico; Combo rúnico; Explosão curta | Elf,Dragonborn |
| Avançada | Battle Cleric | Suporte de linha | Monk 3 + White Mage 3 | Círculo de cura; Golpe sagrado; Vigília | Anão,Humano |
| Avançada | Warden | Defesa de terreno | Knight 3 + Geomancer 3 | Barreira; Zona guardada; Âncora | Anão,Constructo / Golem |
| Avançada | Illusionist | Engano | Oracle 3 + Rogue 3 | Imagem falsa; Confundir; Passagem velada | Moon Elf,Sátiro / Fauno |
| Avançada | Blood Mage | Magia de sacrifício | Black Mage 4 + Alchemist 2 + talento de sangue | Conversão vital; Selo sanguíneo; Explosão carmesim | Vampiro,Half-Demon |
| Avançada | Stormcaller | Clima/eletricidade | Elementalist 4 + Time Mage 2 | Tempestade; Campo condutor; Vento cortante | Harpia / Aviário,Merfolk / Aquático |
| Avançada | Tidecaller | Água/controle | Elementalist 3 + Geomancer 3 + talento de maré | Maré alta; Correnteza; Névoa | Merfolk / Aquático,Lizardfolk |
| Avançada | Artificer | Autômatos/engenharia | Engineer 4 + Runesmith 2 | Drone de suporte; Núcleo auxiliar; Sobrecarga | Gnomo,Constructo / Golem |
| Avançada | Duelist | Esgrima | Thief 3 + Knight 3 | Desafio; Aparar; Ripostar | Humano,High Elf |
| Secreta | Chronomancer | Tempo avançado | Time Mage 5 + talento de conclusão da árvore | Eco temporal; Repetição parcial; Suspender | Moon Elf,Mystical Elf |
| Secreta | Grand Summoner | Mestre das invocações | Summoner 5 + talento de convergência | Convergência; Reforço de vínculo; Chamado supremo | Mystical Elf,Elf |
| Secreta | Lich | Morte avançada | Necromancer 5 + talento de filactério | Âncora de alma; Legião espectral limitada; Frio eterno | Undead |
| Secreta | Demonologist | Pacto supremo | Warlock 5 + talento supremo de pacto | Demônio exaltado; Fusão pactuada; Ordem suprema | Demon,Half-Demon |
| Secreta | Dragon Sage | Ascendência dracônica | Mystic Knight 4 + Elementalist 4 + talento dracônico | Ressonância ancestral; Sopro amplificado; Escamas | Dragonborn |
| Secreta | Spirit Warden | Espíritos e proteção | Shaman 5 + Warden 3 + talento espiritual | Guardião ancestral; Totem de vigília; Véu espiritual | Troll,Wood Elf |
| Secreta | Void Weaver | Espaço/controle | Illusionist 4 + Time Mage 4 + talento do vazio | Dobra espacial; Campo vazio; Ancoragem | Mystical Elf,Dark Elf |
| Secreta | Royal Strategist | Comando político | Bard 3 + Templar 3 + talento de comando | Ordem tática; Reserva; Coordenação | High Elf,Humano |
| Única | Sword Saint | Espadachim lendário | Personagem nomeado; condição de história | Técnica lendária; Corte final; Postura perfeita | Variável |
| Única | Herald of Ash | Avatar de cinzas | Personagem nomeado; condição de história | Chamas ancestrais; Cinzas vivas; Decreto | Variável |
| Única | Moon Oracle | Oráculo lunar | Personagem nomeado; condição de história | Profecia lunar; Selo da noite; Vigília | Variável |

## Distinções obrigatórias de design (v2.0)
- **Affliction Master** é Job **independente**, não uma especialização ou subclasse de Warlock. **Não requer Warlock** e não recebe automaticamente demônio pactuado. É o maior especialista em dano periódico (DoT), cumulativo, propagação e desgaste.
- **Venomancer** é Job independente intermediário de toxinas e envenenamento; o seu foco é veneno, antídotos, zonas tóxicas e redução de eficiência do inimigo. **Não** domina todos os tipos de DoT.
- **Shaman** é versátil: bonecos controláveis, totens, raízes, suporte, venenos e desgaste. Não deve superar Affliction Master em DoT puro, Venomancer em especialização tóxica, nem Summoner em quantidade de invocações.
- **Warlock** permanece demonologista de um demônio principal robusto; não confundir com Affliction Master.
- **Black Mage** inclui magias clássicas de fogo, gelo e raio; **Elementalist** manipula interações elementais e terreno; **Stormcaller**, **Tidecaller**, **Geomancer** e **Mystic Knight** aprofundam outras fantasias. Não adicionar Pyromancer, Cryomancer, Arcanist ou Plague Doctor como Jobs independentes nesta versão. Fogo/gelo/arcano podem ser árvores/escolas internas, sem ampliar catálogo.
- Os nomes de Jobs e kits são provisórios e devem ser refinados antes de produção. Requisitos de progressão são hipóteses, não balanceamento aprovado.

## Definição de kits
As três habilidades por Job são **sementes de design**, não kits finais. Cada Job deverá futuramente receber ações, passiva, reaction/support/movement quando pertinentes, custos, alcance, altura, área, duração, efeitos, contrajogo, animações e testes.

## Jobs únicos
Os três Jobs únicos são **placeholders narrativos**, não personagens aprovados. Podem ser alterados sem afetar o núcleo. Seu acesso depende do personagem, nunca de uma raça inteira.
