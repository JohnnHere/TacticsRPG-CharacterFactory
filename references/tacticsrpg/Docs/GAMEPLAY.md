# GAMEPLAY — Como o jogo funciona hoje

> Documento vivo, restrito às regras de gameplay **como estão implementadas**. Valores são provisórios.
> O planejamento fica no [ROADMAP.md](ROADMAP.md). Quando uma regra mudar no código, atualize aqui.

**Estado atual:** existem movimento em mapa, ataque corpo a corpo e à distância (arco) com direção (frente/lado/costas), alcance vertical por arma, linha de visão, crítico, ordem de turnos por CT, IA mínima, objetivos de vitória/derrota e infraestrutura interna de snapshots de batalha (sem save/load livre para o jogador). Uma batalha pode ser jogada do início ao fim. Há sete habilidades de teste: Corte Pesado, Cura, Faísca, Tiro Mirado, Chuva Curta, Proteção e Gelo Menor; área pequena e modificadores temporários estão implementados. Jobs e progressão por talentos ainda não existem.

> Nota (2026-10-10): quando o sistema de habilidades for implementado, o desbloqueio seguirá a **regra canônica v2.1** do Game Design (`Docs/GameDesign/DESIGN_DECISIONS.md`): aprendizado exclusivamente por árvores de talentos (Job e racial). Este documento continua registrando apenas o que estiver implementado.

---

## 0. Regras centrais (versão inicial, task 1.1)

Resumo das decisões que sustentam o resto do documento. Os detalhes estão nas seções seguintes.

| Tema | Regra | Referência |
|---|---|---|
| Grid | Tiles quadrados, movimento ortogonal, altura inteira de 0 a 9 por tile | FFT, Triangle Strategy |
| Movimento | `Move` (orçamento de custo) + `Jump` (desnível por passo); custo por terreno; aliados atravessáveis, inimigos bloqueiam | FFT |
| Turnos | Ordem por CT e Velocidade; no turno, 1 movimento + 1 ação em qualquer ordem; fazer menos faz voltar mais rápido | FFT |
| Direção | Depende da ordem: Mover → Atacar trava a direção no alvo; qualquer outra combinação (Atacar → Mover, Atacar → Esperar, Só mover, Só esperar) permite escolha manual | FFT |
| Flanco | O ângulo (frente/lado/costas) muda dano, chance de acerto e crítico | FFT, Triangle Strategy |
| Altura | Limita o desnível que a arma alcança, entra na linha de visão, dá alcance extra ao arco e altera o dano em até ±20% | FFT |
| Armas | Cada arma define poder, acerto, alcance, desnível, linha de visão e bônus de crítico | Original |
| Derrota de unidade | HP 0 remove a unidade da batalha (ferimentos e morte permanente ficam para o Estágio 8) | Provisório |
| Objetivos | Configuráveis por mapa, com unidades-chave | Triangle Strategy |
| Câmera | Ângulo fixo em diagonal, giro de 90°, três níveis de zoom, foco automático na unidade da vez | Triangle Strategy |
| Saves | Save/load livre em combate desabilitado; checkpoints condicionais são futuros | MVP 5A.4 |

**Em aberto:** altura afetando o acerto (hoje afeta alcance, linha de visão e dano), contra-ataque e reações, MP e custos de habilidade, condições, unidades maiores que 1 tile.

---

## 1. Grid e mapa

- O mapa é um grid retangular de tiles. Coordenada `(X, Y)`; a altura é propriedade do tile.
- Cada tile tem:
  - **Altura**: inteiro de 0 a 9. Cada unidade de altura equivale a 0,5 unidade de mundo na visualização.
  - **Tipo**: `Ground` (chão), `Mud` (lama) ou `Water` (água profunda).
- Um mapa é um `MapData` (ScriptableObject) com o layout em texto, uma linha por Y:

| Caractere | Significado |
|---|---|
| `0`–`9` | Chão com essa altura |
| `a`–`j` | Lama com altura 0–9 (`a` = 0) |
| `~` | Água (altura 0, não caminhável) |

- O `MapData` também lista as unidades iniciais (nome, posição, direção, arma, velocidade, time, unidade-chave) e os objetivos de vitória e derrota.
- Mapa de teste: `Assets/Resources/Maps/Proving.asset`.

## 2. Unidades

- Cada unidade ocupa **1 tile**, pertence a um **time** (número inteiro) e tem uma **direção** (`Facing`, ortogonal).
- Atributos de combate, valores de teste: HP máximo 100, Força 5, Defesa 3, Evasão 20%, Velocidade 10, uma arma.
- Armas:

| Arma | Poder | Acerto base | Alcance | Desnível máx. | Linha de visão |
|---|---|---|---|---|---|
| Espada | 15 | 90% | 1 (adjacente) | 1 | não |
| Machado | 20 | 80% | 1 (adjacente) | 1 | não |
| Arco | 12 | 85% | 2 a 6 (+1 a cada 2 de altura de vantagem, até +3) | sem limite | sim |

- **Bônus de crítico:** armas e unidades têm um bônus de chance de crítico (hoje 0), para classe, raça e passivas somarem no futuro.

- Atributos de movimento (`MovementProfile`), valores de teste:

| Atributo | Significado | Padrão |
|---|---|---|
| `Move` | Orçamento de custo por movimento | 4 |
| `JumpUp` | Maior subida de altura por passo | 2 |
| `JumpDown` | Maior descida de altura por passo | 2 |

## 3. Movimento

- O movimento é **ortogonal** (4 direções), passo a passo.
- Um passo de um tile para o vizinho é válido se:
  1. o destino está dentro do mapa;
  2. o destino não é água;
  3. o destino não tem um **inimigo** (outro time);
  4. a diferença de altura respeita o salto: subir até `JumpUp`, descer até `JumpDown`.
- **Custo:** cada passo custa o custo do tile de destino. Chão = 1, lama = 2. A altura não altera o custo (como em FFT). O total gasto não pode passar de `Move`.
- **Aliados:** podem ser atravessados, mas o movimento **não pode terminar** em um tile ocupado por aliado.
- **Inimigos:** bloqueiam totalmente a passagem.
- O caminho usado é o de menor custo (Dijkstra). Ao passar o mouse num tile alcançável, o caminho é mostrado.
- Depois de mover, o alcance é recalculado a partir da nova posição.
- Cada turno permite **um movimento**; ele pode ser feito antes ou depois da ação.
- **Voltar ao início do turno:** enquanto a unidade **não tiver agido** (atacado), o movimento pode ser desfeito: ela volta ao tile e à direção em que começou o turno e recupera o movimento, para o jogador repensar. Depois de atacar, não dá mais. Não funciona se outra unidade ocupar o tile inicial. O ponto de início também é salvo no save.
- **Direção:** ao terminar de mover, a unidade fica virada para o último passo dado.

## 3.1 Ataque básico (arma)

- O ataque só atinge **unidades de outro time** no alcance da arma. Para acertar, o alvo precisa estar:
  1. **a uma distância** dentro de `alcance mínimo` e `alcance máximo` da arma (ortogonal, em tiles);
  2. **dentro do desnível** que a arma alcança: a diferença de altura entre atacante e alvo, para cima ou para baixo, não pode passar do **desnível máximo** da arma. O padrão de toda arma é 1; categorias de arma futuras poderão ter outro valor;
  3. **com linha de visão**, se a arma for de projétil (arco).
- **Linha de visão** (estilo FFT): tira-se uma reta do atacante ao alvo, 1 de altura acima do topo de cada tile. Um tile no meio do caminho **bloqueia** se for mais alto que a reta naquele ponto. Atirar de cima passa por cima de muros da mesma altura; obstáculos baixos não bloqueiam. Unidades não bloqueiam o tiro.
- O arco não acerta quem está adjacente (alcance mínimo 2).
- **Atacar um tile vazio** (dentro do alcance, desnível e linha de visão da arma) é uma ação válida: o ataque acontece (animação e mensagem), ninguém é atingido e a **ação é consumida do mesmo jeito**, com o atacante terminando virado para o tile.
- **Alcance por altura:** quem atira de um tile mais alto que o alvo ganha **+1 de alcance máximo a cada 2 níveis de vantagem**, até +3 (o arco chega a 9). Estar em desvantagem não reduz o alcance. Armas corpo a corpo não têm esse bônus; o valor é um atributo da arma, então categorias futuras podem ter o seu.
- Ao atacar, o atacante vira para o alvo, inclusive ao errar. **Mover → Atacar** termina nessa direção e encerra automaticamente após o feedback. **Atacar → Mover**, **Atacar → Esperar** e **Só atacar** liberam a **escolha manual** da direção ao encerrar. Ataque básico (inclusive tile vazio válido) e Corte Pesado seguem a mesma regra. A correção do MVP 5C.1 (§3.1D) substitui o "só atacar preserva a direção do golpe" do MVP 5A.2.
- **Ângulo do golpe:** depende de onde o atacante está em relação ao alvo e para onde o alvo olha.
  - **Frente:** o atacante está no lado para o qual o alvo olha.
  - **Costas:** o atacante está no lado oposto.
  - **Lado:** os outros dois lados (e diagonais exatas).

| Ângulo | Multiplicador de dano | Evasão do alvo que ainda vale |
|---|---|---|
| Frente | ×1,00 | 100% |
| Lado | ×1,15 | 50% |
| Costas | ×1,50 | 0% |

- **Chance de acerto** = `acerto da arma × (1 − evasão do alvo × fator do ângulo)`. Com os valores de teste, a espada acerta 72% pela frente, 81% de lado e 90% pelas costas.
- **Dano** = `max(1, arredonda((poder da arma + Força) × multiplicador do ângulo × multiplicador de altura) − Defesa do alvo)`. Espada em terreno plano: 17 pela frente, 20 de lado, 27 pelas costas.
- **Altura no dano:** cada nível de vantagem (atacante mais alto que o alvo) dá **+4%** de dano; cada nível de desvantagem tira **4%**. O efeito é limitado a **±20%** (5 níveis), para não dominar o ângulo e a arma. Vale também para o crítico e multiplica com o ângulo. Exemplos com a espada de frente: 1 nível acima → 18; 1 nível abaixo → 16. Pelas costas e 1 nível acima → 28. A dica de ataque mostra a vantagem de altura.
- Um sorteio em [0, 1) decide o acerto: acerta se for menor que a chance.
- **Crítico:** só um golpe que acertou pode ser crítico (segundo sorteio). A chance base depende do ângulo; arma e unidade somam bônus por cima (máximo 100%). O crítico causa **×1,5** de dano, calculado junto com o multiplicador do ângulo antes da Defesa.

| Ângulo | Chance base de crítico | Espada: dano normal / crítico |
|---|---|---|
| Frente | 0% | 17 / 27 |
| Lado | 10% | 20 / 32 |
| Costas | 20% | 27 / 42 |

- O arco usa a mesma fórmula (poder 12 + Força 5): pelas costas, 23 de dano.
- HP chega a 0: a unidade é removida do mapa e da fila de turnos.
- Atacar consome a **ação** do turno (uma por turno).

## 3.1A Corte Pesado — MVP 5A (Task 2.1A)

- ID estável `warrior.heavy_slash`, nome **Corte Pesado**: "Um golpe poderoso que sacrifica precisão em troca de maior dano."
- `AbilityDefinition` imutável e catálogo `Abilities` no Core separam parâmetros de validação/execução. `Abilities.TryExecute` exige turno ativo, ação livre, ID disponível, espada ou machado e um tile adjacente válido no alcance da arma, com desnível e linha de visão da arma. O tile pode estar vazio ou ocupado por inimigo vivo; aliado, próprio tile e fora do mapa são rejeitados.
- Reutiliza `Combat.PreviewFrom`/`Execute`: dano = `max(1, arredonda((poder + Força) × ângulo × altura × crítico quando aplicável × 1,35) − Defesa)`; chance = `clamp01(acerto da arma × (1 − evasão × fator do ângulo) − 0,10)`. Ambos os modificadores entram uma vez; crítico, flanco e altura continuam iguais. Frente/plano com espada: 24 de dano e 62% de acerto (ataque básico: 17 e 72%). Valores **provisórios de playtest**, não cânone de balanceamento.
- Consome uma ação inclusive ao errar, trava direção até um eventual movimento posterior e remove derrotados uma vez; não muda movimento nem CT. Alvo inválido, seleção e cancelamento não executam a habilidade. Sem MP, cooldown, área ou status.
- Acesso **exclusivamente como fixture de desenvolvimento**: `DevelopmentAbilityFixture.Apply` concede o ID ao `Hero` do time 0 no início e após load do sandbox. Outras unidades não recebem. Não implementa aprendizado; regra canônica v2.1 continua exclusivamente por árvores de talentos.
- Menu Ação: **Atacar [F]** e, somente para quem possui acesso, **Corte Pesado [H]**; `>` marca a opção selecionada. Prévia real mostra acerto, dano, crítico, ângulo e altura. Corte Pesado destaca tiles válidos, inclusive vazios. Um golpe no vazio vira para o tile e consome exatamente uma ação, sem dano, reação Hit, sorteio ou resultado fictício de acerto/crítico/derrota; reutiliza Attack e feedback de golpe vazio. **Esc** sai da seleção e limpa a habilidade sem gastar ação; M troca para movimento. F continua escolhendo ataque básico.
- **Posse versus disponibilidade (MVP 5A.5):** `Abilities.HasAccess` consulta ID conhecido e `AvailableAbilityIds` da unidade. Sem posse, o botão não aparece e H/Core rejeitam seleção/execução. Com posse e ação usada ou arma incompatível, permanece visível/desabilitado. Para Corte Pesado, a fixture concede somente a nome exato Hero no time 0; Soldier, Ally, Archer e Hero inimigo não recebem esse ID por padrão. O MVP 5B acrescenta grants próprios para Ally/Soldier/Archer, descritos abaixo. É acesso runtime temporário, não Jobs/talentos/equipamento aprendidos; integração futura continua pendente.
- Usa Attack/Hit/Defeat e feedback existentes, com Hit apenas em acerto e um número de dano por resolução. IA continua usando ataque básico.
- Save v2 e semântica do snapshot preservados: os IDs da fixture não são serializados; acesso é reaplicado no sandbox e seleção limpa após load. Persistência de talentos aprendidos permanece futura.
- Validação automatizada do Core e compilação da Presentation realizadas; visual e cancelamento via entrada real precisam de verificação manual no Editor; F5/F9 foram removidos no MVP 5A.4 (ver `Docs/MVP_5A_HEAVY_SLASH.md`).

## 3.1B Lote MVP 5B — habilidades de protótipo (2026-10-13)

Todos os valores são provisórios. O catálogo imutável `Abilities.All` agora tem quatro IDs. Posse, turno, ação disponível, arma e alvo são validados no Core antes de alterar HP/flags. Ações físicas usam `Combat` e `AttackResult`; efeitos de suporte/magia usam `AbilityResult` (tipo, quantidade real e derrota), sem fingir rolagem física. Inválidos e cancelamento não gastam recursos; execução consome uma ação, preserva movimento não usado e remove derrotados uma única vez.

| ID / nome | Regra implementada | Grant temporário / atalho |
|---|---|---|
| `warrior.heavy_slash` / Corte Pesado | Regras acima, preservadas | Hero / H |
| `acolyte.heal` / Cura | Recupera até 30 HP, limitado ao HP faltante; Manhattan 0–3; si ou aliado vivo ferido. Rejeita cheio, morto, inimigo e vazio. Sem arma, altura ou LoS como requisitos; sem crítico, rolagem, dano ou reviver. Não altera facing nem trava direção; escolha final manual inclusive após mover + curar. | Ally / C |
| `mage.spark` / Faísca | Inimigo ou aliado vivo (exceto si), ou tile vazio; Manhattan 1–3; desnível absoluto até 3; `Combat.HasLineOfSight` traça entre centros dos tiles à altura de corpo existente. Terreno acima da linha bloqueia. 20 HP de dano mágico direto (limitado ao HP restante), inclusive fogo amigo, sem arma/força/defesa física/flanco/multiplicador físico de altura/acerto/crítico. Vazio consome uma ação e não causa dano. Sem resistência/status/elemento/DoT. Permissões próprias desta habilidade, não regra global de magia. | Soldier / G |
| `archer.aimed_shot` / Tiro Mirado | Exige arco; alcance mínimo/máximo, bônus de altura, desnível e LoS vêm da arma. Inimigo ou vazio válido; aliado inválido. Chance física +0,15 com clamp; dano bruto ×0,90 antes do arredondamento/defesa, uma vez, incluindo flanco/altura/crítico existentes. Usa `Combat.PreviewFrom/Execute` sem fórmula nova. | Archer / T |

Grants são por nome exato e time 0, reaplicados no início/reconstrução interna; inimigos não recebem por nome. Não são Jobs ou aprendizado, e não substituem a regra v2.1 de aprender exclusivamente por talentos e usar habilidades disponíveis no Job/Subjob/slots futuros. IDs runtime ainda não são serializados. Menu percorre o catálogo e lista somente posse; ação usada/arma incompatível indicam execução indisponível, mas permitem consultar a habilidade. H/C/G/T e mouse verificam posse para abrir a consulta; a execução exige `CanSelect` e alvo válido no Core. M/F continuam movimento/ataque básico.

As habilidades mostram alcance geométrico em quadrados cinza grandes, sem depender de ocupação, HP ferido ou ação livre; marcadores menores azuis (Cura) ou vermelhos (demais habilidades) indicam tiles executáveis conforme `Abilities.CanTargetTile`. Sem alvo válido, Cura continua consultável com aviso; aliado cheio pode estar no alcance sem receber marcador válido. Após gastar a ação, o alcance continua consultável sem marcadores de execução. Tooltips e barra mostram alcance, tipos de alvo, custo e restrições. Prévia de Cura informa HP recuperado; Faísca informa dano direto e sinaliza FOGO AMIGO; Tiro Mirado usa prévia física. Cura/Faísca reutilizam brilho e número flutuante, sem animação de espada; Faísca usa Hit/Defeat do alvo e feedback de derrota existentes. Faísca no vazio mostra texto no tile, sem golpe de arma, dano ou Hit. Tiro Mirado usa feedback/flecha do arco; flecha no vazio segue o ponto selecionado sem dano. Cura não toca Hit. Corte Pesado/ataque básico mantêm animações anteriores.

Faísca e Tiro Mirado seguem ordem ofensiva 5A.2: mover→agir trava direção do alvo e encerra após feedback; agir→mover abre escolha manual; só agir mantém direção ofensiva ao encerrar. Cura é suporte e permite direção manual. Mira/Comandos/Inspeção, fila projetada e política de saves 5A.4 permanecem; F5/F9 seguem inativos. Nenhum mapa, snapshot v2, fórmula CT, sprite ou animação foi modificado.

**Testes executados por checkpoint:** A (Cura): 209 Core passaram; B (Faísca): 212; C (Tiro Mirado): 216; D (integração): 230 Core passaram, 0 falhas. Todos compilados externamente com Roslyn e referências locais; avisos anteriores CS0618/CS1701. Runner externo por reflexão NUnit, não Test Runner/PlayMode. Round-trip JSON externo System.Text.Json de snapshot v2 após Corte Pesado passou; JsonUtility não foi executado. Os 13 testes puros existentes da Presentation foram executados com assemblies Unity: 12 passaram e 1 falhou (`DirectionMappingTests.Index_DerivesFromRealYaw_SurvivesFreeCamera`, empate unitYaw=135/cameraYaw=45: esperava 1, código retorna 2). UnitView e esse teste estão inalterados; divergência preexistente fora do lote, sem modificar animações.

**Correção de targeting (2026-10-14):** `CanReachTile`/`GeometricTiles` separam geometria de `CanSelect` (turno/ação/acesso/arma) e `CanTargetTile`/`TargetTiles` (execução elegível). Faísca já usava alcance próprio 1–3 antes desta correção; o overlay anterior mostrava apenas unidades inimigas válidas. Agora seu mínimo, máximo, desnível e LoS são parâmetros explícitos da habilidade. Cura mantém 30 HP e Manhattan 0–3, sem altura/LoS. Execuções inválidas continuam sem mutação e os casts vazios de Faísca seguem a ordem ofensiva de facing/CT. **258 casos Core passaram, 0 falhas**, por runner externo NUnit/.NET 8, mais round-trip de snapshot v2 via System.Text.Json. Compilação externa Core/Presentation: 0 erros, avisos anteriores CS0618/CS1701. Testes puros de Presentation: 12 passaram e a mesma divergência preexistente de DirectionMapping falhou. Não equivale a execução visual/PlayMode. Relatório e checklist em [MVP_5B_TARGETING_UX.md](MVP_5B_TARGETING_UX.md).

**PlayMode pendente:** abrir Playtest_Passagem, que já contém os quatro fixtures (Proving não tem Soldier aliado). Com todos em HP cheio, Ally/C deve mostrar área sem alvos válidos; clique inválido não gasta ação. Depois ferir um aliado, conferir Cura em si/aliado, cap de HP e ausência de Hit/ataque. Soldier/G: testar distâncias 1/2/3/4, altura/parede, aliado, inimigo e vazio; fogo amigo pode derrotar unidade-chave e causar derrota. Conferir 20 de dano ou gasto único sem dano no vazio, sem espada. Archer/T: comparar F/T, mínimo 2, bônus de altura/LoS, dano/acerto/crit, flecha no vazio e um gasto. Repetir as duas ordens e só ação, Cura após movimento com direção manual, consulta com ação usada, retorno à escolha final, cancelar/inspecionar/reabrir, IA básica, fila, objetivos, Console e F5/F9 inativos. UI, corrotinas e entrada real não foram verificadas nesta correção.

---

## 3.1C MVP 5C — área e modificadores temporários (2026-10-14)

Parâmetros provisórios. A geometria e a consulta corrigidas no 5B permanecem: comandos pertencem aos fixtures, área independe de feridos/inimigos/ação livre e execução revalida o Core. Acesso adicional apenas ao time0/nome exato: Archer recebe Chuva Curta/V além de Tiro/T; Ally recebe Proteção/P além de Cura/C; Soldier recebe Gelo Menor/I além de Faísca/G. Hero mantém somente Corte/H. Nenhum Job/aprendizado foi implementado; regra v2.1 permanece por talentos futuros.

| ID | Implementação |
|---|---|
| `archer.short_volley` | Exige arco; valida o centro pelo alcance mínimo/máximo, bônus de altura e LoS da arma. Qualquer centro geométrico é válido, inclusive ocupado por aliado/vazio. Cruz Manhattan raio1 recortada ao mapa; dano só em inimigos vivos. Não exige novo alcance/LoS por vítima. Cada inimigo é resolvido uma vez pelo Combat existente com modificador 65% antes da defesa; acerto, crítico, flanco e altura continuam por vítima. Uma ação pelo cast inteiro, inclusive área sem inimigos; direção final mira o centro. |
| `acolyte.protection` | Si/aliado vivo a Manhattan 0–3, sem requisito de ferimento/arma/altura/LoS. +3 Defesa efetiva imediatamente, sem alterar a base ou HP. Consome uma ação de suporte, sem mudar/travar facing. Status `status.protection`; refresh sem somar. |
| `mage.minor_ice` | Inimigo vivo a Manhattan 1–3, desnível≤3 e LoS como Faísca, independente de arma. 12 dano mágico direto, sem modificadores físicos/acerto/crítico; sobrevivente recebe `status.chilled`: Move efetivo−1, mínimo1. Rejeita si/aliado/vazio. Uma ação ofensiva; morte limpa status e não aplica novo. Refresh não soma a penalidade. |

`TemporaryStatuses` guarda definição estável, fonte, alvo, duração e flag de turno corrente; `TurnManager.EndTurn` centraliza a contagem e o evento de expiração. Cada efeito dura as próximas **duas ativações completas** do alvo, expirando ao fim da segunda. Aplicação/refresh no alvo já ativo ignora o encerramento corrente, mantendo duas ativações futuras. Outros turnos, preview de fila, cancelamento e snapshots não diminuem a duração. Dano recebido antes/durante essas ativações usa Defesa efetiva. Morte do alvo limpa seus status; efeitos já aplicados a outros alvos não dependem da sobrevivência da fonte. Fim de batalha/reinício/saída limpam modificadores.

Base Defense/Movement ficam intactos. `EffectiveDefense` alimenta Combat; `EffectiveMovement` alimenta o overload de Pathfinder por Unit, highlights, validação real de caminho e IA. `MovementRules.TryMove` verifica adjacência/terreno/orçamento atual/ocupação e move+consome orçamento atomicamente antes da animação. Efeito posterior não interrompe retroativamente movimento já comprometido nem devolve o recurso; futuros cálculos usam o modificador. Undo autorizado devolve a flag de movimento, preservando o status. CT/facing/ordem ofensiva e suporte anteriores mantidos.

Presentation mostra alcance cinza, centros válidos, cruz amarela e marcadores menores das vítimas da Chuva; prévia física individual sem execução. Cast usa um disparo para o centro e impactos/números individuais, sem repetir ação. Proteção usa brilho/texto de aplicação/refresh, sem Hit; Gelo usa dano azul e texto de Move separados, sem espada. Info/inspeção mostram base e valor efetivo, status e ativações restantes; expiração gera histórico/texto. UI/entrada/corrotinas ainda precisam de revisão manual.

Snapshots internos passam deliberadamente a **v3**, serializando IDs de status, fonte por índice do roster, duração e skip-current. Restore aceita v2 sem status (mantém flags/CT/facing) e v3; rejeita IDs/duração/fonte duplicados ou inválidos para não perder silenciosamente o efeito. Captura guarda atributos-base, não soma modificadores novamente. Snapshot v3 é rejeitado por runtimes anteriores; fixture continua reaplicada após restore, sem persistência de talentos. F5/F9/save livre seguem inativos e checkpoints condicionais continuam futuros.

**Validação:** checkpoints A/B/C/D: **269/279/291/308 casos Core PASS, 0 FAIL** no runner externo NUnit/.NET8. Round-trip JSON externo e restauração v3 com fonte/duração/skip e leitura v2 passaram. Core/Presentation e todos os testes compilados externamente com refs Unity, zero erros; avisos anteriores CS0618/CS1701. Tests puros Presentation: 12 PASS e 1 FAIL direcional preexistente, sem mudança de UnitView. JsonUtility real, Unity Test Runner, Console/entrada/feedback visuais: não executados. Checklist em [MVP_5C_ABILITY_BATCH_02.md](MVP_5C_ABILITY_BATCH_02.md).

## 3.1D MVP 5C.1 — tile apontado, menu hierárquico e direção final (2026-10-18)

Escopo: legibilidade do tile sob o cursor, hierarquia do menu de comandos e correção da direção final. Nenhuma habilidade, Job, talento, arma, mapa, fórmula, snapshot (v2/v3) ou regra das seções 3.1A–3.1C foi alterada.

**Destaque do tile apontado.** Durante a mira, o tile sob o ponteiro recebe um **quadro fino** (4 barras nas bordas do tile, sem preencher a face, na peça de hover já existente `MapView.ShowHover`), colorido pela classificação do Core (`TargetingPreview.Classify`): **verde** (`Palette.HoverValid`) = o mesmo teste que autoriza a execução aceita este tile; **laranja** (`Palette.HoverInvalid`) = dentro do alcance geométrico, mas sem alvo elegível; **branco** (`Palette.HoverNeutral`) = neutro (movimento, escolha de direção, fora de alcance). O quadro segue o tile concreto apontado, inclusive em plataformas elevadas (a posição vem do topo do tile), e é fino o bastante para não cobrir terreno nem esconder a unidade ali parada. Não há segundo motor de mira: a autoridade é do Core (`Combat.CanTargetTile`, `Abilities.CanReachTile`/`CanTargetTile`), e o destaque **nunca** autoriza execução — apontar/clicar em tile laranja ou fora de alcance continua sem efeito. Alvo único e área continuam distintos (`TargetTiles` × `GeometricTiles`/`AreaTiles`), e o alcance cinza continua visível mesmo sem nenhum alvo elegível agora (ex.: Cura com todos os aliados em HP cheio). Cancelar a mira, trocar de habilidade, voltar à inspeção, novo turno e fim de batalha limpam o quadro junto com alcance/caminho/área. O cache do tile apontado também é zerado na limpeza: mantê-lo fazia o retorno antecipado de `UpdateHover` impedir o redesenho do **mesmo** tile apontado — essa era a causa do destaque que "sumia" e ficava inconsistente entre ataque básico e habilidades (corrigido em `BattleSandbox.ClearOverlays`, com a política pura `TargetingOverlays.HoverChanged`).

**Menu hierárquico.** A aba Ação passa a ser uma árvore montada no Core por `ActionMenu.Build`, a partir dos dados reais de acesso/turno (sem nomes ou posições fixas):

| Página | Entradas |
|---|---|
| Principal | **Mover [M]**, **Ações >** e **Esperar [Espaço]** |
| Ações | **Atacar [F]**, **Habilidades >** |
| Habilidades | habilidades **possuídas** pela unidade, na ordem do catálogo |

- Disponibilidade vem do turno: Mover desabilita com o motivo "Movimento usado"; Atacar e as habilidades, com "Ação usada"; habilidade possuída com arma incompatível fica desabilitada com "Arma incompatível". O motivo aparece no rótulo e no tooltip. Botões desabilitados não iniciam a mira; atalhos de habilidades possuídas ainda permitem consultar geometria sem executar após gastar a ação. Arma incompatível mantém a entrada visível, mas não produz geometria executável. Os tooltips de habilidades habilitadas preservam as regras de alcance/alvos.
- Habilidade possuída **nunca some** por não haver alvo válido agora (ex.: Cura sem ninguém ferido; ver §3.1B). Habilidade **não possuída não aparece na lista** e o Core segue rejeitando atalho/ID (`HasAccess`/`CanSelect`/`TryExecute`).
- Navegação: **Ações >** / **Habilidades >** entram no nível seguinte; **Voltar** (botão ou Esc) sobe um nível (Habilidades → Ações → Principal), e só do Principal vai para a inspeção livre. Cancelar a mira retorna ao submenu que a lançou (ataque básico → Ações; habilidade → Habilidades) e a página aberta é preservada ao recolher/reabrir o painel; a direção pendente continua sendo retomada, sem encerrar o turno.
- **Voltar** (navegação) e **Backspace** (desfazer movimento) são coisas diferentes: desfazer continua disponível apenas antes de agir e devolve tile, direção e orçamento de movimento do início do turno — desde o MVP 5C.2 **sem botão no menu**, só pelo atalho (§3.1E).
- Atalhos **M/F/Espaço/H/C/G/T/V/P/I** continuam como acesso rápido e entram pela mesma validação e mira do Core. Percorrer, recolher ou reabrir o menu não gasta ação, não altera CT e não encerra turno; pausa/Esc e o turno da IA seguem como antes.

**Direção final — correção (substitui a regra "Attack Only").** O critério deixa de ser "a última coisa feita foi uma ação ofensiva" e passa a ser **"a unidade se moveu E a última coisa feita foi uma ação ofensiva"** — `TurnManager.FacingLocked = _facingLockedByOffensiveAct && HasMoved`, com o flag ofensivo limpo por `RegisterMove`/novo turno e restaurado pelo save. Consequências verificadas:

| Combinação | Direção final |
|---|---|
| Mover → Atacar (básico, Corte Pesado, Tiro Mirado, Faísca, Gelo Menor, Chuva Curta) | **Travada** no alvo (ou no centro da área); encerra sozinho após o feedback, sem escolha manual |
| Atacar → Mover | Escolha **manual** depois do movimento; terminar de mover **não** pula a escolha |
| **Atacar → Esperar sem ter movido** | Escolha **manual** (correção principal: antes encerrava mantendo a direção do golpe) |
| Só mover → Esperar | Escolha manual |
| Só esperar | Escolha manual |
| Cura e Proteção (suporte), em qualquer ordem | Escolha manual; suporte nunca trava |

A escolha de direção **não consome ação** nem altera a fórmula de CT (`max(0, 60 − 20 se moveu − 40 se agiu)`); ela é validada contra o turno corrente (confirmação repetida ou atrasada é rejeitada) e encerra o turno uma única vez, sem duplicar ação, animação ou resolução de dano. Erro e tile vazio válido seguem as mesmas regras; quando ambos os recursos já foram usados e a direção está travada, o turno encerra sozinho. A IA continua encerrando automaticamente, sem prompt manual.

**Validação (2026-10-18):** Unity Test Runner em batch mode, plataforma EditMode, em cópia isolada do projeto (o Editor do projeto real permanecia aberto): **362 testes, 361 PASS, 1 FAIL preexistente** — `DirectionMappingTests.Index_DerivesFromRealYaw_SurvivesFreeCamera` (empate unitYaw=135/cameraYaw=45: espera 1, retorna 2), divergência já registrada nos lotes de MVP 5B/5C, com `UnitView` e o teste intactos e fora do escopo. Cobertura nova no que é automatizável sem rendering/input reais: `Assets/Tests/EditMode/Mvp51HoverMenuFacingTests.cs` (tile apontado 1–7, menu 8–16, direção 17–28); testes de direção existentes atualizados (`TurnManagerTests`, `AbilityTests`, `AbilityBatch02Tests`).

**Revisão técnica 5C.1 (2026-10-18):** corrigidos o Voltar real entre páginas (o helper de pai não era chamado), saída da mira ao abrir outra página, autorização do preview básico, hover recriado em inspeção/comandos e área da Chuva Curta redesenhada após resultado final. Tooltips voltam a mostrar regras de alvo/alcance; Desfazer fica na raiz. Nova execução Unity EditMode: **370 casos, 369 PASS, 1 FAIL direcional preexistente**; 308 casos Core e os 49 de `Mvp51HoverMenuFacingTests` passaram. Os oito casos adicionais incluem navegação e conclusão reais de BattleSandbox, CT/direção/entrada repetida e superfície de tiles. Fontes executadas conferidas por hash com o workspace. Matriz dos 28 requisitos, ajustes e limites em [MVP_5C_1_TECHNICAL_REVIEW.md](MVP_5C_1_TECHNICAL_REVIEW.md). Este resultado substitui a contagem de 362 acima para o estado revisado; não constitui validação visual de PlayMode.

**PlayMode pendente (não verificado):** aparência real do quadro verde/laranja/branco sobre unidades, terreno alto e tiles marcados; raycast do ponteiro e ausência de marcadores antigos após cancelar; navegação com mouse/teclado pela árvore Principal/Ações/Habilidades, rótulo contextual de Voltar, motivos nos itens desabilitados e legibilidade do menu em batalhas grandes (escopo do Estágio 12 / 12.11).

## 3.1E MVP 5C.2 — retorno automático ao menu principal e desfazer só pelo Backspace (2026-10-18)

Escopo: navegação da Presentation depois de uma ação/movimento **executados** e remoção do botão visível de desfazer movimento. Nenhuma habilidade, Job, talento, arma, mapa, fórmula, snapshot (v2/v3), orçamento de movimento, ocupação, animação ou regra de direção final/CT foi alterada; o **recurso** de desfazer movimento do Core continua igual.

**Causa raiz.** `BattleSandbox.AfterAction` reabria os comandos sem resetar `_menuPage`: o submenu que lançou a ação (Ações/Habilidades) continuava aberto depois de atacar/curar, e o jogador precisava subir um nível à mão para reencontrar Mover/Esperar — fricção de navegação, não de regra.

**Retorno automático.** Ao terminar a rotina de uma ação ou movimento **confirmados pelo Core**, a Presentation volta à página **Principal** (`_menuPage = Main`) quando o turno do jogador continua; sem escolhas restantes o fluxo segue como antes (direção final pendente ou fim do turno):

- Vale para ataque básico, Corte Pesado, Tiro Mirado, Chuva Curta, Cura, Proteção, Faísca e Gelo Menor, e para qualquer ação futura que use o mesmo ciclo de comando (`AttackRoutine`/`AttackEmptyRoutine`/`VolleyRoutine`/`MoveActive` + `FinishAction`/`AfterActionFor`).
- **Erro (miss)** e conjuração válida em **tile vazio** contam como execução: a ação foi gasta e o menu volta ao Principal.
- **Não** volta ao Principal em: cancelamento da mira (volta ao submenu que a lançou), tile inválido, habilidade não autorizada, recusa do Core, prévia sem execução e execução que não gastou a ação. A mira e o menu continuam onde estavam, com o aviso "Execução recusada: nenhuma ação foi gasta." quando a rotina foi tentada sem nada confirmado.
- A ordem das ações continua decidindo a direção final: com direção pendente ela tem prioridade sobre o menu (a página, ainda assim, já é a Principal); com a direção travada (moveu e atacou) o turno encerra sozinho, como antes. Nada é reaberto durante animação (`_busy`), no turno da IA (`AfterAction` ignora unidade que não é do time do jogador) nem para uma unidade que já saiu do turno (`AfterActionFor` descarta callback atrasado). Com a batalha decidida (vitória/derrota) os comandos também não reabrem.
- O MENU PRINCIPAL reaberto reflete o que sobrou: Mover continua habilitado e Atacar/habilidades aparecem com "Ação usada" quando a ação foi gasta, e vice-versa depois de só mover.

**Desfazer movimento sem botão.** O item **Desfazer movimento [Backspace]** saiu do MENU PRINCIPAL e **não** foi recriado em nenhum submenu: desfazer movimento voltou a ser **exclusivamente** o atalho Backspace (`TurnManager.CanUndoMove`/`UndoMove`), disponível só antes de agir, devolvendo tile, direção e orçamento de movimento do início do turno. Tentativa inválida (já agiu, nada a desfazer, tile inicial ocupado) não altera estado, e o **Backspace** continua distinto de **Voltar/Esc** (navegação). A aba Sistema e a barra de dica mostram apenas uma linha passiva de ajuda ("Desfazer movimento: Backspace, só antes de agir.") quando o desfazer está disponível — não é comando clicável.

**Validação (2026-10-18):** Unity Test Runner em batch mode, plataforma EditMode, em cópia isolada do projeto (o Editor do projeto real permanecia aberto): **398 casos, 397 PASS, 1 FAIL preexistente** — o mesmo `DirectionMappingTests.Index_DerivesFromRealYaw_SurvivesFreeCamera` (empate unitYaw=135/cameraYaw=45: espera 1, retorna 2) já registrado no MVP 5C.1 e fora do escopo, com `UnitView` e o teste intactos; zero erros de compilação. O baseline revisado do 5C.1 era 370 casos (369 PASS); os **28 casos novos** de `Assets/Tests/EditMode/Mvp52AutoMenuReturnTests.cs` passaram **28/28**, cobrindo retorno automático nas oito ações (1–8), miss e conjuração válida em tile vazio (9–10), recusa/cancelamento/prévia sem navegação (11–13), disponibilidade do menu reaberto e ausência de segunda execução (14–15), movimento, desfazer por atalho e ausência do botão (16–23) e transições de turno/CT/IA/vitória-derrota (24–28). Os testes ativam as entradas reais montadas pelo Core (`ActionMenu.Build`) e dirigem as corrotinas do próprio `BattleSandbox`, com a guarda de reentrada exercitada pelo mesmo `TryAttack` do clique; rendering, raycast e entrada física continuam fora do alcance do EditMode.

**PlayMode pendente (não verificado):** o clique real do mouse disparando ataque/movimento, o desenho do IMGUI confirmando a **ausência física** do botão, a tecla Backspace física e a troca de menu só depois de a animação terminar.

## 3.2 Turnos (CT)

- Estilo FFT: cada unidade tem **CT** (começa em 0) e **Velocidade**. A cada tick todas somam a Velocidade ao CT; quem chega a **100** joga. Se várias estão prontas, joga a de maior CT (empate: a que vem antes na lista).
- No turno, a unidade tem **1 movimento** e **1 ação** (ataque ou habilidade), em qualquer ordem, e pode encerrar o turno a qualquer momento.
- **Direção final (MVP 5A.2, corrigida no MVP 5C.1 — §3.1D):** Mover → Atacar trava a direção para o alvo e encerra após o feedback; **toda outra combinação abre a escolha manual e aguarda confirmação** — Atacar → Mover (depois do movimento), **Atacar → Esperar**, Só atacar, Só mover e Só esperar. Atacar não encerra automaticamente enquanto movimento está livre. A direção manual confirmada prevalece sobre o último passo. **Substitui** a regra anterior de travar a direção após qualquer ataque e a proposta de escolha manual após todo ataque; o MVP 5C.1 corrige o caso **Atacar → Esperar sem ter movido**, que antes encerrava mantendo a direção do golpe.
- Quando ambos os recursos foram usados e a direção está destravada, a escolha abre sozinha. Cancelar uma escolha antecipada só retorna aos recursos ainda livres; após Atacar → Mover, Esc abre pausa e a confirmação continua obrigatória. Recolher/reabrir o painel não devolve recursos. Confirmação manual valida o turno esperado e encerra uma única vez. IA continua encerrando automaticamente.
- **CT ao fim do turno:** `max(0, 60 − 20 se moveu − 40 se agiu)`. Quem só espera volta rápido (60); quem move e age recomeça do zero.
- A fila mostra os próximos 8 turnos, supondo que cada unidade mova e aja no turno dela.
- Ainda não há lentidão/pressa, nem ações com tempo de conjuração.

**Validação MVP 5A.2 (2026-10-12):** 193 casos Core passaram (0 falhas) no runner externo .NET 8 por reflexão NUnit; Core/Presentation compilados com Roslyn e referências do projeto, avisos anteriores CS0618/CS1701. Cobertura inclui as duas ordens para básico/Corte Pesado e erros, só ataque, só mover/esperar, caminho equivalente de ataque vazio, confirmação repetida/inválida, orçamento e CT, save v2 nas duas ordens e legado, encerramento automático da IA. Não equivale ao Unity Test Runner; entrada real, corrotinas, animações e Console aguardam PlayMode.

**Checklist PlayMode MVP 5A.2 (pendente do criador):** usar batalha que não termine com o golpe; testar com F e H: (1) mover e atacar — encerrar após feedback virado para o alvo, sem escolha; (2) atacar e mover — aguardar escolha, confirmar direção diferente do último passo, encerrar uma vez; (3) atacar e Espaço — manter direção do ataque; (4) só mover e Espaço e (5) só Espaço — escolher direção. Repetir erros e ataque básico contra vazio válido nas duas ordens. Durante escolha antecipada, Esc deve retornar apenas aos recursos livres; depois de atacar e mover, Esc pausa sem devolver recursos. Recolher/reabrir não altera flags nem confirma alvo. F5/F9 foram removidos no MVP 5A.4; regressão de snapshots permanece interna. Conferir IA sem prompts, CT, direção visual após confirmação, vitória/derrota e ausência de novos erros no Console.

---

## 3.3 IA mínima

- O jogador controla o **time 0**; todos os outros times são controlados pela IA. Cada turno da IA tem uma pequena pausa para dar para acompanhar.
- No turno, a IA olha todos os tiles onde poderia terminar o movimento e todos os inimigos que poderia atingir de lá:
  - **Se pode atacar:** escolhe a opção de maior dano esperado (`chance de acerto × dano médio`, contando ângulo e crítico, então prefere flanco e costas). Abater o alvo vale muito mais. Em empate, o caminho mais curto. Move, ataca e termina virada para o alvo. Arqueiros se posicionam a 2 a 6 tiles (mais longe em terreno alto) com linha de visão.
  - **Se não pode:** avança até o tile alcançável mais próximo do inimigo mais próximo (distância real de caminho, contornando água e paredes) e termina virada para ele.
- Ainda não considera risco, cura, aliados feridos nem objetivos.
- Em batalhas grandes, o cálculo de "para onde avançar" só olha os **8 inimigos mais próximos** em linha reta.
- **Depuração:** com o overlay de desempenho ligado (F3), aparece a decisão da IA no turno mais recente: resumo do motivo, tempo de cálculo e as melhores opções de ataque avaliadas (alvo, tile, pontuação e custo). O comportamento fica atrás da interface `IAiBehavior`, para doutrinas diferentes entrarem depois.

## 3.4 Objetivos de vitória e derrota

- Configurados por mapa (`MapData`). A **derrota** vale primeiro se as duas condições acontecerem juntas.

| Vitória | Regra |
|---|---|
| `DefeatAllEnemies` | Derrotar todos os inimigos |
| `DefeatKeyEnemies` | Derrotar as unidades-chave inimigas (sem nenhuma marcada, vale todos) |

| Derrota | Regra |
|---|---|
| `AllPlayerUnitsDown` | Todas as unidades do jogador derrotadas |
| `KeyPlayerUnitDown` | Todas as unidades-chave do jogador derrotadas (sem nenhuma marcada, vale todas) |

- Mapa de teste: vencer derrotando todos os inimigos; perder se o Hero (unidade-chave) cair.
- Ao terminar, aparece VITÓRIA ou DERROTA; **R** reinicia a batalha; Esc abre pausa.

## 3.5 Política de save em batalha — MVP 5A.4

- **Save/load manual livre desabilitado no gameplay normal.** F5/F9 não executam saves nem loads; não há Salvar/Carregar na aba Sistema ou na pausa, Continuar save no menu principal ou load na tela de resultado. Continuar na pausa apenas retoma o jogo pausado.
- Não há checkpoints implementados. Batalhas específicas poderão permitir checkpoints mediante condições definidas pelo criador futuramente; não é uma proibição permanente de salvar durante batalhas.
- `BattleSave.Capture/Restore`, `BattleSnapshot` v2 e validação permanecem como infraestrutura interna. Guardam unidades inclusive derrotadas, turno, recursos, CT, direção, início do movimento e histórico. Terreno vem do mapa. IDs da fixture continuam reaplicados pelo carregador interno; talentos persistentes não estão implementados.
- As rotinas privadas de arquivo JSON do sandbox foram preservadas, sem ligação com comandos/teclas/UI normal. Saves legados em `Application.persistentDataPath/battle_save.json` não são apagados, migrados ou oferecidos ao jogador. Versão 2 continua suportada; versões desconhecidas e posições inválidas continuam rejeitadas antes de trocar a cena. Saves antigos conservam `facingLocked` gravado, sem reconstruir ordem de ações inexistente.
- Esta política substitui os controles irrestritos F5/F9 anteriores. Checkpoints, retomada e suspensão de batalhas longas aguardam design (ROADMAP 5.7).

---

## 4. Queda e knockback

- **Queda voluntária não existe**: uma descida maior que `JumpDown` simplesmente bloqueia o passo.
- **Knockback** (empurrão) move a unidade tile a tile em uma direção ortogonal, até a distância pedida. Ele para (colisão) quando o próximo tile:
  - está fora do mapa, é água ou está ocupado por qualquer unidade;
  - é mais alto que o atual em mais de 1 (`MaxRise`).
- Descer é permitido a qualquer altura. Cada degrau descido soma queda insegura de `(descida − 2)` quando a descida passa de 2 (`SafeDrop`).
- **Dano de queda:** `10% do HP máximo × queda insegura` (arredondado para cima). A regra existe, mas o sandbox só registra o valor no Console, não aplica ao HP.
- Ainda não existe dano de colisão nem empurrão causado por habilidades.

## 5. Câmera e controles (sandbox)

A câmera segue o padrão de Triangle Strategy: ângulo diagonal fixo, giro em passos de 90° e três níveis de zoom (mais perto = mais baixa). No início de cada turno ela **segue automaticamente a unidade da vez**, inclusive durante o movimento e acompanhando a altura. Mover a câmera com WASD desprende o foco até o próximo turno.

**Menu de comandos (MVP 5A.3):** inicia sem mira. Mover/M, Atacar/F e Corte Pesado/H entram na mira correspondente. **Voltar: comandos** ou Esc cancela a mira, limpa habilidade/destaques/prévia e retorna ao menu — desde o MVP 5C.1, ao submenu que lançou a mira, não necessariamente ao principal (§3.1D) — sem desfazer movimento executado. **Voltar / Inspecionar** recolhe comandos e entra em um modo separado de inspeção livre: sem alcance de movimento/ataque nem caminho, cliques no mapa não executam ações. Câmera e inspeção/fixação de aliados/inimigos permanecem disponíveis. **Abrir comandos** reabre o painel; M/F/H saem explicitamente da inspeção para a mira disponível. **Backspace** continua sendo a ação separada de desfazer movimento, permitida apenas antes de agir (desde o MVP 5C.2 sem item clicável no menu — §3.1E). Nenhuma navegação altera CT ou recursos.

Esc na inspeção abre pausa. Na escolha final com recursos livres, Esc volta aos comandos; com ambos gastos, abre pausa. Recolher durante direção obrigatória permite inspecionar, mas reabrir retorna à escolha pendente, sem encerrar o turno. Após execução com recursos restantes, volta ao **MENU PRINCIPAL** da árvore de comandos (MVP 5C.2 — §3.1E); sem recursos segue MVP 5A.2. Novo turno e load limpam navegação temporária e mostram comandos ou direção obrigatória conforme o estado restaurado. Pausa mantém navegação; IA não recebe comandos táticos habilitados. Esse fluxo substitui o MVP 5A.1 que apenas ocultava o painel mantendo a mira.

**Menu hierárquico (MVP 5C.1 — §3.1D):** a aba Ação passou a ter níveis — **Principal** (Mover, Ações >, Esperar) → **Ações** (Atacar, Habilidades >) → **Habilidades** (habilidades possuídas) — montados pelo Core a partir do acesso e do turno reais. **Voltar** sobe um nível por vez (e só do Principal vai para a inspeção livre); cancelar a mira volta ao submenu que a lançou; a página aberta sobrevive ao recolher/reabrir. O antigo item "Voltar (desfazer movimento)" virou o comando separado **Desfazer movimento [Backspace]** (MVP 5C.1) e depois ficou **só no atalho**, sem botão em nenhuma página (MVP 5C.2 — §3.1E).

| Aba | Conteúdo |
|---|---|
| Ação | Hierárquica: Principal (Mover, Ações >, Esperar) → Ações (Atacar, Habilidades >) → Habilidades (habilidades possuídas, motivo quando desabilitadas); desfazer movimento só pelo Backspace, sem botão (§3.1E) |
| Info | Arma, Força, Defesa, Evasão, Velocidade, CT, Move/Jump da unidade da vez |
| Sistema | Histórico e Pausa |

**Painel de status (inspeção):** qualquer unidade pode ser consultada a qualquer momento, inclusive durante o turno da IA e sendo inimiga. Passar o mouse sobre ela abre um painel abaixo do menu com nome, HP, time, se é unidade-chave, arma (poder e alcance), Força, Defesa, Evasão, Velocidade, CT, Move, Jump e a altura do tile. O botão direito **fixa** a unidade (marcada com um quadrado ciano no mapa) para o painel continuar aberto ao mover o mouse; clicar de novo nela ou num tile vazio solta. A unidade fixada some do painel se for derrotada.

A fila no canto superior direito possui **recolhido** (unidade atual), **compacto** (6 ativações) e **expandido** (18 ativações, scroll, time, CT atual e velocidade). Recolher/Expandir alternam os modos. Aliado/Inimigo é identificado por texto. A sequência é rotulada **projetada** e usa `TurnManager.PreviewOrder`, que assume mover e agir; o CT listado é o atual, não o de cada ativação futura. A preferência usa PlayerPrefs em GameSettings e é salva ao alterar. O último aviso e a dica do que está sob o mouse (inclusive a prévia do ataque) aparecem numa barra fina na parte de baixo, que some quando não há texto.

| Entrada | Efeito |
|---|---|
| Clique esquerdo em tile azul (modo mover) | Move a unidade da vez |
| M / F (ou botões) | Modo mover / modo atacar |
| Espaço (ou botão Esperar) | Encerra o turno: abre a escolha manual da direção, exceto quando ela já está resolvida (moveu e atacou) |
| Backspace (sem botão no menu) | Desfaz o movimento, se ainda não agiu |
| Mouse sobre uma unidade | Mostra o painel de status dela (qualquer unidade, em qualquer turno) |
| Botão direito em uma unidade | Fixa o painel nela; de novo na mesma, ou em tile vazio, solta |
| Mouse + clique (escolha de direção) | Vira e confirma; Esc volta se há recursos livres, senão pausa |
| R (fim da batalha) | Reinicia a batalha |
| F5 / F9 | Sem função de save/load no gameplay normal |
| Esc | Mira → submenu que a lançou; submenu → página pai (Habilidades → Ações → Principal); Principal → inspeção; inspeção → pausa; direção volta se há recursos livres, senão pausa |
| L | Abre/fecha o histórico da batalha |
| F3 | Liga/desliga o overlay de desempenho e da IA |
| Clique em inimigo em tile vermelho (modo atacar) | Ataca; passar o mouse mostra ângulo, acerto, dano e crítico |
| WASD | Move a câmera (desprende o foco automático) |
| Q / E | Gira a câmera 90° |
| Scroll | Zoom em 3 níveis |
| 1 / 2 | Diminui / aumenta o `Jump` |
| 3 / 4 | Diminui / aumenta o `Move` |
| K | Empurra a unidade da vez 3 tiles para +X (teste de knockback; resultado no Console) |

**Cores no sandbox:** azul = alcance de movimento, vermelho = alcance de ataque (só tiles que a arma realmente alcança, já contando desnível e linha de visão), amarelo = caminho, e o tile sob o mouse leva um **quadro fino**: verde = alvo válido, laranja = dentro do alcance sem alvo elegível, branco = neutro (§3.1D). Herói (unidade-chave) amarelo, aliados azuis, inimigos vermelhos. O cubo branco na cápsula indica a frente da unidade. O nome e o HP aparecem sobre cada unidade (`>` marca a da vez). A fila de turnos fica no canto superior direito.

Para testar os ângulos: o inimigo (espada) começa olhando para o herói, então o primeiro golpe é de frente. Dando a volta pela esquerda (passando pelo aliado) até o tile atrás dele, o golpe é de costas. Ao encerrar o turno, a direção escolhida define de onde a unidade está vulnerável.

**Mapa de teste:** Hero, Ally (espada) e Archer (arco) contra Enemy (espada), Orc (machado) e Bowman (arco). O Bowman fica numa plataforma de altura 4 isolada por penhasco no canto superior direito: o corpo a corpo não o alcança (desnível), só o Archer, com linha de visão. Um muro (altura 9) perto do lago bloqueia tiros.

## 5.1 Editor de mapas

**Tactics > Map Editor** abre um editor visual do `MapData`. Ele edita o mesmo texto de layout, então os assets existentes continuam valendo.

- **Barra única e compacta:** campo do mapa, ferramentas (`+`, `−`, `H`, Chão, Lama, Água, Unid.), slider de tamanho das células e botões que abrem janelas pequenas.
- **Janelas sob demanda:** *Mapa* (largura e altura, máximo 64×64), *Unidades* (lista e ficha da unidade selecionada: nome, time, arma, velocidade, direção, chave) e *Objetivos* (vitória e derrota).
- **Grid:** clique esquerdo aplica a ferramenta e arrastar pinta vários tiles; clique direito inverte (desce/sobe) ou, na ferramenta de unidade, remove. Cada célula mostra a altura (`m` = lama, `~` = água). Unidades aparecem com a inicial do nome e uma faixa branca na frente; unidade sobre água fica magenta.
- Desfazer (Ctrl+Z) funciona em tudo. **Salvar** grava o asset.

## 5.2 Menus e opções

- **Menu principal:** aparece ao abrir o jogo. Lista todos os mapas de `Resources/Maps` (um botão "Jogar" por mapa, então um mapa novo feito no editor já aparece), Opções e Sair.
- **Pausa (Esc):** Continuar (retomar pausa), Opções, Reiniciar batalha e Menu principal, com o resumo das teclas. O jogo congela enquanto o menu está aberto.
- **Opções** (guardadas no computador e valem nas próximas sessões):

| Opção | Valores |
|---|---|
| Velocidade das animações | 1x, 2x, 4x, instantâneo (vale para passos, golpes, efeitos e pausas da IA) |
| Volume geral / dos efeitos | 0% a 100% |
| Tamanho da interface | 100%, 125%, 150%, 200% |
| Paleta para daltonismo | Troca vermelho/azul/verde por cores seguras (azul, laranja-avermelhado, amarelo, roxo) em destaques e unidades |
| Mostrar desempenho | FPS, tempo de quadro, nº de unidades, tamanho do mapa e decisão da IA |

## 5.3 Feedback de combate (provisório, sem arte)

Animações e sons de teste que marcam cada momento do golpe e já respeitam a velocidade de animação. São substituíveis quando houver arte e áudio reais.

| Arma | Animação |
|---|---|
| Espada | Recua um pouco e avança rápido; curta |
| Machado | Levanta devagar e bate pesado; o impacto faz a câmera tremer |
| Arco | Recuo do arqueiro e flecha em arco até o alvo (mais longe = mais tempo de voo) |

- **Acerto:** o alvo brilha e é empurrado de leve; aparece o dano em número flutuante (crítico em amarelo e maior, com tremor extra).
- **Erro:** o alvo desvia para o lado; a flecha passa ao lado. Aparece "Erra".
- **Derrota:** a unidade encolhe até sumir.
- **Tile apontado:** quadro fino verde (alvo válido) / laranja (no alcance sem alvo elegível) / branco (neutro) no tile sob o mouse durante a mira — §3.1D. É provisório e substituível quando houver arte de cursor.
- **Sons:** passos, golpes de espada/machado, disparo de arco, acerto, crítico, erro, derrota, início de turno, desfazer, cliques de menu, vitória e derrota. Sem arquivos de áudio, são tons sintetizados por código. Para usar sons reais, crie um `SoundBank` (Create > Tactics > Sound Bank) em `Resources/SoundBank` e associe clipes a cada evento; o que não for preenchido continua com o som de teste.

## 5.4 Histórico e desempenho

- **Histórico (L):** janela com tudo o que aconteceu, com o número do turno (início de turno, movimentos, ataques, desfazer, saves). Guarda até 300 entradas e vai junto no save.
- **Batalhas grandes:** o pathfinding usa fila binária, a IA limita o cálculo de avanço aos inimigos mais próximos e os tiles do mapa são combinados em poucas malhas. O editor aceita mapas até 64×64.
- **Mapa de estresse:** **Tactics > Criar mapa de estresse (40x40, 60 unidades)** gera `Resources/Maps/Stress`, com dois exércitos de 30 unidades. Escolha "Jogar: Stress" no menu principal e ligue o F3 para ver FPS e tempo da IA. Os testes automáticos também medem o planejamento de um turno inteiro de 30 unidades em mapa 40×40.

## 6. Onde está no código

| Assunto | Arquivo |
|---|---|
| Grid, tiles, unidades no mapa, leitura do layout | `Assets/Scripts/Core/BattleMap.cs` |
| Unidade e armas | `Assets/Scripts/Core/Unit.cs` |
| Ordem de turnos (CT) e fila | `Assets/Scripts/Core/TurnManager.cs` |
| IA | `Assets/Scripts/Core/SimpleAi.cs` |
| Vitória e derrota | `Assets/Scripts/Core/BattleObjectives.cs` |
| Ataque, ângulo, desnível, linha de visão, acerto, crítico e dano | `Assets/Scripts/Core/Combat.cs` |
| Save/load de batalha (snapshot) | `Assets/Scripts/Core/BattleSave.cs` |
| Regras de passo, custo e pathfinding | `Assets/Scripts/Core/Movement.cs` |
| Knockback e dano de queda | `Assets/Scripts/Core/Knockback.cs` |
| Dados de mapa (ScriptableObject) | `Assets/Scripts/Presentation/MapData.cs` |
| Sandbox, entrada e destaques | `Assets/Scripts/Presentation/BattleSandbox.cs`, `MapView.cs` |
| Menu de comandos (hierarquia Principal/Ações/Habilidades) | `Assets/Scripts/Core/ActionMenu.cs` |
| Classificação do tile apontado (hover) | `Assets/Scripts/Core/TargetingPreview.cs`, `Assets/Scripts/Presentation/TargetingOverlays.cs` |
| Menus e opções | `Assets/Scripts/Presentation/GameMenus.cs`, `GameSettings.cs` |
| Animações e efeitos de combate | `Assets/Scripts/Presentation/BattleFeedback.cs`, `UnitView.cs` |
| Áudio | `Assets/Scripts/Presentation/AudioService.cs`, `SoundBank.cs` |
| Histórico da batalha | `Assets/Scripts/Core/BattleLog.cs` |
| Fila de prioridade (pathfinding) | `Assets/Scripts/Core/MinHeap.cs` |
| Câmera | `Assets/Scripts/Presentation/TacticsCamera.cs` |
| Editor de mapas | `Assets/Scripts/Editor/MapEditorWindow.cs`, `MapPopupWindow.cs`, `StressMapMenu.cs` |

`Core` é C# puro (sem `UnityEngine`); `Presentation` só desenha e lê entrada. Os testes do `Core` ficam em `Assets/Tests/EditMode` (Test Runner do Unity).

## 7. Ainda não existe

Sistema completo de Jobs/talentos e habilidades aprendidas, tempo de conjuração, categorias adicionais de arma com desnível próprio, crítico por classe/raça/passivas, altura no acerto, efeitos de terreno além da lama, status avançados/DoT/dispel/resistências (há somente os dois modificadores finitos do MVP5C), IA com doutrinas/objetivos ou uso de habilidades, save automático e vários slots, transparência de tiles que tapam a visão, unidades multi-tile e montarias. Arte/áudio de produção completa continuam pendentes.

## Visual Direction Note

Character visual direction is defined separately in `Docs/ART_DIRECTION.md`.

Gameplay-facing visual implementations should follow the approved character style anchor and subsequent production references.
### Verificação MVP 5A.3 (2026-10-12)

Core/Presentation compilados externamente com Roslyn. 196 casos Core passaram, incluindo comprimentos 1/6/18 da previsão sem mutação e regressões de Corte Pesado/direção final. Runner externo por reflexão NUnit, não Unity Test Runner. Interação IMGUI, persistência após reinício real, animações e Console ainda aguardam PlayMode.

Checklist manual pendente: Comandos → M → Esc → Comandos → Esc → Inspeção → Abrir; repetir com F/H e conferir zero overlays/caminhos na inspeção e clique sem ações. Testar câmera Q/E/WASD/zoom e inspeção/fixação de aliados e inimigos. Comparar recursos/CT antes/depois, desfazer só via Backspace/Voltar explícito, mira após M/F/H. Repetir as cinco regras MVP 5A.2, incluindo recolher durante direção obrigatória e reabrir para confirmar. Testar pausa, turnos IA/jogador, load, vitória/derrota e reinício. Alternar os três modos da fila, scroll e escala UI; reiniciar aplicação e confirmar preferência mantida. Validar mapa Stress e ausência de novos erros no Console. Sobreposição de rótulos e personalização ampla continuam no Estágio 12.

**Validação MVP 5A.4:** 196 casos Core passaram no runner externo NUnit por reflexão; Core/Presentation compilados com avisos anteriores CS0618/CS1701. Inspeção de código confirmou ausência de chamadas normais a SaveGame/LoadGame e de exclusão de arquivos. PlayMode pendente: pressionar F5/F9 em comandos/mira/inspeção/direção/pausa/resultado, conferir nenhum save/load; abrir jogo com save legado e confirmar ausência de Continuar save; testar Reiniciar/R, pausa/opções, vitória/derrota e Console. Arquivo legado deve permanecer intacto. Testes de snapshots usam Capture/Restore; também passou round-trip JSON externo com System.Text.Json (IncludeFields) após Corte Pesado, preservando versão 2, HP e ação usada. Isso não executa JsonUtility do Unity nem arquivo de batalha em disco.


**MVP 5A.5 (2026-10-13):** 205 casos Core passaram no runner externo NUnit por reflexão; Core/Presentation compilados com avisos anteriores CS0618/CS1701. Casos novos cobrem tiles vazios, consumo único/sem dano, inválidos/altura/aliado/fora do mapa, concordância destaque/validação, posse e indisponibilidade, ordem de ações/CT. Animação e menu/teclado reais aguardam PlayMode: Hero H deve destacar vazio e inimigo adjacentes; clicar vazio toca Attack/golpe sem Hit/dano/crit/kill; repetir ataque→movimento e movimento→ataque e conferir direção final. Esc/Voltar cancela sem gasto; inválidos não gastam; após agir, habilidade permanece desabilitada. Soldier/Ally/Archer não mostram H e tecla H não ativa; repetir inspeção, fila, IA e vitória/derrota. F5/F9 seguem inativos; snapshots v2 intactos.
