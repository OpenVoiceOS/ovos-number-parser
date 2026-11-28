import unittest

from ovos_number_parser import extract_number

from ovos_number_parser.numbers_bg import pronounce_number_bg


class TestNegativeCompoundbg(unittest.TestCase):
    def test_negative_compound_roundtrip(self):
        for n in (-9, -21, -200, -1200, -1234, -999999, -1000000):
            self.assertEqual(
                extract_number(pronounce_number_bg(n), lang="bg"), n)


if __name__ == "__main__":
    unittest.main()
