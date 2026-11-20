# Relatório de QA Independente — Orc V1 Resgate de Combate V5

**Data / Hora:** 2026-10-29T15:17:00Z  
**Papel:** QA Independente (fora do Copilot / não orquestração / não produção)  
**Modelo Revisor:** Gemini 3.8 Flash (High) via Antigravity  
**Veredito Global:** `READY_FOR_NEXT_STAGE`  
**Status Artístico Global da Tarefa:** `ARTISTIC_REVISION_REQUIRED` (preservado; pendente aprovação explícita do criador)  
**Status do Criador:** `PENDING_CREATOR`  
**Aprovação Artística Automática:** NÃO CONCEDIDA (reservada exclusivamente ao criador)  
**Implementação Unity / Promoção Runtime:** `runtimeImplemented: false` (nenhuma escrita em `../TacticsRPG`)  

---

## 1. Escopo e Objeto de Julgamento

Julgamento técnico e perceptual independente de **6 pacotes de arte novos** entregues pelos especialistas gratuitos substitutos:

1. **Especialista Corporal (`d145b472-8f98-4d77-ab3b-00199c10ab9f`):**
   - 9 chaves anatômicas estruturais dos 3 clipes traseiros faltantes (3 chaves × 3 corpos):
     - `back_r/Sword-keys` (01-hoist, 02-apex, 03-impact)
     - `back_l/Sword-keys` (01-hoist, 02-apex, 03-impact)
     - `back_l/Axe-keys` (01-hoist, 02-apex, 03-impact)
   - Escopo estritamente desarmado (`layers-off`), sem intermediários.

2. **Especialista de Pegada (`438383d1-01dc-4b15-bf23-59161355cbb8`):**
   - 3 ciclos frontais completos equipados restantes:
     - `front_l/Sword-full` (13 quadros / 730 ms)
     - `front_r/Axe-full` (12 quadros / 1005 ms)
     - `front_l/Axe-full` (12 quadros / 1005 ms)
   - Corpos frontais legados 100% preservados (`allBodyRgbaDelta: 0`); camadas de empunhadura e equipamento autênticas.

---

## 2. Metodologia de Percepção Visual e Limitações

- **Inspeção Visual Real de PNGs:** A inspeção foi realizada diretamente via decodificação de imagem multimodal em resolução nativa (128×128), tiras de contato (`native-strip.png`, `composite-strip.png`), ampliações diagnósticas (8× em `preview-native.png`) e escala tática de jogo (64×64 em `preview-tactical.png`).
- **Nenhuma Simulação por Bounding Box / Hash:** Conforme exigido pela política, bounding boxes e hashes SHA-256 serviram unicamente como verificação de integridade cadastral e congelamento, nunca como substituto de julgamento estético ou perceptual de anatomia.
- **Limitação Temporal Declarada:** Não foi realizada observação contínua de reprodução a 1× em tempo real em navegador/player integrado em tempo contínuo (interface opera por captura e quadro-a-quadro discreto). Conforme decisão formal do Root, a ausência de percepção contínua 1× em runtime não constitui defeito de pixels e não bloqueia a progressão das fases, devendo a fluidez final contínua ser verificada pelo criador.

---

## 3. Matriz de Hashes Exatos dos Pacotes Inspecionados

| Pacote | Arquivo | SHA-256 |
|---|---|---|
| `body-specialist/back_r-Sword-keys` | `clip.json` | `95b9804fc02261daf6ada633dc9758278d09e2b0fd0a3e38c868a6f37c48b81d` |
| `body-specialist/back_r-Sword-keys` | `representative.json` | `7c72785fc8f4605dfdf6f2ee51392da3ef564344a37f79763b9441e3f4ed522c` |
| `body-specialist/back_l-Sword-keys` | `clip.json` | `39b2f8b36927d856c5515bf4ec032854954ebd4bfe79ea332ed165fb5fa0a41b` |
| `body-specialist/back_l-Sword-keys` | `representative.json` | `c43b1f38af22905a05505dcaaa726f063f40949d31f037cf02123e4e4de5af22` |
| `body-specialist/back_l-Axe-keys` | `clip.json` | `82362afc408be95ba51ad49da6d113cdd012ef7ce677463a972bc1f1a97c4c45` |
| `body-specialist/back_l-Axe-keys` | `representative.json` | `da23e428b6d4eadd6d13bffc5c7c43604679a9efda512685457631d9879fe485` |
| `grip-specialist/front_l-Sword-full` | `clip.json` | `56eb4daeb43b35cbb0a50a3b1cc145eba802c5b408b96bf76fa90c3219eb4681` |
| `grip-specialist/front_l-Sword-full` | `representative.json` | `baa4c3c4cc37fa150662e5116aa824395de17b6a73423aa5f91677ced9c85041` |
| `grip-specialist/front_l-Sword-full` | `master.aseprite` | `3efc83c1a17fa45e7f34ea3af985255b2820c924fcfcf76be15095d9dec1e085` |
| `grip-specialist/front_r-Axe-full` | `clip.json` | `dca0ef7e000be50cf8cf39ca69c3b55324ea1a4857a18e1b15278bbae6e3d0f5` |
| `grip-specialist/front_r-Axe-full` | `representative.json` | `4542bbb8ae77ca526d3f5a4d913c4d73cfc30446b21341540955dccb50a35925` |
| `grip-specialist/front_r-Axe-full` | `master.aseprite` | `83f73413521dc5357161423d5d88b55604f316fcc29ba834ea0b5bbd63dd039e` |
| `grip-specialist/front_l-Axe-full` | `clip.json` | `fa3c620d69d7df05bf0afab1fffa35fe37d861feacfc4124cbafa7e9763d7c5c` |
| `grip-specialist/front_l-Axe-full` | `representative.json` | `09c2b3189f0e5adeee682a0a7fcc2ab848c31a7b8c4a40a1ec5db40dfa7befcd` |
| `grip-specialist/front_l-Axe-full` | `master.aseprite` | `4df2d168a97a7a643be47f2b57d85f260a1a9951324a3f9dbe7ab4107ce08938` |

---

## 4. Avaliação Individual dos 6 Pacotes

### 4.1. `body-specialist/back_r-Sword-keys` (3 Chaves Anatômicas Traseiras)
- **Veredito:** `READY_FOR_NEXT_STAGE`
- **Inspeção de Quadros:** `NO_BLOCKING_STATIC_DEFECT_OBSERVED`
- **Análise Anatômica e Cinemática:**
  - **Mão Dominante:** Destro anatômico autêntico. Na perspectiva `back_r` (voltado para nordeste), o braço dominante direito localiza-se à direita da tela.
  - **Arco de Movimento da Espada:** Na chave 01 (hoist), o braço direito é erguido junto ao ombro/nuca com cotovelo flexionado e punho fechado; na chave 02 (apex), o braço projeta-se em corte lateral diagonal para a frente; na chave 03 (impact/follow-through), o corte completa-se baixo junto ao quadril direito.
  - **Braço Inativo (Esquerdo):** Não é cópia congelada. Flexiona o cotovelo e ajusta a angulação nas três chaves para contra-balancear a rotação do tronco.
  - **Resolução do Defeito BODY-01:** O punho direito na chave 03 não está fundido como massa escura ou amputado. Há clara delimitação cromática e geométrica entre a manopla de couro vinho-marrom e as placas da coxa/tasset.
  - **Construção Traseira:** Crânio occipital verde sem vestígios faciais, crista vertebral na placa dorsal, gola alta, cinto traseiro horizontal sem fivela esternal.
- **Métricas Técnicas:** `maxY = 126` em nativo 128; `maxY = 190` em composto 256; 0 pixels de halo (`RGB > 190`).
- **Sugestão Segura para Próxima Fase:** Na interpolação dos intermediários, manter a transição diagonal contínua do punho direito entre o ápice (02) e a finalização (03), sem quedas abruptas de velocidade angular.

---

### 4.2. `body-specialist/back_l-Sword-keys` (3 Chaves Anatômicas Traseiras)
- **Veredito:** `READY_FOR_NEXT_STAGE`
- **Inspeção de Quadros:** `NO_BLOCKING_STATIC_DEFECT_OBSERVED`
- **Análise Anatômica e Cinemática:**
  - **Mão Dominante:** Destro anatômico autêntico. Na perspectiva `back_l` (voltado para noroeste), o ombro direito do personagem está virado para o observador (lado direito da tela). O braço ativo é o direito.
  - **Arco de Movimento:** Chave 01 prepara o golpe com punho erguido na altura do pescoço; chave 02 estende o golpe diagonalmente à frente; chave 03 recolhe a espada na finalização junto ao flanco.
  - **Braço Inativo (Esquerdo):** Estende-se para baixo/frente como contrapeso com ombreira pontiaguda e manopla autêntica.
  - **Construção e Isolamento:** Camada única `body`, sem contaminação por lâminas desenhadas no tronco ou cintura.
- **Métricas Técnicas:** `maxY = 126` (nativo 128), `maxY = 190` (composto 256); 0 pixels de halo.
- **Sugestão Segura para Próxima Fase:** Preservar a curvatura dorsal convexa no meio da rotação para manter a sensação de massa do guerreiro orc.

---

### 4.3. `body-specialist/back_l-Axe-keys` (3 Chaves Anatômicas Traseiras)
- **Veredito:** `READY_FOR_NEXT_STAGE`
- **Inspeção de Quadros:** `NO_BLOCKING_STATIC_DEFECT_OBSERVED`
- **Análise Anatômica e Cinemática:**
  - **Mão Dominante:** Destro anatômico (braço direito na chave 01 hoist acima da cabeça; chave 02 apex arqueado sobre o crânio; chave 03 golpe pesado para baixo).
  - **Verificação do Espaço Negativo Refinado (Lição 17):** Confirmada a eliminação completa dos 94 pixels cinzentos na cavidade entre o crânio, gola e o antebraço arqueado na chave 02 (`02-native.png`). O contorno do crânio e da manopla estão intactos contra o fundo transparente.
  - **Entrega de Peso e Apoio (Heavy Impact):** Na chave 03, o impacto não é mera rotação de braço: a cabeça e o pescoço abaixam, a armadura do dorso comprime-se, as pernas flexionam e o quadril afunda, transmitindo a inércia do machado pesado ao solo.
- **Métricas Técnicas:** `maxY = 126` (nativo 128), `maxY = 190` (composto 256); 0 pixels de halo.
- **Sugestão Segura para Próxima Fase:** Para manter a semiótica de peso do machado de milícia, a descida do ápice (02) ao impacto (03) nos intermediários deve concentrar a aceleração no terço final (menos frames no ar, quadro de impacto com firmeza cravada no solo).

---

### 4.4. `grip-specialist/front_l-Sword-full` (Ciclo Completo Equipado 13f / 730ms)
- **Veredito:** `READY_FOR_NEXT_STAGE`
- **Inspeção de Quadros:** `NO_BLOCKING_STATIC_DEFECT_OBSERVED`
- **Análise da Empunhadura e Camadas:**
  - **Preservação do Corpo:** 100% dos 13 quadros possuem `bodyRgbaDelta: 0` em relação ao corpo canônico legado.
  - **Autenticidade da Manopla:** A camada `handFront` cobre os dedos sobre o cabo. Em 8× e em escala tática, a empunhadura passa sob a luva de couro autêntica; a guarda e o pomo permanecem perfeitamente legíveis.
  - **Cadeia Articular:** Conexão contínua entre dedos, palma, punho e antebraço; ausência de carimbos flutuantes ou máscaras desconectadas.
  - **Intervalo da Arma:** Arma estritamente visível em `visibleInterval: [2..10]`; frames 0, 1, 11 e 12 possuem camadas de arma 100% transparentes (alpha 0).
- **Métricas Técnicas:** 13 quadros, 730 ms, `groundY = 190`.
- **Sugestão Segura:** Aprovado para montagem no patch da matriz; verificação de fluidez 1× contínua remetida ao estúdio/criador.

---

### 4.5. `grip-specialist/front_r-Axe-full` (Ciclo Completo Equipado 12f / 1005ms)
- **Veredito:** `READY_FOR_NEXT_STAGE`
- **Inspeção de Quadros:** `NO_BLOCKING_STATIC_DEFECT_OBSERVED`
- **Análise da Empunhadura e Camadas:**
  - **Preservação do Corpo:** `allBodyRgbaDelta: 0` em todos os 12 quadros.
  - **Autenticidade da Manopla:** A haste de madeira do machado é empunhada sob a luva autêntica. No ápice (F04), a cabeça de ferro fica firmemente sustentada acima do punho fechado; no impacto pesado (F06), a pegada acompanha o vetor de força sem separação.
  - **Braço Ativo vs Inativo:** Tracé anatômico verificado; ausência de inversão de membros.
  - **Intervalo da Arma:** Arma visível estritamente em `visibleInterval: [2..8]`; oculta em 0, 1, 9, 10, 11.
- **Métricas Técnicas:** 12 quadros, 1005 ms, `groundY = 190`.
- **Sugestão Segura:** Aprovado para inclusão no patch de revisão.

---

### 4.6. `grip-specialist/front_l-Axe-full` (Ciclo Completo Equipado 12f / 1005ms)
- **Veredito:** `READY_FOR_NEXT_STAGE`
- **Inspeção de Quadros:** `NO_BLOCKING_STATIC_DEFECT_OBSERVED`
- **Análise da Empunhadura e Camadas:**
  - **Preservação do Corpo:** `allBodyRgbaDelta: 0` em todos os 12 quadros.
  - **Autenticidade da Manopla:** O cabo do machado passa naturalmente sob os dedos da luva em todas as poses de ataque (F02 a F08). Sem máscaras genéricas parametrizadas ou artefatos de recorte.
  - **Leitura em Escala de Jogo:** Em 64px, a cabeça do machado, a silhueta da armadura e o arco do golpe apresentam contraste nítido e legibilidade imediata.
  - **Intervalo da Arma:** Arma oculta na preparação (F00, F01) e recuperação (F09..F11).
- **Métricas Técnicas:** 12 quadros, 1005 ms, `groundY = 190`.
- **Sugestão Segura:** Aprovado para montagem no patch de candidatos.

---

## 5. Contabilidade de Recursos

- **Gerações PixelLab de Produção:** 0 chamadas PixelLab de produção nesta revisão.
- **Custo Monetário / Tokens LLM:** Custo LLM não informado (preço e tokens de provedor não estimados nem inventados como $0.00).
- **Modificações em Arquivos de Produção:** Nenhuma. Nenhum arquivo original foi alterado. Nenhum subagente foi invocado.

---

## 6. Conclusão e Próximos Passos

1. **Julgamento Conclusivo:** Todos os 6 novos pacotes satisfazem os critérios anatômicos, técnicos e de empunhadura, recebendo o veredito unânime de `READY_FOR_NEXT_STAGE`.
2. **Encaminhamento Operacional:**
   - **Chaves Traseiras:** O especialista corporal está liberado para a criação dos quadros intermediários (*in-betweens*) das 3 coreografias traseiras avaliadas (`back_r/Sword`, `back_l/Sword`, `back_l/Axe`).
   - **Pegadas Frontais:** Os 3 ciclos frontais equipados (`front_l/Sword`, `front_r/Axe`, `front_l/Axe`) estão prontos para compor o pacote patch de candidatos para inspeção na interface de revisão interativa e avaliação final do criador.
3. **Preservação de Governança:** 0 chamadas PixelLab de produção nesta revisão; custo LLM não informado. O status do pacote permanece estritamente `ARTISTIC_REVISION_REQUIRED (PENDING_CREATOR)` até que o criador aprove formalmente o resultado integrado.
