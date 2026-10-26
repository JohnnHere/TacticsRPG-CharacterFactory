# Orc Atlético e descarte das direções V4

Data: 2026-10-24. Entregue para avaliação — nova candidata sem aprovação artística.

## Decisão do criador

V4 ativa e V4 Reimaginado (`orc-pixellab-07`) descartados completamente da direção atual. Arquivos históricos preservados; ponteiro `reports/orc-production-current.json` registra `DISCARDED_BY_CREATOR`, revisão/seleção nulas. Auditoria geral retorna `NO_ACTIVE_SELECTION`. Scripts históricos de auditoria/aplicação/exportação V4 recusam reativar a revisão descartada, conforme `reports/orc-discarded-v4-check.json`. Nenhum substituto foi aprovado para produção e nada foi alterado no projeto Unity.

## Novo Orc Atlético — 11

Pedido: parecido com o Veterano Ágil, porém mais musculoso, sem volume inchado, tom verde ligeiramente mais claro e menos cobertura de armadura. Peitoral/abdômen expostos com arnês estreito, ombreira compacta, proteção de antebraço/quadril/joelho e botas. Sem armas integradas. Inspirações Warcraft/Tolkien, materiais gastos, paleta contida e pixel art detalhada.

Somente conceito 04 é imagem de referência autorizada. Conceito pedido ao MCP `edit_image_pro_flash`, seed 8241701, job `1e0cbd5c-6cab-4536-9330-de259a00a366`. Nenhuma imagem da V4 ou do Reimaginado foi usada.

Para Walk, reaproveitar as oito estimativas de pontos já existentes do Ágil, sem repetir aquelas chamadas. Retarget dos ângulos reais de braços/pernas para comprimentos do novo corpo, mantendo orientação em três quartos do guia e registro próprio de cabeça/pescoço. Metadados em `tools/prepare-orc-athletic-walk.py`. Idle discreto a partir da nova imagem. Não copiar cabeça do Ágil para os quadros.

Toda geração é PixelLab em nuvem, usando a conta Pro do criador; mestres e exportações no Aseprite batch isolado. Não declarar geração como desenho manual. Modelos reais e uso cobrado serão registrados após conclusão, separadamente do plano Pro.

## Revisão e ideias reservadas

Revisão canônica nova: `reports/orc-current-review/review.html`, oito Orcs atuais com conceito/Idle/Walk simultâneos. V4/07 excluídos. Reconstrução: `node tools/build-orc-all-review.mjs`.

Vigia do Passo e Matriarca permanecem em `ideas/unique-characters-or-npcs/`, pacotes completos separados. São futuras ideias de NPC **e/ou jogáveis exclusivos/únicos**, não somente NPCs. Página própria `ideas/unique-characters-or-npcs/review.html`; nenhuma animação ausente foi simulada.

Verificar preservação dos 567 arquivos de arte existentes com `experiments/pixellab-orc-athletic-v1/protected-art.json`. Validação técnica e exportação correta não concedem aprovação artística.

## Resultado entregue e recibos

Conceito Pro Flash concluído, 6 gerações cobradas. Walk Skeleton V3: job `e39a59db-c2c0-4b67-b9ff-ba5e2cc39ced`, seed 8241703, 3 gerações cobradas, oito quadros reais sem entrada repetida, 100 ms/quadro (800 ms). Idle `animate_image`: job `2a6d279b-ed3a-4d06-ac4a-bf878f0d689a`, seed 8241702, 2 gerações cobradas; entrada repetida excluída, oito quadros a 200 ms (1600 ms). A ferramenta Idle não expõe seletor de modelo; não chamá-la de modelo Pro por causa do plano da conta.

Duas novas estimativas de pontos (conceito Ágil e conceito Atlético), 0,1 cada; as oito estimativas do Walk Ágil foram reutilizadas sem nova cobrança e copiadas para `experiments/pixellab-orc-athletic-v1/guide/`, com procedência. **Total dos recibos desta rodada: 11,2 gerações.** O conceito Ágil foi estimado como referência de análise; o retarget usa os oito movimentos e os comprimentos do próprio Atlético.

Mestres novos em `characters/orc-pixellab-11/source/aseprite/`: `concept-selected.aseprite`, `idle-study.aseprite`, `walk-study.aseprite`; arquivos raw adicionais preservam as saídas do provedor. PNGs de revisão são derivados exportados pelo Aseprite; não houve edição raster externa nem mistura regional de cabeças. Pose/face/cor mantêm a intenção da referência, mas geração não garante igualdade entre quadros. A aprovação final continua sendo do criador.

A exportação dos três mestres conferiu 17 quadros com os PNGs esperados. A página conferiu 144 quadros visíveis em oito conceitos e 16 clipes, abertura local, layout móvel e ausência de erros JavaScript. Evidências: `reports/orc-athletic-v1-export.json`, `reports/orc-athletic-v1-check.json`, `reports/orc-all-review-check.json`. Todos os 567 arquivos PNG/Aseprite anteriores conferidos intactos.

Seleção de comparação em `reports/orc-study-selection.json`; ponteiro de revisão `reports/orc-study-current-review.json`. O endereço anterior da comparação redireciona para a página nova. Vigia e Matriarca têm categoria reservada tanto no catálogo de origem quanto nos pacotes completos da pasta de ideias. O conjunto V4 descartado não reaparece pelo construtor antigo, que agora recusa essa seleção.

Próximo passo: criador comparar o Atlético com os demais candidatos e decidir a direção; sem escalonar Jobs, conceder Gates ou integrar no Unity automaticamente.
