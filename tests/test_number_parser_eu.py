import unittest

from ovos_number_parser import (extract_number, pronounce_number,
                                 pronounce_ordinal, is_ordinal, is_fractional)
from ovos_number_parser.numbers_eu import (extract_number_eu,
                                           pronounce_number_eu,
                                           pronounce_ordinal_eu,
                                           is_ordinal_eu)


class TestBasquePronounce(unittest.TestCase):
    """Anchors for spoken Basque numbers."""

    def test_pronounce_number(self):
        expected = {0: 'zero', 1: 'bat', 2: 'bi', 3: 'hiru', 4: 'lau', 5: 'bost', 6: 'sei', 7: 'zazpi', 8: 'zortzi', 9: 'bederatzi', 10: 'hamar', 11: 'hamaika', 12: 'hamabi', 13: 'hamahiru', 14: 'hamalau', 15: 'hamabost', 16: 'hamasei', 17: 'hamazazpi', 18: 'hemezortzi', 19: 'hemeretzi', 20: 'hogei', 21: 'hogeita bat', 30: 'hogeita hamar', 42: 'berrogeita bi', 50: 'berrogeita hamar', 66: 'hirurogeita sei', 70: 'hirurogeita hamar', 80: 'laurogei', 90: 'laurogeita hamar', 99: 'laurogeita hemeretzi', 100: 'ehun', 101: 'ehun eta bat', 123: 'ehun eta hogeita hiru', 200: 'berrehun', 500: 'bostehun', 999: 'bederatziehun eta laurogeita hemeretzi', 1000: 'mila', 2000: 'bi mila', 2023: 'bi mila eta hogeita hiru', 1000000: 'milioi bat', 2000000: 'bi milioi'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="eu"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'minus zazpi', -42: 'minus berrogeita bi', 2.5: 'bi koma bost', 3.14: 'hiru koma bat lau', -3.5: 'minus hiru koma bost', 0.5: 'zero koma bost'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="eu"), spoken)


class TestBasqueLargeNumbers(unittest.TestCase):
    """Cardinals above the thousand are composed with the vigesimal eta rule.

    Forms are cited to Euskaltzaindia Araua 7 ("Zenbakien idazkeraz", 1994):
    the -ehun hundreds (never -rehun), the eta-drop before a lower remainder,
    and the head-final "milioi bat" idiom.
    """

    def test_pronounce_large(self):
        expected = {
            1000: 'mila',
            1001: 'mila eta bat',
            1200: 'mila eta berrehun',          # eta kept before bare hundreds
            1202: 'mila berrehun eta bi',        # eta drops before lower remainder
            1936: 'mila bederatziehun eta hogeita hamasei',
            12345: 'hamabi mila hirurehun eta berrogeita bost',
            1000000: 'milioi bat',
            2000000: 'bi milioi',
            1000000000: 'bilioi bat',
        }
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="eu"), spoken)


class TestBasqueOrdinals(unittest.TestCase):
    """Ordinals take -garren; cited to Araua 18 ("Ordinalen ... idazkera", 1994)."""

    def test_pronounce_ordinal(self):
        expected = {
            1: 'lehenengo',        # suppletive, no -garren
            2: 'bigarren',
            5: 'bosgarren',        # bost -> bos- (not *bostgarren)
            10: 'hamargarren',
            16: 'hamaseigarren',
            20: 'hogeigarren',
            100: 'ehungarren',
        }
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_ordinal(number, lang="eu"), spoken)

    def test_is_ordinal(self):
        self.assertEqual(is_ordinal("hamaseigarren", lang="eu"), 16)
        self.assertEqual(is_ordinal("bosgarren", lang="eu"), 5)
        self.assertEqual(is_ordinal("lehenengo", lang="eu"), 1)
        self.assertFalse(is_ordinal("katua", lang="eu"))


class TestBasqueExtract(unittest.TestCase):
    """Anchors for extracting numbers from Basque text."""

    def test_extract_number(self):
        expected = {0: 'zero', 1: 'bat', 2: 'bi', 3: 'hiru', 4: 'lau', 5: 'bost', 6: 'sei', 7: 'zazpi', 8: 'zortzi', 9: 'bederatzi', 10: 'hamar', 11: 'hamaika', 12: 'hamabi', 13: 'hamahiru', 14: 'hamalau', 15: 'hamabost', 16: 'hamasei', 17: 'hamazazpi', 18: 'hemezortzi', 19: 'hemeretzi', 20: 'hogei', 21: 'hogeita bat', 30: 'hogeita hamar', 42: 'berrogeita bi', 50: 'berrogeita hamar', 66: 'hirurogeita sei', 70: 'hirurogeita hamar', 80: 'laurogei', 90: 'laurogeita hamar', 99: 'laurogeita hemeretzi', 100: 'ehun', 101: 'ehun eta bat', 123: 'ehun eta hogeita hiru', 200: 'berrehun', 500: 'bostehun', 999: 'bederatziehun eta laurogeita hemeretzi', 1000: 'mila', 2000: 'bi mila', 2023: 'bi mila eta hogeita hiru', 1000000: 'milioi bat', 2000000: 'bi milioi'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="eu"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'minus zazpi', -42: 'minus berrogeita bi', 2.5: 'bi koma bost', 3.14: 'hiru koma bat lau', -3.5: 'minus hiru koma bost', 0.5: 'zero koma bost'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="eu"), number)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number('hogeita bat katu ditut', lang="eu"),
                         21)

    def test_no_number(self):
        self.assertIn(extract_number("kaixo zer moduz", lang="eu"), (False, None))


class TestBasqueRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000, 1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 1000000, 2000000]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="eu")
                self.assertEqual(extract_number(spoken, lang="eu"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="eu")
                self.assertEqual(extract_number(spoken, lang="eu"), number)


class TestBasqueScaleComposition(unittest.TestCase):
    """Extraction of multi-word cardinals where a scale word (mila, milioi)
    follows a group that must multiply it, or a running total that must be
    added to. Forms are the verified pronounce_number output (Araua 7)."""

    def test_thousand_plus_hundreds(self):
        # "mila ehun ..." is 1000 + 100, not 1000 * 100
        expected = {
            1100: 'mila eta ehun',
            1101: 'mila ehun eta bat',
            1150: 'mila ehun eta berrogeita hamar',
            1199: 'mila ehun eta laurogeita hemeretzi',
            1200: 'mila eta berrehun',
        }
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="eu"), spoken)
                self.assertEqual(extract_number(spoken, lang="eu"), number)

    def test_hundreds_times_thousand(self):
        # "(ehun eta bat) mila" is 101 * 1000
        expected = {
            21000: 'hogeita bat mila',
            21802: 'hogeita bat mila zortziehun eta bi',
            101000: 'ehun eta bat mila',
            123456: 'ehun eta hogeita hiru mila laurehun eta '
                    'berrogeita hamasei',
        }
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="eu"), spoken)
                self.assertEqual(extract_number(spoken, lang="eu"), number)

    def test_millions_head_plus_remainder(self):
        expected = {
            1000001: 'milioi bat eta bat',
            1001000: 'milioi bat eta mila',
            1002982: 'milioi bat bi mila bederatziehun eta laurogeita bi',
            1500000: 'milioi bat eta bostehun mila',
            2500000: 'bi milioi eta bostehun mila',
        }
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="eu"), spoken)
                self.assertEqual(extract_number(spoken, lang="eu"), number)


class TestBasqueSentences(unittest.TestCase):
    """Numbers embedded in natural, agglutinative Basque utterances."""

    def test_sentences(self):
        cases = {
            'berrogeita hamar euro ordaindu ditut': 50,
            'mila bederatziehun eta laurogeita hamar urtean': 1990,
            'ehun eta hogeita hiru orrialde ditu liburuak': 123,
            'hirurogeita hamar kilometro daude hemendik': 70,
            'bi mila eta hogeita hiru urtea': 2023,
        }
        for text, number in cases.items():
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="eu"), number)

    def test_case_and_whitespace_insensitive(self):
        self.assertEqual(extract_number("HOGEI", lang="eu"), 20)
        self.assertEqual(extract_number("Hogeita Bat", lang="eu"), 21)
        self.assertEqual(extract_number("  hamar  ", lang="eu"), 10)


class TestBasqueAdversarial(unittest.TestCase):
    """Malformed / empty / junk input must not crash and must not invent
    numbers."""

    def test_empty_and_junk(self):
        for text in ["", "   ", "kaixo zer moduz", "eta", "minus",
                     "hogeitabat"]:
            with self.subTest(text=text):
                self.assertIn(extract_number(text, lang="eu"), (False, None))

    def test_junk_around_number(self):
        self.assertEqual(extract_number("xyz 123 abc", lang="eu"), 123)


class TestBasqueCardinalSweep(unittest.TestCase):
    """pronounce -> extract must round-trip across the whole 0..1_000_000
    range (dense below 2_100, then sampled)."""

    def test_round_trip_sweep(self):
        numbers = list(range(0, 2101)) + list(range(2101, 1_000_001, 997))
        for number in numbers:
            spoken = pronounce_number_eu(number)
            self.assertEqual(extract_number_eu(spoken), number,
                             f"{number} spoken as {spoken!r}")


class TestBasqueOrdinalSweep(unittest.TestCase):
    """pronounce_ordinal -> is_ordinal must round-trip."""

    def test_ordinal_round_trip(self):
        for number in range(1, 1001):
            spoken = pronounce_ordinal_eu(number)
            self.assertEqual(is_ordinal_eu(spoken), number,
                             f"{number} spoken as {spoken!r}")

    def test_is_ordinal_rejects_junk(self):
        for text in ["", "garren", "katua", "hogei"]:
            with self.subTest(text=text):
                self.assertFalse(is_ordinal_eu(text))


class TestBasqueFractions(unittest.TestCase):
    """Basque fraction nouns, including capitalized forms."""

    def test_basic(self):
        self.assertEqual(is_fractional("erdi", lang="eu"), 0.5)
        self.assertEqual(is_fractional("heren", lang="eu"), 1.0 / 3)
        self.assertEqual(is_fractional("laurden", lang="eu"), 0.25)
        self.assertEqual(is_fractional("ehunen", lang="eu"), 0.01)

    def test_capitalized_input_does_not_crash(self):
        self.assertEqual(is_fractional("Erdi", lang="eu"), 0.5)
        self.assertEqual(is_fractional("LAURDEN", lang="eu"), 0.25)
        self.assertEqual(is_fractional("Ehunen", lang="eu"), 0.01)

    def test_non_fraction_returns_false(self):
        for word in ["", "kaixo", "bost"]:
            with self.subTest(word=word):
                self.assertFalse(is_fractional(word, lang="eu"))


if __name__ == "__main__":
    unittest.main()
