import unittest

from ovos_number_parser import extract_number

from ovos_number_parser.numbers_hr import pronounce_number_hr


class TestCroatianBareThousandAfterScale(unittest.TestCase):
    """A bare "tisuću" (one thousand) following a larger scale must open a new
    additive group, not multiply the larger scale by itself."""

    def test_million_plus_bare_thousand(self):
        self.assertEqual(
            extract_number("milijun tisuću sedamsto deset", lang="hr"), 1001710)
        self.assertEqual(extract_number("milijun tisuću", lang="hr"), 1001000)

    def test_regular_scale_composition_unchanged(self):
        self.assertEqual(extract_number("sto tisuća", lang="hr"), 100000)
        self.assertEqual(
            extract_number("dva milijuna tristo tisuća", lang="hr"), 2300000)

    def test_round_trip_million_boundary(self):
        for number in [1001710, 4001978, 7001935, -1001710, 1001000,
                       1000001, 1234567]:
            with self.subTest(number=number):
                spoken = pronounce_number_hr(number)
                self.assertEqual(extract_number(spoken, lang="hr"), number)


if __name__ == "__main__":
    unittest.main()
