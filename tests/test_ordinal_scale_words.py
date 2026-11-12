"""Russian, Ukrainian, Polish and Czech ordinals of round hundreds, thousands
and millions use the attested words.

The ordinal speller glued a cardinal to the scale word ("дватысячный",
"pięć tysięczny"), gave cardinals for Polish hundreds, and raised KeyError for
the Polish and Czech millions. Sources for the expected values:

- Russian: ru.wikipedia "Порядковое числительное" ("тридцативосьмимиллионный",
  "тридцатипятитысячных"); ru.wiktionary "двухтысячный", "трёхтысячный",
  "четырёхтысячный", "пятитысячный", "десятитысячный", "двадцатитысячный",
  "двадцатипятитысячный", "сорокатысячный", "девяностотысячный",
  "стотысячный", "двухсоттысячный", "пятисоттысячный", "миллионный",
  "двухмиллионный", "двадцатиодномиллионный" (the joining form "одно" of 1),
  "миллиардный";
- Ukrainian: en.wiktionary "двохтисячний", "трьохтисячний",
  "чотирьохтисячний", "п'ятитисячний", "десятитисячний", "двадцятитисячний",
  "сорокатисячний", "дев'яностотисячний", "стотисячний", "двохсоттисячний",
  "мільйонний", "трьохсотий", "чотирьохсотий", "шестисотий";
- Polish: M. Jagodziński, "Liczebniki" ("2000. – dwutysięczny", "2100. – dwa
  tysiące setny", "1 500 000. – milion pięćsettysięczny", "3459. – trzy
  tysiące czterysta pięćdziesiąty dziewiąty"); zpe.gov.pl "Odmiana liczebnika"
  ("tysiąc osiemsetny"); en.wiktionary "trzytysięczny", "pięciotysięczny",
  "dziesięciotysięczny", "jedenastotysięczny", "dwudziestotysięczny",
  "stutysięczny", "pięćsettysięczny"; pl.wiktionary "czterotysięczny",
  "ośmiotysięczny", "czterdziestotysięczny", "dwusetny", "pięćsetny",
  "milionowy", "miliardowy"; the joining forms "dwudziestojedno-", "dwustu-",
  "trzystu-", "czterystu-" from pl.wiktionary "dwudziestojednoletni",
  "dwustuletni", "trzystuletni", "czterystuletni";
- Czech: IJP ÚJČ "tisící" ("tisící dvoustý padesátý druhý" = 1252.),
  "třítisící" ("třítisící dvoustý padesátý první" = 3251.), "stotisící",
  "miliontý", "dvoustý", "třístý" ("třístý třicátý devátý" = 339.),
  "čtyřstý", "pětistý", "devítistý"; SSČ at IJP "dvoustý" ("dvou~ v slož.",
  the joining form of "dvě"); cs.wiktionary "tisící devítistý třicátý
  šestý" and its feminine and neuter forms; IJP "miliardtý" ("čísl. řad.
  k miliarda"; SSČ "miliarda ... tisíc milionů", 10^9 in the Czech long
  scale) and cs.wiktionary "bilion" (10^12); the IJP chapter "Tvoření a
  psaní výrazů složených z číslic a slov" ("42letý (= čtyřicetidvouletý i
  dvaačtyřicetiletý)", "27denní (= dvacetisedmidenní i
  sedmadvacetidenní)") for the tens-first joined stem.
"""
import unittest

from ovos_number_parser import pronounce_number, pronounce_ordinal
from ovos_number_parser.numbers_cs import pronounce_ordinal_cs
from ovos_number_parser.util import GrammaticalGender, Scale

F = GrammaticalGender.FEMININE
N = GrammaticalGender.NEUTRAL

CASES = {
    "ru": {
        2000: "двухтысячный",
        3000: "трёхтысячный",
        4000: "четырёхтысячный",
        5000: "пятитысячный",
        10000: "десятитысячный",
        20000: "двадцатитысячный",
        25000: "двадцатипятитысячный",
        35000: "тридцатипятитысячный",
        40000: "сорокатысячный",
        90000: "девяностотысячный",
        100000: "стотысячный",
        200000: "двухсоттысячный",
        500000: "пятисоттысячный",
        1000000: "миллионный",
        2000000: "двухмиллионный",
        38000000: "тридцативосьмимиллионный",
        21000000: "двадцатиодномиллионный",
        1000000000: "миллиардный",
    },
    "uk": {
        300: "трьохсотий",
        400: "чотирьохсотий",
        600: "шестисотий",
        2000: "двохтисячний",
        3000: "трьохтисячний",
        4000: "чотирьохтисячний",
        5000: "п'ятитисячний",
        10000: "десятитисячний",
        20000: "двадцятитисячний",
        40000: "сорокатисячний",
        90000: "дев'яностотисячний",
        100000: "стотисячний",
        200000: "двохсоттисячний",
        1000000: "мільйонний",
    },
    "pl": {
        200: "dwusetny",
        500: "pięćsetny",
        1800: "tysiąc osiemsetny",
        2000: "dwutysięczny",
        2100: "dwa tysiące setny",
        3000: "trzytysięczny",
        3459: "trzy tysiące czterysta pięćdziesiąty dziewiąty",
        4000: "czterotysięczny",
        5000: "pięciotysięczny",
        8000: "ośmiotysięczny",
        10000: "dziesięciotysięczny",
        11000: "jedenastotysięczny",
        20000: "dwudziestotysięczny",
        40000: "czterdziestotysięczny",
        100000: "stutysięczny",
        500000: "pięćsettysięczny",
        1000000: "milionowy",
        1500000: "milion pięćsettysięczny",
        1000000000: "miliardowy",
        21000: "dwudziestojednotysięczny",
        200000: "dwustutysięczny",
        300000: "trzystutysięczny",
        400000: "czterystutysięczny",
    },
    "cs": {
        200: "dvoustý",
        300: "třístý",
        339: "třístý třicátý devátý",
        400: "čtyřstý",
        500: "pětistý",
        900: "devítistý",
        1252: "tisící dvoustý padesátý druhý",
        1936: "tisící devítistý třicátý šestý",
        2000: "dvoutisící",
        3000: "třítisící",
        3251: "třítisící dvoustý padesátý první",
        100000: "stotisící",
        1000000: "miliontý",
        25000: "dvacetipětitisící",
        10 ** 9: "miliardtý",
        2 * 10 ** 9: "dvoumiliardtý",
        10 ** 12: "biliontý",
    },
}


class TestOrdinalScaleWords(unittest.TestCase):

    def test_ordinals_flag(self):
        for lang, cases in CASES.items():
            for number, expected in cases.items():
                with self.subTest(lang=lang, number=number):
                    self.assertEqual(
                        pronounce_number(number, lang, ordinals=True), expected)

    def test_pronounce_ordinal(self):
        for lang in ("uk", "pl", "cs"):
            for number, expected in CASES[lang].items():
                with self.subTest(lang=lang, number=number):
                    self.assertEqual(pronounce_ordinal(number, lang), expected)

    def test_czech_scale(self):
        # Czech defaults to the long scale; an explicit scale reaches both
        # entry points alike
        self.assertEqual(pronounce_ordinal_cs(2 * 10 ** 9), "dvoumiliardtý")
        for scale in Scale:
            with self.subTest(scale=scale):
                self.assertEqual(
                    pronounce_ordinal(2 * 10 ** 9, "cs", scale=scale),
                    pronounce_number(2 * 10 ** 9, "cs", ordinals=True,
                                     scale=scale))

    def test_czech_gender_reaches_every_word(self):
        self.assertEqual(pronounce_ordinal(1936, "cs", gender=F),
                         "tisící devítistá třicátá šestá")
        self.assertEqual(pronounce_ordinal(1936, "cs", gender=N),
                         "tisící devítisté třicáté šesté")


if __name__ == "__main__":
    unittest.main()
