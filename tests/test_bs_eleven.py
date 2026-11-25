import unittest

import pytest

from ovos_number_parser import pronounce_number


class TestBosnianEleven(unittest.TestCase):
    # Serbo-Croatian "jedànaēst": https://en.wiktionary.org/wiki/jedanaest

    @pytest.mark.xfail(strict=True, reason="https://github.com/OpenVoiceOS/ovos-number-parser/issues/589")
    def test_eleven_is_jedanaest(self):
        self.assertEqual(pronounce_number(11, "bs"), "jedanaest")
        self.assertEqual(pronounce_number(111, "bs"), "sto jedanaest")

    def test_croatian_eleven_keeps_its_spelling(self):
        self.assertEqual(pronounce_number(11, "hr"), "jedanaest")
        self.assertEqual(pronounce_number(12, "bs"), "dvanaest")
