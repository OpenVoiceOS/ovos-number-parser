from ovos_number_parser.util import (Scale, GrammaticalGender, NumberVocabulary, RomanceNumberExtractor)


def swap_gender_ast(word: str, gender: GrammaticalGender) -> str:
    """Swap ordinal/adjective endings between masculine and feminine where applicable.

    For Asturian, ordinals typically end in -u (masc.) and -a (fem.).
    """
    if gender == GrammaticalGender.FEMININE:
        if word.endswith('o'): # neuter
            return word[:-1] + 'a'
        if word.endswith('u'): # masculine
            return word[:-1] + 'a'
        if word.endswith('os'): # plural masculine
            return word[:-2] + 'as'
    else:
        # NOTE: need a native speaker to review, does neuter apply to numbers?
        #if word.endswith('o'): # neuter
        #    return word[:-1] + 'u'
        if word.endswith('a'): # feminine
            return word[:-1] + 'u'
        if word.endswith('es'): # plural neuter
            return word[:-2] + 'os'
    return word


def pluralize_ast(word: str):
    if word.endswith("ón"):
        return word[:-2] + "ones"
    if word.endswith("a"):
        return word[:-1] + "es"
    if word.endswith("u"):
        return word[:-1] + "os"
    if not word.endswith("s"):
        return word + "s"
    return word


_AST = NumberVocabulary(
    LANG="ast",
    swap_gender=swap_gender_ast,  # used for female forms
    pluralize=pluralize_ast,  # use for plural forms

    HUNDRED_PARTICLE="ciento",  # how to read "1XX"
    DENOMINATOR_PARTICLE="avos",  # for fractions  X / N {PARTICLE}
    DIVIDED_BY_ZERO="a dividir por zero",  # how to read X/0 values
    NO_PREV_UNIT=[100, 1000],  # "mil" vs "um mil"  / "cem" vs "um cem"
    NO_PLURAL=[1000],  # "dois mil" vs "dois mils" / "dois milhões" vs "dois milhão"

    NUMBER_OVERFLOW="número exageradamente grande",
    DEFAULT_SCALE=Scale.LONG,
    JOIN_WORD=["y"],

    JOINER_ON_TWENTYS=True,  # add JOIN_WORD from 20-30 - "vinte e um"
    JOINER_ON_HUNDREDS=False,  # add JOIN_WORD from 100-1000 - "duzentos e um"
    JOINER_ON_THOUSANDS=False,  # add JOIN_WORD from 1000-10000 - "mil e duzentos"

    DECIMAL_MARKER=["punto", "coma", ".", ","],
    NEGATIVE_SIGN=["menos"],
    UNITS={
        0: 'cero',
        1: 'un',
        2: 'dos',
        3: 'tres',
        4: 'cuatro',
        5: 'cinco',
        6: 'seis',
        7: 'siete',
        8: 'ocho',
        9: 'nueve'
    },
    TENS={
        10: 'diez',
        11: 'once',
        12: 'doce',
        13: 'trece',
        14: 'catorce',
        15: 'quince',
        16: 'dieciséis',
        17: 'diecisiete',
        18: 'dieciocho',
        19: 'diecinueve',
        20: 'venti',
        21: 'ventiún',
        22: 'ventidós',
        23: 'ventitrés',
        24: 'venticuatro',
        25: 'venticinco',
        26: 'ventiséis',
        27: 'ventisiete',
        28: 'ventiocho',
        29: 'ventinueve',
        30: 'trenta',
        40: 'cuarenta',
        50: 'cincuenta',
        60: 'sesenta',
        70: 'setenta',
        80: 'ochenta',
        90: 'noventa'
    },
    HUNDREDS={
        100: 'cien',
        200: 'doscientos',
        300: 'trescientos',
        400: 'cuatrocientos',
        500: 'quinientos',
        600: 'seiscientos',
        700: 'setecientos',
        800: 'ochocientos',
        900: 'novecientos'
    },
    FRACTION={
        2: 'mediu',
        3: 'terciu',
        4: 'cuartu',
        5: 'quintu',
        6: 'sestu',
        7: 'séptimu',
        8: 'octavu',
        9: 'novenu',
        10: 'décimu',
        11: 'onceavos',
        12: 'doceavos'
    },
    FRACTION_FEMALE={
        2: "media"  # una y media -> 1.5
    },
    SHORT_SCALE={
        10 ** 6: "millón",
        10 ** 3: "mil"
    },
    LONG_SCALE={
        10 ** 6: "millón",
        10 ** 3: "mil"
    },

    GENDERED_SPELLINGS={
        GrammaticalGender.FEMININE: {
            1: "una"
        }
    },
    DIGIT_SPELLINGS={},
    ALT_SPELLINGS={
        "unu": 1,
        "oito": 8,  # https://en.wiktionary.org/wiki/ocho#Asturian
        "otso": 8,
        "uechu": 8,  # medieval form
        "dolce": 12,
        "selce": 16,  # https://en.wiktionary.org/wiki/diecis%C3%A9is#Asturian
        "ventiuno": 21,

        # ordinals with spanish influenced alt forms
        'decimoprimeru': 11,
        "decimosegundu": 12,
        "decimoterceru": 13,
        "decimocuartu": 14,
        "decimoquintu": 15,
        'ventésimu': 20,
        'trentésimu': 30,
    },
    ORDINAL_UNITS={
        1: 'primeru',
        2: 'segundu',
        3: 'terceru',
        4: 'cuartu',
        5: 'quintu',
        6: 'sestu',
        7: 'séptimu',
        8: 'octavu',
        9: 'novenu'
    },
    ORDINAL_TENS={
        10: 'décimu',
        11: 'oncenu',
        12: 'docenu',
        13: 'trecenu',
        14: 'catorcenu',
        15: 'quincenu',
        16: 'decimosestu',
        17: 'decimoséptimu',
        18: 'decimoctavu',
        19: 'decimonovenu',
        20: 'ventenu',
        30: 'trentenu',
        40: 'cuarentenu',
        50: 'cincuentenu',
        60: 'sesentenu',
        70: 'setentenu',
        80: 'ochentenu',
        90: 'noventenu'
    },
    ORDINAL_HUNDREDS={
        100: 'centésimu',
        200: "doscientesimu",
        300: "trescientesimu",
        400: "cuatrocientesimu",
        500: "quinientesimu",
        600: "seiscientesimu",
        700: "setecientesimu",
        800: "ochocientesimu",
        900: "novecientesimu"
    },
    ORDINAL_SHORT_SCALE={
        10 ** 3: "milésimu",
        10 ** 6: "millonésimu",
        10 ** 9: "billonésimu",
        10 ** 12: "trillonésimu",
        10 ** 15: "cuatrillonésimu",
        10 ** 18: "quintillonésimu",
        10 ** 21: "sextillonésimu",
    },
    ORDINAL_LONG_SCALE={
        10 ** 3: "milésimu",
        10 ** 6: "millonésimu",
        10 ** 12: "billonésimu",
        10 ** 18: "trillonésimu",
        10 ** 24: "cuatrillonésimu",
        10 ** 30: "quintillonésimu",
        10 ** 36: "sextillonésimu",
    }
)

AST = RomanceNumberExtractor(_AST)

if __name__ == '__main__':
    print('--- Asturian number tests ---')
    print('16 ->', AST.pronounce_number(16))
    print('21 ->', AST.pronounce_number(21))
    print('35 ->', AST.pronounce_number(35))
    print('101 ->', AST.pronounce_number(101))
    print('1,234 ->', AST.pronounce_number(1234))
    print('1,000,000 ->', AST.pronounce_number(1_000_000))

    print('\n--- Ordinals ---')
    print('1st (m):', AST.pronounce_ordinal(1))
    print('1st (f):', AST.pronounce_ordinal(1, GrammaticalGender.FEMININE))
    print('23rd (m):', AST.pronounce_ordinal(23))
    print('100th:', AST.pronounce_ordinal(100))

    print('\n--- Extraction ---')
    print("'un millón' ->", AST.extract_number('un millón'))
    print("'dos millones trescientos' ->", AST.extract_number('dos millones trescientos'))
    print("'ventiuno' ->", AST.extract_number('ventiuno'))
    print("'tres cuartos' (fraction word) ->", AST.extract_number('tres cuartos'))

    print('\n--- numbers_to_digits ---')
    print(AST.numbers_to_digits('hai dos millones cincuenta persoas'))
    print(AST.numbers_to_digits('merquei ventiuno panes'))
