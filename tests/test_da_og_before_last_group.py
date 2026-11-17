"""Danish links a final group below 100 to a hundred or thousand with "og".

Dansk Sprognævn, svarbase SV00017853: "Man vil altså udtale tallene: et
hundrede og en, et tusinde og en, en million og en." Wiktionary
Appendix:Danish numerals: "tre tusinde to hundrede og fireoghalvtreds"
(3254). Den Danske Ordbog: "tusinde eller tusind talord (mængdetal)".

Ordinals: the cardinal head stays and "og" precedes the last ordinal
(Politikens sprogklumme on sproget.dk: "hundred(e) (og) syttende"). Den
Danske Ordbog lists "hundrede" and "tusinde" as the ordinals of 100 and 1000
and "millionte", "milliardte" for the larger scale words. Dansk Sprognævn,
svarbase SV00000084: "tresindstyvende" and "tressende" both name the 60th.
"""
import unittest

from ovos_number_parser import pronounce_number, pronounce_ordinal


class TestDanishOgBeforeLastGroup(unittest.TestCase):
    CASES = {
        101: "hundrede og en",
        1001: "tusind og en",
        1010: "tusind og ti",
        2001: "to tusind og en",
        2024: "to tusind og fireogtyve",
        2101: "to tusind hundrede og en",
        3254: "tre tusind to hundrede og fireoghalvtreds",
        101000: "hundrede og et tusind",
        1000001: "en million og en",
        2000024: "to millioner og fireogtyve",
        1500: "tusind fem hundrede",
        2000: "to tusind",
        1000: "tusind",
    }

    def test_cardinals(self):
        for value, spoken in self.CASES.items():
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "da"), spoken)


class TestDanishOrdinals(unittest.TestCase):
    CASES = {
        60: "tresindstyvende",
        61: "enogtresindstyvende",
        40: "fyrrende",
        50: "halvtredsende",
        70: "halvfjerdsende",
        80: "firsende",
        90: "halvfemsende",
        100: "hundrede",
        101: "hundrede og første",
        117: "hundrede og syttende",
        200: "to hundrede",
        1000: "tusinde",
        1001: "tusind og første",
        2000: "to tusinde",
        1000000: "millionte",
        2000000: "to millionte",
        1000000000: "milliardte",
    }

    def test_ordinals(self):
        for value, spoken in self.CASES.items():
            with self.subTest(value=value):
                self.assertEqual(pronounce_ordinal(value, "da"), spoken)


if __name__ == "__main__":
    unittest.main()
