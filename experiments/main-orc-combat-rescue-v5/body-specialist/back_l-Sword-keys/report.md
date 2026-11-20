# Orc V1 — 3 Chaves Anatômicas Traseiras back_l/Sword (Espada de Uma Mão)

**Status:** READY_FOR_QA  
**Technical Status:** TECHNICALLY_COMPLETE  
**Artistic Status:** VISUAL_REVIEW_REQUIRED  
**Global Status:** ARTISTIC_REVISION_REQUIRED (PENDING_CREATOR)  

## Escopo
- **Direção:** `back_l`
- **Categoria:** `Sword`
- **Ação:** Golpe lateral diagonal de espada na vista noroeste: preparação alta, ápice corte transversal e impacto descendente
- **Número de chaves:** 3 chaves anatômicas estruturais (`01-hoist`, `02-apex`, `03-impact`)
- **Regime de camadas:** Desarmado estrito (`layers-off`), camada única `body`, sem carimbo de armas ou artefatos.

## Validação Técnica
- **Resolução:** Nativo 128×128 / Composto 256×256 (offset 64,64).
- **Alinhamento do solo:** `nativeGroundY = 126`, `groundY = 190`.
- **Duração dos frames:** Exatamente 160 ms (`0.160` s no Lua Aseprite).
- **Pixels com brilho excessivo:** 0 pixels com RGB > 190.
- **Autoria:** Executável Aseprite oficial (`F:\SteamLibrary\steamapps\common\Aseprite\Aseprite.exe`) via batch `--noinapp` sob perfil exclusivo.

## Chaves Anatômicas e Inspeção Visual

### Chave 01 — 01-hoist
- **Duração:** 160 ms
- **Observação:** Perspectiva noroeste traseira: ombro direito ativo (à direita da imagem) com braço erguido e flexionado, punho fechado em manopla vinho-marrom próximo à gola/pescoço. Braço esquerdo inativo abaixado com braçadeira pontiaguda. Placa dorsal e crânio sem face preservados.
- **Coordenadas anatômicas (128x128):**
  - Ombro ativo: [78, 37]
  - Cotovelo ativo: [101, 53]
  - Punho ativo: [97, 34]
  - Palma/extremidade ativa: [97, 34]
  - Ombro inativo: [42, 38]
  - Cotovelo inativo: [28, 56]
  - Punho inativo: [25, 75]
  - Apoio dos pés: Direito [90, 126], Esquerdo [36, 126]


### Chave 02 — 02-apex
- **Duração:** 160 ms
- **Observação:** Extensão transversal do golpe de espada através da silhueta corporal. Antebraço e punho direito projetados à frente-direita. Braço esquerdo de guarda baixo. Tronco torcido na dinâmica do golpe, sola das botas no chão126.
- **Coordenadas anatômicas (128x128):**
  - Ombro ativo: [79, 41]
  - Cotovelo ativo: [97, 49]
  - Punho ativo: [110, 56]
  - Palma/extremidade ativa: [114, 57]
  - Ombro inativo: [41, 41]
  - Cotovelo inativo: [25, 62]
  - Punho inativo: [20, 79]
  - Apoio dos pés: Direito [94, 126], Esquerdo [33, 126]


### Chave 03 — 03-impact
- **Duração:** 160 ms
- **Observação:** Follow-through baixo do golpe de espada: punho direito desce ao lado do quadril com volume e punho fechado nítidos. Braço esquerdo estabilizado. Base plantada sem deslizamento.
- **Coordenadas anatômicas (128x128):**
  - Ombro ativo: [78, 48]
  - Cotovelo ativo: [97, 65]
  - Punho ativo: [90, 82]
  - Palma/extremidade ativa: [90, 84]
  - Ombro inativo: [39, 46]
  - Cotovelo inativo: [23, 67]
  - Punho inativo: [23, 86]
  - Apoio dos pés: Direito [95, 126], Esquerdo [31, 126]


## Contabilidade e Custos
- Chamadas de API PixelLab nesta sessão: 0
- Créditos consumidos nesta sessão: 0.00
- Saldo restante registrado: 1351.70 gerações
- Refinamentos cirúrgicos locais: Executados via Aseprite Lua (ex: limpeza de 94 pixels de resíduo cinzento de fundo em `back_l-Axe 02`).

## Próximo Passo
Submeter ao QA independente para veredito estrutural antes de gerar quadros intermediários. Nenhuma integração com Unity realizada.
