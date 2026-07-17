"""Finnish number parsing and pronunciation.

Finnish writes numerals below a million as a single agglutinated word:
21 is "kaksikymmentäyksi" and 345 is "kolmesataaneljäkymmentäviisi".
Inside those compounds the ten, hundred and thousand words appear in the
partitive singular ("kymmentä", "sataa", "tuhatta") whenever the multiplier
is greater than one, while the bare forms "kymmenen", "sata" and "tuhat"
stand alone. "miljoona" and "miljardi" are independent nouns written as
separate words and take the partitive ("kaksi miljoonaa").

References:
    * Kotimaisten kielten keskus (Kotus), Kielitoimiston ohjepankki,
      "Numeraalit" / "Lukusanat"
    * https://fi.wikipedia.org/wiki/Numeraali
    * https://en.wiktionary.org/wiki/Appendix:Finnish_numbers
"""
from math import floor

from ovos_number_parser.util import convert_to_mixed_fraction

_NUM_STRING_FI = {
    0: 'nolla',
    1: 'yksi',
    2: 'kaksi',
    3: 'kolme',
    4: 'neljä',
    5: 'viisi',
    6: 'kuusi',
    7: 'seitsemän',
    8: 'kahdeksan',
    9: 'yhdeksän',
    10: 'kymmenen',
}

# ordinal units; the *_COMPOUND forms are the allomorphs used inside larger
# ordinals (11. "yhdestoista", 12. "kahdestoista")
_ORDINAL_UNITS_FI = {
    1: 'ensimmäinen',
    2: 'toinen',
    3: 'kolmas',
    4: 'neljäs',
    5: 'viides',
    6: 'kuudes',
    7: 'seitsemäs',
    8: 'kahdeksas',
    9: 'yhdeksäs',
    10: 'kymmenes',
}
_ORDINAL_UNITS_COMPOUND_FI = dict(_ORDINAL_UNITS_FI)
_ORDINAL_UNITS_COMPOUND_FI[1] = 'yhdes'
_ORDINAL_UNITS_COMPOUND_FI[2] = 'kahdes'

# fraction denominators: ordinal stem + "osa" is fully productive
# ("kolmasosa"); 3..9 also have the synonymous -nnes nouns ("kolmannes")
_FRACTION_STRING_FI = {
    2: 'puoli',
    3: 'kolmasosa',
    4: 'neljäsosa',
    5: 'viidesosa',
    6: 'kuudesosa',
    7: 'seitsemäsosa',
    8: 'kahdeksasosa',
    9: 'yhdeksäsosa',
    10: 'kymmenesosa',
    11: 'yhdestoistaosa',
    12: 'kahdestoistaosa',
    13: 'kolmastoistaosa',
    14: 'neljästoistaosa',
    15: 'viidestoistaosa',
    16: 'kuudestoistaosa',
    17: 'seitsemästoistaosa',
    18: 'kahdeksastoistaosa',
    19: 'yhdeksästoistaosa',
    20: 'kahdeskymmenesosa',
}

_NNES_FRACTIONS_FI = {
    'kolmannes': 3,
    'neljännes': 4,
    'viidennes': 5,
    'kuudennes': 6,
    'seitsemännes': 7,
    'kahdeksannes': 8,
    'yhdeksännes': 9,
}

_MINUS_FI = ("miinus",)
_DECIMAL_MARKER_FI = ("pilkku",)

# well-attested colloquial short forms (accepted on extraction only)
_COLLOQUIAL_NUM_FI = {
    'yks': 1,
    'kaks': 2,
    'viis': 5,
    'kuus': 6,
    'seittemän': 7,
}


def _pronounce_below_1000_fi(num):
    """Pronounce 1..999 as a single compound word."""
    result = ""
    hundreds = num // 100
    if hundreds:
        result += 'sata' if hundreds == 1 else \
            _NUM_STRING_FI[hundreds] + 'sataa'
        num -= hundreds * 100
    if num == 0:
        pass
    elif num <= 10:
        result += _NUM_STRING_FI[num]
    elif num < 20:
        result += _NUM_STRING_FI[num - 10] + 'toista'
    else:
        tens, ones = divmod(num, 10)
        result += _NUM_STRING_FI[tens] + 'kymmentä'
        if ones:
            result += _NUM_STRING_FI[ones]
    return result


def _pronounce_int_fi(num):
    """Pronounce a non-negative integer."""
    if num == 0:
        return _NUM_STRING_FI[0]
    words = []
    for value, name in ((10 ** 12, 'biljoona'), (10 ** 9, 'miljardi'),
                        (10 ** 6, 'miljoona')):
        count = num // value
        if count:
            if count == 1:
                words.append(name)
            else:
                # miljoona/miljardi are separate nouns in the partitive
                words.append(_pronounce_int_fi(count) + ' ' + name + 'a')
            num -= count * value
    compound = ""
    thousands = num // 1000
    if thousands:
        compound += 'tuhat' if thousands == 1 else \
            _pronounce_below_1000_fi(thousands) + 'tuhatta'
        num -= thousands * 1000
    if num:
        compound += _pronounce_below_1000_fi(num)
    if compound:
        words.append(compound)
    return ' '.join(words)


def pronounce_number_fi(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to its spoken Finnish equivalent.

    For example, 5.2 becomes "viisi pilkku kaksi". Cardinals are composed by
    the multiplication-based rule of Kotimaisten kielten keskus (Kotus),
    Kielitoimiston ohjepankki, "Luvut ja numerot: peruslukujen taivuttaminen":
    the sub-thousand part is one agglutinated word with the partitive
    allomorphs "sataa"/"tuhatta" when the multiplier exceeds one, while
    miljoona/miljardi are separate nouns in the partitive ("kaksi miljoonaa").

    Finnish uses the long scale (Wikipedia, "Long and short scales",
    https://en.wikipedia.org/wiki/Long_and_short_scales): the milliard-cognate
    "miljardi" names 10^9 and the billion-cognate "biljoona" names 10^12.

    Args:
        number(float or int): the number to pronounce
        places(int): maximum decimal places to speak
        short_scale (bool): ignored, Finnish uses its own scale words
        scientific (bool): ignored
        ordinals (bool): pronounce as an ordinal ("ensimmäinen")
    Returns:
        (str): The pronounced number
    """
    if ordinals:
        return pronounce_ordinal_fi(number)
    if abs(number) >= 10 ** 15:  # beyond the supported scale words
        return str(number)
    if number < 0:
        return "miinus " + pronounce_number_fi(abs(number), places)
    if number == int(number):
        return _pronounce_int_fi(int(number))
    result = _pronounce_int_fi(floor(number))
    if places > 0:
        # decimals are read digit by digit after "pilkku"
        fraction = str(round(number - floor(number), places))[2:]
        digits = [_NUM_STRING_FI[int(d)] for d in fraction[:places]]
        result += " pilkku " + " ".join(digits)
    return result


def _ordinal_multiplier_fi(number):
    """Ordinal stem of a scale-word multiplier (before "tuhannes"/"miljoonas").

    A bare multiplier takes the compositive ordinal stem rather than the
    standalone form: 2000th is "kahdestuhannes", not "toinentuhannes". Kotus,
    Kielitoimiston ohjepankki, "järjestyslukujen taivuttaminen", gives the
    compound base "kahdeskymmenesyhdes" (21st), showing the compositive stems
    "yhdes"/"kahdes" carry through compounds instead of "ensimmäinen"/"toinen".
    """
    if number in _ORDINAL_UNITS_COMPOUND_FI and number < 10:
        return _ORDINAL_UNITS_COMPOUND_FI[number]
    return pronounce_ordinal_fi(number)


def pronounce_ordinal_fi(number):
    """
    Pronounce a number as a Finnish ordinal.

    1 -> "ensimmäinen", 2 -> "toinen", 21 -> "kahdeskymmenesensimmäinen",
    2000 -> "kahdestuhannes", 2000000 -> "kahdesmiljoonas"

    Compound ordinals mark every inflectable part with the compositive ordinal
    stem (Kotus, Kielitoimiston ohjepankki, "järjestyslukujen taivuttaminen").

    Args:
        number (int): the number to format
    Returns:
        (str): The pronounced ordinal string.
    """
    # only for whole positive numbers including zero
    if number < 0 or number != int(number):
        return number
    number = int(number)
    if number == 0:
        return 'nollas'
    if number in _ORDINAL_UNITS_FI:
        return _ORDINAL_UNITS_FI[number]
    if number < 20:
        return _ORDINAL_UNITS_COMPOUND_FI[number - 10] + 'toista'
    if number < 100:
        tens, ones = divmod(number, 10)
        result = _ORDINAL_UNITS_COMPOUND_FI[tens] + 'kymmenes'
        if ones:
            result += _ORDINAL_UNITS_FI[ones]
        return result
    if number < 1000 and number % 100 == 0:
        hundreds = number // 100
        return 'sadas' if hundreds == 1 else \
            _ORDINAL_UNITS_COMPOUND_FI[hundreds] + 'sadas'
    if number < 10 ** 6 and number % 1000 == 0:
        thousands = number // 1000
        return 'tuhannes' if thousands == 1 else \
            _ordinal_multiplier_fi(thousands) + 'tuhannes'
    if number < 10 ** 9 and number % 10 ** 6 == 0:
        millions = number // 10 ** 6
        return 'miljoonas' if millions == 1 else \
            _ordinal_multiplier_fi(millions) + 'miljoonas'
    if number >= 10 ** 9:
        # above the supported "miljoonas" scale: fall back to digits rather
        # than composing an unidiomatic mix of words and figures
        return str(number)
    # compose: ordinal prefix from the largest round part + remainder.
    # ``head`` must be a strict prefix of ``number`` or the recursion never
    # shrinks; an exact multiple of a base is handled by the branches above,
    # so a base yielding ``head == number`` here is out of representable range.
    for base in (10 ** 6, 1000, 100):
        if number > base:
            head = (number // base) * base
            if head == number:
                continue
            return pronounce_ordinal_fi(head) + \
                pronounce_ordinal_fi(number - head)
    return str(number)


def nice_number_fi(number, speech=True, denominators=range(1, 21)):
    """Finnish helper for nice_number

    This function formats a float to a human understandable string. Like
    4.5 becomes "4 ja puoli" for speech and "4 1/2" for text

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
    den_str = _FRACTION_STRING_FI[den]
    if num > 1:
        # numerals govern the partitive: "kolme neljäsosaa"
        den_str = 'puolta' if den == 2 else den_str + 'a'
        frac = '{} {}'.format(pronounce_number_fi(num), den_str)
    else:
        frac = den_str
    if whole == 0:
        return frac
    return '{} ja {}'.format(whole, frac)


# word → value map used to split compound numbers, including the partitive
# allomorphs that only appear inside compounds ("kymmentä", "sataa",
# "tuhatta") and the teen suffix "toista"
_STRING_NUM_FI = {word: val for val, word in _NUM_STRING_FI.items()}

_COMPOUND_MULTIPLIERS_FI = {
    'kymmentä': 10,
    'sataa': 100,
    'sata': 100,
    'tuhatta': 1000,
    'tuhat': 1000,
}

_SCALE_WORDS_FI = {
    'miljoona': 10 ** 6,
    'miljoonaa': 10 ** 6,
    'miljardi': 10 ** 9,
    'miljardia': 10 ** 9,
    'biljoona': 10 ** 12,
    'biljoonaa': 10 ** 12,
}


def _split_compound_number_fi(word):
    """Split an agglutinated Finnish numeral into its vocabulary parts.

    Returns the list of matched (word, value) parts, or None if the word is
    not entirely composed of number vocabulary.
    """
    vocab = dict(_STRING_NUM_FI)
    vocab.update(_COMPOUND_MULTIPLIERS_FI)
    vocab['toista'] = 'teen'
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


def _compound_value_fi(parts):
    """Evaluate the value of a split Finnish compound numeral."""
    total = 0
    current = 0
    last_unit = 0
    for word, val in parts:
        if val == 'teen':  # "toista" turns the preceding unit into a teen
            current += 10
            last_unit = 0
        elif word in ('tuhatta', 'tuhat'):
            total += (current or 1) * 1000
            current = 0
            last_unit = 0
        elif word in ('sataa', 'sata', 'kymmentä'):
            mult = _COMPOUND_MULTIPLIERS_FI[word]
            if last_unit:
                current += last_unit * (mult - 1)
            else:
                current += mult
            last_unit = 0
        else:
            current += val
            last_unit = val
    return total + current


def _parse_number_word_fi(word):
    """Parse a single Finnish numeral word (possibly compound) into its
    value, or None."""
    word = word.lower().strip().replace('-', '')
    if not word:
        return None
    if word in _STRING_NUM_FI:
        return _STRING_NUM_FI[word]
    if word in _COLLOQUIAL_NUM_FI:
        return _COLLOQUIAL_NUM_FI[word]
    if word in _COMPOUND_MULTIPLIERS_FI:
        return _COMPOUND_MULTIPLIERS_FI[word]
    if word in _SCALE_WORDS_FI:
        return _SCALE_WORDS_FI[word]
    parts = _split_compound_number_fi(word)
    if parts:
        return _compound_value_fi(parts)
    return None


_ORDINAL_REVERSE_FI = {}


def is_ordinal_fi(input_str):
    """
    Check if the given word is a Finnish ordinal number.

    Args:
        input_str (str): the string to check if ordinal
    Returns:
        (bool) or (int): False if not an ordinal, otherwise the number
    """
    if not _ORDINAL_REVERSE_FI:
        candidates = list(range(0, 101)) + \
            [n * 100 for n in range(1, 11)] + [1000, 10 ** 6]
        for n in candidates:
            _ORDINAL_REVERSE_FI[pronounce_ordinal_fi(n)] = n
    return _ORDINAL_REVERSE_FI.get(input_str.lower().strip(), False)


def is_fractional_fi(input_str, short_scale=True):
    """
    Check if the given word is a Finnish fraction.

    Accepts both the productive ordinal + "osa" pattern ("kolmasosa") and
    the -nnes nouns ("kolmannes", "neljännes"), plus the partitive forms
    that follow numerals ("kolme neljäsosaa").

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): ignored, present for API compatibility
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    word = input_str.lower().strip()
    if word in ('puoli', 'puolta'):
        return 0.5
    for den, den_str in _FRACTION_STRING_FI.items():
        if word in (den_str, den_str + 'a'):
            return 1.0 / den
    if word in _NNES_FRACTIONS_FI:
        return 1.0 / _NNES_FRACTIONS_FI[word]
    return False


def _extract_span_fi(tokens, idx):
    """Parse the number starting at tokens[idx].

    Returns (value, next_index) or None. Consumes multi-token constructs:
    "kaksi miljoonaa", "viisi pilkku kaksi", "kaksi kolmasosaa".
    """
    token = tokens[idx]

    if token == 'puolitoista':
        return 1.5, idx + 1

    # digits, including comma decimals
    cleaned = token.replace(',', '.')
    try:
        val = float(cleaned)
        if val == int(val) and '.' not in cleaned:
            val = int(val)
        return val, idx + 1
    except ValueError:
        pass

    frac = is_fractional_fi(token)
    if frac:
        return frac, idx + 1

    val = _parse_number_word_fi(token)
    if val is None:
        return None
    end = idx + 1

    # Large numbers read as a sequence of "[multiplier] scale" groups followed
    # by a sub-million remainder, and the split follows the written form: the
    # sub-thousand part, the thousands part and each scale part are their own
    # words (Kotus, Kielitoimiston ohjepankki, "Luvut ja numerot: numeroina
    # vai kirjoitettuina sanoina?"). A multiplier of one is written bare
    # ("miljoona", not "yksi miljoonaa"), so a scale noun can head the number
    # with no preceding multiplier; the remainder that follows must still be
    # added ("miljoona viisisataatuhatta" = 1 500 000).
    total = 0
    if token in _SCALE_WORDS_FI:
        total = _SCALE_WORDS_FI[token]
        val = 0
        if end < len(tokens):
            nxt = _parse_number_word_fi(tokens[end])
            if nxt is not None and (end + 1 >= len(tokens)
                                    or tokens[end + 1] in _SCALE_WORDS_FI
                                    or nxt < 10 ** 6):
                val = nxt
                end += 1

    # separate scale nouns: "kaksi miljoonaa"
    while end < len(tokens) and tokens[end] in _SCALE_WORDS_FI:
        total += val * _SCALE_WORDS_FI[tokens[end]]
        end += 1
        val = 0
        # a following smaller group continues the same number
        # ("kaksi miljoonaa kolmesataatuhatta")
        if end < len(tokens):
            nxt = _parse_number_word_fi(tokens[end])
            if nxt is not None and (end + 1 >= len(tokens)
                                    or tokens[end + 1] in _SCALE_WORDS_FI
                                    or nxt < 10 ** 6):
                val = nxt
                end += 1
                if end >= len(tokens) or tokens[end] not in _SCALE_WORDS_FI:
                    break
    val += total

    # "kaksi kolmasosaa" → 2/3
    if end < len(tokens):
        frac = is_fractional_fi(tokens[end])
        if frac:
            return val * frac, end + 1

    # decimals: "viisi pilkku kaksi kolme" → 5.23
    if end + 1 < len(tokens) and tokens[end] in _DECIMAL_MARKER_FI:
        digits = []
        j = end + 1
        while j < len(tokens):
            d = _parse_number_word_fi(tokens[j])
            if d is None or d > 9:
                break
            digits.append(str(d))
            j += 1
        if digits:
            return float(str(val) + '.' + ''.join(digits)), j
    return val, end


def extract_number_fi(text, short_scale=True, ordinals=False):
    """
    Extract the first number from Finnish text.

    A written Finnish number splits into parts the same way as its digits: the
    sub-thousand part is one agglutinated word, the thousands part is one word,
    and each scale part (miljoona, miljardi) is its own word, per Kotimaisten
    kielten keskus (Kotus), Kielitoimiston ohjepankki, "Luvut ja numerot:
    numeroina vai kirjoitettuina sanoina?" and "peruslukujen taivuttaminen".
    A multiplier of one is written bare ("miljoona", not "yksi miljoonaa"), so
    a scale noun may head the number with the remainder following it
    ("miljoona viisisataatuhatta" = 1 500 000).

    Args:
        text (str): the string to normalize
        short_scale (bool): ignored, Finnish uses its own scale words
        ordinals (bool): consider ordinal numbers ("toinen" → 2)
    Returns:
        (int, float or False): the extracted number or False if no number
                               was found
    """
    tokens = [t.strip('.,!?;:').lower() for t in text.split()]
    tokens = [t for t in tokens if t]
    for idx in range(len(tokens)):
        negative = idx > 0 and tokens[idx - 1] in _MINUS_FI
        if ordinals:
            val = is_ordinal_fi(tokens[idx])
            if val is not False:
                return -val if negative else val
        span = _extract_span_fi(tokens, idx)
        if span is None:
            continue
        val = span[0]
        return -val if negative else val
    return False


def extract_numbers_fi(text, short_scale=True, ordinals=False):
    """
    Extract all numbers from Finnish text.

    Args:
        text (str): the string to extract numbers from
        short_scale (bool): ignored, Finnish uses its own scale words
        ordinals (bool): consider ordinal numbers
    Returns:
        list: list of extracted numbers
    """
    tokens = [t.strip('.,!?;:').lower() for t in text.split()]
    tokens = [t for t in tokens if t]
    results = []
    idx = 0
    while idx < len(tokens):
        negative = tokens[idx] in _MINUS_FI and idx + 1 < len(tokens)
        start = idx + 1 if negative else idx
        if ordinals and start < len(tokens):
            val = is_ordinal_fi(tokens[start])
            if val is not False:
                results.append(-val if negative else val)
                idx = start + 1
                continue
        span = _extract_span_fi(tokens, start) if start < len(tokens) else None
        if span is None:
            idx += 1
            continue
        val, idx = span
        results.append(-val if negative else val)
    return results
