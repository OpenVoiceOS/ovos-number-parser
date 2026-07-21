import unittest

from ovos_number_parser.numbers_it import (extract_number_it,
                                           pronounce_number_it)


class TestItalianScaleSpacing(unittest.TestCase):
    def test_scale_word_joins_the_whole_group(self):
        # the thousands scale word attaches to a single Italian word, so a
        # multi-token group must collapse first: 101000 is "centounomila",
        # never "cento unomila" (which reads back as 100 + 1000)
        self.assertEqual(pronounce_number_it(101000), "centounomila")
        self.assertEqual(pronounce_number_it(150000), "centocinquantamila")
        self.assertEqual(pronounce_number_it(999000), "novecentonovantanovemila")

    def test_hundred_thousands_roundtrip(self):
        for n in list(range(100000, 1000000, 337)) + [
                101000, 123456, 150000, 200000, 555555, 987654, 999999]:
            spoken = pronounce_number_it(n)
            self.assertEqual(extract_number_it(spoken), n,
                             f"roundtrip failed for {n} -> {spoken!r}")

    def test_negative_hundred_thousands_roundtrip(self):
        for n in [-101000, -123456, -150000, -999000]:
            spoken = pronounce_number_it(n)
            self.assertEqual(extract_number_it(spoken), n,
                             f"roundtrip failed for {n} -> {spoken!r}")

    def test_millions_still_roundtrip(self):
        for n in [1000000, 2500000, 101000000]:
            spoken = pronounce_number_it(n)
            self.assertEqual(extract_number_it(spoken), n,
                             f"roundtrip failed for {n} -> {spoken!r}")


if __name__ == "__main__":
    unittest.main()
