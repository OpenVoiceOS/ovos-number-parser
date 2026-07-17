"""Edge-path tests for the generic language fallbacks."""
import unittest

from ovos_number_parser import numbers_to_digits


class TestGenericNumbersToDigitsEdges(unittest.TestCase):
    def test_adjacent_bare_numbers_sum(self):
        # the shared Romance engine accumulates adjacent bare numbers
        # ("cinque tre" = 5 + 3), exactly as it does for es/ca
        out = numbers_to_digits("cinque tre", "it")
        self.assertEqual(out, "8")

    def test_e_is_not_a_cardinal_conjunction(self):
        # standard Italian cardinals carry no conjunction ("venticinque", never
        # "venti e cinque"), so "e" separates two numbers instead of joining
        # them and numbers_to_digits converts each on its own
        out = numbers_to_digits("due e tre", "it")
        self.assertEqual(out, "2 e 3")

    def test_decimal_marker_not_merged(self):
        # "virgola" is not a connector: both numbers convert separately
        out = numbers_to_digits("cinque virgola due chili", "it")
        self.assertEqual(out, "5 virgola 2 chili")


class TestPerLanguageNumbersToDigits(unittest.TestCase):
    def test_hungarian(self):
        self.assertEqual(numbers_to_digits("huszonöt macska", "hu"),
                         "25 macska")
        self.assertEqual(
            numbers_to_digits("kétezer-ötszáz forint", "hu"), "2500 forint")

    def test_slovenian(self):
        self.assertEqual(numbers_to_digits("petindvajset mačk", "sl"),
                         "25 mačk")
        self.assertEqual(
            numbers_to_digits("dva tisoč tristo evrov", "sl"), "2300 evrov")

    def test_rerouted_natives(self):
        # these languages previously converted nothing above twenty or
        # mishandled comma-grouped scales
        self.assertEqual(numbers_to_digits("veintiuno gatos", "es"),
                         "21 gatos")
        self.assertEqual(
            numbers_to_digits("dos mil quinientos euros", "es"),
            "2500 euros")
        self.assertEqual(numbers_to_digits("vint-i-un gats", "ca"),
                         "21 gats")
        self.assertEqual(
            numbers_to_digits("two thousand, five hundred dollars", "en"),
            "2500 dollars")
        self.assertEqual(numbers_to_digits("éénentwintig katten", "nl"),
                         "21 katten")
        self.assertEqual(
            numbers_to_digits("totusindefemhundrede kroner", "da"),
            "2500 kroner")


if __name__ == "__main__":
    unittest.main()
