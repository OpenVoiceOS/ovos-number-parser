import unittest

from ovos_number_parser.numbers_sv import (extract_number_sv,
                                           pronounce_number_sv)


class TestSwedishBareThousandAfterScale(unittest.TestCase):
    """A bare "ettusen" (one thousand) following a larger scale must be added,
    not collapsed into the preceding scale as a stray one."""

    def test_million_plus_bare_thousand(self):
        self.assertEqual(
            extract_number_sv("en miljon ettusen sjuhundratio"), 1001710)
        self.assertEqual(
            extract_number_sv("sexmiljoner ettusen tvåhundraåttiofem"),
            6001285)

    def test_regular_composition_unchanged(self):
        self.assertEqual(extract_number_sv("ettusen"), 1000)
        self.assertEqual(extract_number_sv("tjugoettusen"), 21000)
        self.assertEqual(extract_number_sv("tvåtusen tjugotre"), 2023)

    def test_round_trip_million_boundary(self):
        for number in [1001710, 4001978, 7001935, -1001710, 1001000,
                       1000001, 1234567]:
            with self.subTest(number=number):
                spoken = pronounce_number_sv(number)
                self.assertEqual(extract_number_sv(spoken), number)


if __name__ == "__main__":
    unittest.main()
