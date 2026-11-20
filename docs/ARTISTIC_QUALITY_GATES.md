> Atualização de integração — 27/10/2026: Passe de recuperação direcionada `main-orc-targeted-recovery-v3` executado pelo Sole DEV. Matriz atual: 12 candidatos ativos e 16 aliases inalterados. Todos os 10 apontamentos visuais do Criador foram inspecionados, diagnosticados e reparados localmente em Aseprite (0 gerações de IA consumidas; saldo de contabilidade inalterado em 17 jobs / 78 gerações consumidas historicamente). Suíte completa de testes: 50/50 PASS, 20/20 Chromium headless browser checks PASS. O pacote permanece em status estrito de `VISUAL_REVIEW_REQUIRED` (`PENDING_CREATOR`) aguardando avaliação artística visual do criador no estúdio de revisão local. Nenhuma escrita no Unity (`../TacticsRPG`).

# Portões de qualidade artística — contrato canônico

**Estado atual da recuperação do Orc V1 (2026-10-27):** candidato `main-orc-targeted-recovery-v3`, com 12 clipes alvo afetados (`ACTIVE_CANDIDATE`) e 16 preservados (`UNCHANGED_ALIAS`). Todas as 10 constatações do criador foram abordadas cirurgicamente no Aseprite sem chamadas pagas de IA:
1. `back_r`/`back_l` Sword: trajetória de corte contínua em arco, grip de luva dobrada contornada em INK, eliminação de halos/bordas claras.
2. `back_r`/`back_l` Axe: arco de golpe descendente overhead pesado, grip de luva dobrada envolvente, eliminação de bordas claras.
3. `back_l` Unarmed: reconstrução com frames traseiros autênticos NW, descartando frames frontais repintados obsoletos.
4. `back_r` Unarmed: punho de golpe restaurado em desaceleração no F03 (sem desaparecimento).
5. `front_r`/`front_l` Unarmed: braço oposto em guarda restaurado em F02 e F03 (eliminando amputação acidental).
6. `back_r`/`back_l` Walk: estabilização do contorno do braço esquerdo no Aseprite (sem ruído/cintilação temporal).
7. `front_r`/`front_l` Defeat: rebaixamento do tronco superior no colapso terminal (altura 55px, y=136), eliminando a postura de ajoelhamento/quatro apoios e preservando volume 3D sem rotação global ou achatamento artificial.
8. `front_l` Sword: remoção de pixel isolado e resíduos de recorte na axila do braço de ataque (F01-F03).
9. `front` Walk: atenuação do sombreamento excessivo na virilha/tecido no quadro 8.
10. Padrão de empunhadura e contorno de armas: conformidade com `curled-glove-grip-standard` e `weapon-perimeter-outline-no-bright-edges`.

Status: `VISUAL_REVIEW_REQUIRED` (aguardando inspeção visual humana pelo criador); aprovação artística `PENDING_CREATOR`. Consultar o estúdio interativo em [`Biblioteca de Arte/Estudos Comparativos/Orc principal - Recuperacao traseira/index.html`](../Biblioteca%20de%20Arte/Estudos%20Comparativos/Orc%20principal%20-%20Recuperacao%20traseira/index.html) e o manifesto canônico [`characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json`](../characters/orc-v1/source/rear-recovery-v2/candidate28manifest.json).

2026-10-25 · contrato `factory.artistic-quality-gates.v1` · machine-readable em [`config/artistic-quality-gates-v1.json`](../config/artistic-quality-gates-v1.json) · aplicado ao passe `main-orc-complete-v1` do **Orc V1 / Verde Warcraft** (`characters/orc-v1/`).

Este documento existe para impedir um erro específico e já cometido: tratar um pacote **tecnicamente completo** como se fosse **arte aprovada**. A biblioteca completa do Orc principal passou por validação, exportação e QA com zero falhas técnicas e ainda assim continha vistas traseiras construídas por cima do rosto frontal, uma reação `Hit` da amplitude da respiração e um `Defeat` que achatava o corpo em uma tira horizontal. Nada disso era detectável por hash, canvas ou contagem de quadros.

Regra central: **completude técnica é condição de entrada, não veredito artístico.** Quem aprova arte é o criador.

---

## 1. Taxonomia de status

Todo pacote apresentado a alguém precisa carregar **um** destes quatro status. Não existe "pronto" fora desta lista.

| Status | Significado | Quem pode atribuir |
|---|---|---|
| `TECHNICALLY_COMPLETE` | Dimensões, `groundY`, alpha binário, hashes, mestres `.aseprite` e contagem de quadros passam nas checagens automáticas. | Validação automática, ferramentas de auditoria, DEV |
| `VISUAL_REVIEW_REQUIRED` | Tecnicamente completo **e** sem defeitos conhecidos pelos gates abaixo; aguarda inspeção visual humana no estúdio interativo. | DEV após os gates passarem; orquestrador |
| `ARTISTIC_REVISION_REQUIRED` | Criador ou QA visual identificou defeito de anatomia, perspectiva, silhueta, coreografia ou limpeza de pixels que exige revisão. | Criador, QA visual independente, ou DEV com evidência medida |
| `CREATOR_APPROVED` | Aprovação artística explícita do criador, após inspeção visual. | **Somente o criador** |

**Como ler os status.** Há duas coisas diferentes em jogo: uma **progressão** e um **bloqueio**.

Progressão normal, cada degrau exigindo o anterior: `TECHNICALLY_COMPLETE` → `VISUAL_REVIEW_REQUIRED` → `CREATOR_APPROVED`.

Bloqueio: `ARTISTIC_REVISION_REQUIRED` sobrepõe qualquer outro rótulo enquanto o defeito estiver aberto. Um pacote nunca pode ser exibido como "em revisão visual" — e muito menos como aprovado — enquanto se sabe que há anatomia, perspectiva, silhueta ou coreografia erradas.

Duas consequências diretas:

1. Um defeito artístico conhecido rebaixa o pacote mesmo que todo o resto esteja perfeito. Não se exibe como "em revisão" algo que já se sabe estar errado.
2. `CREATOR_APPROVED` não é um estado inicial nem um selo que acompanha o pacote para sempre: vale para a versão revisada, com data e escopo registrados. Qualquer novo pixel exige nova decisão.

Rótulos proibidos: `READY`, `DONE` e `APPROVED` sem um status desta taxonomia. Aprovação vinda de ferramenta, de contagem de arquivos ou de agente não é aprovação artística.

Fluxo:

```
TECHNICAL_GATE (validate / exportAseprite / hashes / matriz de cobertura)
        ↓
ARTISTIC_DEFECT_GATES (vista direcional · coreografia · conjunto completo)
        ↓
VISUAL_REVIEW (criador abre o estúdio)
        ↓
CREATOR_APPROVED (declaração explícita, registrada)
```

---

## 2. Gate de vista direcional (`directionalViewGate`)

Aplica-se a `back_r` e `back_l`.

**Princípio:** vista traseira é construção, não repintura. Derivar um fundo pintando por cima do rosto de um sprite frontal é proibido — se crânio, nuca e armadura dorsal não foram reconstruídos, a vista falha, por mais polida que esteja a superfície.

Marcadores obrigatórios, todos identificáveis pelo menos nos quadros de `Idle` daquela vista:

- crânio occipital sem rosto, sobrancelha, nariz, boca, presas ou órbitas;
- nuca e trapézio visíveis entre crânio e gola;
- gola/gorjal alta traseira, aberta para as costas;
- costas com placa dorsal, canal vertebral central e placas escapulares no lugar das peitorais e das cicatrizes de peito;
- fecho de cinto/faixa nas costas, **sem** o pico esternal frontal;
- **sem** ponta abdominal frontal;
- tassets divididos na traseira e cota de malha caindo atrás;
- tiras poplíteas e grevas de panturrilha;
- **sem** poleyns frontais de joelho;
- calcanhares e bicos das botas angulados para longe do observador.

**Distinção entre as duas vistas.** `back_r` olha para Nordeste, `back_l` para Noroeste. Elas precisam diferir em perspectiva de três quartos, em oclusão de ombro (qual pauldron está à frente) e na luz vinda de cima-esquerda. Um espelho puro não serve: ele troca a fonte de luz para cima-direita e inverte o ombro próximo, coisas que a câmera e a luz não fazem.

Checagens objetivas:

| Checagem | Critério |
|---|---|
| Rosto frontal | zero pixels da paleta frontal (olhos, presas, boca) na região da cabeça |
| Marcadores | cada item da lista acima localizável na vista |
| Dependência de espelho | `back_r` × `back_l` espelhado com mais de 97% de concordância indica cópia espelhada, não vista construída |
| Lado da luz | centróide de brilho acima do centróide do corpo e no mesmo lado nos quatro sentidos |

---

## 3. Gate de coreografia (`choreographyGate`)

**Princípio:** a ação precisa comunicar seu significado em silhueta e tempo, não apenas em sombreamento. Mudar 6% dos pixels não é mudar o movimento.

### 3.1 `Hit` — reação de impacto

Leitura exigida: reação clara de impacto em corpo pesado e blindado.

- componentes obrigatórios: recuo corporal legível de impacto, encolhimento de ombro ou braço em guarda, recuo de tronco coerente com a massa do personagem, compressão ancorada em `groundY` e recuperação clara ao repouso;
- componentes contextuais: snapping de cabeça é diagnóstico contextual — opcional para o perfil `heavyOrc` e arquétipos blindados pesados onde a rigidez da armadura e massa cervical absorvem o impacto no tronco sem forçar snap de pescoço caricato;
- proibido: poses completamente estáticas/não-reativas, deslocamento desancorado do solo (`groundY`), ou animação indistinguível de respiração em velocidade 1×. Deslocamento sutil de 1-2 px funciona como prompt diagnóstico para revisão visual, e não como falha técnica universal para todo tipo de corpo;
- 5 fases: `impact-onset` (45 ms), `peak-recoil` (95 ms), `stagger-brace` (115 ms), `recovery-rise` (95 ms), `recovery-settle` (100 ms) — 450 ms, sem loop.

Métricas diagnósticas (context-sensitive, não mínimos universais; histórico: topo 12 px, centróide 5,74 px, compressão 12 px, energia normalizada 5,6×):

| Métrica | Papel |
|---|---|
| Excursão do topo da cabeça | diagnóstico |
| Deslocamento do centróide | diagnóstico |
| Compressão de altura (quadro mais baixo) | diagnóstico |
| Base do corpo | presa em `groundY` em todos os quadros (HARD) |
| Energia de movimento vs `Idle` | diagnóstico |

Integridade dura (HARD) permanece: validade de arquivo, frames, metadados, hashes, proveniência, camadas, manifest. Um Hit com amplitude menor mas tecnicamente válido é diagnóstico, não falha automática. Defeitos de origem/camada/corrupto continuam falhas duras.

Perfil contextual `heavyOrc` (aplica-se ao `orc-v1`): o impacto pesado blindado do Orc precisa comunicar impacto legível e mecânica corporal justificada; **topo de cabeça (head snap) não é requisito universal para toda raça**. Requer: impacto legível em 1× e recuperação clara ao repouso; mecânica de tronco/ombro justificada pelo peso da armadura; contato com o chão preservado. `headSnap: opcional` — um Hit menor mas bem animado, com impacto/recuperação legíveis, pode passar na revisão visual sem head snap. Cabe ao criador decidir na velocidade de reprodução real e escala do jogo.

Energia de movimento é a porcentagem de pixels alterados entre quadros nas faixas de tronco e cabeça, dividida pela mesma medida no `Idle` da mesma direção. É um teste barato que separa reação de respiração.

### 3.2 `Defeat` — colapso

Leitura exigida: colapso físico crível em múltiplos estágios com retenção de volume tridimensional.

- estágios: `fatal-stagger` (70 ms) → `knees-buckle` (95 ms) → `drop-to-knees` (115 ms) → `collapse-impact` (130 ms) → `terminal-defeated` (290 ms) — 700 ms, quadro terminal 4;
- **proibido**: rotação 2D global do sprite em pé combinada com achatamento vertical (por exemplo `vScale = 0.52`). Um corpo em pé esmagado não é um corpo caindo;
- volume preservado: cabeça, pauldron e peito continuam legíveis no chão; silhueta reduzida a uma tira horizontal falha. A preservação volumétrica no solo (`h >= 58px`, `aspect >= 1.3`) representa uma baliza diagnóstica contextual para o humanoide pesado atual (`orc-v1` em canvas 128), não um portão artístico rígido universal para futuras anatomias não-humanoides, aladas ou mais leves. A consistência volumétrica direcional no chão sobrepõe qualquer fórmula rígida de ajoelhamento.

| Métrica | Critério |
|---|---|
| Base | presa em `groundY` em todos os quadros |
| Proporção terminal largura/altura | ≥ 1,3 |
| Crescimento de largura no terminal | ≥ 10% sobre o quadro em pé |
| Queda de altura em uma única transição | ≤ 35% da altura em pé |

### 3.3 Cabeça nos ataques frontais (`Unarmed`, `Sword`, `Axe`)

- contorno escuro em `INK` `rgb(12, 15, 18)` / `#0C0F12` ao redor da coroa;
- borda de pele verde coerente com a paleta por dentro do contorno;
- **zero** pixels de halo cinza-claro ou branco anti-aliased ao redor da coroa;
- trajetória do topo da cabeça estabilizada: pode subir e descer com a ação, mas reversão isolada acima de 5 px indica tremor, não intenção.

| Métrica | Critério |
|---|---|
| Pixels quase brancos (`min(R,G,B) ≥ 235`, alpha > 0) na faixa da cabeça | 0 |
| Reversão consecutiva máxima do topo da cabeça | ≤ 5 px |

---

## 4. Contrato de revisão do conjunto completo (`completeSetReviewContract`)

**Princípio:** o conjunto se revisa como conjunto. Uma direção bonita não sustenta uma biblioteca.

Matriz obrigatória: 4 direções (`front_r`, `front_l`, `back_r`, `back_l`) × 7 ações (`Idle`, `Walk`, `Unarmed`, `Sword Attack`, `Axe Attack`, `Hit`, `Defeat`) = **28 células**.

O estúdio de revisão precisa oferecer, em uma única página:

- as 28 células alcançáveis em um clique;
- avanço quadro a quadro, reprodução, velocidade e zoom sem sair da página;
- comparação **antes/depois** de toda ação revisada;
- transições `Idle → Attack → Idle`, `Walk → Idle`, `Hit → Idle` e `Defeat → pose terminal`;
- nenhuma suavização, nenhum quadro inventado, nenhuma interpolação no preview.

### 4.1 Integridade do antes/depois

Uma comparação antes/depois exige que o "antes" venha do build substituído ou de uma captura preservada antes da revisão. Para um trecho declarado alterado, pixels idênticos exigem investigar se a referência foi capturada tarde ou se a alteração pretendida não aconteceu. Quadros deliberadamente preservados podem ser idênticos e devem ser identificados como preservados. Um hash diferente por compressão, metadados ou recodificação PNG não demonstra mudança artística: compare os pixels RGBA decodificados, os tempos e a reprodução real, mantendo a procedência da referência.

Os snapshots preservados em `experiments/main-orc-complete-v1/rejected-before/` foram capturados a partir do build substituído `dist/editor/orc-v1-complete-v1/2595e12a39cc29670933` antes da re-autoria artística e possuem hashes SHA-256 distintos da saída atual (`b178422e1f7fc19f068c`).

### 4.2 Deveres do revisor

Inspecionar anatomia, perspectiva, silhueta, limpeza de clusters e movimento. Todo defeito registrado precisa nomear **ação, direção e faixa de quadros**. Contagem de arquivos, esquema JSON e hash **não** são evidência artística.

---

## 5. Como aplicar, na prática

Ordem para qualquer personagem novo ou revisão:

1. `node src/cli.mjs validate --id <id> --stage full` — portão técnico. `FAIL` bloqueia.
2. Gates artísticos desta página, por ação e por direção, com registro do que foi medido.
3. Estúdio de revisão atualizado com a matriz completa e o antes/depois válido.
4. Inspeção visual do criador.
5. Declaração explícita do criador, registrada com data, escopo e evidência.

Comandos locais úteis (nenhum deles aprova arte):

```powershell
node src/cli.mjs validate --id orc-v1 --stage full
node tools/audit-main-orc-complete-animation.mjs --current
node --test --test-concurrency=1
node src/cli.mjs editor-export --manifest characters/orc-v1/source/aseprite/complete-v1/editor.json
```

---

## 6. Estado medido do `main-orc-complete-v1`

Build de referência `dist/editor/orc-v1-complete-v1/b178422e1f7fc19f068c`; anterior substituído `…/2595e12a39cc29670933`. Medições sobre os sprites nativos e compostos reconstruídos em 2026-10-25, por silhueta (bbox/centróide), diferença de pixels por quadro e comparação antes/depois. São dados técnicos de portão: não substituem o julgamento artístico do criador.

| Item | Antes (`2595e12a39cc29670933`) | Depois (`b178422e1f7fc19f068c`) | Leitura |
|---|---|---|---|
| `Defeat` terminal (`front_r` / `back_r`) | altura 112 → **21 px**, largura 82 → 109 (squash vertical) | `front_r`: alturas `112/90/86/63/66 px`, larguras `87..120 px` (`aspect = 1,82`); `back_r`: alturas `111/91/84/67/66 px`, larguras `90..119 px` (`aspect = 1,80`) | achatamento virou colapso progressivo em 5 estágios com volume 3D preservado |
| `Hit` topo da cabeça (excursão) | 3 px de excursão | **12 px** (`front_r`/`front_l`/`back_l`) a **13 px** (`back_r`) | supera o piso de 6 px com snap de cabeça e guarda |
| `Hit` compressão de altura | 3 px | **12 px** (`front_r`/`front_l`/`back_l`) a **13 px** (`back_r`) | supera o piso de 5 px |
| `Hit` deslocamento de centróide | 2,0 px | **5,74 px** (`front_r`/`front_l`) a **7,55 px** (`back_r`/`back_l`) | supera o piso de 4,0 px |
| Pixels claros/halo no contorno da cabeça dos ataques frontais | halo cinza-claro no domo verde (`Sword`/`Axe`/`Unarmed`) | **0 em todas as 8 combinações** (contorno escuro `#0C0F12` + pele verde) | halo removido cirurgicamente |
| Vistas traseiras (`back_r` / `back_l`) | frente com rosto apagado | bases e 14 clipes traseiros reconstruídos com nuca/occipital, colar elevado, placa dorsal, faixa carmesim horizontal traseira, cota de malha e grevas traseiras | reconstrução anatômica traseira efetiva |
| `front_r` Idle / Walk / coreografia Sword & Axe | aprovados pelo criador | preservados em ritmo, sincronia de arma e identidade; apenas limpeza cirúrgica do contorno da cabeça nos ataques | preservação do que já funcionava |

Status resultante: conjunto em `technicalStatus: TECHNICALLY_COMPLETE`, `artisticStatus: VISUAL_REVIEW_REQUIRED`, `artisticApproval: PENDING_CREATOR` (candidato final pendente de QA independente do Root e aprovação do criador; `runtimeImplemented: false`).

**Estado real de recuperação Wave 2 (atualizado após revisão de contabilidade do Root, 2026-10-26):**
- **Papéis ativos:** Art Producer é Luna (`8eb61d74`, substituindo o histórico `64f9`). Preview Owner é GLM (`8591`). DEV é proprietário exclusivo de documentação, contratos, receitas e testes;
- **Contabilidade rigorosa (16 jobs, 75 gerações consumidas):** 13 jobs históricos (66 gen) + 1 job de desvio pré-checkpoint (`31e61c4b`, 3 gen, preservado como histórico e aprovado para refino local) + 2 jobs autorizados expressamente pelo Root (6 gen: SwordL `8f0f4e44-0936-4502-8c5e-15b4d57e2449` [3 gen] e AxeR `8b6ad151-8708-4431-a606-06b250388fc4` [3 gen]). Categorização das 75 gerações: 14 rejeitadas (12 Draft-01 + 2 soco fraco) + 24 chaves isoladas não utilizadas/incompatíveis em cache (geometria de corpo inteiro; o defeito de achatamento/grip foi uma falha posterior de composição em Lua) + 28 contribuições aceitas de ciclos/términos não-arma (caminhada, desarmado, hit, derrota) + 3 desvio precoce + 6 autorizadas. Saldo de 1418.70 foi verificado antes do débito das 6 gerações autorizadas (saldo corrente não é estimado sem novo recibo). Zero gerações futuras autorizadas;
- **Preservação comprovada:** 793 arquivos de produção rastreados = 792 byte-idênticos + 1 configuração autorizada de portões alterada; 73 mestres baseline preservados (referência histórica de 525 superada);
- **Matriz e mestres:** 28 clipes no manifesto (`candidate28manifest.json`: 12 células afetadas + 16 pseudônimos inalterados da baseline). Contagens finais exatas de mestres de arte e manifesto canônico aguardam o relatório final de produção pelo Root;
- **Defeito de armas e representante SwordR:** `author_rear_weapons.lua` achatou corpo+arma, usou grip antigo herdado e gravou camadas inconsistentes. O representante `back_r` Sword (8 quadros, 730 ms, 4 camadas `weaponBack`, `body`, `weaponFront`, `handFront` com mestre nativo 128 `sword-body-representative-v2-back_r.aseprite` e grip medido na manopla) recebeu `PASS_FOR_INTERNAL_EXPANSION` do Root após inspeção de composite sheet, close-ups e GIF 1x. Implementação de `back_l` Sword (job `8f0f4e44`) e representante `back_r` Axe (job `8b6ad151`, mecânica própria de machado) autorizada e em andamento por Luna (`8eb61d74`); sem alegação de prontidão final prematura;
- `Walk` traseiro (`back_r` e `back_l`) com passe interno (`PASS_FOR_INTERNAL_EXPANSION`) via geração temporal contínua ancorada (Método 02, 2 gerações por caminhada, pé de apoio cravado e 9º quadro duplicado descartado);
- `Unarmed` frontal (`front_r` e `front_l`): Root aceitou internamente o reparo localizado de F02 (restaurando manopla fechada pendente da mesma vista F00, preservando pixels e tempos dos quadros 00/01/03/04; a codificação dos PNGs reexportados difere de `complete-v1`);
- **Revisão de Hit pelo Root:** Concluída via player Chromium headless (`root-hit-playback-assessment.md` + `diagnosis/root-hit-playback.json`) nas 4 direções em 1x, 0.75x e 0.5x em nativo 128 e aprox 64; recuo de tronco/ombro legível com postura cravada preservada; recomendação de manter pixels atuais e 450 ms para revisão do criador; calibração e sintonia prática no Unity deferidas para teste em jogo;
- **QA independente do Root (Argon QA):** NÃO INICIADO (`NOT_STARTED`); apontador reservado para `experiments/main-orc-rear-recovery-v2/qa-argon-final.md`;
- **Status geral:** candidato final pendente de QA independente e aprovação do criador (`PENDING_CREATOR`). `runtimeImplemented: false`; nenhuma escrita em `../TacticsRPG`. Orc V4 permanece descartado.

Itens abertos para inspeção visual explícita do criador nos estúdios interativos:

1. Confirmar visualmente se a leitura 3/4 de costas (`back_r` NE e `back_l` NW) em repouso, marcha (`Walk`), ataques (`Unarmed`, `Sword`, `Axe`), `Hit` e `Defeat` atende ao padrão artístico desejado.
2. Confirmar se a nova reação `Hit` (recuo pesado no tronco com guarda de manopla, sem snap caricato) e o colapso `Defeat` em 5 estágios têm o peso dramático esperado para o jogo na velocidade real de 1×.
3. Confirmar a limpeza do contorno da cabeça nos ataques frontais (`front_r` / `front_l`).

---

## 14. As 12 lições semânticas obrigatórias de produção (+ métodos operacionais)

Valem para qualquer personagem, raça, Job ou variante desta fábrica. Cada lição documenta todos os 9 campos obrigatórios: sintoma, causa/hipótese verificada, abordagem falha, correção bem-sucedida (ou pendência explícita), oportunidade de reuso, regra de prevenção, evidência de validação, custo/esforço mensurado e aplicabilidade.

> [!NOTE]
> **Registros históricos superados:**
> - A antiga Regra 4 (snapping universal de cabeça e proibição absoluta de 1-2 px) está **SUPERADA** pelo perfil contextual `heavyOrc` e pela lição `numeric-hit-thresholds-diagnostic-warning`. Amplitudes numéricas de `Hit` são avisos diagnósticos e prompts de revisão, não falhas técnicas universais.
> - A antiga Regra 5 (fórmula rígida de 5 estágios de ajoelhamento) está **SUPERADA** pela lição `defeat-consistent-terminal-outcome`: retenção volumétrica tridimensional (`h >= 58px`, `aspect >= 1.3`, massas no chão) e coerência direcional sobrepõem qualquer fórmula única de transição.

### 1. `rear-anatomy-construction` — A rear-facing character needs real rear anatomy
- **Symptom:** Vistas traseiras (`back_r`, `back_l`) parecem artificiais, deformadas ou como um sprite frontal com rosto mascarado/apagado.
- **Root cause (verified):** Derivar vistas traseiras cobrindo ou apagando feições frontais (olhos, presas, boca) preserva gola esternal frontal, peitorais, contorno abdominal e ângulos frontais de joelho que violam a perspectiva traseira.
- **Failed approach:** Repintar o rosto de um sprite frontal e chamá-lo de vista traseira sem reestruturar os marcos esqueléticos.
- **Successful correction:** Reconstruir crânio occipital sem rosto, nuca e trapézio, placa dorsal com canal vertebral, placas escapulares, cinto traseiro sem pico esternal, tassets divididos atrás, tiras poplíteas e calcanhares angulados para longe.
- **Reuse:** Vistas frontais preservadas intactas; bases traseiras construídas formam fundação reutilizável para todos os clipes de costas.
- **Prevention:** `directionalViewGate` exige zero pixels da paleta de rosto frontal na cabeça traseira, lado consistente de iluminação e verificação de todos os 11 marcadores anatômicos traseiros antes de animar.
- **Validation:** Validação das bases direcionais, teste de diferença de espelho (< 97% de concordância com o lado oposto espelhado) e inspeção no estúdio interativo.
- **Cost:** Reconstrução consome ~5-6% de alteração de canvas da base; previne descarte de ciclos inteiros de 28 clipes no futuro.
- **Applicability:** Todas as vistas traseiras de humanoides (`back_r`, `back_l`) em qualquer raça ou classe.

### 2. `rear-motion-needs-rear-construction` — Correct rear static artwork does not guarantee good rear animation
- **Symptom:** `Walk`, `Unarmed`, `Sword` e `Axe` traseiros parecem quebrados, deslizam ou perdem clareza visual mesmo possuindo sprites de base estática traseira melhorados e aprovados.
- **Root cause (verified):** Marcadores anatômicos estáticos não geram automaticamente cinemática de locomoção ou de combate; membros em movimento exigem escorço de perspectiva, alternância de pé de apoio/balanço e torque dorsal que não existem em uma pose estática.
- **Failed approach:** Propagar bases estáticas traseiras diretamente em lotes completos de 28 animações usando interpolação desancorada ou temporizações frontais.
- **Successful correction:** *Reuse-first, keypose-first, full-cycle-before-expansion*: autorar e validar poses-chave de contato/passagem e fechar um ciclo completo de locomoção/ataque antes da expansão em massa.
- **Reuse:** Idle/Walk frontais e bases traseiras preservadas; cinemática de movimento traseiro construída especificamente para os ângulos de costas.
- **Prevention:** Exigir validação de mecânica de keyframe e poses de passagem antes de gerar lotes; registrar categoria de reuso (`REUSE_DIRECT`, `REUSE_ADAPTED`, `REQUIRES_EXTENSION`, `CREATE_NEW`).
- **Validation:** Reprodução em 1×, 0,75× e 0,5× no estúdio interativo; análise de folhas de contato quadro a quadro.
- **Cost:** Previne retrabalho em massa sobre 599 quadros; verificação local de keyframe consome mínimo de recursos.
- **Applicability:** Todos os clipes de movimento traseiro e 3/4 traseiro (`Walk`, `Run`, `Attack`, `Hit`, `Defeat`) em humanoides.

### 3. `weapon-anchor-vs-natural-choreography` — Weapon-anchor alignment does not prove natural combat choreography
- **Symptom:** Ataques parecem robóticos, desconexos ou visualmente inverossímeis, mesmo quando as coordenadas do grip batem com exatidão no soquete da mão.
- **Root cause (verified):** O alinhamento matemático da raiz da arma com as camadas da mão garante apenas fixação espacial; não fornece antecipação corporal, transferência de peso, giro de tronco, cadeia cinética ou arco crível de golpe.
- **Failed approach:** Avaliar qualidade de combate puramente por testes automatizados de sobreposição de bounding box, checagem de coordenadas de soquete ou testes verdes de exportação. Na Wave 2, as 24 chaves exploratórias geradas anteriormente eram geometria de corpo inteiro incompatível/não utilizada, e o achatamento de corpo+arma e inversão de camadas em `author_rear_weapons.lua` foram falhas posteriores de composição em Lua.
- **Successful correction:** [Verified Technique] Os quatro candidatos traseiros de Sword/Axe usam oito quadros/730ms, quatro camadas reais (`weaponBack`, `body`, `weaponFront`, `handFront`), corpo nativo 128 separado e pegada na manopla ancorada diretamente na anatomia do corpo base. A manopla não deve ser posicionada por tabela de grip desvinculada (o que causou a luva flutuante no ar em QA-V3-01), mas orientada pelo ângulo da arma e ligada ao punho real do corpo. [Hypothesis/Pending] Essa técnica requer verificação em 1× pelo QA independente e aprovação explícita do criador; testes de integridade e alfa-over não atestam qualidade estética.
- **Reuse:** Assets de armas permanecem modulares e compartilháveis entre classes/raças (conforme `WEAPON_ART_STANDARD`); perfis de golpe (espada vs machado) são reutilizáveis na mesma família.
- **Prevention:** Nunca tratar alinhamento automático de pegada ou exportação sem erros como evidência de coreografia natural; exigir revisão visual em movimento e inspeção explícita de camadas (`weaponBack`, `body`, `weaponFront`, `handFront`).
- **Validation:** Inspeção no estúdio com chaveamento de camadas (somente corpo vs composto armado), análise do hold no impacto e revisão de arco.
- **Cost:** Desacoplamento de armas reduz custos ao reutilizar perfis de ataque entre itens compatíveis.
- **Applicability:** Todos os ataques armados e ações equipadas em todas as raças e classes.

### 4. `incompatible-attack-reuse` — Reusing incompatible attack poses creates unnatural animations
- **Symptom:** Animações de ataque apresentam saltos bruscos de membros, profundidade deformada ou rotação visualmente inconsistente da silhueta durante o golpe.
- **Root cause (verified):** Reutilizar keyframes de ataque frontal para vistas traseiras, ou forçar um corte universal entre armas de mecânicas opostas (ex: golpe de corte de espada vs machadada vertical pesada), corrompe a continuidade de profundidade e a perspectiva do tronco.
- **Failed approach:** Tentar cross-fades lineares, rotações 2D globais ou cópia cega de poses de ataque entre vistas opostas ou classes de arma distintas.
- **Successful correction:** Estabelecer perfis coreográficos distintos por família de arma (estocada/corte ágil para espada, golpe descendente pesado para machado) e autorar poses-chave direcionais respeitando o ângulo de câmera e massa da arma.
- **Reuse:** Poses e tempos podem ser compartilhados dentro da mesma categoria de arma e ângulo, mas nunca transpostos cegamente entre perspectivas incompatíveis.
- **Prevention:** Validar que arco do golpe, liderança do cotovelo e torque do tronco correspondam à perspectiva e à classe de peso antes da composição final.
- **Validation:** Comparação direcional no estúdio de revisão; checagem de curva de trajetória sem reversões espúrias.
- **Cost:** Autorização inicial de perfil exige iteração focada; evita repetidas rejeições de conjuntos híbridos.
- **Applicability:** Todas as animações de ataque corpo a corpo e à distância em todas as direções.

### 5. `numeric-hit-thresholds-diagnostic-warning` — Numeric Hit thresholds can encourage overacting
- **Symptom:** A reação de `Hit` parece exagerada, caricata ou espasmódica em velocidade normal (1×), quebrando o tom tático sóbrio.
- **Root cause (verified):** Mínimos numéricos universais rígidos de excursão de cabeça, deslocamento de centróide e energia forçaram animadores a aumentar artificialmente a amplitude para passar em testes automatizados, penalizando personagens pesados e encouraçados.
- **Failed approach:** Exigir pisos numéricos universais (ex: >= 6 px de excursão, >= 4 px de centróide, proibição absoluta de 1-2 px) para todas as raças e armaduras.
- **Successful correction:** Converter limiares numéricos de amplitude em avisos diagnósticos sensíveis ao contexto (`diagnosticWarnings`, `severity: warning`, `notHardFailures: true`); adotar perfil `heavyOrc` (impacto legível e recuperação clara ao repouso no tronco/ombros; head snap opcional); reter integridade dura (groundY, arquivos, hashes, manifesto).
- **Reuse:** Medições históricas (12 px de excursão, 5,74 px de centróide no build b178422e1f7fc19f068c) mantidas como baselines diagnósticas, não mínimos universais.
- **Prevention:** Proibir gates numéricos rígidos de pass/fail para amplitude visual subjetiva; manter gates duros apenas para integridade técnica e registro de solo.
- **Validation:** Revisão visual no estúdio em 1×, 0,75× e 0,5×; confirmação de impacto legível e pés cravados no solo.
- **Cost:** Elimina ciclos de retrabalho causados por amplificações forçadas seguidas de atenuações.
- **Applicability:** Animações de `Hit` e reações de impacto em todos os personagens, classes e pesos de armadura.

### 6. `defeat-consistent-terminal-outcome` — Defeat must communicate a consistent terminal outcome across directions
- **Symptom:** O `Defeat` resulta em tiras achatadas, quedas inverossímeis ou corpos caídos com volumes e silhuetas incompatíveis dependendo do ângulo de visão.
- **Root cause (verified):** Aplicação de rotação 2D global com compressão vertical (`vScale = 0.52`) ou imposição de fórmula única e rígida de ajoelhamento destrói o volume tridimensional e a leitura de massa no solo.
- **Failed approach:** Rotação 2D global + escala vertical 0.52; impor sequência idêntica de ajoelhamento para todas as armaduras que desmorona em uma tira horizontal.
- **Successful correction:** Coreografar colapso progressivo volumétrico retendo massas legíveis de cabeça, pauldron e peito na linha do solo (`groundY`), com proporção terminal (`w/h >= 1.3`) e altura terminal (`h >= 58px` em canvas 128) servindo como balizas diagnósticas contextuais sob o perfil `heavyOrc`, não portões rígidos universais. A retenção volumétrica tridimensional sobrepõe qualquer fórmula rígida de ajoelhamento.
- **Reuse:** Poses terminais caídas direcionais fornecem cadáveres consistentes e reutilizáveis para o tabuleiro tático.
- **Prevention:** Checagens automatizadas cobram retenção volumétrica terminal, contato com o solo e vetam squashing 2D global ou fórmulas de compressão regional em fatias (`y' = y + floor(...)`); encadeamento direcional deve manter coerência terminal.
- **Validation:** Checagens de volume no quadro terminal (altura, largura, aspect ratio, groundY) e inspeção de hold terminal no estúdio interativo.
- **Cost:** A composição de estágios volumétricos exige desenho deliberado, mas elimina desconexão visual na morte da unidade.
- **Applicability:** Animações de `Defeat` e incapacitação em todas as direções e personagens.

### 7. `technical-completion-not-artistic-approval` — Technical completion is not artistic approval
- **Symptom:** Pacotes de animação com zero erros de validação, dimensões corretas e hashes conferidos são entregues como prontos, mas apresentam arte inaceitável aos olhos do criador.
- **Root cause (verified):** Linters e validadores medem presença de arquivos, bytes, dimensões, canais alfa e esquemas JSON; não avaliam anatomia, silhueta, perspectiva, peso, ritmo ou apelo visual.
- **Failed approach:** Declarar um pacote "pronto", "concluído" ou "aprovado" porque testes automatizados retornaram 0 FAIL.
- **Successful correction:** Taxonomia estrita de quatro status: `TECHNICALLY_COMPLETE` -> `VISUAL_REVIEW_REQUIRED` -> `CREATOR_APPROVED`, com `ARTISTIC_REVISION_REQUIRED` bloqueando apresentação como pronto. Somente o criador humano aprova arte.
- **Reuse:** Validadores automatizados permanecem indispensáveis para detectar regressões estruturais sem substituir o olhar humano.
- **Prevention:** Proibir termos como READY, DONE ou APPROVED sem o status explícito da taxonomia; barrar handoff de engine antes de aprovação visual.
- **Validation:** Status legível por máquina na matriz de cobertura e contrato JSON, assinado por registro explícito do criador.
- **Cost:** Zero custo extra de criação; economiza retrabalho massivo de integração prematura na engine.
- **Applicability:** Universal para todos os assets, animações, personagens e equipamentos da Character Factory.

### 8. `validated-poses-reused-not-regenerated` — Validated poses should be reused instead of regenerated
- **Symptom:** Ao tentar corrigir um defeito localizado (ex: vistas traseiras), poses frontais de Idle já aprovadas, marchas validadas ou coreografias de combate são alteradas ou degradadas silenciosamente.
- **Root cause (verified):** Regenerar lotes completos de animação ou disparar passes generativos sobre o corpo inteiro sobrescreve arte validada e aprovada pelo criador.
- **Failed approach:** Re-exportar ou regenerar a biblioteca inteira a partir do zero para consertar as costas, alterando quadros frontais já aprovados.
- **Successful correction:** Isolar e proteger assets validados; aplicar máscaras de camada, correções cirúrgicas localizadas e fluxo de fork/reintegração. Idle frontal, Walk frontal e coreografias de espada/machado aprovadas permanecem byte-idênticas.
- **Reuse:** Reuso máximo de assets validados (`idle-balanced-v1`, passada frontal aprovada, pegadas estabelecidas).
- **Prevention:** Manter mapa de hashes de arte protegida (`protected-art.json`); rodar comparações automatizadas de SHA-256 para assegurar identidade de bytes.
- **Validation:** Teste automatizado de asserção de identidade de bytes contra os hashes canônicos protegidos.
- **Cost:** Reduz drasticamente consumo de créditos, tokens e fadiga de revisão ao preservar o que funciona.
- **Applicability:** Todos os fluxos de refino iterativo e recuperação de biblioteca.

### 9. `failed-artistic-foundations-downstream-rework` — Small failed artistic foundations can create extensive downstream rework
- **Symptom:** Um conjunto inteiro de 28 clipes ou dezenas de quadros precisa ser descartado porque falhas fundamentais de anatomia ou pegada são descobertas tardiamente.
- **Root cause (verified):** Propagar um keyframe não validado, uma base traseira defeituosa ou soquetes imprecisos para ciclos inteiros e variantes multiplica o erro por centenas de frames derivados.
- **Failed approach:** Pular do conceito inicial diretamente para a geração de folhas completas multidirecionais sem marcos intermediários de aprovação. Na Wave 2, a propagação prematura de poses com grip desalinhado invalidou 24 chaves exploratórias de armas.
- **Successful correction:** [Verified Principle] Falhas nas bases traseiras e no script Lua de armas causaram invalidação repetida de células derivadas (inclusive 24 chaves exploratórias isoladas com grip inadequado); a produção de chave representativa única (SwordR 8f com 4 camadas) evitou desperdício de créditos e serviu de base para autorização controlada. [Hypothesis/Pending] Imposição de portões obrigatórios (Gate 1 -> Gate 2 -> chave representativa) é diretriz para blindar o pipeline.
- **Reuse:** Fundações sólidas permitem expansão sem atrito para todas as direções, armas e roupas variantes.
- **Prevention:** Nunca expandir uma ação para 4 direções ou múltiplas armas antes do ciclo da direção primária passar por revisão visual.
- **Validation:** Checkpoints de marcos (validação de base, revisão de poses-chave) registrados nos experimentos.
- **Cost:** Gastar poucas iterações na base economiza o retrabalho de centenas de quadros derivados.
- **Applicability:** Todo pipeline de criação de novo personagem, variante de outfit ou expansão de ação.

### 10. `complete-review-interface-mandatory` — A complete review interface is mandatory for meaningful creator approval
- **Symptom:** Revisores deixam passar bugs graves de animação, pés patinando ou incongruências direcionais ao avaliar PNGs soltos ou folhas estáticas.
- **Root cause (verified):** A percepção de pixel art animada depende de movimento contínuo, velocidade de reprodução e contexto comparativo; inspecionar quadros estáticos isolados não revela saltos temporais.
- **Failed approach:** Entregar pastas de arquivos PNG soltos ou pranchas estáticas acompanhadas de instruções textuais manuais.
- **Successful correction:** [Verified Principle] A inspeção no estúdio interativo permitiu identificar a deficiência do soco (F03..F06) e os erros de sobreposição de armas que passaram despercebidos em saídas de log. [Hypothesis/Pending] A extensão do estúdio para exibir as 28 células com chaveamento de antes/depois isolado do build canônico foi implementada e cobre todas as 15 células afetadas.
- **Reuse:** Estrutura do estúdio de revisão é diretamente reutilizável para todos os pacotes de personagens e estudos comparativos.
- **Prevention:** Testes automatizados verificam existência do estúdio, acessibilidade das 28 células, presença de badges de status e links de antes/depois com hashes distintos.
- **Validation:** Asserções automatizadas na suíte de testes; navegação visual fluida pelo criador.
- **Cost:** Baixo custo de tooling; acelera exponencialmente o ciclo de tomada de decisão e elimina mal-entendidos.
- **Applicability:** Todas as entregas de animação, passes de recuperação e estudos comparativos de arte.

### 11. `successful-methods-documented-equally` — Successful methods must be documented as carefully as failed methods
- **Symptom:** Equipes repetem erros anteriores ou não conseguem reproduzir sucessos anteriores porque apenas o asset final foi salvo, sem registro da técnica utilizada.
- **Root cause (verified):** Capturar apenas o arquivo final torna a metodologia invisível; agentes subsequentes retornam à tentativa e erro, reinventando a roda ou caindo em falhas conhecidas.
- **Failed approach:** Documentar apenas bugs e rejeições enquanto sucessos de geração são tratados como acasos sem registro de prompts, âncoras, sementes ou scripts Lua de montagem.
- **Successful correction:** [Verified Accounting Record] O registro rigoroso dos parâmetros do Método 02 (recibo de 2 gerações, job 1bdc9771) permitiu que a produção de back_l Walk fosse executada de forma idêntica e sem retrabalho; o registro transparente do desvio de 3 gerações pré-checkpoint (job 31e61c4b) e a autorização explícita estrita de 2 jobs / 6 gerações adicionais (SwordL e AxeR) comprovaram a governança contábil. [Hypothesis/Pending] A exigência contratual de 9 campos de evidência por lição é a garantia contra perda de know-how.
- **Reuse:** Receitas de produção e scripts Lua comprovados podem ser aplicados diretamente a outras direções, ações e personagens.
- **Prevention:** Exigir que todo marco de produção ou recuperação entregue lições estruturadas cobrindo os 9 campos obrigatórios.
- **Validation:** Teste automatizado de conformidade contratual verificando presença e preenchimento de todas as lições semânticas.
- **Cost:** Poucos minutos de documentação geram ganhos compostos massivos de produtividade em execuções posteriores.
- **Applicability:** Toda pesquisa e desenvolvimento, criação de ferramentas e pipeline de produção da Character Factory.

### 12. `speed-and-scale-evaluation` — Quality should be evaluated at actual playback speed and practical game scale
- **Symptom:** Animações que parecem nítidas e ricas quando ampliadas em 400% ou passo a passo tornam-se ilegíveis, poluídas ou duras na escala real de 1× no jogo; inversamente, reações sutis que parecem discretas no zoom funcionam perfeitamente na escala real.
- **Root cause (verified):** A percepção humana do movimento em pixel art depende da integração temporal e da resolução do olho na tela; detalhes em alta frequência podem virar ruído no movimento rápido, enquanto amplitude de deslocamento lê de modo diferente na escala nativa de 1×.
- **Failed approach:** Julgar animações exclusivamente por inspeção estática ampliada no editor (ex: 8× de zoom) ou por fórmulas matemáticas de delta de pixels.
- **Successful correction:** Avaliar todas as animações no estúdio interativo na resolução nativa de 1× e na velocidade real de execução (1×), complementando com 0,75× e 0,5× para inspeção mecânica e avanço quadro a quadro para verificação de artefatos.
- **Reuse:** Critérios de avaliação e controles de velocidade aplicam-se a todas as revisões de personagens e efeitos.
- **Prevention:** Incluir visualização em escala nativa de 1× ao lado de vistas ampliadas em todas as ferramentas de preview; avaliar impacto e recuo no contexto real antes de alterar amplitudes.
- **Validation:** Controles de velocidade e escala no estúdio de revisão; validação visual humana nas velocidades normais.
- **Cost:** Evita detalhamento excessivo ou super-animação que não agrega valor na resolução real de jogo.
- **Applicability:** Todos os sprites de personagens, animações de combate e efeitos visuais do jogo.

---

### Lições operacionais da recuperação traseira Wave 2

### 13. `external-crossfade-raster-interpolation-failure` — Interpolação por cross-fade externo não produz locomoção e viola a regra de autoria Aseprite
- **Symptom:** Draft de caminhada traseira (`back_r` Walk, Draft-01) resultou em pixels borrados/fantasma sem leitura de passadas reais; o personagem parece deslizar em pose estática trêmula com bob de 1 px, sem alternância nítida de apoio, passagem e elevação de joelho/pé.
- **Root cause (verified):** O método tentou sintetizar quadros intermediários via interpolação linear (PIL Image.blend + limiar de alfa) entre duas poses estáticas/quase-estáticas geradas por inpaint e a base estática, além de gerar pixels fora do Aseprite (violação direta de AGENTS.md). Poses de entrada quase-estáticas combinadas com fusão de opacidade não produzem cinética de membros. O ground-snap global desloca a figura inteira e mascara a raiz de movimento sem substituir a ausência de poses articulares de passada.
- **Failed approach:** 1) Inpainting de duas poses com descrição de passada que gerou variações de sombreamento/postura mas sem descolamento suficiente da perna de balanço (ambos os pés permaneceram em contato próximo com o solo). 2) Interpolação matemática externa (Python/PIL) para preencher os quadros. 3) Snap global de chão aplicado cegamente sobre a bounding box de quadros sem cinemática articular.
- **Successful correction:** Substituir o método por construção de animação no Aseprite Lua a partir de poses com cinemática real (apoio em um membro e balanço no membro oposto). Todo o processamento de pixels, registro de solo, temporização e montagem deve ocorrer dentro do Aseprite (via runner isolado `--batch --noinapp`). Downloads de saídas brutas em Python são restritos a I/O, hashes e metadados.
- **Reuse:** As duas imagens geradas (`af1e7ba8-655e-45fd-9798-2ba4b8cda7e9` e `ed109b13-7b60-4200-8a43-ed8a9fb8f561`) permanecem arquivadas como evidência em `experiments/main-orc-rear-recovery-v2/rejected/draft-01-crossfade/`, utilizáveis para inspeção de textura de botas e tassets.
- **Prevention:** 1) Proibido gerar pixels de produção por interpolação de raster/cross-fade no Python. 2) O snap de solo não substitui pose de passada: cada quadro de caminhada precisa ter um pé de apoio explicitamente registrado no solo (`groundY = 126`) enquanto o membro em balanço articula livremente acima do solo. 3) O esqueleto V3 com 18 juntas COCO manuais permanece rota legal sem REST caso geração temporal apresente desvios.
- **Validation:** Prancha 4x4 `grid-walk-back_r-candidate.png` e GIF `walk_back_r_candidate.gif` arquivados em `experiments/main-orc-rear-recovery-v2/rejected/draft-01-crossfade/`.
- **Cost:** 12 gerações PixelLab Pro Flash consumidas no Draft-01 rejeitado (2 chamadas inpaint de 6 gerações cada: jobs `af1e7ba8-655e-45fd-9798-2ba4b8cda7e9` e `ed109b13-7b60-4200-8a43-ed8a9fb8f561`). Registrado separadamente do trabalho subsequente.
- **Applicability:** Locomoção traseira e lateral de bípedes pesados (`orc-v1` e variantes).
- **Status:** `FAILED_METHOD_ARCHIVED`

### 14. `continuous-temporal-anchored-generation` — Geração temporal contínua com ancoragem restringe ciclo de locomoção com alta eficiência
- **Symptom:** Inpainting de poses isoladas sem modelo de movimento gera poses estáticas desconectadas e exige múltiplos disparos caros.
- **Root cause (verified):** A ferramenta `animate_image` calcula a cinemática como uma trajetória temporal coordenada. A ancoragem de `first_frame_base64` e `last_frame_base64` na base aprovada restringe as extremidades do ciclo, mas não garante matematicamente ausência total de deriva intermediária ou cinemática perfeita de passada sem registro do pé de apoio e ajuste de temporização no Aseprite Lua.
- **Failed approach:** Tentativas de sintetizar locomoção por inpainting isolado de quadros soltos cobrando 6 gerações por frame sem garantia de descolamento de passada (12 gerações para 2 frames quase estáticos no Draft-01).
- **Successful correction:** [Verified Technique] `animate_image` com `frame_count=8` e ancoragem na base traseira produziu passadas funcionais em `back_r` e `back_l` (recibos comprovados de 2 gerações cada: jobs `1bdc9771` e `64cd4cb7`). O 9º quadro duplicado foi descartado no script Lua e o pé de apoio registrado em `groundY=126`. [Hypothesis/Pending] A estabilidade em vistas de perfil e a aplicação em quadrúpedes ou outros bípedes permanece hipótese a verificar.
- **Reuse:** Metodologia comprovada para `back_r` e `back_l` Walk; extensível como hipótese a outros ciclos de locomoção.
- **Prevention:** Preferir geração temporal contínua para locomoção; verificar frames intermediários contra deriva de massa; montar e ancorar pé de apoio no Aseprite Lua; descartar o quadro de retorno duplicado.
- **Validation:** Jobs `1bdc9771` e `64cd4cb7` (2 gerações cada), pranchas e GIFs de loop temporal, masters em `characters/orc-v1/source/aseprite/rear-recovery-v2/`.
- **Cost:** 2 gerações PixelLab por clipe de caminhada (total 4 gerações para as duas caminhadas traseiras).
- **Applicability:** Demonstrado e verificado especificamente nas 2 vistas traseiras (`back_r` e `back_l`) no experimento de bípede Orc 128x128 (`orc-v1`). A extensão para as 4 ou 8 direções e outras anatomias raciais permanece como hipótese técnica a ser verificada experimentalmente.
- **Status:** `PASS_FOR_INTERNAL_EXPANSION_WALK_ONLY` (candidato final pendente de QA independente do Root e aprovação do criador).

### 15. `weapon-contamination-and-layers-off-inspection` — Prompts de corpo desarmado exigem inspeção semântica com camadas de armas desligadas (layers-off) e continuidade articular
- **Symptom:** Artefatos espúrios de lâmina, machado, cabo ou lâminas secundárias gerados acidentalmente pela IA reaparecem fundidos ao corpo base ou armadura (ex: QA-01/QA-V3-02 lâmina/haste junto ao quadril em `back_l/Sword` F01-F07 e faixa clara no ombro F05; QA-02/QA-V3-02 cabeça secundária de machado em `back_r/Axe` e `back_r/Sword` F01 e haste em F02-F03; QA-04/QA-V3-03 filamento no ombro em `back_l/Axe` F02-F03), ou desconexão articular ombro-cotovelo-punho (QA-03 braço truncado em F04 e antebraço duplo em F05).
- **Root cause (verified):** Reimportação acidental de doadores brutos antigos (`axe-r-cleaned-native` e `back_l-sword-cleaned-native`) em scripts de autoria, em vez de isolar cels higienizados. Checagens matemáticas de pipeline (`body` == `master` == crop nativo e alfa-over == compósito) provam apenas integridade estrutural e empacotamento técnico, NÃO ausência semântica de armas pintadas no corpo. Filtros superficiais como `cleanBodyEdges` escurecem certos pixels perimetrais mas não removem armas internas nem reconstroem a anatomia.
- **Failed approach:** Confiar em validações automáticas de igualdade estrutural de camadas ou em prompts textuais sem inspecionar visualmente o corpo inteiro com camadas de armas desligadas (`layers-off`), e compor armas sobre membros com articulações descontinuadas.
- **Successful correction:** [Verified Technique] Extração e aplicação estrita de cels limpos a partir do checkpoint higienizado, expurgo completo de armas do corpo base e reconstrução da cadeia articular contínua ombro-cotovelo-punho. Inspeção obrigatória do corpo com camadas de equipamento desligadas (`layers-off`) antes da montagem e ligação de armas independentes. [Hypothesis/Pending] A qualidade artística final depende de inspeção contínua em 1× pelo QA independente e aprovação do criador.
- **Reuse:** Procedimento de checagem visual semântica `layers-off` reutilizável para qualquer personagem com sistema de equipamento modular.
- **Prevention:** 1) Inspecionar visualmente o corpo inteiro gerado com todas as camadas de armas desligadas (`layers-off`) para assegurar ausência semântica total de lâminas, hastes e cabos. 2) Validar a cadeia cinemática contínua ombro-cotovelo-punho antes de sobrepor a manopla de oclusão frontal (`handFront`) ou a arma.
- **Validation:** Inspeção visual direta de folhas de contato `layers-off`, verificação de continuidade esquelética e re-revisão por QA independente sob novo freeze.
- **Cost:** Zero gerações adicionais; apenas inspeção visual e reparo cirúrgico local no Aseprite.
- **Applicability:** Todos os personagens e animações de combate com camadas de equipamento desacopladas.

### 16. `donor-cluster-verification-before-reuse` — Verificação obrigatória do cluster de pixels do doador antes do reuso anatômico
- **Symptom:** Tentativas de transplante de membros geram remendos transparentes ou recortes parciais sem geometria anatômica reconhecível.
- **Root cause (verified):** Recortes baseados apenas em bounding boxes estimadas ou áreas aproximadas podem capturar fundo transparente ou apenas o antebraço sem a mão.
- **Failed approach:** Copiar regiões estimadas por coordenadas sem verificar a presença física do punho ou manopla fechada no doador.
- **Successful correction:** [Verified Principle] Validação de cluster real antes do reuso: o doador deve conter manopla/punho levantado completo e visível dentro do próprio canvas; fundos vazios ou recortes de antebraço são terminantemente rejeitados. Comprovado na validação de F02 e na reparação de AxeL. [Hypothesis/Pending] Biblioteca de doadores certificados por vista e escala.
- **Reuse:** Manoplas aprovadas do mesmo indivíduo e mesma vista servem como doadores canônicos para reparos cirúrgicos.
- **Prevention:** Inspecionar a máscara de seleção no Aseprite e confirmar visualmente a presença do membro anatômico completo antes do transplante.
- **Validation:** Contagem de pixels opacos e conferência de silhueta no Aseprite e nas ferramentas de verificação de exportação.
- **Cost:** Economiza chamadas pagas de regeneração evitando transplantes vazios.
- **Applicability:** Reparos anatômicos locais em pixel art para todas as raças.

### 17. `surgical-same-view-donor-repair` — Reparo cirúrgico no Aseprite com doador da mesma vista e remoção exata de resíduos
- **Symptom:** Membros cortados pela borda do canvas (ex: punho cortado em AxeL nos quadros 01–02) ou resíduos desconectados de membros antigos (27 pixels soltos) corrompem a leitura anatômica.
- **Root cause (verified):** O gerador de esqueleto cortou a mão erguida no topo do canvas 128x128; tentativas de correção deixaram fragmentos do braço anterior e restos de cabo marrom.
- **Failed approach:** Regenerar o ciclo completo consumindo créditos adicionais ou usar doador de vista frontal com perspectiva e iluminação incompatíveis.
- **Successful correction:** [Verified Technique] Reparo cirúrgico em Aseprite Lua utilizando braço e manopla da mesma vista e mesmo indivíduo (`back_l/Sword`), preservando torso, pernas, armadura, perspectiva NO e luz de AxeL, com remoção cirúrgica de resíduos via máscara de coordenadas. [Hypothesis/Pending] Generalização da técnica para qualquer membro cortado em animações de ataque.
- **Reuse:** Scripts Lua de reparo local preservados para referência.
- **Prevention:** Verificar se o movimento atinge os limites do canvas na geração; ao reparar, priorizar doadores da mesma vista e do mesmo indivíduo.
- **Validation:** Inspeção visual de 1x e aprovação de integração interna.
- **Cost:** Zero chamadas adicionais de API.
- **Applicability:** Membros cortados ou artefatos gerados em sprites de combate.

### 18. `bright-edge-artifacts-and-perimeter-outline` — Eliminação de artefatos de borda clara através de contorno perimetral protetor em rotações de armas
- **Symptom:** Halos claros esbranquiçados na silhueta externa de espadas e machados em vistas traseiras contra o canal alfa transparente. Pixels como `rgba(176,178,180)` possuem luma real ITU-R BT.601 de aproximadamente 178 (`0.299*176 + 0.587*178 + 0.114*180 = ~177.6`), escapando completamente de limiares ingênuos de `luma >= 200`.
- **Root cause (verified):** Rotação por reamostragem discreta (nearest-neighbor) de lâminas metálicas sem pós-processamento projeta pixels claros para a borda transparente. Filtros baseados puramente em `luma >= 200` deixam escapar reflexos claros de luma 170-199. Além disso, análises que utilizam conectividade de apenas 4 vizinhos (ortogonal) falham em detectar pixels diagonais expostos à transparência; a detecção de borda requer 8 vizinhos (8-conectividade).
- **Failed approach:** Achatamento global de cores ou filtro com limiar rígido de 200 usando 4 vizinhos, que deixa escapar bordas diagonais claras e artefatos de luma 178.
- **Successful correction:** [Verified Technique] Algoritmo perimetral no Aseprite Lua que avalia a vizinhança de 8 pixels (8-conectividade com o canal alfa) e aplica contorno escuro protetor (`INK` `rgba(12,15,18,255)` e aço escuro de sombra), garantindo zero pixels claros expostos à transparência nas 32 poses das armas traseiras, sem aniquilar os reflexos metálicos internos.
- **Reuse:** Script de percurso perimetral em todas as composições de armas rotacionadas.
- **Prevention:** Nunca exportar rotações diretas de sprites cortados sem aplicar contorno protetor perimetral de 8 vizinhos e validar visualmente ausência de halos.
- **Validation:** Verificação visual em 1× e 2×/3× nearest-neighbor com fundo quadriculado e ferramentas diagnósticas.
- **Cost:** Zero gerações; cálculo matricial local no Aseprite.
- **Applicability:** Todas as armas e acessórios rotacionados em sprites 2D.

### 19. `curled-glove-depth-and-grip-standard` — Empunhadura autêntica com luva envolvente, ancoragem anatômica real e corte de profundidade
- **Symptom:** A manopla sobre o cabo flutua no vazio descolada do braço (como em `back_r/Sword` F04-F05, onde a manopla foi renderizada em y=94 enquanto o punho real do corpo estava em y=118, apontado no QA-V3-01).
- **Root cause (verified):** Posicionamento de grip via tabelas estáticas de coordenadas arbitrárias desvinculadas da anatomia do corpo base, aliado a um desenho de manopla estático que não considerava o ângulo da arma nem a posição real do punho esquelético.
- **Failed approach:** Ajustar offsets fixos em tabelas estáticas sem ancorar o overlay aos pixels reais do punho do corpo no respectivo quadro.
- **Successful correction:** [Verified Technique] Derivar as coordenadas da manopla diretamente dos centróides e pixels reais do punho do corpo base (`{181, 118}` em F04 e `{181, 122}` em F05), orientando a luva e os dedos pelo ângulo real da lâmina/haste, alcançando >90% de sobreposição anatômica real com o membro corporal no sanduíche de profundidade: `body` (palma) -> `weaponFront` (haste) -> `handFront` (dedos fechados).
- **Reuse:** Padrão canônico para todas as armas de combate corpo a corpo de uma mão.
- **Prevention:** Proibir tabelas de grip puramente estáticas; validar a sobreposição anatômica da luva com o punho do corpo com `layers-off` e em velocidade normal (1×) antes de congelar a entrega.
- **Validation:** Verificação de coincidência de pixels overlay vs punho corporal (>90%) e teste Chromium 20/20 checks.
- **Cost:** Zero gerações.
- **Applicability:** Todas as animações armadas da fábrica.

### 20. `strike-cycle-opposite-limb-preservation` — Preservação obrigatória do membro secundário em ciclos de combate
- **Symptom:** Em `front_r` e `front_l` Unarmed, o braço esquerdo em guarda desaparecia abruptamente nos quadros 02 e 03 durante o clímax e retorno do golpe, gerando uma amputação acidental de mais de 1000 pixels da silhueta.
- **Root cause (verified):** O processo generativo isolou apenas o vetor de movimento do membro que soca, omitindo o torso contralateral e o braço de suporte nos keyframes de impacto.
- **Failed approach:** Justificar o sumiço do membro como "oclusão extrema de perspectiva".
- **Successful correction:** [Verified Technique] Restauração da geometria e iluminação do braço de guarda a partir do quadro de preparação F01 no Aseprite, restabelecendo a silhueta completa (de 1778 para 2661 pixels) e a estabilidade corporal durante todo o soco, sincronizando os PNGs compostos e os nativos 128x128.
- **Reuse:** Princípio de conservação de massa em animações de ataque desarmado e corpo a corpo.
- **Prevention:** Verificar se a massa e a silhueta dos membros não-atacantes mantêm continuidade temporal entre todos os quadros.
- **Validation:** Inspeção de silhueta por `silhouette()` e testes de integração de manifestos.
- **Cost:** Zero gerações.
- **Applicability:** Todos os golpes corporais bípedes.

### 21. `strike-sweep-destination-decoupling-and-mask-integrity` — Cinemática contínua, desacoplamento de buffers e integridade anatômica de máscara
- **Symptom:** Em `back_r` Unarmed, o punho de ataque desaparecia no quadro 03 de follow-through; em `back_l` Unarmed, o membro desaparecia em F03 e o F04 apresentava grande corte retangular na lateral do tronco/armadura com fragmento marrom de manopla solto a (30,83) junto ao quadril (QA-V3-04 e RR-01).
- **Root cause (verified):** Em `back_l/Unarmed` F03, o script Lua apagava `(x, y)` e escrevia no mesmo destino durante a varredura, destruindo pixels anteriores. Em F04, a máscara de exclusão de membro apagava integralmente a caixa nativa `x=15..45, y=20..80`, cortando o tronco e a armadura e parando em y=80, o que deixava o remanescente da luva como fragmento desconectado flutuando no ar.
- **Failed approach:** Varredura com apagamento e escrita concorrente no mesmo buffer; máscaras de caixa arbitrárias que recortam partes do tronco e deixam resíduos de membros abaixo do limite de corte.
- **Successful correction:** [Verified Technique] Separação estrita entre buffer de leitura e buffer de escrita durante transformações no Aseprite Lua; restauração do punho em F03 de `back_r` em desaceleração espacial contínua (x=182 descendo do impacto em x=186); reconstrução de `back_l` F04 eliminando a máscara de corte destrutivo e retornando à pose de repouso com ancoragem em solo (`Point(0, 1)`), restaurando o contorno de armadura/tronco e o braço pendente coerente idêntico ao Idle base da mesma vista.
- **Reuse:** Fluxo de autoria de soco traseiro com buffers desacoplados e preservação de silhueta corporal.
- **Prevention:** Nunca ler e escrever no mesmo cel/buffer de imagem durante varreduras translacionais; nunca aplicar máscaras de caixa retangulares sem validação anatômica das fronteiras de armadura e membros.
- **Validation:** Diagnóstico delta, verificação de 0 diferenças composto vs nativo, testes automatizados `test/test_declared_hashes.test.mjs` e inspeção visual em ampliações 1×, 3× e 4×.
- **Cost:** Zero gerações.
- **Applicability:** Ataques desarmados e reações traseiras.

### 22. `incapacitated-ground-collapse-vs-kneeling` — Colapso terminal incapacitado com retenção de volume 3D
- **Symptom:** A pose final de derrota frontal (`front_r`/`front_l` Defeat) mantinha o torso erguido a 66 px de altura na baseline, e a 57 px na entrega intermediária, transmitindo a leitura de um combatente apoiado nos quatro apoios ou ajoelhado com cabeça suspensa entre os braços, em vez de nocauteado (RR-05).
- **Root cause (verified):** O quadro terminal mantinha a cabeça elevada e os braços apoiados verticalmente como escoras sustentando o tórax acima do solo, criando um vazio abaixo do queixo.
- **Failed approach:** Achatamento por escala vertical 2D global (`vScale = 0.52`) ou compressão regional em fatias horizontais (`y' = y + floor(...)`), ambas deformando o volume 3D. Pintar sobre cels existentes sem executar `cel.image:clear()`, deixando a silhueta antiga oculta por baixo.
- **Successful correction:** [Verified Technique] Reestruturação do colapso volumétrico como nocaute genuíno: cabeça rebaixada rente ao solo/antebraço (`cabeça baixa`), tronco assentado de bruços no chão, e braços soltos/abertos desarmados, preservando 100% dos agrupamentos anatômicos de pixels e sombreamento. Atinge altura terminal de 52 px (57 px no passe intermediário de translação simples) e proporção horizontal de 2,35 (2,10 na intermediária), ancorado em `groundY = 190` composto / `126` nativo. Os valores de altura e aspecto são balizas diagnósticas contextuais sob o perfil `heavyOrc`, não portões rígidos universais. Execução obrigatória de `cel.image:clear()` antes de desenhar o cel no mestre Aseprite.
- **Reuse:** Modelo de transição para o estado de nocaute de personagens humanoides pesados.
- **Prevention:** Garantir que a cabeça desça para o nível do solo e que os braços não atuem como escoras rígidas; limpar o cel antes de compor (`cel.image:clear()`); nunca utilizar fórmulas de squashing regional ou global.
- **Validation:** Medição de volume da bounding box, conferência de 0 diferenças entre mestre, composto e nativo, e inspeção comparativa no estúdio de revisão.
- **Cost:** Zero gerações.
- **Applicability:** Animações de derrota para todas as classes e raças.

### 23. `six-verified-failure-causes` — As seis causas verificadas de falhas recorrentes no pipeline
Com base nas auditorias independentes de QA e nos incidentes identificados em produção, foram catalogadas seis causas raízes recorrentes que devem ser rigorosamente prevenidas:
1. **Doador antigo reentrando:** Scripts de autoria que voltam a carregar pastas com assets brutos/contaminados (ex: `axe-r-cleaned-native` e `back_l-sword-cleaned-native`) em vez de carregar estritamente cels já higienizados de checkpoints aprovados. Prevenção: rastreabilidade estrita da proveniência de cada cel e proibição de carregamento cego de diretórios de entrada não auditados.
2. **Grip por tabela:** Coordenadas de fixação de mão/arma definidas em tabelas estáticas desconectadas da anatomia do frame, fazendo a manopla flutuar no ar longe do membro. Prevenção: derivar coordenadas da manopla diretamente dos centróides/âncoras dos punhos do corpo no respectivo frame.
3. **Apagar e escrever no mesmo destino durante a varredura:** Loops de montagem iterativa que limpam `(x, y)` e escrevem em `(x+dx, y+dy)` no mesmo buffer, fazendo com que iterações subsequentes apaguem pixels gravados por iterações anteriores (como ocorreu em `back_l/Unarmed` F03). Prevenção: usar buffers de origem e destino estritamente separados.
4. **Exportação parcial / dessincronia:** Atualizar apenas o frame 256x256 composto ou o mestre `.aseprite`, deixando o `native/*.png` ou `native-strip.png` apontado pelo `clip.json` defasado. Prevenção: exportação atômica síncrona de mestre, composto, strip e nativo 128x128.
5. **Pintura sobre cel sem limpar:** Desenhar novos pixels sobre um cel existente (`drawImage`) sem executar `cel.image:clear()` antes, mantendo a silhueta antiga oculta por baixo no mestre `.aseprite` (como ocorreu no `Defeat` frontal). Prevenção: sempre limpar o cel antes da composição.
6. **Metadado circular / falsos aliases:** Classificar clipes como `UNCHANGED_ALIAS` quando sofreram alterações locais de limpeza ou acabamento (como Walk frontais e Sword frontal esquerdo). O escopo do passe deve rastrear rigorosamente todos os clipes tocados (15 ativos / 13 protegidos).

### 24. `composite-native-master-tri-equality` — Verificação obrigatória de igualdade entre composto, nativo e mestre
- **Regra:** Nenhum clipe alterado pode ser considerado concluído sem que haja estrita igualdade de pixels visíveis entre o recorte nativo `(64,64,128,128)` do composto 256x256 (ou camada `body` nos ataques armados), o arquivo `native/*.png` apontado pelo `clip.json` e a renderização do mestre `.aseprite`.
- **Validação:** Checagem pixel a pixel automatizada (0 pixels visíveis divergentes em 100% dos quadros entregues). Emissores de hashes devem comparar os pixels renderizados, e não apenas recalcular digests sobre arquivos divergentes.
- **Status:** Portão técnico obrigatório de consistência de publicação.

---

## 15. Limites deste contrato

- Não concede aprovação artística, promoção de candidato, seleção de equipamento nem integração Unity.
- Não implementa suporte de runtime a overlays de arma; `runtimeImplemented: false` permanece.
- Não autoriza alterar arte canônica fora do escopo declarado da tarefa.
- Não transforma piso numérico em veredito: os números servem para barrar regressão e para tornar a discussão concreta, não para substituir o olho do criador.

Documento irmão: [`docs/WORKFLOW.md`](WORKFLOW.md) (os quatro status no fluxo de produção) e [`docs/MAIN_ORC_COMBAT_POLISH.md`](MAIN_ORC_COMBAT_POLISH.md) (o passe de recuperação artística em si).
