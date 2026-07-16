"""Occitan number vocabulary.

Classical orthography (norma classica), Lengadocian referential variety.

Sources:
- Lo Congrès permanent de la lenga occitana, dicod'Òc (https://dicodoc.eu)
- "How to count in Occitan", languagesandnumbers.com/how-to-count-in-occitan
- Wiktionary Occitan numeral and ordinal entries
  (en.wiktionary.org/wiki/Category:Occitan_numerals,
   fr.wiktionary.org/wiki/Catégorie:Ordinaux_en_occitan)

Notes on the grammar encoded below:
- 17-19 and 21-29 join with "-e-" (dètz-e-sèt, vint-e-un); from 31 upward the
  ten and the unit are simply juxtaposed (trenta dos, cinquanta sèt).
- hundreds are analytic: dos cents, tres cents ... nòu cents.
- "mila" (thousand) is invariable and never takes a preceding "un".
- Occitan uses the long scale (milion, miliard).
"""
from ovos_number_parser.util import (Scale, GrammaticalGender, NumberVocabulary,
                                     RomanceNumberExtractor)

_FEM_SPECIAL = {"un": "una", "dos": "doas", "mièg": "mièja"}
_MASC_SPECIAL = {v: k for k, v in _FEM_SPECIAL.items()}


def swap_gender_oc(word: str, gender: GrammaticalGender) -> str:
    """Swap an Occitan numeral/ordinal between grammatical genders.

    Feminine forms of ordinals add -a to the consonant-final masculine
    (primièr/primièra, segond/segonda, tresen/tresena).
    """
    if gender == GrammaticalGender.FEMININE:
        if word in _FEM_SPECIAL:
            return _FEM_SPECIAL[word]
        if word.endswith("ièr") or word.endswith("en") \
                or word in ("segond", "quart", "tèrç"):
            return word + "a"
    elif gender == GrammaticalGender.MASCULINE:
        if word in _MASC_SPECIAL:
            return _MASC_SPECIAL[word]
        if word.endswith("ièra") or word.endswith("ena") or word.endswith("onda"):
            return word[:-1]
    return word


def pluralize_oc(word: str) -> str:
    """Pluralize an Occitan word (sibilant-final words take -es)."""
    if word.endswith("ç"):
        return word[:-1] + "ces"  # tèrç -> tèrces
    if word.endswith("ch") or word.endswith("x"):
        return word + "es"
    if not word.endswith("s"):
        return word + "s"
    return word


# compound ordinals keep the cardinal ten and put the -en suffix on the unit:
# vint-e-unen (21st), trenta dosen (32nd); "unen"/"dosen" are the compound
# unit ordinals (standalone 1st/2nd are primièr/segond)
_ORDINAL_COMPOUND_UNITS = {1: 'unen', 2: 'dosen', 3: 'tresen', 4: 'quatren',
                           5: 'cinquen', 6: 'seisen', 7: 'seten', 8: 'ochen',
                           9: 'noven'}
_CARDINAL_TENS = {20: 'vint', 30: 'trenta', 40: 'quaranta', 50: 'cinquanta',
                  60: 'seissanta', 70: 'setanta', 80: 'ochanta', 90: 'nonanta'}
_ORDINAL_COMPOUNDS = {
    ten + unit: f"{_CARDINAL_TENS[ten]}{'-e-' if ten == 20 else ' '}{word}"
    for ten in _CARDINAL_TENS
    for unit, word in _ORDINAL_COMPOUND_UNITS.items()
}


_OC = NumberVocabulary(
    LANG="oc-FR",
    swap_gender=swap_gender_oc,
    pluralize=pluralize_oc,

    HUNDRED_PARTICLE="cent",  # 1XX reads "cent vint"
    DENOMINATOR_PARTICLE="parts",
    DIVIDED_BY_ZERO="dividit per zèro",
    NO_PREV_UNIT=[100, 1000],  # "cent" / "mila", never "un cent" / "un mila"
    NO_PLURAL=[1000],  # "mila" is invariable: "dos mila"

    NUMBER_OVERFLOW="nombre tròp grand",
    DEFAULT_SCALE=Scale.LONG,
    JOIN_WORD=["e"],

    JOINER_ON_TWENTYS=True,  # vint-e-un
    JOINER_ONLY_ON_TWENTYS=True,  # but "trenta dos", "cinquanta sèt"
    PREFER_EXPLICIT_ORDINALS=True,  # onzen, vint-e-unen
    MULTIPLY_HUNDREDS=True,  # analytic hundreds: "dos cents" = 200
    JOINER_ON_HUNDREDS=False,  # "dos cents trenta"
    JOINER_ON_HUNDRED_PARTICLE=False,  # "cent vint"
    JOINER_ON_THOUSANDS=False,  # "mila dos cents"

    DECIMAL_MARKER=["virgula", "punt", ".", ","],
    NEGATIVE_SIGN=["mens"],
    UNITS={
        0: 'zèro',
        1: 'un',
        2: 'dos',
        3: 'tres',
        4: 'quatre',
        5: 'cinc',
        6: 'sièis',
        7: 'sèt',
        8: 'uèch',
        9: 'nòu',
    },
    TENS={
        10: 'dètz',
        11: 'onze',
        12: 'dotze',
        13: 'tretze',
        14: 'catòrze',
        15: 'quinze',
        16: 'setze',
        17: 'dètz-e-sèt',
        18: 'dètz-e-uèch',
        19: 'dètz-e-nòu',
        20: 'vint',
        30: 'trenta',
        40: 'quaranta',
        50: 'cinquanta',
        60: 'seissanta',
        70: 'setanta',
        80: 'ochanta',
        90: 'nonanta'
    },
    HUNDREDS={
        100: 'cent',
        200: 'dos cents',
        300: 'tres cents',
        400: 'quatre cents',
        500: 'cinc cents',
        600: 'sièis cents',
        700: 'sèt cents',
        800: 'uèch cents',
        900: 'nòu cents'
    },
    FRACTION={
        2: 'mièg',
        3: 'tèrç',
        4: 'quart',
        5: 'cinquen',
        6: 'seisen',
        7: 'seten',
        8: 'ochen',
        9: 'noven',
        10: 'desen',
        11: 'onzen',
        12: 'dotzen',
        13: 'tretzen',
        14: 'catorzen',
        15: 'quinzen',
        16: 'setzen',
        20: 'vinten',
        100: 'centen',
        1000: 'milen'
    },
    FRACTION_FEMALE={
        2: 'mièja'  # "una e mièja" -> 1.5
    },
    SHORT_SCALE={
        1000: 'mila',
        10 ** 6: 'milion',
        10 ** 9: 'miliard',
    },
    LONG_SCALE={
        1000: 'mila',
        10 ** 6: 'milion',
        10 ** 9: 'miliard',
        10 ** 12: 'bilion',
    },

    GENDERED_SPELLINGS={
        GrammaticalGender.FEMININE: {
            1: 'una',
            2: 'doas'
        }
    },
    DIGIT_SPELLINGS={},
    ALT_SPELLINGS={
        'ueitanta': 80,  # attested alternative for ochanta
    },
    ORDINAL_UNITS={
        1: 'primièr',
        2: 'segond',
        3: 'tresen',
        4: 'quatren',
        5: 'cinquen',
        6: 'seisen',
        7: 'seten',
        8: 'ochen',
        9: 'noven',
    },
    ORDINAL_TENS={
        **_ORDINAL_COMPOUNDS,
        1: 'unen',  # extraction alias for compound forms ("vint e unen")
        2: 'dosen',
        10: 'desen',
        11: 'onzen',
        12: 'dotzen',
        13: 'tretzen',
        14: 'catorzen',
        15: 'quinzen',
        16: 'setzen',
        17: 'dètz-e-seten',
        18: 'dètz-e-ochen',
        19: 'dètz-e-noven',
        20: 'vinten',
        30: 'trenten',
        40: 'quaranten',
        50: 'cinquanten',
        60: 'seissanten',
        70: 'setanten',
        80: 'ochanten',
        90: 'nonanten'
    },
    ORDINAL_HUNDREDS={
        100: 'centen',
    },
    ORDINAL_SHORT_SCALE={
        10 ** 3: 'milen',
        10 ** 6: 'milionen',
    },
    ORDINAL_LONG_SCALE={
        10 ** 3: 'milen',
        10 ** 6: 'milionen',
    }
)

OC = RomanceNumberExtractor(_OC)
