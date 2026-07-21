import re
import warnings
from typing import Optional, Union

from ovos_number_parser.util import (convert_to_mixed_fraction, DigitPronunciation,
                                     Scale, GrammaticalGender, NumberVocabulary,
                                     RomanceNumberExtractor)

# Fraction nouns, kept for the standalone ``nice_number_ca`` helper below.
_FRACTION_STRING_CA = {
    2: 'mig',
    3: 'terç',
    4: 'quart',
    5: 'cinquè',
    6: 'sisè',
    7: 'setè',
    8: 'vuitè',
    9: 'novè',
    10: 'desè',
    11: 'onzè',
    12: 'dotzè',
    13: 'tretzè',
    14: 'catorzè',
    15: 'quinzè',
    16: 'setzè',
    17: 'dissetè',
    18: 'divuitè',
    19: 'dinovè',
    20: 'vintè',
    30: 'trentè',
    100: 'centè',
    1000: 'milè'
}

# Tens words that open a hyphenated tens-units compound. The Institut d'Estudis
# Catalans normativa (Optimot fitxa "Guionet en els numerals compostos",
# https://aplicacions.llengua.gencat.cat/llc/AppJava/index.html?action=Principal&method=detall&idFont=11676;
# Consorci per a la Normalització Lingüística "6. Els numerals",
# https://www.cpnl.cat/gramatica/24/6-els-numerals) requires a guionet between
# the tens and the units and, in the twenties, the fused conjunction "-i-":
# "vint-i-u", "trenta-dos", "quaranta-cinc".
_HYPHEN_TENS_CA = ("vint", "trenta", "quaranta", "cinquanta", "seixanta",
                   "setanta", "vuitanta", "noranta")
_HYPHEN_UNITS_CA = ("un", "una", "u", "dos", "dues", "tres", "quatre", "cinc",
                    "sis", "set", "vuit", "nou")

_TWENTY_RE_CA = re.compile(
    r"\bvint i (" + "|".join(_HYPHEN_UNITS_CA) + r")\b")
_TENS_RE_CA = re.compile(
    r"\b(" + "|".join(_HYPHEN_TENS_CA) + r") (" + "|".join(_HYPHEN_UNITS_CA) + r")\b")


def _hyphenate_ca(text: str) -> str:
    """Join spoken tens-units compounds with the normative guionet.

    The shared engine composes a tens-units group with spaces ("vint i tres",
    "quaranta dos"); Catalan writes them hyphenated ("vint-i-tres",
    "quaranta-dos"), the twenties keeping the fused "-i-". Idempotent, so it may
    run at every recursion level without harm.
    """
    text = _TWENTY_RE_CA.sub(r"vint-i-\1", text)
    text = _TENS_RE_CA.sub(r"\1-\2", text)
    return text


def swap_gender_ca(word: str, gender: GrammaticalGender) -> str:
    """Swap Catalan numeral/ordinal words between masculine and feminine.

    Handles the gendered cardinals ("un"/"una", "dos"/"dues",
    "dos-cents"/"dues-centes") and the ordinal/fraction endings
    ("cinquè"/"cinquena", "quart"/"quarta").
    """
    if gender == GrammaticalGender.FEMININE:
        if word == "un":
            return "una"
        if word == "dos":
            return "dues"
        if word == "mig":
            return "mitja"
        if "cents" in word:
            word = word.replace("cents", "centes")
            if word.startswith("dos"):
                word = "dues" + word[3:]
            return word
        if word.endswith("è"):
            return word[:-1] + "ena"       # cinquè -> cinquena, centè -> centena
        if word.endswith(("r", "n", "t", "ç")):
            return word + "a"              # primer -> primera, quart -> quarta
        return word
    # masculine: undo the feminine spellings
    if word == "una":
        return "un"
    if word == "dues":
        return "dos"
    if word == "mitja":
        return "mig"
    if "centes" in word:
        word = word.replace("centes", "cents")
        if word.startswith("dues"):
            word = "dos" + word[4:]
        return word
    if word.endswith("ena"):
        return word[:-3] + "è"
    return word


def pluralize_ca(word: str) -> str:
    """Regular Catalan plural for the scale/fraction words used here."""
    if word.endswith("ó"):
        return word[:-1] + "ons"           # milió -> milions, bilió -> bilions
    if word.endswith("è"):
        return word[:-1] + "ens"           # cinquè -> cinquens
    if word.endswith("ç"):
        return word + "os"                 # terç -> terços
    if not word.endswith("s"):
        return word + "s"                  # miliard -> miliards
    return word


_CA = NumberVocabulary(
    LANG="ca",
    swap_gender=swap_gender_ca,
    pluralize=pluralize_ca,

    HUNDRED_PARTICLE="cent",  # Catalan does not apocopate: "cent", "cent un"
    DENOMINATOR_PARTICLE="avos",
    DIVIDED_BY_ZERO="dividit per zero",
    NO_PREV_UNIT=[1000],  # "mil" not "un mil"
    NO_PLURAL=[1000],     # "dos mil" not "dos mils"

    NUMBER_OVERFLOW="número exageradament gran",
    DEFAULT_SCALE=Scale.LONG,  # 10^9 = "miliard", 10^12 = "bilió"
    JOIN_WORD=["i"],

    JOINER_ON_TWENTYS=True,       # "vint i un" (hyphenated on output)
    JOINER_ONLY_ON_TWENTYS=True,  # "trenta dos", not "trenta i dos"
    JOINER_ON_HUNDREDS=False,     # "cent vint-i-tres", "dos-cents trenta-quatre"
    JOINER_ON_THOUSANDS=False,    # "mil dos-cents"
    JOINER_ON_SCALE_REMAINDER=False,  # "dos mil vint-i-tres", not "... i ..."
    MULTIPLY_HUNDREDS=True,       # "dos cents" (from "dos-cents") = 200

    DECIMAL_MARKER=["coma", "amb", "punt", ".", ","],
    NEGATIVE_SIGN=["menys"],
    UNITS={
        0: 'zero',
        1: 'un',
        2: 'dos',
        3: 'tres',
        4: 'quatre',
        5: 'cinc',
        6: 'sis',
        7: 'set',
        8: 'vuit',
        9: 'nou',
    },
    TENS={
        10: 'deu',
        11: 'onze',
        12: 'dotze',
        13: 'tretze',
        14: 'catorze',
        15: 'quinze',
        16: 'setze',
        17: 'disset',
        18: 'divuit',
        19: 'dinou',
        20: 'vint',
        30: 'trenta',
        40: 'quaranta',
        50: 'cinquanta',
        60: 'seixanta',
        70: 'setanta',
        80: 'vuitanta',
        90: 'noranta'
    },
    HUNDREDS={
        200: 'dos-cents',
        300: 'tres-cents',
        400: 'quatre-cents',
        500: 'cinc-cents',
        600: 'sis-cents',
        700: 'set-cents',
        800: 'vuit-cents',
        900: 'nou-cents'
    },
    FRACTION={
        2: 'mig',
        3: 'terç',
        4: 'quart',
        5: 'cinquè',
        6: 'sisè',
        7: 'setè',
        8: 'vuitè',
        9: 'novè',
        10: 'desè',
        11: 'onzè',
        12: 'dotzè',
        13: 'tretzè',
        14: 'catorzè',
        15: 'quinzè',
        16: 'setzè',
        17: 'dissetè',
        18: 'divuitè',
        19: 'dinovè',
        20: 'vintè',
        30: 'trentè',
        100: 'centè',
        1000: 'milè'
    },
    FRACTION_FEMALE={
        2: 'mitja',
        3: 'terça',
        4: 'quarta'
    },
    SHORT_SCALE={
        1000: 'mil',
        10 ** 6: 'milió',
        10 ** 9: 'bilió',
        10 ** 12: 'trilió',
        10 ** 15: 'quadrilió',
        10 ** 18: 'quintilió',
        10 ** 21: 'sextilió',
        10 ** 24: 'septilió',
    },
    LONG_SCALE={
        1000: 'mil',
        10 ** 6: 'milió',
        10 ** 9: 'miliard',
        10 ** 12: 'bilió',
        10 ** 15: 'biliard',
        10 ** 18: 'trilió',
        10 ** 21: 'triliard',
        10 ** 24: 'quadrilió',
    },

    GENDERED_SPELLINGS={
        GrammaticalGender.FEMININE: {
            1: "una",
            2: "dues"
        }
    },
    DIGIT_SPELLINGS={},
    ALT_SPELLINGS={
        # standalone "u" (before nouns it becomes "un"), dialectal "huit" forms,
        # and the bare hundreds particle used inside compounds after the hyphen
        # is split off for extraction ("dos-cents" -> "dos cents")
        "u": 1,
        "huit": 8,
        "huitanta": 80,
        "cents": 100,
        "centes": 100,
    },
    ORDINAL_UNITS={
        1: 'primer',
        2: 'segon',
        3: 'tercer',
        4: 'quart',
        5: 'cinquè',
        6: 'sisè',
        7: 'setè',
        8: 'vuitè',
        9: 'novè',
    },
    ORDINAL_TENS={
        10: 'desè',
        11: 'onzè',
        12: 'dotzè',
        13: 'tretzè',
        14: 'catorzè',
        15: 'quinzè',
        16: 'setzè',
        17: 'dissetè',
        18: 'divuitè',
        19: 'dinovè',
        20: 'vintè',
        30: 'trentè',
        40: 'quarantè',
        50: 'cinquantè',
        60: 'seixantè',
        70: 'setantè',
        80: 'vuitantè',
        90: 'norantè'
    },
    ORDINAL_HUNDREDS={
        100: 'centè'
    },
    # Unit ordinals used inside a hyphenated tens-units compound. Catalan forms
    # these from the cardinal plus "-è" ("dos" -> "dosè", "quatre" -> "quatrè"),
    # which differs from the standalone ordinals for 1-4 ("primer", "segon",
    # "tercer", "quart"): "vint-i-dosè", not "vint-i-segon".
    ORDINAL_COMPOUND_UNITS={
        1: 'unè',
        2: 'dosè',
        3: 'tresè',
        4: 'quatrè',
        5: 'cinquè',
        6: 'sisè',
        7: 'setè',
        8: 'vuitè',
        9: 'novè',
    },
    ORDINAL_SHORT_SCALE={
        10 ** 3: 'milè',
        10 ** 6: 'milionè'
    },
    ORDINAL_LONG_SCALE={
        10 ** 3: 'milè',
        10 ** 6: 'milionè'
    }
)


class CatalanNumberExtractor(RomanceNumberExtractor):
    """Catalan number engine.

    Adds the Catalan-specific surface conventions the shared engine does not
    model: hyphenated tens-units compounds on output, a digit-by-digit decimal
    reading ("tres coma un quatre" for 3.14), and the ordinal composition rule
    below.
    """

    def _pronounce_ordinal_up_to_999(
            self, n: int,
            gender: GrammaticalGender = GrammaticalGender.MASCULINE) -> str:
        """Ordinal word for 0-999 following the Institut d'Estudis Catalans rule.

        Catalan ordinals are single fused words for 1-19 and the round tens/
        hundreds ("onzè", "vintè", "centè"); every larger number is written as
        the cardinal with only its final element carrying the ordinal ending.
        The masculine ending is the cardinal + "-è" and the feminine the
        cardinal + "-na" ("22è vint-i-dosè" / "22a vint-i-dosena", "54è
        cinquanta-quatrè", "353è tres-cents cinquanta-tresè"), so a tens-units
        compound keeps a cardinal tens word ("vint-i-", "trenta-") and turns
        only the unit ordinal, unlike the shared engine's tens-ordinal + unit-
        ordinal composition ("desè primer", "vintè primer") which is wrong here.

        Source: Consorci per a la Normalització Lingüística, "Els numerals
        ordinals" (reproducing the IEC / Institut d'Estudis Catalans normativa);
        Optimot fitxa "Guionet en els numerals compostos".
        """
        if not 0 <= n <= 999:
            raise ValueError("Number must be between 0 and 999.")
        if n == 0:
            return self.vocab.UNITS[0]

        parts = []
        if n >= 100:
            hundred = n // 100 * 100
            n %= 100
            if n == 0:
                # round hundred takes the ordinal ending itself:
                # "cent" -> "centè", "dos-cents" -> "dos-centè"
                word = self.vocab.ORDINAL_HUNDREDS.get(hundred) \
                    or self.vocab.HUNDREDS[hundred][:-1] + "è"
                return self.vocab.swap_gender(word, gender)
            # otherwise the hundreds stay cardinal; only the tail is ordinal
            parts.append(self.vocab.HUNDRED_PARTICLE if hundred == 100
                         else self.vocab.HUNDREDS[hundred])

        # n is now 1-99
        if n in self.vocab.ORDINAL_TENS:
            # fused single word: teens 11-19 and the round tens 20, 30 ... 90
            parts.append(self.vocab.swap_gender(self.vocab.ORDINAL_TENS[n], gender))
        elif n < 10:
            parts.append(self.vocab.swap_gender(self.vocab.ORDINAL_UNITS[n], gender))
        else:
            ten = n // 10 * 10
            unit = n % 10
            unit_word = self.vocab.swap_gender(
                self.vocab.ORDINAL_COMPOUND_UNITS[unit], gender)
            joiner = "-i-" if ten == 20 else "-"
            parts.append(f"{self.vocab.TENS[ten]}{joiner}{unit_word}")

        return " ".join(parts)

    def pronounce_number(self,
                         number: Union[int, float],
                         places: int = 5,
                         scale: Optional[Scale] = None,
                         ordinals: bool = False,
                         digits: DigitPronunciation = DigitPronunciation.DIGIT_BY_DIGIT,
                         gender: GrammaticalGender = GrammaticalGender.MASCULINE,
                         _force_hundreds_join: bool = False,
                         _under_higher_scale: bool = False) -> str:
        spoken = super().pronounce_number(number, places, scale, ordinals,
                                          digits, gender, _force_hundreds_join,
                                          _under_higher_scale)
        return _hyphenate_ca(spoken)


CA = CatalanNumberExtractor(_CA)


def nice_number_ca(number, speech, denominators=range(1, 21)):
    """ Catalan helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 i mig" for speech and "4 1/2" for text

    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """

    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        # Give up, just represent as a 3 decimal number
        return str(round(number, 3))

    whole, num, den = result

    if not speech:
        if num == 0:
            # TODO: Number grouping?  E.g. "1,000,000"
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)

    if num == 0:
        return str(whole)
    # denominador
    den_str = _FRACTION_STRING_CA[den]
    # fraccions
    if whole == 0:
        if num == 1:
            # un desè
            return_string = 'un {}'.format(den_str)
        else:
            # quatre cinquens
            return_string = '{} {}'.format(num, den_str)

    else:
        # vint i 3 desens
        return_string = '{} i {} {}'.format(whole, num, den_str)
    # plural
    if num > 1:
        if return_string[-1] == "è":
            return_string = return_string[:-1] + "ens"
        else:
            return_string += 's'
    return return_string


##################################################################
# all methods below are deprecated and only for backwards compat
##################################################################

def pronounce_number_ca(number, places=2, short_scale=False, scientific=False):
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    scale = Scale.SHORT if short_scale else Scale.LONG
    return CA.pronounce_number(number, places, scale=scale)


def is_fractional_ca(input_str, short_scale=True):
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return CA.is_fractional(input_str)


def extract_number_ca(text, short_scale=False, ordinals=False):
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    scale = Scale.SHORT if short_scale else Scale.LONG
    return CA.extract_number(text, ordinals=ordinals, scale=scale)


def numbers_to_digits_ca(utterance: str) -> str:
    """
    DEPRECATED
    """
    warnings.warn(
        "migrate to use RomanceNumberExtractor and NumberVocabulary directly instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return CA.numbers_to_digits(utterance)


if __name__ == '__main__':
    print('--- Catalan number tests ---')
    for n in (16, 21, 42, 66, 99, 100, 101, 123, 200, 500, 999, 1000, 2023,
              1_000_000, 2_000_000, 1_234_600):
        print(f'{n} ->', CA.pronounce_number(n))
    print('10^9 ->', CA.pronounce_number(10 ** 9))
    print('10^12 ->', CA.pronounce_number(10 ** 12))
    print("'vint-i-un' ->", CA.extract_number('vint-i-un'))
    print("'un milió dos-cents trenta-quatre mil sis-cents' ->",
          CA.extract_number('un milió dos-cents trenta-quatre mil sis-cents'))
