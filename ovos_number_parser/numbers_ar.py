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
_NORM_TABLE[ord("ة")] = "ه"
_NORM_TABLE[ord("ـ")] = None  # tatweel
for _c in range(0x064B, 0x0653):  # tashkeel (fathatan .. sukun)
    _NORM_TABLE[_c] = None
_NORM_TABLE[0x0670] = None  # superscript alef


def _normalize_ar(text: str) -> str:
    return text.translate(_NORM_TABLE)


# ---------------------------------------------------------------------------
# dialect / language-code resolution
# ---------------------------------------------------------------------------

# ISO 639-3 codes for Arabic varieties routed to this engine, mapped to their
# default pronunciation register. The literary standard (macrolanguage code
# ``ar`` and its individual-language code ``arb``) keeps this module's
# original nominative citation forms as the default; every spoken lect
# defaults to the oblique case instead, since that is the case actually
# produced when these numerals are used in connected speech in those lects.
# Code meanings: ISO 639-3 code table, https://iso639-3.sil.org/code_tables/639/data
# Individual lect entries: https://glottolog.org (search each code below).
AR_DIALECT_DEFAULT_CASE = {
    "ar": "nominative",   # BCP-47/ISO 639-1 macrolanguage code
    "arb": "nominative",  # Standard Arabic (Modern Standard Arabic)
    "ars": "oblique",     # Najdi Arabic
    "acw": "oblique",     # Hijazi Arabic
    "afb": "oblique",     # Gulf Arabic
    "arz": "oblique",     # Egyptian Arabic
    "apc": "oblique",     # North Levantine Arabic
    "ajp": "oblique",     # South Levantine Arabic
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


# masculine citation forms used for pronunciation
_ONES_AR = ["صفر", "واحد", "اثنان", "ثلاثة", "أربعة", "خمسة",
            "ستة", "سبعة", "ثمانية", "تسعة", "عشرة"]
# feminine forms, accepted in extraction (gender polarity)
_ONES_FEM_AR = ["", "واحدة", "اثنتان", "ثلاث", "أربع", "خمس",
                "ست", "سبع", "ثمان", "تسع", "عشر"]
_TENS_AR = {20: "عشرون", 30: "ثلاثون", 40: "أربعون", 50: "خمسون",
            60: "ستون", 70: "سبعون", 80: "ثمانون", 90: "تسعون"}
# 300-900 are written fused: feminine unit + مئة
_HUNDREDS_AR = {100: "مئة", 200: "مئتان", 300: "ثلاثمئة", 400: "أربعمئة",
                500: "خمسمئة", 600: "ستمئة", 700: "سبعمئة",
                800: "ثمانمئة", 900: "تسعمئة"}

# singular / dual / plural (3-10) of the scale words
_SCALES_AR = [
    (1000, "ألف", "ألفان", "آلاف"),
    (1000000, "مليون", "مليونان", "ملايين"),
    (1000000000, "مليار", "ملياران", "مليارات"),
    (1000000000000, "تريليون", "تريليونان", "تريليونات"),
]

_MINUS_AR = "سالب"
_DECIMAL_AR = "فاصلة"
_INFINITY_AR = "ما لا نهاية"

# fraction nouns: denominator -> (singular, dual, plural)
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
# feminine ordinal stems, accepted in extraction
_ORDINAL_STEMS_FEM_AR = {1: "أولى", 2: "ثانية", 3: "ثالثة", 4: "رابعة",
                         5: "خامسة", 6: "سادسة", 7: "سابعة", 8: "ثامنة",
                         9: "تاسعة", 10: "عاشرة"}


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


def _cardinal_two_digit_ar(number: int, case: str = "nominative") -> str:
    """0-99 in masculine citation forms; units come before tens.

    ``case="oblique"`` inflects the dual of two (اثنان -> اثنين, in a units
    slot) and the tens (عشرون -> عشرين). 11 (أحد عشر) and 12 (اثنا عشر) are
    fixed compounds outside those closed sets and are not inflected.
    """
    if number <= 10:
        if number == 2 and case == "oblique":
            return _oblique(_ONES_AR[2])
        return _ONES_AR[number]
    if number == 11:
        return "أحد عشر"
    if number == 12:
        return "اثنا عشر"
    if number < 20:
        return _ONES_AR[number - 10] + " عشر"
    tens, unit = divmod(number, 10)
    tens_word = _TENS_AR[tens * 10]
    if case == "oblique":
        tens_word = _oblique(tens_word)
    if unit == 0:
        return tens_word
    unit_word = _oblique(_ONES_AR[2]) if unit == 2 and case == "oblique" \
        else _ONES_AR[unit]
    return unit_word + _AR_SEPARATOR + tens_word


def _cardinal_three_digit_ar(number: int, case: str = "nominative") -> str:
    """0-999 in masculine citation forms."""
    if number < 100:
        return _cardinal_two_digit_ar(number, case)
    hundreds, rest = divmod(number, 100)
    result = _HUNDREDS_AR[hundreds * 100]
    if hundreds == 2 and case == "oblique":
        result = _oblique(result)
    if rest:
        result += _AR_SEPARATOR + _cardinal_two_digit_ar(rest, case)
    return result


def _cardinal_ar(number: int, case: str = "nominative") -> str:
    if number < 1000:
        return _cardinal_three_digit_ar(number, case)
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
        parts.append(_cardinal_three_digit_ar(remainder, case))
    return _AR_SEPARATOR.join(parts)


def pronounce_number_ar(number, places=2, scientific=False, ordinals=False,
                        case="nominative"):
    """
    Convert a number to its spoken Arabic equivalent.

    Uses masculine forms; the decimal part is read digit by digit after
    "فاصلة" (e.g. 5.2 -> "خمسة فاصلة اثنان").

    Args:
        number (float or int): the number to pronounce
        places (int): maximum decimal places to speak
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "الأول" instead of "واحد"
        case (str): "nominative" (default, unchanged citation forms:
            خمسون, اثنان, مئتان, ...) or "oblique", the case Arabic
            numerals actually take in connected speech (خمسين, اثنين,
            مئتين, ...). Only affects the closed sets documented on
            ``_oblique``; every other word is identical in both registers.
            Ordinals (``ordinals=True``) are unaffected by ``case``.
    Returns:
        (str): The pronounced number
    """
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
        return pronounce_ordinal_ar(number)
    if number < 0:
        return _MINUS_AR + " " + pronounce_number_ar(abs(number), places,
                                                      case=case)

    whole = int(number)
    result = _cardinal_ar(whole, case)
    if isinstance(number, float) and number != whole and places > 0:
        digits = ("%." + str(places) + "f") % (number - whole)
        digits = digits.split(".")[1].rstrip("0")
        if digits:
            result += " " + _DECIMAL_AR + " " + \
                " ".join(_ONES_AR[int(d)] for d in digits)
    return result


def pronounce_ordinal_ar(number):
    """
    Pronounce a number as a Modern Standard Arabic ordinal (masculine,
    with the definite article), e.g. 1 -> "الأول", 25 -> "الخامس والعشرون".

    Args:
        number (int): the number to pronounce
    Returns:
        (str): the ordinal in Arabic
    """
    number = int(number)
    if number <= 0:
        raise ValueError("Arabic ordinals start at 1")
    if number <= 10:
        return "ال" + _ORDINAL_STEMS_AR[number]
    if number < 20:
        return "ال" + _ORDINAL_COMPOUND_UNIT_AR[number - 10] + " عشر"
    if number < 100:
        tens, unit = divmod(number, 10)
        tens_word = "ال" + _TENS_AR[tens * 10]
        if unit == 0:
            return tens_word
        return "ال" + _ORDINAL_COMPOUND_UNIT_AR[unit] + " و" + tens_word
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
            (نصفين), see ``pronounce_number_ar``.
    Returns:
        (str): The formatted string.
    """
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
    for w in _DUAL_NOUNS_AR:
        units[w] = 2
    tens = {}
    for value, word in _TENS_AR.items():
        tens[word] = value
        tens[word[:-2] + "ين"] = value  # oblique case: عشرين, ثلاثين ...
    hundreds = {"مئة": 100, "مائة": 100}
    for value, word in _HUNDREDS_AR.items():
        if value >= 200:
            hundreds[word] = value
            hundreds[word.replace("مئة", "مائة")] = value
    hundreds.update({"مئتين": 200, "مائتين": 200, "ثمانيمئة": 800,
                     "ثمانيمائة": 800})
    # colloquial مية/ميه for مئة/مائة (100), including fused ثلاثمية..تسعمية
    hundreds["مية"] = 100
    for value, word in _HUNDREDS_AR.items():
        if value >= 300:
            hundreds[word.replace("مئة", "مية")] = value
    hundreds["ميتين"] = 200
    # deeper colloquial root (ثلث- instead of ثلاث-) for 300
    hundreds["ثلثمئة"] = 300
    hundreds["ثلثمية"] = 300
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
# dialectal fused teens (Gulf/Levantine): unit+عشر contracted into one word
# ("اثناشر" = 12); accepted spelling variants for the sibilant/interdental
# consonants (ط/ت for ث). See e.g.
# https://en.wikipedia.org/wiki/Arabic_numerals#Numerals_11-19 and Gulf/
# Levantine colloquial numeral references (Peace Corps Jordanian Arabic
# numeral guide; Wiktionary entries for احداشر / اثناشر).
_FUSED_TEENS_LOOKUP = _norm_map({
    "احداشر": 11, "اثناشر": 12, "ثلطاشر": 13, "ثلتاشر": 13,
    "اربعتاشر": 14, "خمستاشر": 15, "ستاشر": 16, "سبعتاشر": 17,
    "ثمنتاشر": 18, "تسعتاشر": 19,
})
_MINUS_LOOKUP = _norm_keys({"سالب", "ناقص"})
_DECIMAL_LOOKUP = _norm_keys({"فاصلة", "فاصله"})
_HUNDRED_MULT_LOOKUP = _norm_keys({"مئة", "مائة"})

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


def _bare(token):
    """Strip a leading definite article when it fronts a number word."""
    if token.startswith("ال") and token[2:] in _NUMBER_WORDS:
        return token[2:]
    return token


def _group_slot(tokens, j):
    """Magnitude slot a number word at ``tokens[j]`` fills in its <1000 group.

    Returns one of ``"unit"``/``"ten"``/``"hundred"`` (which may occur only
    once per group), ``"scale"``/``"frac"`` (which never conflict), or None
    when the token is not a number word."""
    tok = _bare(tokens[j])
    nxt = _bare(tokens[j + 1]) if j + 1 < len(tokens) else None
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
                token[1:].startswith("ال") and
                any(token[3:] in v for v in vocab)):
            tokens.append("و")
            token = token[1:]
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
    tokens = _tokenize_ar(text)
    results = []
    i = 0
    n = len(tokens)
    while i < n:
        tok = tokens[i]
        negative = False
        if tok in _MINUS_LOOKUP and i + 1 < n:
            negative = True
            i += 1
            tok = tokens[i]
        if ordinals:
            value, j = _parse_ordinal_span(tokens, i)
            if value is not None:
                results.append(-value if negative else value)
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
        results.append(-value if negative else value)
        i = j
    return results


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
            # unit followed by مئة multiplies: "ثلاث مئة" = 300
            if nxt in _HUNDRED_MULT_LOOKUP and 1 <= _UNITS_LOOKUP[tok] <= 9:
                if "hundred" in filled:
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
        if tok in _HUNDREDS_LOOKUP:
            if "hundred" in filled:
                break
            current += _HUNDREDS_LOOKUP[tok]
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
