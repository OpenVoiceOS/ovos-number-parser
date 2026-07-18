import unittest

from ovos_number_parser import (extract_number, pronounce_number, is_fractional,
                                pronounce_ordinal)
from ovos_number_parser.util import Scale, GrammaticalGender


class TestCatalanOrdinals(unittest.TestCase):
    """Catalan ordinals verified against the Institut d'Estudis Catalans normativa.

    Source: Consorci per a la Normalització Lingüística, "Els numerals ordinals"
    (reproducing the IEC normativa) and the Optimot fitxa "Guionet en els
    numerals compostos". The masculine ordinal is the cardinal + "-è" and the
    feminine the cardinal + "-na"; only the final element of a compound carries
    the ordinal ending, so a tens-units compound keeps a cardinal tens word
    ("vint-i-unè", not "vintè primer").
    """

    # (number, masculine, feminine)
    IEC_ANCHORS = [
        (1, "primer", "primera"),
        (2, "segon", "segona"),
        (3, "tercer", "tercera"),
        (4, "quart", "quarta"),
        (5, "cinquè", "cinquena"),
        (8, "vuitè", "vuitena"),
        (10, "desè", "desena"),
        # teens each own their own word, never desè + unit
        (11, "onzè", "onzena"),
        (12, "dotzè", "dotzena"),
        (13, "tretzè", "tretzena"),
        (16, "setzè", "setzena"),
        (17, "dissetè", "dissetena"),
        (19, "dinovè", "dinovena"),
        # round tens
        (20, "vintè", "vintena"),
        (30, "trentè", "trentena"),
        (40, "quarantè", "quarantena"),
        (90, "norantè", "norantena"),
        # twenties keep the fused "-i-"; the unit takes the -è/-na form
        (21, "vint-i-unè", "vint-i-unena"),
        (22, "vint-i-dosè", "vint-i-dosena"),
        (23, "vint-i-tresè", "vint-i-tresena"),
        (24, "vint-i-quatrè", "vint-i-quatrena"),
        (29, "vint-i-novè", "vint-i-novena"),
        # thirties onward join with a plain hyphen
        (31, "trenta-unè", "trenta-unena"),
        (42, "quaranta-dosè", "quaranta-dosena"),
        (54, "cinquanta-quatrè", "cinquanta-quatrena"),
        # hundreds: round hundreds take the ending, compounds stay cardinal
        (100, "centè", "centena"),
        (200, "dos-centè", "dos-centena"),
        (300, "tres-centè", "tres-centena"),
        (121, "cent vint-i-unè", "cent vint-i-unena"),
        (353, "tres-cents cinquanta-tresè", "tres-cents cinquanta-tresena"),
        # thousands
        (1000, "milè", "milena"),
        (2000, "dos milè", "dos milena"),
    ]

    def test_masculine_and_feminine(self):
        for n, masc, fem in self.IEC_ANCHORS:
            with self.subTest(number=n, gender="m"):
                self.assertEqual(pronounce_ordinal(n, lang="ca"), masc)
            with self.subTest(number=n, gender="f"):
                self.assertEqual(
                    pronounce_ordinal(n, lang="ca",
                                      gender=GrammaticalGender.FEMININE), fem)

    def test_skill_path_pronounce_number_ordinals(self):
        # ovos-skill-count reaches ordinals through pronounce_number(ordinals=True)
        for n, masc, _ in self.IEC_ANCHORS:
            with self.subTest(number=n):
                self.assertEqual(
                    pronounce_number(n, lang="ca", ordinals=True), masc)

    def test_compound_is_not_naive_tens_plus_unit(self):
        # regression guard: the shared engine used to emit "desè primer" (11)
        # and "vintè primer" (21) by concatenating tens and unit ordinals
        for n in (11, 12, 13, 21, 22, 31):
            spoken = pronounce_ordinal(n, lang="ca")
            self.assertNotIn(" primer", spoken)
            self.assertNotIn("desè ", spoken)
            self.assertNotIn("vintè ", spoken)

    def test_ordinals_round_trip_through_is_fractional(self):
        # the -è ordinal words double as the fraction denominators
        for word, value in (("onzè", 1 / 11), ("dotzè", 1 / 12),
                            ("vintè", 1 / 20), ("centè", 1 / 100)):
            self.assertAlmostEqual(is_fractional(word, lang="ca"), value)


class TestCatalanPronounce(unittest.TestCase):
    """Anchors for spoken Catalan numbers."""

    def test_pronounce_number(self):
        expected = {0: 'zero', 1: 'un', 2: 'dos', 3: 'tres', 4: 'quatre', 5: 'cinc', 6: 'sis', 7: 'set', 8: 'vuit', 9: 'nou', 10: 'deu', 11: 'onze', 12: 'dotze', 13: 'tretze', 14: 'catorze', 15: 'quinze', 16: 'setze', 17: 'disset', 18: 'divuit', 19: 'dinou', 20: 'vint', 21: 'vint-i-un', 30: 'trenta', 42: 'quaranta-dos', 50: 'cinquanta', 66: 'seixanta-sis', 70: 'setanta', 80: 'vuitanta', 90: 'noranta', 99: 'noranta-nou', 100: 'cent', 101: 'cent un', 123: 'cent vint-i-tres', 200: 'dos-cents', 500: 'cinc-cents', 999: 'nou-cents noranta-nou', 1000: 'mil', 2000: 'dos mil', 2023: 'dos mil vint-i-tres', 1000000: 'un milió', 2000000: 'dos milions'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="ca"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'menys set', -42: 'menys quaranta-dos', 2.5: 'dos coma cinc', 3.14: 'tres coma un quatre', -3.5: 'menys tres coma cinc', 0.5: 'zero coma cinc'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="ca"), spoken)


class TestCatalanExtract(unittest.TestCase):
    """Anchors for extracting numbers from Catalan text."""

    def test_extract_number(self):
        expected = {0: 'zero', 1: 'un', 2: 'dos', 3: 'tres', 4: 'quatre', 5: 'cinc', 6: 'sis', 7: 'set', 8: 'vuit', 9: 'nou', 10: 'deu', 11: 'onze', 12: 'dotze', 13: 'tretze', 14: 'catorze', 15: 'quinze', 16: 'setze', 17: 'disset', 18: 'divuit', 19: 'dinou', 20: 'vint', 21: 'vint-i-un', 30: 'trenta', 42: 'quaranta-dos', 50: 'cinquanta', 66: 'seixanta-sis', 70: 'setanta', 80: 'vuitanta', 90: 'noranta', 99: 'noranta-nou', 100: 'cent', 101: 'cent un', 123: 'cent vint-i-tres', 200: 'dos-cents', 500: 'cinc-cents', 999: 'nou-cents noranta-nou', 1000: 'mil', 2000: 'dos mil', 2023: 'dos mil vint-i-tres', 1000000: 'un milió', 2000000: 'dos milions'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="ca"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'menys set', -42: 'menys quaranta-dos', 2.5: 'dos coma cinc', 3.14: 'tres coma un quatre', -3.5: 'menys tres coma cinc', 0.5: 'zero coma cinc'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="ca"), number)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('tinc vint-i-un gats', lang="ca"),
                         21)

    def test_extract_scale_groups(self):
        # Exact written forms taken from the Consorci per a la Normalització
        # Lingüística grammar "6. Els numerals" (IEC normativa) and the Optimot
        # fitxa "Guionet en els numerals compostos": a hundreds group before a
        # scale word multiplies that scale word and the products are summed.
        expected = {
            'cinc-cents mil': 500000,
            'cent mil': 100000,
            'dos milions cent mil': 2100000,
            'dos milions cinc-cents mil': 2500000,
            'un milió dos-cents trenta-quatre mil sis-cents': 1234600,
            'dos milions cinc-cents seixanta-nou mil vuit-cents setanta-cinc':
                2569875,
            'mil cent': 1100,
        }
        for spoken, number in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="ca"), number)

    def test_no_number(self):
        self.assertIn(extract_number("hola com estàs", lang="ca"), (False, None))


class TestCatalanRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 1000000, 2000000, 2100000, 2500000, 3400000, 1500000,
                       2001500, 1234600, 2569875, 9999999]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="ca")
                self.assertEqual(extract_number(spoken, lang="ca"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="ca")
                self.assertEqual(extract_number(spoken, lang="ca"), number)


class TestCatalanLongScale(unittest.TestCase):
    """Catalan is a long-scale language: miliard=10^9, bilió=10^12.

    See https://en.wikipedia.org/wiki/Long_and_short_scales
    """

    def test_extract_long_scale_words(self):
        expected = {
            'un miliard': 10 ** 9,
            'un bilió': 10 ** 12,
            'dos miliards': 2 * 10 ** 9,
            'tres bilions': 3 * 10 ** 12,
            'cinc miliards': 5 * 10 ** 9,
            'un bilió dos miliards': 10 ** 12 + 2 * 10 ** 9,
            'dos milions cinc-cents mil': 2500000,
        }
        for spoken, number in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(
                    extract_number(spoken, lang="ca", scale=Scale.LONG), number)

    def test_short_scale_reads_billion_as_ten_pow_nine(self):
        # the same word "bilió" is 10^9 on the short scale
        self.assertEqual(
            extract_number('un bilió', lang="ca", scale=Scale.SHORT), 10 ** 9)
        self.assertEqual(
            extract_number('un trilió', lang="ca", scale=Scale.SHORT), 10 ** 12)

    def test_pronounce_long_scale(self):
        self.assertEqual(
            pronounce_number(10 ** 9, lang="ca", scale=Scale.LONG), 'un miliard')
        self.assertEqual(
            pronounce_number(10 ** 12, lang="ca", scale=Scale.LONG), 'un bilió')

    def test_round_trip_both_directions(self):
        # pronounce -> extract and (word -> extract -> pronounce) at each order
        for scale in (Scale.LONG, Scale.SHORT):
            for number in (10 ** 6, 10 ** 9, 10 ** 12):
                with self.subTest(scale=scale, number=number):
                    spoken = pronounce_number(number, lang="ca", scale=scale)
                    self.assertEqual(
                        extract_number(spoken, lang="ca", scale=scale), number)

    def test_long_and_short_disagree_above_million(self):
        long_val = extract_number('un bilió', lang="ca", scale=Scale.LONG)
        short_val = extract_number('un bilió', lang="ca", scale=Scale.SHORT)
        self.assertNotEqual(long_val, short_val)
        self.assertEqual(long_val, 10 ** 12)
        self.assertEqual(short_val, 10 ** 9)

    def test_scale_word_alone_without_multiplier(self):
        # a bare scale word ("miliard") still counts as one unit
        self.assertEqual(
            extract_number('miliard', lang="ca", scale=Scale.LONG), 10 ** 9)

    def test_unknown_scale_word_for_scale_is_ignored(self):
        # "miliard" is not a short-scale word; extraction must not invent it
        self.assertEqual(
            extract_number('un miliard', lang="ca", scale=Scale.SHORT), 1)

    def test_no_number_still_false_with_scale(self):
        self.assertIn(
            extract_number("hola com estàs", lang="ca", scale=Scale.LONG),
            (False, None))


class TestCatalanTinyFloat(unittest.TestCase):
    """Scientific-notation floats must not crash pronunciation."""

    def test_tiny_float_does_not_crash(self):
        for number in (1e-9, 1e-12, -1e-9, 1e-300):
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="ca")
                self.assertIsInstance(spoken, str)
                self.assertTrue(spoken)


class TestCatalanFractions(unittest.TestCase):
    """Catalan fraction nouns, gendered/plural and capitalized forms."""

    def test_basic_and_inflected(self):
        self.assertEqual(is_fractional("mig", lang="ca"), 0.5)
        self.assertEqual(is_fractional("mitja", lang="ca"), 0.5)
        self.assertEqual(is_fractional("terç", lang="ca"), 1.0 / 3)
        self.assertEqual(is_fractional("quart", lang="ca"), 0.25)
        self.assertEqual(is_fractional("quarta", lang="ca"), 0.25)
        self.assertEqual(is_fractional("centè", lang="ca"), 0.01)

    def test_capitalized_input_does_not_crash(self):
        self.assertEqual(is_fractional("Mig", lang="ca"), 0.5)
        self.assertEqual(is_fractional("QUART", lang="ca"), 0.25)
        self.assertEqual(is_fractional("Centè", lang="ca"), 0.01)

    def test_non_fraction_returns_false(self):
        for word in ["", "hola", "cinc"]:
            with self.subTest(word=word):
                self.assertFalse(is_fractional(word, lang="ca"))


if __name__ == "__main__":
    unittest.main()


class TestCatalanRoundTripSweep(unittest.TestCase):
    """pronounce -> extract identity across the whole 0..10,000,000 range.

    Dense at the low end where every tens-units and hundreds compound occurs,
    then strided through the millions; every value is checked with both signs.
    """

    def _sweep(self):
        for n in range(0, 3000):
            yield n
        for n in range(3000, 100000, 137):
            yield n
        for n in range(100000, 10_000_001, 4999):
            yield n

    def test_round_trip_both_signs(self):
        bad = []
        for n in self._sweep():
            for value in (n, -n):
                spoken = pronounce_number(value, lang="ca")
                if extract_number(spoken, lang="ca") != value:
                    bad.append((value, spoken))
        self.assertEqual(bad, [], f"round-trip failures: {bad[:10]}")
