"""Slovak cardinals and ordinals below a million are written as one word.

Pravidlá slovenského pravopisu (JÚĽŠ SAV, 3rd ed. 2000): "Dovedna sa píšu
číslovky v základnom tvare, napr. pätnásť, dvadsaťsedem, stojeden,
sedemstodvadsať, tisícpäť, sedemtisícdesať." and "Číslovky označujúce stovky
a tisícky sa píšu spolu, napr. dvesto, sedemsto, tritisíc, dvadsaťsedemtisíc,
stoosemdesiatdvatisíc. Spolu sa píšu aj radové číslovky zložené z jednotiek,
stovák a tisícok, napr. stoprvý, dvetisícdruhý. Číslovky označujúce milióny,
miliardy, bilióny sa píšu oddelene".

Jazyková poradňa JÚĽŠ: "Číslo a počet 2 000 sa vyjadruje nesklonnou základnou
číslovkou dvetisíc".
"""
import unittest

from ovos_number_parser import pronounce_number, pronounce_ordinal


class TestSlovakSolidCardinals(unittest.TestCase):
    CASES = {
        101: "stojeden",
        123: "stodvadsaťtri",
        1000: "tisíc",
        1005: "tisícpäť",
        2000: "dvetisíc",
        2024: "dvetisícdvadsaťštyri",
        2500: "dvetisícpäťsto",
        3000: "tritisíc",
        7010: "sedemtisícdesať",
        27000: "dvadsaťsedemtisíc",
        182000: "stoosemdesiatdvatisíc",
        2000000: "dva milióny",
        5000000: "päť miliónov",
        2003000: "dva milióny tritisíc",
    }

    def test_cardinals(self):
        for value, spoken in self.CASES.items():
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "sk"), spoken)


class TestSlovakSolidOrdinals(unittest.TestCase):
    CASES = {
        101: "stoprvý",
        124: "stodvadsiaty štvrtý",
        1985: "tisícdeväťstoosemdesiaty piaty",
        2002: "dvetisícdruhý",
    }

    def test_ordinals(self):
        for value, spoken in self.CASES.items():
            with self.subTest(value=value):
                self.assertEqual(pronounce_ordinal(value, "sk"), spoken)


if __name__ == "__main__":
    unittest.main()
