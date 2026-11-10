"""Every language reads the same value the same way.

A value below the ``places`` quantum reads up to its first significant digit,
rounded half away from zero, with its sign. A scientific mantissa rounds half
away from zero and carries into the exponent. Each expected reading comes from
a reading that does not pass through the changed code: the language's reading
of an equivalent value at enough places, integer readings of the digits, or
the reading of a value whose digits need no rounding.
"""
from decimal import Decimal
from unittest import mock

import pytest

import ovos_number_parser
from ovos_number_parser import pronounce_number
from ovos_number_parser.numbers_hu import pronounce_number_hu
from ovos_number_parser.numbers_pl import pronounce_number_pl

#: every native backend except kab, which raises for any decimal, and two
#: languages read by Unicode RBNF
LANGS = ("an", "ar", "ast", "az", "bg", "ca", "cs", "da", "de", "el", "en",
         "es", "et", "eu", "fa", "fi", "fr", "fy", "gl", "he", "hr", "hu",
         "id", "it", "ms", "mwl", "nb", "nl", "nn", "oc", "pl", "pt-PT",
         "pt-BR", "ro", "ru", "sk", "sl", "sv", "tr", "uk", "af", "ja")

#: backends with a scientific mode of their own
SCIENTIFIC_MODE = ("ar", "az", "bg", "cs", "el", "en", "fa", "he", "hr", "id",
                   "it", "ms", "pl", "ru", "sk", "sl", "tr", "uk")


def _minus(lang):
    return pronounce_number(-5, lang)[:-len(pronounce_number(5, lang))]


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("value, places, equivalent, covering", [
    (0.0004, 3, 0.0004, 4),
    (-0.0004, 3, -0.0004, 4),
    (1e-07, 3, 1e-07, 7),
    (0.00012345, 3, 0.0001, 4),
    (0.000096, 3, 0.0001, 4),
    (1.5e-05, 3, 2e-05, 5),
    (-2.5e-08, 3, -3e-08, 8),
    (0.04, 1, 0.04, 2),
    (-0.04, 1, -0.04, 2),
])
def test_value_below_the_quantum_reads_its_first_digit(
        lang, value, places, equivalent, covering):
    assert pronounce_number(value, lang, places=places) == \
        pronounce_number(equivalent, lang, places=covering)


@pytest.mark.parametrize("lang, point", [
    ("en", "point"), ("ru", "точка"), ("cs", "tečka"), ("pl", "przecinek"),
    ("it", "virgola"), ("de", "Komma"), ("el", "κόμμα"), ("es", "coma"),
])
@pytest.mark.parametrize("value, digits", [
    (0.0004, "0004"), (0.00012345, "0001"), (0.000096, "0001"),
    (-1e-07, "0000001"),
])
def test_value_below_the_quantum_composed_from_digit_words(
        lang, point, value, digits):
    expected = " ".join([pronounce_number(0, lang), point]
                        + [pronounce_number(int(d), lang) for d in digits])
    if value < 0:
        expected = _minus(lang) + expected
    assert pronounce_number(value, lang, places=3) == expected


@pytest.mark.parametrize("value, mantissa, exponent", [
    (1e-12, 1, 12), (-1.5e-12, -2, 12), (5e-324, 5, 324),
])
def test_fa_fraction_finer_than_its_denominators_reads_scientifically(
        value, mantissa, exponent):
    # fa names denominators down to 10 ** -11 and reads a larger magnitude
    # with "ضرب در ده به توان" (times ten to the power)
    expected = f"{pronounce_number(abs(mantissa), 'fa')} ضرب در ده به توان " \
               f"{_minus('fa')}{pronounce_number(exponent, 'fa')}"
    if mantissa < 0:
        expected = _minus("fa") + expected
    assert pronounce_number(value, "fa", places=3) == expected


@pytest.mark.parametrize("lang", SCIENTIFIC_MODE)
@pytest.mark.parametrize("value, rounded", [
    (123456.0, 123500.0),
    (-123456.0, -123500.0),
    (1.2346e10, 1.235e10),
    (12346 * 10 ** 396, 1235 * 10 ** 397),
    (9.9996e10, 1e11),
    (99996 * 10 ** 396, 10 ** 401),
])
def test_scientific_mantissa_rounds_with_carry(lang, value, rounded):
    # the rounded value has three mantissa decimals, so no backend rounds it
    assert pronounce_number(value, lang, places=3, scientific=True) == \
        pronounce_number(rounded, lang, places=3, scientific=True)


def _hu(whole, numerator, denominator):
    return " ".join([pronounce_number(whole, "hu"), "egész",
                     pronounce_number(numerator, "hu"), denominator])


@pytest.mark.parametrize("value, places, whole, numerator, denominator", [
    (2000.5, 2, 2000, 50, "század"),
    (3000.25, 2, 3000, 25, "század"),
    (2000000.5, 1, 2000000, 5, "tized"),
])
def test_hu_round_thousands_whole_part_has_no_hyphen(
        value, places, whole, numerator, denominator):
    expected = _hu(whole, numerator, denominator)
    assert pronounce_number(value, "hu", places=places) == expected
    assert pronounce_number(-value, "hu", places=places) == \
        _minus("hu") + expected


@pytest.mark.parametrize("value, numerator", [(0.0025, 3), (0.0045, 5)])
def test_hu_direct_call_rounds_half_up(value, numerator):
    assert pronounce_number_hu(value, 3) == _hu(0, numerator, "ezred")


@pytest.mark.parametrize("lang", ("et", "fi", "fy"))
def test_ordinal_flag_on_a_non_ordinal_value_returns_words(lang):
    assert pronounce_number(-2.0, lang, ordinals=True) == \
        _minus(lang) + pronounce_number(2, lang, ordinals=True)
    assert pronounce_number(3.5, lang, ordinals=True) == \
        pronounce_number(3.5, lang)
    assert pronounce_number(-3.5, lang, ordinals=True) == \
        pronounce_number(-3.5, lang)
    assert pronounce_number(-1e16, lang, ordinals=True) == \
        pronounce_number(-10 ** 16, lang, ordinals=True)


def test_pl_direct_call_past_the_scale_words():
    expected = pronounce_number(-10 ** 300, "pl")
    assert pronounce_number_pl(-1e300) == expected
    assert pronounce_number_pl(-10 ** 300) == expected


@pytest.mark.parametrize("lang, connective", [
    ("an", "por diez elevau a"),
    ("ca", "per deu elevat a"),
    ("es", "por diez elevado a"),
    ("pt-PT", "vezes dez elevado a"),
    # the words of the ar and ms backends under scientific=True
    ("ar", "في عشرة أس"),
    ("ms", "kali sepuluh pangkat"),
])
def test_fallback_mantissa_without_fraction_has_no_decimal_word(
        lang, connective):
    for value, mantissa in ((10 ** 400, 1), (-2 * 10 ** 400, -2)):
        assert pronounce_number(value, lang) == \
            f"{pronounce_number(mantissa, lang)} {connective} " \
            f"{pronounce_number(400, lang)}"


@pytest.mark.parametrize("lang", ("uk", "ru"))
def test_ordinal_past_the_scale_words_reads_like_the_cardinal(lang):
    for value in (10 ** 100 + 5, 10 ** 100 + 21):
        assert pronounce_number(value, lang, ordinals=True) == \
            pronounce_number(value, lang)


@pytest.mark.parametrize("value, places", [(-0.25, 3), (-0.5, 1), (-0.04, 1)])
def test_negative_fraction_dispatches_once(value, places):
    dispatch = ovos_number_parser._pronounce_number_dispatch
    with mock.patch.object(ovos_number_parser, "_pronounce_number_dispatch",
                           side_effect=dispatch) as spy:
        pronounce_number(value, "en", places=places)
    assert spy.call_count == 1


@pytest.mark.parametrize("lang", LANGS + ("kab",))
def test_scientific_flag_changes_the_reading_only_in_scientific_mode(lang):
    changed = pronounce_number(1234, lang, scientific=True) != \
        pronounce_number(1234, lang)
    assert changed == (lang in SCIENTIFIC_MODE)


#: the scientific readings of values below the default quantum before the
#: change, which read every mantissa digit
DEV_SCIENTIFIC = {
    ('ar', 1.602e-19): 'واحد فاصلة ستة صفر اثنان في عشرة أس سالب تسعة عشر',
    ('az', 1.602e-19): 'bir nöqtə altı sıfır iki vurulsun on üstü mənfi on doqquz',
    ('bg', 1.602e-19): 'едно запетая шест нула две по десет на степен минус деветнадесет',
    ('cs', 1.602e-19): 'jedna tečka šest nula dva krát deset na mocninu záporné devatenáct',
    ('el', 1.602e-19): 'ένα κόμμα έξι μηδέν δύο επί δέκα στη δύναμη του μείον δεκαεννέα',
    ('en', 1.602e-19): 'one point six zero two times ten to the power of negative nineteen',
    ('fa', 1.602e-19): 'یک و ششصد و دو هزارم ضرب در ده به توان منفی نوزده',
    ('he', 1.602e-19): 'אחת נקודה שש אפס שתיים כפול עשר בחזקת מינוס תשע עשרה',
    ('hr', 1.602e-19): 'jedan zarez šest nula dva puta deset na minus devetnaest',
    ('id', 1.602e-19): 'satu koma enam nol dua kali sepuluh pangkat minus sembilan belas',
    ('it', 1.602e-19): 'uno virgola sei zero due per dieci elevato alla meno diciannove',
    ('ms', 1.602e-19): 'satu koma enam sifar dua kali sepuluh pangkat minus sembilan belas',
    ('pl', 1.602e-19): 'jeden przecinek sześć zero dwa razy dziesięć do potęgi minus dziewiętnaście',
    ('ru', 1.602e-19): 'один точка шесть ноль два на десять в степени минус девятнадцать',
    ('sk', 1.602e-19): 'jeden celá šesť nula dva krát desať na mocninu mínus devätnásť',
    ('sl', 1.602e-19): 'ena cela šest nič dve krat deset na minus devetnajst',
    ('tr', 1.602e-19): 'bir virgül altı sıfır iki çarpı on üzeri eksi on dokuz',
    ('uk', 1.602e-19): "один крапка шість нуль два на десять у ступені мінус дев'ятнадцять",
    ('ar', 6.022e-23): 'ستة فاصلة صفر اثنان اثنان في عشرة أس سالب ثلاثة وعشرون',
    ('az', 6.022e-23): 'altı nöqtə sıfır iki iki vurulsun on üstü mənfi iyirmi üç',
    ('bg', 6.022e-23): 'шест запетая нула две две по десет на степен минус двадесет и три',
    ('cs', 6.022e-23): 'šest tečka nula dva dva krát deset na mocninu záporné dvacet tři',
    ('el', 6.022e-23): 'έξι κόμμα μηδέν δύο δύο επί δέκα στη δύναμη του μείον είκοσι τρία',
    ('en', 6.022e-23): 'six point zero two two times ten to the power of negative twenty three',
    ('fa', 6.022e-23): 'شش و بیست و دو هزارم ضرب در ده به توان منفی بیست و سه',
    ('he', 6.022e-23): 'שש נקודה אפס שתיים שתיים כפול עשר בחזקת מינוס עשרים ושלוש',
    ('hr', 6.022e-23): 'šest zarez nula dva dva puta deset na minus dvadeset tri',
    ('id', 6.022e-23): 'enam koma nol dua dua kali sepuluh pangkat minus dua puluh tiga',
    ('it', 6.022e-23): 'sei virgola zero due due per dieci elevato alla meno ventitré',
    ('ms', 6.022e-23): 'enam koma sifar dua dua kali sepuluh pangkat minus dua puluh tiga',
    ('pl', 6.022e-23): 'sześć przecinek zero dwa dwa razy dziesięć do potęgi minus dwadzieścia trzy',
    ('ru', 6.022e-23): 'шесть точка ноль два два на десять в степени минус двадцать три',
    ('sk', 6.022e-23): 'šesť celá nula dva dva krát desať na mocninu mínus dvadsaťtri',
    ('sl', 6.022e-23): 'šest celih nič dve dve krat deset na minus triindvajset',
    ('tr', 6.022e-23): 'altı virgül sıfır iki iki çarpı on üzeri eksi yirmi üç',
    ('uk', 6.022e-23): 'шість крапка нуль два два на десять у ступені мінус двадцять три',
    ('ar', 0.00015): 'واحد فاصلة خمسة في عشرة أس سالب أربعة',
    ('az', 0.00015): 'bir nöqtə beş vurulsun on üstü mənfi dörd',
    ('bg', 0.00015): 'едно запетая пет по десет на степен минус четири',
    ('cs', 0.00015): 'jedna tečka pět krát deset na mocninu záporné čtyři',
    ('el', 0.00015): 'ένα κόμμα πέντε επί δέκα στη δύναμη του μείον τέσσερα',
    ('en', 0.00015): 'one point five times ten to the power of negative four',
    ('fa', 0.00015): 'یک و نیم ضرب در ده به توان منفی چهار',
    ('he', 0.00015): 'אחת נקודה חמש כפול עשר בחזקת מינוס ארבע',
    ('hr', 0.00015): 'jedan zarez pet puta deset na minus četiri',
    ('id', 0.00015): 'satu koma lima kali sepuluh pangkat minus empat',
    ('it', 0.00015): 'uno virgola cinque per dieci elevato alla meno quattro',
    ('ms', 0.00015): 'satu koma lima kali sepuluh pangkat minus empat',
    ('pl', 0.00015): 'jeden przecinek pięć razy dziesięć do potęgi minus cztery',
    ('ru', 0.00015): 'один точка пять на десять в степени минус четыре',
    ('sk', 0.00015): 'jeden celá päť krát desať na mocninu mínus štyri',
    ('sl', 0.00015): 'ena cela pet krat deset na minus štiri',
    ('tr', 0.00015): 'bir virgül beş çarpı on üzeri eksi dört',
    ('uk', 0.00015): "один крапка п'ять на десять у ступені мінус чотири",
}


@pytest.mark.parametrize("lang, value", list(DEV_SCIENTIFIC))
def test_scientific_value_below_the_quantum_keeps_its_mantissa(lang, value):
    assert pronounce_number(value, lang, scientific=True) == \
        DEV_SCIENTIFIC[lang, value]


@pytest.mark.parametrize("lang", SCIENTIFIC_MODE)
@pytest.mark.parametrize("value, rounded", [
    (12.3449, 12.34),
    (0.012344, 0.01234),
    (-0.012344, -0.01234),
    (0.0012345, 0.001235),
    (1.2345, 1.235),
    (0.0015, 0.0015),
])
def test_scientific_mantissa_rounds_once(lang, value, rounded):
    # the rounded value has at most three mantissa decimals, so at six places
    # no backend rounds it
    assert pronounce_number(value, lang, places=3, scientific=True) == \
        pronounce_number(rounded, lang, places=6, scientific=True)


#: the scientific connective, from each language's own scientific reading
CONNECTIVES = {
    "en": "times ten to the power of",
    "es": "por diez elevado a",
    "pt-PT": "vezes dez elevado a",
    "de": "mal zehn hoch",
    "fr": "fois dix puissance",
    "ar": "في عشرة أس",
}


@pytest.mark.parametrize("lang", CONNECTIVES)
@pytest.mark.parametrize("value, mantissa, exponent", [
    (Decimal("1E-5000"), 1, -5000),
    (Decimal("-1E-400"), -1, -400),
    (Decimal("-7.6E-400"), -8, -400),
    (5e-324, 5, -324),
])
def test_value_past_the_float_range_reads_scientifically(
        lang, value, mantissa, exponent):
    assert pronounce_number(value, lang) == " ".join([
        pronounce_number(mantissa, lang), CONNECTIVES[lang],
        pronounce_number(exponent, lang)])


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("value", ["-1E-300", "2.5E-12", "-0.00012"])
def test_decimal_in_the_float_range_reads_like_the_float(lang, value):
    assert pronounce_number(Decimal(value), lang) == \
        pronounce_number(float(value), lang)


@pytest.mark.parametrize("lang", LANGS)
def test_first_digit_at_the_last_decimal_reads_in_full(lang):
    assert pronounce_number(9e-323, lang, places=3) == \
        pronounce_number(9e-323, lang, places=323)


@pytest.mark.parametrize("value, places, expected", [
    # superessive of the ordinals: Wiktionary "huszonötödik",
    # "huszonnyolcadik", "harmincadik", "ezredik"; adverbs: Wiktionary
    # "Module:number list/data/hu"
    (7e-25, 3, "hétszer tíz a mínusz huszonötödiken"),
    (4e-25, 24, "négyszer tíz a mínusz huszonötödiken"),
    (9.6e-29, 3, "egyszer tíz a mínusz huszonnyolcadikon"),
    (-7e-30, 3, "mínusz hétszer tíz a mínusz harmincadikon"),
    (Decimal("-1E-1000"), 3, "mínusz egyszer tíz a mínusz ezrediken"),
])
def test_hu_value_finer_than_its_denominators(value, places, expected):
    assert pronounce_number(value, "hu", places=places) == expected


def test_hu_direct_call_finer_than_its_denominators():
    assert pronounce_number_hu(7e-26, 30) == \
        "hétszer tíz a mínusz huszonhatodikon"
