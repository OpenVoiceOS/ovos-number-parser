import unittest

from ovos_number_parser.numbers_el import (extract_number_el,
                                           pronounce_number_el)


class TestGreekScaleComposition(unittest.TestCase):
    """A bare scale word following a larger scale must continue the number:
    added when descending ("εκατομμύριο χίλια"), multiplied when the smaller
    scale precedes a larger one ("χίλια δισεκατομμύρια")."""

    def test_million_plus_bare_thousand(self):
        self.assertEqual(
            extract_number_el("ένα εκατομμύριο χίλια επτακόσια δέκα"), 1001710)

    def test_thousand_times_billion(self):
        self.assertEqual(extract_number_el("χίλια δισεκατομμύρια"),
                         1000000000000)

    def test_regular_composition_unchanged(self):
        self.assertEqual(
            extract_number_el("δύο εκατομμύρια τριακόσιες χιλιάδες"), 2300000)
        self.assertEqual(extract_number_el("χίλια"), 1000)

    def test_round_trip_million_boundary(self):
        for number in [1001710, 4001978, 7001935, -1001710, 1001000,
                       1000001, 1234567, 1000000000000]:
            with self.subTest(number=number):
                spoken = pronounce_number_el(number)
                self.assertEqual(extract_number_el(spoken), number)


if __name__ == "__main__":
    unittest.main()
