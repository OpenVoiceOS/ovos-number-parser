from ovos_number_parser.util import (Scale, GrammaticalGender, NumberVocabulary, RomanceNumberExtractor)


def swap_gender_an(word: str, gender: GrammaticalGender) -> str:
    """Swap ordinal/adjective endings between masculine and feminine.

    Aragonese ordinals end in -o (masc.) and -a (fem.): primero/primera,
    cuatreno/cuatrena.
    """
    if gender == GrammaticalGender.FEMININE:
        if word.endswith('o'):
            return word[:-1] + 'a'
        if word.endswith('os'):
            return word[:-2] + 'as'
    else:
        if word.endswith('a'):
            return word[:-1] + 'o'
        if word.endswith('as'):
            return word[:-2] + 'os'
    return word


def pluralize_an(word: str):
    if word.endswith("ón"):
        return word[:-2] + "ones"
    if not word.endswith("s"):
        return word + "s"
    return word


_AN = NumberVocabulary(
    LANG="an",
    swap_gender=swap_gender_an,  # used for female forms
    pluralize=pluralize_an,  # used for plural forms

    HUNDRED_PARTICLE="ciento",  # how to read "1XX" - "ciento vinte"
    DENOMINATOR_PARTICLE="avos",  # for fractions  X / N {PARTICLE}
    DIVIDED_BY_ZERO="dividiu por zero",  # how to read X/0 values
    NO_PREV_UNIT=[100, 1000],  # "mil" not "un mil" / "cient" not "un cient"
    NO_PLURAL=[1000],  # "dos mil" not "dos mils"

    NUMBER_OVERFLOW="numero exageradament gran",
    DEFAULT_SCALE=Scale.LONG,
    JOIN_WORD=["y"],

    JOINER_ON_TWENTYS=True,  # 21-29 have fused spellings, joiner kept for extraction
    JOINER_ON_HUNDREDS=False,  # "ciento trenta", "docientos vintiún"
    JOINER_ON_THOUSANDS=False,  # "mil docientos"

    DECIMAL_MARKER=["coma", "punto", ".", ","],
    NEGATIVE_SIGN=["menos"],
    UNITS={
        0: 'zero',
        1: 'un',
        2: 'dos',
        3: 'tres',
        4: 'cuatre',
        5: 'cinco',
        6: 'seis',
        7: 'siet',
        8: 'ueito',
        9: 'nueu'
    },
    TENS={
        10: 'diez',
        11: 'once',
        12: 'doce',
        13: 'trece',
        14: 'catorze',
        15: 'quince',
        16: 'deciséis',
        17: 'decisiet',
        18: 'deciueito',
        19: 'decinueu',
        20: 'vinte',
        21: 'vintiún',
        22: 'vintidós',
        23: 'vintitrés',
        24: 'vinticuatre',
        25: 'vinticinco',
        26: 'vintiséis',
        27: 'vintisiet',
        28: 'vintiueito',
        29: 'vintinueu',
        30: 'trenta',
        40: 'cuaranta',
        50: 'cincuanta',
        60: 'sixanta',
        70: 'setanta',
        80: 'uitanta',
        90: 'novanta'
    },
    HUNDREDS={
        100: 'cient',
        200: 'docientos',
        300: 'trecientos',
        400: 'cuatrecientos',
        500: 'cincocientos',
        600: 'seicientos',
        700: 'sietecientos',
        800: 'uitcientos',
        900: 'noucientos'
    },
    FRACTION={
        2: 'meyo',
        3: 'tercio',
        4: 'cuarto'
    },
    FRACTION_FEMALE={
        2: "meya"  # una y meya -> 1.5
    },
    SHORT_SCALE={
        10 ** 3: "mil",
        10 ** 6: "millón"
    },
    LONG_SCALE={
        10 ** 3: "mil",
        10 ** 6: "millón"
    },

    GENDERED_SPELLINGS={
        GrammaticalGender.FEMININE: {
            1: "una"
        }
    },
    DIGIT_SPELLINGS={},
    ALT_SPELLINGS={
        # dialectal / variant spellings kept for extraction only
        "uno": 1,
        "quatre": 4,
        "quatro": 4,
        "cuatro": 4,
        "cinc": 5,
        "sies": 6,
        "sieis": 6,
        "siete": 7,
        "set": 7,
        "ueit": 8,
        "güeito": 8,
        "nou": 9,
        "deu": 10,
        "dotse": 12,
        "dotze": 12,
        "tretse": 13,
        "tretze": 13,
        "catorce": 14,
        "sece": 16,
        "setse": 16,
        "decisiete": 17,
        "decinou": 19,
        "vint": 20,
        "vente": 20,
        "vintiuno": 21,
        "ventiún": 21,
        "ventiuno": 21,
        "ventidós": 22,
        "ventitrés": 23,
        "cuarenta": 40,
        "quaranta": 40,
        "quarenta": 40,
        "cinquanta": 50,
        "sisanta": 60,
        "sesenta": 60,
        "setenta": 70,
        "noranta": 90,
        "cien": 100,
        "cent": 100,
        "ciento": 100
    },
    ORDINAL_UNITS={
        1: 'primero',
        2: 'segundo',
        3: 'tercero',
        4: 'cuatreno',
        5: 'cinqueno',
        6: 'seiseno',
        7: 'seteno',
        8: 'uiteno',
        9: 'noveno'
    },
    ORDINAL_TENS={
        10: 'deceno',
        11: 'onceno',
        12: 'doceno',
        13: 'treceno',
        14: 'catorzeno',
        15: 'quinceno',
        16: 'deciseiseno',
        17: 'decisieteno',
        18: 'deciueiteno',
        19: 'decinoveno',
        20: 'venteno',
        30: 'trenteno',
        40: 'cuaranteno',
        50: 'cincuanteno',
        60: 'sixanteno',
        70: 'setanteno',
        80: 'uitanteno',
        90: 'novanteno'
    },
    ORDINAL_HUNDREDS={
        100: 'centeno'
    },
    ORDINAL_SHORT_SCALE={
        10 ** 3: "mileno"
    },
    ORDINAL_LONG_SCALE={
        10 ** 3: "mileno"
    }
)

AN = RomanceNumberExtractor(_AN)

if __name__ == '__main__':
    print('--- Aragonese number tests ---')
    print('16 ->', AN.pronounce_number(16))
    print('21 ->', AN.pronounce_number(21))
    print('35 ->', AN.pronounce_number(35))
    print('101 ->', AN.pronounce_number(101))
    print('1,234 ->', AN.pronounce_number(1234))
    print('1,000,000 ->', AN.pronounce_number(1_000_000))

    print('\n--- Ordinals ---')
    print('1st (m):', AN.pronounce_ordinal(1))
    print('1st (f):', AN.pronounce_ordinal(1, GrammaticalGender.FEMININE))
    print('4th (m):', AN.pronounce_ordinal(4))
    print('11th:', AN.pronounce_ordinal(11))

    print('\n--- Extraction ---')
    print("'un millón' ->", AN.extract_number('un millón'))
    print("'trenta y cinco' ->", AN.extract_number('trenta y cinco'))
    print("'vintiún' ->", AN.extract_number('vintiún'))

    print('\n--- numbers_to_digits ---')
    print(AN.numbers_to_digits('bi ha docientos cincuanta personas'))
