# Parecer de QA Temporal e Visual Independente — Candidato V6

**Veredito Global:** `TEMPORAL_PASS`  
**Status Artístico:** `VISUAL_REVIEW_COMPLETED`  
**Aprovação do Criador:** `PENDING_CREATOR` (Aprovação artística permanece exclusiva do criador)  
**Elegibilidade para Revisão do Criador:** `READY_FOR_CREATOR_REVIEW: true`  

---

## 1. Identificação do Objeto e Ambiente de Teste

- **Manifesto Auditado:** `characters/orc-v1/source/artistic-reconstruction-v6/candidate28manifest.json`
- **Hash SHA-256 do Manifesto:** `5d68b52d3e2b2a0931d689afb5a9dd438c178835d05efb02a5fb2bcf0c64b7ca`
- **Página de Inspeção:** `Biblioteca de Arte/Estudos Comparativos/Orc principal - Reconstrucao artistica/index.html`
- **Ambiente de Execução:** Navegador real — `Chromium Headless Shell 156.0.8078.4` (via Playwright / automação CDP em Windows); binário fallback `Microsoft Edge 156.0.4314.50` testado e operacional.
- **Data da Revisão:** 30 de Outubro de 2026
- **Propósito:** Preencher a lacuna declarada pelo parecer estático anterior (que marcou a percepção temporal como `NÃO VERIFICADO`), avaliando a qualidade cinética real, ritmo, peso, legibilidade e fluidez dos 8 ataques e transições do Orc V1.

---

## 2. Matriz de Execuções e Métricas de Playback

Todos os 8 ataques foram reproduzidos em velocidade normal (1×) e velocidade reduzida (0,5×), com passo de quadro integral (F00 até o quadro final), verificação tática (64 px) e teste de transição armada/desarmada (`idle-attack-idle`).

| Clipe | Duração | Quadros | Execuções 1× (Loops) | Execuções 0,5× (Loops) | Passo a Quadro | Intervalo da Arma | Veredito Temporal |
|---|---|---|---|---|---|---|---|
| `front_r/Sword` | 730 ms | 13 | 4 loops completos (3511 ms) | 2 loops completos (3008 ms) | 13 quadros verificados | F02..F10 (arma visível) | **TEMPORAL_PASS** |
| `front_l/Sword` | 730 ms | 13 | 4 loops completos (3507 ms) | 2 loops completos (3001 ms) | 13 quadros verificados | F02..F10 (arma visível) | **TEMPORAL_PASS** |
| `back_r/Sword` | 950 ms | 12 | 3 loops completos (3514 ms) | 1 loop completo (3009 ms) | 12 quadros verificados | F01..F09 (arma visível) | **TEMPORAL_PASS** |
| `back_l/Sword` | 950 ms | 12 | 3 loops completos (3509 ms) | 1 loop completo (3008 ms) | 12 quadros verificados | F01..F09 (arma visível) | **TEMPORAL_PASS** |
| `front_r/Axe` | 1005 ms | 12 | 3 loops completos (3526 ms) | 1 loop completo (3003 ms) | 12 quadros verificados | F02..F08 (arma visível) | **TEMPORAL_PASS** |
| `front_l/Axe` | 1005 ms | 12 | 3 loops completos (3534 ms) | 1 loop completo (3014 ms) | 12 quadros verificados | F02..F08 (arma visível) | **TEMPORAL_PASS** |
| `back_r/Axe` | 1320 ms | 12 | 3 loops completos (4636 ms) | 1 loop completo (3310 ms) | 12 quadros verificados | F01..F09 (arma visível) | **TEMPORAL_PASS** |
| `back_l/Axe` | 1320 ms | 12 | 3 loops completos (4627 ms) | 1 loop completo (3305 ms) | 12 quadros verificados | F01..F09 (arma visível) | **TEMPORAL_PASS** |

---

## 3. Investigação Específica dos Pontos Retificados

### 3.1. V6-QA-01: Axila de `front_l/Sword` (Quadros F03–F04)
- **Histórico:** Na versão anterior, foi apontada uma projeção preta espúria / acúmulo sob a axila nos quadros de armação F03–F04, que causava uma emenda visual desconfortável.
- **Avaliação em Movimento (1× e 0,5×):**
  - Inspecionei a sequência contínua F01 → F02 → F03 → F04 → F05.
  - No quadro F02, o braço está próximo ao torso; ao erguer o braço em F03 e F04 (antecipação e armação alta), a cavidade axilar se abre de forma anatomicamente coerente.
  - O espaço aberto exibe corretamente o acolchoamento avermelhado sob a armadura de placas, com contorno escuro limpo e sombra de contato proporcional.
  - Não há piscada, estalo ("popping"), descontinuidade ou resíduo de silhueta espúria durante a passagem contínua.
  - **Resultado:** **`CLOSED / TEMPORAL_PASS`**.

### 3.2. V6-QA-02: Ponta da Espada de `back_l/Sword` (Quadros F07–F09)
- **Histórico:** No candidato rejeitado anterior, a espada descia excessivamente nos quadros de recuperação, penetrando visualmente abaixo da linha do piso (`groundY = 190`).
- **Avaliação em Movimento (1× e 0,5×):**
  - A linha do solo canônica no canvas 256×256 é `groundY = 190` (correspondente ao apoio dos pés).
  - Medição física dos limites inferiores da lâmina nos quadros de descida e recuperação:
    - **F07:** vértice inferior da ponta da espada em `y = 187` (+3 px de folga acima do piso).
    - **F08:** vértice inferior da ponta da espada em `y = 185` (+5 px de folga acima do piso).
    - **F09:** vértice inferior da ponta da espada em `y = 173` (+17 px de folga acima do piso).
  - Em reprodução contínua (1×) e lenta (0,5×), a lâmina desacelera em diagonal, suspensa ao lado da perna direita, lendo claramente como um arco de recuperação livre no ar, sem jamais sugerir que a ponta colide ou se enterra no solo.
  - Em F10, a arma se desfaz conforme a regra `attack-only`, e o corpo retorna à guarda desarmada sem solavancos.
  - **Resultado:** **`CLOSED / TEMPORAL_PASS`**.

---

## 4. Avaliação Cinética e Artística das Quatro Famílias

### 4.1. Espadas Traseiras (`back_r/Sword` e `back_l/Sword`)
- **Continuidade do Corte:** O corte apresenta um arco nítido e legível em ambas as vistas:
  1. *Antecipação (F01–F03):* A mão estabelece a pegada na espada junto ao flanco/quadril e a ergue em diagonal ascendente.
  2. *Armação no Ombro (F04–F05):* A espada atinge o ápice atrás da ombreira.
  3. *Aceleração (F05–F06, 40 ms):* Golpe rápido de descida horizontal/oblíqua.
  4. *Impacto (F07–F08, 80 ms / 100 ms):* Extensão completa do golpe com linha de corte limpa.
  5. *Recuperação (F09–F11):* Desaceleração suave, remoção da arma e transição natural para a postura de guarda.
- **Cadeia Articular e Pegada:** A cadeia ombro-cotovelo-punho permanece unificada em todos os quadros. Não foi observada arma orbitando em torno de braço estático, nem saltos de pose ou membros se deformando.

### 4.2. Machados Traseiros (`back_r/Axe` e `back_l/Axe`)
- **Peso e Dinâmica Corporal:** 
  - O golpe do Machado de Milícia transmite impacto pesado e deliberado (1320 ms de duração total).
  - Diferente de animações mecânicas rígidas de "gangorra", o corpo inteiro participa: durante o ápice (F04–F05) o tronco estende, e na descida e impacto (F06–F08) há um afundamento perceptível do quadril e flexão ativa dos joelhos.
  - A base das pernas se alarga no impacto para absorver o peso do golpe.
- **Tamanho da Cabeça do Machado:** A proporção da cabeça do machado em relação ao cabo e à mão foi inspecionada quadro a quadro; ela se mantém estável e visualmente consistente em todo o ciclo, sem efeitos de dilatação ou encolhimento artificial.

### 4.3. Compatibilidade entre Vistas Traseiras (`back_r` vs `back_l`)
- Ambas as câmeras traseiras representam a mesma técnica e identidade de combate.
- A perspectiva de cada vista é autônoma: `back_r` (Norte-Leste) expõe o flanco direito e o dorso com iluminação vinda da frente-esquerda; `back_l` (Norte-Oeste) expõe a curvatura dorsal e a ombreira esquerda com perspectiva angular distinta.
- A iluminação respeita rigorosamente a luz superior-esquerda do padrão do projeto.
- Confirmado: não há espelhamento 2D simplista; trata-se de construção direcional tridimensional genuína.

### 4.4. Preservação dos Ataques Frontais (`front_r` e `front_l`)
- A coreografia frontal original, que já havia sido elogiada e mantida como baseline, permaneceu com tempos e movimentos byte-preservados.
- Os retoques localizados de limpeza de pixels isolados no corpo base eliminaram ruídos de contorno claro e pontos flutuantes, garantindo que o playback em 1× ocorra sem cintilações ou ruído visual nas bordas.

---

## 5. Inspeção em Escala Tática (64 px) e Prática (128 px)

- **Escala Prática (128×128, zoom = 0,5):** Perfeita legibilidade de todos os detalhes da armadura de placas, cota de malha, lâminas e expressões faciais.
- **Escala Tática de Jogo (64×64, zoom = 0,25):** 
  - Avaliada diretamente nos quadros de impacto e aceleração.
  - A silhueta do Orc guerreiro (massa muscular robusta, placas escuras, pele verde) e os arcos luminosos do aço da espada e do ferro do machado destacam-se imediatamente sobre o fundo com contraste adequado.
  - O sentido e a direção do ataque são imediatamente reconhecíveis em fração de segundo, atendendo aos requisitos de gameplay tático em grade.

---

## 6. Transições de Estado (`idle-attack-idle`)

- Testada a transição completa de combate: `Idle (sem arma) → Entrada e Ataque → Recuperação → Retorno a Idle`.
- Respeito estrito à política `attack-only-v1`:
  - Durante o ciclo Idle (2200 ms), as armas permanecem totalmente ocultas.
  - As armas aparecem exclusivamente durante o intervalo declarado do ataque (saque e golpe).
  - Após a recuperação do golpe, a arma desaparece e o personagem retoma a respiração cíclica sem descontinuidade na posição dos pés ou na massa corporal.

---

## 7. Limitações Metodológicas

- A inspeção temporal foi realizada em ambiente local através do Chromium Headless Shell (v156.0.8078.4) via Playwright, utilizando requisições reais de animação (`requestAnimationFrame`), medições de tempo de quadro em alta precisão (`performance.now`) e renderização em tela real.
- Embora a percepção de fluidez tenha sido verificada tanto por amostragem contínua em rAF quanto por inspeção visual direta de capturas e recortes dos quadros renderizados, **a aprovação artística final e soberana é exclusiva do criador humano**.

---

## 8. Conclusão e Veredito

Os defeitos temporais e cinemáticos que motivaram rejeições anteriores foram completamente sanados no candidato V6 (manifesto `5d68b52d...`). Os 8 ataques apresentam coreografia consistente, peso natural, cortes legíveis, ausência de clipping no solo e perfeita adesão às regras de direção e equipamento.

**Veredito:** **`TEMPORAL_PASS`**  
**Recomendação:** Promover o candidato V6 para avaliação visual do criador sob a página interativa de revisão (`Biblioteca de Arte/Estudos Comparativos/Orc principal - Reconstrucao artistica/index.html`).

*Nenhuma fonte de arte, código do jogo Unity ou arquivos fora do escopo de QA foram modificados durante esta inspeção.*
