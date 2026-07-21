"""Estonian number parsing and pronunciation.

Estonian agglutinates teens ("kaksteist" = 12), tens ("kakskümmend" = 20)
and hundreds ("kakssada" = 200) into single words, but writes the remaining
numeral words separately: 21 is "kakskümmend üks" (two words) and 2500 is
"kaks tuhat viissada". The scale nouns "miljon" and "miljard" follow a
numeral in the partitive ("kaks miljonit").

References:
    * Eesti Keele Instituut (EKI), Eesti keele käsiraamat, "Arvsõnad"
      (õigekiri: põhiarvsõnad kirjutatakse kokku ainult -teist(kümmend),
      -kümmend ja -sada liitumites, muidu lahku)
    * https://et.wikipedia.org/wiki/Arvs%C3%B5na
    * https://en.wiktionary.org/wiki/Appendix:Estonian_numbers
"""
from math import floor, isfinite

from ovos_number_parser.util import convert_to_mixed_fraction

_NUM_STRING_ET = {
    0: 'null',
    1: 'üks',
    2: 'kaks',
    3: 'kolm',
    4: 'neli',
    5: 'viis',
    6: 'kuus',
    7: 'seitse',
    8: 'kaheksa',
    9: 'üheksa',
    10: 'kümme',
}

# genitive stems used inside ordinals ("kahekümnes" = 20th)
_GENITIVE_UNITS_ET = {
    1: 'ühe',
    2: 'kahe',
    3: 'kolme',
    4: 'nelja',
    5: 'viie',
    6: 'kuue',
    7: 'seitsme',
    8: 'kaheksa',
    9: 'üheksa',
}

_ORDINAL_UNITS_ET = {
    1: 'esimene',
    2: 'teine',
    3: 'kolmas',
    4: 'neljas',
    5: 'viies',
    6: 'kuues',
    7: 'seitsmes',
    8: 'kaheksas',
    9: 'üheksas',
    10: 'kümnes',
}

_FRACTION_STRING_ET = {
    2: 'pool',
    3: 'kolmandik',
    4: 'neljandik',
    5: 'viiendik',
    6: 'kuuendik',
    7: 'seitsmendik',
    8: 'kaheksandik',
    9: 'üheksandik',
    10: 'kümnendik',
    11: 'üheteistkümnendik',
    12: 'kaheteistkümnendik',
    13: 'kolmeteistkümnendik',
    14: 'neljateistkümnendik',
    15: 'viieteistkümnendik',
    16: 'kuueteistkümnendik',
    17: 'seitsmeteistkümnendik',
    18: 'kaheksateistkümnendik',
    19: 'üheksateistkümnendik',
    20: 'kahekümnendik',
}

_MINUS_ET = ("miinus",)
_DECIMAL_MARKER_ET = ("koma",)


def _pronounce_below_1000_et(num):
    """Pronounce 1..999; -sada, -kümmend and -teist join into one word,
    everything else is a separate word."""
    words = []
    hundreds = num // 100
    if hundreds:
        words.append('sada' if hundreds == 1 else
                     _NUM_STRING_ET[hundreds] + 'sada')
        num -= hundreds * 100
    if num == 0:
        pass
    elif num <= 10:
        words.append(_NUM_STRING_ET[num])
    elif num < 20:
        words.append(_NUM_STRING_ET[num - 10] + 'teist')
    else:
        tens, ones = divmod(num, 10)
        word = _NUM_STRING_ET[tens] + 'kümmend'
        words.append(word)
        if ones:
            words.append(_NUM_STRING_ET[ones])
    return ' '.join(words)


def _pronounce_int_et(num):
    """Pronounce a non-negative integer."""
    if num == 0:
        return _NUM_STRING_ET[0]
    words = []
    for value, name, partitive in ((10 ** 12, 'biljon', 'biljonit'),
                                   (10 ** 9, 'miljard', 'miljardit'),
                                   (10 ** 6, 'miljon', 'miljonit')):
        count = num // value
        if count:
            if count == 1:
                words.append(name)
            else:
                words.append(_pronounce_int_et(count) + ' ' + partitive)
            num -= count * value
    thousands = num // 1000
    if thousands:
        if thousands == 1:
            words.append('tuhat')
        else:
            words.append(_pronounce_below_1000_et(thousands) + ' tuhat')
        num -= thousands * 1000
    if num:
        words.append(_pronounce_below_1000_et(num))
    return ' '.join(words)


def pronounce_number_et(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to its spoken Estonian equivalent.

    For example, 5.2 becomes "viis koma kaks".

    Estonian uses the long scale (Wikipedia, "Long and short scales",
    https://en.wikipedia.org/wiki/Long_and_short_scales): the milliard-cognate
    "miljard" names 10^9 and the billion-cognate "biljon" names 10^12.

    Args:
        number(float or int): the number to pronounce
        places(int): maximum decimal places to speak
        short_scale (bool): ignored, Estonian uses its own scale words
        scientific (bool): ignored
        ordinals (bool): pronounce as an ordinal ("esimene")
    Returns:
        (str): The pronounced number
    """
    if ordinals:
        return pronounce_ordinal_et(number)
    if abs(number) >= 10 ** 15:  # beyond the supported scale words
        return str(number)
    if number < 0:
        return "miinus " + pronounce_number_et(abs(number), places)
    if number == int(number):
        return _pronounce_int_et(int(number))
    result = _pronounce_int_et(floor(number))
    if places > 0:
        # decimals are read digit by digit after "koma"
        fraction = str(round(number - floor(number), places))[2:]
        digits = [_NUM_STRING_ET[int(d)] for d in fraction[:places]]
        result += " koma " + " ".join(digits)
    return result


def pronounce_ordinal_et(number):
    """
    Pronounce a number as an Estonian ordinal.

    1 -> "esimene", 2 -> "teine", 21 -> "kahekümne esimene"

    Args:
        number (int): the number to format
    Returns:
        (str): The pronounced ordinal string.
    """
    # only for whole positive numbers
    if number < 1 or number != int(number):
        return number
    number = int(number)
    if number in _ORDINAL_UNITS_ET:
        return _ORDINAL_UNITS_ET[number]
    if number < 20:
        return _GENITIVE_UNITS_ET[number - 10] + 'teistkümnes'
    if number < 100:
        tens, ones = divmod(number, 10)
        tens_ordinal = _GENITIVE_UNITS_ET[tens] + 'kümnes'
        if not ones:
            return tens_ordinal
        # the leading part goes to the genitive: "kahekümne esimene"
        return _GENITIVE_UNITS_ET[tens] + 'kümne ' + _ORDINAL_UNITS_ET[ones]
    if number < 1000 and number % 100 == 0:
        hundreds = number // 100
        return 'sajas' if hundreds == 1 else \
            _GENITIVE_UNITS_ET[hundreds] + 'sajas'
    if number < 10 ** 6 and number % 1000 == 0 and number // 1000 <= 10:
        thousands = number // 1000
        return 'tuhandes' if thousands == 1 else \
            _GENITIVE_UNITS_ET[thousands] + 'tuhandes'
    if number == 10 ** 6:
        return 'miljones'
    # compose: genitive round part + ordinal remainder ("saja esimene")
    if 100 < number < 1000:
        hundreds = number // 100
        head = 'saja' if hundreds == 1 else \
            _GENITIVE_UNITS_ET[hundreds] + 'saja'
        return head + ' ' + pronounce_ordinal_et(number % 100)
    if 1000 < number < 10 ** 6:
        thousands = number // 1000
        head = 'tuhande' if thousands == 1 else \
            _pronounce_int_et(thousands) + ' tuhande'
        return head + ' ' + pronounce_ordinal_et(number % 1000)
    return str(number)


def nice_number_et(number, speech=True, denominators=range(1, 21)):
    """Estonian helper for nice_number

    This function formats a float to a human understandable string. Like
    4.5 becomes "4 ja pool" for speech and "4 1/2" for text

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
        return str(round(number, 3)).replace(".", ",")

    whole, num, den = result

    if not speech:
        if num == 0:
            return str(whole)
        return '{} {}/{}'.format(whole, num, den)

    if num == 0:
        return str(whole)
    den_str = _FRACTION_STRING_ET[den]
    if num > 1:
        # numerals govern the partitive: "kaks kolmandikku"
        den_str = 'poolt' if den == 2 else den_str + 'ku'
        frac = '{} {}'.format(pronounce_number_et(num), den_str)
    else:
        frac = den_str
    if whole == 0:
        return frac
    return '{} ja {}'.format(whole, frac)


# word → value map used to split compound numbers, including the suffixes
# that only appear inside compounds ("teist", "kümmend", "sada")
_STRING_NUM_ET = {word: val for val, word in _NUM_STRING_ET.items()}

_COMPOUND_MULTIPLIERS_ET = {
    'kümmend': 10,
    'sada': 100,
}

_SCALE_WORDS_ET = {
    'tuhat': 1000,
    'tuhande': 1000,
    'miljon': 10 ** 6,
    'miljonit': 10 ** 6,
    'miljard': 10 ** 9,
    'miljardit': 10 ** 9,
    'biljon': 10 ** 12,
    'biljonit': 10 ** 12,
}


def _split_compound_number_et(word):
    """Split an agglutinated Estonian numeral ("kakskümmend", "viissada")
    into its vocabulary parts.

    Returns the list of matched (word, value) parts, or None if the word is
    not entirely composed of number vocabulary.
    """
    vocab = dict(_STRING_NUM_ET)
    vocab.update(_COMPOUND_MULTIPLIERS_ET)
    vocab['teist'] = 'teen'
    keys = sorted(vocab, key=len, reverse=True)
    parts = []
    rest = word
    while rest:
        for key in keys:
            if rest.startswith(key):
                parts.append((key, vocab[key]))
                rest = rest[len(key):]
                break
        else:
            return None
    return parts


def _compound_value_et(parts):
    """Evaluate the value of a split Estonian compound numeral."""
    current = 0
    last_unit = 0
    for word, val in parts:
        if val == 'teen':  # "teist" turns the preceding unit into a teen
            current += 10
            last_unit = 0
        elif word in _COMPOUND_MULTIPLIERS_ET:
            mult = _COMPOUND_MULTIPLIERS_ET[word]
            if last_unit:
                current += last_unit * (mult - 1)
            else:
                current += mult
            last_unit = 0
        else:
            current += val
            last_unit = val
    return current


def _parse_number_word_et(word):
    """Parse a single Estonian numeral word (possibly compound) into its
    value, or None."""
    word = word.lower().strip().replace('-', '')
    if not word:
        return None
    if word in _STRING_NUM_ET:
        return _STRING_NUM_ET[word]
    if word in _COMPOUND_MULTIPLIERS_ET:
        return _COMPOUND_MULTIPLIERS_ET[word]
    if word in _SCALE_WORDS_ET:
        return _SCALE_WORDS_ET[word]
    parts = _split_compound_number_et(word)
    if parts:
        return _compound_value_et(parts)
    return None


_ORDINAL_REVERSE_ET = {}


def is_ordinal_et(input_str):
    """
    Check if the given word is an Estonian ordinal number.

    Args:
        input_str (str): the string to check if ordinal
    Returns:
        (bool) or (int): False if not an ordinal, otherwise the number
    """
    if not _ORDINAL_REVERSE_ET:
        candidates = list(range(1, 101)) + \
            [n * 100 for n in range(1, 11)] + [1000, 10 ** 6]
        for n in candidates:
            _ORDINAL_REVERSE_ET[pronounce_ordinal_et(n)] = n
    return _ORDINAL_REVERSE_ET.get(input_str.lower().strip(), False)


def is_fractional_et(input_str, short_scale=True):
    """
    Check if the given word is an Estonian fraction.

    Accepts the -ndik nouns ("kolmandik"), their partitive forms that
    follow numerals ("kaks kolmandikku"), plus "pool" (1/2) and
    "veerand" (1/4).

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): ignored, present for API compatibility
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    word = input_str.lower().strip()
    if word in ('pool', 'poolt'):
        return 0.5
    if word in ('veerand', 'veerandit'):
        return 0.25
    for den, den_str in _FRACTION_STRING_ET.items():
        if word in (den_str, den_str + 'ku'):
            return 1.0 / den
    return False


def _extract_span_et(tokens, idx):
    """Parse the number starting at tokens[idx].

    Returns (value, next_index) or None. Numerals above the hundreds are
    written as separate words in Estonian, so consecutive number tokens are
    accumulated: "kakskümmend üks" = 21, "kaks tuhat viissada" = 2500.
    """
    token = tokens[idx]

    if token == 'poolteist':
        return 1.5, idx + 1

    # digits, including comma decimals
    cleaned = token.replace(',', '.')
    try:
        val = float(cleaned)
        if isfinite(val):
            if val == int(val) and '.' not in cleaned:
                val = int(val)
            return val, idx + 1
    except ValueError:
        pass

    frac = is_fractional_et(token)
    if frac:
        return frac, idx + 1

    if _parse_number_word_et(token) is None:
        return None

    # accumulate the separately written numeral words
    total = 0
    current = 0
    prev = None
    end = idx
    while end < len(tokens):
        word = tokens[end]
        if word in _SCALE_WORDS_ET:
            total += (current or 1) * _SCALE_WORDS_ET[word]
            current = 0
            prev = None
            end += 1
            continue
        val = _parse_number_word_et(word)
        if val is None:
            break
        # a number word only continues the span while values descend
        # ("kakskümmend üks"); otherwise it starts a new number
        if prev is not None and val >= prev:
            break
        current += val
        prev = val
        end += 1
    val = total + current

    # "kaks kolmandikku" → 2/3
    if end < len(tokens):
        frac = is_fractional_et(tokens[end])
        if frac:
            return val * frac, end + 1

    # decimals: "viis koma kaks kolm" → 5.23
    if end + 1 < len(tokens) and tokens[end] in _DECIMAL_MARKER_ET:
        digits = []
        j = end + 1
        while j < len(tokens):
            d = _parse_number_word_et(tokens[j])
            if d is None or d > 9:
                break
            digits.append(str(d))
            j += 1
        if digits:
            return float(str(val) + '.' + ''.join(digits)), j
    return val, end


def extract_number_et(text, short_scale=True, ordinals=False):
    """
    Extract the first number from Estonian text.

    Args:
        text (str): the string to normalize
        short_scale (bool): ignored, Estonian uses its own scale words
        ordinals (bool): consider ordinal numbers ("teine" → 2)
    Returns:
        (int, float or False): the extracted number or False if no number
                               was found
    """
    tokens = [t.strip('.,!?;:').lower() for t in text.split()]
    tokens = [t for t in tokens if t]
    for idx in range(len(tokens)):
        negative = idx > 0 and tokens[idx - 1] in _MINUS_ET
        if ordinals:
            val = is_ordinal_et(tokens[idx])
            if val is not False:
                return -val if negative else val
        span = _extract_span_et(tokens, idx)
        if span is None:
            continue
        val = span[0]
        return -val if negative else val
    return False


def extract_numbers_et(text, short_scale=True, ordinals=False):
    """
    Extract all numbers from Estonian text.

    Args:
        text (str): the string to extract numbers from
        short_scale (bool): ignored, Estonian uses its own scale words
        ordinals (bool): consider ordinal numbers
    Returns:
        list: list of extracted numbers
    """
    tokens = [t.strip('.,!?;:').lower() for t in text.split()]
    tokens = [t for t in tokens if t]
    results = []
    idx = 0
    while idx < len(tokens):
        negative = tokens[idx] in _MINUS_ET and idx + 1 < len(tokens)
        start = idx + 1 if negative else idx
        if ordinals and start < len(tokens):
            val = is_ordinal_et(tokens[start])
            if val is not False:
                results.append(-val if negative else val)
                idx = start + 1
                continue
        span = _extract_span_et(tokens, start) if start < len(tokens) else None
        if span is None:
            idx += 1
            continue
        val, idx = span
        results.append(-val if negative else val)
    return results
