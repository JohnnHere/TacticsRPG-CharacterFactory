# Pedido de criacao — hero-reference

Etapa: concept. Consultar este piloto como referencia historica de leitura/implementacao. Descrever e revisar o material existente. Para criar arte nova, abrir outro ID de personagem.

Leia AGENTS.md e os documentos apontados em handoff.json. Abra e observe as imagens antes de gerar.

## Identidade e fontes

Raca: Humano; perfil documentado: Humanoide; fantasia: Adaptação.
Job: Warrior; papel: Dano físico. Afinidades sao contexto, sem bloqueio racial.
Ficha completa: character.json anexado. Campos TBD sao lacunas/propostas, nunca fatos aprovados.

- Proporcoes compactas taticas, maturidade, silhueta legivel no zoom do jogo.
- Clusters intencionais, materiais distintos, luz coerente com a ancora observada, detalhe controlado.
- Raca, individuo, Job, cultura, faccao, equipamento e forma sao eixos independentes.
- Sem espelhamento entre vistas; preservar mao dominante e assimetrias.
- Conceito e sprite nativo sao entregas diferentes. Reduzir conceito nao cria sprite pronto.
- Camadas 2D precisam de canvas, registro e timeline identicos; sobrepor imagens arbitrarias nao produz roupa compativel.
- Cores de pele, presas, cultura e ornamentacao racial ausentes nas fontes permanecem TBD/proposta.
- Gera-se conceito, depois base nativa, depois vistas, depois animacoes por lotes revisados.


Hero e referencia opcional de leitura e implementacao. Seu cabelo, armadura, arma e cores nao sao um uniforme do jogo.

## Geracao na conversa

Se image_gen estiver disponivel, usar a ferramenta de imagem com estas referencias e salvar o resultado no workspace. Verificar a skill de imagem da sessao. Sem ferramenta, entregar instrucoes e registrar NOT_RUN; nao simular criacao com texto/SVG ou recoloracao do Hero.
Nao acionar APIs pagas ou automatizar login em Google/ChatGPT. O pacote tambem pode ser usado manualmente em outra ferramenta disponivel ao criador.

## Entrega

Salvar candidatos PNG sem substituir refs aprovadas, registrar prompt/modelo quando conhecidos, mostrar preview e solicitar avaliacao artistica do lote. Nao autoaprovar. Conceito em resolucao alta permanece em concepts/. Sprite nativo precisa de producao propria e entra em sprites/ somente via importacao validada.

## Ficha resolvida

```json
{
  "schemaVersion": 1,
  "id": "hero-reference",
  "identityId": "27a807a5-c1c0-4a86-a549-ae2b4b6a1f0d",
  "name": "Human Warrior Pilot / Hero do sandbox",
  "status": "reference_only",
  "createdAt": "2026-10-18T22:29:57.102Z",
  "styleId": "tactics-core-v1",
  "race": {
    "id": "humano",
    "name": "Humano",
    "bodyProfile": "Humanoide"
  },
  "job": {
    "id": "warrior",
    "name": "Warrior"
  },
  "role": "TBD",
  "culture": "TBD",
  "faction": "TBD",
  "form": "base",
  "appearance": {
    "face": "Humano masculino adulto/jovem-adulto, cabelo castanho, expressao seria.",
    "body": "Proporcoes compactas do piloto; nao obrigatorias para outras racas.",
    "palette": [
      "prata",
      "azul-marinho",
      "couro marrom",
      "ouro contido"
    ],
    "dominantHand": "Revisao entre vistas pendente no historico",
    "asymmetries": [
      "capa e espada"
    ],
    "lighting": "Consultar ancora."
  },
  "outfit": {
    "id": "warrior-candidate",
    "description": "Armadura do piloto. Opcional como referencia, nao uniforme global.",
    "equipmentMode": "embedded-pilot-exception",
    "weapon": "TBD"
  },
  "profile": {
    "width": 128,
    "height": 128,
    "groundY": 126,
    "ppu": 100,
    "counts": {
      "Idle": 4,
      "Walk": 6,
      "Attack": 5,
      "Hit": 3,
      "Defeat": 5
    },
    "note": "Baseline do piloto humanoide 1 tile; anatomias diferentes exigem perfil e revisao. Walk atual usa 3 quadros/tile."
  },
  "references": [
    {
      "path": "references/tacticsrpg/Docs/Art/References/character_style_anchor_v1.png",
      "role": "global-style-anchor"
    }
  ],
  "derivedFrom": null,
  "reuseAssessment": [
    {
      "component": "rendering/reference contract",
      "category": "REUSE_DIRECT",
      "evidence": "Docs/ART_DIRECTION.md + ancora",
      "adaptation": "Aplicar ao novo corpo; revisar em escala de jogo."
    },
    {
      "component": "race anatomy/face",
      "category": "CREATE_NEW",
      "evidence": "RACES.md fornece perfil, sem modelo racial aprovado.",
      "adaptation": "TBD",
      "artRisk": "TBD",
      "technicalRisk": "Validar canvas/escala",
      "dependencies": [],
      "validation": "NOT_RUN",
      "productionImpact": "TBD"
    },
    {
      "component": "job outfit",
      "category": "CREATE_NEW",
      "evidence": "references/tacticsrpg/Docs/GameDesign/JOB_CATALOG.md",
      "adaptation": "TBD",
      "artRisk": "Identidade de classe deve permanecer entre racas.",
      "technicalRisk": "Camadas por vista/quadro",
      "dependencies": [],
      "validation": "NOT_RUN",
      "productionImpact": "TBD"
    },
    {
      "component": "Unity registration",
      "category": "REQUIRES_EXTENSION",
      "evidence": "UnitVisuals fixa WarriorPilot.",
      "adaptation": "Registro multi-personagem externo a esta fabrica.",
      "validation": "NOT_RUN"
    }
  ]
}
```
