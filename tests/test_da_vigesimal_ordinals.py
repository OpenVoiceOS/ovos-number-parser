"""Danish ordinals of the tens 40-90, in both written forms.

Dansk Sprognævn, sproget.dk answer SV00000084: "I 1986 blev ordene fyrrende,
halvtredsende, tressende, halvfjerdsende, firsende og halvfemsende optaget i
Retskrivningsordbogen ved siden af fyrretyvende, halvtredsindstyvende,
tresindstyvende, halvfjerdsindstyvende, firsindstyvende og
halvfemsindstyvende. De er af nyere dato end formerne på -tyvende, men lige
så korrekte."

Each pair names the ordinal of the same ten: 40, 50, 60, 70, 80 and 90. A
compound puts the unit first and joins it with "og", as the cardinal does
("toogfyrre" = 42).
"""
import unittest

from ovos_number_parser import extract_number
from ovos_number_parser.numbers_da import is_ordinal_da

TENS = {40: ("fyrretyvende", "fyrrende"),
        50: ("halvtredsindstyvende", "halvtredsende"),
        60: ("tresindstyvende", "tressende"),
        70: ("halvfjerdsindstyvende", "halvfjerdsende"),
        80: ("firsindstyvende", "firsende"),
        90: ("halvfemsindstyvende", "halvfemsende")}

#: unit word, its value
UNITS = [("en", 1), ("to", 2), ("tre", 3), ("syv", 7), ("ni", 9)]


class TestVigesimalOrdinals(unittest.TestCase):

    def test_each_ten_in_both_forms(self):
        for value, words in TENS.items():
            for word in words:
                with self.subTest(word=word):
                    self.assertEqual(is_ordinal_da(word), value)

    def test_unit_og_ten(self):
        for value, words in TENS.items():
            for word in words:
                for unit, unit_value in UNITS:
                    compound = f"{unit}og{word}"
                    with self.subTest(word=compound):
                        self.assertEqual(is_ordinal_da(compound),
                                         unit_value + value)

    def test_in_a_sentence(self):
        self.assertEqual(extract_number("han blev nummer toogfyrretyvende",
                                        lang="da", ordinals=True), 42)
        self.assertEqual(extract_number("den halvtredsindstyvende dag",
                                        lang="da", ordinals=True), 50)

    def test_twenty_and_thirty_keep_their_reading(self):
        for word, value in [("tyvende", 20), ("enogtyvende", 21),
                            ("tredivte", 30), ("femogtredivte", 35)]:
            with self.subTest(word=word):
                self.assertEqual(is_ordinal_da(word), value)

    def test_a_cardinal_ten_is_no_ordinal(self):
        for word in ("fyrre", "halvtreds", "tres", "firs", "halvfems"):
            with self.subTest(word=word):
                self.assertIs(is_ordinal_da(word), False)


if __name__ == "__main__":
    unittest.main()
