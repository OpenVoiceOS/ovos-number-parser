"""Number tools for Modern Greek.

Pronunciation defaults to the neuter citation forms with their accents
(the forms used for counting in the abstract). Extraction accepts every
gender variant (τρία/τρεις, τέσσερα/τέσσερις, ένα/ένας/μία, feminine
hundreds like διακόσιες), both the επτά/εφτά, οκτώ/οχτώ and εννέα/εννιά
spellings, and unaccented input: matching is done on text with the Greek
tonos and diaeresis stripped and the final sigma folded.
"""

from math import isfinite
from ovos_number_parser.util import convert_to_mixed_fraction

# tonos/diaeresis stripping + final sigma folding, applied after casefold
_NORM_TABLE = {ord(a): b for a, b in zip("άέήίόύώϊϋΐΰς", "αεηιουωιυιυσ")}


def _normalize_el(text: str) -> str:
    return text.casefold().translate(_NORM_TABLE)


# neuter citation forms used for pronunciation
_ONES_EL = ["μηδέν", "ένα", "δύο", "τρία", "τέσσερα", "πέντε",
            "έξι", "επτά", "οκτώ", "εννέα", "δέκα"]
_TEENS_EL = {11: "έντεκα", 12: "δώδεκα", 13: "δεκατρία", 14: "δεκατέσσερα",
             15: "δεκαπέντε", 16: "δεκαέξι", 17: "δεκαεπτά",
             18: "δεκαοκτώ", 19: "δεκαεννέα"}
_TENS_EL = {20: "είκοσι", 30: "τριάντα", 40: "σαράντα", 50: "πενήντα",
            60: "εξήντα", 70: "εβδομήντα", 80: "ογδόντα", 90: "ενενήντα"}
# neuter hundreds; 100 alternates εκατό/εκατόν (εκατόν before a vowel)
_HUNDREDS_EL = {200: "διακόσια", 300: "τριακόσια", 400: "τετρακόσια",
                500: "πεντακόσια", 600: "εξακόσια", 700: "επτακόσια",
                800: "οκτακόσια", 900: "εννιακόσια"}

# feminine forms used when counting χιλιάδες (thousands are feminine)
_ONES_FEM_EL = {1: "μία", 3: "τρεις", 4: "τέσσερις"}
_TEENS_FEM_EL = {13: "δεκατρείς", 14: "δεκατέσσερις"}
_HUNDREDS_FEM_EL = {200: "διακόσιες", 300: "τριακόσιες", 400: "τετρακόσιες",
                    500: "πεντακόσιες", 600: "εξακόσιες", 700: "επτακόσιες",
                    800: "οκτακόσιες", 900: "εννιακόσιες"}

_MINUS_EL = "μείον"
_DECIMAL_EL = "κόμμα"
_INFINITY_EL = "άπειρο"

# fraction nouns (neuter): denominator -> (singular, plural)
_FRACTIONS_EL = {
    2: ("μισό", "μισά"),
    3: ("τρίτο", "τρίτα"),
    4: ("τέταρτο", "τέταρτα"),
    5: ("πέμπτο", "πέμπτα"),
    6: ("έκτο", "έκτα"),
    7: ("έβδομο", "έβδομα"),
    8: ("όγδοο", "όγδοα"),
    9: ("ένατο", "ένατα"),
    10: ("δέκατο", "δέκατα"),
}

# masculine ordinal citation forms
_ORDINAL_UNITS_EL = {1: "πρώτος", 2: "δεύτερος", 3: "τρίτος",
                     4: "τέταρτος", 5: "πέμπτος", 6: "έκτος",
                     7: "έβδομος", 8: "όγδοος", 9: "ένατος",
                     10: "δέκατος", 11: "ενδέκατος", 12: "δωδέκατος"}
_ORDINAL_TENS_EL = {20: "εικοστός", 30: "τριακοστός", 40: "τεσσαρακοστός",
                    50: "πεντηκοστός", 60: "εξηκοστός", 70: "εβδομηκοστός",
                    80: "ογδοηκοστός", 90: "ενενηκοστός"}
_ORDINAL_HUNDREDS_EL = {100: "εκατοστός", 200: "διακοσιοστός",
                        300: "τριακοσιοστός", 400: "τετρακοσιοστός",
                        500: "πεντακοσιοστός", 600: "εξακοσιοστός",
                        700: "επτακοσιοστός", 800: "οκτακοσιοστός",
                        900: "εννιακοσιοστός"}
_ORDINAL_SCALES_EL = {1000: "χιλιοστός", 1000000: "εκατομμυριοστός"}

_VOWELS_EL = set("αεηιουω")


# ---------------------------------------------------------------------------
# pronunciation
# ---------------------------------------------------------------------------

def _two_digit_el(number: int, feminine: bool = False) -> str:
    """0-99 in neuter (or feminine, for counting χιλιάδες) forms."""
    if number <= 10:
        if feminine and number in _ONES_FEM_EL:
            return _ONES_FEM_EL[number]
        return _ONES_EL[number]
    if number < 20:
        if feminine and number in _TEENS_FEM_EL:
            return _TEENS_FEM_EL[number]
        return _TEENS_EL[number]
    tens, unit = divmod(number, 10)
    if unit == 0:
        return _TENS_EL[tens * 10]
    return _TENS_EL[tens * 10] + " " + _two_digit_el(unit, feminine)


def _three_digit_el(number: int, feminine: bool = False) -> str:
    """0-999 in neuter (or feminine) forms."""
    if number < 100:
        return _two_digit_el(number, feminine)
    hundreds, rest = divmod(number, 100)
    if hundreds == 1:
        if not rest:
            return "εκατό"
        rest_word = _two_digit_el(rest, feminine)
        prefix = "εκατόν" if _normalize_el(rest_word)[0] in _VOWELS_EL \
            else "εκατό"
        return prefix + " " + rest_word
    table = _HUNDREDS_FEM_EL if feminine else _HUNDREDS_EL
    result = table[hundreds * 100]
    if rest:
        result += " " + _two_digit_el(rest, feminine)
    return result


def _cardinal_el(number: int) -> str:
    if number < 1000:
        return _three_digit_el(number)
    parts = []
    billions, remainder = divmod(number, 1000000000)
    if billions:
        if billions == 1:
            parts.append("ένα δισεκατομμύριο")
        else:
            parts.append(_cardinal_el(billions) + " δισεκατομμύρια")
    millions, remainder = divmod(remainder, 1000000)
    if millions:
        if millions == 1:
            parts.append("ένα εκατομμύριο")
        else:
            parts.append(_cardinal_el(millions) + " εκατομμύρια")
    thousands, remainder = divmod(remainder, 1000)
    if thousands:
        if thousands == 1:
            parts.append("χίλια")
        else:
            # thousands are counted with the feminine numerals
            parts.append(_three_digit_el(thousands, feminine=True) +
                         " χιλιάδες")
    if remainder:
        parts.append(_three_digit_el(remainder))
    return " ".join(parts)


def pronounce_number_el(number, places=2, scientific=False, ordinals=False):
    """
    Convert a number to its spoken Modern Greek equivalent.

    Uses the neuter citation forms; the decimal part is read digit by
    digit after "κόμμα" (e.g. 3.14 -> "τρία κόμμα ένα τέσσερα").

    Args:
        number (float or int): the number to pronounce
        places (int): maximum decimal places to speak
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce the ordinal form "πρώτος" instead of "ένα"
    Returns:
        (str): The pronounced number
    """
    if number == float("inf"):
        return _INFINITY_EL
    if number == float("-inf"):
        return _MINUS_EL + " " + _INFINITY_EL
    if scientific:
        if number == 0:
            return _ONES_EL[0]
        n, power = ('%E' % number).replace("+", "").split("E")
        power = int(power)
        if power != 0:
            mantissa = pronounce_number_el(abs(float(n)), places)
            exponent = pronounce_number_el(abs(power), places)
            return "{}{} επί δέκα στη δύναμη {}{}".format(
                _MINUS_EL + " " if float(n) < 0 else "", mantissa,
                _MINUS_EL + " " if power < 0 else "", exponent)
    if ordinals:
        return pronounce_ordinal_el(number)
    if number < 0:
        return _MINUS_EL + " " + pronounce_number_el(abs(number), places)

    whole = int(number)
    result = _cardinal_el(whole)
    if isinstance(number, float) and number != whole and places > 0:
        digits = ("%." + str(places) + "f") % (number - whole)
        digits = digits.split(".")[1].rstrip("0")
        if digits:
            result += " " + _DECIMAL_EL + " " + \
                " ".join(_ONES_EL[int(d)] for d in digits)
    return result


def pronounce_ordinal_el(number):
    """
    Pronounce a number as a Modern Greek ordinal (masculine),
    e.g. 1 -> "πρώτος", 13 -> "δέκατος τρίτος", 21 -> "εικοστός πρώτος".

    Args:
        number (int): the number to pronounce
    Returns:
        (str): the ordinal in Greek
    """
    number = int(number)
    if number <= 0:
        raise ValueError("Greek ordinals start at 1")
    if number in _ORDINAL_SCALES_EL:
        return _ORDINAL_SCALES_EL[number]
    parts = []
    remainder = number
    if remainder >= 100:
        hundreds, remainder = divmod(remainder, 100)
        if hundreds > 9:
            raise ValueError(f"Greek ordinal too large: {number}")
        parts.append(_ORDINAL_HUNDREDS_EL[hundreds * 100])
    if remainder >= 20:
        tens, remainder = divmod(remainder, 10)
        parts.append(_ORDINAL_TENS_EL[tens * 10])
    elif remainder >= 13:
        parts.append(_ORDINAL_UNITS_EL[10])
        remainder -= 10
    if remainder:
        parts.append(_ORDINAL_UNITS_EL[remainder])
    return " ".join(parts)


def nice_number_el(number, speech=True, denominators=range(1, 11)):
    """Greek helper for nice_number

    Formats a float as a whole number plus a Greek fraction noun, e.g.
    4.5 becomes "4 και μισό" for speech and "4 1/2" for text. Fraction
    nouns exist for denominators 2-10 (μισό, τρίτο, τέταρτο, ...); the
    neuter plural is used for numerators above 1 (δύο τρίτα).

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
    if den in _FRACTIONS_EL:
        singular, plural = _FRACTIONS_EL[den]
        if num == 1:
            frac = singular
        else:
            frac = '{} {}'.format(num, plural)
    elif num == 1:
        frac = 'ένα {}'.format(pronounce_ordinal_el(den).replace("ος", "ο"))
    else:
        frac = '{} {}'.format(num,
                              pronounce_ordinal_el(den).replace("ος", "α"))
    if whole == 0:
        return frac
    return '{} και {}'.format(whole, frac)


# ---------------------------------------------------------------------------
# extraction
# ---------------------------------------------------------------------------

def _norm_map(mapping):
    return {_normalize_el(k): v for k, v in mapping.items()}


def _build_lookup():
    units = {}
    for i, w in enumerate(_ONES_EL):
        units[w] = i
    for value, w in _TEENS_EL.items():
        units[w] = value
    # gender variants
    units.update({"ένας": 1, "μία": 1, "μια": 1, "μίας": 1, "ενός": 1,
                  "τρεις": 3, "τέσσερις": 4, "τέσσερεις": 4,
                  "δεκατρείς": 13, "δεκατέσσερις": 14, "δεκατέσσερεις": 14})
    # accepted spelling variants
    units.update({"εφτά": 7, "οχτώ": 8, "εννιά": 9, "ένδεκα": 11,
                  "δεκαέξη": 16, "δεκαεφτά": 17, "δεκαοχτώ": 18,
                  "δεκαεννιά": 19})
    tens = dict((w, v) for v, w in _TENS_EL.items())
    hundreds = {"εκατό": 100, "εκατόν": 100}
    for value, w in _HUNDREDS_EL.items():
        hundreds[w] = value
        hundreds[_HUNDREDS_FEM_EL[value]] = value
        hundreds[w[:-1] + "οι"] = value  # masculine -οι
    # spelling variants of the hundreds
    hundreds.update({"εφτακόσια": 700, "εφτακόσιες": 700,
                     "οχτακόσια": 800, "οχτακόσιες": 800,
                     "εννιακόσα": 900})
    scales = {"χίλια": 1000, "χίλιες": 1000, "χιλιάδες": 1000,
              "χιλιάδα": 1000,
              "εκατομμύριο": 1000000, "εκατομμύρια": 1000000,
              "δισεκατομμύριο": 1000000000, "δισεκατομμύρια": 1000000000,
              "τρισεκατομμύριο": 1000000000000,
              "τρισεκατομμύρια": 1000000000000}
    # fraction words usable inside a number ("πέντε και μισό")
    fractions = {"μισό": 0.5, "μισή": 0.5, "μισός": 0.5}
    for den, (singular, _plural) in _FRACTIONS_EL.items():
        if den > 2:
            fractions[singular] = 1.0 / den
    return (_norm_map(units), _norm_map(tens), _norm_map(hundreds),
            _norm_map(scales), _norm_map(fractions))


(_UNITS_LOOKUP, _TENS_LOOKUP, _HUNDREDS_LOOKUP, _SCALES_LOOKUP,
 _FRACTIONS_LOOKUP) = _build_lookup()

_MINUS_LOOKUP = {_normalize_el(w) for w in ("μείον", "πλην")}
_DECIMAL_LOOKUP = {_normalize_el("κόμμα")}
_AND_WORD = _normalize_el("και")


def _gendered(masculine):
    """The three gender forms of an ordinal given the masculine in -ος."""
    stem = masculine[:-2]
    return (masculine, stem + "η", stem + "ο")


def _build_ordinal_lookup():
    units = {}
    for value, w in _ORDINAL_UNITS_EL.items():
        for form in _gendered(w):
            units[form] = value
    # variants: κατά-form feminines and the έντεκα-based 11th
    units.update({"δευτέρα": 2, "εντέκατος": 11, "εντέκατη": 11,
                  "εντέκατο": 11})
    tens = {}
    for value, w in _ORDINAL_TENS_EL.items():
        for form in _gendered(w):
            tens[form] = value
    hundreds = {}
    for value, w in _ORDINAL_HUNDREDS_EL.items():
        for form in _gendered(w):
            hundreds[form] = value
    scales = {}
    for value, w in _ORDINAL_SCALES_EL.items():
        for form in _gendered(w):
            scales[form] = value
    return (_norm_map(units), _norm_map(tens), _norm_map(hundreds),
            _norm_map(scales))


(_ORD_UNITS_LOOKUP, _ORD_TENS_LOOKUP, _ORD_HUNDREDS_LOOKUP,
 _ORD_SCALES_LOOKUP) = _build_ordinal_lookup()


def _is_number(s):
    try:
        # a non-finite token ("inf", "nan", "1e309" or an overflowing digit
        # string) carries no usable number and must not be treated as one
        return isfinite(float(s))
    except ValueError:
        return False


def _tokenize_el(text):
    """Normalize (casefold, strip accents) and split into clean tokens."""
    tokens = []
    for token in _normalize_el(text).split():
        token = token.strip(".!?;:,·")
        if not token:
            continue
        # Greek decimal comma between digits: "3,14" -> "3.14"
        if "," in token:
            parts = token.split(",")
            if len(parts) == 2 and parts[0].lstrip("-").isdigit() \
                    and parts[1].isdigit():
                token = parts[0] + "." + parts[1]
        tokens.append(token)
    return tokens


def _parse_ordinal_span(tokens, i):
    """Try to read an ordinal starting at tokens[i].

    Returns (value, next_index) or (None, i)."""
    n = len(tokens)
    value = 0
    j = i
    if j < n and tokens[j] in _ORD_SCALES_LOOKUP:
        return _ORD_SCALES_LOOKUP[tokens[j]], j + 1
    if j < n and tokens[j] in _ORD_HUNDREDS_LOOKUP:
        value += _ORD_HUNDREDS_LOOKUP[tokens[j]]
        j += 1
    if j < n and tokens[j] in _ORD_TENS_LOOKUP:
        value += _ORD_TENS_LOOKUP[tokens[j]]
        j += 1
        if j < n and tokens[j] in _ORD_UNITS_LOOKUP and \
                1 <= _ORD_UNITS_LOOKUP[tokens[j]] <= 9:
            value += _ORD_UNITS_LOOKUP[tokens[j]]
            j += 1
    elif j < n and tokens[j] in _ORD_UNITS_LOOKUP:
        unit = _ORD_UNITS_LOOKUP[tokens[j]]
        j += 1
        if unit == 10 and j < n and tokens[j] in _ORD_UNITS_LOOKUP and \
                1 <= _ORD_UNITS_LOOKUP[tokens[j]] <= 9:
            # "δέκατος τρίτος" = 13
            unit += _ORD_UNITS_LOOKUP[tokens[j]]
            j += 1
        value += unit
    if j == i:
        return None, i
    return value, j


def _parse_number_span(tokens, i):
    """Parse one number starting at tokens[i].

    Returns (value, next_index); value is None if no number starts here.
    Within a three-digit group only descending ranks are accepted
    (hundreds, then tens, then units), so adjacent separate numbers
    ("ένα δύο") are not merged."""
    total = 0
    current = 0
    started = False
    last_rank = 4
    last_scale = None
    n = len(tokens)
    j = i
    while j < n:
        tok = tokens[j]
        if tok == _AND_WORD and started and j + 1 < n and \
                tokens[j + 1] in _FRACTIONS_LOOKUP:
            j += 1
            continue
        if _is_number(tok):
            if started:
                break
            value = float(tok)
            if value.is_integer():
                value = int(value)
            return value, j + 1
        if tok in _HUNDREDS_LOOKUP and last_rank > 3:
            current += _HUNDREDS_LOOKUP[tok]
            started = True
            last_rank = 3
            j += 1
            continue
        if tok in _TENS_LOOKUP and last_rank > 2:
            current += _TENS_LOOKUP[tok]
            started = True
            last_rank = 2
            j += 1
            continue
        if tok in _UNITS_LOOKUP and last_rank > 1:
            current += _UNITS_LOOKUP[tok]
            started = True
            last_rank = 1
            j += 1
            continue
        if tok in _SCALES_LOOKUP:
            scale = _SCALES_LOOKUP[tok]
            if started and current == 0:
                # a bare scale word directly after another scale word
                if last_scale is not None and scale < last_scale:
                    # descending sequence ("εκατομμύριο χίλια"): add one of it
                    total += scale
                    last_scale = scale
                    j += 1
                    continue
                if last_scale is not None and scale == last_scale:
                    break  # a repeat of the same scale ends the number
                # ascending sequence ("χίλια δισεκατομμύρια"): the smaller
                # scale multiplies the larger one that follows
                total *= scale
                last_scale = scale
                j += 1
                continue
            total += (current if current else 1) * scale
            current = 0
            started = True
            last_rank = 4
            last_scale = scale
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
    """Parse what follows "κόμμα".

    A run of bare digit words is read digit by digit
    ("κόμμα ένα τέσσερα" = .14); otherwise the following number N with d
    integer digits is N / 10^d ("κόμμα είκοσι πέντε" = .25).

    Returns (fraction, next_index) or (None, i)."""
    n = len(tokens)
    digits = []
    j = i
    while j < n and tokens[j] in _UNITS_LOOKUP and \
            _UNITS_LOOKUP[tokens[j]] <= 9:
        digits.append(_UNITS_LOOKUP[tokens[j]])
        j += 1
    if digits:
        return sum(d / 10 ** (k + 1) for k, d in enumerate(digits)), j
    value, j = _parse_number_span(tokens, i)
    if value is None or value != int(value):
        return None, i
    return value / 10 ** len(str(int(value))), j


def extract_numbers_el(text, short_scale=True, ordinals=False):
    """
    Takes in a string and extracts a list of numbers.

    Accepts every gender variant of the numerals and unaccented input.

    Args:
        text (str): the string to extract numbers from
        short_scale (bool): ignored, Greek scale words are unambiguous
        ordinals (bool): consider ordinal numbers ("τρίτος" = 3)
    Returns:
        list: list of extracted numbers as floats
    """
    tokens = _tokenize_el(text)
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
        # decimal part: "κόμμα" + digits or a number
        if j < n and tokens[j] in _DECIMAL_LOOKUP:
            frac, j2 = _parse_decimal_part(tokens, j + 1)
            if frac is not None:
                value += frac
                j = j2
        results.append(-value if negative else value)
        i = j
    return results


def extract_number_el(text, ordinals=False):
    """
    Extract the first number found in Modern Greek text.

    Args:
        text (str): the string to extract a number from
        ordinals (bool): consider ordinal numbers ("τρίτος" = 3)
    Returns:
        (int, float or False): the extracted number, or False if the text
                               contains no number
    """
    numbers = extract_numbers_el(text, ordinals=ordinals)
    if not numbers:
        return False
    value = numbers[0]
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def is_fractional_el(input_str, short_scale=True):
    """
    Check if the given word is a Greek fraction noun.

    Recognizes the fraction nouns for 1/2 .. 1/10 (μισό, τρίτο, τέταρτο,
    πέμπτο, ...) in any gender of "half" and in singular or plural.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): ignored, present for API compatibility
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    word = _normalize_el(input_str.strip())
    if word in (_normalize_el("μισό"), _normalize_el("μισή"),
                _normalize_el("μισός")):
        return 0.5
    for den, (singular, plural) in _FRACTIONS_EL.items():
        if word in (_normalize_el(singular), _normalize_el(plural)):
            return 1.0 / den
    return False


def is_ordinal_el(input_str):
    """
    Check if the given text is a Greek ordinal number in any gender.

    Args:
        input_str (str): the string to check if ordinal
    Returns:
        (bool) or (int): False if not an ordinal, otherwise the number
    """
    tokens = _tokenize_el(input_str)
    if not tokens:
        return False
    value, j = _parse_ordinal_span(tokens, 0)
    if value is not None and j == len(tokens):
        return value
    return False
