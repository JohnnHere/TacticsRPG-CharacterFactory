# Validação técnica e revisão

Windows PowerShell + System.Drawing estão disponíveis na auditoria inicial. O script é somente leitura dos assets; opcionalmente escreve um relatório no caminho indicado. Em outros sistemas use decodificador disponível equivalente; não instale dependências sem autorização. Python não estava executável; o `quick_validate.py` oficial de skill-creator não pôde ser executado. Validação estrutural local deve ser registrada separadamente.

Da raiz:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .agents/skills/character-art-design/scripts/validate_character_assets.ps1 -AssetRoot Assets/Resources/Characters/WarriorPilot -OutputPath .agents/skills/character-art-design/tests/pilot-report.json
powershell -NoProfile -ExecutionPolicy Bypass -File .agents/skills/character-art-design/tests/test_validator.ps1
```

`ExecutionPolicy Bypass` aplica-se apenas ao processo de teste dos scripts locais revisados; não altera a política do sistema. Foi necessário nesta máquina, onde execução de scripts era bloqueada. Exit 0 = sem FAIL, não aprovação artística; exit 1 = FAIL. Erro de ambiente/parâmetro também encerra sem conformidade. Relatório JSON mantém status por verificação. Não escrever relatório em pastas de produção.

Perfil opcional `-ProfilePath <json>` substitui parâmetros padrão: `width`, `height`, `groundY`, `groundTolerance`, `minHeight`, `maxHeight`, `ppu`, `prefix`, `requireMeta`, `requireComplete`, `counts`, `exceptions`. `groundY:null` ou ambos limites de altura nulos desativam essa medição com NOT_RUN. `counts` substitui o inventário completo de estados. Para lote parcial use `requireComplete:false` e apenas estados pertinentes, mantendo o validador de nomes. Contagens aceitas 1–16 não comprovam compatibilidade do Walk.

Exceções: mapa `"arquivo/relativo.png|check": "motivo aprovado/documentado"` reclassifica FAIL para WARNING, preservando medida/motivo. Nunca esconda erro de formato, GUID ou runtime como aprovação artística. Perfis e exceções devem constar no pacote do personagem; evitar regras humanoides em formas excepcionais. Baseline de altura 90–105 é aproximação de auditoria, não nova regra canônica.

Checks: assinatura/decodificação PNG, dimensões, canal alfa explícito, transparência, bounds visíveis (qualquer alfa >0), chão, altura, borda/clipping, alfa parcial (possível halo), pixels decodificados duplicados, naming/inventário/sequência conforme perfil, metas/DefaultTexturePlatform/GUID duplicado dentro do lote, amplitude de topo do Idle e variações grandes de altura por vista. GUID global requer scan adicional do projeto. Não normaliza/salva PNGs.

Limitações: não aceita paleta+tRNS como RGBA de produção; processamento usa GetPixel, apropriado para lotes pequenos de 128px. Não determina halo por cor de borda, clusters intencionais, mão dominante, identidade cultural, qualidade de loop ou proporções subjetivas. Review entre direções, paleta/contatos e playtest são humanos. Bounds incluindo alfa parcial podem revelar resíduos, não localizar automaticamente o pé anatômico.

Confirme Resources.Load dentro de Unity após import autorizado; scan de metas não prova import atual. Execute EditMode DirectionMapping/IdleFrame/WalkFrame quando editor disponível, e PlayMode manual de production.md. Nesta tarefa nenhum código Unity mudou; não executar editor alterando assets como efeito colateral da criação da skill.
