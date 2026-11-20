# Experimento 04 — arquitetura híbrida: duas espadas sobre um corpo

Piloto. Uma animação de corpo, duas espadas compatíveis, composição offline no Aseprite.
**A pergunta central: dá para trocar a espada sem reconstruir corpo, braço ou mão?**

## Gate 0 — já decidido pelo orquestrador, com medição

Base escolhida: **`front_l/Sword`**
`characters/orc-v1/source/combat-recovery-v8/frontal-inbetween/front_l-sword/clip.json`
(14 quadros, 730 ms, armado F02–F11, `contactEvent` F08/325 ms).

Justificativa medida: mão sem defeitos nas duas direções (0 pixels órfãos, 0 alfa parcial, 0
quase-branco, saltos de centroide idênticos), `body` sem arma embutida nas duas, e `front_l` tem a
junção ombro/axila mais legível após a reiluminação já aplicada (razão tinta/claro 1,14 contra 1,29).

## Limites duros

- **Zero PixelLab, zero geração.** Tudo no Aseprite.
- **Não altere o corpo.** Camada `body` e `handFront` de cada quadro têm de continuar
  **byte-idênticas** ao original entre as duas variantes e contra a fonte.
- Não toque em `characters/`, `assets/`, `reports/`, `../TacticsRPG`. Não faça commit.
- Não mexa em outras direções, outras ações, outros personagens, Unity.
- Trabalhe em `experiments/main-orc-hybrid-weapon-04/`.

## Variante A — a espada atual

Espada do Recruta:
`characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/recruit-sword.png` + `weapon.json`
(canvas 96×96, `grip` em `48,66`, uma mão direita).

Recomponha com ela usando o mesmo contrato de camadas do original:
`weaponBack → body → weaponFront → handFront`.

## Variante B — espada compatível nova

Crie **uma** variante no Aseprite, partindo da arte existente, com identidade visual distinta:

- **Perfil do cabo idêntico** em espessura, região de contato e pivô (`grip` 48,66 no mesmo canvas
  96×96), para a mesma mão servir.
- **Guarda e punho compatíveis** — mesma folga, mesmo ponto de oclusão.
- **Lâmina visivelmente diferente**: perfil (ex.: mais estreita com fio curvo, ou mais larga com
  ponta facetada) e material (ex.: aço polido claro contra aço fosco atual), mantendo a linguagem
  visual do jogo: contorno escuro, poucos valores, dither coerente.
- Comprimento dentro de ±10% do atual; nada de muda de categoria de peso ou de técnica.
- Salve como mestre `.aseprite` + PNG em `variants/sword-b/`, com procedência e hashes.

Não é permitido entregar a mesma arte com nome diferente. A silhueta da lâmina tem de mudar.

## Stage A e B — quadros representativos

Três quadros: **F02** (preparação), **F08** (impacto), **F11** (recuperação).
Componha com Variante A e com Variante B **usando exatamente os mesmos quadros de corpo**.

Regra obrigatória: `body` e `handFront` **idênticos byte a byte** entre A e B. Só podem variar
arte de arma, transformação da arma e oclusão por camada.

Inspecione e relate: continuidade de braço e mão, pegada, orientação da arma, oclusão,
transparência, qualidade de borda, geometria e identidade do personagem. **Distinga defeito herdado
da fonte de defeito introduzido pela composição.** Se a composição introduzir problema grave novo,
pare e relate em vez de seguir.

## Grip profile reusável

Escreva `grip-profile.json` com: fonte da animação, família de arma, referência da mão que empunha,
ponto de contato no cabo, pivô, orientação por quadro, regras de oclusão (o que vai em
`weaponBack` × `weaponFront` × `handFront`), e referência de tempos.

Pegada só conta se **parecer** pegada: o cabo entra na palma, a luva oclui o cabo onde for o caso,
o punho mantém relação coerente com o antebraço e fica estável no movimento. Coordenada correta com
palma aberta é reprovado. Um overlay de luva pode ser criado se servir às **duas** variantes.

## Stage C — export completo

Só se A e B passarem nos representativos: componha os **14 quadros** completos para A e para B,
preservando tempos, coreografia e as mesmas referências de corpo. Exporte pelo pipeline existente.

## Artefatos e diagnóstico de borda

Separe sempre três saídas: `body-only/`, `weapon-only/` e `composite/`. Verifique se algum halo
claro novo vem do corpo, da arma, da transformação, da composição, da máscara ou da exportação.
Não escureça o Orc globalmente; preserve highlights metálicos legítimos. Defeito herdado da fonte
tem de ser reportado como herdado, separado do que a composição introduziu.

## Entrega, em `experiments/main-orc-hybrid-weapon-04/`

1. `variants/sword-a/` e `variants/sword-b/` — mestres `.aseprite`, PNGs, hashes, procedência.
2. `representative/{a,b}/` — `body-only/`, `weapon-only/`, `composite/` em F02, F08, F11.
3. `full/{a,b}/` — os 14 quadros completos, se o Stage C passou (senão, declare o motivo).
4. `grip-profile.json`.
5. `pixel-diff.json` — prova de que `body`/`handFront` são idênticos entre A e B e contra a fonte.
6. `report.md` — Gate 0, contaminação do body, fontes das variantes, grip profile, resultados por
   estágio, defeitos herdados versus introduzidos, limitações, e métricas de reuso
   (quadros de corpo reutilizados, quadros de corpo alterados = 0, variantes criadas,
   ajustes específicos de arma, correções de pegada, chamadas PixelLab = 0).

## Critério de sucesso técnico

Mesmas quadros de corpo nas duas variantes; zero reconstrução de corpo para a B; ambas as espadas
reconhecíveis; pegada reproduzível e visualmente convincente; nenhum artefato novo relevante;
tempos preservados. Sucesso técnico **não** é aprovação artística — o criador julga.
