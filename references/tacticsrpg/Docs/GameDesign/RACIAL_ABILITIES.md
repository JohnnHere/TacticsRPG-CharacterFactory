# Sistema de habilidades raciais — proposta v0.1, regra de aprendizado v2.1

## Regra de aprendizado (v2.1, canônica)
- A habilidade inata e as propriedades anatômicas existem desde a criação, sem desbloqueio. Toda progressão racial (habilidades evolutivas, transformações, técnicas, poderes) acontece **exclusivamente na árvore de talentos racial**: pontos de progressão, pré-requisitos entre nós e requisitos internos da árvore.
- Nenhuma habilidade racial é desbloqueada por exploração, missões, rituais, itens, NPCs ou eventos narrativos. Transformações são **talentos** aprendidos, não gatilhos de história (ex.: formas do Lobisomem; poderes vampíricos; técnicas dracônicas do Dragonborn).

## Contrato de design
Cada raça começa com **1 traço inato**, **1 habilidade ativa** e uma pequena progressão de **4–6 nós futuros na árvore racial** (quantidade ainda não aprovada). A habilidade inata permanece vinculada à raça; outras podem ter seleção/equipamento conforme limites a definir. Jobs continuam sendo o eixo principal do combate.

## Categorias reutilizáveis
- Passivas condicionais: HP baixo, flanco, altitude, terreno, alvo marcado.
- Ativas: dano, proteção, controle, movimentação, suporte, conjuração.
- Alteração de forma: aparência, parâmetros, restrições de ação, duração, reversão.
- Interação de terreno: água, pântano, floresta, elevação, obstáculos.
- Recursos: MP/cooldown por padrão; Sangue, Corrupção ou Fome somente se comprovarem valor.

## Mecânicas avançadas a prototipar (todas como nós da árvore racial)
1. Lobisomem: humano fora de batalha; formas Predadora, Brutal, Lunar e eventualmente Alfa **aprendidas e aprimoradas na árvore racial**; não presumir todas simultâneas.
2. Dragonborn: linhagem elemental e sopro; evolução dracônica somente como hipótese.
3. Vampiro: predação, drenagem e eventual recurso Sangue; estabelecer alvos válidos.
4. Undead: imunidades biológicas, tratamento diferenciado de cura e persistência profana com contrajogo.
5. Constructo: módulos limitados e interação com reparo/cura; não criar inventário paralelo no MVP.
6. Harpia: voo limitado, altitude e vulnerabilidade antiaérea.
7. Merfolk: mobilidade anfíbia e manipulação local de água; sem exigir mapas aquáticos.
8. Centauro: galope, custo de terreno e restrições anatômicas documentadas.
9. Moon Elf: ciclo lunar em combate, sem depender necessariamente de lua astronômica global.

## Esquema conceitual de dados
`RaceId`, `AbilityId`, `Trigger`, `TargetRule`, `Cost`, `Cooldown`, `Effect[]`, `Prerequisites[]`, `Tags[]`, `VisualCue`, `Counterplay`, `BalanceNotes`.

## Critérios de aceite para cada habilidade
Texto de regra não ambíguo; custo; alcance; duração; stacking; interação com Jobs; AI utilizável; animação viável; testes de borda; contra-jogo. **Números e fórmulas permanecem TBD.**

## Retificação High Elf v1.0
A antiga 'Maestria de Escola' como traço inato não é cânone. High Elf é uma identidade aristocrática com acesso institucional e recursos, não superioridade mágica biológica. Proposta: traço de **Rede de Influência** (benefícios narrativos/recrutamento/treinamento, não combate bruto) e ativa aprendida **Comando de Corte** (suporte tático obtido por educação).
