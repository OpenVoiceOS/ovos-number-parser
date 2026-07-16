"""Croatian number parsing and pronunciation.

Croatian writes compound numerals as separate words ("dvadeset jedan" = 21),
optionally joined with "i" ("dvadeset i jedan"). Scale words decline with
the count: "tisuću" (1000), "dvije tisuće" (2000), "pet tisuća" (5000),
"milijun" / "dva milijuna", "milijarda" / "dvije milijarde" / "pet milijardi".
Croatian uses the long scale (milijun = 1e6, milijarda = 1e9, bilijun = 1e12).
"""
from collections import OrderedDict

from ovos_number_parser.util import convert_to_mixed_fraction, is_numeric, look_for_fractions, \
    invert_dict, ReplaceableNumber, partition_list, tokenize, Token

_NUM_STRING_HR = {
    0: 'nula',
    1: 'jedan',
    2: 'dva',
    3: 'tri',
    4: 'četiri',
    5: 'pet',
    6: 'šest',
    7: 'sedam',
    8: 'osam',
    9: 'devet',
    10: 'deset',
    11: 'jedanaest',
    12: 'dvanaest',
    13: 'trinaest',
    14: 'četrnaest',
    15: 'petnaest',
    16: 'šesnaest',
    17: 'sedamnaest',
    18: 'osamnaest',
    19: 'devetnaest',
    20: 'dvadeset',
    30: 'trideset',
    40: 'četrdeset',
    50: 'pedeset',
    60: 'šezdeset',
    70: 'sedamdeset',
    80: 'osamdeset',
    90: 'devedeset',
    100: 'sto',
    200: 'dvjesto',
    300: 'tristo',
    400: 'četiristo',
    500: 'petsto',
    600: 'šesto',
    700: 'sedamsto',
    800: 'osamsto',
    900: 'devetsto'
}

_FRACTION_STRING_HR = {
    2: 'polovina',
    3: 'trećina',
    4: 'četvrtina',
    5: 'petina',
    6: 'šestina',
    7: 'sedmina',
    8: 'osmina',
    9: 'devetina',
    10: 'desetina',
    11: 'jedanaestina',
    12: 'dvanaestina',
    13: 'trinaestina',
    14: 'četrnaestina',
    15: 'petnaestina',
    16: 'šesnaestina',
    17: 'sedamnaestina',
    18: 'osamnaestina',
    19: 'devetnaestina',
    20: 'dvadesetina',
    1e2: 'stotinka',
    1e3: 'tisućinka'
}

# Croatian scale words (long scale: each power of 1000 alternates
# -ijun / -ijarda). The same names apply regardless of the short_scale
# flag, since Croatian only uses the long scale.
_SCALE_HR = OrderedDict([
    (1e3, 'tisuća'),
    (1e6, 'milijun'),
    (1e9, 'milijarda'),
    (1e12, 'bilijun'),
    (1e15, 'bilijarda'),
    (1e18, 'trilijun'),
    (1e21, 'trilijarda'),
    (1e24, 'kvadrilijun'),
])

_ORDINAL_BASE_HR = {
    1: 'prvi',
    2: 'drugi',
    3: 'treći',
    4: 'četvrti',
    5: 'peti',
    6: 'šesti',
    7: 'sedmi',
    8: 'osmi',
    9: 'deveti',
    10: 'deseti',
    11: 'jedanaesti',
    12: 'dvanaesti',
    13: 'trinaesti',
    14: 'četrnaesti',
    15: 'petnaesti',
    16: 'šesnaesti',
    17: 'sedamnaesti',
    18: 'osamnaesti',
    19: 'devetnaesti',
    20: 'dvadeseti',
    30: 'trideseti',
    40: 'četrdeseti',
    50: 'pedeseti',
    60: 'šezdeseti',
    70: 'sedamdeseti',
    80: 'osamdeseti',
    90: 'devedeseti',
    1e2: 'stoti',
    1e3: 'tisući'
}

_ORDINAL_HUNDREDS_HR = {
    200: 'dvjestoti', 300: 'tristoti', 400: 'četiristoti',
    500: 'petstoti', 600: 'šeststoti', 700: 'sedamstoti',
    800: 'osamstoti', 900: 'devetstoti',
}

_SHORT_ORDINAL_HR = {
    1e6: 'milijunti',
}
_SHORT_ORDINAL_HR.update(_ORDINAL_BASE_HR)

# negate next number (-2 = 0 - 2)
_NEGATIVES = {"minus"}

# words that continue a number ("dvadeset i jedan" = 21)
_CONNECTORS = {"i"}

# sum the next number (dvadeset dva = 20 + 2, sto deset = 100 + 10)
_SUMS = {'dvadeset', '20', 'trideset', '30', 'četrdeset', '40', 'pedeset', '50',
         'šezdeset', '60', 'sedamdeset', '70', 'osamdeset', '80', 'devedeset', '90',
         'sto', '100', 'dvjesto', '200', 'tristo', '300', 'četiristo', '400',
         'petsto', '500', 'šesto', '600', 'sedamsto', '700', 'osamsto', '800',
         'devetsto', '900'}

# declined forms of the scale words used when speaking multiples
_SCALE_DECLENSIONS_HR = {
    "tisuću": 1e3,
    "tisuće": 1e3,
    "milijuna": 1e6,
    "milijardu": 1e9,
    "milijarde": 1e9,
    "milijardi": 1e9,
    "bilijuna": 1e12,
    "bilijarde": 1e15,
    "bilijardi": 1e15,
    "trilijuna": 1e18,
    "trilijarde": 1e21,
    "trilijardi": 1e21,
    "kvadrilijuna": 1e24,
}

_MULTIPLIES_HR = set(_SCALE_HR.values()) | set(_SCALE_DECLENSIONS_HR)

# split sentence parse separately and sum ( 2 and a half = 2 + 0.5 )
_FRACTION_MARKER = {"i"}

# decimal marker ( 1 point 5 = 1 + 0.5)
_DECIMAL_MARKER = {"zarez", "cijela", "cijele", "cijelih", "točka"}

_STRING_NUM_HR = invert_dict(_NUM_STRING_HR)
_STRING_NUM_HR.update({
    "dvjesta": 200,
    "šeststo": 600,
    "polovina": 0.5,
    "polovica": 0.5,
    "pola": 0.5,
    "pol": 0.5,
})

_STRING_SHORT_ORDINAL_HR = invert_dict(_SHORT_ORDINAL_HR)


def plural_hr(num: int, one: str, few: str, many: str):
    """Pick the Croatian noun form that follows the number ``num``."""
    num %= 100
    if num // 10 == 1:
        return many
    if num % 10 == 1:
        return one
    if 2 <= num % 10 <= 4:
        return few
    return many


def _feminine_hr(spoken: str) -> str:
    """Turn a trailing masculine numeral into its feminine form."""
    if spoken.endswith("jedan"):
        return spoken[:-len("jedan")] + "jedna"
    if spoken.endswith("dva"):
        return spoken[:-len("dva")] + "dvije"
    return spoken


def nice_number_hr(number, speech=True, denominators=range(1, 21)):
    """Croatian helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 i pol" for speech and "4 1/2" for text

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
    den_str = plural_hr(num, _FRACTION_STRING_HR[den],
                        _FRACTION_STRING_HR[den][:-1] + 'e',
                        _FRACTION_STRING_HR[den])
    if whole == 0:
        if num == 1:
            return_string = '{}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1 and den == 2:
        return_string = '{} i pol'.format(whole)
    else:
        return_string = '{} i {} {}'.format(whole, num, den_str)

    return return_string


def pronounce_number_hr(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'pet zarez dva'

    Args:
        number(float or int): the number to pronounce
        places(int): maximum decimal places to speak
        short_scale (bool): ignored, Croatian only uses the long scale
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
    Returns:
        (str): The pronounced number
    """
    num = number
    # deal with infinity
    if num == float("inf"):
        return "beskonačnost"
    elif num == float("-inf"):
        return "minus beskonačnost"
    if scientific:
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:
            return '{}{} puta deset na {}{}'.format(
                'minus ' if float(n) < 0 else '',
                pronounce_number_hr(
                    abs(float(n)), places, short_scale, False, ordinals=False),
                'minus ' if power < 0 else '',
                pronounce_number_hr(abs(power), places, short_scale, False,
                                    ordinals=True))

    number_names = _NUM_STRING_HR.copy()
    number_names.update(_SCALE_HR)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    hundreds = list(_SCALE_HR.values())

    # deal with negative numbers
    result = ""
    if num < 0:
        result = "minus "
    num = abs(num)

    # check for a direct match
    if num in number_names and not ordinals:
        result += number_names[num]
    else:
        def _sub_thousand(n, ordinals=False):
            assert 0 <= n <= 999
            if n in _SHORT_ORDINAL_HR and ordinals:
                return _SHORT_ORDINAL_HR[n]
            if n in _ORDINAL_HUNDREDS_HR and ordinals:
                return _ORDINAL_HUNDREDS_HR[n]
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                return tens[q - 1] + (" " + _sub_thousand(r, ordinals) if r
                                      else "")
            else:
                q, r = divmod(n, 100)
                return _NUM_STRING_HR[q * 100] + \
                    (" " + _sub_thousand(r, ordinals) if r else "")

        def _scale_hr(n):
            if n > max(_SCALE_HR.keys()):
                return "beskonačnost"
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
                    if i > len(hundreds):
                        return ""
                    scale_word = hundreds[i - 1]
                    if ordi:
                        if i * 1000 in _SHORT_ORDINAL_HR:
                            if z == 1:
                                number = _SHORT_ORDINAL_HR[i * 1000]
                            else:
                                number += " " + _SHORT_ORDINAL_HR[i * 1000]
                        else:
                            number += " " + scale_word + "ti"
                    elif scale_word.endswith("a"):
                        # feminine scale nouns (tisuća, milijarda, ...)
                        if i == 1:
                            # 1000 is spoken "tisuću"
                            one = "tisuću"
                        else:
                            one = scale_word
                        if z == 1:
                            number = one
                        else:
                            # genitive plural: "tisuća" but "milijardi"
                            many = scale_word if i == 1 \
                                else scale_word[:-1] + "i"
                            number = _feminine_hr(number) + " " + plural_hr(
                                z, scale_word, scale_word[:-1] + "e", many)
                    else:
                        # masculine scale nouns (milijun, bilijun, ...)
                        if z == 1:
                            number = scale_word
                        else:
                            number += " " + plural_hr(
                                z, scale_word, scale_word + "a",
                                scale_word + "a")

                res.append(number)
                ordi = False

            return " ".join(reversed(res))

        def _split_by(n, split=1000):
            assert 0 <= n
            res = []
            while n:
                n, r = divmod(n, split)
                res.append(r)
            return res

        result += _scale_hr(num)

    # deal with scientific notation unpronounceable as number
    if not result and "e" in str(num):
        return pronounce_number_hr(num, places, short_scale, scientific=True)
    # Deal with fractional part
    elif not num == int(num) and places > 0:
        if abs(num) < 1.0 and (result == "minus " or not result):
            result += "nula"
        result += " zarez"
        _num_str = str(num)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result


def pronounce_ordinal_hr(number):
    """
    Pronounce a number as a Croatian ordinal.

    Only the last element of a compound numeral takes the ordinal form:
    21st is "dvadeset prvi".

    Args:
        number (int): the number to pronounce
    Returns:
        (str): the ordinal in Croatian
    """
    number = int(number)
    if number <= 0:
        raise ValueError("Croatian ordinals start at 1")
    if number in _SHORT_ORDINAL_HR:
        return _SHORT_ORDINAL_HR[number]
    if number in _ORDINAL_HUNDREDS_HR:
        return _ORDINAL_HUNDREDS_HR[number]
    if number < 100:
        tens = number // 10 * 10
        unit = number % 10
        return f"{_NUM_STRING_HR[tens]} {_SHORT_ORDINAL_HR[unit]}"
    last = number % 100
    if last:
        prefix = number - last
        return f"{pronounce_number_hr(prefix)} {pronounce_ordinal_hr(last)}"
    raise NotImplementedError(f"cannot pronounce {number} as a Croatian ordinal")


def numbers_to_digits_hr(text, short_scale=True, ordinals=False):
    """
    Convert words in a string into their equivalent numbers.
    Args:
        text str:
        short_scale boolean: ignored, Croatian only uses the long scale
        ordinals boolean: True if ordinals (e.g. first, second, third) should
                          be parsed to their number values (1, 2, 3...)

    Returns:
        str
        The original text, with numbers subbed in where appropriate.

    """
    text = text.lower()
    tokens = _drop_connectors_hr(tokenize(text))
    numbers_to_replace = \
        _extract_numbers_with_text_hr(tokens, short_scale, ordinals)
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


def _extract_numbers_with_text_hr(tokens, short_scale=True,
                                  ordinals=False, fractional_numbers=True):
    """
    Extract all numbers from a list of Tokens, with the words that
    represent them.

    Args:
        [Token]: The tokens to parse.
        short_scale bool: ignored, Croatian only uses the long scale
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
            _extract_number_with_text_hr(tokens, short_scale,
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


def _extract_number_with_text_hr(tokens, short_scale=True,
                                 ordinals=False, fractional_numbers=True):
    """
    This function extracts a number from a list of Tokens.

    Args:
        tokens str: the string to normalize
        short_scale (bool): ignored, Croatian only uses the long scale
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
        fractional_numbers (bool): True if we should look for fractions and
                                   decimals.
    Returns:
        ReplaceableNumber

    """
    number, tokens = \
        _extract_number_with_text_hr_helper(tokens, short_scale,
                                            ordinals, fractional_numbers)
    return ReplaceableNumber(number, tokens)


def _extract_number_with_text_hr_helper(tokens,
                                        short_scale=True, ordinals=False,
                                        fractional_numbers=True):
    """
    Helper for _extract_number_with_text_hr.

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
            _extract_fraction_with_text_hr(tokens, short_scale, ordinals)
        if fraction:
            return fraction, fraction_text

        decimal, decimal_text = \
            _extract_decimal_with_text_hr(tokens, short_scale, ordinals)
        if decimal:
            return decimal, decimal_text

    return _extract_whole_number_with_text_hr(tokens, short_scale, ordinals)


def _extract_fraction_with_text_hr(tokens, short_scale, ordinals):
    """
    Extract fraction numbers from a string ("dva i pol" = 2.5).

    Args:
        tokens [Token]: words and their indexes in the original string.
        short_scale boolean:
        ordinals boolean:

    Returns:
        (int or float, [Token])
        The value found, and the list of relevant tokens.
        (None, None) if no fraction value is found.

    """
    for c in _FRACTION_MARKER:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_hr(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_hr(partitions[2], short_scale,
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


def _extract_decimal_with_text_hr(tokens, short_scale, ordinals):
    """
    Extract decimal numbers from a string ("pet zarez dva" = 5.2).

    Notes:
        While this is a helper for extract_number_hr, it also depends on
        extract_number_hr, to parse out the components of the decimal.

        This does not currently handle things like:
            number dot number number number

    Args:
        tokens [Token]: The text to parse.
        short_scale boolean:
        ordinals boolean:

    Returns:
        (float, [Token])
        The value found and relevant tokens.
        (None, None) if no decimal value is found.

    """
    for c in _DECIMAL_MARKER:
        partitions = partition_list(tokens, lambda t: t.word == c)

        if len(partitions) == 3:
            numbers1 = \
                _extract_numbers_with_text_hr(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_hr(partitions[2], short_scale,
                                              ordinals, fractional_numbers=False)

            if not numbers1 or not numbers2:
                return None, None

            number = numbers1[-1]
            decimal = numbers2[0]
            # concatenate consecutive single digits after the marker
            # ("zarez jedan četiri" -> .14)
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

            # TODO handle number dot number number number
            if "." not in str(decimal.text):
                _frac2 = float('0.' + str(decimal.value))
                return (number.value - _frac2 if number.value < 0
                        else number.value + _frac2), \
                       number.tokens + partitions[1] + decimal.tokens
    return None, None


def _extract_whole_number_with_text_hr(tokens, short_scale, ordinals):
    """
    Handle numbers not handled by the decimal or fraction functions. This is
    generally whole numbers.

    Args:
        tokens [Token]:
        short_scale boolean:
        ordinals boolean:

    Returns:
        int or float, [Tokens]
        The value parsed, and tokens that it corresponds to.

    """
    multiplies, string_num_ordinal, string_num_scale = \
        _initialize_number_data(short_scale)

    number_words = []  # type: [Token]
    val = False
    prev_val = None
    next_val = None
    to_sum = []
    for idx, token in enumerate(tokens):
        current_val = None
        if next_val:
            next_val = None
            continue

        word = token.word
        if word in _NEGATIVES:
            number_words.append(token)
            continue

        prev_word = tokens[idx - 1].word if idx > 0 else ""
        next_word = tokens[idx + 1].word if idx + 1 < len(tokens) else ""

        # In Croatian ordinals in digits are written with a trailing
        # point (1., 2., ...)
        if is_numeric(word[:-1]) and \
                (word.endswith(".")):
            word = word[:-1]

        # Normalize Croatian gender inflection (jedan, jedna, jedno, ...)
        if not ordinals:
            word = _text_hr_inflection_normalize(word)

        if word not in string_num_scale and \
                word not in _STRING_NUM_HR and \
                word not in _SUMS and \
                word not in multiplies and \
                not (ordinals and word in string_num_ordinal) and \
                not is_numeric(word) and \
                not is_fractional_hr(word, short_scale=short_scale) and \
                not look_for_fractions(word.split('/')):
            words_only = [token.word for token in number_words]
            if number_words and not all([w in _NEGATIVES for w in words_only]):
                break
            else:
                number_words = []
                continue
        elif word not in multiplies \
                and prev_word not in multiplies \
                and prev_word not in _SUMS \
                and not (ordinals and prev_word in string_num_ordinal) \
                and prev_word not in _NEGATIVES:
            number_words = [token]
        elif prev_word in _SUMS and word in _SUMS:
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
        if word in _STRING_NUM_HR:
            val = _STRING_NUM_HR.get(word)
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
        # dvadeset dva, pedeset šest
        if (prev_word in _SUMS and val and val < 10) \
                or (prev_word in _SUMS and val and val < 100 and prev_val >= 100) \
                or all([prev_word in multiplies, val < prev_val if prev_val else False]):
            if prev_val < 0:
                # continue a negated number: "minus četrdeset dva" = -(40+2)
                val = prev_val - val
            else:
                val = prev_val + val

        # is the prev word a number and should we multiply it?
        # dvije tisuće, šest milijuna
        if word in multiplies:
            if not prev_val:
                prev_val = 1
            val = prev_val * val

        # is this a spoken fraction?
        # pola šalice
        if val is False:
            val = is_fractional_hr(word, short_scale=short_scale)
            current_val = val

        # 2 petine
        if not ordinals:
            next_val = is_fractional_hr(next_word, short_scale=short_scale)
            if next_val:
                if not val:
                    val = 1
                val = val * next_val
                number_words.append(tokens[idx + 1])

        # is this a negative number?
        if val and prev_word and prev_word in _NEGATIVES:
            val = 0 - val

        # let's make sure it isn't a fraction
        if not val:
            # look for fractions like "2/3"
            a_pieces = word.split('/')
            if look_for_fractions(a_pieces):
                val = float(a_pieces[0]) / float(a_pieces[1])
        else:
            if all([
                prev_word in _SUMS,
                word not in _SUMS,
                word not in multiplies,
                current_val >= 10,
                # teens continue a preceding hundred ("sto deset" = 110)
                not (prev_val and prev_val >= 100 and current_val < 100)
            ]):
                # Backtrack - we've got numbers we can't sum.
                number_words.pop()
                val = prev_val
                break
            prev_val = val

            if word in multiplies and next_word not in multiplies:
                # handle long numbers
                # šesto šezdeset šest
                # dva milijuna petsto tisuća
                #
                # If all remaining scale words are smaller than the
                # current one, set the current group aside in to_sum
                # and start assembling the next group.
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

    return val, number_words


def _initialize_number_data(short_scale):
    """
    Generate dictionaries of words to numbers.

    This is a helper function for _extract_whole_number.

    Args:
        short_scale boolean: ignored, Croatian only uses the long scale

    Returns:
        (set(str), dict(str, number), dict(str, number))
        multiplies, string_num_ordinal, string_num_scale

    """
    string_num_scale_hr = invert_dict(_SCALE_HR)
    string_num_scale_hr.update(_SCALE_DECLENSIONS_HR)
    return _MULTIPLIES_HR, _STRING_SHORT_ORDINAL_HR, string_num_scale_hr


def _drop_connectors_hr(tokens):
    """Drop the joiner "i" between number words ("dvadeset i jedan" = 21).

    The "i" is kept when it introduces a fraction ("dva i pol" = 2.5), which
    is handled by the fraction marker logic instead.
    """
    def _is_whole_number_word(word):
        word = _text_hr_inflection_normalize(word)
        if word in _STRING_NUM_HR:
            return _STRING_NUM_HR[word] >= 1
        return word in _SUMS or word in _MULTIPLIES_HR or \
            (is_numeric(word) and float(word) >= 1)

    filtered = []
    for idx, token in enumerate(tokens):
        if token.word in _CONNECTORS and 0 < idx < len(tokens) - 1 and \
                _is_whole_number_word(tokens[idx - 1].word) and \
                _is_whole_number_word(tokens[idx + 1].word):
            continue
        filtered.append(token)
    return [Token(t.word, i) for i, t in enumerate(filtered)]


def extract_number_hr(text, short_scale=True, ordinals=False):
    """
    This function extracts a number from a text string

    Args:
        text (str): the string to normalize
        short_scale (bool): ignored, Croatian only uses the long scale
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
    Returns:
        (int) or (float) or False: The extracted number or False if no number
                                   was found

    """
    tokens = _drop_connectors_hr(tokenize(text.lower()))
    value = _extract_number_with_text_hr(tokens, short_scale, ordinals).value
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return value


def is_fractional_hr(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): ignored, Croatian only uses the long scale
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    input_str = input_str.lower()
    # normalize plural forms (dvije trećine -> trećina)
    if input_str.endswith("ine"):
        input_str = input_str[:-1] + "a"

    fractions = {"pola": 2, "pol": 2, "polovica": 2, "polovice": 2}

    for num, name in _FRACTION_STRING_HR.items():
        fractions[name] = num

    if input_str in fractions:
        return 1.0 / fractions[input_str]
    return False


def _text_hr_inflection_normalize(word):
    """
    Croatian gender/case normalizer for the numerals one and two.

    Args:
        word (str)

    Returns:
        word (str)

    """
    if word in ("jedna", "jedno", "jednu", "jednog", "jednom", "jednoj"):
        return "jedan"
    if word in ("dvije", "dvje"):
        return "dva"
    return word
