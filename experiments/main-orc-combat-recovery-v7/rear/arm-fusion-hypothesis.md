# Hipótese de fusão do braço — V7 back_l

## Observações

Os corpos brutos de `raw/sword/` e `raw/axe/` foram gerados em 128×128. Nos ápices a mão e o antebraço frequentemente ficam incorporados à massa escura do ombro; a orientação e a palma não podem ser distinguidas. Na segunda tentativa `raw/sword2/`, afastar as juntas para a direita produziu mão mais separada nos quadros elevados, mas o braço volta a fundir-se ao tronco durante a descida. A cadeia ombro–cotovelo–punho–palma não é verificável ao longo desse trecho. Essas são observações visuais, não prova do funcionamento interno do modelo.

## Hipóteses técnicas

- **Resolução:** no canvas 128 o antebraço ocupa apenas poucos pixels de largura; contorno escuro, luva e armadura competem pelos mesmos pixels. Uma folga pequena pode desaparecer por quantização ou reconstrução gerativa. Não medimos ainda a largura real em cada frame.
- **Oclusão projetada:** ao deslocar o punho para dentro da projeção da cabeça ou da placa dorsal, o membro se sobrepõe à silhueta do tronco e perde a separação; sem pista de profundidade clara, o modelo pode integrar seu contorno à armadura.
- **Esqueleto:** coordenadas 2D e profundidade solicitadas não garantem volumetria; em alguns quadros a distância projetada cotovelo–punho é curta e a flexão dobra o antebraço sobre o ombro. A hipótese de colapso é compatível com os raws, mas não estabelece uma causa interna do gerador.
- **Espaço negativo:** as primeiras sequências pediam mão próxima ou sobre a cabeça/torso, sem especificar uma faixa de transparência contínua entre braço e cabeça/pescoço. A segunda afastou a mão no ápice, melhorando a separação nesse trecho, sem resolver a descida. A abertura deve ser visível na saída, não apenas prescrita.
- **Identidade versus pose:** as espaldeiras largas e escuras da referência ocupam o mesmo espaço onde se pede o membro; a manutenção da identidade pode competir com a nova silhueta. Isto é hipótese, não causa comprovada.

## Mudança de método

Não repetir o job temporal de 12 poses nem aprovar quase: testar apenas um ápice. O resultado precisa mostrar punho acima da cabeça, cotovelo legível, palma fechada, antebraço separado e espaço negativo entre braço e cabeça/pescoço. Inspecionar corpo inteiro desarmado antes de qualquer composição.
