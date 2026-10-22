# Regras de acesso a Jobs v2.1

## Regra canônica v2.1 (substitui propostas anteriores)
- Desbloqueio de Jobs e aprendizado de habilidades são **progressão pura**: níveis de Jobs, combinações de classes, pontos de progressão e pré-requisitos de talentos (`DESIGN_DECISIONS.md` §Regra canônica v2.1).
- **Nenhum** Job ou habilidade é desbloqueado por missões, exploração, itens encontrados, NPCs, tutores obrigatórios, rituais, provas, contratos, pactos ou eventos narrativos. Facção/cultura podem explicar o *tema* do acesso, mas a fórmula de desbloqueio é progressão.
- O caráter "secreto" de um Job está em requisitos complexos ou ocultos na interface — nunca em conteúdo narrativo.
- Recrutamento de personagens para o grupo permanece narrativo e independente desta regra.

## Camadas independentes
1. `RaceId`: traços biológicos e forma; não define moralidade ou facção.
2. `CultureId`/`LineageId`: tradição e conhecimentos; High Elf é condição aristocrática/institucional.
3. `FactionId` e reputação: narrativa, recrutamento e conflitos; **não** participam da fórmula de desbloqueio de habilidades/Jobs (v2.1).
4. `RecruitmentRule`: quando e como uma unidade entra no grupo (narrativo, preservado).
5. `JobUnlockRule`: pré-requisitos de progressão (níveis de Jobs e talentos).
6. `JobAffinityRule`: caminhos facilitados, sem bloquear alternativas.
7. `JobCompatibilityRule`: apenas restrições físicas/sobrenaturais justificadas, com variantes de animação e equipamentos quando necessário.
8. `UniqueJobOwnerId`: Jobs de personagem, não de raça.

## Política inicial
- Todas as 28 raças são jogáveis em alguma medida; nem todas são recrutáveis cedo, comuns ou amigáveis ao protagonista.
- **Todas as raças podem alcançar Jobs universais e a maior parte dos intermediários/avançados**, por treinamento e acesso narrativo.
- Afinidade reduz esforço ou oferece mentor alternativo, não muda a potência final por origem.
- Bloqueios absolutos são raros e justificados por anatomia/essência (ex.: metamorfose lupina racial, sopro biológico de Dragonborn), **não por preconceito do mundo**.
- Jobs secretos exigem progressão complexa e/ou requisitos ocultos na interface; Jobs únicos dependem de personagem definido, com habilidades aprendidas pela árvore do Job.
- Um High Elf não ganha magia inata superior: sua aristocracia pode facilitar acesso a academia, tutores e patrocínio, enquanto outros podem conquistar acesso por mérito, missão ou rebelião.
- Raças hostis por facção podem se tornar aliadas por deserção, pacto, missão ou diplomacia.

## Modelo de dificuldade de acesso (por unidade, não por espécie inteira)
- **A — Natural:** requisitos usuais de progressão atendidos.
- **B — Aprendível:** requisitos usuais com custo de pontos adicional leve.
- **C — Raro:** cadeia de pré-requisitos longa (múltiplos Jobs/talentos).
- **D — Secreto:** requisitos complexos ou ocultos na interface até quase atendidos.
- **E — Exclusivo:** só personagem definido ou poder racial intrínseco (sem aprendizado; identidade do personagem).
- Nenhum Job universal recebe E por raça; E para Jobs únicos não significa raça proibida.

## Afinidades exemplares, sem travas
- Orc: Warrior/Berserker A, White Mage B/C (cadeia de progressão mais longa).
- Gnomo: Engineer/Artificer A, Berserker B/C conforme pontos investidos.
- Moon Elf: Time Mage/Chronomancer facilitado por talentos da tradição lunar, não inato.
- High Elf: Samurai/Royal Strategist via talentos culturais; origem não garante talento.
- Merfolk: Tidecaller A, Dragoon B com pré-requisitos adaptados.
- Constructo: Artificer/Runesmith A; White Mage possível, mas cura sobre corpo artificial exige interação explícita (condição de execução).
- Demon: Warlock A, Paladin C mediante cadeia de progressão mais longa (não proibição moral).
- Undead: Necromancer A, White Mage B/C com cura/resurreição adaptadas (condição de execução).

## Algoritmo de desbloqueio
`Unlocked = JobPrerequisitesMet && TalentPointsSpent && CompatibleBodyPlan && !UniqueOwnerMismatch`
Afinidade altera custo de pontos/rota de talentos, não `Unlocked` diretamente. Mostrar na UI requisito faltante e rota alternativa.

## Adições v2.0 (revisadas v2.1: gatilhos narrativos substituídos por talentos)
- **Venomancer**: Alchemist 3 + Rogue 2 + talento de toxicologia; afinidades Lizardfolk, Goblin e Dark Elf. Não exclusivo.
- **Affliction Master**: Oracle 4 + Venomancer 3 + Black Mage 3 + talento de aflição; afinidades Dark Elf, Undead, Vampiro e Half-Demon. **Não exige Warlock nem pacto demoníaco**.
- **Shaman**: continua Acolyte 2 + Elementalist 2 + talento de rito natural; acesso a venenos/raízes/bonecos sem ser o melhor DoT.
- Nenhum requisito numérico é definitivo; `RaceId`, `FactionId`, `CultureId` e `JobId` não devem ser inferidos do nome de exibição.
