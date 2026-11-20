# Orc V1 — 3 Chaves Anatômicas Traseiras back_r/Sword (Espada de Uma Mão)

**Status:** READY_FOR_QA  
**Technical Status:** TECHNICALLY_COMPLETE  
**Artistic Status:** VISUAL_REVIEW_REQUIRED  
**Global Status:** ARTISTIC_REVISION_REQUIRED (PENDING_CREATOR)  

## Escopo
- **Direção:** `back_r`
- **Categoria:** `Sword`
- **Ação:** Golpe lateral diagonal de espada de uma mão: preparação flexão de cotovelo, ápice extensão lateral, impacto e recuperação baixa
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
- **Observação:** Braço direito ativo com cotovelo flexionado à altura do ombro, antebraço inclinado para trás e punho fechado em manopla vinho-marrom legível. Braço esquerdo inativo abaixado com braçadeira de espinhos e punho fechado. Crânio occipital verde sem rosto, placa dorsal com costura vertebral, botas cravadas no chão.
- **Coordenadas anatômicas (128x128):**
  - Ombro ativo: [82, 47]
  - Cotovelo ativo: [106, 63]
  - Punho ativo: [101, 42]
  - Palma/extremidade ativa: [98, 48]
  - Ombro inativo: [43, 49]
  - Cotovelo inativo: [29, 67]
  - Punho inativo: [27, 85]
  - Apoio dos pés: Direito [92, 126], Esquerdo [38, 126]


### Chave 02 — 02-apex
- **Duração:** 160 ms
- **Observação:** Extensão lateral do braço direito à frente e à direita na direção do corte. Cotovelo, antebraço e punho fechado em cadeia contínua e arredondada. Braço esquerdo mantido baixo como contrapeso. Tronco inclinado acompanhando o movimento, base cravada.
- **Coordenadas anatômicas (128x128):**
  - Ombro ativo: [84, 39]
  - Cotovelo ativo: [100, 47]
  - Punho ativo: [114, 55]
  - Palma/extremidade ativa: [118, 56]
  - Ombro inativo: [46, 40]
  - Cotovelo inativo: [29, 62]
  - Punho inativo: [25, 79]
  - Apoio dos pés: Direito [96, 126], Esquerdo [36, 126]


### Chave 03 — 03-impact
- **Duração:** 160 ms
- **Observação:** Término e follow-through do golpe: braço direito desce junto ao quadril direito com punho fechado apontado para baixo. Tronco articulado para frente, joelhos flexionados, base larga cravada no solo.
- **Coordenadas anatômicas (128x128):**
  - Ombro ativo: [84, 51]
  - Cotovelo ativo: [101, 67]
  - Punho ativo: [95, 85]
  - Palma/extremidade ativa: [95, 87]
  - Ombro inativo: [45, 49]
  - Cotovelo inativo: [29, 70]
  - Punho inativo: [28, 89]
  - Apoio dos pés: Direito [96, 126], Esquerdo [34, 126]


## Contabilidade e Custos
- Chamadas de API PixelLab nesta sessão: 0
- Créditos consumidos nesta sessão: 0.00
- Saldo restante registrado: 1351.70 gerações
- Refinamentos cirúrgicos locais: Executados via Aseprite Lua (ex: limpeza de 94 pixels de resíduo cinzento de fundo em `back_l-Axe 02`).

## Próximo Passo
Submeter ao QA independente para veredito estrutural antes de gerar quadros intermediários. Nenhuma integração com Unity realizada.
