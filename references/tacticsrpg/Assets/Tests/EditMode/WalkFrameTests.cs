using NUnit.Framework;
using TacticsRPG.Presentation;

namespace TacticsRPG.Tests
{
    /// <summary>
    /// Congela o contrato de sincronia do Walk do MVP 3B (`HUMAN_WARRIOR_ANIMATIONS.md` §4):
    /// 6 quadros, 3 por passo, ciclo completo = 2 passos. A seleção depende só do passo
    /// cumulativo + `t` normalizado (a velocidade 1×/2×/4×/50× já está embutida no `t` pela
    /// `GameSettings.Duration` de MoveAlong — não é multiplicada de novo). Função pura —
    /// sem rendering Unity.
    /// </summary>
    [TestFixture]
    public class WalkFrameTests
    {
        const int FramesPerStep = 3;
        const int FrameCount = 6;

        [Test]
        public void FirstStep_UsesFirstHalf()
        {
            Assert.AreEqual(0, UnitView.WalkFrameIndex(0, 0.00f, FramesPerStep, FrameCount));
            Assert.AreEqual(1, UnitView.WalkFrameIndex(0, 0.50f, FramesPerStep, FrameCount));
            Assert.AreEqual(2, UnitView.WalkFrameIndex(0, 0.99f, FramesPerStep, FrameCount));
        }

        [Test]
        public void SecondStep_UsesSecondHalf()
        {
            Assert.AreEqual(3, UnitView.WalkFrameIndex(1, 0.00f, FramesPerStep, FrameCount));
            Assert.AreEqual(4, UnitView.WalkFrameIndex(1, 0.50f, FramesPerStep, FrameCount));
            Assert.AreEqual(5, UnitView.WalkFrameIndex(1, 0.99f, FramesPerStep, FrameCount));
        }

        [Test]
        public void ThirdStep_ReturnsToFirstHalf_CycleContinues()
        {
            Assert.AreEqual(0, UnitView.WalkFrameIndex(2, 0.10f, FramesPerStep, FrameCount));
            Assert.AreEqual(3, UnitView.WalkFrameIndex(3, 0.10f, FramesPerStep, FrameCount));
        }

        [Test]
        public void NormalizedT_Boundaries_StayInRange()
        {
            // t=1 exato clampa no último quadro do trecho (o próximo passo assume a sequência).
            Assert.AreEqual(2, UnitView.WalkFrameIndex(0, 1.00f, FramesPerStep, FrameCount));
            Assert.AreEqual(0, UnitView.WalkFrameIndex(0, 0.00f, FramesPerStep, FrameCount));
        }

        [Test]
        public void LongPath_NeverOutOfRange_ContinuousPhase()
        {
            for (int step = 0; step < 12; step++)
            for (int tTick = 0; tTick <= 10; tTick++)
            {
                float t = tTick / 10f;
                int idx = UnitView.WalkFrameIndex(step, t, FramesPerStep, FrameCount);
                Assert.That(idx, Is.InRange(0, FrameCount - 1), $"step={step} t={t}");
            }
        }

        [Test]
        public void Selection_IsDeterministic_SpeedIndependent()
        {
            // O `t` já chega normalizado pela GameSettings.Duration — a função não depende de
            // velocidade: mesmos (passo, t) produzem o mesmo quadro em qualquer velocidade.
            int a = UnitView.WalkFrameIndex(4, 0.35f, FramesPerStep, FrameCount);
            int b = UnitView.WalkFrameIndex(4, 0.35f, FramesPerStep, FrameCount);
            Assert.AreEqual(a, b);
            Assert.AreEqual(1, a); // passo 4 (par) → primeira metade: 12 % 6 = 0 + floor(1.05)=1 → 1
        }

        [Test]
        public void FreshMovement_StartsAtFrameZero_AndDegenerateInputsAreSafe()
        {
            Assert.AreEqual(0, UnitView.WalkFrameIndex(0, 0f, FramesPerStep, FrameCount)); // início limpo
            Assert.AreEqual(0, UnitView.WalkFrameIndex(3, 0.5f, 0, FrameCount));           // sem frames/passo
            Assert.AreEqual(0, UnitView.WalkFrameIndex(3, 0.5f, FramesPerStep, 0));        // sem clipe
        }
    }
}