"""Number tools for Hebrew.

Pronunciation defaults to the masculine citation forms. Extraction accepts
both genders (numbers 1-19 and the fraction nouns differ by gender), the
construct-state forms used before counted nouns (``שני``/``שתי``, and
``שלושת`` .. ``עשרת`` before ``אלפים``), and the dual forms that encode
value times two (``מאתיים`` = 200, ``אלפיים`` = 2000). Niqqud (vowel
points and cantillation marks) is stripped before matching.
"""

from math import isfinite
from ovos_number_parser.util import convert_to_mixed_fraction

# niqqud and cantillation marks are stripped so vocalized text matches
_NORM_TABLE = {c: None for c in range(0x0591, 0x05C8)}
_NORM_TABLE[0x05BE] = ord("-")  # maqaf joins words like a hyphen


def _normalize_he(text: str) -> str:
    return text.translate(_NORM_TABLE)


# masculine citation forms used for pronunciation
_ONES_HE = ["אפס", "אחד", "שניים", "שלושה", "ארבעה", "חמישה",
            "שישה", "שבעה", "שמונה", "תשעה", "עשרה"]
# feminine forms, accepted in extraction
_ONES_FEM_HE = ["", "אחת", "שתיים", "שלוש", "ארבע", "חמש",
                "שש", "שבע", "שמונה", "תשע", "עשר"]
# construct-state forms: שני/שתי before nouns, שלושת..עשרת before אלפים
_ONES_CONSTRUCT_HE = {2: "שני", 3: "שלושת", 4: "ארבעת", 5: "חמשת",
                      6: "ששת", 7: "שבעת", 8: "שמונת", 9: "תשעת",
                      10: "עשרת"}

# 12 uses the reduced forms שנים/שתים in the teen compounds
_TEEN_UNIT_HE = {1: "אחד", 2: "שנים", 3: "שלושה", 4: "ארבעה", 5: "חמישה",
                 6: "שישה", 7: "שבעה", 8: "שמונה", 9: "תשעה"}
_TEEN_UNIT_FEM_HE = {1: "אחת", 2: "שתים", 3: "שלוש", 4: "ארבע", 5: "חמש",
                     6: "שש", 7: "שבע", 8: "שמונה", 9: "תשע"}

_TENS_HE = {20: "עשרים", 30: "שלושים", 40: "ארבעים", 50: "חמישים",
            60: "שישים", 70: "שבעים", 80: "שמונים", 90: "תשעים"}

_HUNDRED_HE = "מאה"
_HUNDRED_DUAL_HE = "מאתיים"  # 200
_HUNDREDS_PLURAL_HE = "מאות"  # 300-900: feminine unit + מאות

_THOUSAND_HE = "אלף"
_THOUSAND_DUAL_HE = "אלפיים"  # 2000
_THOUSANDS_PLURAL_HE = "אלפים"  # 3000-10000: construct unit + אלפים

# scale words above the thousands
_SCALES_HE = [
    (1000000, "מיליון", "מיליונים"),
    (1000000000, "מיליארד", "מיליארדים"),
    (1000000000000, "טריליון", "טריליונים"),
]

_MINUS_HE = "מינוס"
_DECIMAL_HE = "נקודה"
_INFINITY_HE = "אינסוף"

# fraction nouns: denominator -> (singular, plural, numerator gender)
# שליש and רבע are masculine, the ordinal-derived fifth..tenth are feminine
_FRACTIONS_HE = {
    2: ("חצי", "חצאים", "m"),
    3: ("שליש", "שלישים", "m"),
    4: ("רבע", "רבעים", "m"),
    5: ("חמישית", "חמישיות", "f"),
    6: ("שישית", "שישיות", "f"),
    7: ("שביעית", "שביעיות", "f"),
    8: ("שמינית", "שמיניות", "f"),
    9: ("תשיעית", "תשיעיות", "f"),
    10: ("עשירית", "עשיריות", "f"),
}

# ordinal forms exist for 1-10; larger ordinals use the definite cardinal
_ORDINALS_HE = {1: "ראשון", 2: "שני", 3: "שלישי", 4: "רביעי", 5: "חמישי",
                6: "שישי", 7: "שביעי", 8: "שמיני", 9: "תשיעי", 10: "עשירי"}
_ORDINALS_FEM_HE = {1: "ראשונה", 2: "שנייה", 3: "שלישית", 4: "רביעית",
                    5: "חמישית", 6: "שישית", 7: "שביעית", 8: "שמינית",
                    9: "תשיעית", 10: "עשירית"}


# ---------------------------------------------------------------------------
# pronunciation
# ---------------------------------------------------------------------------

def _join_he(parts):
    """Space-join, prefixing the conjunction ו to the final component."""
    if len(parts) > 1:
        parts = parts[:-1] + ["ו" + parts[-1]]
    return " ".join(parts)


def _two_digit_parts_he(number, feminine=False):
    """0-99 as a list of components (units last, so ו lands on them)."""
    ones = _ONES_FEM_HE if feminine else _ONES_HE
    if number <= 10:
        return [ones[number]]
    if number < 20:
        teen = _TEEN_UNIT_FEM_HE if feminine else _TEEN_UNIT_HE
        suffix = " עשרה" if feminine else " עשר"
        return [teen[number - 10] + suffix]
    tens, unit = divmod(number, 10)
    parts = [_TENS_HE[tens * 10]]
    if unit:
        parts.append(ones[unit])
    return parts


def _three_digit_parts_he(number, feminine=False):
    """0-999 as a list of components."""
    if number < 100:
        return _two_digit_parts_he(number, feminine)
    hundreds, rest = divmod(number, 100)
    if hundreds == 1:
        parts = [_HUNDRED_HE]
    elif hundreds == 2:
        parts = [_HUNDRED_DUAL_HE]
    else:
        parts = [_ONES_FEM_HE[hundreds] + " " + _HUNDREDS_PLURAL_HE]
    if rest:
        parts += _two_digit_parts_he(rest, feminine)
    return parts


def _thousands_component_he(count):
    """The thousands block as a single component."""
    if count == 1:
        return _THOUSAND_HE
    if count == 2:
        return _THOUSAND_DUAL_HE
    if 3 <= count <= 10:
        return _ONES_CONSTRUCT_HE[count] + " " + _THOUSANDS_PLURAL_HE
    return _cardinal_he(count) + " " + _THOUSAND_HE


def _cardinal_he(number, feminine=False):
    if number < 1000:
        return _join_he(_three_digit_parts_he(number, feminine))
    parts = []
    remainder = number
    for value, singular, _plural in reversed(_SCALES_HE):
        count, remainder = divmod(remainder, value)
        if not count:
            continue
        if count == 1:
            parts.append(singular)
        elif count == 2:
            parts.append(_ONES_CONSTRUCT_HE[2] + " " + singular)
        else:
            parts.append(_cardinal_he(count) + " " + singular)
    thousands, remainder = divmod(remainder, 1000)
    if thousands:
        parts.append(_thousands_component_he(thousands))
    if remainder:
        parts += _three_digit_parts_he(remainder, feminine)
    return _join_he(parts)


def pronounce_number_he(number, places=2, scientific=False, ordinals=False,
                        feminine=True):
    """
    Convert a number to its spoken Hebrew equivalent.

    Uses the feminine forms, which are the abstract counting forms in Hebrew:
    the Academy of the Hebrew Language rules that an unspecified number -- in
    arithmetic, phone numbers, counting aloud -- is expressed in the feminine,
    independent of any noun's gender ("4.3 השימוש בשם המספר"). The decimal part
    is read digit by digit after "נקודה" (e.g. 5.2 -> "חמש נקודה שתיים").

    Args:
        number (float or int): the number to pronounce
        places (int): maximum decimal places to speak
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "ראשון" instead of "אחד"
        feminine (bool): use the feminine (abstract counting) forms; True by
            default per the Academy ruling. Callers with a masculine noun
            context (some date fields) pass feminine=False.
    Returns:
        (str): The pronounced number
    """
    if number == float("inf"):
        return _INFINITY_HE
    if number == float("-inf"):
        return _MINUS_HE + " " + _INFINITY_HE
    if scientific:
        if number == 0:
            return _ONES_HE[0]
        n, power = ('%E' % number).replace("+", "").split("E")
        power = int(power)
        if power != 0:
            mantissa = pronounce_number_he(abs(float(n)), places,
                                           feminine=feminine)
            exponent = pronounce_number_he(abs(power), places,
                                           feminine=feminine)
            return "{}{} כפול עשר בחזקת {}{}".format(
                _MINUS_HE + " " if float(n) < 0 else "", mantissa,
                _MINUS_HE + " " if power < 0 else "", exponent)
    if ordinals:
        return pronounce_ordinal_he(number)
    if number < 0:
        return _MINUS_HE + " " + pronounce_number_he(abs(number), places,
                                                     feminine=feminine)

    whole = int(number)
    # "אפס" (zero) is genderless; the feminine ones-list carries "" at index 0
    # because there it means "no units digit", so spell a zero whole part
    # explicitly
    result = _cardinal_he(whole, feminine=feminine) if whole else _ONES_HE[0]
    if isinstance(number, float) and number != whole and places > 0:
        digits = ("%." + str(places) + "f") % (number - whole)
        digits = digits.split(".")[1].rstrip("0")
        if digits:
            result += " " + _DECIMAL_HE + " " + \
                " ".join(_ONES_FEM_HE[int(d)] or _ONES_HE[0] for d in digits)
    return result


def pronounce_ordinal_he(number):
    """
    Pronounce a number as a Hebrew ordinal (masculine, with the definite
    article for 11+), e.g. 1 -> "ראשון", 25 -> "העשרים וחמישה".

    Ordinal forms exist for 1-10 only; larger ordinals use the definite
    cardinal, which is the standard Hebrew pattern.

    Args:
        number (int): the number to pronounce
    Returns:
        (str): the ordinal in Hebrew
    """
    number = int(number)
    if number <= 0:
        raise ValueError("Hebrew ordinals start at 1")
    if number <= 10:
        return _ORDINALS_HE[number]
    return "ה" + _cardinal_he(number)


def nice_number_he(number, speech=True, denominators=range(1, 11)):
    """Hebrew helper for nice_number

    Formats a float as a whole number plus a Hebrew fraction noun, e.g.
    4.5 becomes "4 וחצי" for speech and "4 1/2" for text. Fraction nouns
    exist for denominators 2-10 (חצי, שליש, רבע, חמישית...); numerators
    2+ take the plural with construct-state agreement ("שני שלישים",
    "שלוש חמישיות").

    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 10]
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
    if den in _FRACTIONS_HE:
        singular, plural, gender = _FRACTIONS_HE[den]
        if num == 1:
            frac = singular
        elif num == 2:
            two = "שתי" if gender == "f" else "שני"
            frac = '{} {}'.format(two, plural)
        else:
            count = _cardinal_he(num, feminine=gender == "f")
            frac = '{} {}'.format(count, plural)
    elif num == 1:
        frac = 'חלק אחד מתוך {}'.format(_cardinal_he(den))
    else:
        frac = '{} חלקים מתוך {}'.format(_cardinal_he(num), _cardinal_he(den))
    if whole == 0:
        return frac
    return '{} ו{}'.format(whole, frac)


# ---------------------------------------------------------------------------
# extraction
# ---------------------------------------------------------------------------

def _build_lookup():
    units = {}
    for i, w in enumerate(_ONES_HE):
        units[w] = i
    for i, w in enumerate(_ONES_FEM_HE):
        if w:
            units[w] = i
    for value, word in _ONES_CONSTRUCT_HE.items():
        units[word] = value
    units["שתי"] = 2
    units["שנים"] = 2  # reduced form used in שנים עשר
    units["שתים"] = 2  # reduced form used in שתים עשרה
    tens = dict((w, v) for v, w in _TENS_HE.items())
    scales = {_THOUSAND_HE: 1000, _THOUSANDS_PLURAL_HE: 1000}
    scale_duals = {_THOUSAND_DUAL_HE: 2000, _HUNDRED_DUAL_HE: 200}
    for value, singular, plural in _SCALES_HE:
        scales[singular] = value
        scales[plural] = value
    # unambiguous fraction words usable inside a number ("חמישה וחצי")
    fractions = {"חצי": 0.5, "שליש": 1 / 3, "רבע": 0.25}
    return units, tens, scales, scale_duals, fractions


(_UNITS_LOOKUP, _TENS_LOOKUP, _SCALES_LOOKUP, _SCALE_DUALS_LOOKUP,
 _FRACTIONS_LOOKUP) = _build_lookup()

_TEEN_SECOND_LOOKUP = {"עשר", "עשרה"}
_MINUS_LOOKUP = {"מינוס", "פחות"}
_DECIMAL_LOOKUP = {"נקודה"}
_HUNDRED_WORDS = {_HUNDRED_HE: 100}
_HUNDRED_MULT_LOOKUP = {_HUNDREDS_PLURAL_HE}

_ORDINAL_UNITS_LOOKUP = {w: v for v, w in _ORDINALS_HE.items()}
_ORDINAL_UNITS_LOOKUP.update({w: v for v, w in _ORDINALS_FEM_HE.items()})


def _is_number(s):
    try:
        # a non-finite token ("inf", "nan", "1e309" or an overflowing digit
        # string) carries no usable number and must not be treated as one
        return isfinite(float(s))
    except ValueError:
        return False


def _in_vocab(token):
    return (token in _UNITS_LOOKUP or token in _TENS_LOOKUP or
            token in _SCALES_LOOKUP or token in _SCALE_DUALS_LOOKUP or
            token in _FRACTIONS_LOOKUP or token in _TEEN_SECOND_LOOKUP or
            token in _HUNDRED_WORDS or token in _HUNDRED_MULT_LOOKUP or
            token in _ORDINAL_UNITS_LOOKUP)


def _tokenize_he(text):
    """Normalize and split, detaching the attached conjunction ו.

    Final-letter forms (ם/ן/ץ/ף/ך) are inherent to Hebrew spelling, so no
    folding is applied; only the prefixes ו (and ה before number words)
    are detached when what remains is number vocabulary.
    """
    tokens = []
    for token in _normalize_he(text).split():
        token = token.strip(".,!?;:״׳\"'")
        if not token:
            continue
        if not _in_vocab(token) and len(token) > 1 and token[0] == "ו" and (
                _in_vocab(token[1:]) or
                (token[1] == "ה" and _in_vocab(token[2:]))):
            tokens.append("ו")
            token = token[1:]
        tokens.append(token)
    return tokens


def _strip_article(token):
    if len(token) > 1 and token[0] == "ה" and _in_vocab(token[1:]):
        return token[1:]
    return token


def _parse_ordinal_span(tokens, i):
    """Try to read an ordinal starting at tokens[i].

    Returns (value, next_index) or (None, i)."""
    tok = _strip_article(tokens[i])
    if tok in _ORDINAL_UNITS_LOOKUP:
        return _ORDINAL_UNITS_LOOKUP[tok], i + 1
    # definite cardinal used as an ordinal: "האחד עשר", "העשרים ואחד"
    if tokens[i].startswith("ה") and tok != tokens[i]:
        stripped = [tok] + tokens[i + 1:]
        value, j = _parse_number_span(stripped, 0)
        if value is not None and float(value).is_integer():
            return int(value), i + (j - 0)
    return None, i


def extract_numbers_he(text, short_scale=True, ordinals=False):
    """
    Takes in a string and extracts a list of numbers.

    Accepts both genders of the numerals, the construct-state forms and
    the dual forms מאתיים/אלפיים.

    Args:
        text (str): the string to extract numbers from
        short_scale (bool): ignored, Hebrew scale words are unambiguous
        ordinals (bool): consider ordinal numbers ("שלישי" = 3)
    Returns:
        list: list of extracted numbers as floats
    """
    tokens = _tokenize_he(text)
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
        # decimal part: "נקודה" + digit words
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
    n = len(tokens)
    j = i
    while j < n:
        tok = tokens[j]
        if tok == "ו" and started and j + 1 < n:
            # the conjunction only continues the number if a number word
            # follows and forms part of the same number
            nxt = tokens[j + 1]
            if (nxt in _UNITS_LOOKUP or nxt in _TENS_LOOKUP or
                    nxt in _SCALES_LOOKUP or nxt in _SCALE_DUALS_LOOKUP or
                    nxt in _HUNDRED_WORDS or nxt in _FRACTIONS_LOOKUP):
                j += 1
                continue
            break
        if _is_number(tok):
            if started:
                break
            value = float(tok)
            if value.is_integer():
                value = int(value)
            return value, j + 1
        # teens: unit word followed by עשר/עשרה
        if tok in _UNITS_LOOKUP and 1 <= _UNITS_LOOKUP[tok] <= 9 and \
                j + 1 < n and tokens[j + 1] in _TEEN_SECOND_LOOKUP:
            current += 10 + _UNITS_LOOKUP[tok]
            started = True
            j += 2
            continue
        if tok in _UNITS_LOOKUP:
            # feminine unit followed by מאות multiplies: "שלוש מאות" = 300
            if j + 1 < n and tokens[j + 1] in _HUNDRED_MULT_LOOKUP and \
                    3 <= _UNITS_LOOKUP[tok] <= 9:
                current += _UNITS_LOOKUP[tok] * 100
                started = True
                j += 2
                continue
            current += _UNITS_LOOKUP[tok]
            started = True
            j += 1
            continue
        if tok in _TENS_LOOKUP:
            current += _TENS_LOOKUP[tok]
            started = True
            j += 1
            continue
        if tok in _HUNDRED_WORDS:
            current += _HUNDRED_WORDS[tok]
            started = True
            j += 1
            continue
        if tok in _SCALES_LOOKUP:
            total += (current if current else 1) * _SCALES_LOOKUP[tok]
            current = 0
            started = True
            j += 1
            continue
        if tok in _SCALE_DUALS_LOOKUP:
            value = _SCALE_DUALS_LOOKUP[tok]
            if value == 200:
                current += 200
            else:
                total += value
                current = 0
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
    """Parse the digit words following "נקודה".

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
    if digits:
        return sum(d / 10 ** (k + 1) for k, d in enumerate(digits)), j
    return None, i


def extract_number_he(text, ordinals=False):
    """
    Extract the first number found in Hebrew text.

    Args:
        text (str): the string to extract a number from
        ordinals (bool): consider ordinal numbers ("שלישי" = 3)
    Returns:
        (int, float or False): the extracted number, or False if the text
                               contains no number
    """
    numbers = extract_numbers_he(text, ordinals=ordinals)
    if not numbers:
        return False
    value = numbers[0]
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def is_fractional_he(input_str, short_scale=True):
    """
    Check if the given word is a Hebrew fraction noun.

    Recognizes the fraction nouns for 1/2 .. 1/10 (חצי, שליש, רבע,
    חמישית...), with or without the definite article.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): ignored, present for API compatibility
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    word = _normalize_he(input_str.strip())
    if len(word) > 1 and word[0] == "ה":
        word = word[1:]
    for den, (singular, _plural, _gender) in _FRACTIONS_HE.items():
        if word == singular:
            return 1.0 / den
    return False


def is_ordinal_he(input_str):
    """
    Check if the given text is a Hebrew ordinal number.

    Args:
        input_str (str): the string to check if ordinal
    Returns:
        (bool) or (int): False if not an ordinal, otherwise the number
    """
    tokens = _tokenize_he(input_str)
    if not tokens:
        return False
    value, j = _parse_ordinal_span(tokens, 0)
    if value is not None and j == len(tokens):
        return value
    return False
