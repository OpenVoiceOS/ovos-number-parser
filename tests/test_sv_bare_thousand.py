import unittest

from ovos_number_parser.numbers_sv import pronounce_number_sv
from ovos_number_parser import extract_number


class TestSwedishBareThousandAfterScale(unittest.TestCase):
    """A bare "ettusen" (one thousand) following a larger scale must be added,
    not collapsed into the preceding scale as a stray one."""

    def test_million_plus_bare_thousand(self):
        self.assertEqual(
            extract_number("en miljon ettusen sjuhundratio", lang="sv"), 1001710)
        self.assertEqual(
            extract_number("sexmiljoner ettusen tvåhundraåttiofem", lang="sv"),
            6001285)

    def test_regular_composition_unchanged(self):
        self.assertEqual(extract_number("ettusen", lang="sv"), 1000)
        self.assertEqual(extract_number("tjugoettusen", lang="sv"), 21000)
        self.assertEqual(extract_number("tvåtusen tjugotre", lang="sv"), 2023)

    def test_round_trip_million_boundary(self):
        for number in [1001710, 4001978, 7001935, -1001710, 1001000,
                       1000001, 1234567]:
            with self.subTest(number=number):
                spoken = pronounce_number_sv(number)
                self.assertEqual(extract_number(spoken, lang="sv"), number)


if __name__ == "__main__":
    unittest.main()
