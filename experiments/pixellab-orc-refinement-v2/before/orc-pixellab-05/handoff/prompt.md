# Pedido de criacao — orc-pixellab-05

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
  "id": "orc-pixellab-05",
  "identityId": "9891c3ed-5b4c-44c0-8192-cf7786d8a7ef",
  "name": "Infante de Ferro",
  "status": "candidate",
  "createdAt": "2026-10-23T12:53:21.732Z",
  "styleId": "pixellab-orc-contrast-study-v2",
  "race": {
    "id": "orc",
    "name": "Orc",
    "bodyProfile": "Robusto (variações individuais candidatas)"
  },
  "job": {
    "id": "warrior",
    "name": "Warrior"
  },
  "role": "Estudo independente de Orc Warrior",
  "culture": "TBD",
  "faction": "TBD",
  "form": "base",
  "appearance": {
    "face": "Proposta PixelLab pendente",
    "hair": "Descrito no prompt; candidato",
    "ageImpression": "Adulto",
    "body": "A heavy adult male orc shock infantryman in the broad cinematic Uruk-hai tradition of Tolkien fantasy: dense powerful torso, thick neck, squared scarred face, heavy brow, blunt tusks, ash-grey skin with a cold undertone, close-cropped black hair. Functional dark gunmetal plate assembled from broad overlapping bands, iron rivets, a rough dark-red waist cloth and utilitarian leather bindings. Militaristic, disciplined and brutal, with a distinctly different silhouette and palette from a green heroic warrior. No franchise emblems or recognizable named character details.",
    "palette": [],
    "dominantHand": "TBD após resultado",
    "asymmetries": [],
    "lighting": "PixelLab candidato"
  },
  "outfit": {
    "id": "orc-pixellab-05-candidate",
    "description": "A heavy adult male orc shock infantryman in the broad cinematic Uruk-hai tradition of Tolkien fantasy: dense powerful torso, thick neck, squared scarred face, heavy brow, blunt tusks, ash-grey skin with a cold undertone, close-cropped black hair. Functional dark gunmetal plate assembled from broad overlapping bands, iron rivets, a rough dark-red waist cloth and utilitarian leather bindings. Militaristic, disciplined and brutal, with a distinctly different silhouette and palette from a green heroic warrior. No franchise emblems or recognizable named character details. undefined",
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
    "note": "Estudos candidatos; ainda não é contrato de runtime."
  },
  "references": [],
  "derivedFrom": null,
  "reuseAssessment": [
    {
      "component": "Character identity, silhouette, face, palette, outfit and poses",
      "category": "CREATE_NEW",
      "evidence": "Creator requested a new contrast round with three distinct textual briefs.",
      "adaptation": "PixelLab Create image Pro from a blank 128x128 Aseprite document; text only, no image conditioning.",
      "artRisk": "The model may converge on the first round despite different prompts.",
      "technicalRisk": "Animation and small-scale readability remain review studies.",
      "dependencies": [
        "Installed PixelLab extension and authenticated account"
      ],
      "validation": "NOT_RUN",
      "productionImpact": "No current candidate, approval, or production asset is replaced."
    },
    {
      "component": "Aseprite masters, export and review tools",
      "category": "REUSE_DIRECT",
      "evidence": "Existing local Aseprite bridge and packaging workflow.",
      "adaptation": "New independent IDs and source paths.",
      "artRisk": "Technical export does not prove artistic quality.",
      "technicalRisk": "None beyond normal preview checks.",
      "dependencies": [
        "Aseprite 1.3+"
      ],
      "validation": "NOT_RUN",
      "productionImpact": "Candidate review only."
    }
  ],
  "artExploration": {
    "experiment": "pixellab-independent-orc-round2-v1",
    "inputImages": [],
    "styleReferences": [],
    "legacyPixels": false,
    "textualInspirations": [
      "Tolkien",
      "World of Warcraft"
    ],
    "candidateAnimationsAuthorized": true,
    "selection": null
  }
}
```
