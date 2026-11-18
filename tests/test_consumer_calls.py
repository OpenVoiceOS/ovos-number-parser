"""The calls that consumers of the package make, with the answers they need.

simple_NER passes ``numbers_to_digits(text, lang)`` to ovos-date-parser
``extract_datetime`` (``simple_NER/annotators/temporal_ner.py``), so a clock
time has to keep its half hour. ovos-ha-pipeline calls ``extract_number`` on
the whole utterance (``NumberKeyword.match``), so a unit word after a count
must leave the count alone.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits


class TestClockTimeKeepsItsHalfHour(unittest.TestCase):
    def test_numbers_to_digits(self):
        # German "halb drei" is half an hour before three, 2:30; French "et
        # demie" and Galician "e media" after an hour are its half hour
        for text, lang, expected in (
                ("um halb drei", "de-DE", "um 2:30"),
                ("weck mich um halb drei", "de-DE", "weck mich um 2:30"),
                ("à cinq heures et demie", "fr-FR", "à 5 heures et demie"),
                ("dans deux heures et demie", "fr-FR", "dans 2 heures et demie"),
                ("ás cinco e media", "gl-ES", "ás 5 e media")):
            with self.subTest(lang=lang, text=text):
                self.assertEqual(numbers_to_digits(text, lang), expected)


class TestUnitAfterACount(unittest.TestCase):
    def test_seconds(self):
        # "secondi" and "segons" are the unit "seconds" after a count
        for text, lang, expected in (
                ("dieci secondi", "it-IT", 10),
                ("trenta secondi", "it-IT", 30),
                ("tra dieci secondi", "it-IT", 10),
                ("vint segons", "ca-ES", 20),
                ("trenta segons", "ca-ES", 30),
                ("d aquí a vint segons", "ca-ES", 20)):
            with self.subTest(lang=lang, text=text):
                self.assertEqual(extract_number(text, lang), expected)


class TestPronouncedThousands(unittest.TestCase):
    def test_a_thousand_and_its_rest(self):
        # pronounce_number(1001, "en") is "one thousand, one"
        for text, lang, expected in (
                ("one thousand, one", "en-US", 1001),
                ("two thousand, twenty three", "en-US", 2023),
                ("mil e un segundos", "gl-ES", 1001)):
            with self.subTest(lang=lang, text=text):
                self.assertEqual(extract_number(text, lang), expected)


if __name__ == "__main__":
    unittest.main()
