import unittest

from ovos_number_parser.numbers_es import (pronounce_number_es,
                                           extract_number_es)


class TestSpanishCienPronounce(unittest.TestCase):
    def test_exact_hundred_is_cien(self):
        # 100 is "cien"; "ciento" only precedes a remainder
        self.assertEqual(pronounce_number_es(100), "cien")
        self.assertEqual(pronounce_number_es(101), "ciento uno")
        self.assertEqual(pronounce_number_es(150), "ciento cincuenta")
        self.assertEqual(pronounce_number_es(1100), "mil cien")
        self.assertEqual(pronounce_number_es(100000), "cien mil")

    def test_roundtrip_up_to_100000(self):
        bad = []
        for n in list(range(0, 3000)) + list(range(3000, 100001, 331)):
            if extract_number_es(pronounce_number_es(n)) != n:
                bad.append(n)
        self.assertEqual(bad, [], f"round-trip failures: {bad[:10]}")


if __name__ == "__main__":
    unittest.main()
