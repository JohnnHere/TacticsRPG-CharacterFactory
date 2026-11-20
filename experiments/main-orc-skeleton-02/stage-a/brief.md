# Experimento 02 — Estágio A: auditoria do corpo

Você é o revisor do **Estágio A**. Seu produto é um veredito sobre a qualidade e a contaminação do
corpo, com medição. Você não desenha, não gera, não corrige arte.

## Limites duros

- **Zero chamadas pagas ao PixelLab.** Não invoque geração.
- Não edite nada em `characters/`, `assets/`, `reports/` nem em `../TacticsRPG`.
- Não faça commit.
- Escreva apenas em `experiments/main-orc-skeleton-02/stage-a/`.

## O que auditar

1. **Arte gerada no Experimento 01**: os 14 quadros em
   `experiments/main-orc-skeleton-first-01/pixellab-frames/00.png` … `13.png`.
   Eles foram gerados por esqueleto, com a espada dentro da geração. A pergunta é se sobrou corpo
   limpo ou se a arma contaminou a anatomia.
2. **As cinco poses-chave do clipe de produção atual**, em
   `characters/orc-v1/source/combat-recovery-v8/rear-arc/back_l-sword/`, nos índices 0, 5, 8, 9 e
   13. Esse clipe guarda camadas separadas: `body`, `handFront`, `weaponBack`, `weaponFront`.
   Ele é a alternativa de corpo limpo e precisa ser auditado com o mesmo rigor.

## Como medir, sem confiar no olho

Para cada um dos 14 quadros gerados, e para as 5 poses do clipe atual:

- Silhueta e bounding box do corpo, e proporção entre altura da cabeça e altura total.
- Cadeia anatômica: comprimentos de úmero, antebraço, coxa e canela, e a variação entre quadros.
  Membros que mudam de comprimento são anatomia quebrada.
- Ancoragem no chão: os tornozelos não podem afundar nem flutuar.
- Continuidade de contorno: existe borda clara indevida, pixel órfão ou penhasco de alfa.
- **Contaminação por arma**: no quadro gerado não existe camada, então procure geometria de arma
  embutida. Compare a silhueta com o corpo esperado e identifique regiões onde há lâmina, cabo ou
  guarda sobrepostos ao braço, ombro ou tronco. Quantifique em pixels.

## Veredito obrigatório, por pose

Use exatamente um destes rótulos, com a evidência que o sustenta:

- `CLEAN_BODY` — corpo utilizável sem geometria de arma.
- `RECOVERABLE_BODY` — o corpo pode ser separado com edição local limitada, **sem inventar anatomia**.
- `CONTAMINATED_BODY` — a arma cobre ou substitui geometria essencial do corpo.

Regra explícita: não apague pixels de espada se isso deixar mão ou antebraço anatomicamente
inválidos, e não fabrique anatomia faltante com formas geométricas genéricas. Se a separação não for
convincente, preserve a evidência e relate a limitação.

## Entrega

- `experiments/main-orc-skeleton-02/stage-a/report.md` — veredito por pose, tabela de medidas,
  e uma conclusão clara: o corpo do Experimento 01 serve ou não serve como base.
- `experiments/main-orc-skeleton-02/stage-a/measurements.json` — os números que você calculou.
- Recortes ampliados das regiões onde você alega contaminação ou defeito anatômico, em
  `stage-a/evidence/`, com nomes que digam quadro e região.

Não conclua que o corpo ficou bom só porque o esqueleto foi seguido. O que conta é o pixel.
