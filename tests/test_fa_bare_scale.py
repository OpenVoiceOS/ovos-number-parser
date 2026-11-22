import unittest

from ovos_number_parser.numbers_fa import pronounce_number_fa
from ovos_number_parser import extract_number


class TestFarsiBareScale(unittest.TestCase):
    """A bare scale word ("... و هزار") means one of that scale and must be
    added, not dropped."""

    def test_million_plus_bare_thousand(self):
        self.assertEqual(
            extract_number("یک میلیون و هزار و هفتصد و ده", lang="fa"), 1001710)
        self.assertEqual(extract_number("هزار", lang="fa"), 1000)

    def test_regular_composition_unchanged(self):
        self.assertEqual(extract_number("دو هزار", lang="fa"), 2000)
        self.assertEqual(extract_number("سیصد هزار", lang="fa"), 300000)

    def test_round_trip_million_boundary(self):
        for number in [1001710, 4001978, 7001935, -1001710, 1001000,
                       1000001, 1234567, 1000000000000]:
            with self.subTest(number=number):
                spoken = pronounce_number_fa(number)
                self.assertEqual(extract_number(spoken, lang="fa"), number)


if __name__ == "__main__":
    unittest.main()
