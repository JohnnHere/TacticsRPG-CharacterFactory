# Pedido de criacao — orc-pixellab-07

Etapa: concept. Criar candidato de conceito 2D para aprovacao; nao produzir lote de sprites/animacoes finais nesta etapa.

Leia AGENTS.md e os documentos apontados em handoff.json. Abra e observe as imagens antes de gerar.

## Identidade e fontes

Raca: Orc; perfil documentado: Robusto; fantasia: Fúria.
Job: Warrior; papel: Dano físico. Afinidades sao contexto, sem bloqueio racial.
Ficha completa: character.json anexado. Campos TBD sao lacunas/propostas, nunca fatos aprovados.

- Proporcoes compactas taticas, maturidade, silhueta legivel no zoom do jogo.
- Clusters intencionais, materiais distintos, luz coerente com a ancora observada, detalhe controlado.
- Raca, individuo, Job, cultura, faccao, equipamento e forma sao eixos independentes.
- Sem espelhamento entre vistas; preservar mao dominante e assimetrias.
- Conceitos e sprites base do personagem ficam sem armas; armas sao assets separados, exibidos somente quando equipados e invocados por uma acao.
- Conceito e sprite nativo sao entregas diferentes. Reduzir conceito nao cria sprite pronto.
- Camadas 2D precisam de canvas, registro e timeline identicos; sobrepor imagens arbitrarias nao produz roupa compativel.
- Cores de pele, presas, cultura e ornamentacao racial ausentes nas fontes permanecem TBD/proposta.
- Gera-se conceito, depois base nativa, depois vistas, depois animacoes por lotes revisados.


Hero e referencia opcional de leitura e implementacao. Seu cabelo, armadura, arma e cores nao sao um uniforme do jogo.

## Autoria obrigatoria no Aseprite

Decisao expressa do criador em 2026-10-22: TODA a producao de arte deve acontecer no Aseprite, incluindo conceitos, sprites, poses, animacoes e acabamento. A fonte .aseprite salva e o arquivo mestre; PNGs/folhas sao derivados. Autoria por scripts Lua executados no Aseprite e permitida, com codigo, procedencia e referencias registrados; declarar que e autoria programatica do agente, nao desenho manual nem geracao inteligente do editor.
Nao usar image_gen ou outra geracao externa para produzir arte nova sem nova instrucao explicita do criador. Nao desenhar/reconstruir/recolorir pixels fora do Aseprite. Ferramentas externas podem organizar metadados, comparar hashes/pixels e montar previews sem alterar a arte. Legados aprovados preservam sua procedencia original.
Usar processos batch ocultos enquanto o criador usa a maquina; nao disputar a GUI. Sem Aseprite disponivel, registrar NOT_RUN e o bloqueio real; nao substituir a ferramenta. Preservar gates e copiar referencias sem promover historicos rejeitados.

## Entrega

Salvar candidatos PNG sem substituir refs aprovadas, registrar prompt/modelo quando conhecidos, mostrar preview e solicitar avaliacao artistica do lote. Nao autoaprovar. Conceito em resolucao alta permanece em concepts/. Sprite nativo precisa de producao propria e entra em sprites/ somente via importacao validada.

## Ficha resolvida

```json
{
  "schemaVersion": 1,
  "id": "orc-pixellab-07",
  "identityId": "7379deab-a507-4bca-acb9-c3b40e03980c",
  "name": "Veterano V4 Reimaginado",
  "status": "candidate",
  "createdAt": "2026-10-23T14:49:32.766Z",
  "styleId": "pixellab-v4-reinterpretation-v1",
  "race": {
    "id": "orc",
    "name": "Orc",
    "bodyProfile": "Robusto e atlético (candidato)"
  },
  "job": {
    "id": "warrior",
    "name": "Warrior"
  },
  "role": "Quarta opção da rodada PixelLab + Aseprite; releitura do Orc Warrior V4",
  "culture": "TBD",
  "faction": "TBD",
  "form": "base",
  "appearance": {
    "face": "Releitura de V4: face madura, sobrancelha marcada, presas curtas e olhos âmbar",
    "hair": "TBD",
    "ageImpression": "Adulto",
    "body": "Atlético e compacto, força funcional",
    "palette": [
      "verde-oliva",
      "vermelho carmim",
      "ferro escuro",
      "prata contida",
      "couro castanho"
    ],
    "dominantHand": "TBD após resultado",
    "asymmetries": [
      "Ombreira metálica assimétrica"
    ],
    "lighting": "Candidato PixelLab inspirado nos valores da V4"
  },
  "outfit": {
    "id": "orc-pixellab-07-candidate",
    "description": "Armadura funcional de ferro escuro, ombreira metálica assimétrica, lenço carmim, tiras de couro e cinto largo.",
    "equipmentMode": "weapon-independent-base",
    "weapon": "Asset separado; mãos vazias"
  },
  "profile": {
    "width": 128,
    "height": 128,
    "groundY": null,
    "ppu": 100,
    "counts": {
      "Idle": 8,
      "Walk": 8
    },
    "note": "Estudo conceitual candidato; formato de sprite de jogo ainda depende de validação."
  },
  "references": [
    {
      "path": "characters/orc-01-aseprite-v4/source/aseprite/retouched/concept/concept_front_r_00.png",
      "role": "creator-requested-design-reference",
      "sha256": "d08854d1870db326c99e4211db1565d22fc7371e3f03090ce482368d1163b16f"
    }
  ],
  "derivedFrom": null,
  "reuseAssessment": [
    {
      "component": "Character identity, pose and armor",
      "category": "CREATE_NEW",
      "evidence": "New PixelLab generation in a blank Aseprite canvas; the creator requested one V4-inspired option.",
      "adaptation": "Retain selected visual cues while redesigning the rendering and silhouette; no source pixels pasted.",
      "artRisk": "Model may reproduce V4 too literally or flatten its distinctive shapes.",
      "technicalRisk": "Generated concept may need cleanup before any production sprite use.",
      "dependencies": [
        "PixelLab Pro extension",
        "Aseprite blank 128x128 master"
      ],
      "validation": "GENERATED_PENDING_CREATOR_REVIEW",
      "productionImpact": "Candidate comparison only; no production or Unity assets replaced."
    },
    {
      "component": "Palette and material contrast",
      "category": "REUSE_ADAPTED",
      "evidence": "V4 style reference: characters/orc-01-aseprite-v4/source/aseprite/retouched/concept/concept_front_r_00.png; SHA256 d08854d1870db326c99e4211db1565d22fc7371e3f03090ce482368d1163b16f",
      "adaptation": "Use V4 olive, crimson, dark iron and controlled silver palette cues as PixelLab guidance.",
      "artRisk": "Palette may overwhelm the new silhouette.",
      "technicalRisk": "No runtime impact at concept stage.",
      "dependencies": [
        "PixelLab style/reference input"
      ],
      "validation": "GENERATED_PENDING_CREATOR_REVIEW",
      "productionImpact": "No active recipe or approval changes."
    }
  ],
  "artExploration": {
    "experiment": "pixellab-independent-orc-round2-v1",
    "inputImages": [
      "characters/orc-01-aseprite-v4/source/aseprite/retouched/concept/concept_front_r_00.png"
    ],
    "styleReferences": [
      "characters/orc-pixellab-07/source/pixellab-results/Style/v4-style-128.png"
    ],
    "referenceSha256": {
      "characters/orc-01-aseprite-v4/source/aseprite/retouched/concept/concept_front_r_00.png": "d08854d1870db326c99e4211db1565d22fc7371e3f03090ce482368d1163b16f"
    },
    "legacyPixels": false,
    "conceptualInfluence": "Aseprite Orc Warrior V4, explicitly authorized by creator for candidate 07 only.",
    "textualInspirations": [
      "World of Warcraft",
      "Tolkien"
    ],
    "candidateAnimationsAuthorized": true,
    "selection": null
  },
  "visualInspirationFrom": {
    "character": "orc-01-aseprite-v4",
    "role": "creator-authorized-style-reference-only",
    "sha256": "d08854d1870db326c99e4211db1565d22fc7371e3f03090ce482368d1163b16f"
  }
}
```
