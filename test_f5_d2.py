"""
SOEN 6011 - Deliverable 2 - Validation tests for f(x) = a * b^x.

Run:  python3 -m unittest test_f5_d2 -v
"""
import math
import random
import unittest

from f5_mathcore import (power_abx, _abs, _floor_to_int, _round_to_int, _int_pow2)
from f5_exceptions import DomainError, OverflowGuard


class TestPrimitives(unittest.TestCase):
    def test_abs(self):
        self.assertEqual(_abs(-3.5), 3.5)
        self.assertEqual(_abs(4.0), 4.0)

    def test_floor(self):
        for v in [-3.9, -1.0, -0.1, 0.0, 0.1, 2.9, 5.0, 7.7]:
            self.assertEqual(_floor_to_int(v), math.floor(v))

    def test_round(self):
        for v in [-2.6, -2.4, -0.5, 0.5, 1.4, 1.5, 2.5, 9.49, 9.5]:
            self.assertEqual(_round_to_int(v), math.floor(v + 0.5))

    def test_pow2(self):
        for n in range(-20, 21):
            self.assertTrue(abs(_int_pow2(n) - 2.0 ** n) <= abs(2.0 ** n) * 1e-15 + 1e-300)


class TestAccuracy(unittest.TestCase):
    def test_random_30k(self):
        random.seed(11)
        worst = 0.0
        for _ in range(30000):
            a = random.uniform(-1000, 1000)
            b = math.exp(random.uniform(-5, 5))
            x = random.uniform(-40, 40)
            t = x * math.log(b)
            if t > 700 or t < -700 or a == 0:
                continue
            ref = a * math.exp(t)
            if not math.isfinite(ref):
                continue
            worst = max(worst, abs(power_abx(a, b, x) - ref) / (abs(ref) + 1e-300))
        self.assertLess(worst, 1e-12)

    def test_spot(self):
        cases = [(3, 2, 4, 48.0), (100, 0.5, 3, 12.5), (1, 2, 10, 1024.0),
                 (7, 1, 99, 7.0), (4, 9, 0, 4.0), (-3, 2, 3, -24.0),
                 (0, 5, 7, 0.0), (1, math.e, 1, math.e)]
        for a, b, x, expected in cases:
            self.assertTrue(math.isclose(power_abx(a, b, x), expected,
                                         rel_tol=1e-12, abs_tol=1e-12))


class TestGuards(unittest.TestCase):
    def test_negative_base(self):
        with self.assertRaises(DomainError):
            power_abx(1, -2, 0.5)

    def test_zero_base(self):
        with self.assertRaises(DomainError):
            power_abx(1, 0, 2)

    def test_overflow_in_exp(self):
        with self.assertRaises(OverflowGuard):
            power_abx(1, 10, 1000)

    def test_overflow_in_multiply(self):
        with self.assertRaises(OverflowGuard):
            power_abx(1e300, 2, 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
