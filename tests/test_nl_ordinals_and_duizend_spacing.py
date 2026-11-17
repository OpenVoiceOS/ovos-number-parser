"""Dutch ordinals follow the last part of the number; a space follows "duizend".

Sources: Taaladvies.net, "Aaneenschrijven van telwoorden (algemeen)"
(https://taaladvies.net/aaneenschrijven-van-telwoorden/): "Na het woord
duizend (en samenstellingen hiermee, zoals vierduizend) staat een spatie"
(4002 "vierduizend twee", 28 064 "achtentwintigduizend vierenzestig"), "Miljoen
en miljard zijn altijd aparte woorden", and for ordinals "3220e drieduizend
tweehonderdtwintigste", "4 000 000e vier miljoenste"; Onze Taal,
"Honderdeneende / honderdeneerste" ("In samengestelde rangtelwoorden ga je van
het laatste deel uit": "honderdeneerste", the form "honderdeerste" is correct
as well); Wiktionary nl "eerste", "derde", "achtste", "miljoenste".

The oracle below spells numbers from word lists, one digit group at a time,
and takes the ordinal ending from the last word of the cardinal. The gold
table is written by hand from the sources.
"""
import random
import unittest

from ovos_number_parser import extract_number, pronounce_number, \
    pronounce_ordinal

GOLD_ORDINALS = {
    1: "eerste", 2: "tweede", 3: "derde", 4: "vierde", 7: "zevende",
    8: "achtste", 9: "negende", 10: "tiende", 12: "twaalfde",
    19: "negentiende", 20: "twintigste", 21: "eenentwintigste",
    23: "drieëntwintigste", 38: "achtendertigste", 100: "honderdste",
    101: "honderdeerste", 102: "honderdtweede", 103: "honderdderde",
    108: "honderdachtste", 110: "honderdtiende", 111: "honderdelfde",
    135: "honderdvijfendertigste", 203: "tweehonderdderde",
    1000: "duizendste", 1001: "duizend eerste", 1003: "duizend derde",
    1008: "duizend achtste", 1100: "duizend honderdste",
    3220: "drieduizend tweehonderdtwintigste",
    4002: "vierduizend tweede", 6028: "zesduizend achtentwintigste",
    100000: "honderdduizendste", 1000000: "miljoenste",
    2000000: "twee miljoenste", 4000000: "vier miljoenste",
    4400000: "vier miljoen vierhonderdduizendste",
    1000000000: "miljardste",
    1000001: "één miljoen eerste",
    1001000000: "één miljard één miljoenste",
}

GOLD_CARDINALS = {
    101: "honderdeen", 1000: "duizend", 1001: "duizend een",
    1135: "duizend honderdvijfendertig", 2022: "tweeduizend tweeëntwintig",
    4002: "vierduizend twee", 6028: "zesduizend achtentwintig",
    28064: "achtentwintigduizend vierenzestig",
    100000: "honderdduizend", 115000: "honderdvijftienduizend",
    271850: "tweehonderdeenenzeventigduizend achthonderdvijftig",
    1000000: "één miljoen", 3000000: "drie miljoen",
    5200000000: "vijf miljard tweehonderd miljoen",
    347625728221: "driehonderdzevenenveertig miljard zeshonderdvijfentwintig "
                  "miljoen zevenhonderdachtentwintigduizend "
                  "tweehonderdeenentwintig",
}

UNITS = ["", "een", "twee", "drie", "vier", "vijf", "zes", "zeven", "acht",
         "negen", "tien", "elf", "twaalf", "dertien", "veertien", "vijftien",
         "zestien", "zeventien", "achttien", "negentien"]
TENS = ["", "", "twintig", "dertig", "veertig", "vijftig", "zestig",
        "zeventig", "tachtig", "negentig"]
LAST_WORD_ORDINAL = {  # ending of the cardinal -> ending of the ordinal
    "een": "eerste", "drie": "derde", "acht": "achtste"}


def below_100(n):
    if n < 20:
        return UNITS[n]
    unit, ten = UNITS[n % 10], TENS[n // 10]
    if not unit:
        return ten
    glue = "ën" if unit in ("twee", "drie") else "en"
    return unit + glue + ten


def below_1000(n):
    head = ""
    if n >= 100:
        head = ("" if n // 100 == 1 else UNITS[n // 100]) + "honderd"
    return head + below_100(n % 100)


def oracle_cardinal(n):
    if n == 1:
        return "één"
    words = []
    for scale, name in ((10 ** 9, "miljard"), (10 ** 6, "miljoen")):
        count, n = divmod(n, scale)
        if count:
            words.append(("één" if count == 1 else below_1000(count)) +
                         " " + name)
    thousands, rest = divmod(n, 1000)
    if thousands:
        words.append("duizend" if thousands == 1
                     else below_1000(thousands) + "duizend")
    if rest:
        words.append(below_1000(rest))
    return " ".join(words)


def oracle_ordinal(n):
    if n == 1:
        return "eerste"
    cardinal = oracle_cardinal(n)
    if cardinal == "één miljoen" or cardinal == "één miljard":
        return cardinal.split(" ")[1] + "ste"
    for ending, ordinal in LAST_WORD_ORDINAL.items():
        if cardinal.endswith(ending) and not cardinal.endswith(
                ("tien", "negen", "zeven")):
            return cardinal[:-len(ending)] + ordinal
    last = cardinal.split(" ")[-1]
    ends_in_small = any(last.endswith(w) for w in UNITS[2:20] if w) \
        and not last.endswith(("tig", "honderd", "duizend"))
    return cardinal + ("de" if ends_in_small else "ste")


def boundary_numbers():
    numbers = set(range(1, 3001))
    tails = [0, 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 18, 19, 20, 21, 23, 28,
             99, 100, 101, 102, 103, 108, 110, 113, 199, 200, 999]
    heads = [1, 2, 3, 8, 10, 11, 20, 21, 100, 101, 108, 999]
    for tail in tails:
        for head in heads:
            numbers.add(head * 1000 + tail)
            numbers.add(head * 10 ** 6 + tail)
            numbers.add(head * 10 ** 6 + head * 1000 + tail)
    for power in range(0, 10):
        for base in (1, 2, 3):
            for delta in (-1, 0, 1):
                numbers.add(base * 10 ** power + delta)
    numbers.add(10 ** 9)
    numbers.update(random.Random(5).randrange(1, 10 ** 9)
                   for _ in range(3000))
    return sorted(n for n in numbers if 1 <= n <= 10 ** 9)


class TestGold(unittest.TestCase):
    def test_ordinals(self):
        for number, expected in GOLD_ORDINALS.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_ordinal(number, "nl-nl"), expected)

    def test_cardinals(self):
        for number, expected in GOLD_CARDINALS.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, "nl-nl"), expected)


class TestSweep(unittest.TestCase):
    NUMBERS = boundary_numbers()

    def test_sweep_size(self):
        self.assertGreater(len(self.NUMBERS), 4000)

    def test_cardinals_match_the_oracle(self):
        for number in self.NUMBERS:
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, "nl-nl"),
                                 oracle_cardinal(number))

    def test_ordinals_match_the_oracle(self):
        for number in self.NUMBERS:
            with self.subTest(number=number):
                self.assertEqual(pronounce_ordinal(number, "nl-nl"),
                                 oracle_ordinal(number))

    def test_no_stray_spaces_and_cardinals_below_a_million_read_back(self):
        for number in [n for n in self.NUMBERS if n < 10 ** 6]:
            spoken = pronounce_number(number, "nl-nl")
            with self.subTest(number=number):
                self.assertEqual(spoken, spoken.strip())
                self.assertNotIn("  ", spoken)
                self.assertEqual(extract_number(spoken, "nl-nl"), number)


class TestReadBackAfterDuizend(unittest.TestCase):
    """The extractor joins the words that a space separates after "duizend"."""

    ROWS = [("tweeduizend een", 2001),
            ("tweeduizend een komma vijf", 2001.5),
            ("duizend honderd vijftig", 1150),
            ("tweeduizend drie honderd", 2300),
            ("tweeduizend vijf honderd", 2500),
            ("drieduizend twee honderd vijftig", 3250),
            ("drieduizend tweehonderd vijftig", 3250),
            ("één miljoen tweeduizend drie", 1002003),
            # a number word of 1000 or more never joins
            ("tweeduizend vierduizend", 4000),
            ("vijfduizend tweehonderdduizend", 200000),
            # the article "een" before a noun stays out of the number
            ("tweeduizend een maand", 1),
            ("tweeduizend twee auto's", 2002)]

    def test_rows(self):
        for text, expected in self.ROWS:
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, "nl-nl"), expected)


class TestOracleAgreesWithGold(unittest.TestCase):
    """The oracle is checked against the hand-written gold first."""

    def test_oracle(self):
        for number, expected in GOLD_ORDINALS.items():
            with self.subTest(ordinal=number):
                self.assertEqual(oracle_ordinal(number), expected)
        for number, expected in GOLD_CARDINALS.items():
            with self.subTest(cardinal=number):
                self.assertEqual(oracle_cardinal(number), expected)


if __name__ == "__main__":
    unittest.main()
