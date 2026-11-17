"""Slovenian reads 2 as masculine "dva" before tisoč and milijon.

Slovenski pravopis, člen 544, quoted by ZRC SAZU svetovalnica "Zapis stotic":
"Druge glavne števnike pišemo narazen: sto enajst, dva tisoč, sedem milijonov".
Wiktionary Module:number list/data/sl: 2000 "dva tisoč", ordinal "dvatisoči".
Lektorsko društvo Slovenije, Jezikovni pogovor 2014: "leto 2002 pravilno samo
kot [dva tisoč dve]" -- the final digit keeps the counting form "dve".
Slovenski pravopis, via slo-na-dlani.si: "dvesto dva tisoč dvesto".
"""
import unittest

from ovos_number_parser import pronounce_number, pronounce_ordinal


class TestSlovenianTwoBeforeTisoc(unittest.TestCase):
    CASES = {
        2000: "dva tisoč",
        2002: "dva tisoč dve",
        2024: "dva tisoč štiriindvajset",
        3000: "tri tisoč",
        22000: "dvaindvajset tisoč",
        202000: "dvesto dva tisoč",
        202200: "dvesto dva tisoč dvesto",
        102000: "sto dva tisoč",
    }

    def test_cardinals(self):
        for value, spoken in self.CASES.items():
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "sl"), spoken)

    def test_units_keep_the_counting_form(self):
        self.assertEqual(pronounce_number(102, "sl"), "sto dve")
        self.assertEqual(pronounce_number(2, "sl"), "dve")

    def test_ordinal_of_2000(self):
        self.assertEqual(pronounce_ordinal(2000, "sl"), "dvatisoči")


if __name__ == "__main__":
    unittest.main()
