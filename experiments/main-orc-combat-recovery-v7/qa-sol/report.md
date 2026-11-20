# V7 — rejeição do criador e localização forense

**Veredito final: ARTISTIC_REJECTED. Autoridade: CRIADOR.**

Status operacional: ARTISTIC_REVISION_REQUIRED. Aprovação do criador: REJECTED. Missão: localização de defeitos, sem aprovação ou liberação do pacote.

Freeze: `fde1fe23f2d637589b6abef6b9b946b6c4370cc8ae5f3927525fb038397b2579`.

O criador examinou a página V7 e determinou: os problemas de frame pioraram; o flash da espada **FRONTAL** continua; o ataque de costas está **MENOS uniforme** que antes. Essa decisão substitui o parecer anterior. Os arquivos pre-creator-rejection-* preservam o histórico, sem validade corrente de aprovação.

## Mapa forense

| Defeito | Célula / transição | Região e evidência | Grau de certeza |
|---|---|---|---|
| Flash frontal persistente | front_r/Sword F11→F12 | Corpo, x94..161/y86..180 composto; 317 pixels candidatos. Arma já oculta. | Defeito confirmado pelo criador; localização desta ocorrência é candidata. |
| Flash frontal persistente | front_l/Sword F11→F12 | Corpo, x94..159/y86..180 composto; 265 pixels candidatos. Arma já oculta. | Mesma distinção. |
| Entrada frontal a investigar | front_r e front_l/Sword F00→F01 | Respectivamente x93..108/y103..145 e x148..160/y103..144; 71/39 pixels candidatos. | Candidato secundário, não flash provado. |
| Mudança de pose frontal | front_r e front_l/Sword F02→F03 | Respectivamente x77..167/y86..174 e x88..170/y86..174; 284/243 candidatos. | Movimento pode explicar a contagem; não classificar automaticamente como defeito. |
| União manga/ombreira e volume do braço | back_l/Sword e back_l/Axe F03/F04 contra F06/F09 | ROI nativa x86..116/y30..58: abertura estreita, membro depois espesso/curvo. Body-only torna o problema legível. | Achado visual estático independente, compatível com a rejeição. |
| Técnica menos uniforme | back_l/Sword e back_l/Axe F06→F10, comparados por fase aos frontais e back_r | Palma Sword ápice [100,19], contato [109,81]; Axe [95,15]→[101,76], nativo. Trajetória exterior sem cruzamento corporal convincente. | Achado estático localizado; piora temporal global é relato do criador, não medição deste QA. |

As coordenadas compostas usam canvas 256; nativas usam 128. Somar [64,64] para converter nativo em composto. As caixas do detector delimitam todos os hits da transição e podem incluir regiões distintas; não são contornos de um único flash.

## Flash frontal: procedimento e hipótese

[Hotspots completos](frontal-flash-hotspots.json) lista cada pixel e luminância antes/depois nas camadas body, weaponFront e handFront. Detector: max(luma antes,depois) ≥130 e |delta| ≥40; pixels transparentes tratados como luminância zero. Esses limiares servem apenas para localizar mudanças claras. Deslocamento normal de um metal claro também os dispara.

[Retorno body-only](frontal-return-body.png): primeira linha front_r, segunda front_l; colunas F10/F11/F12. A transição F11→F12 altera pose e distribuição de luz do corpo em ambas as vistas. Como o equipamento está oculto, a hipótese prioritária para esta transição é a troca do corpo/material no retorno, e não um efeito da lâmina sobreposta. **Não está comprovado que esse seja o instante exato do flash relatado nem sua causa raiz.** Inspecionar também as mudanças da arma em frontal-flash-hotspots.json durante o golpe.

A correção medida anteriormente nos bookends **traseiros** não responde ao flash **frontal**. Contorno já existente no V5 e preservação byte a byte não demonstram ausência de defeito. O negativo estático anterior sobre contornos frontais não deve ser usado para encerrar essa objeção.

## Costas: localização para reparo

[Chaves Sword](Sword-keys.png), [chaves Axe](Axe-keys.png), [corpo Sword](Sword-body.png), [corpo Axe](Axe-body.png). Linhas: front_r/front_l/back_r/back_l. Na linha back_l, colunas F03/F06/F07/F09/F10. Abertura F03 e contato F09/F10 concentram os contrastes de volume/ligação; comparar a execução completa por fase antes de alterar mais frames. Os marcos anatômicos são referências declaradas nos clipes, não uma reconstrução 3D comprovada.

Os dados anteriores de hashes, chão e transparência seguem válidos apenas como integridade técnica. Não compensam a rejeição e não encerram nenhum defeito artístico.

## Limites e estado final

Sem navegador disponível para percepção contínua nesta sessão: 1×, 0,5× e escala tática temporal continuam NÃO VERIFICADO pelo agente. O relato perceptivo do criador é a autoridade da rejeição; não depende de reprodução pelo QA. Nenhuma nova aprovação foi emitida. Nenhuma arte, fonte, manifesto ou Unity foi alterada; saídas restritas a qa-sol. Zero PixelLab, sem subagentes, custo LLM não informado.
