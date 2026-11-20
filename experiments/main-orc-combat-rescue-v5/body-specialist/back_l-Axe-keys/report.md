# Orc V1 — 3 Chaves Anatômicas Traseiras back_l/Axe (Machado de Uma Mão)

**Status:** READY_FOR_QA  
**Technical Status:** TECHNICALLY_COMPLETE  
**Artistic Status:** VISUAL_REVIEW_REQUIRED  
**Global Status:** ARTISTIC_REVISION_REQUIRED (PENDING_CREATOR)  

## Escopo
- **Direção:** `back_l`
- **Categoria:** `Axe`
- **Ação:** Golpe pesado vertical de machado (overhead cleave) na vista noroeste: hoist curvado, ápice sobre a coroa com espaço negativo transparente limpo, e impacto descendente com flexão corporal
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
- **Observação:** Preparação do machado: braço direito erguido para trás, cotovelo flexionado acima da cabeça, punho fechado em manopla vinho-marrom segurando imaginariamente o topo do cabo. Braço esquerdo de guarda estendido para baixo.
- **Coordenadas anatômicas (128x128):**
  - Ombro ativo: [79, 38]
  - Cotovelo ativo: [101, 31]
  - Punho ativo: [81, 15]
  - Palma/extremidade ativa: [81, 15]
  - Ombro inativo: [42, 41]
  - Cotovelo inativo: [27, 55]
  - Punho inativo: [25, 75]
  - Apoio dos pés: Direito [91, 126], Esquerdo [36, 126]


### Chave 02 — 02-apex
- **Duração:** 160 ms
- **Observação:** Ápice sobre a cabeça: antebraço direito arqueado acima da coroa com punho fechado [65, 10]. Espaço negativo triangular sob o braço e acima do pescoço cirurgicamente limpo de resíduos cinzentos (94 pixels removidos para alfa 0 transparente). Coluna arqueada, base plantada.
- **Coordenadas anatômicas (128x128):**
  - Ombro ativo: [78, 40]
  - Cotovelo ativo: [95, 19]
  - Punho ativo: [65, 10]
  - Palma/extremidade ativa: [65, 10]
  - Ombro inativo: [40, 43]
  - Cotovelo inativo: [25, 58]
  - Punho inativo: [20, 78]
  - Apoio dos pés: Direito [94, 126], Esquerdo [33, 126]


### Chave 03 — 03-impact
- **Duração:** 160 ms
- **Observação:** Impacto vertical do machado: tronco flexionado para a frente, braço direito projetado para baixo com cotovelo, antebraço e punho contínuos ao lado do quadril/coxa. Braço esquerdo firme na guarda. Joelhos dobrados sustentando o golpe.
- **Coordenadas anatômicas (128x128):**
  - Ombro ativo: [78, 53]
  - Cotovelo ativo: [92, 68]
  - Punho ativo: [89, 85]
  - Palma/extremidade ativa: [89, 87]
  - Ombro inativo: [38, 50]
  - Cotovelo inativo: [23, 70]
  - Punho inativo: [22, 86]
  - Apoio dos pés: Direito [94, 126], Esquerdo [29, 126]


## Contabilidade e Custos
- Chamadas de API PixelLab nesta sessão: 0
- Créditos consumidos nesta sessão: 0.00
- Saldo restante registrado: 1351.70 gerações
- Refinamentos cirúrgicos locais: Executados via Aseprite Lua (ex: limpeza de 94 pixels de resíduo cinzento de fundo em `back_l-Axe 02`).

## Próximo Passo
Submeter ao QA independente para veredito estrutural antes de gerar quadros intermediários. Nenhuma integração com Unity realizada.
