import unittest

from ovos_number_parser import extract_number, pronounce_number, pronounce_ordinal, is_fractional


class TestWestFrisianPronounce(unittest.TestCase):
    """Anchors for spoken West Frisian numbers."""

    def test_pronounce_number(self):
        expected = {0: 'nul', 1: 'ien', 2: 'twa', 3: 'trije', 4: 'fjouwer',
                    5: 'fiif', 6: 'seis', 7: 'sân', 8: 'acht', 9: 'njoggen',
                    10: 'tsien', 11: 'alve', 12: 'tolve', 13: 'trettjin',
                    14: 'fjirtjin', 15: 'fyftjin', 16: 'sechstjin',
                    17: 'santjin', 18: 'achttjin', 19: 'njoggentjin',
                    20: 'tweintich', 21: 'ienentweintich', 30: 'tritich',
                    42: 'twaenfjirtich', 50: 'fyftich', 66: 'seisensechstich',
                    70: 'santich', 80: 'tachtich', 90: 'njoggentich',
                    99: 'njoggenennjoggentich', 100: 'ienhûndert',
                    200: 'twahûndert', 500: 'fiifhûndert',
                    999: 'njoggenhûndertnjoggenennjoggentich',
                    1000: 'ientûzen', 2000: 'twatûzen',
                    2023: 'twatûzentrijeentweintich',
                    1000000: 'ien miljoen ', 2000000: 'twa miljoen '}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="fy"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'min sân', -42: 'min twaenfjirtich',
                    2.5: 'twa komma fiif nul nul',
                    3.14: 'trije komma ien fjouwer nul',
                    -3.5: 'min trije komma fiif nul nul',
                    0.5: 'nul komma fiif nul nul'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="fy"), spoken)

    def test_pronounce_ordinal(self):
        expected = {1: 'earste', 2: 'twadde', 3: 'tredde', 4: 'fjirde',
                    5: 'fyfte', 6: 'sechste', 7: 'sânde', 8: 'achtste',
                    9: 'njoggende', 10: 'tsiende', 11: 'alfde', 12: 'tolfde',
                    13: 'trettjinde', 20: 'tweintichste',
                    21: 'ienentweintichste'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_ordinal(number, lang="fy"), spoken)

    def test_pronounce_ordinal_zero(self):
        # zeroth previously raised KeyError in the compound branch; it now
        # takes the regular suffix like the sibling Dutch "nulste"
        self.assertEqual(pronounce_ordinal(0, lang="fy"), "nulste")


class TestWestFrisianExtract(unittest.TestCase):
    """Anchors for extracting numbers from West Frisian text."""

    def test_extract_number(self):
        expected = {1: 'ien', 2: 'twa', 3: 'trije', 4: 'fjouwer', 5: 'fiif',
                    6: 'seis', 7: 'sân', 8: 'acht', 9: 'njoggen', 10: 'tsien',
                    11: 'alve', 12: 'tolve', 13: 'trettjin', 14: 'fjirtjin',
                    15: 'fyftjin', 16: 'sechstjin', 17: 'santjin',
                    18: 'achttjin', 19: 'njoggentjin', 20: 'tweintich',
                    21: 'ienentweintich', 30: 'tritich', 42: 'twaenfjirtich',
                    100: 'hûndert', 1000: 'tûzen',
                    123: 'ienhûnderttrijeentweintich',
                    1000000: 'ien miljoen'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="fy"), number)

    def test_extract_variant_spellings(self):
        # non-etymological variants without -s- and plain-ASCII spellings
        self.assertEqual(extract_number("sechtjin", lang="fy"), 16)
        self.assertEqual(extract_number("sechtich", lang="fy"), 60)
        self.assertEqual(extract_number("san", lang="fy"), 7)
        self.assertEqual(extract_number("hundert", lang="fy"), 100)

    def test_extract_from_sentence(self):
        self.assertEqual(
            extract_number('ik haw ienentweintich katten', lang="fy"), 21)

    def test_is_fractional(self):
        self.assertEqual(is_fractional("heal", lang="fy"), 0.5)
        self.assertEqual(is_fractional("kwart", lang="fy"), 0.25)
        self.assertEqual(is_fractional("tredde", lang="fy"), 1.0 / 3)
        self.assertFalse(is_fractional("hynder", lang="fy"))

    def test_no_number(self):
        self.assertIn(extract_number("hoi hoe giet it", lang="fy"),
                      (False, None))


class TestWestFrisianRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        numbers = list(range(0, 200)) + [
            201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 1000,
            1001, 1234, 2000, 2023, 5000, 9999, 10000, 100000, 1000000,
            2000000]
        for number in numbers:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="fy")
                self.assertEqual(extract_number(spoken, lang="fy"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, 2.5, 3.14, -3.5, 0.5]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="fy")
                self.assertEqual(extract_number(spoken, lang="fy"), number)

    def test_round_trip_negative_millions_with_remainder(self):
        # the negative marker only reaches the first scale group, so the
        # trailing groups of "min ... miljoen ..." must still inherit the sign
        for number in [-1500000, -1225280, -2540830, -5443013, -6634040,
                       -1001710]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="fy")
                self.assertEqual(extract_number(spoken, lang="fy"), number)


if __name__ == "__main__":
    unittest.main()
