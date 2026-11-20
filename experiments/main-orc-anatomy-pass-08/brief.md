# Passe anatômico experimental — quadro 08, braço direito de ataque

Trabalho de autoria delicada no Aseprite. Um quadro, um membro, zero geração.

## Limites duros

- **Zero chamadas ao PixelLab.** Nenhuma geração, paga ou gratuita.
- Não redesenhe o personagem. Não espelhe o Orc. Não interpole quadros.
- **A espada fica fora desta edição.** Você edita somente o corpo.
- Não toque em `characters/`, `assets/`, `reports/` nem em `../TacticsRPG`. Não faça commit.
- Trabalhe em cópia, em `experiments/main-orc-anatomy-pass-08/`. As fontes em
  `experiments/main-orc-skeleton-02/stage-bcde/` são somente leitura.

## Base e referências

- **Alvo:** `experiments/main-orc-skeleton-02/stage-bcde/body-only/08.png` (256×256).
- **Vizinhos para consulta:** `body-only/05.png` (elevação) e `body-only/09.png` (seguimento).
- **Referências de movimento, apenas isso:** `experiments/main-orc-skeleton-first-01/poses-fixed.json`
  e `sequence-fixed.json`. As coordenadas de lá são estimativas de planejamento — **não são alvos
  obrigatórios**. O que manda é a arte e a anatomia.

## O defeito, já diagnosticado

No 08, a cadeia ombro → cotovelo → punho está quase **horizontal**, o que dá leitura de golpe
lateral — a reclamação recorrente do criador. Medidas aproximadas do quadro atual: ombro em
(~147,112), cotovelo em (~168,120), punho/luva em (~181,125). O antebraço aponta para fora, não
para baixo.

Os vizinhos provam que o Orc sabe fazer o movimento certo: no 05 o antebraço dobra para cima, no 09
ele desce dobrado junto ao corpo. O 08 é o elo que falta: **o instante da diagonal descendente**.

## O que reautoriar — e só isso

O **braço direito de ataque**: ombro, braço superior, cotovelo, antebraço, pulso e a ligação com a
mão. Objetivo: a articulação tem de ficar **legível e anatomicamente plausível**, com a cadeia em
diagonal descendente — ombro alto, cotovelo abaixo e à frente, antebraço descendo na direção do
contato. É coerente com 05 erguido antes e 09 recolhido depois.

A posição **da mão pode mudar pouco** — se mudar, registre o novo ponto de contato com precisão de
pixel, porque a arma será composta depois sobre esse ponto. Não mova a mão mais do que o necessário
para a articulação ficar correta.

## O que é intocável

Rosto, cabeça, chifres/cabelo, armadura do tronco, cinto, pernas, botas, paleta, estilo, escala e
o contorno escuro externo do corpo. O ombro pode ser retratado **apenas na junção indispensável**
com o braço. Tudo o que estiver fora do braço e dessa junção tem de ficar **byte-idêntico**.

Não copie o braço inteiro de outra pose: use 05 e 09 como referência de comprimento e articulação,
não como fonte de colagem. Os comprimentos de úmero e antebraço do próprio 08 devem ser
preservados dentro de uma tolerância apertada — membro que muda de tamanho é anatomia quebrada.

## Método

Aseprite, autoria manual ou Lua registrada, no seu perfil batch isolado. Salve mestre editável e
registre a procedência (autoria programática/manual, fonte, hash de entrada e saída). Amostragem
inteira, sem interpolação, sem blur, sem cor fora da paleta existente do orc.

## Entrega, em `experiments/main-orc-anatomy-pass-08/`

1. `candidate-08.png` — o PNG candidato único (body-only, 256×256).
2. `master-08.aseprite` — o mestre salvo.
3. `before-after.png` — comparação antes/depois em **1×** e ampliada (4× ou 8×) lado a lado.
4. `changed-regions.png` — mapa das regiões alteradas, com as caixas marcadas sobre o quadro.
5. `report.md` — mapa de juntas antes/depois (ombro, cotovelo, punho), comprimentos de úmero e
   antebraço antes/depois, o novo ponto de contato da mão se mudou, e a confirmação explícita de
   que as mudanças ficaram limitadas ao braço e à junção indispensável do ombro.
6. `pixel-diff.json` — lista das caixas alteradas e contagem de pixels mudados por caixa.

## Critério de sucesso

O quadro 08, visto sozinho, tem de ler como **corte descendente** — não como golpe lateral. E o Orc
tem de continuar sendo o mesmo Orc. Se você concluir que não é possível corrigir a articulação sem
comprometer a identidade, **pare e explique o conflito** em `report.md`; não amplie o escopo.
