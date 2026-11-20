# Relatório de QA Independente — Quatro Ciclos Traseiros Desarmados Orc V1

**Data / Hora:** 2026-10-29T16:15:30Z  
**Papel:** QA Independente (fora do Copilot / não orquestração / não produtor)  
**Modelo Revisor:** Gemini 3.8 Flash (High) via Antigravity  
**Veredito Global:** `REVISIONS_REQUIRED`  
**Status Artístico Global da Tarefa:** `ARTISTIC_REVISION_REQUIRED` (Preservado / Inalterado)  
**Status do Criador:** `PENDING_CREATOR`  
**Aprovação Artística Automática:** NÃO CONCEDIDA (reservada exclusivamente ao criador)  
**Implementação Unity / Promoção Runtime:** `runtimeImplemented: false` (nenhuma escrita em `../TacticsRPG`)  
**Arquivo Estruturado:** [`full-rear-bodies-result.json`](file:///C:/Users/Jo%C3%A3o%20Orlando/Documents/Projetos%20Unity/TacticsRPG-CharacterFactory/experiments/main-orc-combat-rescue-v5/qa-antigravity-flash/full-rear-bodies-result.json)

---

## 1. Escopo e Objeto de Avaliação

Avaliação independente de **quatro ciclos completos traseiros desarmados** (12 quadros cada, camada única `body`):
1. `back_r-Sword-full` (12f / 730 ms) — Entrega nova (`3c2b5bd7`)
2. `back_l-Sword-full` (12f / 730 ms) — Entrega nova (`3c2b5bd7`)
3. `back_l-Axe-full` (12f / 1100 ms) — Entrega nova (`3c2b5bd7`)
4. `full-back-r-axe` (12f / 1100 ms) — Ciclo canônico prévio preservado

---

## 2. Matriz de Hashes e Vereditos por Ciclo

| Ciclo | Direção / Ação | Duração / Quadros | SHA-256 do `clip.json` | Veredito |
|---|---|---|---|---|
| `back_r-Sword-full` | `back_r` / Sword Attack | 730 ms / 12f | `aa676dec82400f5d7d9a64823fe4a21963e82387ec98fb58f89a843221edbbc9` | **`REVISIONS_REQUIRED`** |
| `back_l-Sword-full` | `back_l` / Sword Attack | 730 ms / 12f | `6da82bacaeb1b2ebea97adddc62ddc632f0bcf8eb099f11aa3232b6bdf25555f` | **`REVISIONS_REQUIRED`** |
| `back_l-Axe-full` | `back_l` / Axe Attack | 1100 ms / 12f | `88ecfde6b588f0c63c5d915a2ad68230e58448c832db6924dec58cdbff288cc9` | **`REVISIONS_REQUIRED`** |
| `full-back-r-axe` | `back_r` / Axe Attack | 1100 ms / 12f | `2ab5ae40d7a11c0b4b271ca41f090608c3d721366da90ee1c6d1ebce9c1321c3` | **`READY_FOR_REAR_GRIPS`** |

---

## 3. Verificação de Preservação das Chaves Aceitas

As nove chaves estruturais aprovadas anteriormente foram auditadas em seus índices nos 3 novos ciclos completos (`03.png` = hoist, `04.png` = apex, `07.png` = impact):

- `back_r-Sword-full`: F03, F04 e F07 apresentam **100% de correspondência byte-a-byte e pixel-a-pixel** com as chaves aceitas.
- `back_l-Sword-full`: F03, F04 e F07 apresentam **100% de correspondência byte-a-byte e pixel-a-pixel**.
- `back_l-Axe-full`: F03, F04 e F07 apresentam **100% de correspondência byte-a-byte e pixel-a-pixel** (incluindo o espaço negativo de 94px limpo em F04).

As fundações das chaves estruturais foram integralmente mantidas. Os defeitos encontrados concentram-se estritamente nos **quadros intermediários novos** (*in-betweens*).

---

## 4. Defeitos Críticos Confirmados nos Intermediários

| ID | Severidade | Ciclo / Quadro | Sintoma | Evidência Perceptual e Cromática | Causa Raiz | Impacto / Risco | Sugestão Segura de Reparo |
|---|---|---|---|---|---|---|---|
| **DEFECT-REAR-01** | **HIGH** | `back_r-Sword-full` / **F06** | Contaminação por rastro/lâmina de espada pintada sobre o corpo desarmado. | **272 pixels claros** (`rgba > 180, 180, 180, 255`) formando um arco curvo de corte (*swoosh*) que desce do ombro direito (x:105, y:20) cruzando o flanco, cota de malha e perna direita até (x:30, y:110). | A geração da ponte de descida (F04→F07) no PixelLab alucinou um efeito visual de corte diretamente no prompt, não removido na montagem. | Violação estrita da política `layers-off` (Lição 15). Ao sobrepor a espada e os efeitos independentes na etapa seguinte, haverá duplicação de lâmina e artefatos de colisão fantasma. | Limpeza cirúrgica local em Aseprite: converter os 272 pixels do rastro para alfa 0 ou restaurar os pixels subjacentes da armadura a partir de F05/F07. **Custo: 0 créditos PixelLab.** |
| **DEFECT-REAR-02** | **HIGH** | `back_l-Axe-full` / **F02** | Contaminação direta por arma: cabeça de machado e cabo repousando no ombro. | Perfil nítido de lâmina de machado em ferro (x:85..108, y:10..22) e cabo de madeira marrom (x:70..85, y:18..24) empunhado no ombro direito. | O quadro intermediário de entrada F02 gerou o orc apoiando um machado no ombro; foi empacotado sem higienização `layers-off` (idêntico ao defeito histórico QA-02). | Violação de `layers-off`. Causa aparição súbita de um machado em F02 que some abruptamente em F03 (hoist desarmado), e duplicará a silhueta quando a camada `weaponFront`/`weaponBack` for acoplada. | Apagar o machado e o cabo em F02 no Aseprite; reautorar a manopla direita como punho fechado desarmado erguendo-se em direção a F03. **Custo: 0 créditos PixelLab.** |
| **DEFECT-REAR-03** | **MEDIUM** | `back_l-Sword-full` / **F05** | Filamento/gancho preto saliente saindo do contorno do ombro para o ar. | **7 pixels pretos** verticais em x:95..96, y:28..33 projetando-se no espaço vazio entre a ombreira direita e o punho. Presente apenas em F05 (ausente em F04 e F06). | Artefato de interpolação residual não limpo na silhueta (idêntico a QA-04). | Pisca visualmente por 1 quadro durante a descida rápida do golpe, quebrando a limpeza do contorno. | Apagar cirurgicamente os 7 pixels do filamento no Aseprite, preservando a transparência natural da cavidade. **Custo: 0 créditos PixelLab.** |

---

## 5. Análise de Transições e Cinemática

### 5.1. `full-back-r-axe` (Ciclo Aprovado: `READY_FOR_REAR_GRIPS`)
- **F00→F03 (Entrada e Hoist):** Antecipação e subida contínua do braço direito até o hoist erguido; braço esquerdo ajusta naturalmente como contrapeso.
- **F04→F07 (Ápice e Descida Pesada):** O arco do machado desce verticalmente com aceleração progressiva; em F07 (impacto), o peso é absorvido pelo corpo inteiro (compressão cervical, afundamento do quadril e flexão dos joelhos). A manopla direita no impacto mantém separação legível em relação à coxa (reparo `repair1` preservado).
- **F07→F11 (Recuperação):** O corpo reergue-se com estabilidade e retorna à postura neutra sem estalos ou membros congelados.
- **Conclusão:** Nenhum defeito estático ou cinemático bloqueante. Apto para receber camadas de pegada e equipamento.

### 5.2. `back_r-Sword-full`
- **F00→F04:** Preparação e subida limpas; corpo preserva construção dorsal autêntica.
- **F05→F07:** Bloqueado pelo **DEFECT-REAR-01** (rastro branco de 272 pixels em F06). Tirando esse artefato sobreposto, a mecânica da descida e o término baixo em F07 (com manopla separada da armadura) são promissores.
- **F07→F11:** Recuperação fluida e retorno estável à guarda.

### 5.3. `back_l-Axe-full`
- **F00→F03:** Bloqueado pelo **DEFECT-REAR-02** (machado desenhado no ombro em F02). A transição F01 (desarmado) → F02 (armado no ombro) → F03 (desarmado erguido) constitui quebra inaceitável de continuidade.
- **F04→F07:** A descida a partir do ápice e a entrega de peso no solo em F07 funcionam muito bem; a cavidade do crânio em F04 mantém-se limpa.
- **F07→F11:** Recuperação pesada e consistente.

### 5.4. `back_l-Sword-full`
- **F00→F04:** Progressão diagonal coerente para visão noroeste; braço dominante direito nítido.
- **F05→F07:** Apresenta o **DEFECT-REAR-03** (filamento de 7 pixels em F05). A dinâmica geral do corte diagonal e o impacto em F07 respeitam a anatomia do Orc V1.
- **F07→F11:** Recuperação e reequilíbrio articular consistentes.

---

## 6. Limitações Perceptuais

- A análise de movimento foi conduzida quadro a quadro e em tiras sequenciais discretas em escalas 128×128 (nativa) e 64×64 (tática).
- Não foi observada reprodução contínua a 1× em tempo real em navegador/player contínuo. Conforme diretrizes formais do Root, essa limitação de interface é conhecida, transparente e não invalida o diagnóstico de pixels acima.

---

## 7. Contabilidade de Recursos

- **Gerações PixelLab de Produção:** 0 chamadas consumidas neste QA.
- **Custo Monetário / Tokens LLM:** Custo LLM não informado (preço e tokens de provedor não estimados nem inventados como $0.00).
- **Edição de Arquivos de Arte:** Nenhuma. Todos os arquivos de arte originais permanecem intactos.

---

## 8. Encaminhamento e Próximos Passos

1. **Vereditos:**
   - `full-back-r-axe`: **`READY_FOR_REAR_GRIPS`** (pronto para receber as camadas de pegada/equipamento).
   - `back_r-Sword-full`: **`REVISIONS_REQUIRED`** (aguarda limpeza do rastro F06).
   - `back_l-Axe-full`: **`REVISIONS_REQUIRED`** (aguarda remoção do machado em F02).
   - `back_l-Sword-full`: **`REVISIONS_REQUIRED`** (aguarda remoção do filamento em F05).
2. **Plano de Correção Segura para o DEV:**
   - Todos os três reparos são estritamente locais no Aseprite (máscara/apagador em batch Lua), **sem nenhuma nova chamada ou gasto de créditos no PixelLab**.
   - Após a limpeza cirúrgica dos quadros F06 (`back_r/Sword`), F02 (`back_l/Axe`) e F05 (`back_l/Sword`), o pacote de 4 corpos traseiros estará apto a receber a integração das 4 pegadas traseiras independentes pelo Root.
