"""Hand-verified ordinal anchors for the newly supported languages."""
import unittest

from ovos_number_parser import is_fractional, pronounce_ordinal


class TestPronounceOrdinalAnchors(unittest.TestCase):
    """Hand-verified ordinals for the newly wired languages."""
    ANCHORS = {
        "cs": [(1, "první"), (2, "druhý"), (21, "dvacátý první"),
               (45, "čtyřicátý pátý"), (100, "stý"), (200, "dvoustý"),
               (1000, "tisící")],
        "pl": [(1, "pierwszy"), (2, "drugi"), (21, "dwudziesty pierwszy"),
               (45, "czterdziesty piąty"), (100, "setny"), (200, "dwusetny"),
               (1000, "tysięczny")],
        "uk": [(1, "перший"), (2, "другий"), (21, "двадцять перший"),
               (100, "сотий"), (200, "двохсотий"), (1000, "тисячний")],
        "eu": [(1, "lehenengo"), (2, "bigarren"), (3, "hirugarren"),
               (4, "laugarren"), (5, "bosgarren"), (10, "hamargarren"),
               (20, "hogeigarren")],
        "fa": [(1, "اول"), (2, "دوم"), (3, "سوم"), (5, "پنجم"),
               (10, "دهم"), (20, "بیستم")],
        "sl": [(1, "prvi"), (2, "drugi"), (3, "tretji"), (10, "deseti"),
               (21, "enaindvajseti"), (100, "stoti")],
        "gl": [(1, "primeiro"), (2, "segundo"), (3, "terceiro")],
    }

    def test_anchors(self):
        for lang, pairs in self.ANCHORS.items():
            for n, expected in pairs:
                self.assertEqual(pronounce_ordinal(n, lang), expected,
                                 f"{lang} {n}")

    def test_invalid_ordinals_raise(self):
        # basque forms a zeroth ordinal (zerogarren) rather than rejecting it
        for lang in ("cs", "pl", "uk", "fa"):
            with self.assertRaises(ValueError, msg=lang):
                pronounce_ordinal(0, lang)


class TestFarsiFractions(unittest.TestCase):
    def test_is_fractional(self):
        self.assertEqual(is_fractional("نیم", "fa"), 0.5)
        self.assertAlmostEqual(is_fractional("سوم", "fa"), 1 / 3)
        self.assertFalse(is_fractional("خانه", "fa"))


if __name__ == "__main__":
    unittest.main()
