import math
import unittest

from ovos_number_parser.numbers_ru import pronounce_number_ru
from ovos_number_parser.numbers_de import pronounce_number_de

INF_WORD = "бесконечность"

# magnitudes above the largest named Russian scale, including exact Python ints
# (whose str() carries no "e") and values past the float ceiling
FINITE_SWEEP = [
    1e60, 1e93, 1e120, 1e123, 1e150, 1e200, 1e303, 1e306, 1.7e308,
    10 ** 120, 10 ** 200, 10 ** 306, 10 ** 320, 10 ** 400, 2 ** 1024, 10 ** 500,
]


class TestRussianLargeNumbers(unittest.TestCase):
    def test_finite_never_empty(self):
        for x in FINITE_SWEEP:
            self.assertTrue(pronounce_number_ru(x), f"empty for {x!r}")

    def test_finite_never_infinity(self):
        for x in FINITE_SWEEP:
            self.assertNotIn(INF_WORD, pronounce_number_ru(x),
                             f"false infinity for {x!r}")

    def test_actual_infinity_still_spoken(self):
        self.assertEqual(pronounce_number_ru(math.inf), INF_WORD)
        self.assertEqual(pronounce_number_ru(-math.inf), "минус " + INF_WORD)

    def test_small_numbers_unchanged(self):
        self.assertEqual(pronounce_number_ru(5), "пять")
        self.assertEqual(pronounce_number_ru(-3.5), "минус три точка пять")

    def test_rounds_not_truncates(self):
        self.assertEqual(pronounce_number_ru(3.14159, places=4),
                         "три точка один четыре один шесть")

    def test_rounding_carries_into_integer(self):
        self.assertEqual(pronounce_number_ru(0.999999, places=2), "один")

    def test_rounds_to_zero_has_no_minus(self):
        self.assertEqual(pronounce_number_ru(-0.004, places=2), "ноль")

    def test_other_backend_no_false_infinity(self):
        # a sibling backend that falls back to a raw digit string must also
        # never emit an infinity word for a finite value
        for x in [1e120, 1e200, 1e306]:
            r = pronounce_number_de(x)
            self.assertTrue(r)
            self.assertNotIn("unendlich", r)


if __name__ == "__main__":
    unittest.main()
