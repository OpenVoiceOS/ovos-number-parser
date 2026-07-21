import unittest

from ovos_number_parser.numbers_tr import (extract_number_tr,
                                           pronounce_number_tr)


class TestTurkishHundredsAfterThousand(unittest.TestCase):
    def test_bare_hundred_after_thousand_adds(self):
        self.assertEqual(extract_number_tr("bin yüz"), 1100)
        self.assertEqual(extract_number_tr("bin yüz bir"), 1101)
        self.assertEqual(extract_number_tr("iki bin yüz"), 2100)

    def test_multiplier_uses_unchanged(self):
        self.assertEqual(extract_number_tr("iki yüz"), 200)
        self.assertEqual(extract_number_tr("yüz bin"), 100000)
        self.assertEqual(extract_number_tr("bin iki yüz"), 1200)
        self.assertEqual(extract_number_tr("yüz"), 100)

    def test_natural_sentence(self):
        self.assertEqual(
            extract_number_tr("bana bin yüz tane lazım"), 1100)

    def test_roundtrip_to_one_million(self):
        bad = []
        for n in list(range(0, 5000)) + list(range(5000, 1000001, 997)):
            if extract_number_tr(pronounce_number_tr(n)) != n:
                bad.append(n)
        self.assertEqual(bad, [], f"round-trip failures: {bad[:10]}")


if __name__ == "__main__":
    unittest.main()
