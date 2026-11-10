"""Very large magnitudes read as numbers in every language.

Each expected value comes from a reading the fix does not compute: the same
value given as an int, the language's reading of a smaller value, or the
scientific reading assembled from ``pronounce_number`` of the mantissa and the
exponent plus a cited connective.
"""
import unittest

from ovos_number_parser import pronounce_number, _pronounce_bignum_fallback
from ovos_number_parser.util import scientific_notation

#: every native backend except kab, whose finite ceiling of 9999 is documented
NATIVE = ["an", "ar", "ast", "az", "bg", "ca", "cs", "da", "de", "el", "en",
          "es", "et", "eu", "fa", "fi", "fr", "fy", "gl", "he", "hr", "hu",
          "id", "it", "ms", "mwl", "nb", "nl", "nn", "oc", "pl", "pt-PT",
          "pt-BR", "ro", "ru", "sk", "sl", "sv", "tr", "uk"]

#: backends whose named scales end below 10 ** 100; above that they read the
#: value in their own scientific form
SCIENTIFIC_BACKENDS = ["az", "bg", "fa", "hr", "sk", "sl", "tr", "uk"]

#: backends with a scientific mode of their own, whose connective the
#: dispatcher fallback reuses
SCIENTIFIC_MODE = ["az", "bg", "cs", "fa", "hr", "pl", "ru", "sk", "sl",
                   "tr", "uk"]


def minus_word(lang):
    """The minus word of the language's ordinary negative reading."""
    return pronounce_number(-5, lang)[:-len(pronounce_number(5, lang))]


class _ReprWrapper(float):
    """A float whose repr is not a bare number while its str is, as numpy 2
    writes "np.float64(1e+16)" and "1e+16"."""

    __str__ = float.__repr__

    def __repr__(self):
        return f"np.float64({float.__repr__(self)})"


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

    def test_float_subclass_with_wrapped_repr(self):
        for lang in ("en", "de", "fr"):
            for value, exact in ((1e16, 10 ** 16), (-2.5e20, -25 * 10 ** 19)):
                with self.subTest(lang=lang, value=value):
                    self.assertEqual(
                        pronounce_number(_ReprWrapper(value), lang),
                        pronounce_number(exact, lang))

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
        # 111 * 10 ** 398 repeats a mantissa digit and takes the dispatcher
        # fallback; 10 ** 400 reads in the backend
        for lang, value in (("en", 10 ** 400), ("en", 111 * 10 ** 398),
                            ("ru", 10 ** 100), ("ru", 10 ** 400),
                            ("cs", 10 ** 400), ("cs", 111 * 10 ** 398),
                            ("pl", 10 ** 400)):
            with self.subTest(lang=lang, value=value):
                self.assertEqual(
                    pronounce_number(-value, lang),
                    minus_word(lang) + pronounce_number(value, lang))

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
        # "нула нула" and "jedan jedan" read the mantissa digit by digit;
        # they are not padding, and the reading keeps the backend's words
        cases = [(lang, 111 * 10 ** 398) for lang in SCIENTIFIC_MODE]
        # past the named scales of these four, inside those of the rest
        cases += [(lang, 4007432372075044522000117569525566)
                  for lang in ("bg", "fa", "hr", "sk")]
        for lang, value in cases:
            with self.subTest(lang=lang, value=value):
                scientific = pronounce_number(value, lang, scientific=True)
                self.assertEqual(pronounce_number(value, lang), scientific)
                self.assertEqual(pronounce_number(-value, lang),
                                 minus_word(lang) + scientific)

    def test_fallback_speaks_the_backend_words(self):
        # the dispatcher fallback replaces a backend reading it flags as
        # padded, so both must say the same words for every value
        for lang in SCIENTIFIC_MODE:
            for value in (10 ** 30, 12 * 10 ** 29, 4 * 10 ** 33, 10 ** 100,
                          128 * 10 ** 398):
                with self.subTest(lang=lang, value=value):
                    self.assertEqual(
                        _pronounce_bignum_fallback(value, lang, 3),
                        pronounce_number(value, lang, scientific=True))

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

    def test_croatian_cardinal_exponent(self):
        # hr.wikipedia "Dan kad je Zemlja stala (2008.)": "tri puta deset na
        # sedam metara u sekundi"; 111 * 10 ** 28 takes the dispatcher
        # fallback, the other values the backend
        for value, mantissa, exponent, kwargs in (
                (10 ** 30, 1, 30, {}),
                (111 * 10 ** 28, 1.11, 30, {}),
                (-10 ** 400, -1, 400, {}),
                (3 * 10 ** 7, 3, 7, {"scientific": True})):
            with self.subTest(value=value, **kwargs):
                self.assertEqual(
                    pronounce_number(value, "hr", **kwargs),
                    f"{pronounce_number(mantissa, 'hr')} puta deset na "
                    f"{pronounce_number(exponent, 'hr')}")

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


class TestScientificNotation(unittest.TestCase):
    """Beyond the float range the mantissa rounds, as '%E' does."""

    def test_rounds_the_mantissa(self):
        # 9.99999999...E+400 rounds up to 1.000000E+401;
        # 1.234567890E+400 rounds to 1.234568E+400
        for value, expected in ((10 ** 401 - 1, "1.000000E+401"),
                                (1 - 10 ** 401, "-1.000000E+401"),
                                (1234567890 * 10 ** 391, "1.234568E+400"),
                                (10 ** 400, "1.000000E+400")):
            with self.subTest(value=expected):
                self.assertEqual(scientific_notation(value), expected)

    def test_spoken_value_is_rounded(self):
        for lang in ("cs", "pl", "en", "ru"):
            with self.subTest(lang=lang):
                self.assertEqual(pronounce_number(10 ** 401 - 1, lang),
                                 pronounce_number(10 ** 401, lang))


if __name__ == "__main__":
    unittest.main()
