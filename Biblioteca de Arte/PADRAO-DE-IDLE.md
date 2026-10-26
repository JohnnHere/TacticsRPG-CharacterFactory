# Padrão fixo obrigatório de Idle — criação de personagens

Decisão canônica do criador em 2026-10-25. O meio-termo aprovado do Infante de Ferro é o **padrão fixo de design do Idle normal**, obrigatório para a criação de personagens e variantes daqui para frente. Não é referência opcional, ponto de partida livre ou autorização para cada personagem ter seu próprio padrão. Esta definição substitui as orientações anteriores que permitiam variar cadência, amplitude ou contagem por personalidade, roupa ou anatomia a critério do agente.

## Contrato comum obrigatório

- Mesma linguagem de movimento: presença viva e tranquila, respiração contida, cabeça/pescoço ligados naturalmente ao tronco, apoios firmes e assentamento discreto das mãos.
- Mesmas cinco fases/poses principais, no ritmo aprovado: **400 / 450 / 500 / 450 / 400 ms**, total **2200 ms** por ciclo.
- Mesma intensidade visual do meio-termo: **2 px de excursão vertical da cabeça na escala humanoide 128×128**. Em outra resolução, manter amplitude proporcional e a mesma percepção de sutileza, sem aumentar a agitação por gosto do agente.
- Ciclo suave, sem ofegância, balanço excessivo, deslocamento dos pés ou alteração arbitrária de postura. Qualidade de rosto, paleta, materiais e clusters preservada.
- Personagens diferentes devem parecer parte da mesma direção de animação quando vistos juntos. Job, armadura, temperamento e raça não autorizam por si só outro ritmo ou outro estilo de respiração.

Os números de amplitude são aplicados à escala de referência, não às coordenadas absolutas do rosto de todo personagem. **Ajustar o encaixe à anatomia não significa mudar o padrão**: preservar anatomia e identidade próprias, sem copiar a cabeça, o corpo ou a roupa do Infante. A morfologia pode exigir poses correspondentes; não deve gerar um novo estilo de Idle.

## Exceções e anatomias incompatíveis

Se uma anatomia ou estado especial não puder seguir o padrão, registrar o motivo e obter autorização explícita do criador para a exceção antes de produzir outro Idle. O agente não decide sozinho uma exceção por tamanho, personalidade, raça, Job ou preferência estética. A autorização deve identificar personagem/estado, motivo e escopo. Estados especiais como exaustão ou ferimento não substituem silenciosamente o Idle normal.

## Obrigatório na criação e revisão

1. Ler este documento e config/idle-art-standard-v1.json antes de autorar o Idle de um personagem novo ou uma nova versão.
2. Conferir o mestre e o ciclo aprovado, reaproveitar movimento/fontes compatíveis e preservar a identidade individual. Fonte mestre no Aseprite.
3. Produzir e revisar as cinco fases e os tempos fixos; comparar lado a lado com o padrão em tamanho nativo. Validar também início/fim e apresentação conjunta com outros personagens.
4. Registrar revisão do padrão, tempos, amplitude medida, procedência e eventual autorização de exceção no clip/handoff do personagem.
5. Qualquer divergência sem autorização é **fora do padrão**, não uma nova interpretação artística aceitável. Não apresentar como pronto para produção.

Baseline técnica antiga, receita histórica, preferência de modelo generativo ou contagem herdada não têm precedência sobre esta decisão. Ao produzir um novo Idle, alinhar o perfil local ao contrato de cinco fases antes da autoria/exportação e manter evidência dos históricos; não falsificar compatibilidade com o runtime antigo.

Não usar compressão regional do tronco, partes desconexas, colagem de cabeça ou redução de detalhes para simular sutileza. PixelLab pode auxiliar a geração autorizada; acabamento, timing e mestre seguem no Aseprite. Exportação correta não comprova conformidade artística.

## Fontes canônicas e biblioteca

Contrato: config/idle-art-standard-v1.json, ID idle-balanced-v1. Referência aprovada: characters/orc-pixellab-05/source/studies/Idle/clip.json, revisão infante-idle-balanced-v3. Mestre: characters/orc-pixellab-05/source/aseprite/infante-idle-balanced-v3/source/infante-idle-balanced.aseprite. Evidência: characters/orc-pixellab-05/source/creator-approval-idle-balanced-v3.json.

A biblioteca recebe uma cópia atualizada em PADRAO-DE-IDLE.md. O prepare inclui automaticamente documento, contrato e instrução obrigatória no handoff. A comparação das três versões preserva as alternativas como histórico; só o meio-termo é o padrão aprovado.

Não é uma migração automática das artes existentes: suas revisões permanecem preservadas até tarefa explícita de adequação. Este pedido não integra Unity, não produz armas e não concede todos os Gates dos personagens. O próximo trabalho de criação já deve nascer conforme o padrão, sem pedir ao criador que repita essa decisão.
