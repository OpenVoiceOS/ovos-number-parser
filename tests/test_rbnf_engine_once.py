import ovos_number_parser
from ovos_number_parser import pronounce_number


def test_a_locale_parses_its_rule_file_once():
    ovos_number_parser._rbnf_engine.cache_clear()
    spoken = [pronounce_number(n, "bs") for n in (22, 22, 35)]
    assert spoken == ["dvadeset dva", "dvadeset dva", "trideset pet"]
    assert ovos_number_parser._rbnf_engine.cache_info().misses == 1
