import math
import unittest

from integrate import integrate


class TestIntegrate(unittest.TestCase):
    def test_known_integral_sin(self) -> None:
        """Проверка интеграла sin(x) на [0, pi] ≈ 2."""
        result = integrate(math.sin, 0.0, math.pi, n_iter=200_000)
        self.assertAlmostEqual(result, 2.0, places=3)

    def test_stability_wrt_n_iter(self) -> None:
        """
        Проверка устойчивости к изменению числа итераций:
        результат при большем n_iter должен быть близок к результату
        при меньшем n_iter.
        """
        f = lambda x: x**2
        res_coarse = integrate(f, 0.0, 1.0, n_iter=1_000)
        res_fine = integrate(f, 0.0, 1.0, n_iter=100_000)
        self.assertAlmostEqual(res_coarse, res_fine, places=2)


if __name__ == "__main__":
    unittest.main()