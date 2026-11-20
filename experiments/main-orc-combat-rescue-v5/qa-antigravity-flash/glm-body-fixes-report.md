# Parecer de QA Independente — Correções Corporais GLM (`back_r/Sword` F06 & `back_l/Axe` F02)

**Documento:** `experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/glm-body-fixes-report.md`  
**JSON Estruturado:** `experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/glm-body-fixes-result.json`  
**Revisor:** Gemini 3.8 Flash (QA Independente via Antigravity)  
**Data:** 29 de Outubro de 2026  
**Checkpoint Avaliado:** `GLM_BODY_FIXES_READY`  
**Produtor do Pacote:** `15ef8466-7a3d-431c-baee-4abbf7da3698` (GLM 5.3 / Cline)  
**Status Técnico:** `TECHNICALLY_COMPLETE`  
**Vereditos por Clipe:**  
- `back_r/Sword`: **`READY_FOR_REAR_GRIPS`**  
- `back_l/Axe`: **`READY_FOR_REAR_GRIPS`**  
**Status Artístico Global:** `ARTISTIC_REVISION_REQUIRED` (*inalterado*)  
**Aprovação do Criador:** `PENDING_CREATOR`  

---

## 1. Escopo Delimitado e Contexto Operacional

Este parecer de QA independente avalia com inspeção multimodal direta a re-entrega das duas correções corporais traseiras no marco `GLM_BODY_FIXES_READY`, após as duas reprovações anteriores:
1. **`back_r/Sword` F06:** Correção dos defeitos residuais `DEFECT-REAR-01-RESIDUAL-A` (5 pixels flutuantes) e `RESIDUAL-B` (couro vinho espalhado sobre a cota de malha).
2. **`back_l/Axe` F02:** Correção do defeito persistente `DEFECT-REAR-02` (haste de madeira transversal sobre o trapézio/pescoço, pino vertical e bloco de couro no lugar da mão), que motivou a escalada de produtor.

### Fora de Escopo
- `back_l/Sword`: Já liberado anteriormente como `READY_FOR_REAR_GRIPS` e mantido intocado.
- `back_r/Axe`: Já avaliado e liberado como `READY_FOR_MATRIX_REVIEW`.
- Ciclos frontais, matriz canônica de 28 células e integração Unity.

---

## 2. Metodologia de Auditoria e Limite Visual Declarado

O produtor `15ef8466-7a3d-431c-baee-4abbf7da3698` declarou formalmente que operou **sem visão de imagem**, limitando-se a métricas textuais via Pillow e execução de scripts Lua no Aseprite, somado a um job de inpaint no PixelLab. Portanto, todas as asserções quantitativas do produtor (ex.: delta de 510 px, runs de feixe, etc.) foram tratadas neste laudo como meras hipóteses técnicas.

A auditoria deste revisor independente realizou **inspeção multimodal direta** de cada frame corrigido, suas camadas, zooms comparativos antes/depois, e exame de continuidade temporal com os quadros vizinhos imediatos.

---

## 3. Avaliação de `back_r/Sword` F06 (`DEFECT-REAR-01-RESIDUAL-A` & `B`)

### 3.1 Eliminação dos 5 Pixels Flutuantes (RESIDUAL-A)
- **Coordenadas Auditadas:** `(112,64)`, `(110,69)`, `(109,70)`, `(108,71)`, `(107,72)` no canvas nativo 128 (equivalentes a `[176,128]`, `[174,133]`, `[173,134]`, `[172,135]`, `[171,136]` no canvas 256).
- **Resultado Visual:** Os 5 pixels flutuantes foram convertidos para alfa = 0.
- **Integridade da Silhueta:** A limpeza não abriu nenhum buraco no contorno do antebraço ou no espaço livre circundante. O contorno da manopla e do punho é nítido e estanque.

### 3.2 Reconstrução da Cota de Malha (RESIDUAL-B)
- **Região Auditada:** `y = 88..94 / x = 45..55` no canvas nativo 128.
- **Resultado Visual:** Exatamente 30 pixels da família couro-vinho (`#592d2b`, `#34181e`, `#30171c`) foram substituídos pela textura de cota de malha de aço (`#413f4c` / `#1f1c24`), utilizando doadores das mesmas coordenadas dos quadros `F05` e `F07`.
- **Preservação de Vestimenta:** A aba do tasset de couro legítimo à esquerda (`x = 40..44`) foi preservada intacta.
- **Acabamento:** A emenda diagonal e a mancha avermelhada desapareceram. A saia de cota de malha apresenta padrão de entrelaçamento visualmente contínuo e homogêneo com o restante da armadura.

### 3.3 Preservação Estrutural do Clipe
- Os outros 11 quadros de `back_r/Sword` permanecem **100% byte-idênticos** à versão anterior.
- As três chaves aprovadas (`F03`, `F04`, `F07`) mantêm SHA-256 byte-idênticos.
- **Veredito para `back_r/Sword`:** **`READY_FOR_REAR_GRIPS`**.

---

## 4. Avaliação de `back_l/Axe` F02 (`DEFECT-REAR-02-PERSISTENT`)

### 4.1 Eliminação da Haste e Artefatos Espúrios
- **Haste Transversal e Pino:** A haste de madeira castanha escura (`y19 x76..90` e `y20 x73..87`) e o pino vertical sobre o pescoço (`x70..72, y16..18`) foram **totalmente removidos**.
- **Trapézio e Nuca:** O pescoço verde do Orc e a gola da couraça estão limpos, com transição anatômica correta e espaço negativo livre entre o crânio e a ombreira.

### 4.2 Reconstrução Anatômica do Braço Direito
- **Substituição do Bloco de Couro:** O bloco retangular amorfo (`x82..92, y15..20`) que fingia ser uma mão foi substituído por uma **luva de couro marrom genuinamente articulada**, com dedos cerrados, definição de nós e polegar travado.
- **Cadeia Articular Contínua:** O braço direito conecta-se organicamente a partir do ombro couraçado, passando pelo cotovelo fletido e antebraço com braçadeira de malha/aço, culminando no punho erguido na altura da cabeça.
- **Ausência de Amputação ou Buracos:** Não há descontinuidade na silhueta, transparência vazando no contorno ou dedos derretidos decorrentes do inpaint por IA.

### 4.3 Coerência Cinética na Sequência
A inspeção visual da transição `F01` &rarr; `F02` &rarr; `F03` comprova excelente dinâmica de preparação de ataque:
- **F01 (load-begin):** Braço direito estendido baixo, punho repousando próximo ao quadril.
- **F02 (elbow-hoist):** O cotovelo projeta-se para fora e o punho sobe até o nível do ombro/rosto em movimento preparatório ascendente.
- **F03 (validated-hoist):** O braço conclui o carregamento, içando o punho alto acima da cabeça.

### 4.4 Preservação Estrutural do Clipe
- Os outros 11 quadros de `back_l/Axe` permanecem **100% byte-idênticos** à versão anterior.
- As três chaves aprovadas (`F03`, `F04`, `F07`) mantêm SHA-256 byte-idênticos.
- **Veredito para `back_l/Axe`:** **`READY_FOR_REAR_GRIPS`**.

---

## 5. Tabela de Hashes SHA-256 dos Arquivos de Entrega

| Arquivo | Dimensão | SHA-256 Verificado em Disco | Status |
|---|---|---|---|
| `back_r-Sword-full/clip.json` | JSON | `aba36d665239bf6464d53bce2a50132ff24b6e1cdb246c7ab6039345a9dede88` | Validado |
| `back_r-Sword-full/body256.aseprite` | 256×256 (12f) | `3da678e9b7980074f08a8e0c5a89e22d9b1f771719cc5c9775cc4ecf81438303` | Validado |
| `back_r-Sword-full/native128.aseprite` | 128×128 (12f) | `acccc22600ce9d3b787dbb77ce02f9078b8382b099b2a7ee97e319437a24e27b` | Validado |
| `back_r-Sword-full/body256/06.png` | 256×256 | `14d17af1422597791bdf1653b77f6795fba39fba178e90a9e9ba159ef0362faf` | Corrigido |
| `back_r-Sword-full/native/06.png` | 128×128 | `88a125c47494c08db45551e12a115a9c2dc83344322afaf19e6cbdd892dba402` | Corrigido |
| `back_l-Axe-full/clip.json` | JSON | `d87cd8331b46e48e962ac118c01b0fd10d7ad86dcd101f7bc8f3e6093f539ef2` | Validado |
| `back_l-Axe-full/body256.aseprite` | 256×256 (12f) | `8358307076f7b54bc050448bfe0e0fefbe602d2eb10ec703ba5d552a093809e5` | Validado |
| `back_l-Axe-full/native128.aseprite` | 128×128 (12f) | `9df41216491bcf32df7cab92f31e045ba32caedc8cdbbefa3c044497f2cccdc9` | Validado |
| `back_l-Axe-full/body256/02.png` | 256×256 | `97d6438914b434c76b92ffcc040c59800fc48bc96db4073fb118e69b56ddcf63` | Corrigido |
| `back_l-Axe-full/native/02.png` | 128×128 | `9cf40e9477fbaf361e6c38234ea7c37a77ec818987eb733b8a1ec5a7a7bc9b6c` | Corrigido |

---

## 6. Limitações Críticas da Avaliação

1. **Inspeção Estática e Tiras vs Percepção 1× ao Vivo:** A avaliação foi realizada por inspeção multimodal estática e comparativa de quadros e tiras. A apreciação em tempo real contínuo no motor de jogo final permanece como critério da matriz integrada.
2. **Escopo Restrito aos Dois Corpos Reparados:** Este veredito aprova a geometria e o acabamento dos corpos desarmados (`layers-off`). As camadas de armas e pegadas correspondentes para estes clipes ainda devem ser construídas e submetidas.
3. **Aprovação do Criador:** O status geral permanece estritamente `ARTISTIC_REVISION_REQUIRED`, pendente de aprovação final do criador (`PENDING_CREATOR`).

---

## 7. Veredito Final e Próximos Passos

- **`back_r/Sword`:** **`READY_FOR_REAR_GRIPS`**
- **`back_l/Axe`:** **`READY_FOR_REAR_GRIPS`**
- **Veredito Consolidado do Pacote:** **`READY_FOR_REAR_GRIPS`**
- **Recomendação ao Root / Orquestrador:**
  - Com a aprovação destes dois corpos reparados, somada à liberação prévia de `back_l/Sword` e `back_r/Axe`, **todos os 4 corpos traseiros de combate (`full-rear-bodies`) estão agora plenamente aprovados para receber suas respectivas pegadas de armas**.
  - O especialista de pegada pode ser acionado para estender os grips traseiros pendentes (`back_r/Sword`, `back_l/Sword`, `back_l/Axe`).
- **Contabilidade de Recursos:**
  - Chamadas PixelLab de produção nesta revisão pelo QA: **0**
  - Custo de inferência LLM: **Não informado**
  - Consumo do produtor auditado nos recibos: 1 job PixelLab inpaint (`-6.0` créditos, saldo `1342.70` &rarr; `1336.70`).
  - Modificações em arte / Unity / Git: **Nenhuma**.