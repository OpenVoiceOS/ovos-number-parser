"""Number tools for Modern Standard Arabic and its major spoken lects.

Pronunciation defaults to the masculine nominative citation forms (the forms
used for counting in the abstract, e.g. ``خمسون``, ``اثنان``). Connected
speech governs numerals into the oblique (genitive/accusative) case instead
(``خمسين``, ``اثنين``); pass ``case="oblique"`` to ``pronounce_number_ar`` to
get those forms, see that function's docstring for the closed set of words
this affects and the grammar reference. Extraction accepts both genders and
both cases as input, since Arabic numerals 3-10 take the opposite gender of
the counted noun (gender polarity), both nominative and oblique dual/plural
case endings (``اثنان``/``اثنين``, ``عشرون``/``عشرين``), Western (0-9),
Eastern Arabic-Indic (٠-٩) and Persian/Urdu (۰-۹) digits, and numbers
written immediately adjacent to punctuation (``٢٠٢٤،``, ``25.``).

``resolve_ar_lang`` maps BCP-47 and ISO 639-3 Arabic language codes (the
literary standard and its major spoken lects) to this engine and to each
lect's default register -- see its docstring for the code table and
citations.
"""

import re
from math import isfinite
from ovos_number_parser.util import convert_to_mixed_fraction

_AR_SEPARATOR = " و"  # the conjunction attaches to the following word

# Arabic-Indic and Persian (extended Arabic-Indic) digits, decimal/thousands
# separators, hamza/taa normalization and diacritics stripping used to match
# typed variants
_NORM_TABLE = {ord(e): w for e, w in zip("٠١٢٣٤٥٦٧٨٩", "0123456789")}
# Persian / Urdu digits (U+06F0..U+06F9) carry the same values as 0-9
_NORM_TABLE.update({ord(e): w for e, w in zip("۰۱۲۳۴۵۶۷۸۹", "0123456789")})
_NORM_TABLE[ord("٫")] = "."  # Arabic decimal separator
_NORM_TABLE[ord("٬")] = None  # Arabic thousands separator
_NORM_TABLE[ord("أ")] = "ا"
_NORM_TABLE[ord("إ")] = "ا"
_NORM_TABLE[ord("آ")] = "ا"
_NORM_TABLE[ord("ى")] = "ي"
_NORM_TABLE[ord("ـ")] = None  # tatweel
for _c in range(0x064B, 0x0653):  # tashkeel (fathatan .. sukun)
    _NORM_TABLE[_c] = None
_NORM_TABLE[0x0670] = None  # superscript alef
# ة is typed as ه so often that the two are one letter here, except in the
# hundred مية, which ميه spells too. English Wiktionary gives ميه as an Egyptian
# spelling of مية mayya "water"; the SADA transcripts ("SADA - SBA & SDAIA Audio
# Dataset for Arabic", 2023, transcribed by hand) write it for the hundred
# after a unit word 30 times ("خمس ميه"), before و and a number 56 times ("ميه
# وخمسين") and before a scale word or unit 18 times ("ميه الف"). Both
# spellings are one word, read by the context rules of _HOMOGRAPHS_AR.
_TAA_MARBUTA_RE = re.compile(r"(?<!مي)ة")
_MEEH_RE = re.compile(r"(?<=مي)ه(?!\w)")


def _normalize_ar(text: str) -> str:
    text = _TAA_MARBUTA_RE.sub("ه", text.translate(_NORM_TABLE))
    return _MEEH_RE.sub("ة", text)


# ---------------------------------------------------------------------------
# dialect / language-code resolution
# ---------------------------------------------------------------------------

# ISO 639-3 codes for Arabic varieties routed to this engine, mapped to their
# default pronunciation register. The literary standard (macrolanguage code
# ``ar`` and its individual-language code ``arb``) keeps this module's
# original nominative citation forms as the default; every spoken lect
# defaults to the oblique case instead.
#
# A grammar stands behind that default for three lects only, each giving the
# ‑een/‑iin forms and no ‑aan/‑uun forms: Hijazi (Omar 1975, "itneen",
# "talaatiin"), Gulf (Qafisheh 1970, "'iθneen") and Egyptian (Dirr 1904,
# "etnen, itnen"); see AR_LECT_FORMS for the full references. For Najdi,
# Levantine, Mesopotamian, Moroccan, Tunisian and Libyan no grammar has been
# read, and the default is extrapolated from those three.
#
# Code meanings: ISO 639-3 code table, https://iso639-3.sil.org/code_tables/639/data
AR_DIALECT_DEFAULT_CASE = {
    "ar": "nominative",   # BCP-47/ISO 639-1 macrolanguage code
    "arb": "nominative",  # Standard Arabic (Modern Standard Arabic)
    "ars": "oblique",     # Najdi Arabic
    "acw": "oblique",     # Hijazi Arabic
    "afb": "oblique",     # Gulf Arabic
    "arz": "oblique",     # Egyptian Arabic
    "apc": "oblique",     # Levantine Arabic
    # South Levantine Arabic: retired and merged into apc on 2023-01-20
    # (ISO 639-3 change request 2022-006); still accepted as input
    "ajp": "oblique",
    "acm": "oblique",     # Mesopotamian Arabic (Iraqi)
    "ary": "oblique",     # Moroccan Arabic
    "aeb": "oblique",     # Tunisian Arabic
    "ayl": "oblique",     # Libyan Arabic
}


def resolve_ar_lang(lang: str):
    """
    Resolve a BCP-47 or ISO 639-3 language code to this Arabic engine's
    default pronunciation register.

    Accepts the macrolanguage code (``ar``), BCP-47 forms built on it
    (``ar-SA``, ``ar-EG``, ``ar-x-...``), and the ISO 639-3 codes for the
    individual language and lects this engine serves (``arb``, ``ars``,
    ``acw``, ``afb``, ``arz``, ``apc``, ``ajp``, ``acm``, ``ary``, ``aeb``,
    ``ayl``), matched case-insensitively on the primary subtag.

    Args:
        lang (str): a BCP-47 or ISO 639-3 language code.
    Returns:
        (str) or (None): ``"nominative"`` or ``"oblique"``, the lect's
                         default register, or None if ``lang`` does not name
                         an Arabic variety this engine serves.
    """
    return AR_DIALECT_DEFAULT_CASE.get(lang.lower().split("-")[0])


# Gender. A cardinal takes the form that goes with the gender of the counted
# noun, and the rule differs by range:
#
# - 1 and 2 agree with the noun (واحد/واحدة, اثنان/اثنتان). Ryding, "A
#   Reference Grammar of Modern Standard Arabic" (Cambridge UP, 2005), ch. 15
#   section 1.2: 'The numeral "two" has both feminine and masculine forms and
#   it also inflects for case.' English Wikipedia, "Arabic grammar",
#   Numerals: "The numerals 1 and 2 are adjectives. Thus they follow the noun
#   and agree with gender."
# - 3 to 10 take reverse agreement (gender polarity): a masculine noun takes
#   the form with ة (ثلاثة), a feminine noun the form without it (ثلاث).
#   Ryding ch. 15 section 1.3: "if the singular noun is masculine, the
#   numeral will have the feminine marker taa3 marbuuTa, and if the singular
#   noun is feminine, the numeral will be in the masculine form." W. Wright,
#   "A Grammar of the Arabic Language", 3rd ed. (1896), vol. 1 section 319:
#   "The cardinal numbers from 3 to 10 take the fem. form, when the objects
#   numbered are of the masc. gender; and conversely, the masc. form, when
#   the objects numbered are fem."
# - Feminine eight is ثمان (Ryding ch. 15 section 1.3 table, "thamaanin"; its
#   note 5: "nominative and genitive have identical form: thamaan-in").
_ONES_AR = ["صفر", "واحد", "اثنان", "ثلاثة", "أربعة", "خمسة",
            "ستة", "سبعة", "ثمانية", "تسعة", "عشرة"]
_ONES_FEM_AR = ["", "واحدة", "اثنتان", "ثلاث", "أربع", "خمس",
                "ست", "سبع", "ثمان", "تسع", "عشر"]
# 11 to 19 with a feminine noun. In 11 and 12 both parts agree with the noun;
# in 13 to 19 the unit is reversed and عشرة agrees. Ryding ch. 15 section
# 1.4: "both components of the compound numerals eleven and twelve agree
# with the counted noun in gender"; section 1.5: "the first part of the
# compound number shows gender polarity with the counted noun, while the
# second part of the compound number shows direct gender agreement with the
# counted noun". Ryding's section 1.5 table gives the feminine eighteen as
# "thamaaniy-a cashrat-a" (ثماني عشرة). Twelve is the only teen with a case
# form: Wikipedia "Arabic grammar" table, feminine nominative اثنتا عشرة,
# feminine oblique اثنتي عشرة; Arabic Wikipedia "العدد والمعدود", table of
# compound numbers, "اثنتا/اثنتي عشرة".
_TEENS_FEM_AR = {11: "إحدى عشرة", 12: "اثنتا عشرة", 13: "ثلاث عشرة",
                 14: "أربع عشرة", 15: "خمس عشرة", 16: "ست عشرة",
                 17: "سبع عشرة", 18: "ثماني عشرة", 19: "تسع عشرة"}
_TWELVE_FEM_OBLIQUE_AR = "اثنتي عشرة"

_CASES_AR = ("nominative", "oblique", "genitive", "accusative")


def _resolve_case_ar(case) -> str:
    """The register a case name selects: "nominative" or "oblique".

    None selects the nominative. "genitive" and "accusative" select the
    oblique, which is the genitive and the accusative together (Ryding
    ch. 15 section 1.4: twelve "shows two case inflections, nominative and
    genitive-accusative"). Any other value raises ValueError.
    """
    if case is None or case == "nominative":
        return "nominative"
    if case in ("oblique", "genitive", "accusative"):
        return "oblique"
    raise ValueError("Arabic case must be one of None, "
                     + ", ".join(repr(c) for c in _CASES_AR)
                     + f"; got {case!r}")


def _is_feminine_ar(gender) -> bool:
    """True for the feminine, False for the masculine; ValueError otherwise.

    Arabic has two genders. ``GrammaticalGender`` is a str enum, so the plain
    strings "masculine" and "feminine" are accepted too.
    """
    if gender is None or gender == "masculine":
        return False
    if gender == "feminine":
        return True
    raise ValueError("Arabic gender must be masculine or feminine; "
                     f"got {gender!r}")
_TENS_AR = {20: "عشرون", 30: "ثلاثون", 40: "أربعون", 50: "خمسون",
            60: "ستون", 70: "سبعون", 80: "ثمانون", 90: "تسعون"}
# 300-900 are written fused: feminine unit + مئة
_HUNDREDS_AR = {100: "مئة", 200: "مئتان", 300: "ثلاثمئة", 400: "أربعمئة",
                500: "خمسمئة", 600: "ستمئة", 700: "سبعمئة",
                800: "ثمانمئة", 900: "تسعمئة"}

# singular / dual / plural (3-10) of the scale words. Ryding ch. 15 section
# 1.9 (p. 350): "The word for thousand in Arabic is 'alf plural 'aalaaf";
# p. 155: "million/s milyuun/malaayiin". English Wiktionary, مليار, Arabic:
# "billion (10^9)", borrowed from French milliard. No source read gives
# تريليون; English Wiktionary has no Arabic entry for it.
_SCALES_AR = [
    (1000, "ألف", "ألفان", "آلاف"),
    (1000000, "مليون", "مليونان", "ملايين"),
    (1000000000, "مليار", "ملياران", "مليارات"),
    (1000000000000, "تريليون", "تريليونان", "تريليونات"),
]

# English Wiktionary, سالب, Arabic noun: "(mathematics) negative (of a
# number)", with "سَالِبُ وَاحِدٍ" "negative one"; فاصلة: "decimal point".
# Ryding ch. 14 section 5 (p. 326): "maa laa nihaayat-a infinity ('that
# which has no end')".
_MINUS_AR = "سالب"
_DECIMAL_AR = "فاصلة"
_INFINITY_AR = "ما لا نهاية"

# fraction nouns: denominator -> (singular, dual, plural). Ryding ch. 15
# section 3.1 (p. 360): "a half niSf/'anSaaf", "a third thulth/'athlaath",
# "a fourth, a quarter rubc/'arbaac".
_FRACTIONS_AR = {
    2: ("نصف", "نصفان", "أنصاف"),
    3: ("ثلث", "ثلثان", "أثلاث"),
    4: ("ربع", "ربعان", "أرباع"),
    5: ("خمس", "خمسان", "أخماس"),
    6: ("سدس", "سدسان", "أسداس"),
    7: ("سبع", "سبعان", "أسباع"),
    8: ("ثمن", "ثمنان", "أثمان"),
    9: ("تسع", "تسعان", "أتساع"),
    10: ("عشر", "عشران", "أعشار"),
}

# ordinal stems (without the article); 1 is irregular, 1 in compounds is حادي
_ORDINAL_STEMS_AR = {1: "أول", 2: "ثاني", 3: "ثالث", 4: "رابع", 5: "خامس",
                     6: "سادس", 7: "سابع", 8: "ثامن", 9: "تاسع", 10: "عاشر"}
_ORDINAL_COMPOUND_UNIT_AR = {1: "حادي", 2: "ثاني", 3: "ثالث", 4: "رابع",
                             5: "خامس", 6: "سادس", 7: "سابع", 8: "ثامن",
                             9: "تاسع"}
# Ordinals are adjectives and agree with the noun in gender, with no
# polarity. Ryding ch. 15 section 2: "Ordinal numerals are essentially
# adjectives. They usually follow the noun that they modify and agree with it
# in gender"; section 2.1: 'The Arabic words for "first" are 'awwal (m.) and
# 'uulaa (f.).' Wikipedia "Arabic grammar", Ordinal numerals, lists the
# feminine of each, أولى to عاشرة. Arabic Wikipedia "العدد والمعدود", section
# الصياغة على وزن (فاعل), rule 2: in compound and conjoined ordinals أحد/إحدى
# and واحد/واحدة become الحادي and الحادية; rule 3: the ordinal keeps the
# gender of what it counts, "عدا ألفاظ العقود والمئة والألف فهي ثابتة على
# صورة واحدة" (except the tens, the hundred and the thousand, which keep one
# form).
_ORDINAL_STEMS_FEM_AR = {1: "أولى", 2: "ثانية", 3: "ثالثة", 4: "رابعة",
                         5: "خامسة", 6: "سادسة", 7: "سابعة", 8: "ثامنة",
                         9: "تاسعة", 10: "عاشرة"}
_ORDINAL_COMPOUND_UNIT_FEM_AR = {**{u: _ORDINAL_STEMS_FEM_AR[u]
                                    for u in range(2, 10)}, 1: "حادية"}


# ---------------------------------------------------------------------------
# pronunciation
# ---------------------------------------------------------------------------

def _oblique(word: str) -> str:
    """
    Oblique (genitive/accusative) form of a nominative dual or sound
    masculine plural word, formed by replacing the nominative ending
    (spelled ``ـان``/``ـون``) with the oblique ending (spelled ``ـين``).

    This single substitution covers every closed set this module's oblique
    register touches: the duals (``اثنان`` -> ``اثنين``, ``مئتان`` ->
    ``مئتين``, ``ألفان`` -> ``ألفين``, ``مليونان`` -> ``مليونين``, the
    fraction duals ``نصفان`` -> ``نصفين`` ...) and the tens (``خمسون`` ->
    ``خمسين``), since both endings are two letters long. Citation: Karin C.
    Ryding, "A Reference Grammar of Modern Standard Arabic" (Cambridge
    University Press, 2005), section 9.2 (the dual, -ān/-ayn) and section
    9.5.2 (the sound masculine plural / tens, -ūn/-īn).
    """
    return word[:-2] + "ين"


def _cardinal_two_digit_ar(number: int, case: str = "nominative",
                           feminine: bool = False) -> str:
    """0-99; units come before tens.

    ``case="oblique"`` inflects the dual of two (اثنان -> اثنين, in a units
    slot), the tens (عشرون -> عشرين), and the dual embedded in twelve
    (اثنا عشر -> اثني عشر, Ryding section 9.2: the compound declines in its
    first element only, عشر itself never changes). 11 (أحد عشر) is a fixed
    compound outside those closed sets and is not inflected in either case.

    ``feminine`` selects the forms for a feminine counted noun (see
    ``_ONES_FEM_AR`` and ``_TEENS_FEM_AR``). The tens have no gender; in 21
    to 99 the unit takes the gender its own range takes. Ryding ch. 15
    section 1.6: the tens "do not show any gender distinctions"; section
    1.6.3.1: 'The numeral "one" shows straight gender agreement with the
    noun'; section 1.6.3.2: the units three to nine "show reverse gender
    with the counted noun". Wikipedia "Arabic grammar": 20 to 99 show
    "agreement in gender with the numerals 1 and 2, and polarity for
    numerals 3–9".
    """
    ones = _ONES_FEM_AR if feminine else _ONES_AR
    if number == 0:
        return _ONES_AR[0]
    if number <= 10:
        if number == 2 and case == "oblique":
            return _oblique(ones[2])
        return ones[number]
    if feminine and number < 20:
        if number == 12 and case == "oblique":
            return _TWELVE_FEM_OBLIQUE_AR
        return _TEENS_FEM_AR[number]
    if number == 11:
        return "أحد عشر"
    if number == 12:
        return "اثني عشر" if case == "oblique" else "اثنا عشر"
    if number < 20:
        return _ONES_AR[number - 10] + " عشر"
    tens, unit = divmod(number, 10)
    tens_word = _TENS_AR[tens * 10]
    if case == "oblique":
        tens_word = _oblique(tens_word)
    if unit == 0:
        return tens_word
    unit_word = _oblique(ones[2]) if unit == 2 and case == "oblique" \
        else ones[unit]
    return unit_word + _AR_SEPARATOR + tens_word


def _cardinal_three_digit_ar(number: int, case: str = "nominative",
                             feminine: bool = False) -> str:
    """0-999. The hundred word has one form for either gender, and the gender
    reaches the part after it: 103 with a feminine noun is مئة وثلاث.

    Arabic Wikipedia "العدد والمعدود", classification table: the powers of
    ten "لا تتغير" (do not change) for gender, and a conjoined number
    "يتبع العدد الأخير" (follows its last number). Wikipedia "Arabic
    grammar" gives the feminine "wa-thalāthun wa-sittūna sanatan" after
    "thamānī mi'atin" in 94,863 years.
    """
    if number < 100:
        return _cardinal_two_digit_ar(number, case, feminine)
    hundreds, rest = divmod(number, 100)
    result = _HUNDREDS_AR[hundreds * 100]
    if hundreds == 2 and case == "oblique":
        result = _oblique(result)
    if rest:
        result += _AR_SEPARATOR + _cardinal_two_digit_ar(rest, case, feminine)
    return result


def _cardinal_ar(number: int, case: str = "nominative",
                 feminine: bool = False) -> str:
    """Any whole number. The count before a scale word counts that word,
    which is masculine (ألف, مليون ...), so it stays masculine whatever the
    counted noun; only the last group below a thousand takes ``feminine``.
    Wikipedia "Arabic grammar": "thalāthatu ālāfin" 3,000; "iṯnā ‘ašara
    alfan wa-mi'atāni wa-thnatāni wa-‘ishrūna sanatan" 12,222 years.
    """
    if number < 1000:
        return _cardinal_three_digit_ar(number, case, feminine)
    parts = []
    remainder = number
    for value, singular, dual, plural in reversed(_SCALES_AR):
        count, remainder = divmod(remainder, value)
        if not count:
            continue
        if count == 1:
            parts.append(singular)
        elif count == 2:
            parts.append(_oblique(dual) if case == "oblique" else dual)
        elif 3 <= count <= 10:
            # scale nouns are masculine, so 3-10 take the ة-marked numeral
            parts.append(_ONES_AR[count] + " " + plural)
        else:
            parts.append(_cardinal_ar(count, case) + " " + singular)
    if remainder:
        parts.append(_cardinal_three_digit_ar(remainder, case, feminine))
    return _AR_SEPARATOR.join(parts)


# ---------------------------------------------------------------------------
# lect cardinal forms
# ---------------------------------------------------------------------------

# A lect does not say the literary cardinal. Where this module composes
# "خمسة عشر" for 15, Jidda and Abu Dhabi both say "خمسطعش" and Cairo says
# "خمستاشر"; where it composes "ثلاثمئة", Jidda says "تلتمية" and Abu Dhabi
# "ثلاثمية". A table below gives, for one lect, the word it uses for a value,
# and only the values whose word differs from the literary form -- this module
# still composes the number, so a table names words and never arithmetic.
#
# Keyed by the ISO 639-3 code of the individual Arabic language, which is what
# a caller passes as lang (acw, afb, arz); the macrolanguage
# code ar and the literary arb have no table and keep the literary
# words, and so does any lect no source has been read for -- Najdi ars
# among them, which is deliberate and not an oversight.
#
# Every form is quoted from a published grammar with its page. The Arabic
# spelling of each is the form written in modern transcripts, counted
# whole-word with an optional attached article or conjunction, with that count
# beside it; the tokenisation is named because the defensible ones differ by
# more than a factor of two on the same spelling, and an unstated method makes
# a correct count indistinguishable from a wrong one.
AR_LECT_FORMS = {
    # Hijazi Arabic (urban Jidda). Source: Margaret K. Omar, Saudi Arabic Basic Course: Urban Hijazi Dialect,
    # Foreign Service Institute, 1975.
    "acw": {
        2: "اتنين",           # Omar 1975 p. 59 itneen; SADA n=79
        3: "تلاتة",           # Omar 1975 p. 59 talaata; SADA n=69
        8: "تمنية",           # Omar 1975 p. 59 tamanya; SADA n=12
        11: "إحدعش",          # Omar 1975 p. 59 iHda9š; SADA n=22
        12: "اتنعش",          # Omar 1975 p. 59 itna9š; SADA n=1
        13: "تلاطعش",         # Omar 1975 p. 68 talaṭṭa9š; SADA n=1
        14: "اربعطعش",        # Omar 1975 p. 68 arba9ṭa9š; SADA n=12
        15: "خمسطعش",         # Omar 1975 p. 68 xamasṭa9š; SADA n=36
        16: "سطعش",           # Omar 1975 p. 68 siṭṭa9š; SADA n=5
        17: "سبعطعش",         # Omar 1975 p. 68 saba9ṭa9š; SADA n=28
        18: "تمنطعش",         # Omar 1975 p. 68 tamanṭa9š; SADA n=2
        19: "تسعطعش",         # Omar 1975 p. 68 tisa9ṭa9š; SADA n=11
        30: "تلاتين",         # Omar 1975 p. 68 talaatiin; SADA n=26
        80: "تمانين",         # Omar 1975 p. 68 tamaniin; SADA n=14
        100: "مية",           # Omar 1975 p. 68 miyya; SADA n=2154
        200: "ميتين",         # Omar 1975 p. 69 miyyateen, "a common alternate form is /miiteen/"; SADA n=800
        300: "تلتمية",        # Omar 1975 p. 69 talatmiyya; SADA n=13
        400: "اربعمية",       # Omar 1975 p. 69 arba9miyya; SADA n=70
        500: "خمسمية",        # Omar 1975 p. 69 xamsmiyya; SADA n=514
        600: "ستمية",         # Omar 1975 p. 69 sittmiyya; SADA n=37
        700: "سبعمية",        # Omar 1975 p. 69 sab9miyya; SADA n=79
        800: "تمنمية",        # Omar 1975 p. 69 tamanmiyya; SADA n=1
        900: "تسعمية",        # Omar 1975 p. 69 tis9miyya; SADA n=110
    },
    # Gulf Arabic (Abu Dhabi data). Source: Hamdi A. Qafisheh, Basic Gulf Arabic, Based on Colloquial Abu Dhabi
    # Arabic, University of Arizona, 1970, glossary.
    "afb": {
        11: "حدعش",           # Qafisheh 1970 p. 298 ḥdaʕʃ; SADA n=17
        12: "ثنعش",           # Qafisheh 1970 p. 305 θnaʕʃ; SADA n=2
        13: "ثلاطعش",         # Qafisheh 1970 p. 305 θalaṭṭaʕʃ; SADA n=8
        14: "اربعطعش",        # Qafisheh 1970 p. 293 'arbaʕṭaʕʃ; SADA n=12
        15: "خمسطعش",         # Qafisheh 1970 p. 306 xamsṭaʕʃ; SADA n=36
        16: "سطعش",           # Qafisheh 1970 p. 303 siṭṭaʕʃ; SADA n=5
        17: "سبعطعش",         # Qafisheh 1970 p. 302 sabaʕṭaʕʃ; SADA n=28
        18: "ثمنطعش",         # Qafisheh 1970 p. 305 θamanṭaʕʃ; SADA n=18
        19: "تسعطعش",         # Qafisheh 1970 p. 304 tisaʕṭaʕʃ; SADA n=11
        100: "مية",           # Qafisheh 1970 p. 301 miya; SADA n=2154
        200: "ميتين",         # Qafisheh 1970 p. 301 miyateen; SADA n=800
        300: "ثلاثمية",       # Qafisheh 1970 p. 305 θalaθmiya; SADA n=177
        400: "اربعمية",       # Qafisheh 1970 p. 293 'arbaʕmiya; SADA n=70
        500: "خمسمية",        # Qafisheh 1970 p. 306 xamsmiya; SADA n=514
        600: "ستمية",         # Qafisheh 1970 p. 303 sitmiya; SADA n=37
        700: "سبعمية",        # Qafisheh 1970 p. 302 sabaʕmiya; SADA n=79
        800: "ثمنمية",        # Qafisheh 1970 p. 305 θamanmiya; SADA n=16
        900: "تسعمية",        # Qafisheh 1970 p. 304 tisiʕmiya; SADA n=110
    },
    # Egyptian Arabic (Cairene). Source: Adolf Dirr, Colloquial Egyptian Arabic Grammar, for the Use of
    # Tourists, tr. W. H. Lyall, 1904, pp. 24 and 26.
    "arz": {
        2: "اتنين",           # Dirr 1904 p. 24 etnén; masc 567, sada 79
        3: "تلاتة",           # Dirr 1904 p. 24 telátä; sada 69, omni 88, masc 385 as تلاته
        8: "تمانية",          # Dirr 1904 p. 24 temányä; omni 69, sada 21, masc 10 as تمانيه
        11: "حداشر",          # Dirr 1904 p. 26 ḥaddášar; masc 11, sada 7, omni 17
        12: "اتناشر",         # Dirr 1904 p. 26 etnášar; masc 76, omni 34, sada 5
        13: "تلتاشر",         # Dirr 1904 p. 26 telatášar; masc 11, sada 2. masc writes the syncopated تلتاشر 11 and تلاتاشر 0, so the syncopated form ships
        14: "اربعتاشر",       # Dirr 1904 p. 26 arbaḫtášar; masc 10, omni 13, sada 5
        15: "خمستاشر",        # Dirr 1904 p. 26 ḫamastášar; omni 68, sada 12, masc 6
        16: "ستاشر",          # Dirr 1904 p. 26 sittášar; masc 8, sada 4, omni 2
        17: "سبعتاشر",        # Dirr 1904 p. 26 sab'atášar; sada 14, omni 6, masc 5
        18: "تمنتاشر",        # Dirr 1904 p. 26 temantášar; masc 4, omni 4, sada 2
        19: "تسعتاشر",        # Dirr 1904 p. 26 tis'atášar; masc 5, omni 3, sada 0
        30: "تلاتين",         # Dirr 1904 p. 26 telátín; omni 91, sada 26, masc 25
        80: "تمانين",         # Dirr 1904 p. 26 tamánín; omni 37, masc 22, sada 14
        100: "مية",           # Dirr 1904 p. 26 míya; sada 2154, omni 200, masc 950 as ميه
        200: "ميتين",         # Dirr 1904 p. 26 mítén; sada 800, masc 47, omni 41
        300: "تلتمية",        # Dirr 1904 p. 26 tultêmíya; sada 13, omni 3, masc 22 as تلتميه
        400: "ربعمية",        # Dirr 1904 p. 26 rub'êmíyä; sada 9, omni 3, masc 3 as ربعميه
        500: "خمسمية",        # Dirr 1904 p. 26 ḫumsêmíyä; sada 514, omni 8, masc 10 as خمسميه
        600: "ستمية",         # Dirr 1904 p. 26 suttêmíyä; sada 37, omni 3 as ستميه, masc 5 as ستميه
        700: "سبعمية",        # Dirr 1904 p. 26 sub'êmíyä; sada 79, omni 3, masc 8 as سبعميه
        800: "تمنمية",        # Dirr 1904 p. 26 tumnêmíyä; thin: sada 1, omni 6 as تمنميه, masc 2 as تمنميه
        900: "تسعمية",        # Dirr 1904 p. 26 tus'êmíyä; sada 110, omni 5 as تسعميه, masc 10 as تسعميه
    },
}


def resolve_ar_lect(lang: str):
    """The ISO 639-3 code of the lect whose cardinals lang names, or None.

    Only a lect this module ships a table for resolves; every other Arabic code,
    including the macrolanguage ar and the literary arb, returns None and
    keeps the literary cardinals.
    """
    code = lang.lower().replace("_", "-").split("-")[0]
    return code if code in AR_LECT_FORMS else None


def _lect_cardinal(words: str, number, case: str, lect: str,
                   feminine: bool = False) -> str:
    """Rewrite the literary words of words into lect's.

    The substitution is keyed by VALUE and never by a spelling: the literary word
    for each value in the table is asked of this module, in the case being spoken,
    so a table cannot be thrown off by a change to how the literary form is
    written. Whole words only, and an attached conjunction is kept.

    The tables cite masculine forms only. With ``feminine`` the words for 1 to
    19, which have a gender, stay literary; the tens and hundreds, which have
    one form for both genders, are still rewritten.
    """
    forms = AR_LECT_FORMS.get(lect)
    if not forms:
        return words
    if feminine:
        forms = {value: form for value, form in forms.items() if value >= 20}
    if isinstance(number, int) and number in forms:
        return forms[number]
    said = {}
    for value, form in forms.items():
        literary = _cardinal_ar(value, case)
        if literary and literary != form:
            said[literary] = form
    if not said:
        return words
    pattern = re.compile(r"(?<!\S)(و?)(" + "|".join(re.escape(w) for w in
                                                   sorted(said, key=len, reverse=True)) + r")(?!\S)")
    return pattern.sub(lambda m: m.group(1) + said[m.group(2)], words)


def pronounce_number_ar(number, places=2, scientific=False, ordinals=False,
                        case="nominative", lect=None, gender="masculine"):
    """
    Convert a number to its spoken Arabic equivalent.

    The decimal part is read digit by digit in the masculine citation form
    after "فاصلة" (e.g. 5.2 -> "خمسة فاصلة اثنان").

    Args:
        number (float or int): the number to pronounce
        places (int): maximum decimal places to speak
        scientific (bool): pronounce in scientific notation, in the
            masculine citation forms
        ordinals (bool): pronounce in ordinal form "الأول" instead of "واحد"
        case (str): "nominative" (default, citation forms: خمسون, اثنان,
            مئتان, ...) or "oblique", the case Arabic numerals take in
            connected speech (خمسين, اثنين, مئتين, ...); "genitive" and
            "accusative" are names for the oblique. Only affects the closed
            sets documented on ``_oblique``; every other word is identical
            in both registers. Any other value raises ValueError.
        lect (str, optional): the ISO 639-3 code of an Arabic lect whose own
            cardinal words should be spoken instead of the literary ones --
            ``acw`` (Hijazi), ``afb`` (Gulf), ``arz`` (Egyptian). The number is
            composed the same way either way and only the words differ; see
            :data:`AR_LECT_FORMS`. A lect with no table, the macrolanguage
            ``ar`` and the literary ``arb`` all keep the literary words.
            Ordinals and scientific notation are unaffected.
        gender (GrammaticalGender or str): the gender of the counted noun,
            "masculine" (default) or "feminine"; any other value raises
            ValueError. See ``_ONES_FEM_AR`` and ``pronounce_ordinal_ar``.
    Returns:
        (str): The pronounced number
    """
    case = _resolve_case_ar(case)
    feminine = _is_feminine_ar(gender)
    if number == float("inf"):
        return _INFINITY_AR
    if number == float("-inf"):
        return _MINUS_AR + " " + _INFINITY_AR
    if scientific:
        if number == 0:
            return _ONES_AR[0]
        n, power = ('%E' % number).replace("+", "").split("E")
        power = int(power)
        if power != 0:
            mantissa = pronounce_number_ar(abs(float(n)), places, case=case)
            exponent = pronounce_number_ar(abs(power), places, case=case)
            return "{}{} في عشرة أس {}{}".format(
                _MINUS_AR + " " if float(n) < 0 else "", mantissa,
                _MINUS_AR + " " if power < 0 else "", exponent)
    if ordinals:
        return pronounce_ordinal_ar(number, gender=gender, case=case)
    if number < 0:
        return _MINUS_AR + " " + pronounce_number_ar(abs(number), places,
                                                      case=case, lect=lect,
                                                      gender=gender)

    whole = int(number)
    result = _cardinal_ar(whole, case, feminine)
    if lect:
        result = _lect_cardinal(result, whole if number == whole else None,
                                case, lect, feminine)
    if isinstance(number, float) and number != whole and places > 0:
        digits = ("%." + str(places) + "f") % (number - whole)
        digits = digits.split(".")[1].rstrip("0")
        if digits:
            result += " " + _DECIMAL_AR + " " + \
                " ".join(_ONES_AR[int(d)] for d in digits)
    return result


def pronounce_ordinal_ar(number, gender="masculine", case="nominative"):
    """
    Pronounce a number as a Modern Standard Arabic ordinal with the definite
    article, e.g. 1 -> "الأول", 25 -> "الخامس والعشرون"; with a feminine
    noun "الأولى", "الخامسة والعشرون".

    The ordinal agrees with its noun in gender (see
    ``_ORDINAL_STEMS_FEM_AR``). Case is visible in writing only in the tens
    of 20th to 99th, which decline like the cardinal tens: الحادي والعشرين.
    Ryding ch. 15 section 2.4: "Both parts of the tens ordinal agree in case
    and definiteness with the modified noun", with "fii l-qarn-i l-Haadii
    wa-l-cishriina" (in the twenty-first century). Arabic Wikipedia
    "العدد والمعدود": "قرأتُ المقالةَ الحاديةَ والعشرين". The teens are
    invariable: Ryding ch. 15 section 2.3, "both parts of the compound teens
    ordinal are always in the accusative case"; the feminine teens take
    عشرة, "al-Haadiyat-a cashrat-a", "al-thaaniyat-a cashrat-a".

    Above 99 the masculine nominative is the definite cardinal ("المئة",
    "الألف"). The hundredth and the thousandth have one form for both
    genders and cases (Ryding ch. 15 section 2.5: "hundredth ... agrees in
    definiteness and case, but not in gender"; Arabic Wikipedia, rule 3 of
    الصياغة على وزن فاعل, quoted at ``_ORDINAL_STEMS_FEM_AR``). No source
    read gives the feminine or oblique of any other ordinal above 99, so
    those raise NotImplementedError rather than return an unattested form.

    Args:
        number (int): the number to pronounce
        gender (GrammaticalGender or str): "masculine" (default) or
            "feminine"
        case (str): None, "nominative" (default), "oblique", "genitive" or
            "accusative"; see ``pronounce_number_ar``
    Returns:
        (str): the ordinal in Arabic
    """
    case = _resolve_case_ar(case)
    feminine = _is_feminine_ar(gender)
    number = int(number)
    if number <= 0:
        raise ValueError("Arabic ordinals start at 1")
    stems = _ORDINAL_STEMS_FEM_AR if feminine else _ORDINAL_STEMS_AR
    units = _ORDINAL_COMPOUND_UNIT_FEM_AR if feminine \
        else _ORDINAL_COMPOUND_UNIT_AR
    if number <= 10:
        return "ال" + stems[number]
    if number < 20:
        return "ال" + units[number - 10] + (" عشرة" if feminine else " عشر")
    if number < 100:
        tens, unit = divmod(number, 10)
        tens_word = _TENS_AR[tens * 10]
        if case == "oblique":
            tens_word = _oblique(tens_word)
        tens_word = "ال" + tens_word
        if unit == 0:
            return tens_word
        return "ال" + units[unit] + " و" + tens_word
    if (feminine or case == "oblique") and number not in (100, 1000):
        raise NotImplementedError(
            "the feminine and oblique Arabic ordinals above 99 are "
            "implemented for 100 and 1000 only")
    # beyond 99 Arabic uses the definite cardinal ("المئة", "الألف")
    return "ال" + _cardinal_ar(number)


def nice_number_ar(number, speech=True, denominators=range(1, 11),
                   case="nominative"):
    """Arabic helper for nice_number

    Formats a float as a whole number plus an Arabic fraction noun, e.g.
    4.5 becomes "4 ونصف" for speech and "4 1/2" for text. Fraction nouns
    exist for denominators 2-10 (نصف, ثلث, ربع, ...); the dual is used for
    a numerator of 2 (ثلثان, or ثلثين in the oblique case) and the plural
    for 3-10 (ثلاثة أرباع).

    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 10]
        case (str): "nominative" (default, e.g. نصفان) or "oblique"
            (نصفين); "genitive" and "accusative" name the oblique, and any
            other value raises ValueError, see ``pronounce_number_ar``.
    Returns:
        (str): The formatted string.
    """
    case = _resolve_case_ar(case)
    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        return str(round(number, 3))
    whole, num, den = result
    if not speech:
        if num == 0:
            return str(whole)
        return '{} {}/{}'.format(whole, num, den)
    if num == 0:
        return str(whole)
    if den in _FRACTIONS_AR:
        singular, dual, plural = _FRACTIONS_AR[den]
        if num == 1:
            frac = singular
        elif num == 2:
            frac = _oblique(dual) if case == "oblique" else dual
        else:
            frac = '{} {}'.format(num, plural)
    elif num == 1:
        frac = 'جزء من {}'.format(_cardinal_ar(den, case))
    else:
        frac = '{} أجزاء من {}'.format(num, _cardinal_ar(den, case))
    if whole == 0:
        return frac
    return '{} و{}'.format(whole, frac)


# ---------------------------------------------------------------------------
# extraction
# ---------------------------------------------------------------------------

def _norm_keys(words):
    return {_normalize_ar(w) for w in words}


def _norm_map(mapping):
    return {_normalize_ar(k): v for k, v in mapping.items()}


# dual forms of common counting nouns carry the value 2 lexically
# ("ساعتين" = two hours); both nominative (ـان) and oblique (ـين) endings
_DUAL_NOUNS_AR = {
    "يومان", "يومين", "ساعتان", "ساعتين", "دقيقتان", "دقيقتين",
    "ثانيتان", "ثانيتين", "أسبوعان", "أسبوعين", "شهران", "شهرين",
    "سنتان", "سنتين", "عامان", "عامين", "ليلتان", "ليلتين",
    "مرتان", "مرتين", "اثنتان", "اثنتين",
    "ريالان", "ريالين", "دولاران", "دولارين", "درهمان", "درهمين",
    "جنيهان", "جنيهين",
}


def _build_lookup():
    units = {}
    for i, w in enumerate(_ONES_AR):
        units[w] = i
    for i, w in enumerate(_ONES_FEM_AR):
        if w:
            units[w] = i
    units["اثنين"] = 2  # oblique masculine dual
    units["اثنتين"] = 2  # oblique feminine dual
    units["ثماني"] = 8  # alternative feminine 8
    # ثنتين: Qafisheh 1970 (Gulf): "The feminine forms of waahed 'one' and
    # 'iθneen 'two' are wahda and θinteen" (the OCR of the archive.org scan
    # prints θ as @); English Wiktionary, ثنتين, Arabic:
    # the accusative/genitive feminine of اِثْنَان. ثنين: English Wiktionary,
    # ثنين, Tunisian Arabic: "ṯnīn ... (only when is a digit) two".
    units.update({"ثنتين": 2, "ثنين": 2})
    # the three of the dialects that merge ث into ت (Egyptian, Levantine)
    units.update({"تلاتة": 3, "تلات": 3})
    # Every form AR_LECT_FORMS can SPEAK, this module must also READ: a library that
    # says a word and then cannot recognise it is two libraries. These are the lect
    # spellings whose skeleton nothing above already covers.
    units.update({"اتنين": 2, "تمنية": 8, "تمانية": 8})
    # Egyptian, borrowed from Italian zero: English Wiktionary, زيرو,
    # Egyptian Arabic, "zīrō ... zero"
    units["زيرو"] = 0
    for w in _DUAL_NOUNS_AR:
        units[w] = 2
    tens = {}
    for value, word in _TENS_AR.items():
        tens[word] = value
        tens[word[:-2] + "ين"] = value  # oblique case: عشرين, ثلاثين ...
    # ت for ث in the lects that merge them; see AR_LECT_FORMS
    tens.update({"تلاتين": 30, "تمانين": 80})
    hundreds = {"مئة": 100, "مائة": 100}
    for value, word in _HUNDREDS_AR.items():
        if value >= 200:
            hundreds[word] = value
            hundreds[word.replace("مئة", "مائة")] = value
    hundreds.update({"مئتين": 200, "مائتين": 200, "ثمانيمئة": 800,
                     "ثمانيمائة": 800})
    # colloquial مية for مئة/مائة (100), including fused ثلاثمية..تسعمية
    # (Qafisheh 1970 gives θalaθmiya 300 and θamaanmiya 800, which the OCR of
    # the archive.org scan prints "§Sala6miya" and "§amaanmiya"); see
    # AR_LECT_FORMS
    hundreds["مية"] = 100
    for value, word in _HUNDREDS_AR.items():
        if value >= 300:
            hundreds[word.replace("مئة", "مية")] = value
    hundreds["ميتين"] = 200
    # ثلث is the classical spelling of ثلاث, with a dagger alif that the
    # normalisation strips: Quran 18:25, Uthmani text, "ثَلَٰثَ مِا۟ئَةٍ"
    hundreds["ثلثمئة"] = 300
    # the lect hundreds built on the fraction prefixes (tult-, rub'-, tumn-), and the
    # ت-for-ث spellings; see AR_LECT_FORMS
    hundreds.update({"تلتمية": 300, "ربعمية": 400, "تمنمية": 800, "ثمنمية": 800})
    scales = {}
    scale_duals = {}
    for value, singular, dual, plural in _SCALES_AR:
        scales[singular] = value
        scales[plural] = value
        scale_duals[dual] = 2 * value
    scales.update({"ألفا": 1000, "ألوف": 1000, "مليونا": 1000000,
                   "مليارا": 1000000000})
    scale_duals.update({"ألفين": 2000, "مليونين": 2000000,
                        "مليارين": 2000000000})
    # unambiguous fraction words usable inside a number ("خمسة ونصف")
    fractions = {"نصف": 0.5, "ثلث": 1 / 3, "ربع": 0.25, "سدس": 1 / 6,
                 "ثمن": 0.125}
    return (_norm_map(units), _norm_map(tens), _norm_map(hundreds),
            _norm_map(scales), _norm_map(scale_duals), _norm_map(fractions))


(_UNITS_LOOKUP, _TENS_LOOKUP, _HUNDREDS_LOOKUP, _SCALES_LOOKUP,
 _SCALE_DUALS_LOOKUP, _FRACTIONS_LOOKUP) = _build_lookup()

_TEEN_FIRST_LOOKUP = _norm_map({"أحد": 1, "إحدى": 1, "اثنا": 2, "اثني": 2,
                                "اثنتا": 2, "اثنتي": 2})
_TEEN_SECOND_LOOKUP = _norm_keys({"عشر", "عشرة"})
# dialectal fused teens: unit+عشر contracted into one word ("خمسطعش" = 15).
# Only the spellings of the lect tables are read, which are the forms the
# grammars give (see AR_LECT_FORMS): Omar 1975 for Hijazi, Qafisheh 1970 for
# Gulf, and Dirr 1904, p. 26, "The Numerals from 11 upwards are" for
# Egyptian, which the OCR of the archive.org scan prints "haddiisar",
# "etndsar". English Wiktionary gives the Egyptian eleven and twelve: حداشر,
# "ḥidāšaṛ ... eleven"; اتناشر, "itnāšar ... twelve".
# Teen spellings read beside the lect tables, and never written.
# Qafisheh 1970 prints the Gulf fourteen both ways: "arbaʕtaʕʃ 14" with a
# plain t in the vocabulary of p. 153, and "'arbaʕṭaʕʃ fourteen" with ṭ in the
# glossary of p. 293 (the underdot shows on the archive.org page scans, not
# in their OCR). The rest are English Wiktionary's numeral entries,
# quoted as lect, headword, transliteration, meaning, with the alternative
# and attributive forms each entry lists. The parser does not ask which lect
# wrote a spelling. Left out: إيدو, a Nabk form of the North Levantine eleven,
# which also spells ايدو "his hand" (English Wiktionary, ايد, "hand").
_ATTESTED_TEENS_AR = {
    "اربعتعش": 14,
    # Egyptian Arabic, تلاتاشر "talattāšaṛ", "thirteen"
    "تلاتاشر": 13,
    # Gulf Arabic, خمستعش "ḵamistaʕaš", "fifteen"
    "خمستعش": 15,
    # Iraqi Arabic, اثنعش "iṯnaʕaš", "twelve"
    "اثنعش": 12,
    # South Levantine Arabic, حدعش "ḥdaʕš", "eleven"; listed with it: هدعش
    "هدعش": 11,
    # South Levantine Arabic, تنعش "tnaʕš", "twelve"
    "تنعش": 12,
    # South Levantine Arabic, تلتعش "talattaʕš", "thirteen"
    "تلتعش": 13,
    # South Levantine Arabic, أربعتعش "ʔarbaʕtaʕš", "fourteen"
    "أربعتعش": 14,
    # South Levantine Arabic, ستعش "sittaʕš", "sixteen"
    "ستعش": 16,
    # South Levantine Arabic, سبعتعش "sabaʕtaʕš", "seventeen"
    "سبعتعش": 17,
    # South Levantine Arabic, تمنتعش "tamantaʕš", "eighteen"
    "تمنتعش": 18,
    # South Levantine Arabic, تسعتعش "tisaʕtaʕš", "nineteen"
    "تسعتعش": 19,
    # North Levantine Arabic, إدعش "ʔidaʕš", "eleven"; listed with it: إدعشر, إيدعش
    "إدعش": 11, "إدعشر": 11, "إيدعش": 11,
    # North Levantine Arabic, طنعش "ṭnaʕš", "twelve"; listed with it: إطنو, اطنعش, اطنو, طنعشر
    "إطنو": 12, "اطنعش": 12, "اطنو": 12, "طنعش": 12, "طنعشر": 12,
    # North Levantine Arabic, تلتطعش "t͡ɬɐtɑʕʃ", "thirteen"; listed with it: تلتطعشر
    "تلتطعش": 13, "تلتطعشر": 13,
    # Moroccan Arabic, حداش "ḥdāš", "eleven"; listed with it: حداشل
    "حداش": 11, "حداشل": 11,
    # Moroccan Arabic, تناش "tnāš", "twelve"; listed with it: تناشر, تناشل
    "تناش": 12, "تناشر": 12, "تناشل": 12,
    # Moroccan Arabic, تلتاش "tlattāš", "thirteen"; listed with it: تلتاشل, تلطاش
    "تلتاش": 13, "تلتاشل": 13, "تلطاش": 13,
    # Moroccan Arabic, ربعتاش "rbaʕtāš", "fourteen"; listed with it: أربعتاش, أربعطاش, ربعتاشر, ربعتاشل, ربعطاش
    "أربعتاش": 14, "أربعطاش": 14, "ربعتاش": 14, "ربعتاشر": 14, "ربعتاشل": 14, "ربعطاش": 14,
    # Moroccan Arabic, خمستاش "ḵmastāš", "fifteen"; listed with it: خمستاشل, خمسطاش
    "خمستاش": 15, "خمستاشل": 15, "خمسطاش": 15,
    # Moroccan Arabic, ستاش "sittāš", "sixteen"; listed with it: ستاشل, سطاش
    "ستاش": 16, "ستاشل": 16, "سطاش": 16,
    # Moroccan Arabic, سبعتاش "sbaʕtāš", "seventeen"; listed with it: سبعتاشل, سبعطاش
    "سبعتاش": 17, "سبعتاشل": 17, "سبعطاش": 17,
    # Moroccan Arabic, تمنتاش "tmantāš", "eighteen"; listed with it: تمنتاشل, تمنطاش
    "تمنتاش": 18, "تمنتاشل": 18, "تمنطاش": 18,
    # Moroccan Arabic, تسعتاش "tsaʕtāš", "nineteen"; listed with it: تسعتاشل, تسعطاش
    "تسعتاش": 19, "تسعتاشل": 19, "تسعطاش": 19,
}
_FUSED_TEENS_LOOKUP = _norm_map({
    **{form: value
       for forms in AR_LECT_FORMS.values()
       for value, form in forms.items() if 11 <= value <= 19},
    **_ATTESTED_TEENS_AR})
# ناقص is the minus sign of the number after it, as سالب is. Omar 1975,
# pp. 62-63: "Three minus one talaata naagiṣ waaHid" (the OCR of the
# archive.org scan prints ṣ as $). "عشرة ناقص اثنين" is
# the two numbers 10 and -2: this module normalises numbers and computes
# nothing, so it never reads a difference.
_MINUS_LOOKUP = _norm_keys({"سالب", "ناقص"})
_DECIMAL_LOOKUP = _norm_keys({"فاصلة", "فاصله"})
# a unit before the hundred multiplies it: Dirr 1904, p. 26, gives 300 as
# "tultemiya" and, spaced, "tult mit"; Ryding ch. 15 (p. 348): "five hundred
# xams-u mi'at-in"
_HUNDRED_MULT_LOOKUP = _norm_keys({"مئة", "مائة", "مية"})
# The construct form of the hundred. Before the item counted, the hundred takes
# a final -t, which the Arabic script writes ميت. Hamdi A. Qafisheh, "Basic Gulf
# Arabic, Based on Colloquial Abu Dhabi Arabic" (University of Arizona, 1970),
# p. 59: "If the cardinal numerals 100, 300, 400... 900 are followed by the item
# counted, they take the suffix -t: miya but miyat doolaar". Margaret K. Omar,
# "Saudi Arabic Basic Course: Urban Hijazi Dialect" (Foreign Service Institute,
# 1975), p. 69: "/miyya/ becomes /miyyat/ in a construct phrase", with "miyyat
# alf dulaar" 100,000 dollars. The same letters spell ميت "dead", so the word
# is read as 100 only after و inside a number already started ("الف وميت ريال"
# is 1100). Alone, "ميت ريال" stays no number, because telling it from "a dead
# ..." needs to know that the next word is a counted noun.
_CONSTRUCT_HUNDRED_LOOKUP = _norm_map({"ميت": 100})

# Words that are also everyday words. A normaliser must not change what the
# text says: reading water as 100 changes it, while leaving a real hundred as
# the word مية only misses a conversion. So each of these is a number only
# where its context makes that unambiguous, and is otherwise left as written.
# English Wiktionary gives the everyday senses:
# - مية: Egyptian Arabic, "water" (Etymology 1) as well as "hundred"
#   (Etymology 2); South Levantine Arabic, "alternative form of مَيّ ...
#   water".
# - ميتين: Egyptian Arabic, "two hundred" (Etymology 1) and "plural of ميّت"
#   dead (Etymology 2). ميت: Arabic, "dead"; the construct hundred, see
#   _CONSTRUCT_HUNDRED_LOOKUP.
# - التلات: Moroccan Arabic, "Tuesday", with "يوم التلات"; the alternative
#   form التلاتة. الاثنين: Arabic, "Monday", with "يَوْم الاِثْنَيْن"; Hijazi
#   Arabic, "Monday", "al-itnēn".
# - الست: Egyptian Arabic, "woman", "Mrs, Miss, lady (title for a woman)",
#   with "الست اللى فى الصورة" "the woman that's in this picture".
# Such a word is a number when:
# - a unit word comes before it ("خمس مية"), or it is inside a number
#   already started ("الف ومية");
# - a scale word, a unit of measure, time or currency, or a per-cent word
#   (بالمية, في المية, بالمئة, %) comes directly after it;
# - و and a number word come after it ("مية وخمسين"); او is "or" and joins
#   nothing;
# - it is the whole text, bar one proclitic: a short answer ("بكم؟" ...
#   "مية"). With the article, المية and الميتين alone are "the water" and "the
#   dead", so they are not.
# A homograph next to another homograph is a number only when something else
# makes that other one a number: "الست مية" and "ميت مية" stay as written.
# The construct ميت needs its counted word after it: a scale word, a unit or a
# per-cent word (Dirr 1904, p. 26: "100,000 mit elf"). After يوم a day name is
# a day name unless a scale word follows it. A hundred word after a homograph
# never makes it a number: after التلات, التلاتة or الست it could be 300 or
# 600, or a day or a lady and then 100, so the two words stay as written;
# after the other homographs it is read by its own context.
_WATER_HUNDRED = _normalize_ar("مية")
_DEAD_TWO_HUNDRED = "ميتين"
_CONSTRUCT_HUNDRED = "ميت"
_DAY_NAMES = _norm_keys({"التلات", "التلاتة", "الاتنين", "الاثنين"})
# the homographs that are units three to nine, which build the hundreds
_HUNDRED_UNIT_HOMOGRAPHS = _norm_keys({"التلات", "التلاتة", "الست"})
_HOMOGRAPHS_AR = {_WATER_HUNDRED, _DEAD_TWO_HUNDRED, _CONSTRUCT_HUNDRED,
                  "ال" + _WATER_HUNDRED, "ال" + _DEAD_TWO_HUNDRED,
                  "الست"} | _DAY_NAMES
# يوم, alone or behind a one-letter proclitic (ويوم, بيوم)
_DAY_WORDS = {"يوم"} | {c + "يوم" for c in "وبلف"}
_PER_CENT_WORDS = _norm_keys({"بالمية", "بالمئة", "بالمائة", "%"})
_PER_CENT_AFTER_FI = _norm_keys({"المية", "المئة", "المائة"})
# units of currency, weight, length, volume and time, singular, dual and plural
_UNIT_WORDS_AR = _norm_keys({
    "ريال", "ريالات", "ريالين", "دولار", "دولارات", "دولارين", "جنيه",
    "جنيهات", "جنيهين", "درهم", "دراهم", "درهمين", "دينار", "دنانير",
    "يورو", "كيلو", "كيلوات", "كم", "كيلومتر", "كيلومترات", "متر", "أمتار",
    "مترات", "سم", "غرام", "غرامات", "جرام", "جرامات", "لتر", "لترات",
    "ساعة", "ساعات", "ساعتين", "دقيقة", "دقائق", "دقايق", "دقيقتين",
    "ثانية", "ثواني", "ثانيتين", "يوم", "أيام", "يومين", "سنة", "سنين",
    "سنوات", "سنتين", "شهر", "شهور", "أشهر", "شهرين", "أسبوع", "أسابيع",
    "اسبوعين"})
# the canonical spelling of each, for numbers_to_digits
_CONTEXT_CANONICAL_AR = {
    _WATER_HUNDRED: "مئة", _DEAD_TWO_HUNDRED: "مئتين",
    _CONSTRUCT_HUNDRED: "مئة", "ال" + _WATER_HUNDRED: "المئة",
    "ال" + _DEAD_TWO_HUNDRED: "المئتين", "الست": "ست",
    **_norm_map({"التلات": "ثلاث", "التلاتة": "ثلاثة", "الاتنين": "اثنين",
                 "الاثنين": "اثنين"})}

_ORDINAL_UNITS_LOOKUP = _norm_map(
    {stem: value for value, stem in _ORDINAL_STEMS_AR.items()})
_ORDINAL_UNITS_LOOKUP.update(_norm_map(
    {stem: value for value, stem in _ORDINAL_STEMS_FEM_AR.items()}))
_ORDINAL_UNITS_LOOKUP.update(_norm_map({"حادي": 1, "حادية": 1}))

# every cardinal building-block word, used to strip a tolerated ال- article
_NUMBER_WORDS = (set(_UNITS_LOOKUP) | set(_TENS_LOOKUP) | set(_HUNDREDS_LOOKUP) |
                 set(_SCALES_LOOKUP) | set(_SCALE_DUALS_LOOKUP) |
                 set(_FRACTIONS_LOOKUP) | set(_TEEN_FIRST_LOOKUP) |
                 _TEEN_SECOND_LOOKUP | set(_FUSED_TEENS_LOOKUP))


# A proclitic written onto a number word: the prepositions ب "with, for" and ل
# "to, for" and the conjunction ف "and so". Ryding, "A Reference Grammar of
# Modern Standard Arabic" (Cambridge UP, 2005), ch. 16 section 2.1 (p. 367),
# the one-letter prepositions bi- and li-: "they do not exist as independent
# orthographical items and they need to be prefixed to the noun that follows";
# section 2.1.2 (p. 371) on li- before the article: "the 'alif of the definite
# article is deleted and the laam of li- attaches directly to the laam of the
# definite article". W. Wright, "A Grammar of the Arabic Language", 3rd ed.,
# vol. 1, section 355 (p. 279): inseparable particles are "those which are
# always united in writing with the following noun"; section 366 (p. 290)
# lists و and ف as the inseparable conjunctions. و keeps its own handling in
# _tokenize_ar, because it joins the parts of one number.
_PROCLITICS_AR = "بلف"
# The fraction nouns are left out: ثمن is also "price", so بثمن is "for the
# price of" far more often than "with an eighth".
_PROCLITIC_HOSTS = _NUMBER_WORDS - set(_FRACTIONS_LOOKUP)
# Whole words that the split would misread: لست "I am not" is ل + ست (six).
_PROCLITIC_NOT_NUMBERS = _norm_keys({"لست"})
# The hundred with the article after ب is "per cent" and stays whole:
# عشرة بالمية, عشرة بالمئة. English Wiktionary, بالمية, South Levantine
# Arabic: "percent", with "ميّة بالميّة" "100%". No source was found for the
# spelling بالمئة.
_PROCLITIC_NOT_HOSTS = _norm_keys({"المئة", "المائة", "المية"})


def _split_proclitic(token):
    """Split ب, ل or ف off a number word: ("ب", "الفين") for "بالفين".

    Returns None unless the rest of the token is a cardinal number word, with
    or without the article, and the whole token is not itself a known word.
    """
    if len(token) < 3 or token[0] not in _PROCLITICS_AR or \
            token in _PROCLITIC_NOT_NUMBERS or token in _NUMBER_WORDS:
        return None
    rest = token[1:]
    if rest in _PROCLITIC_NOT_HOSTS:
        return None
    if rest in _PROCLITIC_HOSTS or \
            rest.startswith("ال") and rest[2:] in _PROCLITIC_HOSTS:
        return token[0], rest
    # li- before the article drops the article's alif: للالف is ل + الالف
    if token[0] == "ل" and rest.startswith("ل") and \
            rest[1:] in _PROCLITIC_HOSTS:
        return token[0], "ا" + rest
    return None


def _bare(token):
    """Strip a leading definite article when it fronts a number word."""
    if token.startswith("ال") and token[2:] in _NUMBER_WORDS:
        return token[2:]
    return token


def _is_whole_text(tokens, j):
    """True when tokens[j] is the whole text, bar a proclitic ("مية", "بمية"):
    a short answer ("بكم؟" ... "مية") is its number."""
    return all(t in _PROCLITICS_AR + "و" for i, t in enumerate(tokens)
               if i != j)


def _licenses(tokens, k):
    """True when the number word at tokens[k] can make the word before it a
    number: any number word, except a homograph that nothing else makes a
    number ("الست مية", "ميت مية")."""
    return tokens[k] not in _HOMOGRAPHS_AR or not _out_of_context(tokens, k)


def _counted_word_follows(tokens, j):
    """True when a scale word, a unit, or a per-cent word comes directly after
    the homograph at tokens[j]. A hundred word after it never does: the day
    names and الست are the only homographs that are units, and a hundred after
    them is either ambiguous or no multiplication at all (see
    _hundred_after_a_day_or_lady)."""
    if j + 1 >= len(tokens):
        return False
    nxt = tokens[j + 1]
    if _bare(nxt) in _SCALES_LOOKUP or _bare(nxt) in _SCALE_DUALS_LOOKUP:
        return _licenses(tokens, j + 1)
    if _bare(nxt) in _HUNDRED_MULT_LOOKUP:
        return False
    return nxt in _UNIT_WORDS_AR or nxt in _PER_CENT_WORDS or \
        nxt == "في" and j + 2 < len(tokens) and \
        tokens[j + 2] in _PER_CENT_AFTER_FI


def _joined_to_a_number(tokens, j):
    """True when و and a number word come directly after tokens[j]. او is
    "or" and joins nothing."""
    return j + 2 < len(tokens) and tokens[j + 1] == "و" and (
        _is_number(tokens[j + 2]) or _group_slot(tokens, j + 2) is not None
        and _licenses(tokens, j + 2))


def _hundred_after_a_day_or_lady(tokens, j):
    """True when the hundred word at tokens[j] follows التلات, التلاتة or
    الست with nothing marking a day: "التلات مية ريال" is 300 riyals, or
    Tuesday and 100 riyals, so neither word is read, and a possible 300 is
    never split. الاتنين and الاثنين do not build hundreds (200 is ميتين), and
    after يوم a day name is a day, so after those the hundred reads alone."""
    return _bare(tokens[j]) in _HUNDRED_MULT_LOOKUP and j > 0 and \
        tokens[j - 1] in _HUNDRED_UNIT_HOMOGRAPHS and \
        not (j > 1 and tokens[j - 2] in _DAY_WORDS)


def _out_of_context(tokens, j):
    """True when tokens[j], the first word of a possible number, is a word
    that is also an everyday word and nothing around it makes it a number."""
    tok = tokens[j]
    if _hundred_after_a_day_or_lady(tokens, j):
        return True
    if tok not in _HOMOGRAPHS_AR:
        return False
    if tok in _DAY_NAMES and j > 0 and tokens[j - 1] in _DAY_WORDS:
        # a scale word after it still makes it a number, so that the scale
        # word is never read alone as a smaller number
        nxt = _bare(tokens[j + 1]) if j + 1 < len(tokens) else None
        return not (nxt in _SCALES_LOOKUP or nxt in _SCALE_DUALS_LOOKUP)
    if _counted_word_follows(tokens, j):
        return False
    if tok == _CONSTRUCT_HUNDRED:
        return True
    if _joined_to_a_number(tokens, j):
        return False
    return not (_is_whole_text(tokens, j) and
                tok not in ("ال" + _WATER_HUNDRED, "ال" + _DEAD_TWO_HUNDRED))


def _group_slot(tokens, j):
    """Magnitude slot a number word at ``tokens[j]`` fills in its <1000 group.

    Returns one of ``"unit"``/``"ten"``/``"hundred"`` (which may occur only
    once per group), ``"scale"``/``"frac"`` (which never conflict), or None
    when the token is not a number word."""
    tok = _bare(tokens[j])
    nxt = _bare(tokens[j + 1]) if j + 1 < len(tokens) else None
    if tok in _CONSTRUCT_HUNDRED_LOOKUP:
        return "hundred" if j > 0 and tokens[j - 1] == "و" else None
    if tok in _TEEN_FIRST_LOOKUP and nxt in _TEEN_SECOND_LOOKUP:
        return "unit"
    if tok in _FUSED_TEENS_LOOKUP:
        return "unit"
    if tok in _UNITS_LOOKUP:
        if nxt in _HUNDRED_MULT_LOOKUP and 1 <= _UNITS_LOOKUP[tok] <= 9:
            return "hundred"
        return "unit"
    if tok in _TENS_LOOKUP:
        return "ten"
    if tok in _HUNDREDS_LOOKUP:
        return "hundred"
    if tok in _SCALES_LOOKUP or tok in _SCALE_DUALS_LOOKUP:
        return "scale"
    if tok in _FRACTIONS_LOOKUP:
        return "frac"
    return None


def _is_number(s):
    try:
        # a non-finite token ("inf", "nan", "1e309" or an overflowing digit
        # string) carries no usable number and must not be treated as one
        return isfinite(float(s))
    except ValueError:
        return False


def _tokenize_ar(text):
    """Normalize and split, detaching the attached conjunction "و"."""
    tokens = []
    for token in _normalize_ar(text).split():
        token = token.strip(".,!?;:؟،؛")
        if not token:
            continue
        vocab = (_UNITS_LOOKUP, _TENS_LOOKUP, _HUNDREDS_LOOKUP,
                 _SCALES_LOOKUP, _SCALE_DUALS_LOOKUP, _FRACTIONS_LOOKUP,
                 _TEEN_FIRST_LOOKUP, _ORDINAL_UNITS_LOOKUP,
                 _FUSED_TEENS_LOOKUP)
        whole_word = any(token in v for v in (
            _UNITS_LOOKUP, _TENS_LOOKUP, _HUNDREDS_LOOKUP, _SCALES_LOOKUP,
            _SCALE_DUALS_LOOKUP, _FRACTIONS_LOOKUP, _TEEN_FIRST_LOOKUP,
            _ORDINAL_UNITS_LOOKUP, _FUSED_TEENS_LOOKUP)) or \
            token in _TEEN_SECOND_LOOKUP
        if not whole_word and len(token) > 1 and token[0] == "و" and (
                any(token[1:] in v for v in vocab) or
                token[1:] in _TEEN_SECOND_LOOKUP or
                token[1:] in _CONSTRUCT_HUNDRED_LOOKUP or
                token[1:].startswith("ال") and
                any(token[3:] in v for v in vocab)):
            tokens.append("و")
            token = token[1:]
        elif not whole_word:
            split = _split_proclitic(token)
            if split:
                tokens.append(split[0])
                token = split[1]
        tokens.append(token)
    return tokens


def _parse_ordinal_span(tokens, i):
    """Try to read an ordinal starting at tokens[i].

    Returns (value, next_index) or (None, i)."""
    def strip_article(tok):
        return tok[2:] if tok.startswith("ال") else tok

    tok = strip_article(tokens[i])
    if tok in _ORDINAL_UNITS_LOOKUP:
        unit = _ORDINAL_UNITS_LOOKUP[tok]
        j = i + 1
        # teens: "الحادي عشر" = 11
        if j < len(tokens) and strip_article(tokens[j]) in _TEEN_SECOND_LOOKUP:
            return 10 + unit, j + 1
        # compounds: "الخامس والعشرون" = 25
        if j + 1 < len(tokens) and tokens[j] == "و" and \
                strip_article(tokens[j + 1]) in _TENS_LOOKUP:
            return unit + _TENS_LOOKUP[strip_article(tokens[j + 1])], j + 2
        return unit, j
    if tok in _TENS_LOOKUP and tokens[i].startswith("ال"):
        return _TENS_LOOKUP[tok], i + 1
    return None, i


def _number_spans(tokens, ordinals=False):
    """Yield (start, end, value) for each number in tokens; start includes a
    minus sign before the number."""
    i = 0
    n = len(tokens)
    while i < n:
        start = i
        tok = tokens[i]
        negative = False
        if tok in _MINUS_LOOKUP and i + 1 < n:
            negative = True
            i += 1
            tok = tokens[i]
        if ordinals:
            value, j = _parse_ordinal_span(tokens, i)
            if value is not None:
                yield start, j, -value if negative else value
                i = j
                continue
        value, j = _parse_number_span(tokens, i)
        if value is None:
            i += 1
            continue
        # decimal part: "فاصلة" + digits or a number
        if j < n and tokens[j] in _DECIMAL_LOOKUP:
            frac, j2 = _parse_decimal_part(tokens, j + 1)
            if frac is not None:
                value += frac
                j = j2
        yield start, j, -value if negative else value
        i = j


def extract_numbers_ar(text, short_scale=True, ordinals=False):
    """
    Takes in a string and extracts a list of numbers.

    Accepts both genders of the numerals, nominative and oblique case
    endings, Eastern Arabic-Indic digits and the "٫" decimal separator.

    Args:
        text (str): the string to extract numbers from
        short_scale (bool): ignored, Arabic scale words are unambiguous
        ordinals (bool): consider ordinal numbers ("الثالث" = 3)
    Returns:
        list: list of extracted numbers as floats
    """
    return [value for _, _, value in
            _number_spans(_tokenize_ar(text), ordinals)]


def _parse_number_span(tokens, i):
    """Parse one number starting at tokens[i].

    Returns (value, next_index); value is None if no number starts here."""
    total = 0
    current = 0
    started = False
    filled = set()  # magnitude slots already used in the current <1000 group
    n = len(tokens)
    j = i
    while j < n:
        raw = tokens[j]
        if raw == "و" and started and j + 1 < n:
            # the conjunction continues the number only when the next word is
            # a number component that fills a slot not already taken (two
            # units in a row, "ثلاثة وخمسة", are separate numbers, not eight)
            slot = _group_slot(tokens, j + 1)
            if slot == "hundred" and "hundred" in filled and \
                    _bare(tokens[j + 1]) in _UNITS_LOOKUP:
                # with the hundred filled, a unit after و joins this number and
                # does not multiply the next hundred: "مية و اربعة مية و اربعة"
                # is 104 and 104, never 100 and 404
                slot = "unit"
            if slot in ("scale", "frac") or (
                    slot in ("unit", "ten", "hundred") and slot not in filled):
                j += 1
                continue
            break
        if _is_number(raw):
            if started:
                break
            value = float(raw)
            if value.is_integer():
                value = int(value)
            # a digit run directly followed by a scale word multiplies it
            # ("355 ألف" = 355000)
            j2 = j + 1
            tok2 = _bare(tokens[j2]) if j2 < n else None
            if tok2 in _SCALES_LOOKUP:
                value = value * _SCALES_LOOKUP[tok2]
                j2 += 1
            return value, j2
        if not started and _out_of_context(tokens, j):
            break
        tok = _bare(raw)
        nxt = _bare(tokens[j + 1]) if j + 1 < n else None
        # dialectal fused teens: one word carries both the unit and ten slot
        if tok in _FUSED_TEENS_LOOKUP:
            if {"unit", "ten"} & filled:
                break
            current += _FUSED_TEENS_LOOKUP[tok]
            filled |= {"unit", "ten"}
            started = True
            j += 1
            continue
        # teens: unit word followed by عشر/عشرة
        if (tok in _TEEN_FIRST_LOOKUP or
                (tok in _UNITS_LOOKUP and 1 <= _UNITS_LOOKUP[tok] <= 9)) and \
                nxt in _TEEN_SECOND_LOOKUP:
            if {"unit", "ten"} & filled:
                break
            unit = _TEEN_FIRST_LOOKUP.get(tok) or _UNITS_LOOKUP[tok]
            current += 10 + unit
            filled |= {"unit", "ten"}
            started = True
            j += 2
            continue
        if tok in _UNITS_LOOKUP:
            # unit followed by مئة multiplies: "ثلاث مئة" = 300. The SADA
            # transcripts write two hundred this way too ("اثنين مية واثنين" 202)
            if nxt in _HUNDRED_MULT_LOOKUP and 1 <= _UNITS_LOOKUP[tok] <= 9 and not (
                    "hundred" in filled and tokens[j - 1] == "و"):
                # after a unit or a ten with no و it is a second number:
                # "إثنين إثنين مئة" is 2 and 200, never 202
                if "hundred" in filled or \
                        {"unit", "ten"} & filled and tokens[j - 1] != "و":
                    break
                current += _UNITS_LOOKUP[tok] * 100
                filled.add("hundred")
                started = True
                j += 2
                continue
            if "unit" in filled:
                break
            current += _UNITS_LOOKUP[tok]
            filled.add("unit")
            started = True
            j += 1
            continue
        if tok in _TENS_LOOKUP:
            if "ten" in filled:
                break
            current += _TENS_LOOKUP[tok]
            filled.add("ten")
            started = True
            j += 1
            continue
        if tok in _HUNDREDS_LOOKUP or tok in _CONSTRUCT_HUNDRED_LOOKUP and (
                not started or j > i and tokens[j - 1] == "و"):
            # a hundred written straight after a ten is a second number:
            # "تلاتين مية وعشرين" is 30 and 120, never 130 and 20
            if "hundred" in filled or \
                    "ten" in filled and tokens[j - 1] != "و":
                break
            current += _HUNDREDS_LOOKUP.get(tok) or \
                _CONSTRUCT_HUNDRED_LOOKUP[tok]
            filled.add("hundred")
            started = True
            j += 1
            continue
        if tok in _SCALES_LOOKUP:
            total += (current if current else 1) * _SCALES_LOOKUP[tok]
            current = 0
            filled = set()
            started = True
            j += 1
            continue
        if tok in _SCALE_DUALS_LOOKUP:
            total += _SCALE_DUALS_LOOKUP[tok]
            current = 0
            filled = set()
            started = True
            j += 1
            continue
        if tok in _FRACTIONS_LOOKUP:
            current += _FRACTIONS_LOOKUP[tok]
            started = True
            j += 1
            break  # a fraction noun ends the number
        break
    if not started:
        return None, i
    return total + current, j


def _parse_decimal_part(tokens, i):
    """Parse what follows "فاصلة".

    A run of bare digit words (no conjunction) is read digit by digit
    ("فاصلة اثنان خمسة" = .25); otherwise the following number N with d
    integer digits is N / 10^d ("فاصلة خمسة وعشرون" = .25).

    Returns (fraction, next_index) or (None, i)."""
    n = len(tokens)
    digits = []
    j = i
    while j < n and tokens[j] in _UNITS_LOOKUP and \
            _UNITS_LOOKUP[tokens[j]] <= 9 and \
            not (j + 1 < n and tokens[j + 1] in _TEEN_SECOND_LOOKUP) and \
            not (j + 1 < n and tokens[j + 1] in _HUNDRED_MULT_LOOKUP):
        digits.append(_UNITS_LOOKUP[tokens[j]])
        j += 1
        if j < n and tokens[j] == "و":
            digits = None
            break
    if digits:
        return sum(d / 10 ** (k + 1) for k, d in enumerate(digits)), j
    value, j = _parse_number_span(tokens, i)
    if value is None or value != int(value):
        return None, i
    return value / 10 ** len(str(int(value))), j


def extract_number_ar(text, ordinals=False):
    """
    Extract the first number found in Modern Standard Arabic text.

    Args:
        text (str): the string to extract a number from
        ordinals (bool): consider ordinal numbers ("الثالث" = 3)
    Returns:
        (int, float or False): the extracted number, or False if the text
                               contains no number
    """
    numbers = extract_numbers_ar(text, ordinals=ordinals)
    if not numbers:
        return False
    value = numbers[0]
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def is_fractional_ar(input_str, short_scale=True):
    """
    Check if the given word is an Arabic fraction noun.

    Recognizes the fraction nouns for 1/2 .. 1/10 (نصف, ثلث, ربع, خمس,
    سدس, سبع, ثمن, تسع, عشر), with or without the definite article.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): ignored, present for API compatibility
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    word = _normalize_ar(input_str.strip())
    if word.startswith("ال"):
        word = word[2:]
    for den, (singular, dual, plural) in _FRACTIONS_AR.items():
        if word == _normalize_ar(singular):
            return 1.0 / den
    return False


def is_ordinal_ar(input_str):
    """
    Check if the given text is an Arabic ordinal number.

    Args:
        input_str (str): the string to check if ordinal
    Returns:
        (bool) or (int): False if not an ordinal, otherwise the number
    """
    tokens = _tokenize_ar(input_str)
    if not tokens:
        return False
    value, j = _parse_ordinal_span(tokens, 0)
    if value is not None and j == len(tokens):
        return value
    return False


# A clitic (و "and", ف "so/then", ب "with/by", ل "to/for") can be written
# glued directly onto a digit run ("و355"). Tokenizers that check whole
# whitespace tokens then fail to recognise the digits as a number, so the run
# never joins a following scale word into a mixed span ("و355 ألف" should be
# 355000 with the clitic re-attached: "و355000"). Both patterns match only at
# a token boundary, so a clitic letter occurring mid-word is never touched.
_CLITIC_BEFORE_DIGITS_RE = re.compile(r'(?<!\S)([وفبل])([0-9٠-٩۰-۹])')
_CLITIC_SPACE_DIGITS_RE = re.compile(r'(?<!\S)([وفبل]) (?=[0-9٠-٩۰-۹])')
_WORD_RE = re.compile(r'\S+')


def _detach_proclitic(match):
    """Put a space after a و, ب, ل or ف written onto a number word, so the
    converter replaces the number word and the proclitic is glued back on.
    A detached و still joins the parts of one number ("الف و خمسين" is
    1050), because the converter reads it as a connector."""
    word = match.group(0)
    bare = _normalize_ar(word.strip(".,!?;:؟،؛"))
    if word[0] == "و" and len(bare) > 1 and \
            _tokenize_ar(bare)[0] == "و" and extract_numbers_ar(bare[1:]):
        return "و " + word[1:]
    split = _split_proclitic(bare)
    # only when the rest is a number by itself, or the space would stay
    if split and word[0] in _PROCLITICS_AR and extract_numbers_ar(split[1]):
        return word[0] + " " + word[1:]
    return word


def _continues_a_number_ar(word):
    """True for a word that is a number only inside a number already
    started: the construct hundred ميت, with or without an attached و."""
    return _normalize_ar(word).removeprefix("و") in _CONSTRUCT_HUNDRED_LOOKUP


def _first_number_words_ar(words):
    """How many of `words` the first number covers, as this module reads them,
    or None when the first number does not start at the first word."""
    tokens, owner = [], []
    for w, word in enumerate(words):
        for token in _tokenize_ar(word):
            tokens.append(token)
            owner.append(w)
    for start, end, _ in _number_spans(tokens):
        if owner[start] != 0:
            return None
        return owner[end - 1] + 1
    return None


_MASK_RE = re.compile("\uf8ff(.)\uf8ff")
_PUNCT_AR = ".,!?;:؟،؛"


def _resolve_context_words_ar(utterance):
    """Decide each word that is a number only in context (see
    ``_out_of_context``) against its sentence.

    The span converter reads words one at a time, so such a word is settled
    first: where the sentence makes it a number it is spelled the
    unambiguous way (مية as مئة), and elsewhere it is masked, so the converter
    reads it as no number. Returns the rewritten text and the masked words.
    """
    written = utterance.split()
    words = list(written)
    tokens, owner = [], []
    for w, word in enumerate(words):
        for token in _tokenize_ar(word):
            tokens.append(token)
            owner.append(w)
    in_number = set()
    for start, end, _ in _number_spans(tokens):
        in_number.update(range(start, end))
    masked = []
    for k, token in enumerate(tokens):
        if token not in _CONTEXT_CANONICAL_AR and not (
                k not in in_number and _hundred_after_a_day_or_lady(tokens, k)):
            continue
        w = owner[k]
        word = written[w]
        if k in in_number:
            lead = word[:len(word) - len(word.lstrip(_PUNCT_AR))]
            trail = word[len(word.rstrip(_PUNCT_AR)):]
            prefix = "".join(t for i, t in enumerate(tokens)
                             if owner[i] == w and i < k)
            words[w] = lead + prefix + _CONTEXT_CANONICAL_AR[token] + trail
        else:
            words[w] = "\uf8ff" + chr(0xE000 + len(masked)) + "\uf8ff"
            masked.append(word)
    if words == written:
        return utterance, masked
    return " ".join(words), masked


def numbers_to_digits_ar(utterance: str, lang: str = "ar") -> str:
    """Replace spoken Arabic number spans with digits.

    Splits a clitic glued onto a digit run ("و355 ألف" -> "و 355 ألف"), or a
    و, ب, ل or ف glued onto a number word ("بالفين" -> "ب الفين"), so the
    number reads as an ordinary token, converts through the shared
    span converter, then glues the clitic back onto the produced digits
    ("و355000"). Text without glued clitics passes through the converter
    unchanged.
    """
    # deferred: the shared converter lives in the package root, which imports
    # this module — importing it at module level would be circular
    from ovos_number_parser import _numbers_to_digits_generic
    resolved, masked = _resolve_context_words_ar(utterance)
    spaced = _CLITIC_BEFORE_DIGITS_RE.sub(r'\1 \2', resolved)
    spaced = _WORD_RE.sub(_detach_proclitic, spaced)
    converted = _numbers_to_digits_generic(spaced, lang,
                                           continues=_continues_a_number_ar,
                                           first_number_words=_first_number_words_ar)
    converted = _CLITIC_SPACE_DIGITS_RE.sub(r'\1', converted)
    return _MASK_RE.sub(lambda m: masked[ord(m.group(1)) - 0xE000], converted)
