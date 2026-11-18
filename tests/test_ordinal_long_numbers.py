"""Ordinals of long numbers read in words or decline with a named error."""
import unittest

from ovos_number_parser import pronounce_number, pronounce_ordinal

LANGS = ("et", "fi", "sv", "nb", "nn", "hu", "da", "de", "nl", "fy")

# (language, first number whose ordinal is not read in words)
LIMIT = {
    "et": 10 ** 15,
    "fi": 10 ** 15,
    "sv": 10 ** 24,
    "nb": 10 ** 21,
    "nn": 10 ** 21,
    "hu": 10 ** 24,
    "da": 10 ** 24,
    "de": 10 ** 24,
    "nl": 10 ** 24,
    "fy": 10 ** 24,
}

ROWS = {
    "sv": [
        (10 ** 9, "miljardte"),
        (2 * 10 ** 9, "tvåmiljardte"),
        (10 ** 12, "biljonte"),
        (10 ** 15, "biljardte"),
        (10 ** 18, "triljonte"),
        (10 ** 21, "triljardte"),
        (10 ** 9 + 7, "en miljard sjunde"),
        (10 ** 12 + 7, "en biljon sjunde"),
    ],
    "nb": [
        (10 ** 9, "milliardte"),
        (2 * 10 ** 9, "to milliardte"),
        (10 ** 12, "billionte"),
        (10 ** 15, "billiardte"),
        (10 ** 18, "trillionte"),
        (10 ** 9 + 7, "en milliard og sjuende"),
        (10 ** 12 + 3, "en billion og tredje"),
        (1010000001, "en milliard ti millioner og første"),
        (1200000007, "en milliard to hundre millioner og sjuende"),
        (2100000000, "to milliarder hundre millionte"),
        (1010000000, "en milliard ti millionte"),
    ],
    "nn": [
        (10 ** 9, "milliardte"),
        (2 * 10 ** 9, "to milliardte"),
        (10 ** 12, "billionte"),
        (10 ** 18, "trillionte"),
        (10 ** 9 + 7, "ein milliard og sjuande"),
        (2100000000, "to milliardar hundre millionte"),
    ],
    "fi": [
        (10 ** 9, "miljardis"),
        (2 * 10 ** 9, "kahdesmiljardis"),
        (10 ** 9 + 7, "miljardisseitsemäs"),
        (1500000000, "miljardisviidessadasmiljoonas"),
        (10 ** 12, "biljoonas"),
        (3 * 10 ** 12, "kolmasbiljoonas"),
        (10 ** 12 + 7, "biljoonasseitsemäs"),
    ],
    "hu": [
        (10 ** 9, "egymilliárdodik"),
        (2 * 10 ** 9, "kétmilliárdodik"),
        (10 ** 12, "egybilliomodik"),
        (10 ** 15, "egybilliárdodik"),
        (10 ** 18, "egytrilliomodik"),
        (10 ** 21, "egytrilliárdodik"),
        (10 ** 9 + 7, "egymilliárd-hetedik"),
        # the last digit of a number past 2 ** 53 is read from the integer
        (12345678901234567893,
         "tizenkéttrillió-háromszáznegyvenötbilliárd-hatszázhetvennyolcbillió-"
         "kilencszázegymilliárd-kétszázharmincnégymillió-ötszázhatvanhétezer-"
         "nyolcszázkilencvenharmadik"),
    ],
    "et": [
        (10 ** 6, "miljones"),
        (2 * 10 ** 6, "kahemiljones"),
        (10 ** 9, "miljardes"),
        (10 ** 12, "biljones"),
        (10 ** 6 + 7, "miljoni seitsmes"),
        (10 ** 9 + 7, "miljardi seitsmes"),
        (10 ** 12 + 7, "biljoni seitsmes"),
        (3002003, "kolme miljoni kahe tuhande kolmas"),
        (15 * 10 ** 6, "viieteistkümne miljones"),
        (2003, "kahe tuhande kolmas"),
        (21000, "kahekümne ühe tuhandes"),
        (110000, "saja kümne tuhandes"),
        (10000, "kümne tuhandes"),
        (10 ** 7, "kümne miljones"),
        (5010000, "viie miljoni kümne tuhandes"),
        (10 ** 10, "kümne miljardes"),
        (10 ** 13, "kümne biljones"),
    ],
}


class TestOrdinalLongNumbers(unittest.TestCase):
    def test_rows(self):
        for lang, rows in ROWS.items():
            for number, expected in rows:
                with self.subTest(lang=lang, number=number):
                    self.assertEqual(pronounce_ordinal(number, lang), expected)

    def test_words_below_the_limit_and_named_error_from_it(self):
        for lang in LANGS:
            limit = LIMIT[lang]
            for digits in range(1, 31):
                number = 10 ** (digits - 1) + 7
                with self.subTest(lang=lang, digits=digits):
                    if number >= limit:
                        with self.assertRaises(NotImplementedError):
                            pronounce_ordinal(number, lang)
                    else:
                        spoken = pronounce_ordinal(number, lang)
                        self.assertIsInstance(spoken, str)
                        self.assertFalse(any(c.isdigit() for c in spoken),
                                         spoken)

    def test_no_error_below_the_limit_for_round_counts(self):
        for lang in LANGS:
            for exponent in range(3, 31):
                for count in (1, 2, 9, 10, 11, 20, 100):
                    number = count * 10 ** exponent
                    if number >= LIMIT[lang]:
                        continue
                    with self.subTest(lang=lang, number=number):
                        spoken = pronounce_ordinal(number, lang)
                        self.assertFalse(any(c.isdigit() for c in spoken),
                                         spoken)

    def test_limit_is_where_the_cardinal_writer_stops(self):
        # the cardinal writer reads the digits back, or in scientific form
        scientific = {"sv": "gånger", "da": "gange", "de": "mal", "nl": "maal"}
        for lang in LANGS:
            limit = LIMIT[lang]
            with self.subTest(lang=lang):
                below = pronounce_number(limit - 1, lang)
                self.assertFalse(any(c.isdigit() for c in below), below)
                at = pronounce_number(limit, lang)
                if lang in scientific:
                    self.assertIn(scientific[lang], at)
                else:
                    self.assertEqual(at, str(limit))

    def test_ordinals_flag_matches(self):
        for lang in ("et", "fi"):
            for number in (10 ** 9 + 7, 10 ** 12):
                with self.subTest(lang=lang, number=number):
                    self.assertEqual(
                        pronounce_number(number, lang, ordinals=True),
                        pronounce_ordinal(number, lang))


if __name__ == "__main__":
    unittest.main()
