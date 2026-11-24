import unittest

import pytest

from ovos_number_parser import pronounce_number, pronounce_ordinal


class TestCroatianRoundOrdinals(unittest.TestCase):

    @pytest.mark.xfail(strict=True, reason="https://github.com/OpenVoiceOS/ovos-number-parser/issues/576")
    def test_a_round_thousand_has_an_ordinal(self):
        # the exact form is not cited; the call must answer, and not with the cardinal
        spoken = pronounce_ordinal(2000, "hr")
        self.assertIsInstance(spoken, str)
        self.assertNotEqual(spoken, pronounce_number(2000, "hr"))
