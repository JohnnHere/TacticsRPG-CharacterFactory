using NUnit.Framework;
using TacticsRPG.Presentation;

namespace TacticsRPG.Tests
{
    /// <summary>
    /// Congela o contrato de timing do Idle do MVP 3 (`HUMAN_WARRIOR_ANIMATIONS.md` §4):
    /// 4 quadros a 0,24 s = ciclo de 0,96 s @1×, distribuição uniforme, loop e guardas.
    /// Função pura — sem rendering Unity.
    /// </summary>
    [TestFixture]
    public class IdleFrameTests
    {
        const float SecondsPerFrame = 0.24f;

        [Test]
        public void FourFrames_UniformDistribution_AndLoop()
        {
            Assert.AreEqual(0, UnitView.IdleFrameIndex(0.00f, 4, SecondsPerFrame));
            Assert.AreEqual(0, UnitView.IdleFrameIndex(0.23f, 4, SecondsPerFrame));
            Assert.AreEqual(1, UnitView.IdleFrameIndex(0.24f, 4, SecondsPerFrame));
            Assert.AreEqual(3, UnitView.IdleFrameIndex(0.95f, 4, SecondsPerFrame));
            Assert.AreEqual(0, UnitView.IdleFrameIndex(0.96f, 4, SecondsPerFrame)); // volta ao início
            Assert.AreEqual(1, UnitView.IdleFrameIndex(1.30f, 4, SecondsPerFrame)); // 1,25 ciclos → quadro 1
        }

        [Test]
        public void Guards_DegenerateInputs()
        {
            Assert.AreEqual(0, UnitView.IdleFrameIndex(10f, 0, SecondsPerFrame)); // sem quadros
            Assert.AreEqual(0, UnitView.IdleFrameIndex(10f, 4, 0f));              // sem tempo por quadro
        }
    }
}