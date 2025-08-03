from collections import OrderedDict

from ovos_number_parser.util import (invert_dict, convert_to_mixed_fraction, tokenize, look_for_fractions,
                                     partition_list, is_numeric, Token, ReplaceableNumber)


_NUM_STRING_CS = {
    0: 'nula',
    1: 'jedna',
    2: 'dva',
    3: 'tři',
    4: 'čtyři',
    5: 'pět',
    6: 'šest',
    7: 'sedm',
    8: 'osm',
    9: 'devět',
    10: 'deset',
    11: 'jedenáct',
    12: 'dvanáct',
    13: 'třináct',
    14: 'čtrnáct',
    15: 'patnáct',
    16: 'šestnáct',
    17: 'sedmnáct',
    18: 'osmnáct',
    19: 'devatenáct',
    20: 'dvacet',
    30: 'třicet',
    40: 'čtyřicet',
    50: 'padesát',
    60: 'šedesát',
    70: 'sedmdesát',
    80: 'osmdesát',
    90: 'devadesát'
}

_FRACTION_STRING_CS = {
    2: 'polovina',
    3: 'třetina',
    4: 'čtvrtina',
    5: 'pětina',
    6: 'šestina',
    7: 'sedmina',
    8: 'osmina',
    9: 'devítina',
    10: 'desetina',
    11: 'jedenáctina',
    12: 'dvanáctina',
    13: 'třináctina',
    14: 'čtrnáctina',
    15: 'patnáctina',
    16: 'šestnáctina',
    17: 'sedmnáctina',
    18: 'osmnáctina',
    19: 'devatenáctina',
    20: 'dvacetina',
    30: 'třicetina',
    40: 'čtyřicetina',
    50: 'padesátina',
    60: 'šedesátina',
    70: 'sedmdesátina',
    80: 'osmdesátina',
    90: 'devadesátina',
    1e2: 'setina',
    1e3: 'tisícina'
}

_LONG_SCALE_CS = OrderedDict([
    (100, 'sto'),
    (1000, 'tisíc'),
    (1000000, 'milion'),
    (1e9, "miliarda"),
    (1e12, "bilion"),
    (1e15, "biliarda"),
    (1e18, "trilion"),
    (1e21, "triliarda"),
    (1e24, "kvadrilion"),
    (1e27, "kvadriliarda"),
    (1e30, "kvintilion"),
    (1e33, "kvintiliarda"),
    (1e36, "sextilion"),
    (1e39, "sextiliarda"),
    (1e42, "septilion"),
    (1e45, "septiliarda"),
    (1e48, "oktilion"),
    (1e51, "oktiliarda"),
    (1e54, "nonilion"),
    (1e57, "noniliarda"),
    (1e60, "decilion"),
    (1e63, "deciliarda"),
    (1e120, "vigintilion"),
    (1e180, "trigintilion"),
    (1e303, "kvinkvagintiliarda"),
    (1e600, "centilion"),
    (1e603, "centiliarda")
])

_SHORT_SCALE_CS = OrderedDict([
    (100, 'sto'),
    (1000, 'tisíc'),
    (1000000, 'million'),
    (1e9, "billion"),
    (1e12, 'trillion'),
    (1e15, "quadrillion"),
    (1e18, "quintillion"),
    (1e21, "sextillion"),
    (1e24, "septillion"),
    (1e27, "octillion"),
    (1e30, "nonillion"),
    (1e33, "decillion"),
    (1e36, "undecillion"),
    (1e39, "duodecillion"),
    (1e42, "tredecillion"),
    (1e45, "quadrdecillion"),
    (1e48, "quindecillion"),
    (1e51, "sexdecillion"),
    (1e54, "septendecillion"),
    (1e57, "octodecillion"),
    (1e60, "novemdecillion"),
    (1e63, "vigintillion"),
    (1e66, "unvigintillion"),
    (1e69, "uuovigintillion"),
    (1e72, "tresvigintillion"),
    (1e75, "quattuorvigintillion"),
    (1e78, "quinquavigintillion"),
    (1e81, "qesvigintillion"),
    (1e84, "septemvigintillion"),
    (1e87, "octovigintillion"),
    (1e90, "novemvigintillion"),
    (1e93, "trigintillion"),
    (1e96, "untrigintillion"),
    (1e99, "duotrigintillion"),
    (1e102, "trestrigintillion"),
    (1e105, "quattuortrigintillion"),
    (1e108, "quinquatrigintillion"),
    (1e111, "sestrigintillion"),
    (1e114, "septentrigintillion"),
    (1e117, "octotrigintillion"),
    (1e120, "noventrigintillion"),
    (1e123, "quadragintillion"),
    (1e153, "quinquagintillion"),
    (1e183, "sexagintillion"),
    (1e213, "septuagintillion"),
    (1e243, "octogintillion"),
    (1e273, "nonagintillion"),
    (1e303, "centillion"),
    (1e306, "uncentillion"),
    (1e309, "duocentillion"),
    (1e312, "trescentillion"),
    (1e333, "decicentillion"),
    (1e336, "undecicentillion"),
    (1e363, "viginticentillion"),
    (1e366, "unviginticentillion"),
    (1e393, "trigintacentillion"),
    (1e423, "quadragintacentillion"),
    (1e453, "quinquagintacentillion"),
    (1e483, "sexagintacentillion"),
    (1e513, "septuagintacentillion"),
    (1e543, "ctogintacentillion"),
    (1e573, "nonagintacentillion"),
    (1e603, "ducentillion"),
    (1e903, "trecentillion"),
    (1e1203, "quadringentillion"),
    (1e1503, "quingentillion"),
    (1e1803, "sescentillion"),
    (1e2103, "septingentillion"),
    (1e2403, "octingentillion"),
    (1e2703, "nongentillion"),
    (1e3003, "millinillion")
])

_ORDINAL_BASE_CS = {
    1: 'první',
    2: 'druhý',
    3: 'třetí',
    4: 'čtvrtý',
    5: 'pátý',
    6: 'šestý',
    7: 'sedmý',
    8: 'osmý',
    9: 'devátý',
    10: 'desátý',
    11: 'jedenáctý',
    12: 'dvanáctý',
    13: 'třináctý',
    14: 'čtrnáctý',
    15: 'patnáctý',
    16: 'šestnáctý',
    17: 'sedmnáctý',
    18: 'osmnáctý',
    19: 'devatenáctý',
    20: 'dvacátý',
    30: 'třicátý',
    40: "čtyřicátý",
    50: "padesátý",
    60: "šedesátý",
    70: "sedmdesátý",
    80: "osmdesátý",
    90: "devadesátý",
    1e2: "stý",
    1e3: "tisící"
}

_SHORT_ORDINAL_CS = {
    1e6: "miliontý",
    1e9: "billiontý",
    1e12: "trilliontý",
    1e15: "quadrilliontý",
    1e18: "quintilliontý",
    1e21: "sextilliontý",
    1e24: "septilliontý",
    1e27: "oktiliontý",
    1e30: "nonilliontý",
    1e33: "decilliontý"
    # TODO > 1e-33
}
_SHORT_ORDINAL_CS.update(_ORDINAL_BASE_CS)

_LONG_ORDINAL_CS = {
    1e6: "miliontý",
    1e9: "miliardtý",
    1e12: "biliontý",
    1e15: "biliardtý",
    1e18: "triliontý",
    1e21: "triliardtý",
    1e24: "kvadriliontý",
    1e27: "kvadriliardtý",
    1e30: "kvintiliontý",
    1e33: "kvintiliardtý",
    1e36: "sextiliontý",
    1e39: "sextiliardtý",
    1e42: "septiliontý",
    1e45: "septiliardtý",
    1e48: "oktilion",
    1e51: "oktiliardtý",
    1e54: "noniliontý",
    1e57: "noniliardtý",
    1e60: "deciliontý"
    # TODO > 1e60
}
_LONG_ORDINAL_CS.update(_ORDINAL_BASE_CS)


def generate_plurals_cs(originals):
    """
    Return a new set or dict containing the plural form of the original values,

    In English this means all with 's' appended to them.

    Args:
        originals set(str) or dict(str, any): values to pluralize

    Returns:
        set(str) or dict(str, any)

    """
    if isinstance(originals, dict):
        return {key + 'ý': value for key, value in originals.items()}
    return {value + "ý" for value in originals}


# negate next number (-2 = 0 - 2)
_NEGATIVES = {"záporné", "mínus"}

# sum the next number (twenty two = 20 + 2)
_SUMS = {'dvacet', '20', 'třicet', '30', 'čtyřicet', '40', 'padesát', '50',
         'šedesát', '60', 'sedmdesát', '70', 'osmdesát', '80', 'devadesát', '90'}

_MULTIPLIES_LONG_SCALE_CS = set(_LONG_SCALE_CS.values()) | \
                            generate_plurals_cs(_LONG_SCALE_CS.values())

_MULTIPLIES_SHORT_SCALE_CS = set(_SHORT_SCALE_CS.values()) | \
                             generate_plurals_cs(_SHORT_SCALE_CS.values())

# split sentence parse separately and sum ( 2 and a half = 2 + 0.5 )
_FRACTION_MARKER = {"a"}

# decimal marker ( 1 point 5 = 1 + 0.5)
_DECIMAL_MARKER = {"bod", "tečka", "čárka", "celá"}

_STRING_NUM_CS = invert_dict(_NUM_STRING_CS)
_STRING_NUM_CS.update(generate_plurals_cs(_STRING_NUM_CS))
_STRING_NUM_CS.update({
    "polovina": 0.5,
    "půlka": 0.5,
    "půl": 0.5,
    "jeden": 1,
    "dvojice": 2,
    "dvoje": 2
})

_STRING_SHORT_ORDINAL_CS = invert_dict(_SHORT_ORDINAL_CS)
_STRING_LONG_ORDINAL_CS = invert_dict(_LONG_ORDINAL_CS)


def numbers_to_digits_cs(text, short_scale=True, ordinals=False):
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
    text = text.lower()
    tokens = tokenize(text)
    numbers_to_replace = \
        _extract_numbers_with_text_cs(tokens, short_scale, ordinals)
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


def _extract_numbers_with_text_cs(tokens, short_scale=True,
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
            _extract_number_with_text_cs(tokens, short_scale,
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


def _extract_number_with_text_cs(tokens, short_scale=True,
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
        _extract_number_with_text_cs_helper(tokens, short_scale,
                                            ordinals, fractional_numbers)
    # while tokens and tokens[0].word in _ARTICLES_CS:
    #    tokens.pop(0)
    return ReplaceableNumber(number, tokens)


def _extract_number_with_text_cs_helper(tokens,
                                        short_scale=True, ordinals=False,
                                        fractional_numbers=True):
    """
    Helper for _extract_number_with_text_en.

    This contains the real logic for parsing, but produces
    a result that needs a little cleaning (specific, it may
    contain leading articles that can be trimmed off).

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
            _extract_fraction_with_text_cs(tokens, short_scale, ordinals)
        if fraction:
            return fraction, fraction_text

        decimal, decimal_text = \
            _extract_decimal_with_text_cs(tokens, short_scale, ordinals)
        if decimal:
            return decimal, decimal_text

    return _extract_whole_number_with_text_cs(tokens, short_scale, ordinals)


def _extract_fraction_with_text_cs(tokens, short_scale, ordinals):
    """
    Extract fraction numbers from a string.

    This function handles text such as '2 and 3/4'. Note that "one half" or
    similar will be parsed by the whole number function.

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
                _extract_numbers_with_text_cs(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_cs(partitions[2], short_scale,
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


def _extract_decimal_with_text_cs(tokens, short_scale, ordinals):
    """
    Extract decimal numbers from a string.

    This function handles text such as '2 point 5'.

    Notes:
        While this is a helper for extract_number_xx, it also depends on
        extract_number_xx, to parse out the components of the decimal.

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
                _extract_numbers_with_text_cs(partitions[0], short_scale,
                                              ordinals, fractional_numbers=False)
            numbers2 = \
                _extract_numbers_with_text_cs(partitions[2], short_scale,
                                              ordinals, fractional_numbers=False)

            if not numbers1 or not numbers2:
                return None, None

            number = numbers1[-1]
            decimal = numbers2[0]

            # TODO handle number dot number number number
            if "." not in str(decimal.text):
                return number.value + float('0.' + str(decimal.value)), \
                       number.tokens + partitions[1] + decimal.tokens
    return None, None


def _extract_whole_number_with_text_cs(tokens, short_scale, ordinals):
    """
    Handle numbers not handled by the decimal or fraction functions. This is
    generally whole numbers. Note that phrases such as "one half" will be
    handled by this function, while "one and a half" are handled by the
    fraction function.

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
        # if word in _ARTICLES_CS or word in _NEGATIVES:
        if word in word in _NEGATIVES:
            number_words.append(token)
            continue

        prev_word = tokens[idx - 1].word if idx > 0 else ""
        next_word = tokens[idx + 1].word if idx + 1 < len(tokens) else ""

        # In czech we do no use suffix (1st,2nd,..) but use point instead (1.,2.,..)
        if is_numeric(word[:-1]) and \
                (word.endswith(".")):
            # explicit ordinals, 1st, 2nd, 3rd, 4th.... Nth
            word = word[:-1]

            # handle nth one
        #    if next_word == "one":
        # would return 1 instead otherwise
        #        tokens[idx + 1] = Token("", idx)
        #        next_word = ""

        # Normalize Czech inflection of numbers(jedna,jeden,jedno,...)
        if not ordinals:
            word = _text_cs_inflection_normalize(word, 1)

        if word not in string_num_scale and \
                word not in _STRING_NUM_CS and \
                word not in _SUMS and \
                word not in multiplies and \
                not (ordinals and word in string_num_ordinal) and \
                not is_numeric(word) and \
                not is_fractional_cs(word, short_scale=short_scale) and \
                not look_for_fractions(word.split('/')):
            words_only = [token.word for token in number_words]
            # if number_words and not all([w in _ARTICLES_CS |
            #                             _NEGATIVES for w in words_only]):
            if number_words and not all([w in _NEGATIVES for w in words_only]):
                break
            else:
                number_words = []
                continue
        elif word not in multiplies \
                and prev_word not in multiplies \
                and prev_word not in _SUMS \
                and not (ordinals and prev_word in string_num_ordinal) \
                and prev_word not in _NEGATIVES:  # \
            # and prev_word not in _ARTICLES_CS:
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
        if word in _STRING_NUM_CS:
            val = _STRING_NUM_CS.get(word)
            current_val = val
        elif word in string_num_scale:
            val = string_num_scale.get(word)
            current_val = val
        elif ordinals and word in string_num_ordinal:
            val = string_num_ordinal[word]
            current_val = val

        # is the prev word an ordinal number and current word is one?
        # second one, third one
        if ordinals and prev_word in string_num_ordinal and val == 1:
            val = prev_val

        # is the prev word a number and should we sum it?
        # twenty two, fifty six
        if (prev_word in _SUMS and val and val < 10) or all([prev_word in
                                                             multiplies,
                                                             val < prev_val if prev_val else False]):
            val = prev_val + val

        # For Czech only: If Ordinal previous number will be also in ordinal number format
        # dvacátý první = twentieth first
        if (prev_word in string_num_ordinal and val and val < 10) or all([prev_word in
                                                                          multiplies,
                                                                          val < prev_val if prev_val else False]):
            val = prev_val + val

        # is the prev word a number and should we multiply it?
        # twenty hundred, six hundred
        if word in multiplies:
            if not prev_val:
                prev_val = 1
            val = prev_val * val

        # is this a spoken fraction?
        # half cup
        if val is False:
            val = is_fractional_cs(word, short_scale=short_scale)
            current_val = val

        # 2 fifths
        if not ordinals:
            next_val = is_fractional_cs(next_word, short_scale=short_scale)
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
            aPieces = word.split('/')
            if look_for_fractions(aPieces):
                val = float(aPieces[0]) / float(aPieces[1])
                current_val = val

        else:
            if all([
                prev_word in _SUMS,
                word not in _SUMS,
                word not in multiplies,
                current_val >= 10]):
                # Backtrack - we've got numbers we can't sum.
                number_words.pop()
                val = prev_val
                break
            prev_val = val

            if word in multiplies and next_word not in multiplies:
                # handle long numbers
                # six hundred sixty six
                # two million five hundred thousand
                #
                # This logic is somewhat complex, and warrants
                # extensive documentation for the next coder's sake.
                #
                # The current word is a power of ten. `current_val` is
                # its integer value. `val` is our working sum
                # (above, when `current_val` is 1 million, `val` is
                # 2 million.)
                #
                # We have a dict `string_num_scale` containing [value, word]
                # pairs for "all" powers of ten: string_num_scale[10] == "ten.
                #
                # We need go over the rest of the tokens, looking for other
                # powers of ten. If we find one, we compare it with the current
                # value, to see if it's smaller than the current power of ten.
                #
                # Numbers which are not powers of ten will be passed over.
                #
                # If all the remaining powers of ten are smaller than our
                # current value, we can set the current value aside for later,
                # and begin extracting another portion of our final result.
                # For example, suppose we have the following string.
                # The current word is "million".`val` is 9000000.
                # `current_val` is 1000000.
                #
                #    "nine **million** nine *hundred* seven **thousand**
                #     six *hundred* fifty seven"
                #
                # Iterating over the rest of the string, the current
                # value is larger than all remaining powers of ten.
                #
                # The if statement passes, and nine million (9000000)
                # is appended to `to_sum`.
                #
                # The main variables are reset, and the main loop begins
                # assembling another number, which will also be appended
                # under the same conditions.
                #
                # By the end of the main loop, to_sum will be a list of each
                # "place" from 100 up: [9000000, 907000, 600]
                #
                # The final three digits will be added to the sum of that list
                # at the end of the main loop, to produce the extracted number:
                #
                #    sum([9000000, 907000, 600]) + 57
                # == 9,000,000 + 907,000 + 600 + 57
                # == 9,907,657
                #
                # >>> foo = "nine million nine hundred seven thousand six
                #            hundred fifty seven"
                # >>> extract_number(foo)
                # 9907657

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
    Generate dictionaries of words to numbers, based on scale.

    This is a helper function for _extract_whole_number.

    Args:
        short_scale boolean:

    Returns:
        (set(str), dict(str, number), dict(str, number))
        multiplies, string_num_ordinal, string_num_scale

    """
    multiplies = _MULTIPLIES_SHORT_SCALE_CS if short_scale \
        else _MULTIPLIES_LONG_SCALE_CS

    string_num_ordinal_cs = _STRING_SHORT_ORDINAL_CS if short_scale \
        else _STRING_LONG_ORDINAL_CS

    string_num_scale_cs = _SHORT_SCALE_CS if short_scale else _LONG_SCALE_CS
    string_num_scale_cs = invert_dict(string_num_scale_cs)
    string_num_scale_cs.update(generate_plurals_cs(string_num_scale_cs))
    return multiplies, string_num_ordinal_cs, string_num_scale_cs


def extract_number_cs(text, short_scale=True, ordinals=False):
    """
    This function extracts a number from a text string,
    handles pronunciations in long scale and short scale

    https://en.wikipedia.org/wiki/Names_of_large_numbers

    Args:
        text (str): the string to normalize
        short_scale (bool): use short scale if True, long scale if False
        ordinals (bool): consider ordinal numbers, third=3 instead of 1/3
    Returns:
        (int) or (float) or False: The extracted number or False if no number
                                   was found

    """
    return _extract_number_with_text_cs(tokenize(text.lower()),
                                        short_scale, ordinals).value


def is_fractional_cs(input_str, short_scale=True):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.endswith('iny', -3):  # leading number is bigger than one ( one třetina, two třetiny)
        # Normalize to format of one (třetiny > třetina)
        input_str = input_str[:len(input_str) - 1] + "a"

    fracts = {"celá": 1}  # first four numbers have little different format

    for num in _FRACTION_STRING_CS:  # Numbers from 2 to 1 hundret, more is not usualy used in common speech
        if num > 1:
            fracts[_FRACTION_STRING_CS[num]] = num

    if input_str.lower() in fracts:
        return 1.0 / fracts[input_str.lower()]
    return False


def _text_cs_inflection_normalize(word, arg):
    """
    Czech Inflection normalizer.

    This try to normalize known inflection. This function is called
    from multiple places, each one is defined with arg.

    Args:
        word [Word]
        arg [Int]

    Returns:
        word [Word]

    """
    if arg == 1:  # _extract_whole_number_with_text_cs
        # Number one (jedna)
        if len(word) == 5 and word.startswith("jed"):
            suffix = 'en', 'no', 'ny'
            if word.endswith(suffix, 3):
                word = "jedna"

        # Number two (dva)
        elif word == "dvě":
            word = "dva"

    elif arg == 2:  # extract_datetime_cs  TODO: This is ugly
        if word == "hodina":
            word = "hodin"
        if word == "hodiny":
            word = "hodin"
        if word == "hodinu":
            word = "hodin"
        if word == "minuta":
            word = "minut"
        if word == "minuty":
            word = "minut"
        if word == "minutu":
            word = "minut"
        if word == "minutu":
            word = "minut"
        if word == "sekunda":
            word = "sekund"
        if word == "sekundy":
            word = "sekund"
        if word == "sekundu":
            word = "sekund"
        if word == "dní":
            word = "den"
        if word == "dnů":
            word = "den"
        if word == "dny":
            word = "den"
        if word == "týdny":
            word = "týden"
        if word == "týdnů":
            word = "týden"
        if word == "měsíců":
            word = "měsíc"
        if word == "měsíce":
            word = "měsíc"
        if word == "měsíci":
            word = "měsíc"
        if word == "roky":
            word = "rok"
        if word == "roků":
            word = "rok"
        if word == "let":
            word = "rok"
        if word == "včerejšku":
            word = "včera"
        if word == "zítřku":
            word = "zítra"
        if word == "zítřejší":
            word = "zítra"
        if word == "ranní":
            word = "ráno"
        if word == "dopolední":
            word = "dopoledne"
        if word == "polední":
            word = "poledne"
        if word == "odpolední":
            word = "odpoledne"
        if word == "večerní":
            word = "večer"
        if word == "noční":
            word = "noc"
        if word == "víkendech":
            word = "víkend"
        if word == "víkendu":
            word = "víkend"
        if word == "všedních":
            word = "všední"
        if word == "všedním":
            word = "všední"

        # Months
        if word == "únoru":
            word = "únor"
        elif word == "červenci":
            word = "červenec"
        elif word == "července":
            word = "červenec"
        elif word == "listopadu":
            word = "listopad"
        elif word == "prosinci":
            word = "prosinec"

    return word


def nice_number_cs(number, speech=True, denominators=range(1, 21)):
    """ English helper for nice_number

    This function formats a float to human understandable functions. Like
    4.5 becomes "4 and a half" for speech and "4 1/2" for text

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
            # TODO: Number grouping?  E.g. "1,000,000"
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)

    if num == 0:
        return str(whole)
    den_str = _FRACTION_STRING_CS[den]
    if whole == 0:
        if num == 1:
            return_string = '{}'.format(den_str)
        else:
            return_string = '{} {}'.format(num, den_str)
    elif num == 1:
        return_string = '{} a {}'.format(whole, den_str)
    else:
        return_string = '{} a {} {}'.format(whole, num, den_str)
    if num > 4:
        return_string = return_string[:-1]
    elif num > 1:
        return_string = return_string[:-1] + 'y'

    return return_string


def pronounce_number_cs(number, places=2, short_scale=True, scientific=False,
                        ordinals=False):
    """
    Convert a number to it's spoken equivalent

    For example, '5.2' would return 'five point two'

    Args:
        num(float or int): the number to pronounce (under 100)
        places(int): maximum decimal places to speak
        short_scale (bool) : use short (True) or long scale (False)
            https://en.wikipedia.org/wiki/Names_of_large_numbers
        scientific (bool): pronounce in scientific notation
        ordinals (bool): pronounce in ordinal form "first" instead of "one"
    Returns:
        (str): The pronounced number
    """
    num = number
    # deal with infinity
    if num == float("inf"):
        return "nekonečno"
    elif num == float("-inf"):
        return "záporné nekonečno"
    if scientific:
        number = '%E' % num
        n, power = number.replace("+", "").split("E")
        power = int(power)
        if power != 0:
            if ordinals:
                # This handles zápornés of powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} krát deset k {}{} mocnině'.format(
                    'záporné ' if float(n) < 0 else '',
                    pronounce_number_cs(
                        abs(float(n)), places, short_scale, False, ordinals=False),
                    'záporné ' if power < 0 else '',
                    pronounce_number_cs(abs(power), places, short_scale, False, ordinals=True))
            else:
                # This handles zápornés of powers separately from the normal
                # handling since each call disables the scientific flag
                return '{}{} krát deset na mocninu {}{}'.format(
                    'záporné ' if float(n) < 0 else '',
                    pronounce_number_cs(
                        abs(float(n)), places, short_scale, False),
                    'záporné ' if power < 0 else '',
                    pronounce_number_cs(abs(power), places, short_scale, False))

    if short_scale:
        number_names = _NUM_STRING_CS.copy()
        number_names.update(_SHORT_SCALE_CS)
    else:
        number_names = _NUM_STRING_CS.copy()
        number_names.update(_LONG_SCALE_CS)

    digits = [number_names[n] for n in range(0, 20)]

    tens = [number_names[n] for n in range(10, 100, 10)]

    if short_scale:
        hundreds = [_SHORT_SCALE_CS[n] for n in _SHORT_SCALE_CS.keys()]
    else:
        hundreds = [_LONG_SCALE_CS[n] for n in _LONG_SCALE_CS.keys()]

    # deal with zápornés
    result = ""
    if num < 0:
        result = "záporné " if scientific else "mínus "
    num = abs(num)

    if not ordinals:
        try:
            # deal with 4 digits
            # usually if it's a 4 digit num it should be said like a date
            # i.e. 1972 => nineteen seventy two
            if len(str(num)) == 4 and isinstance(num, int):
                _num = str(num)
                # deal with 1000, 2000, 2001, 2100, 3123, etc
                # is skipped as the rest of the
                # functin deals with this already
                if _num[1:4] == '000' or _num[1:3] == '00' or int(_num[0:2]) >= 20:
                    pass
                # deal with 1900, 1300, etc
                # i.e. 1900 => nineteen hundred
                elif _num[2:4] == '00':
                    first = number_names[int(_num[0:2])]
                    last = number_names[100]
                    return first + " " + last
                # deal with 1960, 1961, etc
                # i.e. 1960 => nineteen sixty
                #      1961 => nineteen sixty one
                else:
                    first = number_names[int(_num[0:2])]
                    if _num[3:4] == '0':
                        last = number_names[int(_num[2:4])]
                    else:
                        second = number_names[int(_num[2:3]) * 10]
                        last = second + " " + number_names[int(_num[3:4])]
                    return first + " " + last
        # exception used to catch any unforseen edge cases
        # will default back to normal subroutine
        except Exception as e:
            # TODO this probably shouldn't go to stdout
            print('ERROR: Exception in pronounce_number_cs: {}' + repr(e))

    # check for a direct match
    if num in number_names and not ordinals:
        if num > 90:
            result += "jedna "
        result += number_names[num]
    else:
        def _sub_thousand(n, ordinals=False):
            assert 0 <= n <= 999
            if n in _SHORT_ORDINAL_CS and ordinals:
                return _SHORT_ORDINAL_CS[n]
            if n <= 19:
                return digits[n]
            elif n <= 99:
                q, r = divmod(n, 10)
                return tens[q - 1] + (" " + _sub_thousand(r, ordinals) if r
                                      else "")
            else:
                q, r = divmod(n, 100)
                return digits[q] + " sto" + (
                    " a " + _sub_thousand(r, ordinals) if r else "")

        def _short_scale(n):
            if n >= max(_SHORT_SCALE_CS.keys()):
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

                        if i * 1000 in _SHORT_ORDINAL_CS:
                            if z == 1:
                                number = _SHORT_ORDINAL_CS[i * 1000]
                            else:
                                number += _SHORT_ORDINAL_CS[i * 1000]
                        else:
                            if n not in _SHORT_SCALE_CS:
                                num = int("1" + "0" * (len(str(n)) - 2))

                                number += _SHORT_SCALE_CS[num] + "tý"
                            else:
                                number = _SHORT_SCALE_CS[n] + "tý"
                    else:
                        number += hundreds[i]
                res.append(number)
                ordi = False

            return ", ".join(reversed(res))

        def _split_by(n, split=1000):
            assert 0 <= n
            res = []
            while n:
                n, r = divmod(n, split)
                res.append(r)
            return res

        def _long_scale(n):
            if n >= max(_LONG_SCALE_CS.keys()):
                return "nekonečno"
            ordi = ordinals
            if int(n) != n:
                ordi = False
            n = int(n)
            assert 0 <= n
            res = []
            for i, z in enumerate(_split_by(n, 1000000)):
                if not z:
                    continue
                number = pronounce_number_cs(z, places, True, scientific,
                                             ordinals=ordi and not i)
                # strip off the comma after the thousand
                if i:
                    if i >= len(hundreds):
                        return ""
                    # plus one as we skip 'thousand'
                    # (and 'hundred', but this is excluded by index value)
                    number = number.replace(',', '')

                    if ordi:
                        if i * 1000000 in _LONG_ORDINAL_CS:
                            if z == 1:
                                number = _LONG_ORDINAL_CS[
                                    (i + 1) * 1000000]
                            else:
                                number += _LONG_ORDINAL_CS[
                                    (i + 1) * 1000000]
                        else:
                            if n not in _LONG_SCALE_CS:
                                num = int("1" + "0" * (len(str(n)) - 2))

                                number += " " + _LONG_SCALE_CS[
                                    num] + "tý"
                            else:
                                number = " " + _LONG_SCALE_CS[n] + "tý"
                    else:

                        number += " " + hundreds[i + 1]
                res.append(number)
            return ", ".join(reversed(res))

        if short_scale:
            result += _short_scale(num)
        else:
            result += _long_scale(num)

    # deal with scientific notation unpronounceable as number
    if not result and "e" in str(num):
        return pronounce_number_cs(num, places, short_scale, scientific=True)
    # Deal with fractional part
    elif not num == int(num) and places > 0:
        if abs(num) < 1.0 and (result == "mínus " or not result):
            result += "nula"
        result += " tečka"
        _num_str = str(num)
        _num_str = _num_str.split(".")[1][0:places]
        for char in _num_str:
            result += " " + number_names[int(char)]
    return result
