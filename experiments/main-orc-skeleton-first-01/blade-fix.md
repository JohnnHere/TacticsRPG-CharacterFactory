# Correção focada — única permitida nesta etapa

O esqueleto está bom e não deve ser refeito. O defeito está nos campos da lâmina.

## O que a auditoria mediu

Percorri os 14 quadros do seu `sequence.json`, reconstruí a ponta da lâmina a partir de
`grip.point` + `grip.bladeDirection` com o comprimento que você usou, e achei três defeitos.

| # | Defeito | Onde | Número |
|---|---|---|---|
| 1 | A ponta sai do canvas por cima | F05 `apex-hold` | ponta em `y = -0,019` |
| 2 | A lâmina atravessa o chão no seguimento e na recuperação | F09 a F13 | `y` de 0,825 a 0,844, com chão em 0,742 |
| 3 | A lâmina termina apontando para o chão | F11 `settle-grip` | direção `(0,07; 1,00)`, vertical para baixo |

## A causa raiz, medida

Você usou comprimento de lâmina **0,30** em fração do canvas.

A arma real não tem esse tamanho. Medi
`characters/orc-v1/source/combat-rescue-v5/combat/weapons/Sword/recruit-sword.png`:
canvas 96×96, `grip` em `(48,66)`, e o ponto mais distante do cabo está em `(47,7)`, isto é
**59,01 px**. No composto de 256 a arma é desenhada praticamente em escala 1:1 — o bbox de
`weaponFront` no quadro 02 vai de `y=66` a `y=134` com a mão em `y=120`, o que confirma isso.
Portanto o comprimento correto é **0,227**, não 0,30.

Com 0,30 a ponta avança 28% além do que a arma alcança, e é exatamente isso que a joga fora do
canvas no ápice e para dentro do chão no seguimento.

## O que corrigir

1. **Comprimento.** Use **0,227** como comprimento da lâmina do cabo até a ponta, em todos os
   quadros. Registre esse número no relatório como derivado da arma, com a conta.
2. **Ápice.** Com 0,227 a ponta em F05 fica em `y = 0,281 − 0,227 = 0,054`, dentro do canvas.
   Verifique você mesmo e confirme.
3. **Seguimento e recuperação.** O problema não é só o comprimento: a lâmina continua apontando
   para baixo até o fim. Depois do contato a espada deve girar para uma posição de recuperação
   atravessada, com a ponta para a frente ou para o lado, não cravada no chão. Ajuste
   `bladeDirection` em F09 a F13 para que a ponta fique acima do chão em todos eles.
4. **Regra de segurança.** Nenhuma ponta pode sair do intervalo `0,02 ≤ y ≤ 0,742` e
   `0,02 ≤ x ≤ 0,98` em nenhum quadro.

## O que NÃO mexer

O esqueleto está aprovado pela minha medição. Não altere nenhuma junta COCO, nem as cinco poses,
nem a grade de 730 ms, nem as fases, nem o `contactEvent` em F08/325 ms. Só os campos de
empunhadura: `grip.point`, `grip.bladeDirection` e o comprimento que você declarar.

## Prova

Atualize `sequence.json` e `poses.json`, e acrescente ao `report.md` uma tabela com a ponta da
lâmina quadro a quadro, mostrando que ela permanece no intervalo acima e que o arco de descida
continua monotônico de cima para baixo entre F05 e F08.
