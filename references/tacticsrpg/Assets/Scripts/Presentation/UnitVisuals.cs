using System.Collections.Generic;
using TacticsRPG.Core;
using UnityEngine;

namespace TacticsRPG.Presentation
{
    /// <summary>
    /// MVP 1 (Estágio 10.2b): amarração unidade → sprite. Hoje apenas o Hero de teste do sandbox
    /// (time do jogador, unidade-chave, nome "Hero" no MapData — ex.: mapa Proving) recebe o sprite
    /// do Human Warrior Pilot. Nenhuma outra unidade é afetada.
    /// MVP 2: conjunto direcional (4 diagonais de tela) carregado uma única vez e cacheado;
    /// vista ausente cai no sprite estático do MVP 1 (fallback em cascata, sem espelhamento).
    /// MVP 3A: quadros de Idle por direção (hoje só front_r), mesmo esquema de cache/fallback;
    /// vista sem clipe continua no estático do MVP 2.
    /// MVP 3B: quadros de Walk por direção (hoje só front_r), tocados durante o MoveAlong real.
    /// MVP 4: clipes de combate por direção — Attack (um shot), Hit (um shot no alvo) e Defeat
    /// (trava até a view sumir) — mesmo esquema de cache/fallback/re-sondagem.
    /// Extensões futuras: demais vistas se surgirem; sem Animator.
    /// </summary>
    public static class UnitVisuals
    {
        const string WarriorPilotBase = "Characters/WarriorPilot/";
        const string WarriorPilotSprite = WarriorPilotBase + "warrior_pilot_mvp1_static_128";

        // Escala visual do piloto (MVP 1): +15% sobre o tamanho nativo para leitura em campo.
        // Proporções originais preservadas; apenas Presentation (perfil visual do personagem).
        const float WarriorPilotScale = 1.15f;

        // Índices do conjunto direcional (rótulos de TELA; ver HUMAN_WARRIOR_DIRECTIONS.md §2):
        // d = (yawUnidade − yawCâmera) mod 360; índice = RoundToInt((d + 45)/90) mod 4.
        public const int BackLeft = 0, BackRight = 1, FrontRight = 2, FrontLeft = 3;

        // Sondagem de quadros por clipe: 00..15 (contrato do MVP 3, HUMAN_WARRIOR_ANIMATIONS.md §3).
        const int MaxFramesPerClip = 16;

        static Sprite[] _warriorDirections;
        static bool _warriorDirectionsLoaded;
        static Sprite[][] _idleByDirection;
        static bool _idleLoaded;
        static Sprite[][] _walkByDirection;
        static bool _walkLoaded;
        static Sprite[][] _attackByDirection;
        static bool _attackLoaded;
        static Sprite[][] _hitByDirection;
        static bool _hitLoaded;
        static Sprite[][] _defeatByDirection;
        static bool _defeatLoaded;

        /// <summary>Sprite opcional da unidade; null mantém o boneco procedural (cápsula).</summary>
        public static Sprite SpriteFor(Unit unit) =>
            IsWarriorPilot(unit) ? Resources.Load<Sprite>(WarriorPilotSprite) : null;

        /// <summary>Multiplicador de escala visual da unidade (1 = tamanho nativo do sprite).</summary>
        public static float ScaleFor(Unit unit) => IsWarriorPilot(unit) ? WarriorPilotScale : 1f;

        /// <summary>
        /// Conjunto direcional cacheado [BackLeft, BackRight, FrontRight, FrontLeft] — entradas
        /// podem ser nulas (queda no estático por vista). null se a unidade não tem conjunto
        /// ou se nenhum sprite direcional carregou. Carrega uma única vez.
        /// </summary>
        public static Sprite[] DirectionsFor(Unit unit)
        {
            if (!IsWarriorPilot(unit)) return null;
            if (!_warriorDirectionsLoaded)
            {
                _warriorDirectionsLoaded = true;
                _warriorDirections = new[]
                {
                    Resources.Load<Sprite>(WarriorPilotBase + "Directions/warrior_pilot_dir_back_l"),
                    Resources.Load<Sprite>(WarriorPilotBase + "Directions/warrior_pilot_dir_back_r"),
                    Resources.Load<Sprite>(WarriorPilotBase + "Directions/warrior_pilot_dir_front_r"),
                    Resources.Load<Sprite>(WarriorPilotBase + "Directions/warrior_pilot_dir_front_l"),
                };
            }

            for (int i = 0; i < _warriorDirections.Length; i++)
                if (_warriorDirections[i] != null) return _warriorDirections;
            return null;
        }

        /// <summary>
        /// MVP 3A: quadros de Idle por índice de direção (mesma ordem de DirectionsFor);
        /// entradas null = vista sem clipe (cai no estático do MVP 2). Sonda índices 00..15 por
        /// vista; re-sonda (uma vez por construção de batalha) enquanto houver direção sem clipe.
        /// null se a unidade não tem clipes ou nada carregou.
        /// </summary>
        public static Sprite[][] IdleFramesFor(Unit unit)
        {
            if (!IsWarriorPilot(unit)) return null;
            _idleByDirection = LoadClipByDirection("Idle", "idle", ref _idleLoaded, ref _idleByDirection);
            return AnyClip(_idleByDirection) ? _idleByDirection : null;
        }

        /// <summary>
        /// MVP 3B: quadros de Walk por índice de direção (mesmas convenções de IdleFramesFor;
        /// hoje só front_r). Tocado durante o MoveAlong real; vista sem clipe → estático MVP 2.
        /// </summary>
        public static Sprite[][] WalkFramesFor(Unit unit)
        {
            if (!IsWarriorPilot(unit)) return null;
            _walkByDirection = LoadClipByDirection("Walk", "walk", ref _walkLoaded, ref _walkByDirection);
            return AnyClip(_walkByDirection) ? _walkByDirection : null;
        }

        /// <summary>MVP 4: quadros de Attack por direção (um shot no atacante).</summary>
        public static Sprite[][] AttackFramesFor(Unit unit)
        {
            if (!IsWarriorPilot(unit)) return null;
            _attackByDirection = LoadClipByDirection("Attack", "attack", ref _attackLoaded, ref _attackByDirection);
            return AnyClip(_attackByDirection) ? _attackByDirection : null;
        }

        /// <summary>MVP 4: quadros de Hit por direção (um shot no alvo quando o golpe ACERTA).</summary>
        public static Sprite[][] HitFramesFor(Unit unit)
        {
            if (!IsWarriorPilot(unit)) return null;
            _hitByDirection = LoadClipByDirection("Hit", "hit", ref _hitLoaded, ref _hitByDirection);
            return AnyClip(_hitByDirection) ? _hitByDirection : null;
        }

        /// <summary>MVP 4: quadros de Defeat por direção (trava até a view ser destruída).</summary>
        public static Sprite[][] DefeatFramesFor(Unit unit)
        {
            if (!IsWarriorPilot(unit)) return null;
            _defeatByDirection = LoadClipByDirection("Defeat", "defeat", ref _defeatLoaded, ref _defeatByDirection);
            return AnyClip(_defeatByDirection) ? _defeatByDirection : null;
        }

        // Sonda <pasta>/<prefixo>_<vista>_<00..MaxFramesPerClip> por direção e devolve a tabela
        // cacheada (só strings/arquivos na carga, nunca no playback).
        //
        // Ciclo de vida do cache: com Enter Play Mode configurado para NÃO recarregar o domínio,
        // campos estáticos sobrevivem entre sessões de play — uma sondagem anterior à importação
        // dos assets gravaria vazio para sempre. Por isso a tabela é re-sondada enquanto houver
        // direção sem clipe (uma vez por CreateViews; custo ínfimo: Resources.Load nulo por
        // direção faltante). Tabelas completas são sonda únicas, como antes.
        static Sprite[][] LoadClipByDirection(string folder, string prefix, ref bool loaded, ref Sprite[][] cache)
        {
            bool complete = cache != null;
            for (int dir = 0; complete && dir < 4; dir++)
                complete = cache[dir] != null;

            if (loaded && complete) return cache;

            loaded = true;
            cache = new Sprite[4][];
            for (int dir = 0; dir < 4; dir++)
            {
                var frames = new List<Sprite>(6);
                for (int i = 0; i < MaxFramesPerClip; i++)
                {
                    Sprite frame = Resources.Load<Sprite>(
                        $"{WarriorPilotBase}Animations/{folder}/{prefix}_{UnitView.DirectionNames[dir]}_{i:00}");
                    if (frame == null) break;
                    frames.Add(frame);
                }
                if (frames.Count > 0) cache[dir] = frames.ToArray();
            }
            return cache;
        }

        static bool AnyClip(Sprite[][] table)
        {
            for (int dir = 0; dir < table.Length; dir++)
                if (table[dir] != null) return true;
            return false;
        }

        static bool IsWarriorPilot(Unit unit) =>
            unit != null && unit.Team == BattleObjectives.DefaultPlayerTeam && unit.IsKey && unit.Name == "Hero";
    }
}
