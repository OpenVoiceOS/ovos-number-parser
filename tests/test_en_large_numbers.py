import math
import unittest

from ovos_number_parser.numbers_en import (
    pronounce_number_en,
    extract_number_en,
)

# magnitudes spanning the named short-scale range and beyond, including exact
# Python ints (whose str() carries no "e") and values past the float ceiling
FINITE_SWEEP = [
    1e33, 1e66, 1e100, 1e120, 1e123, 1e126, 1e150, 1e200, 1e303, 1e306,
    1.7e308, 10 ** 123, 10 ** 126, 10 ** 150, 10 ** 200, 10 ** 306, 10 ** 320,
    10 ** 500,
]


class TestEnglishLargeNumbers(unittest.TestCase):
    def test_finite_never_empty(self):
        for x in FINITE_SWEEP:
            self.assertTrue(pronounce_number_en(x), f"empty for {x!r}")

    def test_finite_never_infinity(self):
        for x in FINITE_SWEEP:
            self.assertNotIn("infinity", pronounce_number_en(x),
                             f"false infinity for {x!r}")

    def test_named_scale_gap_filled(self):
        # values inside the former table gap now get their canonical name
        self.assertEqual(pronounce_number_en(1e126), "one unquadragintillion")
        self.assertEqual(pronounce_number_en(1e150),
                         "one novenquadragintillion")
        self.assertEqual(pronounce_number_en(1e303), "one centillion")

    def test_actual_infinity_still_spoken(self):
        self.assertEqual(pronounce_number_en(math.inf), "infinity")
        self.assertEqual(pronounce_number_en(-math.inf), "negative infinity")

    def test_roundtrip_named_values(self):
        for x in [1e123, 1e126, 1e150, 1e153, 1e300, 1e303, 1e306]:
            name = pronounce_number_en(x)
            self.assertEqual(extract_number_en(name), x, name)

    def test_googol(self):
        self.assertEqual(extract_number_en("one googol"), 1e100)
        self.assertEqual(extract_number_en("googol"), 1e100)
        self.assertEqual(extract_number_en("two googol"), 2e100)
        # googolplex overflows a float and is not fabricated
        self.assertFalse(extract_number_en("googolplex"))


if __name__ == "__main__":
    unittest.main()
