using NUnit.Framework;
using TacticsRPG.Presentation;

namespace TacticsRPG.Tests
{
    /// <summary>
    /// Congela a tabela verificada do MVP 2: índice de vista direcional (back_l=0, back_r=1,
    /// front_r=2, front_l=3) para as 16 combinações de facing de mundo (0/90/180/270) ×
    /// yaw da câmera (45/135/225/315). Derivado de: sen(d)>0 → direita da tela;
    /// −cos(d)>0 → frente (para a câmera), com d = (θu − θc) mod 360 — ver
    /// `Docs/Art/Characters/HUMAN_WARRIOR_DIRECTIONS.md` §2. Sem Unity rendering: só a
    /// função pura `UnitView.DirectionIndex`.
    /// </summary>
    [TestFixture]
    public class DirectionMappingTests
    {
        // Linha = facing de mundo (θu), coluna = yaw da câmera (θc) em {45, 135, 225, 315}.
        static readonly int[,] Expected =
        {
            // 45   135  225  315
            { 0,   3,   2,   1 }, // θu =   0 (0,1)
            { 1,   0,   3,   2 }, // θu =  90 (1,0)
            { 2,   1,   0,   3 }, // θu = 180 (0,-1)
            { 3,   2,   1,   0 }, // θu = 270 (-1,0)
        };

        [Test]
        public void AllFacingTimesCameraRotations_MatchVerifiedTable()
        {
            for (int facing = 0; facing < 4; facing++)
            for (int cam = 0; cam < 4; cam++)
            {
                float unitYaw = facing * 90f;
                float cameraYaw = 45f + cam * 90f;
                int idx = UnitView.DirectionIndex(unitYaw, cameraYaw);
                Assert.AreEqual(Expected[facing, cam], idx,
                    $"θu={unitYaw}° θc={cameraYaw}°: esperado índice {Expected[facing, cam]}, obtido {idx}");
            }
        }

        [Test]
        public void Index_IsStableAtExactDiagonals_AndSwapsOncePerQuarter()
        {
            // Exatamente nas diagonais de repouso (d = 45/135/225/315) o resultado é inteiro exato
            // (RoundToInt não arredonda nada) — sem oscilar e sem o risco do arredondamento
            // bancário do RoundToInt(0.5), que trocaria back_r↔back_l.
            Assert.AreEqual(1, UnitView.DirectionIndex(90f, 45f));   // d=45  → back_r
            Assert.AreEqual(2, UnitView.DirectionIndex(180f, 45f));  // d=135 → front_r
            Assert.AreEqual(3, UnitView.DirectionIndex(270f, 45f));  // d=225 → front_l
            Assert.AreEqual(0, UnitView.DirectionIndex(0f, 45f));    // d=315 → back_l
        }

        [Test]
        public void Index_DerivesFromRealYaw_SurvivesFreeCamera()
        {
            // Yaw contínuo (câmera girando): escolhe a VISTA DIAGONAL mais próxima (limites nos
            // cardinais) — nunca salta 90° para o lado oposto perto de uma diagonal de repouso.
            Assert.AreEqual(2, UnitView.DirectionIndex(180f, 60f));  // d=120 → mais perto de 135 (front_r)
            Assert.AreEqual(1, UnitView.DirectionIndex(180f, 100f)); // d=80  → mais perto de 45  (back_r)
            Assert.AreEqual(1, UnitView.DirectionIndex(180f, 115f)); // d=65  → mais perto de 45  (back_r)
            Assert.AreEqual(1, UnitView.DirectionIndex(135f, 45f));  // d=90 (limite) → vizinho equidistante
        }

        [Test]
        public void Index_WrapsNegativeAngles()
        {
            // Yaws negativos/>360 normalizam pelo Repeat antes do piso.
            Assert.AreEqual(UnitView.DirectionIndex(90f, 45f), UnitView.DirectionIndex(-270f, -315f));
            Assert.AreEqual(UnitView.DirectionIndex(90f, 45f), UnitView.DirectionIndex(450f, 405f));
        }
    }
}