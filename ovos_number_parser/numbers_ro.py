from ovos_number_parser.util import (Scale, GrammaticalGender, NumberVocabulary,
                                     RomanceNumberExtractor)

# feminine forms of the words that mark gender, applied token by token
_FEMININE_FORMS = {
    # cardinals
    "unu": "una",
    "doi": "două",
    "doisprezece": "douăsprezece",
    # ordinals
    "primul": "prima",
    "unulea": "una",
    "doilea": "doua",
    "treilea": "treia",
    "patrulea": "patra",
    "cincilea": "cincea",
    "șaselea": "șasea",
    "șaptelea": "șaptea",
    "optulea": "opta",
    "nouălea": "noua",
    "zecelea": "zecea",
    "sutălea": "suta",
    "miilea": "mia",
    "milionulea": "milioana",
    "miliardulea": "miliarda",
}

_MASCULINE_FORMS = {v: k for k, v in _FEMININE_FORMS.items()}

_PLURAL_FORMS = {
    "sută": "sute",
    "mie": "mii",
    "milion": "milioane",
    "miliard": "miliarde",
    "bilion": "bilioane",
    "biliard": "biliarde",
    "trilion": "trilioane",
    "jumătate": "jumătăți",
    "sfert": "sferturi",
    "pătrime": "pătrimi",
}


def _swap_token_ro(word: str, gender: GrammaticalGender) -> str:
    if gender == GrammaticalGender.FEMININE:
        if word in _FEMININE_FORMS:
            return _FEMININE_FORMS[word]
        # regular ordinal endings: "-zecilea" -> "-zecea",
        # "-sprezecelea" -> "-sprezecea"
        if word.endswith("zecilea"):
            return word[:-len("zecilea")] + "zecea"
        if word.endswith("celea"):
            return word[:-len("celea")] + "cea"
    elif gender == GrammaticalGender.MASCULINE and word in _MASCULINE_FORMS:
        return _MASCULINE_FORMS[word]
    return word


def swap_gender_ro(word: str, gender: GrammaticalGender) -> str:
    """Swap the grammatical gender of a Romanian number word (or phrase)."""
    return " ".join(_swap_token_ro(w, gender) for w in word.split())


def pluralize_ro(word: str) -> str:
    if word in _PLURAL_FORMS:
        return _PLURAL_FORMS[word]
    # fraction nouns in "-ime" take "-imi" ("treime" -> "treimi")
    if word.endswith("ime"):
        return word[:-1] + "i"
    return word


_RO = NumberVocabulary(
    LANG="ro-RO",
    swap_gender=swap_gender_ro,
    pluralize=pluralize_ro,

    HUNDRED_PARTICLE="o sută",  # how to read "1XX"
    DENOMINATOR_PARTICLE="părți",  # for fractions X / N {PARTICLE}
    DIVIDED_BY_ZERO="împărțit la zero",
    NO_PREV_UNIT=[],
    NO_PLURAL=[],

    NUMBER_OVERFLOW="număr exagerat de mare",
    # Romanian uses the long scale: milion 10^6, miliard 10^9, bilion 10^12
    DEFAULT_SCALE=Scale.LONG,

    # "și" joins tens to units and is the only joiner that is pronounced;
    # "de" links counts of twenty and above to their scale word
    # ("douăzeci de mii") and is dropped during extraction
    JOIN_WORD=["și", "de"],
    MULTIPLICATIVE_JOIN_WORD=["de"],
    JOINER_ON_TWENTYS=True,  # "douăzeci și unu"
    JOINER_ON_HUNDREDS=False,  # "o sută douăzeci" - no joiner after hundreds
    JOINER_ON_HUNDRED_PARTICLE=False,
    JOINER_ON_THOUSANDS=False,
    JOINER_ON_SCALE_REMAINDER=False,  # "două mii unu" - remainder stands bare

    SCALE_LINKER="de",  # "douăzeci de mii", "o sută de milioane"
    MULTIPLY_HUNDREDS=True,  # "două sute" = 200
    SCALE_ONE={
        100: "o sută",
        1000: "o mie",
        10 ** 6: "un milion",
        10 ** 9: "un miliard",
        10 ** 12: "un bilion",
        10 ** 15: "un biliard",
        10 ** 18: "un trilion",
    },
    # "mie" is feminine ("două mii", "douăzeci și una de mii"); "milion",
    # "miliard" and "bilion" are neuter - masculine in the singular,
    # feminine agreement in the plural ("două milioane",
    # "douăzeci și unu de milioane")
    SCALE_GENDERS={
        1000: GrammaticalGender.FEMININE,
        10 ** 6: GrammaticalGender.NEUTRAL,
        10 ** 9: GrammaticalGender.NEUTRAL,
        10 ** 12: GrammaticalGender.NEUTRAL,
        10 ** 15: GrammaticalGender.NEUTRAL,
        10 ** 18: GrammaticalGender.NEUTRAL,
    },

    DECIMAL_MARKER=["virgulă", "virgula", ",", "."],
    NEGATIVE_SIGN=["minus"],
    UNITS={
        0: "zero",
        1: "unu",
        2: "doi",
        3: "trei",
        4: "patru",
        5: "cinci",
        6: "șase",
        7: "șapte",
        8: "opt",
        9: "nouă",
    },
    TENS={
        10: "zece",
        11: "unsprezece",
        12: "doisprezece",
        13: "treisprezece",
        14: "paisprezece",
        15: "cincisprezece",
        16: "șaisprezece",
        17: "șaptesprezece",
        18: "optsprezece",
        19: "nouăsprezece",
        20: "douăzeci",
        30: "treizeci",
        40: "patruzeci",
        50: "cincizeci",
        60: "șaizeci",
        70: "șaptezeci",
        80: "optzeci",
        90: "nouăzeci",
    },
    HUNDREDS={
        100: "o sută",
        200: "două sute",
        300: "trei sute",
        400: "patru sute",
        500: "cinci sute",
        600: "șase sute",
        700: "șapte sute",
        800: "opt sute",
        900: "nouă sute",
    },
    FRACTION={
        2: "jumătate",
        3: "treime",
        4: "sfert",
        5: "cincime",
        6: "șesime",
        7: "șeptime",
        8: "optime",
        9: "noime",
        10: "zecime",
        11: "unsprezecime",
        12: "douăsprezecime",
        13: "treisprezecime",
        14: "paisprezecime",
        15: "cincisprezecime",
        16: "șaisprezecime",
        17: "șaptesprezecime",
        18: "optsprezecime",
        19: "nouăsprezecime",
        20: "douăzecime",
        100: "sutime",
        1000: "miime",
    },
    FRACTION_FEMALE={
        4: "pătrime",  # synonym of "sfert"
    },
    FRACTION_ONE={
        2: "o jumătate",
        3: "o treime",
        4: "un sfert",
        5: "o cincime",
        6: "o șesime",
        7: "o șeptime",
        8: "o optime",
        9: "o noime",
        10: "o zecime",
        20: "o douăzecime",
        100: "o sutime",
        1000: "o miime",
    },
    # fraction nouns are feminine: "două treimi", "două jumătăți"
    FRACTION_NUMERATOR_GENDER=GrammaticalGender.FEMININE,
    # Romanian follows the long scale (DOOM, Academia Română); both maps
    # carry the same standard readings
    SHORT_SCALE={
        1000: "mie",
        10 ** 6: "milion",
        10 ** 9: "miliard",
        10 ** 12: "bilion",
        10 ** 15: "biliard",
        10 ** 18: "trilion",
    },
    LONG_SCALE={
        1000: "mie",
        10 ** 6: "milion",
        10 ** 9: "miliard",
        10 ** 12: "bilion",
        10 ** 15: "biliard",
        10 ** 18: "trilion",
    },

    GENDERED_SPELLINGS={
        GrammaticalGender.FEMININE: {
            1: "una",
            2: "două",
            12: "douăsprezece",
        },
        # neuter: masculine agreement in the singular, feminine in the plural
        GrammaticalGender.NEUTRAL: {
            2: "două",
            12: "douăsprezece",
        },
    },
    DIGIT_SPELLINGS={},
    ALT_SPELLINGS={
        # "un"/"o" - the forms of "one" used before nouns and scale words
        "un": 1,
        # bare hundreds word, for extraction ("două sute", "sute de mii")
        "sută": 100,
        "suta": 100,
        "sute": 100,
        # colloquial short teens (accepted for extraction, never pronounced)
        "unșpe": 11,
        "doișpe": 12,
        "treișpe": 13,
        "paișpe": 14,
        "cinșpe": 15,
        "cincișpe": 15,
        "șaișpe": 16,
        "șapteșpe": 17,
        "șaptișpe": 17,
        "optișpe": 18,
        "opșpe": 18,
        "nouășpe": 19,
        # uncontracted teen variants
        "patrusprezece": 14,
        "șasesprezece": 16,
    },
    # ordinals take the particle "al" (m) / "a" (f): "al doilea", "a doua"
    ORDINAL_PREFIX={
        GrammaticalGender.MASCULINE: "al",
        GrammaticalGender.FEMININE: "a",
    },
    ORDINAL_UNPREFIXED=[1],  # "primul"/"prima" stand alone
    ORDINAL_COMPOUND_CARDINAL_TENS=True,  # "al douăzeci și unulea"
    ORDINAL_COMPOUND_UNITS={1: "unulea"},  # 1st is "primul", but 21st "unulea"
    ORDINAL_UNITS={
        1: "primul",
        2: "doilea",
        3: "treilea",
        4: "patrulea",
        5: "cincilea",
        6: "șaselea",
        7: "șaptelea",
        8: "optulea",
        9: "nouălea",
    },
    ORDINAL_TENS={
        10: "zecelea",
        11: "unsprezecelea",
        12: "doisprezecelea",
        13: "treisprezecelea",
        14: "paisprezecelea",
        15: "cincisprezecelea",
        16: "șaisprezecelea",
        17: "șaptesprezecelea",
        18: "optsprezecelea",
        19: "nouăsprezecelea",
        20: "douăzecilea",
        30: "treizecilea",
        40: "patruzecilea",
        50: "cincizecilea",
        60: "șaizecilea",
        70: "șaptezecilea",
        80: "optzecilea",
        90: "nouăzecilea",
    },
    ORDINAL_HUNDREDS={
        100: "sutălea",
    },
    ORDINAL_SHORT_SCALE={
        10 ** 3: "miilea",
        10 ** 6: "milionulea",
        10 ** 9: "miliardulea",
    },
    ORDINAL_LONG_SCALE={
        10 ** 3: "miilea",
        10 ** 6: "milionulea",
        10 ** 9: "miliardulea",
    },
)

RO = RomanceNumberExtractor(_RO)
