"""Scale words of cs, it, uk, the shared Romance engine and regional French.

Every expected reading is composed in this file from the scale names of the
language's own tables (cited in the pull request), with the count of each
group read by ``pronounce_number`` below a thousand. The readings must also
extract back to the same value.
"""
import re
import unittest

from unicode_rbnf import RbnfEngine

from ovos_number_parser import (extract_number, pronounce_number,
                                _pronounce_bignum_fallback)

#: Czech long scale (cs.wikipedia "Názvy velkých čísel")
CS_LONG = ["tisíc", "milion", "miliarda", "bilion", "biliarda", "trilion",
           "triliarda", "kvadrilion", "kvadriliarda", "kvintilion",
           "kvintiliarda", "sextilion", "sextiliarda", "septilion",
           "septiliarda", "oktilion", "oktiliarda", "nonilion", "noniliarda",
           "decilion", "deciliarda"]

#: Italian long scale (it.wikipedia "Scala lunga e scala corta"), singular
IT_LONG = ["mille", "milione", "miliardo", "bilione", "biliardo", "trilione",
           "triliardo", "quadrilione", "quadriliardo", "quintilione",
           "quintiliardo", "sestilione", "sestiliardo", "settilione",
           "settiliardo", "ottilione", "ottiliardo", "nonilione",
           "noniliardo", "decilione", "deciliardo"]

#: Ukrainian short scale (uk.wikipedia "Іменні назви степенів тисячі")
UK_SHORT = ["тисяча", "мільйон", "мільярд", "трильйон", "квадрильйон",
            "квінтильйон", "секстильйон", "септильйон", "октильйон",
            "нонільйон", "децильйон", "ундецильйон", "додецильйон",
            "тредецильйон", "кватордецильйон", "квіндецильйон",
            "сексдецильйон", "септендецильйон", "октодецильйон",
            "новемдецильйон", "вігінтильйон"]

#: Ukrainian long scale (same article, rule "N")
UK_LONG = ["тисяча", "мільйон", "мільярд", "більйон", "більярд", "трильйон",
           "трильярд", "квадрильйон", "квадрильярд", "квінтильйон",
           "квінтильярд", "секстильйон", "секстильярд", "септильйон",
           "септильярд", "октильйон", "октильярд", "нонільйон", "нонільярд",
           "децильйон", "децильярд"]


def compose_cs(n):
    """Czech long-scale reading: groups of three digits, largest first,
    each count followed by the uninflected scale noun."""
    groups = []
    k = 0
    while n:
        n, z = divmod(n, 1000)
        if z:
            word = pronounce_number(z, "cs")
            groups.append(word if not k else f"{word} {CS_LONG[k - 1]}")
        k += 1
    return ", ".join(reversed(groups))


def compose_it(n):
    """Italian long-scale reading of a multiple of a million: "un" and the
    singular for one, the fused count and the plural otherwise."""
    groups = []
    k = 0
    while n:
        n, z = divmod(n, 1000)
        if z:
            assert k >= 2
            name = IT_LONG[k - 1]
            if z == 1:
                groups.append(f"un {name}")
            else:
                plural = name[:-1] + "i"
                groups.append(f"{pronounce_number(z, 'it')} {plural}")
        k += 1
    return " ".join(reversed(groups))


def ukrainian_genitive_plural(noun):
    """Genitive plural after five to twenty: "трильйонів", "більярдів"."""
    return noun + "ів"


class TestCzechLongScale(unittest.TestCase):
    def test_powers_of_a_thousand(self):
        for k, name in enumerate(CS_LONG[2:], start=3):
            with self.subTest(power=3 * k):
                self.assertEqual(pronounce_number(10 ** (3 * k), "cs"), name)

    def test_composed_readings(self):
        values = [7 * 10 ** 9, 7 * 10 ** 12, 10 ** 16, 7 * 10 ** 15,
                  999999 * 10 ** 12, 2 * 10 ** 15 + 5, 1234567890,
                  1234567890123, 1234567890123456789, 5 * 10 ** 60 + 3]
        for value in values:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "cs"),
                                 compose_cs(value))

    def test_round_trip(self):
        for value in [7 * 10 ** 12, 10 ** 16, 1234567890123456789,
                      999999 * 10 ** 12, 7 * 10 ** 63]:
            with self.subTest(value=value):
                spoken = pronounce_number(value, "cs")
                self.assertEqual(extract_number(spoken, "cs"), value)

    def test_past_the_table_reads_scientifically(self):
        self.assertEqual(pronounce_number(10 ** 66, "cs"),
                         pronounce_number(10 ** 66, "cs", scientific=True))


class TestItalianLongScale(unittest.TestCase):
    def test_powers_of_a_thousand(self):
        for k, name in enumerate(IT_LONG[1:], start=2):
            with self.subTest(power=3 * k):
                self.assertEqual(pronounce_number(10 ** (3 * k), "it"),
                                 f"un {name}")

    def test_composed_readings(self):
        values = [7 * 10 ** 9, 7 * 10 ** 12, 10 ** 16, 7 * 10 ** 15,
                  10 ** 24, 999 * 10 ** 63, 2 * 10 ** 12 + 10 ** 6,
                  21 * 10 ** 15]
        for value in values:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "it"),
                                 compose_it(value))

    def test_round_trip(self):
        for value in [7 * 10 ** 12, 10 ** 15, 10 ** 24, 1234567890123456789,
                      21 * 10 ** 15, 999 * 10 ** 63]:
            with self.subTest(value=value):
                spoken = pronounce_number(value, "it")
                self.assertEqual(extract_number(spoken, "it"), value)

    def test_thousand_of_a_scale_still_reads(self):
        # "mille miliardi" and "mille bilioni" are the other reading the
        # source gives for 10 ** 12 and 10 ** 15
        self.assertEqual(extract_number("mille miliardi", "it"), 10 ** 12)
        self.assertEqual(extract_number("mille bilioni", "it"), 10 ** 15)

    def test_past_the_table_reads_scientifically(self):
        spoken = pronounce_number(10 ** 66, "it")
        self.assertEqual(spoken, _pronounce_bignum_fallback(10 ** 66, "it", 3))


class TestUkrainianScales(unittest.TestCase):
    def test_short_scale_powers(self):
        for k, name in enumerate(UK_SHORT[2:], start=3):
            with self.subTest(power=3 * k):
                self.assertEqual(pronounce_number(10 ** (3 * k), "uk"), name)
                seven = f"сім {ukrainian_genitive_plural(name)}"
                self.assertEqual(pronounce_number(7 * 10 ** (3 * k), "uk"),
                                 seven)
                self.assertEqual(extract_number(seven, "uk"),
                                 7 * 10 ** (3 * k))

    def test_long_scale_powers(self):
        for k, name in enumerate(UK_LONG[2:], start=3):
            with self.subTest(power=3 * k):
                value = 10 ** (3 * k)
                self.assertEqual(
                    pronounce_number(value, "uk", short_scale=False), name)
                seven = f"сім {ukrainian_genitive_plural(name)}"
                self.assertEqual(
                    pronounce_number(7 * value, "uk", short_scale=False),
                    seven)
                self.assertEqual(
                    extract_number(seven, "uk", short_scale=False), 7 * value)

    def test_round_trip(self):
        for value in [7 * 10 ** 12, 10 ** 16, 5 * 10 ** 12 + 7,
                      1234567890123456789, 987654321987654321987]:
            for short in (True, False):
                with self.subTest(value=value, short_scale=short):
                    spoken = pronounce_number(value, "uk", short_scale=short)
                    self.assertEqual(
                        extract_number(spoken, "uk", short_scale=short), value)

    def test_long_only_word_reads_in_the_long_scale(self):
        self.assertEqual(extract_number("сім більярдів", "uk"), 7 * 10 ** 15)


class TestRomanceScalesDoNotStack(unittest.TestCase):
    #: (lang, first value past the largest scale word, last value read in
    #: words, the largest scale word in its plural)
    CASES = [
        ("ro", 10 ** 24, 999999 * 10 ** 18, "trilioane"),
        ("pt-BR", 10 ** 69, 999999 * 10 ** 63, "vigintilhões"),
        ("gl", 10 ** 400, None, None),
        ("es", 10 ** 42, 999999 * 10 ** 36, "sextillones"),
        ("ca", 10 ** 30, 999999 * 10 ** 24, "quadrilions"),
        ("an", 10 ** 12, 999999 * 10 ** 6, "millones"),
    ]

    def test_past_the_largest_scale_reads_scientifically(self):
        for lang, first, _, _ in self.CASES:
            for value in (first, 7 * first, 123456789 * first):
                with self.subTest(lang=lang, value=value):
                    self.assertEqual(pronounce_number(value, lang),
                                     _pronounce_bignum_fallback(value, lang, 3))

    def test_stacked_readings(self):
        # "zece miliarde de trilioane de trilioane de trilioane ...",
        # "dez undecilhões vigintilhões", "dez mil quintillóns
        # unsexagintillóns"
        for lang, value in (("ro", 10 ** 100), ("pt-BR", 10 ** 100),
                            ("gl", 10 ** 400)):
            with self.subTest(lang=lang):
                self.assertEqual(pronounce_number(value, lang),
                                 _pronounce_bignum_fallback(value, lang, 3))

    def test_largest_scale_word_appears_once(self):
        for lang, _, last, word in self.CASES:
            if last is None:
                continue
            with self.subTest(lang=lang):
                spoken = pronounce_number(last, lang)
                self.assertEqual(spoken.split().count(word), 1, spoken)


class TestFrenchLargeFloats(unittest.TestCase):
    def test_non_whole_float_reads_like_its_magnitude(self):
        for value in (1e15 + 0.5, 1234567890123456.5, -1e15 - 0.5):
            with self.subTest(value=value):
                spoken = pronounce_number(value, "fr")
                self.assertIsNone(re.search(r"\d", spoken), spoken)
                self.assertEqual(spoken,
                                 _pronounce_bignum_fallback(value, "fr", 3))

    def test_non_whole_float_from_a_thousand_reads_in_words(self):
        for value, whole, decimals in [(1234.5, 1234, "5"),
                                       (1000.25, 1000, "25"),
                                       (123456.75, 123456, "75")]:
            with self.subTest(value=value):
                digits = " ".join(pronounce_number(int(d), "fr")
                                  for d in decimals)
                self.assertEqual(
                    pronounce_number(value, "fr"),
                    f"{pronounce_number(whole, 'fr')} virgule {digits}")


class TestRegionalFrenchCardinals(unittest.TestCase):
    #: CLDR RBNF fr_BE and fr_CH spellout-cardinal tens 70, 80 and 90
    TENS = {"fr-BE": {70: "septante", 90: "nonante"},
            "fr-CH": {70: "septante", 80: "huitante", 90: "nonante"}}

    def test_seventy_to_ninety_nine(self):
        for lang, tens in self.TENS.items():
            for n in range(70, 100):
                ten, unit = divmod(n, 10)
                if ten * 10 not in tens:
                    continue
                word = tens[ten * 10]
                if unit == 1:
                    word += "-et-un"
                elif unit:
                    word += "-" + pronounce_number(unit, "fr")
                with self.subTest(lang=lang, n=n):
                    self.assertEqual(pronounce_number(n, lang), word)
                    self.assertEqual(extract_number(word, lang), n)

    def test_agrees_with_cldr(self):
        # CLDR fr_BE joins 81-89 with a space ("quatre-vingt un") and writes
        # "quatre-vingts mille"; fr-BE keeps the France forms there, which
        # the Académie française writes "quatre-vingt-un" and
        # "quatre-vingt mille"
        values = list(range(2000)) + [71000, 80000, 91000000, 999999,
                                      1980, 197519, 70707070707]
        for locale, lang in (("fr_BE", "fr-BE"), ("fr_CH", "fr-CH")):
            engine = RbnfEngine.for_language(locale)
            for value in values:
                expected = engine.format_number(value).text
                if lang == "fr-BE":
                    expected = re.sub(r"quatre-vingt (?=(un|deux|trois|quatre"
                                      r"|cinq|six|sept|huit|neuf)\b)",
                                      "quatre-vingt-", expected)
                    expected = expected.replace("quatre-vingts mille",
                                                "quatre-vingt mille")
                with self.subTest(lang=lang, value=value):
                    self.assertEqual(pronounce_number(value, lang), expected)

    def test_round_trip(self):
        for lang in ("fr-BE", "fr-CH"):
            for value in list(range(2000)) + [71000, 91000000]:
                with self.subTest(lang=lang, value=value):
                    self.assertEqual(
                        extract_number(pronounce_number(value, lang), lang),
                        value)

    def test_france_keeps_vigesimal_tens(self):
        for lang in ("fr", "fr-FR", "fr-CA"):
            with self.subTest(lang=lang):
                self.assertEqual(pronounce_number(77, lang),
                                 "soixante-dix-sept")
                self.assertEqual(pronounce_number(98, lang),
                                 "quatre-vingt-dix-huit")


if __name__ == "__main__":
    unittest.main()
