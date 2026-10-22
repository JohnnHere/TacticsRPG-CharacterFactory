using System.Collections;
using System.Collections.Generic;
using TacticsRPG.Core;
using UnityEngine;

namespace TacticsRPG.Presentation
{
    /// <summary>
    /// Boneco genérico (cápsula com "nariz" indicando a frente) que reflete uma <see cref="Core.Unit"/>.
    /// MVP 2: um sprite opcional (ex.: Human Warrior Pilot) substitui visualmente a cápsula —
    /// billboard de câmera em filho próprio; a vista do sprite é o indicador de direção em jogo.
    /// MVP 3D: nas unidades com sprite o cubo branco "Front" fica com o renderer desligado
    /// (o facing tático continua no Core e no debug F3); cápsulas mantêm o indicador como antes.
    /// </summary>
    public sealed class UnitView : MonoBehaviour
    {
        const float StepTime = 0.22f;
        const float HopPerHeight = 0.12f;
        // Cápsula primitiva tem altura 2; com escala Y 0.5 fica 1 e o pivô no centro.
        const float BodyHalfHeight = 0.5f;

        Renderer _renderer;
        Transform _spriteHolder;
        SpriteRenderer _sprite;
        Transform _facingMark;
        Transform _shadow;
        BattleMap _map;
        static Material _shadowMaterial;
        MaterialPropertyBlock _block;
        Color _baseColor;
        Vector3 _baseScale;
        Sprite[] _directions;
        Sprite _fallbackSprite;
        Sprite[][] _idleByDirection;
        Sprite[][] _walkByDirection;
        float _scale = 1f;
        int _dirIndex = -1;
        float _idleTime;
        bool _moving;
        int _stepIndex;
        float _stepT;
        Sprite[][] _overrideByDirection;   // MVP 4: clipe transitório de combate (Attack/Hit/Defeat)
        float _overrideTime;
        float _overrideSecondsPerFrame = 0.1f;
        bool _overrideEnds;                // true = one-shot (expira); false = Defeat (trava até sumir)

        // Durações por quadro (MVP 4): Attack 5×0,09 ≈ 0,45 s; Hit 3×0,08 = 0,24 s; Defeat 5×0,12 = 0,60 s.
        public const float AttackSecondsPerFrame = 0.09f;
        public const float HitSecondsPerFrame = 0.08f;
        public const float DefeatSecondsPerFrame = 0.12f;

        // MVP 3 (HUMAN_WARRIOR_ANIMATIONS.md §4): Idle de 4 quadros a 0,24 s (ciclo ~0,96 s @1×);
        // Walk de 6 quadros, 3 por passo (ciclo = 2 passos = 0,44 s @1×).
        const float IdleSecondsPerFrame = 0.24f;
        const int WalkFramesPerStep = 3;

        // Rótulos de tela na ordem dos índices do conjunto direcional (UnitVisuals).
        public static readonly string[] DirectionNames = { "back_l", "back_r", "front_r", "front_l" };

        /// <summary>Depuração (F3): última vista direcional selecionada, ex.: "[front_r d=135°]".</summary>
        public string DirectionLabel { get; private set; } = "";

        public Unit Unit { get; private set; }

        public static UnitView Create(Unit unit, Color color, BattleMap map, Sprite sprite = null, float spriteScale = 1f)
        {
            // Raiz com escala uniforme 1: filhos (sprite, indicadores) não herdam escala distorcida
            // e o Vanish continua encolhendo o conjunto inteiro. Visual da cápsula é idêntico ao anterior.
            var go = new GameObject(unit.Name);

            var body = GameObject.CreatePrimitive(PrimitiveType.Capsule);
            body.name = "Body";
            Destroy(body.GetComponent<Collider>());
            body.transform.SetParent(go.transform, false);
            body.transform.localScale = new Vector3(0.6f, BodyHalfHeight, 0.6f);

            var nose = GameObject.CreatePrimitive(PrimitiveType.Cube);
            nose.name = "Front";
            Destroy(nose.GetComponent<Collider>());
            nose.transform.SetParent(body.transform, false);
            nose.transform.localPosition = new Vector3(0f, 0.3f, 0.6f);
            nose.transform.localScale = new Vector3(0.4f, 0.4f, 0.4f);
            nose.GetComponent<Renderer>().sharedMaterial = MapView.GetMaterial(Color.white);

            var view = go.AddComponent<UnitView>();
            view.Unit = unit;
            view._map = map;
            view._facingMark = nose.transform;
            view._renderer = body.GetComponent<Renderer>();
            view._renderer.sharedMaterial = MapView.GetMaterial(Color.white);
            view._baseScale = go.transform.localScale;
            if (sprite != null) view.UseSprite(sprite, spriteScale);
            view.SetColor(color);
            view.Place(map, unit.Pos);
            view.SetFacing(unit.Facing);
            return view;
        }

        /// <summary>
        /// Troca a cápsula por um sprite (MVP 1: arte estática). O sprite é billboard da câmera tática
        /// (giros de 90° legíveis sem espelhar), escalado por um multiplicador de perfil visual com os
        /// pés continuando no chão do tile. O cubo branco "Front" é DESLIGADO nas unidades com sprite
        /// (a direção já é lida pela própria arte; MVP 3D a pedido do criador) — GameObject e facing
        /// do Core permanecem intactos. Cápsulas (unidades sem sprite) continuam com o indicador.
        /// </summary>
        public void UseSprite(Sprite sprite, float scale = 1f)
        {
            if (_spriteHolder == null)
            {
                _spriteHolder = new GameObject("Sprite").transform;
                _spriteHolder.SetParent(transform, false);
                _sprite = _spriteHolder.gameObject.AddComponent<SpriteRenderer>();
                CreateGroundShadow();
            }

            _scale = scale;
            _fallbackSprite = sprite;
            _spriteHolder.localScale = Vector3.one * scale;
            ApplySprite(sprite);

            // MVP 3D: esconde o indicador branco nas unidades com sprite (poluição visual sobre a
            // arte). Nada de gameplay: Facing vive no Core e a vista do sprite já comunica direção.
            if (_facingMark != null && _facingMark.TryGetComponent(out Renderer markRenderer))
                markRenderer.enabled = false;

            _renderer.enabled = false;
        }

        /// <summary>
        /// MVP 2: conjunto direcional (rótulos de tela: back_l, back_r, front_r, front_l). A vista é
        /// escolhida pelo ângulo relativo entre o facing de mundo (rotação da raiz, definida pelo
        /// Core) e o yaw REAL da câmera; vista ausente cai no sprite estático (sem espelhamento).
        /// Requer UseSprite chamado antes (fallback/escala já configurados).
        /// </summary>
        public void UseDirectionalSprites(Sprite[] byDirection)
        {
            if (_spriteHolder == null) return;
            _directions = byDirection;
            _dirIndex = -1; // força re-seleção no próximo LateUpdate
        }

        /// <summary>
        /// MVP 3A: quadros de Idle por índice de direção (entradas null → estático do MVP 2).
        /// Toca em loop enquanto a unidade está parada; o clock não reinicia ao trocar de vista.
        /// Requer UseSprite já chamado. Estrutura tolera o Walk futuro (estado por clipe).
        /// </summary>
        public void UseIdleFrames(Sprite[][] idleByDirection)
        {
            if (_spriteHolder == null) return;
            _idleByDirection = idleByDirection;
        }

        /// <summary>
        /// MVP 3B: quadros de Walk por índice de direção (entradas null → estático do MVP 2
        /// durante o movimento). Requer UseSprite já chamado.
        /// </summary>
        public void UseWalkFrames(Sprite[][] walkByDirection)
        {
            if (_spriteHolder == null) return;
            _walkByDirection = walkByDirection;
        }

        /// <summary>
        /// MVP 4: clipe de combate de UM shot (Attack no atacante; Hit no alvo quando o golpe
        /// acerta). Toca uma vez com o clock da velocidade de animação e devolve para
        /// Idle/Walk/estático; a vista do quadro segue o DirectionIndex (giro de câmera ok).
        /// Tabela null ou sem quadros = ignora (cápsulas e vistas sem arte não são afetadas).
        /// </summary>
        public void PlayOneShot(Sprite[][] byDirection, float secondsPerFrame)
        {
            if (_spriteHolder == null || byDirection == null) return;
            _overrideByDirection = byDirection;
            _overrideSecondsPerFrame = Mathf.Max(0.01f, secondsPerFrame);
            _overrideTime = 0f;
            _overrideEnds = true;
        }

        /// <summary>
        /// MVP 4: clipe de Defeat — como PlayOneShot, mas SEM expirar: trava o visual no clipe
        /// até a view ser destruída (Idle/Walk/estático não retomam). Não altera o resultado do
        /// gameplay; apenas dá tempo para a animação terminar antes do desaparecimento.
        /// </summary>
        public void PlayDefeat(Sprite[][] byDirection, float secondsPerFrame)
        {
            if (_spriteHolder == null || byDirection == null) return;
            _overrideByDirection = byDirection;
            _overrideSecondsPerFrame = Mathf.Max(0.01f, secondsPerFrame);
            _overrideTime = 0f;
            _overrideEnds = false;
        }

        /// <summary>
        /// Quadro de Idle para o tempo decorrido (loop uniforme; puro e testável).
        /// Ex.: 4 quadros a 0,24 s → ciclo de 0,96 s.
        /// </summary>
        public static int IdleFrameIndex(float elapsedSeconds, int frameCount, float secondsPerFrame) =>
            frameCount <= 0 ? 0 : Mathf.FloorToInt(elapsedSeconds / Mathf.Max(0.001f, secondsPerFrame)) % frameCount;

        /// <summary>
        /// MVP 3B: quadro de Walk a partir do passo CUMULATIVO do caminho e do `t` normalizado
        /// (0→1) do passo atual — o mesmo `t` da interpolação de MoveAlong, então a velocidade
        /// de animação (1×/2×/4×/50×) já está embutida e NÃO é multiplicada de novo. Ciclo de
        /// `framesPerStep` passos: pares de passos usam a primeira metade dos quadros, ímpares a
        /// segunda (6 quadros = 3/passo); `t ≥ 1` clampA no último quadro do trecho. Puro e
        /// testável; garante índice dentro de [0, frameCount).
        /// </summary>
        public static int WalkFrameIndex(int stepIndex, float stepT, int framesPerStep, int frameCount)
        {
            if (frameCount <= 0 || framesPerStep <= 0) return 0;
            int inStep = stepT <= 0f ? 0 : Mathf.Min(framesPerStep - 1, Mathf.FloorToInt(stepT * framesPerStep));
            return Mathf.Abs(stepIndex * framesPerStep + inStep) % frameCount;
        }

        // Aplica o sprite (e reposiciona os pés — cada vista tem bounds próprios) só quando muda.
        void ApplySprite(Sprite sprite)
        {
            if (sprite == null || _sprite.sprite == sprite) return;
            _sprite.sprite = sprite;
            _spriteHolder.localPosition = new Vector3(0f, -BodyHalfHeight - sprite.bounds.min.y * _scale, 0f);
        }

        /// <summary>
        /// MVP 2: índice da vista direcional (rótulos de TELA) a partir dos yaws em graus da
        /// unidade (raiz, definida pelo Core Facing) e da câmera. Vista mais próxima da direção
        /// aparente em tela: setores de 90° centrados nas diagonais (45°+90k), limites nos
        /// cardinais (0/90/180/270) — nos estados de repouso (câmera quantizada) d é exatamente
        /// diagonal e o resultado é inteiro exato; durante o giro da câmera (ou numa futura
        /// câmera livre) escolhe a vista vizinha mais próxima em vez de saltar 90°. O arredondamento
        /// bancário do RoundToInt é inofensivo aqui: casos .5 caem só nos cardinais, onde ambos
        /// os vizinhos são equidistantes. Tabela das 16 combinações congelada em DirectionMappingTests
        /// e em `HUMAN_WARRIOR_DIRECTIONS.md` §2.
        /// </summary>
        public static int DirectionIndex(float unitYaw, float cameraYaw) =>
            Mathf.RoundToInt((Mathf.Repeat(unitYaw - cameraYaw, 360f) + 45f) / 90f) & 3;

        // Sombra de contato simples (disco transparente): ancora a leitura do sprite no tile.
        // Fica no chão mesmo durante o hop (segue o tile mais próximo) e encolhe junto no Vanish.
        void CreateGroundShadow()
        {
            var disc = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            disc.name = "Shadow";
            Destroy(disc.GetComponent<Collider>());

            _shadowMaterial ??= CreateShadowMaterial();
            Renderer r = disc.GetComponent<Renderer>();
            r.sharedMaterial = _shadowMaterial;
            r.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off;
            r.receiveShadows = false;

            _shadow = disc.transform;
            _shadow.SetParent(transform, false);
            _shadow.localScale = new Vector3(0.7f, 0.01f, 0.7f);
        }

        // MVP 4 (correção do disco magenta do playtest 1.14): a sombra usa O MESMO shader do
        // sprite do piloto — que já renderiza corretamente neste projeto/URP. A versão anterior
        // buscava "Sprites/Default" por nome via Shader.Find, que resolveu para o error-shader
        // (disco magenta). Não depender de busca por nome.
        Material CreateShadowMaterial()
        {
            Shader shader = _sprite != null && _sprite.sharedMaterial != null
                ? _sprite.sharedMaterial.shader
                : null;
            if (shader == null) shader = Shader.Find("Sprites/Default");
            return new Material(shader) { color = new Color(0f, 0f, 0f, 0.35f) };
        }

        // Billboard cilíndrico: acompanha os giros de 90° da câmera sem deitar o sprite e sem
        // tocar no facing tático (que vive no Core e aparece no debug F3). A sombra é presa ao
        // topo do tile mais próximo a cada quadro (acompanha desníveis, hop e empurrões).
        void LateUpdate()
        {
            if (_spriteHolder == null) return;
            Camera cam = Camera.main;
            if (cam == null) return;

            Vector3 forward = cam.transform.forward;
            forward.y = 0f;
            if (forward.sqrMagnitude > 0.0001f) _spriteHolder.rotation = Quaternion.LookRotation(forward);

            if (_directions != null)
            {
                // d = ângulo relativo facing (raiz) × câmera; setores de 90° centrados nas
                // diagonais (45°+90k). Derivado do yaw real — sobrevive a câmera livre no futuro.
                int idx = DirectionIndex(transform.eulerAngles.y, cam.transform.eulerAngles.y);
                if (idx != _dirIndex)
                {
                    float d = Mathf.Repeat(transform.eulerAngles.y - cam.transform.eulerAngles.y, 360f);
                    _dirIndex = idx;
                    DirectionLabel = $"[{DirectionNames[idx]} d={d:0}°]"; // aloca só na troca
                }

                // MVP 3A/3B: ÚNICA autoridade de seleção de sprite. Em movimento, o Walk avança
                // pelo t do passo mantido em MoveAlong; parado, o Idle avança pelo relógio.
                // Sem clipe na vista → estático do MVP 2 → estático MVP 1 → cápsula (ApplySprite
                // ignora repetição — nada de carga ou alocação por quadro).
                // MVP 4: estado transitório de combate tem precedência (Defeat > Hit > Attack);
                // o quadro segue o DirectionIndex e o clock da velocidade de animação. One-shot
                // expira sozinho e devolve para Walk/Idle/estático; vista sem quadro do clipe →
                // estático do MVP 2 (fallback imediato, sem travar). Defeat não expira.
                if (_overrideByDirection != null)
                {
                    Sprite[] clip = _overrideByDirection[idx];
                    if (clip == null)
                    {
                        _overrideByDirection = null;
                    }
                    else
                    {
                        _overrideTime += Time.deltaTime * GameSettings.AnimationSpeed;
                        ApplySprite(clip[IdleFrameIndex(_overrideTime, clip.Length, _overrideSecondsPerFrame)]);
                        if (_overrideEnds && _overrideTime >= clip.Length * _overrideSecondsPerFrame)
                            _overrideByDirection = null; // terminou → Idle/Walk/estático retomam
                    }
                }

                if (_overrideByDirection == null)
                {
                    if (_moving)
                    {
                        Sprite[] walk = _walkByDirection?[idx];
                        if (walk != null)
                            ApplySprite(walk[WalkFrameIndex(_stepIndex, _stepT, WalkFramesPerStep, walk.Length)]);
                        else
                            ApplySprite(_directions[idx] ?? _fallbackSprite);
                    }
                    else
                    {
                        Sprite[] idle = _idleByDirection?[idx];
                        if (idle != null)
                        {
                            _idleTime += Time.deltaTime * GameSettings.AnimationSpeed;
                            ApplySprite(idle[IdleFrameIndex(_idleTime, idle.Length, IdleSecondsPerFrame)]);
                        }
                        else
                        {
                            ApplySprite(_directions[idx] ?? _fallbackSprite);
                        }
                    }
                }
            }

            if (_shadow != null && _map != null)
            {
                var tile = new GridPos(Mathf.RoundToInt(transform.position.x), Mathf.RoundToInt(transform.position.z));
                float ground = MapView.TileTop(_map, tile).y + 0.02f;
                float s = Mathf.Max(0.05f, transform.localScale.y);
                _shadow.localPosition = new Vector3(0f, (ground - transform.position.y) / s, 0f);
            }
        }

        /// <summary>Muda a cor base (usada também ao trocar a paleta de daltonismo).</summary>
        public void SetColor(Color color)
        {
            _baseColor = color;
            Tint(VisualBase);
        }

        // Sprite usa branco como cor de repouso (não repinta a arte); cápsula usa a cor do time.
        Color VisualBase => _sprite != null ? Color.white : _baseColor;

        // Cor por MaterialPropertyBlock: não cria material novo e aceita URP (_BaseColor) e Standard (_Color).
        void Tint(Color color)
        {
            _block ??= new MaterialPropertyBlock();
            _renderer.GetPropertyBlock(_block);
            _block.SetColor("_BaseColor", color);
            _block.SetColor("_Color", color);
            _renderer.SetPropertyBlock(_block);
            if (_sprite != null) _sprite.color = color;
        }

        public void Place(BattleMap map, GridPos pos) => transform.position = StandPoint(map, pos);

        public void SetFacing(GridPos facing)
        {
            if (facing.X == 0 && facing.Y == 0) return;
            transform.rotation = Quaternion.LookRotation(new Vector3(facing.X, 0f, facing.Y));
        }

        /// <summary>Clareia a unidade e volta à cor base (feedback de dano).</summary>
        public IEnumerator Flash(Color flashColor, float seconds)
        {
            float duration = Mathf.Max(0.01f, seconds);
            for (float t = 0f; t < 1f; t += Time.deltaTime / duration)
            {
                Tint(Color.Lerp(flashColor, VisualBase, t));
                yield return null;
            }

            Tint(VisualBase);
        }

        /// <summary>Encolhe até sumir (derrota).</summary>
        public IEnumerator Vanish(float seconds)
        {
            float duration = Mathf.Max(0.01f, seconds);
            for (float t = 0f; t < 1f; t += Time.deltaTime / duration)
            {
                transform.localScale = _baseScale * (1f - t);
                yield return null;
            }

            transform.localScale = Vector3.zero;
        }

        public IEnumerator MoveAlong(BattleMap map, IReadOnlyList<GridPos> path)
        {
            float stepTime = GameSettings.Duration(StepTime);
            _moving = true;   // MVP 3B: Walk avança enquanto este trecho é interpolado
            _stepIndex = 0;   // fase do ciclo reinicia por ação (contínua DENTRO do caminho)
            try
            {
                foreach (GridPos next in path)
                {
                    Vector3 from = transform.position;
                    Vector3 to = StandPoint(map, next);
                    float hop = Mathf.Abs(to.y - from.y) * HopPerHeight / MapView.HeightUnit + 0.05f;

                    Vector3 flat = new Vector3(to.x - from.x, 0f, to.z - from.z);
                    if (flat != Vector3.zero) transform.rotation = Quaternion.LookRotation(flat);
                    AudioService.Play(SoundId.Step);

                    for (float t = 0f; t < 1f; t += Time.deltaTime / stepTime)
                    {
                        _stepT = t; // LateUpdate consome o mesmo t → sincronia sem relógio extra
                        Vector3 p = Vector3.Lerp(from, to, t);
                        p.y += Mathf.Sin(t * Mathf.PI) * hop;
                        transform.position = p;
                        yield return null;
                    }

                    _stepT = 0f;
                    _stepIndex++; // fase contínua: próximo passo usa a outra metade do ciclo
                    transform.position = to;
                }
            }
            finally
            {
                _moving = false; // volta ao Idle; roda também se a corotina for interrompida
                _stepT = 0f;
            }
        }

        static Vector3 StandPoint(BattleMap map, GridPos pos) =>
            MapView.TileTop(map, pos) + Vector3.up * BodyHalfHeight;
    }
}
