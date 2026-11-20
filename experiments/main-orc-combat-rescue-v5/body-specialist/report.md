# Orc V1 — especialidade corporal / três chaves back_r Axe

**BODY_AXE_KEYS_READY**. Empacotamento **TECHNICALLY_COMPLETE**; arte **VISUAL_REVIEW_REQUIRED**, sem parecer independente ou aprovação do criador. Matriz global permanece **ARTISTIC_REVISION_REQUIRED / PENDING_CREATOR**. Não propagar.

Entregues três mestres nativos 128 e seus três mestres compostos 256, com exports separados. Chaves: preparação/hoist, ápice pré-descida, impacto/follow-through. Corpo desarmado, punhos vazios; nenhuma arma ou camada de pegada adicionada. Ground126/190, offset64,64. Não há intermediários nem outros clipes novos.

## Método e leitura visual

A entrada é o corpo V1 original extraído sem alteração do pedido Argon, não os corpos rejeitados. O método foi skeleton-v3 com EXATAMENTE três esqueletos completos, cada um com 18 juntas: braço ativo dobra sobre a coroa; mão inativa, ombros, quadril, joelhos e apoios participam. Não há cópia de coluna F00, doador, rotação/compressão de corpo ou transformação de membro.

O primeiro job acertou a flexão corporal no impacto, mas cortou a mão nas duas poses altas. Essas duas foram editadas juntas pelo PixelLab; raw e recibos anteriores permanecem preservados. A preparação ficou integral. O ápice ainda tangenciou a borda em seis pixels: no Aseprite, após registro integral de +2px no chão, quatro pixels de contorno escuro arredondam a tampa do punho. Um pixel branco isolado da preparação foi substituído localmente. Código Lua registra as coordenadas. Nenhuma edição raster artística externa. Os zooms Pillow são diagnósticos, nunca fontes.

Na preparação e ápice, o cotovelo direito está flexionado e o antebraço retorna por cima da coroa, em vez de abrir horizontalmente. No impacto, a placa dorsal inclina com o tronco e a cabeça, o ombro direito cede, o punho desce junto ao corpo, os joelhos flexionam e a base abre. O braço inativo muda nas três chaves. Veja as imagens sem marcação antes de ligar as juntas. Coordenadas em representative.json foram lidas dos exports finais, aproximadas ±2px; os esqueletos solicitados são guardados separadamente, não tratados como evidência dos pixels.

## Evidência e verificação

review.html mostra AFTER em três colunas, BEFORE do corpo rejeitado F01/F02/F04, articulações opcionais e inspeção sequencial em 1×/2×/3×. São poses-chave separadas: não se declara um ciclo final, naturalidade contínua em 1× ou percurso comprovado da arma. Não há overlays que escondam a anatomia. Pegada final pertence à outra especialidade.

Os seis arquivos Aseprite foram salvos pelo executável autorizado em batch --noinapp, perfil exclusivo tmp/aseprite-body-specialist-profile. Três mestres nativos reabertos e reexportados: pixels RGBA coincidem 3/3. Recorte64,64 do composto coincide com nativo 3/3. Frames únicos de 160ms (Lua 0.160 segundos), chão126, zero pixels com RGB todos >190. Evidência em technical-verification.json e reexport-timing.json. Estes checks são técnicos, não aprovação artística.

## Custo e isolamento

Job skeleton e1b57e4c-e707-4e12-ace7-0745bd9bbb44: 2 gerações cobradas, três saídas. Job edit 74f03969-32ca-4150-9778-628df917f790: 10 gerações cobradas, duas correções das mesmas chaves. Total12; saldo medido1382.70 antes e1370.70 depois. Sem compra/assinatura. A primeira chamada teve erro de validação de tamanho de action, sem job emitido; recibo preservado.

Escritas limitadas às duas pastas body-specialist e ao perfil exclusivo expressamente solicitado. Nenhuma fonte anterior, arma, matriz, documento global, pasta grip-specialist ou Unity foi escrita. Não foi repetida auditoria global de3506 fontes; não se atribui uma preservação rehasheada que não foi executada.

## Handoff

Root deve enviar este freeze de três chaves ao MESMO QA independente Grok. QA não foi criado nem executado aqui. Aguardar parecer antes de intermediários, back_l ou Sword. O ápice tem apenas1px transparente acima da tampa do punho: verificar contorno e espaço para equipamento no composto256. O criador retém aprovação artística. Manifestos globais e integração continuam com Root.
