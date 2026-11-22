import unittest

from ovos_number_parser import extract_number

from ovos_number_parser.numbers_tr import pronounce_number_tr


class TestTurkishHundredsAfterThousand(unittest.TestCase):
    def test_bare_hundred_after_thousand_adds(self):
        self.assertEqual(extract_number("bin yüz", lang="tr"), 1100)
        self.assertEqual(extract_number("bin yüz bir", lang="tr"), 1101)
        self.assertEqual(extract_number("iki bin yüz", lang="tr"), 2100)

    def test_multiplier_uses_unchanged(self):
        self.assertEqual(extract_number("iki yüz", lang="tr"), 200)
        self.assertEqual(extract_number("yüz bin", lang="tr"), 100000)
        self.assertEqual(extract_number("bin iki yüz", lang="tr"), 1200)
        self.assertEqual(extract_number("yüz", lang="tr"), 100)

    def test_natural_sentence(self):
        self.assertEqual(
            extract_number("bana bin yüz tane lazım", lang="tr"), 1100)

    def test_roundtrip_to_one_million(self):
        bad = []
        for n in list(range(0, 5000)) + list(range(5000, 1000001, 997)):
            if extract_number(pronounce_number_tr(n), lang="tr") != n:
                bad.append(n)
        self.assertEqual(bad, [], f"round-trip failures: {bad[:10]}")


if __name__ == "__main__":
    unittest.main()
