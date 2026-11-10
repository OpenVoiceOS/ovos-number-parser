"""Very large magnitudes read as numbers in every language.

Each expected value comes from a reading the fix does not compute: the same
value given as an int, the language's reading of a smaller value, or the
scientific reading assembled from ``pronounce_number`` of the mantissa and the
exponent plus a cited connective.
"""
import unittest

from ovos_number_parser import pronounce_number

#: every native backend except kab, whose finite ceiling of 9999 is documented
NATIVE = ["an", "ar", "ast", "az", "bg", "ca", "cs", "da", "de", "el", "en",
          "es", "et", "eu", "fa", "fi", "fr", "fy", "gl", "he", "hr", "hu",
          "id", "it", "ms", "mwl", "nb", "nl", "nn", "oc", "pl", "pt-PT",
          "pt-BR", "ro", "ru", "sk", "sl", "sv", "tr", "uk"]

#: backends whose named scales end below 10 ** 100; above that they read the
#: value in their own scientific form
SCIENTIFIC_BACKENDS = ["az", "bg", "fa", "hr", "sk", "sl", "tr", "uk"]


class TestFloatReadsAsTheIntItWrites(unittest.TestCase):
    """A float this large is a whole number; it reads as the int of its repr."""

    def test_float_matches_int(self):
        for lang in NATIVE:
            for value, exact in ((1e16, 10 ** 16), (1e22, 10 ** 22),
                                 (1e100, 10 ** 100), (1e300, 10 ** 300)):
                for sign in (1, -1):
                    with self.subTest(lang=lang, value=sign * value):
                        self.assertEqual(
                            pronounce_number(sign * value, lang),
                            pronounce_number(sign * exact, lang))

    def test_no_exponent_string(self):
        for lang in ("nb", "nn", "da", "de", "fy", "hu", "nl", "sv", "fr"):
            for value in (1e22, -1e22, 1e100, -1e300):
                with self.subTest(lang=lang, value=value):
                    self.assertNotIn("e+", pronounce_number(value, lang))


class TestIntegerArithmetic(unittest.TestCase):
    """Digits above 2 ** 53 survive; the low groups read as the low value."""

    def test_low_groups_match_the_smaller_value(self):
        value = 654321987654321987
        low = value % 10 ** 6
        for lang in ("da", "de", "fy", "hu", "nl", "sv"):
            with self.subTest(lang=lang):
                self.assertTrue(
                    pronounce_number(value, lang).endswith(
                        pronounce_number(low, lang)),
                    pronounce_number(value, lang))


class TestSignedHugeIntegers(unittest.TestCase):
    """A negative value reads as the minus word plus the positive reading."""

    def test_negative_is_minus_plus_positive(self):
        for lang, value in (("en", 10 ** 400), ("ru", 10 ** 100),
                            ("ru", 10 ** 400), ("cs", 10 ** 400),
                            ("pl", 10 ** 400)):
            with self.subTest(lang=lang, value=value):
                positive = pronounce_number(value, lang)
                negative = pronounce_number(-value, lang)
                self.assertTrue(negative.endswith(positive), negative)
                self.assertTrue(negative[:-len(positive)].strip(), negative)

    def test_beyond_the_float_range_is_not_empty(self):
        for lang in ("cs", "pl"):
            with self.subTest(lang=lang):
                self.assertEqual(
                    pronounce_number(10 ** 400, lang),
                    pronounce_number(10 ** 300, lang, scientific=True)
                    .replace(pronounce_number(300, lang),
                             pronounce_number(400, lang)))


class TestNoInfinityOrZeroForAFiniteValue(unittest.TestCase):
    """Past its named scales a backend reads its own scientific form."""

    def test_reads_scientifically(self):
        for lang in SCIENTIFIC_BACKENDS:
            for value in (10 ** 100, -10 ** 100):
                with self.subTest(lang=lang, value=value):
                    self.assertEqual(
                        pronounce_number(value, lang),
                        pronounce_number(value, lang, scientific=True))

    def test_bg_fa_from_their_last_scale(self):
        for lang, value in (("bg", 10 ** 21), ("bg", -10 ** 25),
                            ("fa", 10 ** 21), ("fa", -10 ** 25)):
            with self.subTest(lang=lang, value=value):
                self.assertEqual(
                    pronounce_number(value, lang),
                    pronounce_number(value, lang, scientific=True))

    def test_repeated_mantissa_digit(self):
        # "нула нула" reads the mantissa digit by digit; it is not padding
        value = 4007432372075044522000117569525566
        for lang in ("bg", "fa", "sk"):
            for sign in (1, -1):
                with self.subTest(lang=lang, sign=sign):
                    self.assertEqual(
                        pronounce_number(sign * value, lang),
                        pronounce_number(sign * value, lang, scientific=True))

    def test_beyond_the_float_range(self):
        for lang in SCIENTIFIC_BACKENDS:
            for sign in (1, -1):
                with self.subTest(lang=lang, sign=sign):
                    self.assertEqual(
                        pronounce_number(sign * 10 ** 400, lang),
                        pronounce_number(sign * 10 ** 300, lang,
                                         scientific=True)
                        .replace(pronounce_number(300, lang),
                                 pronounce_number(400, lang)))


class TestLocalizedConnective(unittest.TestCase):
    """The scientific fallback joins mantissa and exponent in the language."""

    CONNECTIVE = {
        # an.wikipedia "Numero π": "factor primo elevau a una potencia";
        # "Albert Einstein": "a masa (m) por a velocidat d'a luz (c) elevada"
        "an": "por diez elevau a",
        # el.wikipedia "Δύναμη του 10": "10^6 (δέκα στη δύναμη του έξι)";
        # "Πολλαπλασιασμός": "πέντε επί δύο"
        "el": "επί δέκα στη δύναμη του",
        # he.wikipedia "כתיב מדעי": "E" stands for "כפול עשר בחזקת"
        "he": "כפול עשר בחזקת",
        # id.wikipedia "Notasi ilmiah": "satu koma dua lima kali sepuluh
        # pangkat negatif 8"
        "id": "kali sepuluh pangkat",
    }

    def test_fallback_uses_the_language_connective(self):
        for lang, connective in self.CONNECTIVE.items():
            for value, exponent in ((10 ** 25, 25), (10 ** 100, 100),
                                    (-10 ** 400, 400)):
                mantissa = 1.0 if value > 0 else -1.0
                with self.subTest(lang=lang, value=value):
                    self.assertEqual(
                        pronounce_number(value, lang),
                        f"{pronounce_number(mantissa, lang)} {connective} "
                        f"{pronounce_number(exponent, lang)}")

    def test_greek_scientific_mode(self):
        self.assertEqual(
            pronounce_number(2e5, "el", scientific=True),
            f"{pronounce_number(2, 'el')} επί δέκα στη δύναμη του "
            f"{pronounce_number(5, 'el')}")


class TestBareNumeralFallback(unittest.TestCase):
    """et and fi hand back the digits of a whole float, never "x.0"."""

    def test_whole_float_below_1e16(self):
        for lang in ("et", "fi"):
            for value in (1e15, -1e15, 2.5e15):
                with self.subTest(lang=lang, value=value):
                    self.assertEqual(pronounce_number(value, lang),
                                     pronounce_number(int(value), lang))


class TestFrenchLargeValues(unittest.TestCase):
    """fr reads a whole float of 1e16 and up scientifically, like the int."""

    def test_float_reads_scientifically(self):
        for value, mantissa, exponent in ((1e16, 1, 16), (-1e22, -1, 22)):
            with self.subTest(value=value):
                self.assertEqual(
                    pronounce_number(value, "fr"),
                    f"{pronounce_number(mantissa, 'fr')} fois dix puissance "
                    f"{pronounce_number(exponent, 'fr')}")

if __name__ == "__main__":
    unittest.main()
