from collections import OrderedDict

import re
from ovos_number_parser.util import (invert_dict, convert_to_mixed_fraction, tokenize, look_for_fractions,
                                     partition_list, is_numeric, Token, ReplaceableNumber)

_NUM_STRING_SK = {
    0: 'nula',
    1: 'jeden',
    2: 'dva',
    3: 'tri',
    4: 'štyri',
    5: 'päť',
    6: 'šesť',
    7: 'sedem',
    8: 'osem',
    9: 'deväť',
    10: 'desať',
    11: 'jedenásť',
    12: 'dvanásť',
    13: 'trinásť',
    14: 'štrnásť',
    15: 'pätnásť',
    16: 'šestnásť',
    17: 'sedemnásť',
    18: 'osemnásť',
    19: 'devätnásť',
    20: 'dvadsať',
    30: 'tridsať',
    40: 'štyridsať',
    50: 'päťdesiat',
    60: 'šesťdesiat',
    70: 'sedemdesiat',
    80: 'osemdesiat',
    90: 'deväťdesiat'
}

# multiples of one hundred are single compound words in Slovak
_HUNDREDS_SK = {
    1: 'sto',
    2: 'dvesto',
    3: 'tristo',
    4: 'štyristo',
    5: 'päťsto',
    6: 'šesťsto',
    7: 'sedemsto',
    8: 'osemsto',
    9: 'deväťsto'
}

_FRACTION_STRING_SK = {
    2: 'polovica',
    3: 'tretina',
    4: 'štvrtina',
    5: 'pätina',
    6: 'šestina',
    7: 'sedmina',
    8: 'osmina',
    9: 'devätina',
    10: 'desatina',
    11: 'jedenástina',
    12: 'dvanástina',
    13: 'trinástina',
    14: 'štrnástina',
    15: 'pätnástina',
    16: 'šestnástina',
    17: 'sedemnástina',
    18: 'osemnástina',
    19: 'devätnástina',
    20: 'dvadsatina',
    30: 'tridsatina',
    40: 'štyridsatina',
    50: 'päťdesiatina',
    60: 'šesťdesiatina',
    70: 'sedemdesiatina',
    80: 'osemdesiatina',
    90: 'deväťdesiatina',
    1e2: 'stotina',
    1e3: 'tisícina'
}

# Slovak uses the long scale (milión, miliarda, bilión, ...)
_SCALE_SK = OrderedDict([
    (100, 'sto'),
    (1000, 'tisíc'),
    (1000000, 'milión'),
    (10 ** 9, 'miliarda'),
    (10 ** 12, 'bilión'),
    (10 ** 15, 'biliarda'),
    (10 ** 18, 'trilión'),
    (10 ** 21, 'triliarda'),
    (10 ** 24, 'kvadrilión')
])

_ORDINAL_BASE_SK = {
    1: 'prvý',
    2: 'druhý',
    3: 'tretí',
    4: 'štvrtý',
    5: 'piaty',
    6: 'šiesty',
    7: 'siedmy',
    8: 'ôsmy',
    9: 'deviaty',
    10: 'desiaty',
    11: 'jedenásty',
    12: 'dvanásty',
    13: 'trinásty',
    14: 'štrnásty',
    15: 'pätnásty',
    16: 'šestnásty',
    17: 'sedemnásty',
    18: 'osemnásty',
    19: 'devätnásty',
    20: 'dvadsiaty',
    30: 'tridsiaty',
    40: 'štyridsiaty',
    50: 'päťdesiaty',
    60: 'šesťdesiaty',
    70: 'sedemdesiaty',
    80: 'osemdesiaty',
    90: 'deväťdesiaty',
    1e2: 'stý',
    1e3: 'tisíci'
}

_ORDINAL_SK = {
    1e6: 'miliónty'
}
_ORDINAL_SK.update(_ORDINAL_BASE_SK)

_ORDINAL_HUNDREDS_SK = {
    200: 'dvojstý', 300: 'trojstý', 400: 'štvorstý', 500: 'päťstý',
    600: 'šesťstý', 700: 'sedemstý', 800: 'osemstý', 900: 'deväťstý',
}

# negate next number (-2 = 0 - 2)
_NEGATIVES_SK = {"záporné", "mínus"}

# sum the next number (dvadsať jeden = 20 + 1)
_SUMS_SK = {'dvadsať', '20', 'tridsať', '30', 'štyridsať', '40',
            'päťdesiat', '50', 'šesťdesiat', '60', 'sedemdesiat', '70',
            'osemdesiat', '80', 'deväťdesiat', '90'}

# declined forms of scale words ("dva tisíce", "tri milióny", "päť miliónov")
# and the compound hundreds, all of which multiply the preceding numeral
_SCALE_DECLENSIONS_SK = {
    "tisíce": 1000,
    "milióny": 1000000,
    "miliónov": 1000000,
    "miliardy": 10 ** 9,
    "miliárd": 10 ** 9,
    "bilióny": 10 ** 12,
    "biliónov": 10 ** 12,
    "biliardy": 10 ** 15,
    "biliárd": 10 ** 15,
}
_SCALE_DECLENSIONS_SK.update(
    {word: n * 100 for n, word in _HUNDREDS_SK.items() if n > 1})

_MULTIPLIES_SK = set(_SCALE_SK.values()) | set(_SCALE_DECLENSIONS_SK)

# split sentence parse separately and sum ( 2 and a half = 2 + 0.5 )
_FRACTION_MARKER_SK = {"a"}

# decimal marker ( "päť celá dva" = 5.2 )
_DECIMAL_MARKER_SK = {"celá", "celé", "celých", "čiarka", "bod"}

# the pieces a joined tens-units compound can be split into
_TENS_WORDS_SK = [_NUM_STRING_SK[n] for n in range(90, 10, -10)]
_UNIT_WORDS_SK = {_NUM_STRING_SK[n] for n in range(1, 10)} | {"jedna", "dve"}

_STRING_NUM_SK = invert_dict(_NUM_STRING_SK)
_STRING_NUM_SK.update({
    "jedna": 1,
    "jedno": 1,
    "dve": 2,
    "polovica": 0.5,
    "pol": 0.5,
})


def _scale_declined_sk(word, count):
    """Return the Slovak form of a scale word for a given multiplier."""
    if count == 1:
        return word
    few = 2 <= count <= 4
    if word == "tisíc":
        return "tisíce" if few else "tisíc"
    if word.endswith("ión"):
        return word + ("y" if few else "ov")
    if word.endswith("iarda"):
        return word[:-1] + "y" if few else word[:-4] + "árd"
    return word


def _text_sk_inflection_normalize(word):
    """Normalize known Slovak inflections of "jeden" and "dva"."""
    if word in ("jedna", "jedno", "jedny"):
        return "jeden"
    if word == "dve":
        return "dva"
    return word


def _expand_compound_numbers_sk(text):
    """Split the joined tens-units spellings into their component words.

    Slovak writes 21-99 as one word (dvadsaťjeden); the extractor works on
    number words, so the compounds are separated before tokenizing. Both
    spellings therefore parse.
    """
    words = []
    for word in text.split():
        lowered = word.lower()
        for tens_word in _TENS_WORDS_SK:
            if lowered.startswith(tens_word) and lowered != tens_word:
                rest = lowered[len(tens_word):]
                if rest in _UNIT_WORDS_SK:
                    words.append(tens_word)
                    words.append(rest)
                    break
        else:
            words.append(word)
    return " ".join(words)


def numbers_to_digits_sk(text, short_scale=True, ordinals=False):
    """
    Convert words in a string into their equivalent numbers.
    Args:
        text str:
        short_scale boolean: True if short scale numbers should be used.
        ordinals boolean: True if ordinals (e.g. first, second, third) should
                          be parsed to their number values (1, 2, 3...)

    Returns:
        str
        The original text, with numbers subbed in where appropriate.

    """
    text = _expand_compound_numbers_sk(text.lower())
    tokens = tokenize(text)
    numbers_to_replace = \
        _extract_numbers_with_text_sk(tokens, short_scale, ordinals)
    numbers_to_replace.sort(key=lambda number: number.start_index)

    results = []
    for token in tokens:
        if not numbers_to_replace or \
                token.index < numbers_to_replace[0].start_index:
            results.append(token.word)
        else:
            if numbers_to_replace and \
                    token.index == numbers_to_replace[0].start_index:
                results.append(str(numbers_to_replace[0].value))
            if numbers_to_replace and \
                    token.index == numbers_to_replace[0].end_index:
                numbers_to_replace.pop(0)

    return ' '.join(results)


def _extract_numbers_with_text_sk(tokens, short_scale=True,
                                  ordinals=False, fractional_numbers=True):
    """
    Extract all numbers from a list of Tokens, with the words that
    represent them.

    Args:
        [Token]: The tokens to parse.
        short_scale bool: True if short scale numbers should be used, False for
                          long scale. True by default.
        ordinals bool: True if ordinal words (first, second, third, etc) should
                       be parsed.
        fractional_numbers bool: True if we should look for fractions and
                                 decimals.

    Returns:
        [ReplaceableNumber]: A list of tuples, each containing a number and a
                         string.

    """
    placeholder = "<placeholder>"  # inserted to maintain correct indices
    results = []
    while True:
        to_replace = \
            _extract_number_with_text_sk(tokens, short_scale,
                                         ordinals, fractional_numbers)

        if not to_replace:
            break

        results.append(to_replace)

        tokens = [
            t if not
            to_replace.start_index <= t.index <= to_replace.end_index
            else
            Token(placeholder, t.index) for t in tokens
        ]
    results.sort(key=lambda n: n.start_index)
    return results


def _extract_number_with_text_sk(tokens, short_scale=True,
                                 ordinals=False, fractional_numbers=True):
    """
    This function extracts a number from a list of Tokens.

    Args:
        tokens str: the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
        fractional_numbers (bool): True if we should look for fractions and
                                   decimals.
    Returns:
        ReplaceableNumber

    """
    number, tokens = \
        _extract_number_with_text_sk_helper(tokens, short_scale,
                                            ordinals, fractional_numbers)
    return ReplaceableNumber(number, tokens)


def _extract_number_with_text_sk_helper(tokens,
                                        short_scale=True, ordinals=False,
                                        fractional_numbers=True):
    """
    Helper for _extract_number_with_text_sk.

    Args:
        tokens [Token]:
        short_scale boolean:
        ordinals boolean:
        fractional_numbers boolean:

    Returns:
        int or float, [Tokens]

    """
    if fractional_numbers:
        fraction, fraction_text = \
            _extract_fraction_with_text_sk(tokens, short_scale, ordinals)
        if fraction:
            return fraction, fraction_text

        decimal, decimal_text = \
            _extract_decimal_with_text_sk(tokens, short_scale, ordinals)
        if decimal:
            return decimal, decimal_text

    return _extract_whole_number_with_text_sk(tokens, short_scale, ordinals)


def _extract_fraction_with_text_sk(tokens, short_scale, ordinals):
    """
    Extract fraction numbers from a string ("dva a pol").

    Args:
        tokens [Token]: words and their indexes in the original string.
        short_scale boolean:
        ordinals boolean:

    Returns:
        (int or float, [Token])
        The value found, and the list of relevant tokens.
        (None, None) if no fraction value is found.

    """
    for c in _FRACTION_MARKER_SK:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_sk(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_sk(partitions[2], short_scale,
                                              ordinals, fractional_numbers=True)

            if not numbers1 or not numbers2:
                return None, None

            # ensure first is not a fraction and second is a fraction
            num1 = numbers1[-1]
            num2 = numbers2[0]
            if num1.value >= 1 and 0 < num2.value < 1:
                return num1.value + num2.value, \
                       num1.tokens + partitions[1] + num2.tokens

    return None, None


def _extract_decimal_with_text_sk(tokens, short_scale, ordinals):
    """
    Extract decimal numbers from a string ("päť celá dva").

    Args:
        tokens [Token]: The text to parse.
        short_scale boolean:
        ordinals boolean:

    Returns:
        (float, [Token])
        The value found and relevant tokens.
        (None, None) if no decimal value is found.

    """
    for c in _DECIMAL_MARKER_SK:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_sk(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_sk(partitions[2], short_scale,
                                              ordinals, fractional_numbers=False)

            if not numbers1 or not numbers2:
                return None, None

            number = numbers1[-1]
            decimal = numbers2[0]
            # concatenate consecutive single digits after the marker
            # ("celá jeden štyri" -> .14)
            _digits = ""
            _digit_tokens = []
            _prev_end = None
            for _num in numbers2:
                _v = _num.value
                if _v is None or _v is False or float(_v) != int(_v) \
                        or not 0 <= _v <= 9:
                    break
                if _prev_end is not None and _num.start_index != _prev_end + 1:
                    break
                _digits += str(int(_v))
                _digit_tokens.extend(_num.tokens)
                _prev_end = _num.end_index
            if len(_digits) > 1:
                _frac = float("0." + _digits)
                return (number.value - _frac if number.value < 0
                        else number.value + _frac), \
                    number.tokens + partitions[1] + _digit_tokens

            if "." not in str(decimal.text):
                _frac2 = float('0.' + str(decimal.value))
                return (number.value - _frac2 if number.value < 0
                        else number.value + _frac2), \
                       number.tokens + partitions[1] + decimal.tokens
    return None, None


def _extract_whole_number_with_text_sk(tokens, short_scale, ordinals):
    """
    Handle numbers not handled by the decimal or fraction functions.

    Args:
        tokens [Token]:
        short_scale boolean:
        ordinals boolean:

    Returns:
        int or float, [Tokens]
        The value parsed, and tokens that it corresponds to.

    """
    multiplies, string_num_ordinal, string_num_scale = \
        _initialize_number_data_sk(short_scale)

    number_words = []  # type: [Token]
    val = False
    prev_val = None
    next_val = None
    negative = False
    to_sum = []
    for idx, token in enumerate(tokens):
        current_val = None
        if next_val:
            next_val = None
            continue

        word = token.word
        if word in _NEGATIVES_SK:
            negative = True
            number_words.append(token)
            continue

        prev_word = tokens[idx - 1].word if idx > 0 else ""
        next_word = tokens[idx + 1].word if idx + 1 < len(tokens) else ""

        # Slovak marks written ordinals with a trailing point (1., 2., ...)
        if is_numeric(word[:-1]) and word.endswith("."):
            word = word[:-1]

        # Normalize Slovak inflection of numbers (jedna, jedno, dve, ...)
        if not ordinals:
            word = _text_sk_inflection_normalize(word)

        if word not in string_num_scale and \
                word not in _STRING_NUM_SK and \
                word not in _SUMS_SK and \
                word not in multiplies and \
                not (ordinals and word in string_num_ordinal) and \
                not is_numeric(word) and \
                not is_fractional_sk(word, short_scale=short_scale) and \
                not look_for_fractions(word.split('/')):
            words_only = [token.word for token in number_words]
            if number_words and not all([w in _NEGATIVES_SK for w in words_only]):
                break
            else:
                number_words = []
                continue
        elif word not in multiplies \
                and prev_word not in multiplies \
                and prev_word not in _SUMS_SK \
                and not (ordinals and prev_word in string_num_ordinal) \
                and prev_word not in _NEGATIVES_SK:
            number_words = [token]
        elif prev_word in _SUMS_SK and word in _SUMS_SK:
            number_words = [token]
        else:
            number_words.append(token)

        # is this word already a number ?
        if is_numeric(word):
            if word.isdigit():  # doesn't work with decimals
                val = int(word)
            else:
                val = float(word)
            current_val = val

        # is this word the name of a number ?
        if word in _STRING_NUM_SK:
            val = _STRING_NUM_SK.get(word)
            current_val = val
        elif word in string_num_scale:
            val = string_num_scale.get(word)
            current_val = val
        elif ordinals and word in string_num_ordinal:
            val = string_num_ordinal[word]
            current_val = val

        # is the prev word an ordinal number and current word is one?
        if ordinals and prev_word in string_num_ordinal and val == 1:
            val = prev_val

        # is the prev word a number and should we sum it?
        # dvadsať dva, päťdesiat šesť
        if (prev_word in _SUMS_SK and val and val < 10) or all([prev_word in
                                                                multiplies,
                                                                val < prev_val if prev_val else False]):
            if prev_val < 0:
                # continue a negated number: "mínus štyridsať dva" = -(40+2)
                val = prev_val - val
            else:
                val = prev_val + val

        # composed ordinals: "dvadsiaty prvý"
        if (prev_word in string_num_ordinal and val and val < 10) or all([prev_word in
                                                                          multiplies,
                                                                          val < prev_val if prev_val else False]):
            if prev_val < 0:
                val = prev_val - val
            else:
                val = prev_val + val

        # is the prev word a number and should we multiply it?
        # a smaller scale word right after a bigger one ("tisíc deväťsto")
        # was already summed above and must not multiply
        if word in multiplies and (not prev_val or current_val > prev_val):
            if not prev_val:
                prev_val = 1
            val = prev_val * val

        # is this a spoken fraction? "pol pohára"
        if val is False:
            val = is_fractional_sk(word, short_scale=short_scale)
            current_val = val

        # 2 pätiny
        if not ordinals:
            next_val = is_fractional_sk(next_word, short_scale=short_scale)
            if next_val:
                if not val:
                    val = 1
                val = val * next_val
                number_words.append(tokens[idx + 1])

        # the sign is applied once to the whole number after parsing,
        # so no per-token negation happens here

        # let's make sure it isn't a fraction
        if not val:
            # look for fractions like "2/3"
            aPieces = word.split('/')
            if look_for_fractions(aPieces):
                val = float(aPieces[0]) / float(aPieces[1])
                current_val = val

        else:
            if all([
                prev_word in _SUMS_SK,
                word not in _SUMS_SK,
                word not in multiplies,
                current_val >= 10]):
                # Backtrack - we've got numbers we can't sum.
                number_words.pop()
                val = prev_val
                break
            prev_val = val

            if word in multiplies:
                # handle long numbers: if all remaining scale words are
                # smaller than the current one, set the current value aside
                # and start assembling the next portion
                time_to_sum = True
                for other_token in tokens[idx + 1:]:
                    if other_token.word in multiplies:
                        if string_num_scale[other_token.word] >= current_val:
                            time_to_sum = False
                        else:
                            continue
                    if not time_to_sum:
                        break
                if time_to_sum:
                    to_sum.append(val)
                    val = 0
                    prev_val = 0

    if val is not None and to_sum:
        val += sum(to_sum)
    if negative and val not in (None, False):
        val = -val

    return val, number_words


def _initialize_number_data_sk(short_scale):
    """
    Generate dictionaries of words to numbers.

    Args:
        short_scale boolean:

    Returns:
        (set(str), dict(str, number), dict(str, number))
        multiplies, string_num_ordinal, string_num_scale

    """
    string_num_ordinal_sk = invert_dict(_ORDINAL_SK)
    string_num_scale_sk = invert_dict(_SCALE_SK)
    string_num_scale_sk.update(_SCALE_DECLENSIONS_SK)
    return _MULTIPLIES_SK, string_num_ordinal_sk, string_num_scale_sk


def extract_number_sk(text, short_scale=True, ordinals=False):
    """
    This function extracts a number from a text string

    Numeral structure follows the Rules of Slovak Orthography
    (Pravidlá slovenského pravopisu, Jazykovedný ústav Ľudovíta Štúra SAV,
    3rd ed. 2000): the million/milliard groups are separate lexical words that
    multiply the group before them, while the thousand and hundred groups form
    their own additive portions ("dvestopäťdesiattritisíc štyristo dvadsaťosem").
    Each such group is set aside and summed independently, so a millions group
    followed by a hundred-thousands group accumulates correctly.

    Args:
        text (str): the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
    Returns:
        (int) or (float) or False: The extracted number or False if no number
                                   was found

    """
    text = re.sub(r"(?<=[^\W\d]),", " ", text)
    text = _expand_compound_numbers_sk(text.lower())
    return _extract_number_with_text_sk(tokenize(text),
                                        short_scale, ordinals).value


def is_fractional_sk(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    input_str = input_str.lower()
    # plural fractions: tretiny -> tretina, pätiny -> pätina
    if input_str.endswith('iny', -3):
        input_str = input_str[:len(input_str) - 1] + "a"

    fracts = {"celá": 1, "pol": 2, "polovica": 2, "polovice": 2,
              "polovici": 2, "polovicu": 2}

    for num in _FRACTION_STRING_SK:
        if num > 1:
            fracts[_FRACTION_STRING_SK[num]] = num

    if input_str in fracts:
        return 1.0 / fracts[input_str]
    return False


def nice_number_sk(number, speech=True, denominators=range(1, 21)):
    """Slovak helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 a polovica" for speech and "4 1/2" for text

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
        return str(round(number, 3))

    whole, num, den = result

    if not speech:
        if num == 0:
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)

    if num == 0:
        return str(whole)
    den_str = _FRACTION_STRING_SK[den]
    # decline the fraction noun: 1 tretina, 2-4 tretiny, 5+ tretín
    if num > 4:
        if den_str == "polovica":
            den_str = "polovíc"
        elif den_str.endswith("ina"):
            den_str = den_str[:-3] + "ín"
    elif num > 1:
        if den_str == "polovica":
            den_str = "polovice"
        elif den_str.endswith("ina"):
            den_str = den_str[:-1] + "y"
    if whole == 0:
        if num == 1:
            return_string = '{}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1:
        return_string = '{} a {}'.format(whole, den_str)
    else:
        return_string = '{} a {} {}'.format(whole, num, den_str)

    return return_string


def pronounce_number_sk(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to its spoken Slovak equivalent

    For example, '5.2' would return 'päť celá dva'

    Word forms follow the Rules of Slovak Orthography (Pravidlá slovenského
    pravopisu, Jazykovedný ústav Ľudovíta Štúra SAV, 3rd ed. 2000): million and
    milliard groups are spoken as separate words, so the output round-trips
    through extract_number_sk.

    Args:
        number(float or int): the number to pronounce
        places(int): maximum decimal places to speak
        short_scale (bool): kept for API compatibility; Slovak uses the
            long scale names regardless
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "prvý" instead of "jeden"
    Returns:
        (str): The pronounced number
    """
    num = number
    # deal with infinity
    if num == float("inf"):
        return "nekonečno"
    elif num == float("-inf"):
        return "mínus nekonečno"
    if scientific:
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:
            if ordinals:
                return '{}{} krát desať na {}{} mocninu'.format(
                    'mínus ' if float(n) < 0 else '',
                    pronounce_number_sk(
                        abs(float(n)), places, short_scale, False, ordinals=False),
                    'mínus ' if power < 0 else '',
                    pronounce_number_sk(abs(power), places, short_scale, False, ordinals=True))
            else:
                return '{}{} krát desať na mocninu {}{}'.format(
                    'mínus ' if float(n) < 0 else '',
                    pronounce_number_sk(
                        abs(float(n)), places, short_scale, False),
                    'mínus ' if power < 0 else '',
                    pronounce_number_sk(abs(power), places, short_scale, False))

    number_names = _NUM_STRING_SK.copy()
    number_names.update(_SCALE_SK)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    hundreds = list(_SCALE_SK.values())

    # deal with negative numbers
    result = ""
    if num < 0:
        result = "mínus "
    num = abs(num)

    # check for a direct match
    if num in number_names and not ordinals:
        result += number_names[num]
    else:
        def _sub_thousand(n, ordinals=False):
            assert 0 <= n <= 999
            if n in _ORDINAL_SK and ordinals:
                return _ORDINAL_SK[n]
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                # units join the tens into a single word: dvadsaťjeden
                return tens[q - 1] + (_sub_thousand(r, ordinals) if r
                                      else "")
            else:
                q, r = divmod(n, 100)
                hundred = _HUNDREDS_SK[q]
                return hundred + (
                    " " + _sub_thousand(r, ordinals) if r else "")

        def _split_by(n, split=1000):
            assert 0 <= n
            res = []
            while n:
                n, r = divmod(n, split)
                res.append(r)
            return res

        def _whole_number(n):
            if n >= max(_SCALE_SK.keys()) * 1000:
                return "nekonečno"
            ordi = ordinals

            if int(n) != n:
                ordi = False
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000)):
                if not z:
                    continue
                number = _sub_thousand(z, not i and ordi)

                if i:
                    if i >= len(hundreds):
                        return ""
                    number += " "
                    if ordi:
                        if i * 1000 in _ORDINAL_SK:
                            if z == 1:
                                number = _ORDINAL_SK[i * 1000]
                            else:
                                number += _ORDINAL_SK[i * 1000]
                        else:
                            number += hundreds[i] + "ty"
                    else:
                        number += _scale_declined_sk(hundreds[i], z)
                res.append(number)
                ordi = False

            return " ".join(reversed(res))

        result += _whole_number(num)

    # deal with scientific notation unpronounceable as number
    if not result and "e" in str(num):
        return pronounce_number_sk(num, places, short_scale, scientific=True)
    # Deal with fractional part
    elif not num == int(num) and places > 0:
        if abs(num) < 1.0 and (result == "mínus " or not result):
            result += "nula"
        result += " celá"
        _num_str = str(num)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result


def pronounce_ordinal_sk(number):
    """
    Pronounce a number as a Slovak ordinal.

    Args:
        number (int): the number to pronounce
    Returns:
        (str): the ordinal in Slovak
    """
    number = int(number)
    if number <= 0:
        raise ValueError("Slovak ordinals start at 1")
    if number in _ORDINAL_SK:
        return _ORDINAL_SK[number]
    if number in _ORDINAL_HUNDREDS_SK:
        return _ORDINAL_HUNDREDS_SK[number]
    if number < 100:
        tens = number // 10 * 10
        unit = number % 10
        return f"{_ORDINAL_SK[tens]} {_ORDINAL_SK[unit]}"
    last = number % 100
    if last:
        prefix = number - last
        return f"{pronounce_number_sk(prefix)} {pronounce_ordinal_sk(last)}"
    raise NotImplementedError(f"cannot pronounce {number} as a Slovak ordinal")
