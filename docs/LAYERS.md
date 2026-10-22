# Corpo e roupas em camadas 2D

O modelo inicial compoe corpo e roupa em PNGs offline. Cada variante de roupa gera o sprite completo que o Unity toca como hoje; a fonte editavel mantem essas pecas separadas. Armas sao assets independentes: nao fazem parte do personagem base nem de Idle/Walk e so devem ser renderizadas quando uma acao equipada as invoca. Nao existe deformacao/rig 3D nem overlay dinamico de arma nesta fabrica/runtime.

## Contrato de uma camada

PNG RGBA8 no canvas exato da ficha, sem trim, deslocamento, espelhamento ou reescala. Pixels desenhados no mesmo sistema de coordenadas. Todas as pecas de um quadro compartilham direcao de tela e instante da animacao. Mascara de oclusao deve estar desenhada no alfa da camada. Capa atras/capa na frente, mao e arco podem exigir pecas separadas e ordem distinta por quadro.

Corpo robusto Orc e corpo Undead variavel nao aceitam automaticamente a mesma roupa. Reutilizar exige adaptacao visual e revisao de clipping, volume, proporcao e contatos. A descricao da classe pode ser comum enquanto o desenho tem variante anatomica.

## Exemplo executavel quando houver arte

Coloque body_front_r.png e outfit_front_r.png em characters/<id>/source/layers/. Copie source/layers.example.json para source/layers.json e ajuste o slot para o ID real. A composicao base fica sem arma. Um asset de arma separado nao e suportado pelo contrato atual do compose; a invocacao em uma acao depende de uma futura extensao.

```json
{
  "schemaVersion": 1,
  "frames": [
    {
      "slot": "orc_01_mvp1_static_128.png",
      "layers": ["body_front_r.png", "outfit_front_r.png"]
    }
  ]
}
```

`node src/cli.mjs compose --id orc-01 --manifest characters/orc-01/source/layers.json`

Ordem de tras para frente, composicao source-over por pixel. O programa valida todos os frames/caminhos/canvas antes de escrever as saidas. Registra hashes de cada camada em assets.json. Saida existente exige --force. Gate 1 e obrigatorio; para quadros de animacao, a revisao da base/vistas tambem e obrigatoria. Nao adicione uma arma a todos os frames para simular uma arma equipada: a regra e invocar o asset separado apenas na acao correspondente.

## Reuso real

Separar materiais de roupa na fonte ajuda recoloracoes controladas. Rosto, pele, corpo e assimetrias do individuo permanecem fixos quando troca Job. Armas devem ter assets proprios, encaixes e regras de acao; animação de ataque com espada nao vira tiro de arco so por trocar a arma. Novos movimentos pedem autoria dos quadros e suporte de playback/sincronia no jogo. Clipes do piloto nao sao uma biblioteca universal para 63 Jobs.
