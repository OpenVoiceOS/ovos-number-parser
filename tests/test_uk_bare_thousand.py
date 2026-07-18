import unittest

from ovos_number_parser.numbers_uk import (extract_number_uk,
                                           pronounce_number_uk)


class TestUkrainianBareThousandAfterScale(unittest.TestCase):
    """A bare "тисяча" (one thousand) following a larger scale must open a new
    additive group, not multiply the larger scale by itself."""

    def test_million_plus_bare_thousand(self):
        self.assertEqual(
            extract_number_uk("мільйон тисяча сімсот десять"), 1001710)
        self.assertEqual(extract_number_uk("мільйон тисяча"), 1001000)

    def test_regular_scale_composition_unchanged(self):
        self.assertEqual(extract_number_uk("сто тисяч"), 100000)
        self.assertEqual(
            extract_number_uk("два мільйони триста тисяч"), 2300000)

    def test_round_trip_million_boundary(self):
        for number in [1001710, 4001978, 7001935, -1001710, 1001000,
                       1000001, 1234567]:
            with self.subTest(number=number):
                spoken = pronounce_number_uk(number)
                self.assertEqual(extract_number_uk(spoken), number)


if __name__ == "__main__":
    unittest.main()
